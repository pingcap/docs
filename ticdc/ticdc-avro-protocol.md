---
title: TiCDC Avro Protocol
summary: Learn the concept of TiCDC Avro Protocol and how to use it.
---

# TiCDC Avro Protocol

TiCDC Avro protocol is a third-party implementation of the [Confluent Avro](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html) data exchange protocol defined by [Confluent Platform](https://docs.confluent.io/platform/current/platform.html). Avro is a data format defined by [Apache Avro™](https://avro.apache.org/)

This document describes how TiCDC implements the Confluent Avro protocol, and the interaction between Avro and [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html).

> **Warning:**
>
> Starting from v7.3.0, if you enable TiCDC to [replicate tables without a valid index](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index), TiCDC will report an error when you create a changefeed that uses the Avro protocol.

## Use Avro

The following is a configuration example using Avro:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

The value of `--schema-registry` supports the `https` protocol and `username:password` authentication. The username and password must be URL-encoded. For example, `--schema-registry=https://username:password@schema-registry-uri.com`.

> **Note：**
> 
> When using the Avro protocol, one Kafka topic can only contain data for one table. You need to configure the [Topic dispatcher](/ticdc/ticdc-sink-to-kafka.md#topic-dispatchers) in the configuration file. 

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

## Definition of the data format

TiCDC converts a DML event into a Kafka event, and the Key and Value of an event are encoded according to the Avro protocol.

### Key data format

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

- `{{TableName}}` indicates the name of the table where the event occurs.
- `{{Namespace}}` is the namespace of Avro.
- `{{ColumnValueBlock}}` defines the format of each column of data.

The `fields` in the key contains only primary key columns or unique index columns.

### Value data format

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

The data format of Value is the same as that of Key, by default. However, `fields` in the Value contains all columns.

> **Note:**
>
> The Avro protocol encodes DML events as follows: 
> 
> - For Delete events, Avro only encodes the Key part. The Value part is empty. 
> - For Insert events, Avro encodes all column data to the Value part. 
> - For Update events, Avro encodes only all column data that is updated to the Value part.

## TiDB extension fields

By default, Avro only collects data of changed rows in DML events and does not collect the type of data changes or TiDB-specific CommitTS (the unique identifiers of transactions). To address this issue, TiCDC introduces the following three TiDB extension fields to the Avro protocol message. When `enable-tidb-extension` is set to `true` (`false` by default) in `sink-uri`, TiCDC adds these three fields to the Avro messages during message generation.

- `_tidb_op`: The DML type. "c" indicates insert and "u" indicates updates.
- `_tidb_commit_ts`: The unique identifier of a transaction.
- `_tidb_commit_physical_time`: The physical timestamp in a transaction identifier.

The following is a configuration example:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

After you enable [`enable-tidb-extension`](#tidb-extension-fields), the data format of the Value will be as follows:

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
        {
            "name":"_tidb_op",
            "type":"string"
        },
        {
            "name":"_tidb_commit_ts",
            "type":"long"
        },
        {
            "name":"_tidb_commit_physical_time",
            "type":"long"
        }
    ]
}
```

Compared with the Value data format with `enable-tidb-extension` disabled, three new fields are added: `_tidb_op`, `_tidb_commit_ts`, and `_tidb_commit_physical_time`.

### Column data format

The Column data is the `{{ColumnValueBlock}}` part of the Key/Value data format. TiCDC generates the Column data format based on the SQL Type. The basic Column data format is as follows:

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"{{TIDB_TYPE}}"
        },
        "type":"{{AVRO_TYPE}}"
    }
}
```

If one column can be NULL, the Column data format can be:

```
{
    "default":null,
    "name":"{{ColumnName}}",
    "type":[
        "null",
        {
            "connect.parameters":{
                "tidb_type":"{{TIDB_TYPE}}"
            },
            "type":"{{AVRO_TYPE}}"
        }
    ]
}
```

- `{{ColumnName}}` indicates the column name.
- `{{TIDB_TYPE}}` indicates the type in TiDB, which is not a one-to-one mapping with the SQL type.
- `{{AVRO_TYPE}}` indicates the type in the [Avro Specification](https://avro.apache.org/docs/++version++/specification).

| SQL TYPE   | TIDB_TYPE | AVRO_TYPE | Description                                                                                                               |
|------------|-----------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| BOOL       | INT       | int       |                                                                                                                           |
| TINYINT    | INT       | int       | When it is unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| SMALLINT   | INT       | int       | When it is unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| MEDIUMINT  | INT       | int       | When it is unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| INT        | INT       | int       | When it is unsigned, TIDB_TYPE is INT UNSIGNED and AVRO_TYPE is long.                                                      |
| BIGINT     | BIGINT    | long      | When it is unsigned, TIDB_TYPE is BIGINT UNSIGNED. If `avro-bigint-unsigned-handling-mode` is string, AVRO_TYPE is string. |
| TINYBLOB   | BLOB      | bytes     |  -                                                                                                                         |
| BLOB       | BLOB      | bytes     |  -                                                                                                                         |
| MEDIUMBLOB | BLOB      | bytes     |  -                                                                                                                         |
| LONGBLOB   | BLOB      | bytes     |  -                                                                                                                         |
| BINARY     | BLOB      | bytes     |  -                                                                                                                        |
| VARBINARY  | BLOB      | bytes     |  -                                                                                                                        |
| TINYTEXT   | TEXT      | string    |  -                                                                                                                        |
| TEXT       | TEXT      | string    |  -                                                                                                                        |
| MEDIUMTEXT | TEXT      | string    |  -                                                                                                                        |
| LONGTEXT   | TEXT      | string    |  -                                                                                                                         |
| CHAR       | TEXT      | string    |  -                                                                                                                         |
| VARCHAR    | TEXT      | string    |  -                                                                                                                         |
| FLOAT      | FLOAT     | double    |  -                                                                                                                         |
| DOUBLE     | DOUBLE    | double    |  -                                                                                                                         |
| DATE       | DATE      | string    |  -                                                                                                                         |
| DATETIME   | DATETIME  | string    |  -                                                                                                                         |
| TIMESTAMP  | TIMESTAMP | string    |  -                                                                                                                         |
| TIME       | TIME      | string    |  -                                                                                                                         |
| YEAR       | YEAR      | int       |  -                                                                                                                         |
| BIT        | BIT       | bytes     |  -                                                                                                                         |
| JSON       | JSON      | string    |  -                                                                                                                         |
| ENUM       | ENUM      | string    |  -                                                                                                                         |
| SET        | SET       | string    |  -                                                                                                                         |
| DECIMAL    | DECIMAL   | bytes     | When `avro-decimal-handling-mode` is string, AVRO_TYPE is string.                                                         |

In the Avro protocol, two other `sink-uri` parameters might affect the Column data format as well: `avro-decimal-handling-mode` and `avro-bigint-unsigned-handling-mode`.

- `avro-decimal-handling-mode` controls how Avro handles decimal fields, including:

    - string: Avro handles decimal fields as strings.
    - precise: Avro handles decimal fields as bytes.

- `avro-bigint-unsigned-handling-mode` controls how Avro handles BIGINT UNSIGNED fields, including:

    - string: Avro handles BIGINT UNSIGNED fields as strings.
    - long: Avro handles BIGINT UNSIGNED fields as 64-bit signed integers. When the value is greater than `9223372036854775807`, overflow will occur.

The following is a configuration example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

Most SQL types are mapped to the base Column data format. Some other SQL types extend the base data format to provide more information.

BIT(64)

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"BIT",
            "length":"64"
        },
        "type":"bytes"
    }
}
```

ENUM/SET(a,b,c)

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"ENUM/SET",
            "allowed":"a,b,c"
        },
        "type":"string"
    }
}
```

DECIMAL(10, 4)

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"DECIMAL",
        },
        "logicalType":"decimal",
        "precision":10,
        "scale":4,
        "type":"bytes"
    }
}
```

## DDL events and schema changes

Avro does not send DDL events and Watermark events to downstream. It checks whether a schema changes each time a DML event occurs. If a schema changes, Avro generates a new schema and registers it with the Schema Registry. If the schema change does not pass the compatibility check, the registration fails. TiCDC does not resolve any schema compatibility issues.

For example, the default [compatibility policy](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html#compatibility-types) of Confluent Schema Registry is `BACKWARD`, and you add a non-empty column to the source table. In this situation, Avro generates a new schema but fails to register it with Schema Registry due to compatibility issues. At this time, the changefeed enters an error state.

Note that, even if a schema change passes the compatibility check and a new version is registered, the data producers and consumers still need to acquire the new schema for data encoding and decoding.

For more information about schemas, refer to [Schema Registry related documents](https://docs.confluent.io/platform/current/schema-registry/avro.html).

## Consumer implementation

The TiCDC Avro protocol can be deserialized by [`io.confluent.kafka.serializers.KafkaAvroDeserializer`](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html#avro-deserializer).

The consumer program can acquire the latest schema via [Schema Registry API](https://docs.confluent.io/platform/current/schema-registry/develop/api.html), and then use the schema to deserialize the data encoded by the TiCDC Avro protocol.

### Distinguish event types

The consumer program can distinguish DML event types by the following rules:

* If there is only the Key part, it is a Delete event.
* If there are both Key and Value parts, it is either an Insert or an Update event. If the [TiDB extension fields](#tidb-extension-fields) are enabled, you can use the `_tidb_op` field to identify if it is an Insert or Update event. If the TiDB extension fields are not enabled, you cannot distinguish them.

## Topic distribution

Schema Registry supports three [Subject Name Strategies](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy): TopicNameStrategy, RecordNameStrategy, and TopicRecordNameStrategy. Currently, TiCDC Avro only supports TopicNameStrategy, which means that a Kafka topic can only receive data in one data format. Therefore, TiCDC Avro prohibits mapping multiple tables to the same topic. When you create a changefeed, an error will be reported if the topic rule does not include the `{schema}` and `{table}` placeholders in the configured distribution rule.

## Compatibility

When upgrading the TiCDC cluster to v7.0.0, if a table replicated using Avro contains the `FLOAT` data type, you need to manually adjust the compatibility policy of Confluent Schema Registry to `None` before upgrading so that the changefeed can successfully update the schema. Otherwise, after upgrading, the changefeed will be unable to update the schema and enter an error state. For more information, see [#8490](https://github.com/pingcap/tiflow/issues/8490).
