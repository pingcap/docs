---
title: TiCDC Simple Protocol
summary: Learn how to use the TiCDC Simple protocol and the data format implementation.
---

# TiCDC Simple Protocol

TiCDC Simple protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between heterogeneous databases. This document describes how to use the TiCDC Simple protocol and the data format implementation.

## Use the TiCDC Simple protocol

When you use Kafka as the downstream, specify `protocol` as `"simple"` in the changefeed configuration. Then TiCDC encodes each row change or DDL event as a message, and sends the data change event to the downstream.

The configuration example for using the Simple protocol is as follows:

`sink-uri` configuration:

```shell
--sink-uri = "kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0"
```

Changefeed configuration:

```toml
[sink]
protocol = "simple"

# The following configuration parameters controls the sending behavior of bootstrap messages.
# send-bootstrap-interval-in-sec controls the time interval for sending bootstrap messages, in seconds.
# The default value is 120 seconds, which means that a bootstrap message is sent every 120 seconds for each table.
send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count controls the message interval for sending bootstrap, in message count.
# The default value is 10000, which means that a bootstrap message is sent every 10000 row changed messages for each table.
send-bootstrap-in-msg-count = 10000
# Note: If you want to disable the sending of bootstrap messages, set both send-bootstrap-interval-in-sec and send-bootstrap-in-msg-count to 0.

# send-bootstrap-to-all-partition controls whether to send bootstrap messages to all partitions.
# The default value is true, which means that bootstrap messages are sent to all partitions of the corresponding table topic.
# Setting it to false means the bootstrap message is sent to only the first partition of the corresponding table topic.
send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# encoding-format controls the encoding format of the Simple protocol messages. Currently, the Simple protocol message supports "json" and "avro" encoding formats.
# The default value is "json".
encoding-format = "json"
```

## Message types

The TiCDC Simple protocol has the following message types.

DDL:

- `CREATE`: the creating table event.
- `RENAME`: the renaming table event.
- `CINDEX`: the creating index event.
- `DINDEX`: the deleting index event.
- `ERASE`: the deleting table event.
- `TRUNCATE`: the truncating table event.
- `ALTER`: the altering table event, including adding columns, deleting columns, modifying column types, and other `ALTER TABLE` statements supported by TiCDC.
- `QUERY`: other DDL events.

DML:

- `INSERT`: the inserting event.
- `UPDATE`: the updating event.
- `DELETE`: the deleting event.

Other:

- `WATERMARK`: equal to the TSO in the upstream TiDB cluster. Containing a 64-bit timestamp, the `WATERMARK` event is used to mark the table replication progress. All events earlier than the watermark have been sent to the downstream.
- `BOOTSTRAP`: containing the schema information of a table, used to build the table schema for the downstream.

## Message format

In the Simple protocol, each message contains only one event. The Simple protocol supports encoding messages in JSON and Avro formats. This document uses JSON format as an example. For Avro format messages, their fields and meanings are the same as those in JSON format messages, but the encoding format is different. For details about the Avro schema format, see [Simple Protocol Avro Schema](https://github.com/pingcap/tiflow/blob/master/pkg/sink/codec/simple/message.json).

### DDL

TiCDC encodes a DDL event in the following JSON format:

```json
{
   "version":1,
   "type":"ALTER",
   "sql":"ALTER TABLE `user` ADD COLUMN `createTime` TIMESTAMP",
   "commitTs":447987408682614795,
   "buildTs":1708936343598,
   "tableSchema":{
      "schema":"simple",
      "table":"user",
      "tableID":148,
      "version":447987408682614791,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"createTime",
            "dataType":{
               "mysqlType":"timestamp",
               "charset":"binary",
               "collate":"binary",
               "length":19
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   },
   "preTableSchema":{
      "schema":"simple",
      "table":"user",
      "tableID":148,
      "version":447984074911121426,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   }
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                                   |
| ------------- | ------- | ------------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`.     |
| `type`        | String  | The DDL event type, including `CREATE`, `RENAME`, `CINDEX`, `DINDEX`, `ERASE`, `TRUNCATE`, `ALTER`, and `QUERY`. |
| `sql`         | String  | The DDL statement.                                            |
| `commitTs`    | Number  | The commit timestamp when the DDL statement execution is completed in the upstream.    |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |
| `tableSchema` | Object  | The current schema information of the table. For more details, see [TableSchema definition](#tableschema-definition).  |
| `preTableSchema` | Object | The schema information of the table before the DDL statement is executed.  |

All DDL events, except the `CREATE` type of DDL event, have the `preTableSchema` field, which records the schema information of the table before the DDL statement is executed.

### DML

#### INSERT

TiCEC encodes an `INSERT` event in the following JSON format:

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"INSERT",
   "commitTs":447984084414103554,
   "buildTs":1708923662983,
   "schemaVersion":447984074911121426,
   "data":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"90.5"
   }
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`. |
| `database`    | String  | The name of the database.                                 |
| `table`       | String  | The name of the table.                                    |
| `tableID`     | Number  | The ID of the table.                                      |
| `type`        | String  | The DML event type, including `INSERT`, `UPDATE`, and `DELETE`. |
| `commitTs`    | Number  | The commit timestamp when the DML statement execution is completed in the upstream. |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |
| `schemaVersion` | Number | The schema version number of the table when the DML message is encoded. |
| `data`        | Object  | The inserted data, where the field name is the column name and the field value is the column value. |

The `INSERT` event only contains the `data` field, and does not contain the `old` field.

#### UPDATE

TiCDC encodes an `UPDATE` event in the following JSON format:

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"UPDATE",
   "commitTs":447984099186180098,
   "buildTs":1708923719184,
   "schemaVersion":447984074911121426,
   "data":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"95"
   },
   "old":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"90.5"
   }
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`. |
| `database`    | String  | The name of the database.                                 |
| `table`       | String  | The name of the table.                                    |
| `tableID`     | Number  | The ID of the table.                                      |
| `type`        | String  | The DML event type, including `INSERT`, `UPDATE`, and `DELETE`. |
| `commitTs`    | Number  | The commit timestamp when the DML statement execution is completed in the upstream. |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |
| `schemaVersion` | Number | The schema version number of the table when the DML message is encoded. |
| `data`        | Object  | The data after updating, where the field name is the column name and the field value is the column value. |
| `old`         | Object  | The data before updating, where the field name is the column name and the field value is the column value. |

The `UPDATE` event contains both the `data` and `old` fields, which represent the data after and before updating respectively.

#### DELETE

TiCDC encodes a `DELETE` event in the following JSON format:

```json
{
   "version":1,
   "database":"simple",
   "table":"user",
   "tableID":148,
   "type":"DELETE",
   "commitTs":447984114259722243,
   "buildTs":1708923776484,
   "schemaVersion":447984074911121426,
   "old":{
      "age":"25",
      "id":"1",
      "name":"John Doe",
      "score":"95"
   }
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`. |
| `database`    | String  | The name of the database.                                 |
| `table`       | String  | The name of the table.                                    |
| `tableID`     | Number  | The ID of the table.                                      |
| `type`        | String  | The DML event type, including `INSERT`, `UPDATE`, and `DELETE`. |
| `commitTs`    | Number  | The commit timestamp when the DML statement execution is completed in the upstream. |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |
| `schemaVersion` | Number | The schema version number of the table when the DML message is encoded. |
| `old`         | Object  | The deleted data, where the field name is the column name and the field value is the column value. |

The `DELETE` event only contains the `old` field, and does not contain the `data` field.

### WATERMARK

TiCDC encodes a `WATERMARK` event in the following JSON format:

```json
{
   "version":1,
   "type":"WATERMARK",
   "commitTs":447984124732375041,
   "buildTs":1708923816911
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`. |
| `type`        | String  | The `WATERMARK` event type.                               |
| `commitTs`    | Number  | The commit timestamp of the `WATERMARK`.                  |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |

### BOOTSTRAP

TiCDC encodes a `BOOTSTRAP` event in the following JSON format:

```json
{
   "version":1,
   "type":"BOOTSTRAP",
   "commitTs":0,
   "buildTs":1708924603278,
   "tableSchema":{
      "schema":"simple",
      "table":"new_user",
      "tableID":148,
      "version":447984074911121426,
      "columns":[
         {
            "name":"id",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":false,
            "default":null
         },
         {
            "name":"name",
            "dataType":{
               "mysqlType":"varchar",
               "charset":"utf8mb4",
               "collate":"utf8mb4_bin",
               "length":255
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"age",
            "dataType":{
               "mysqlType":"int",
               "charset":"binary",
               "collate":"binary",
               "length":11
            },
            "nullable":true,
            "default":null
         },
         {
            "name":"score",
            "dataType":{
               "mysqlType":"float",
               "charset":"binary",
               "collate":"binary",
               "length":12
            },
            "nullable":true,
            "default":null
         }
      ],
      "indexes":[
         {
            "name":"primary",
            "unique":true,
            "primary":true,
            "nullable":false,
            "columns":[
               "id"
            ]
         }
      ]
   }
}
```

The fields in the preceding JSON data are explained as follows:

| Field         | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `version`     | Number  | The version number of the protocol, which is currently `1`. |
| `type`        | String  | The `BOOTSTRAP` event type.                               |
| `commitTs`    | Number  | The `commitTs` of the `BOOTSTRAP` is `0`. Because it is generated internally by TiCDC, its `commitTs` is meaningless. |
| `buildTs`     | Number  | The UNIX timestamp when the message is successfully encoded within TiCDC. |
| `tableSchema` | Object  | The schema information of the table. For more details, see [TableSchema definition](#tableschema-definition). |

## Message generation and sending rules

### DDL

- Generation time: TiCDC sends DDL events after all transactions before this DDL event have been sent.
- Destination: TiCDC sends DDL events to all partitions of the corresponding topic.

### DML

- Generation time: TiCDC sends DML events in the order of the `commitTs` of the transaction.
- Destination: TiCDC sends DDL events to the corresponding partition of the corresponding topic according to the user-configured dispatch rules.

### WATERMARK

- Generation time: TiCDC sends `WATERMARK` events periodically to mark the replication progress of a changefeed. The current interval is 1 second.
- Destination: TiCDC sends `WATERMARK` events to all partitions of the corresponding topic.

### BOOTSTRAP

- Generation time:
    - After creating a new changefeed, before the first DML event of a table is sent, TiCDC sends a `BOOTSTRAP` event to the downstream to build the table schema.
    - Additionally, TiCDC sends `BOOTSTRAP` events periodically to allow newly joined consumers to build the table schema. The default interval is 120 seconds or every 10000 messages. You can adjust the sending interval by configuring the `send-bootstrap-interval-in-sec` and `send-bootstrap-in-msg-count` parameters in the sink configuration.
    - If a table does not receive any new DML messages within 30 minutes, the table is considered inactive. TiCDC stops sending `BOOTSTRAP` events for the table until new DML events are received.
- Destination: By default, TiCDC sends `BOOTSTRAP` events to all partitions of the corresponding topic. You can adjust the sending strategy by configuring the `send-bootstrap-to-all-partition` parameter in the sink configuration.

## Message consumption methods

Because the TiCDC Simple protocol does not include the schema information of the table when sending DML messages, the downstream needs to receive DDL or BOOTSTRAP messages and cache the schema information of the table when consuming DML messages. When receiving a DML message, the downstream can obtain the corresponding table schema information through the `table` name and `schemaVersion` field in the DML message, and then correctly consume the DML message.

The following describes how to correctly consume DML messages based on DDL or BOOTSTRAP messages. According to preceding descriptions, the following information is known:

- Each DML message contains a `schemaVersion` field to mark the schema version number of the table corresponding to the DML message.
- Each DDL message contains a `tableSchema` and `preTableSchema` field to mark the schema information of the table before and after the DDL event.
- Each BOOTSTRAP message contains a `tableSchema` field to mark the schema information of the table corresponding to the BOOTSTRAP message.

The consumption methods are introduced in the following two scenarios.

### Scenario 1: The consumer starts consuming from the beginning

In this scenario, the consumer starts consuming from the beginning, so the consumer can receive all DDL and BOOTSTRAP messages of the table. In this case, the consumer can obtain the schema information of the table through the `table` name and `schemaVersion` field in the DML message. The detailed process is as follows:

![TiCDC Simple Protocol consumer scene 1](/media/ticdc/ticdc-simple-consumer-1.png)

### Scenario 2: The consumer starts consuming from the middle

When a new consumer joins the consumer group, it might start consuming from the middle, so it might miss the previous DDL and BOOTSTRAP messages. In this case, the consumer might receive some DML messages before obtaining the schema information of the table. Therefore, the consumer needs to wait for a period of time until it receives the DDL or BOOTSTRAP message to obtain the schema information of the table. Because TiCDC sends BOOTSTRAP messages periodically, the consumer can always obtain the schema information of the table within a period of time. The detailed process is as follows:

![TiCDC Simple Protocol consumer scene 2](/media/ticdc/ticdc-simple-consumer-2.png)

## Reference

### TableSchema definition

TableSchema is a JSON object that contains the schema information of the table, including the table name, table ID, table version number, column information, and index information. The JSON message format is as follows:

``` json
{
    "schema":"simple",
    "table":"user",
    "tableID":148,
    "version":447984074911121426,
    "columns":[
        {
        "name":"id",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":false,
        "default":null
        },
        {
        "name":"name",
        "dataType":{
            "mysqlType":"varchar",
            "charset":"utf8mb4",
            "collate":"utf8mb4_bin",
            "length":255
        },
        "nullable":true,
        "default":null
        },
        {
        "name":"age",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":true,
        "default":null
        },
        {
        "name":"score",
        "dataType":{
            "mysqlType":"float",
            "charset":"binary",
            "collate":"binary",
            "length":12
        },
        "nullable":true,
        "default":null
        }
    ],
    "indexes":[
        {
        "name":"primary",
        "unique":true,
        "primary":true,
        "nullable":false,
        "columns":[
            "id"
        ]
        }
    ]
}
```

The preceding JSON data is explained as follows:

| Field      | Type   | Description                                                         |
| ---------- | ------ | ------------------------------------------------------------------- |
| `schema`   | String | The name of the database.                                           |
| `table`    | String | The name of the table.                                              |
| `tableID`  | Number | The ID of the table.                                                |
| `version`  | Number | The schema version number of the table.                             |
| `columns`  | Array  | The column information, including the column name, data type, whether it can be null, and the default value. |
| `indexes`  | Array  | The index information, including the index name, whether it is unique, whether it is a primary key, and the index column. |

You can uniquely identify the schema information of a table by the table name and the schema version number.

> **Note:**
>
> Due to the implementation limitations of TiDB, the schema version number of a table does not change when the `RENAME TABLE` DDL operation is executed.

#### Column definition

Column is a JSON object that contains the schema information of the column, including the column name, data type, whether it can be null, and the default value.

```json
{
        "name":"id",
        "dataType":{
            "mysqlType":"int",
            "charset":"binary",
            "collate":"binary",
            "length":11
        },
        "nullable":false,
        "default":null
}
```

The preceding JSON data is explained as follows:

| Field      | Type   | Description                                                         |
| ---------- | ------ | ------------------------------------------------------------------- |
| `name`     | String | The name of the column.                                             |
| `dataType` | Object | The data type information, including the MySQL data type, character set, collation, and field length. |
| `nullable` | Boolean | Whether the column can be null.                                    |
| `default`  | String | The default value of the column.                                    |

#### Index definition

Index is a JSON object that contains the schema information of the index, including the index name, whether it is unique, whether it is a primary key, and the index column.

```json
{
        "name":"primary",
        "unique":true,
        "primary":true,
        "nullable":false,
        "columns":[
            "id"
        ]
}
```

The preceding JSON data is explained as follows:

| Field      | Type   | Description                                                         |
| ---------- | ------ | ------------------------------------------------------------------- |
| `name`     | String | The name of the index.                                              |
| `unique`   | Boolean | Whether the index is unique.                                       |
| `primary`  | Boolean | Whether the index is a primary key.                                |
| `nullable` | Boolean | Whether the index can be null.                                     |
| `columns`  | Array  | The column names included in the index.                             |

### mysqlType reference table

The following table describes the value range of the `mysqlType` field in the TiCDC Simple protocol and its type in TiDB (Golang) and Avro (Java). When you need to parse DML messages, you can correctly parse the data according to this table and the `mysqlType` field in the DML message, depending on the protocol and language you use.

**TiDB Type (Golang)** represents the type of the corresponding `mysqlType` when it is processed in TiDB and TiCDC (Golang). **Avro Type (Java)** represents the type of the corresponding `mysqlType` when it is encoded into Avro format messages.

| MySQL Type | Value Range | TiDB Type (Golang) | Avro Type (Java) |
| --- | --- | --- | --- |
| tinyint | [-128, 127] | int64 | long |
| tinyint unsigned | [0, 255] | uint64 | long |
| smallint | [-32768, 32767] | int64 | long |
| smallint unsigned | [0, 65535] | uint64 | long |
| mediumint | [-8388608, 8388607] | int64 | long |
| mediumint unsigned | [0, 16777215] | uint64 | long |
| int | [-2147483648, 2147483647] | int64 | long |
| int unsigned | [0, 4294967295] | uint64 | long |
| bigint | [-9223372036854775808, 9223372036854775807] | int64 | long |
| bigint unsigned | [0, 9223372036854775807] | uint64 | long |
| bigint unsigned | [9223372036854775808, 18446744073709551615] | uint64 | string |
| float | / | float32 | float |
| double | / | float64 | double |
| decimal | / | string | string |
| varchar | / | []uint8 | string |
| char | / | []uint8 | string |
| varbinary | / | []uint8 | bytes |
| binary | / | []uint8 | bytes |
| tinytext | / | []uint8 | string |
| text | / | []uint8 | string |
| mediumtext | / | []uint8 | string |
| longtext | / | []uint8 | string |
| tinyblob | / | []uint8 | bytes |
| blob | / | []uint8 | bytes |
| mediumblob | / | []uint8 | bytes |
| longblob | / | []uint8 | bytes |
| date | / | string | string |
| datetime | / | string | string |
| timestamp | / | string | string |
| time | / | string | string |
| year | / | int64 | long |
| enum | / | uint64 | long |
| set | / | uint64 | long |
| bit | / | uint64 | long |
| json | / | string | string |
| bool | / | int64 | long |

### Avro schema definition

The Simple protocol supports outputting messages in Avro format. For details about the Avro schema format, see [Simple Protocol Avro Schema](https://github.com/pingcap/tiflow/blob/master/pkg/sink/codec/simple/message.json).
