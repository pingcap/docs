---
title: TiCDC Debezium Protocol
summary: Learn the concept of the TiCDC Debezium Protocol and how to use it.
---

# TiCDC Debezium Protocol

[Debezium](https://debezium.io/) is a tool for capturing database changes. It converts each captured database change into a message called an "event" and sends these events to Kafka. Starting from v8.0.0, TiCDC supports sending TiDB changes to Kafka using a Debezium style output format, simplifying migration from MySQL databases for users who had previously been using Debezium's MySQL integration. Starting from v9.0.0, TiCDC supports DDL events and WATERMARK events.

## Use the Debezium message format

When you use Kafka as the downstream sink, specify the `protocol` field as `debezium` in `sink-uri` configuration. Then TiCDC encapsulates the Debezium messages based on the events and sends TiDB data change events to the downstream.

The Debezium protocol supports the following types of events:

- DDL event: represents a DDL change record. After the upstream DDL statement is successfully executed, the DDL event is sent to every Message Queue (MQ) partition.

- DML event: represents a row data change record. The DML event is sent when a row change occurs. It contains the information about the row after the change occurs.

- WATERMARK event: represents a special point in time. It indicates that the events received before this point are complete. The WATERMARK event applies only to the TiDB extension field and takes effect when you set [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) to `true` in `sink-uri`.

The configuration example for using the Debezium message format is as follows:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

The Debezium output format contains the schema information of the current row so that downstream consumers can better understand the data structure of the current row. For scenarios where schema information is unnecessary, you can also disable the schema output by setting the `debezium-disable-schema` parameter to `true` in the changefeed configuration file or `sink-uri`.

In addition, the original Debezium format does not include important fields such as the unique transaction identifier of the `CommitTS` in TiDB. To ensure data integrity, TiCDC adds two fields, `CommitTs` and `ClusterID`, to the Debezium format to identify the relevant information of TiDB data changes.

## Message format definition

This section describes the message formats of DDL events, DML events and WATERMARK events.

### DDL event

TiCDC encodes a DDL event into a Kafka message, with both the key and value encoded in the Debezium format.

#### Key format

```json
{
    "payload": {
        "databaseName": "test"
    },
    "schema": {
        "type": "struct",
        "name": "io.debezium.connector.mysql.SchemaChangeKey",
        "optional": false,
        "version": 1,
        "fields": [
            {
                "field": "databaseName",
                "optional": false,
                "type": "string"
            }
        ]
    }
}
```

The fields in the key only include the database name. The fields are explained as follows:

| Field            | Type    | Description                                         |
|:------------------|:--------|:------------------------------------------------|
| `payload`        | JSON    | The information about database name. |
| `schema.fields`  | JSON    | The type information of each field in the payload. |
| `schema.type`    | String  | The data type of the field.                                      |
| `schema.optional` | Boolean | Indicates whether the field is optional. When it is `true`, the field is optional.  |
| `schema.version`   | String  | The schema version.                                 |

#### Value format

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "test",
            "table": "table1",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 1,
            "cluster_id": "test_cluster"
        },
        "ts_ms": 1701326309000,
        "databaseName": "test",
        "schemaName": null,
        "ddl": "RENAME TABLE test.table1 to test.table2",
        "tableChanges": [
            {
                "type": "ALTER",
                "id": "\"test\".\"table2\",\"test\".\"table1\"",
                "table": {
                    "defaultCharsetName": "",
                    "primaryKeyColumnNames": [
                        "id"
                    ],
                    "columns": [
                        {
                            "name": "id",
                            "jdbcType": 4,
                            "nativeType": null,
                            "comment": null,
                            "defaultValueExpression": null,
                            "enumValues": null,
                            "typeName": "INT",
                            "typeExpression": "INT",
                            "charsetName": null,
                            "length": 0,
                            "scale": null,
                            "position": 1,
                            "optional": false,
                            "autoIncremented": false,
                            "generated": false
                        }
                    ],
                    "comment": null
                }
            }
        ]
    },
    "schema": {
        "optional": false,
        "type": "struct",
        "version": 1,
        "name": "io.debezium.connector.mysql.SchemaChangeValue",
        "fields": [
            {
                "field": "source",
                "name": "io.debezium.connector.mysql.Source",
                "optional": false,
                "type": "struct",
                "fields": [
                    {
                        "field": "version",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "connector",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "name",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "ts_ms",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "snapshot",
                        "optional": true,
                        "type": "string",
                        "parameters": {
                            "allowed": "true,last,false,incremental"
                        },
                        "default": "false",
                        "name": "io.debezium.data.Enum",
                        "version": 1
                    },
                    {
                        "field": "db",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "sequence",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "table",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "server_id",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "gtid",
                        "optional": true,
                        "type": "string"
                    },
                    {
                        "field": "file",
                        "optional": false,
                        "type": "string"
                    },
                    {
                        "field": "pos",
                        "optional": false,
                        "type": "int64"
                    },
                    {
                        "field": "row",
                        "optional": false,
                        "type": "int32"
                    },
                    {
                        "field": "thread",
                        "optional": true,
                        "type": "int64"
                    },
                    {
                        "field": "query",
                        "optional": true,
                        "type": "string"
                    }
                ]
            },
            {
                "field": "ts_ms",
                "optional": false,
                "type": "int64"
            },
            {
                "field": "databaseName",
                "optional": true,
                "type": "string"
            },
            {
                "field": "schemaName",
                "optional": true,
                "type": "string"
            },
            {
                "field": "ddl",
                "optional": true,
                "type": "string"
            },
            {
                "field": "tableChanges",
                "optional": false,
                "type": "array",
                "items": {
                    "name": "io.debezium.connector.schema.Change",
                    "optional": false,
                    "type": "struct",
                    "version": 1,
                    "fields": [
                        {
                            "field": "type",
                            "optional": false,
                            "type": "string"
                        },
                        {
                            "field": "id",
                            "optional": false,
                            "type": "string"
                        },
                        {
                            "field": "table",
                            "optional": true,
                            "type": "struct",
                            "name": "io.debezium.connector.schema.Table",
                            "version": 1,
                            "fields": [
                                {
                                    "field": "defaultCharsetName",
                                    "optional": true,
                                    "type": "string"
                                },
                                {
                                    "field": "primaryKeyColumnNames",
                                    "optional": true,
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "optional": false
                                    }
                                },
                                {
                                    "field": "columns",
                                    "optional": false,
                                    "type": "array",
                                    "items": {
                                        "name": "io.debezium.connector.schema.Column",
                                        "optional": false,
                                        "type": "struct",
                                        "version": 1,
                                        "fields": [
                                            {
                                                "field": "name",
                                                "optional": false,
                                                "type": "string"
                                            },
                                            {
                                                "field": "jdbcType",
                                                "optional": false,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "nativeType",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "typeName",
                                                "optional": false,
                                                "type": "string"
                                            },
                                            {
                                                "field": "typeExpression",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "charsetName",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "length",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "scale",
                                                "optional": true,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "position",
                                                "optional": false,
                                                "type": "int32"
                                            },
                                            {
                                                "field": "optional",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "autoIncremented",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "generated",
                                                "optional": true,
                                                "type": "boolean"
                                            },
                                            {
                                                "field": "comment",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "defaultValueExpression",
                                                "optional": true,
                                                "type": "string"
                                            },
                                            {
                                                "field": "enumValues",
                                                "optional": true,
                                                "type": "array",
                                                "items": {
                                                    "type": "string",
                                                    "optional": false
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "field": "comment",
                                    "optional": true,
                                    "type": "string"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
}
```

The key fields of the preceding JSON data are explained as follows:

| Field      | Type   | Description                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.ts_ms`     | Number | The timestamp (in milliseconds) when TiCDC generates this message. |
| `payload.ddl`    | String   | The SQL statement of the DDL event.     |
| `payload.databaseName`     | String   | The name of the database where the event occurs.     |
| `payload.source.commit_ts`     | Number  | The `CommitTs` value of the event.       |
| `payload.source.db`     | String   | The name of the database where the event occurs.    |
| `payload.source.table`     | String  |  The name of the table where the event occurs.   |
| `payload.tableChanges` | Array | A structured representation of the entire table schema after the schema change. The `tableChanges` field contains an array that includes entries for each column of the table. Because the structured representation presents data in JSON or Avro format, consumers can easily read messages without first processing them through a DDL parser. |
| `payload.tableChanges.type`     | String   | Describes the kind of change. The value is one of the following: `CREATE`, indicating that the table is created; `ALTER`, indicating that the table is modified; `DROP`, indicating that the table is deleted. |
| `payload.tableChanges.id`     | String   | Full identifier of the table that was created, altered, or dropped. In the case of a table rename, this identifier is a concatenation of `<old>` and `<new>` table names. |
| `payload.tableChanges.table.defaultCharsetName` | string   | The character set of the table where the event occurs. |
| `payload.tableChanges.table.primaryKeyColumnNames` | string   | List of columns that compose the table's primary key. |
| `payload.tableChanges.table.columns` | Array   | Metadata for each column in the changed table. |
| `payload.tableChanges.table.columns.name` | String   | The name of the column. |
| `payload.tableChanges.table.columns.jdbcType` | Number | The JDBC type of the column. |
| `payload.tableChanges.table.columns.comment` | String | The comment of the column. |
| `payload.tableChanges.table.columns.defaultValueExpression` | String | The default value of the column. |
| `payload.tableChanges.table.columns.enumValues` | String | The enumeration values of the column. The format is `['e1', 'e2']`. |
| `payload.tableChanges.table.columns.charsetName` | String | The character set of the column. |
| `payload.tableChanges.table.columns.length` | Number | The length of the column. |
| `payload.tableChanges.table.columns.scale` | Number | The scale of the column. |
| `payload.tableChanges.table.columns.position` | Number | The position of the column. |
| `payload.tableChanges.table.columns.optional` | Boolean | Indicates whether the column is optional. When it is `true`, the column is optional. |
| `schema.fields`     | JSON   | The type information of each field in the payload, including the schema information of columns in the changed table.   |
| `schema.name`     | String  | The name of the schema, in the `"{cluster-name}.{schema-name}.{table-name}.SchemaChangeValue"` format. |
| `schema.optional` | Boolean | Indicates whether the field is optional. When it is `true`, the field is optional.  |
| `schema.type`     | String  | The data type of the field. |

### DML event

TiCDC encodes a DML event into a Kafka message, with both the key and value encoded in the Debezium format.

#### Key format

```json
{
    "payload": {
        "tiny": 1
    },
    "schema": {
        "fields": [
        {
            "field":"tiny",
            "optional":true,
            "type":"int16"
        }
        ],
        "name": "test_cluster.test.table1.Key",
        "optional": false,
        "type":"struct"
    }
}
```

The fields in the key only include primary key or unique index columns. The fields are explained as follows:

| Field            | Type    | Description                                                                 |
|:------------------|:--------|:----------------------------------------------------------------------------|
| `payload`       | JSON    | The information about primary key or unique index columns. The key and value in each field represent the column name and its current value, respectively. |
| `schema.fields`  | JSON    | The type information of each field in the payload, including the schema information of the row data before and after the change. |
| `schema.name`   | String  | The name of the schema, in the `"{cluster-name}.{schema-name}.{table-name}.Key"` format. |
| `schema.optional` | Boolean | Indicates whether the field is optional. When it is `true`, the field is optional.  |
| `schema.type`    | String  | The data type of the field.                                      |

#### Value format

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "test",
            "table": "table1",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 1,
            "cluster_id": "test_cluster"
        },
        "ts_ms": 1701326309000,
        "transaction": null,
        "op": "u",
        "before": { "tiny": 2 },
        "after": { "tiny": 1 }
    },
    "schema": {
        "type": "struct",
        "optional": false,
        "name": "test_cluster.test.table1.Envelope",
        "version": 1,
        "fields": [
            {
                "type": "struct",
                "optional": true,
                "name": "test_cluster.test.table1.Value",
                "field": "before",
                "fields": [{ "type": "int16", "optional": true, "field": "tiny" }]
            },
            {
                "type": "struct",
                "optional": true,
                "name": "test_cluster.test.table1.Value",
                "field": "after",
                "fields": [{ "type": "int16", "optional": true, "field": "tiny" }]
            },
            {
                "type": "struct",
                "fields": [
                    { "type": "string", "optional": false, "field": "version" },
                    { "type": "string", "optional": false, "field": "connector" },
                    { "type": "string", "optional": false, "field": "name" },
                    { "type": "int64", "optional": false, "field": "ts_ms" },
                    {
                        "type": "string",
                        "optional": true,
                        "name": "io.debezium.data.Enum",
                        "version": 1,
                        "parameters": { "allowed": "true,last,false,incremental" },
                        "default": "false",
                        "field": "snapshot"
                    },
                    { "type": "string", "optional": false, "field": "db" },
                    { "type": "string", "optional": true, "field": "sequence" },
                    { "type": "string", "optional": true, "field": "table" },
                    { "type": "int64", "optional": false, "field": "server_id" },
                    { "type": "string", "optional": true, "field": "gtid" },
                    { "type": "string", "optional": false, "field": "file" },
                    { "type": "int64", "optional": false, "field": "pos" },
                    { "type": "int32", "optional": false, "field": "row" },
                    { "type": "int64", "optional": true, "field": "thread" },
                    { "type": "string", "optional": true, "field": "query" }
                ],
                "optional": false,
                "name": "io.debezium.connector.mysql.Source",
                "field": "source"
            },
            { "type": "string", "optional": false, "field": "op" },
            { "type": "int64", "optional": true, "field": "ts_ms" },
            {
                "type": "struct",
                "fields": [
                    { "type": "string", "optional": false, "field": "id" },
                    { "type": "int64", "optional": false, "field": "total_order" },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "data_collection_order"
                    }
                ],
                "optional": true,
                "name": "event.block",
                "version": 1,
                "field": "transaction"
            }
        ]
    }
}
```

The key fields of the preceding JSON data are explained as follows:

| Field      | Type   | Description                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.op`        | String | The type of the change event. `"c"` indicates an `INSERT` event, `"u"` indicates an `UPDATE` event, and `"d"` indicates a `DELETE` event.  |
| `payload.ts_ms`     | Number | The timestamp (in milliseconds) when TiCDC generates this message. |
| `payload.before`    | JSON   | The data value before the change event of a statement. For `"c"` events, the value of the `before` field is `null`.     |
| `payload.after`     | JSON   | The data value after the change event of a statement. For `"d"` events, the value of the `after` field is `null`.     |
| `payload.source.commit_ts`     | Number  | The `CommitTs` value of the event.       |
| `payload.source.db`     | String   | The name of the database where the event occurs.    |
| `payload.source.table`     | String  |  The name of the table where the event occurs.   |
| `schema.fields`     | JSON   | The type information of each field in the payload, including the schema information of the row data before and after the change.   |
| `schema.fields[1].fields[n].tidb_type`     | String  | The TiDB type of each column in `payload.after`. This field exists only when `enable-tidb-extension = true`.   |
| `schema.name`    | String  | The name of the schema, in the `"{cluster-name}.{schema-name}.{table-name}.Envelope"` format. |
| `schema.optional` | Boolean | Indicates whether the field is optional. When it is `true`, the field is optional.  |
| `schema.type`    | String  | The data type of the field.                                      |

### WATERMARK event

TiCDC encodes a WATERMARK event into a Kafka message, with both the key and value encoded in the Debezium format.

#### Key format

```json
{
    "payload": {},
    "schema": {
        "fields": [],
        "optional": false,
        "name": "test_cluster.watermark.Key",
        "type": "struct"
    }
}
```

The fields are explained as follows:

| Field            | Type    | Description                                                                 |
|:------------------|:--------|:----------------------------------------------------------------------------|
| `schema.name`   | String  | The name of the schema, in the `"{cluster-name}.watermark.Key"` format. |

#### Value format

```json
{
    "payload": {
        "source": {
            "version": "2.4.0.Final",
            "connector": "TiCDC",
            "name": "test_cluster",
            "ts_ms": 0,
            "snapshot": "false",
            "db": "",
            "table": "",
            "server_id": 0,
            "gtid": null,
            "file": "",
            "pos": 0,
            "row": 0,
            "thread": 0,
            "query": null,
            "commit_ts": 3,
            "cluster_id": "test_cluster"
        },
        "op": "m",
        "ts_ms": 1701326309000,
        "transaction": null
    },
    "schema": {
        "type": "struct",
        "optional": false,
        "name": "test_cluster.watermark.Envelope",
        "version": 1,
        "fields": [
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "version"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "connector"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "name"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "ts_ms"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "name": "io.debezium.data.Enum",
                        "version": 1,
                        "parameters": {
                            "allowed": "true,last,false,incremental"
                        },
                        "default": "false",
                        "field": "snapshot"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "db"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "sequence"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "table"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "server_id"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "gtid"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "file"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "pos"
                    },
                    {
                        "type": "int32",
                        "optional": false,
                        "field": "row"
                    },
                    {
                        "type": "int64",
                        "optional": true,
                        "field": "thread"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "query"
                    }
                ],
                "optional": false,
                "name": "io.debezium.connector.mysql.Source",
                "field": "source"
            },
            {
                "type": "string",
                "optional": false,
                "field": "op"
            },
            {
                "type": "int64",
                "optional": true,
                "field": "ts_ms"
            },
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "id"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "total_order"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "data_collection_order"
                    }
                ],
                "optional": true,
                "name": "event.block",
                "version": 1,
                "field": "transaction"
            }
        ]
    }
}
```

The key fields of the preceding JSON data are explained as follows:

| Field      | Type   | Description                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.op`        | String | The type of the change event. `"m"` indicates an watermark event.  |
| `payload.ts_ms`     | Number | The timestamp (in milliseconds) when TiCDC generates this message. |
| `payload.source.commit_ts`     | Number  | The `CommitTs` value of the event.      |
| `payload.source.db`     | String   | The name of the database where the event occurs.    |
| `payload.source.table`     | String  |  The name of the table where the event occurs.   |
| `schema.fields`     | JSON   | The type information of each field in the payload, including the schema information of the row data before and after the change.   |
| `schema.name`    | String  | The name of the schema, in the `"{cluster-name}.watermark.Envelope"` format. |
| `schema.optional` | Boolean | Indicates whether the field is optional. When it is `true`, the field is optional.  |
| `schema.type`    | String  | The data type of the field.          |

### Data type mapping

The data format mapping in the TiCDC Debezium message basically follows the [Debezium data type mapping rules](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types), which is generally consistent with the native message of the Debezium Connector for MySQL. However, for some data types, the following differences exist between TiCDC Debezium and Debezium Connector messages:

- Currently, TiDB does not support spatial data types, including GEOMETRY, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, and GEOMETRYCOLLECTION.

- For string-like data types, including Varchar, String, VarString, TinyBlob, MediumBlob, BLOB, and LongBlob, when the column has the BINARY flag, TiCDC encodes it as a String type after encoding it in Base64; when the column does not have the BINARY flag, TiCDC encodes it directly as a String type. The native Debezium Connector encodes it in different ways according to `binary.handling.mode`.

- For the Decimal data type, including DECIMAL and NUMERIC, TiCDC uses the float64 type to represent it. The native Debezium Connector encodes it in float32 or float64 according to the different precision of the data type.

- TiCDC converts REAL to DOUBLE, and converts BOOLEAN to TINYINT(1) when the length is one.

- In TiCDC, the BLOB, TEXT, GEOMETRY, or JSON column does not have a default value.

- Debezium FLOAT data convert `"5.61"` to `"5.610000133514404"`, but TiCDC does not.

- TiCDC print the wrong `flen` with the FLOAT [tidb#57060](https://github.com/pingcap/tidb/issues/57060).

- Debezium converts `charsetName` to `"utf8mb4"` when the column collation is `"utf8_unicode_ci"` and the character set is null, but TiCDC does not.

- TiCDC treats `\` as an escaped quotation in ENUM elements, but Debezium does not. For example, TiCDC encodes ENUM elements like `("c,\'d','g,''h")` to `('c,'d', 'g,''h')`.

- TiCDC converts the default value of TIME like `'1000-00-00 01:00:00.000'` to `"1000-00-00"`, but Debezium does not.
