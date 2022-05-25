---
title: TiCDC Avro Protocol
summary: Learn the concept of TiCDC Avro Protocol and how to use it.
---

# TiCDC Avro Protocol

Avro is a data exchange format protocol defined by [Apache Avro™](https://avro.apache.org/) and chosen by [Confluent Platform](https://docs.confluent.io/platform/current/platform.html) as the default data exchange format. This document describes the implementation of the Avro data format in TiCDC, including TiDB extension fields, definition of the Avro data format, and the interaction between Avro and [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html).

## Use Avro

When using Message Queue (MQ) as downstream sink, you can specify Avro in `sink-uri`. TiCDC wraps Avro Messages with events as the basic unit and sends TiDB DML events downstream. When Avro detects a schema change, it registers the latest schema with Schema Registry.

The following is a configuration example using Avro:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro" --schema-registry=http://127.0.0.1:8081
```

The value of `--schema-registry` supports the https protocol and `username:password` authentication, for example, `--schema-registry=https://username:password@schema-registry-uri.com`. The username and password must be URL-encoded.

## TiDB extension fields

By default, Avro only includes data of the row where data changes in the DML event, excluding the type of data change or unique identifiers of TiDB-specific CommitTS  transactions. To address this issue, TiCDC introduces the following three TiDB extension fields to the Avro protocol. When `enable-tidb-extension` is set to `true` (defaults to `false`) in `sink-uri`, TiCDC generates Avro messages with these three fields:

- `_tidb_op`: The DML type. "c" indicates insert and "u" indicates updates.
- `_tidb_commit_ts`: The unique identifier of a transaction.
- `_tidb_commit_physical_time`: The physical timestamp in a transaction identifier.

The following is a configuration example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081
```

## Definition of the data format

TiCDC converts a DML event into a Kafka event, and the Key and value of an event are encoded according to the Avro protocol.

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
- `{{Namespace}}` is a combination of the changefeed namespace and the schema name of the data source.
- `{{ColumnValueBlock}}` defines the format of each row of data.

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

The data format of Value is the same as that of Key, by default. However, `fields` in the Value contains all columns, not just the primary key columns.

After you enable `enable-tidb-extension`, the data format of the Value will be as follows:

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

If one row can be NULL, the Column data format can be:

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
- `{{AVRO_TYPE}}` indicates the type in [avro spec](https://avro.apache.org/docs/current/spec.html).

| SQL TYPE   | TIDB_TYPE | AVRO_TYPE | Description                                                                                                               |
|------------|-----------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| BOOL       | INT       | int       |                                                                                                                           |
| TINYINT    | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| SMALLINT   | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| MEDIUMINT  | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED.                                                                            |
| INT        | INT       | int       | When it's unsigned, TIDB_TYPE is INT UNSIGNED and AVRO_TYPE is long.                                                      |
| BIGINT     | BIGINT    | long      | When it's unsigned, TIDB_TYPE is BIGINT UNSIGNED. If `avro-bigint-unsigned-handling-mode` is string, AVRO_TYPE is string. |
| TINYBLOB   | BLOB      | bytes     |                                                                                                                           |
| BLOB       | BLOB      | bytes     |                                                                                                                           |
| MEDIUMBLOB | BLOB      | bytes     |                                                                                                                           |
| LONGBLOB   | BLOB      | bytes     |                                                                                                                           |
| BINARY     | BLOB      | bytes     |                                                                                                                           |
| VARBINARY  | BLOB      | bytes     |                                                                                                                           |
| TINYTEXT   | TEXT      | string    |                                                                                                                           |
| TEXT       | TEXT      | string    |                                                                                                                           |
| MEDIUMTEXT | TEXT      | string    |                                                                                                                           |
| LONGTEXT   | TEXT      | string    |                                                                                                                           |
| CHAR       | TEXT      | string    |                                                                                                                           |
| VARCHAR    | TEXT      | string    |                                                                                                                           |
| FLOAT      | FLOAT     | double    |                                                                                                                           |
| DOUBLE     | DOUBLE    | double    |                                                                                                                           |
| DATE       | DATE      | string    |                                                                                                                           |
| DATETIME   | DATETIME  | string    |                                                                                                                           |
| TIMESTAMP  | TIMESTAMP | string    |                                                                                                                           |
| TIME       | TIME      | string    |                                                                                                                           |
| YEAR       | YEAR      | int       |                                                                                                                           |
| BIT        | BIT       | bytes     |                                                                                                                           |
| JSON       | JSON      | string    |                                                                                                                           |
| ENUM       | ENUM      | string    |                                                                                                                           |
| SET        | SET       | string    |                                                                                                                           |
| DECIMAL    | DECIMAL   | bytes     | When `avro-decimal-handling-mode` is string, AVRO_TYPE is string.                                                         |

In the Avro protocol, there are two other `sink-uri` parameters that affect the Column data format: `avro-decimal-handling-mode` and `avro-bigint-unsigned-handling-mode`.

- `avro-decimal-handling-mode` controls how Avro handles decimal fields, including:

    - string: Avro handles decimal fields as strings.
    - precise：Avro stores decimal fields as bytes.

- `avro-bigint-unsigned-handling-mode` controls how Avro handles BIGINT UNSIGNED fields, including:

    - string: Avro handles BIGINT UNSIGNED fields as strings.
    - long: Avro handles BIGINT UNSIGNED fields as 64-bit signed integers, which might result in overflow.

The following is a configuration example:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081
```

Most SQL Types are mapped to the base Column data format. Some other SQL types are expanded on the base data format to provide more information.

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

Avro does not generate DDL events downstream. It checks whether a schema changes at each DML event. If a schema changes, Avro generates a new schema and registers it with the Schema Registry. If the schema change does not pass the compatibility check, the registration fails. Avro does not resolve any schema compatibility issues.

Note that, even if the compatibility check is passed and the registration succeeds, Avro producers and consumers still need to perform an upgrade to ensure normal running of the system.

Assume that the default compatibility policy of Confluent Schema Registry is `BACKWARD` and add a non-empty column to the source table. In this condition, Avro will fail to generate a new schema and register it with Schema Registry due to compatibility issues. At this time, the changefeed is displayed as erroneous.

For more information about schemas, refer to [Schema Registry related materials](https://docs.confluent.io/platform/current/schema-registry/avro.html).

## Topic distribution

Schema Registry supports three [Subject Name Strategies](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy). Currently, TiCDC Avro only supports TopicNameStrategy, which means that a Kafka topic can only receive data in one data format. Therefore, TiCDC Avro prohibits mapping multiple tables to the same topic. When creating a changefeed, an error will be reported if the topic rule does not include the `{schema}` and `{table}` placeholders in the configured distribution rule.
