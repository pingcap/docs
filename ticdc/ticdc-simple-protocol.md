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
# The default value is 10000, which means that a bootstrap message is sent every 10000 row changes for each table.
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

DML:

- `INSERT`: the inserting event.
- `UPDATE`: the updating event.
- `DELETE`: the deleting event.

DDL:

- `CREATE`: the creating table event.
- `RENAME`: the renaming table event.
- `CINDEX`: the creating index event.
- `DINDEX`: the deleting index event.
- `ERASE`: the deleting table event.
- `TRUNCATE`: the truncating table event.
- `ALTER`: the altering table event, including adding columns, deleting columns, modifying column types, and other `ALTER TABLE` statements supported by TiCDC.
- `QUERY`: other DDL events.

Other:

- `WATERMARK`: equal to the TSO in the upstream TiDB cluster. Containing a 64-bit timestamp, the `WATERMARK` event is used to mark the table replication progress. All events earlier than the watermark have been sent to the downstream.
- `BOOTSTRAP`: containing the schema information of a table, used to build the table schema for the downstream.

## Message format

In the Simple protocol, each message contains only one event. The Simple protocol supports encoding messages in JSON and Avro formats. This document uses JSON format as an example. For Avro format messages, their fields and meanings are the same as those in JSON format messages, but the encoding format is different. For more information, see the [Avro schema definition](#avro-schema-definition).

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

- 生成时机：DDL 事件将会在该 DDL 发生之前的所有事务都被发送完毕后发送。
- 发送目的地：DDL 事件将会被发送到对应 Topic 的所有的 Partition。

### DML

- 生成时机：DML 事件会按照事务的 commitTs 顺序被发送。
- 发送目的地：DML 事件将会按照用户配置的 Dispatch 规则发送到对应 Topic 对应 Partition。

### WATERMARK

- 生成时机：WATERMARK 事件会周期性地被发送，用于标记一个 changefeed 的同步进度，目前的周期为 1 秒钟。
- 发送目的地：WATERMARK 事件将会被发送到对应 Topic 的所有的 Partition。

### BOOTSTRAP

- 生成时机：
    - 创建一个新的 changefeed 后，在一张表的第一条 DML 事件发送之前，TiCDC 会发送 BOOTSTRAP 事件给下游，用于给下游构建表的结构。
    - 此外，BOOTSTRAP 事件会周期性地被发送，以供下游新加入的 consumer 构建表的结构。目前默认每 120 秒或者每间隔 10000 个消息发送一次，可以通过 sink 配置项 `send-bootstrap-interval-in-sec` 和 `send-bootstrap-in-msg-count` 来调整发送周期。
    - 如果一张表在 30 分钟内没有收到任何新的 DML 消息，那么该表将被认为是不活跃的。我们将停止为该表发送 BOOTSTRAP 事件，直到该表收到新的 DML 事件。
- 发送目的地：BOOTSTRAP 事件默认发送到对应 Topic 的所有的 Partition，可以通过 sink 配置项 `send-bootstrap-to-all-partition` 来调整发送策略。

## Message consumption scenarios

由于 Simple Protocol 在发送 DML 消息时没有包含表的 schema 信息，因此在消费 DML 消息时，下游需要先接收到 DDL 或者 BOOTSTRAP 消息，并且把表的 schema 信息缓存起来。在接收到 DML 消息时，通过 DML 消息中的 table 名和 schemaVersion 字段来获取对应的 tableSchema 信息，从而正确地消费 DML 消息。

下面将会介绍如何正确地根据 DDL 或者 BOOTSTRAP 消息来消费 DML 消息。
根据上述文档的描述，我们已知如下信息

- 每个 DML 消息都会包含一个 schemaVersion 字段，用于标记该 DML 消息对应的表的 schema 版本号。
- 每个 DDL 消息都会包含一个 tableSchema 和 preTableSchema 字段，用于标记该 DDL 发生前后的表的 schema 信息。
- 每个 BOOTSTRAP 消息都会包含一个 tableSchema 字段，用于标记该 BOOTSTRAP 对应的表的 schema 信息。

接下来，我们将介绍两种场景下的消费方法。

### 场景一：消费者从头开始消费

在此场景下，消费者从头开始消费，因此消费者能够接收到该表的所有 DDL 和 BOOTSTRAP 消息。此时，消费者可以通过一个 DML 消息中的 table 名和 schemaVersion 字段来获取对应的 tableSchema 信息。具体步骤如下图所示：

![TiCDC Simple Protocol consumer scene 1](/media/ticdc/ticdc-simple-consumer-1.png)

### 场景二：消费者从中间开始消费

在一个新的消费者加入到消费者组时，它可能会从中间开始消费，因此它可能会错过之前的 DDL 和 BOOTSTRAP 消息。在这种情况下，消费者可能会先接收到一些 DML 消息，但是此时它还没有该表的 schema 信息。因此，它需要先等待一段时间，直到它接收到该表 DDL 或 BOOTSTRAP 消息，从而获取到该表的 schema 信息。由于 BOOTSTRAP 消息会周期性地被发送，消费者总是能够在一段时间内获取到该表的 schema 信息。具体步骤如下图所示：

![TiCDC Simple Protocol consumer scene 2](/media/ticdc/ticdc-simple-consumer-2.png)

## Reference

### TableSchema definition

TableSchema 是一个 JSON 对象，包含了表的 schema 信息，包括表名、表 ID、表的版本号、列信息和索引信息。
其 JSON 消息格式如下：

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

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| schema    | string | 数据库名。                                                         |
| table     | string | 表名。                                                                     |
| tableID   | number    | 表的 ID。                                                              |
| version   | number    | 表的 schema 版本号。                                                       |
| columns   | array  | 列信息，包括列名、数据类型、是否可为空、默认值等。                         |
| indexes   | array  | 索引信息，包括索引名、是否唯一、是否主键、索引列等。                       |

你可以通过表名和表的 schema 版本号 来唯一标识一张表的 schema 信息。

注意：由于 TiDB 的实现限制，在执行 RENAME TABLE 的 DDL 操作时，表的 schema 版本号不会发生变化。

#### Column 定义 

Column 是一个 JSON 对象，包含了列的 schema 信息，包括列名、数据类型、是否可为空、默认值等。

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

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| name      | string | 列名。                                                                     |
| dataType  | object | 数据类型信息，包括 MySQL 数据类型、字符集、字符序、字段长度。                   |
| nullable  | boolean | 是否可为空。                                                              |
| default   | string | 默认值。                                                                   |

#### Index 定义

Index 是一个 JSON 对象，包含了索引的 schema 信息，包括索引名、是否唯一、是否主键、索引列等。

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

以上 JSON 数据的字段解释如下：

| 字段      | 类型   | 说明                                                                      |
| --------- | ------ | ------------------------------------------------------------------------- |
| name      | string | 索引名。                                                                   |
| unique    | boolean | 是否唯一。                                                                |
| primary   | boolean | 是否主键。                                                                |
| nullable  | boolean | 是否可为空。                                                              |
| columns   | array  | 索引包含的列名。                                                            |

### mysqlType 参考表格

以下表格描述了 TiCDC Simple Protocol 中所有的 mysqlType 字段的取值范围及其在 TiDB(Golang) 和 Avro(JAVA) 中的类型。
当你需要对 DML 消息进行解析时，取决于你所使用的协议和语言，可以根据该表格和 DML 消息中的 mysqlType 字段来正确地解析数据。
其中 TiDB Type (Golang) 代表了对应 mysqlType 在 TiDB 和 TiCDC (Golang) 中处理时的类型，Avro Type (Java) 代表了对应 mysqlType 在编码为 Avro 格式消息时的类型。

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
