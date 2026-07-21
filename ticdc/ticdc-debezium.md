---
title: TiCDC Debezium Protocol
summary: TiCDC Debezium プロトコルの概念とその使用方法を学びます。
---

# TiCDC Debeziumプロトコル {#ticdc-debezium-protocol}

TiCDC [Debezium](https://debezium.io/) 、データベースの変更をキャプチャするためのツールです。キャプチャされたデータベースの変更はそれぞれ「イベント」と呼ばれるメッセージに変換され、Kafka に送信されます。v8.0.0以降、TiCDCはDebeziumスタイルの出力形式を使用してTiDBの変更をKafkaに送信することをサポートするため、これまでDebeziumのMySQL統合を使用していたユーザーにとって、MySQLデータベースからの移行が簡素化されます。

## Debeziumメッセージ形式を使用する {#use-the-debezium-message-format}

Kafkaをダウンストリームシンクとして使用する場合は、 `sink-uri`設定で`protocol`フィールドを`debezium`に指定します。TiCDCはイベントに基づいてDebeziumメッセージをカプセル化し、TiDBデータ変更イベントをダウンストリームに送信します。

Currently, the Debezium protocol only supports Row Changed events and directly ignores DDL events and WATERMARK events. A Row changed event represents a data change in a row. When a row changes, the Row Changed event is sent, including relevant information about the row both before and after the change. A WATERMARK event marks the replication progress of a table, indicating that all events earlier than the watermark have been sent to the downstream.

Debezium メッセージ形式を使用するための構成例は次のとおりです。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

Debeziumの出力形式には、下流のコンシューマーが現在の行のデータ構造をより適切に理解できるように、現在の行のスキーマ情報が含まれています。スキーマ情報が不要なシナリオでは、changefeed設定ファイルで`debezium-disable-schema`パラメータを`true`または`sink-uri`に設定することで、スキーマ出力を無効にすることもできます。

In addition, the original Debezium format does not include important fields such as the unique transaction identifier of the `CommitTS` in TiDB. To ensure data integrity, TiCDC adds two fields, `CommitTs` and `ClusterID`, to the Debezium format to identify the relevant information of TiDB data changes.

## メッセージ形式の定義 {#message-format-definition}

このセクションでは、Debezium 形式の DML イベント出力の形式定義について説明します。

### DMLイベント {#dml-event}

TiCDC は、キーと値の両方を Debezium 形式でエンコードして、DML イベントを Kafka メッセージにエンコードします。

#### キーフォーマット {#key-format}

```json
{
    "payload": {
        "a": 4
    },
    "schema": {
        "fields": [
            {
                "field": "a",
                "optional": true,
                "type": "int32"
            }
        ],
        "name": "default.test.t2.Key",
        "optional": false,
        "type": "struct"
    }
}
```

キーのフィールドには、主キーまたは一意インデックス列のみが含まれます。各フィールドの説明は以下のとおりです。

| フィールド名                | 型     | 説明                                                                                                                                                        |
| :---------------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `payload`         | JSON    | 主キーまたは一意インデックス列に関する情報。各フィールドのキーと値は、それぞれ列名とその現在の値を表します。 |
| `schema.fields`   | JSON    | payload内の各フィールドの型情報（変更前後の行データのスキーマ情報を含む）。                                                                                                                   |
| `schema.name`     | String  | スキーマの名前（形式は`"{cluster-name}.{schema-name}.{table-name}.Key"` 。                                                                                            |
| `schema.optional` | Boolean | フィールドがオプションかどうかを示します。`true`の場合、フィールドはオプションです。                                                                        |
| `schema.type`     | string       | フィールドのデータ型。                                                                                                                                               |

#### 値の形式 {#value-format}

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

前述のJSONデータの主要なフィールドの説明は以下のとおりです。

| フィールド名                   | 型    | 説明                                                                                                                               |
| :------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------- |
| payload.op             | String | 変更イベントのタイプ。1 `"c"` `INSERT`イベント、 `"u"` `UPDATE`イベント、 `"d"` `DELETE`イベントを示します。                                                    |
| payload.ts_ms          | number     | TiCDC がこのメッセージを生成したときのタイムスタンプ (ミリ秒単位)。                                                                                           |
| payload.before         | JSON   | ステートメントの変更イベント前のデータ値。イベントが`"c"`の場合、フィールド`before`の値は`null`になります。                                                                    |
| payload.after               | JSON   | The data value after the change event of a statement. For `"d"` events, the value of the `after` field is `null`.                |
| payload.source.commit_ts    | number     | TiCDC がこのメッセージを生成するときの`CommitTs`識別子。                                                                                             |
| payload.source.db         | string      | イベントが発生したデータベースの名前。                                                                                                              |
| payload.source.table | string      | イベントが発生するテーブルの名前。                                                                                                                |
| schema.fields        | JSON   | ペイロード内の各フィールドの型情報。変更前後の行データのスキーマ情報を含みます。 |
| schema.name              | string      | スキーマの名前（形式は`"{cluster-name}.{schema-name}.{table-name}.Envelope"` 。                                                              |
| schema.optional          | boolean   | フィールドがオプションかどうかを示します。 `true`の場合、フィールドはオプションです。                                                                                   |
| schema.type              | string      | フィールドのデータ型。                                                                                                                      |

### Data type mapping {#data-type-mapping}

TiCDC Debeziumメッセージのデータ形式マッピングは基本的に[Debeziumデータ型マッピングルール](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types)準拠しており、これはMySQL用Debeziumコネクタのネイティブメッセージと概ね一致しています。ただし、一部のデータ型については、TiCDC DebeziumメッセージとDebeziumコネクタメッセージの間に以下の違いがあります。

-   現在、TiDB は、GEOMETRY、LINESTRING、POLYGON、MULTIPOINT、MULTILINESTRING、MULTIPOLYGON、GEOMETRYCOLLECTION などの空間データ型をサポートしていません。

-   Varchar、String、VarString、TinyBlob、MediumBlob、BLOB、LongBlobなどの文字列型データ型の場合、列にBINARYフラグが付いている場合、TiCDCはBase64でエンコードした後、String型としてエンコードします。列にBINARYフラグが付いていない場合は、TiCDCは直接String型としてエンコードします。ネイティブDebeziumコネクタは、 `binary.handling.mode`に従って異なる方法でエンコードします。

-   TiCDCは、 `DECIMAL`と`NUMERIC`含むDecimalデータ型をfloat64型で表現します。ネイティブのDebeziumコネクタは、データ型の精度に応じて、float32またはfloat64でエンコードします。
