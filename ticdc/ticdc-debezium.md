---
title: TiCDC Debezium Protocol
summary: Learn the concept of the TiCDC Debezium Protocol and how to use it.
---

# TiCDC Debezium Protocol

[Debezium](https://debezium.io/) is a tool for capturing database changes. It converts each captured database change into a message called an "event" and sends these events to Kafka. Starting from v8.0.0, TiCDC supports sending TiDB changes to Kafka using a Debezium style output format, simplifying migration from MySQL databases for users who had previously been using Debezium's MySQL integration.

## Use the Debezium message format

When you use Kafka as the downstream sink, specify the `protocol` field as `debezium` in `sink-uri` configuration. Then TiCDC encapsulates the Debezium messages based on the events and sends TiDB data change events to the downstream.

Currently, the Debezium protocol only supports Row Changed events and directly ignores DDL events and WATERMARK events. A Row changed event represents a data change in a row. When a row changes, the Row Changed event is sent, including relevant information about the row both before and after the change. A WATERMARK event marks the replication progress of a table, indicating that all events earlier than the watermark have been sent to the downstream.

The configuration example for using the Debezium message format is as follows:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

The Debezium output format contains the schema information of the current row so that downstream consumers can better understand the data structure of the current row. For scenarios where schema information is unnecessary, you can also disable the schema output by setting the `debezium-disable-schema` parameter to `true` in the changefeed configuration file or `sink-uri`.

In addition, the original Debezium format does not include important fields such as the unique transaction identifier of the `CommitTS` in TiDB. To ensure data integrity, TiCDC adds two fields, `CommitTs` and `ClusterID`, to the Debezium format to identify the relevant information of TiDB data changes.

## Message format definition

This section describes the format definition of the DML event output in the Debezium format.

### DML event

TiCDC encodes a DML event in the following format:

```json
{
    "payload":{
        "ts_ms":1707103832957,
        "transaction":null,
        "op":"c",
        "before":null,
        "after":{
            "a":4,
            "b":2
        },
        "source":{
            "version":"2.4.0.Final",
            "connector":"TiCDC",
            "name":"default",
            "ts_ms":1707103832263,
            "snapshot":"false",
            "db":"test",
            "table":"t2",
            "server_id":0,
            "gtid":null,
            "file":"",
            "pos":0,
            "row":0,
            "thread":0,
            "query":null,
            "commit_ts":447507027004751877,
            "cluster_id":"default"
        }
    },
    "schema":{
        "type":"struct",
        "optional":false,
        "name":"default.test.t2.Envelope",
        "version":1,
        "fields":{
            {
                "type":"struct",
                "optional":true,
                "name":"default.test.t2.Value",
                "field":"before",
                "fields":[
                    {
                        "type":"int32",
                        "optional":false,
                        "field":"a"
                    },
                    {
                        "type":"int32",
                        "optional":true,
                        "field":"b"
                    }
                ]
            },
            {
                "type":"struct",
                "optional":true,
                "name":"default.test.t2.Value",
                "field":"after",
                "fields":[
                    {
                        "type":"int32",
                        "optional":false,
                        "field":"a"
                    },
                    {
                        "type":"int32",
                        "optional":true,
                        "field":"b"
                    }
                ]
            },
            {
                "type":"string",
                "optional":false,
                "field":"op"
            },
            ...
        }
    }
}
```

The key fields of the preceding JSON data are explained as follows:

| Field      | Type   | Description                                            |
|:----------|:-------|:-------------------------------------------------------|
| payload.op        | String | The type of the change event. `"c"` indicates an `INSERT` event, `"u"` indicates an `UPDATE` event, and `"d"` indicates a `DELETE` event.  |
| payload.ts_ms     | Number | The timestamp (in milliseconds) when TiCDC generates this message. |
| payload.before    | JSON   | The data value before the change event of a statement. For `"c"` events, the value of the `before` field is `null`.     |
| payload.after     | JSON   | The data value after the change event of a statement. For `"d"` events, the value of the `after` field is `null`.     |
| payload.source.commit_ts     | Number  | The `CommitTs` identifier when TiCDC generates this message.       |
| payload.source.db     | String   | The name of the database where the event occurs.    |
| payload.source.table     | String  |  The name of the table where the event occurs.   |
| schema.fields     | JSON   |  The type information of each field in the payload, including the schema information of the row data before and after the change.   |

### Data type mapping

The data format mapping in the TiCDC Debezium message basically follows the [Debezium data type mapping rules](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types), which is generally consistent with the native message of the Debezium Connector for MySQL. However, for some data types, the following differences exist between TiCDC Debezium and Debezium Connector messages:

- Currently, TiDB does not support spatial data types, including GEOMETRY, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, and GEOMETRYCOLLECTION.

- For string-like data types, including Varchar, String, VarString, TinyBlob, MediumBlob, BLOB, and LongBlob, when the column has the BINARY flag, TiCDC encodes it as a String type after encoding it in Base64; when the column does not have the BINARY flag, TiCDC encodes it directly as a String type. The native Debezium Connector encodes it in different ways according to `binary.handling.mode`.

- For the Decimal data type, including `DECIMAL` and `NUMERIC`, TiCDC uses the float64 type to represent it. The native Debezium Connector encodes it in float32 or float64 according to the different precision of the data type.
