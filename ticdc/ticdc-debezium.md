---
title: TiCDC Debezium Protocol
summary: TiCDC Debezium プロトコルの概念とその使用方法を学びます。
---

# TiCDC デベジウム プロトコル {#ticdc-debezium-protocol}

[デベジウム](https://debezium.io/) 、データベースの変更をキャプチャするためのツールです。キャプチャされた各データベースの変更を「イベント」と呼ばれるメッセージに変換し、これらのイベントを Kafka に送信します。v8.0.0 以降、TiCDC は Debezium スタイルの出力形式を使用して TiDB の変更を Kafka に送信することをサポートし、これまで Debezium の MySQL 統合を使用していたユーザーにとって MySQL データベースからの移行を簡素化します。

## Debeziumメッセージ形式を使用する {#use-the-debezium-message-format}

Kafka をダウンストリーム シンクとして使用する場合は、 `sink-uri`構成で`protocol`フィールドを`debezium`に指定します。すると、TiCDC はイベントに基づいて Debezium メッセージをカプセル化し、TiDB データ変更イベントをダウンストリームに送信します。

現在、Debezium プロトコルは行変更イベントのみをサポートしており、DDL イベントと WATERMARK イベントは直接無視されます。行変更イベントは、行内のデータ変更を表します。行が変更されると、変更前と変更後の行に関する関連情報を含む行変更イベントが送信されます。WATERMARK イベントは、テーブルのレプリケーションの進行状況を示し、ウォーターマークより前のすべてのイベントがダウンストリームに送信されたことを示します。

Debezium メッセージ形式を使用するための構成例は次のとおりです。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

Debezium 出力形式には、下流の消費者が現在の行のデータ構造をよりよく理解できるように、現在の行のスキーマ情報が含まれています。スキーマ情報が不要なシナリオでは、changefeed 構成ファイルで`debezium-disable-schema`パラメータを`true`に設定するか、 `sink-uri`に設定して、スキーマ出力を無効にすることもできます。

さらに、元の Debezium 形式には、TiDB の`CommitTS`の一意のトランザクション識別子などの重要なフィールドが含まれていません。データの整合性を確保するために、TiCDC は、TiDB データの変更の関連情報を識別できるように、Debezium 形式に`CommitTs`と`ClusterID` 2 つのフィールドを追加します。

## メッセージ形式の定義 {#message-format-definition}

このセクションでは、Debezium 形式の DML イベント出力の形式定義について説明します。

### DMLイベント {#dml-event}

TiCDC は DML イベントを次の形式でエンコードします。

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

上記の JSON データの主要なフィールドは次のように説明されます。

| 分野                | タイプ | 説明                                                                            |
| :---------------- | :-- | :---------------------------------------------------------------------------- |
| ペイロード.op          | 弦   | 変更イベントのタイプ。1 `"c"` `INSERT`イベント、 `"u"` `UPDATE`イベント、 `"d"` `DELETE`イベントを示します。 |
| ペイロード.ts_ms       | 番号  | TiCDC がこのメッセージを生成したときのタイムスタンプ (ミリ秒単位)。                                        |
| ペイロード.before      | 翻訳  | ステートメントの変更イベント前のデータ値。 `"c"`イベントの場合、 `before`フィールドの値は`null`です。                 |
| ペイロード後            | 翻訳  | ステートメントの変更イベント後のデータ値。 `"d"`イベントの場合、 `after`フィールドの値は`null`です。                  |
| ペイロード.ソース.コミット_ts | 番号  | TiCDC がこのメッセージを生成するときの`CommitTs`識別子。                                          |
| ペイロード.ソース.db      | 弦   | イベントが発生したデータベースの名前。                                                           |
| ペイロード.ソース.テーブル    | 弦   | イベントが発生するテーブルの名前。                                                             |
| スキーマフィールド         | 翻訳  | 変更前後の行データのスキーマ情報を含む、ペイロード内の各フィールドの型情報。                                        |

### データ型マッピング {#data-type-mapping}

TiCDC Debezium メッセージのデータ形式マッピングは基本的に[Debezium データ型マッピングルール](https://debezium.io/documentation/reference/2.4/connectors/mysql.html#mysql-data-types)に従います。これは、MySQL 用の Debezium Connector のネイティブ メッセージとほぼ一致しています。ただし、一部のデータ型については、TiCDC Debezium メッセージと Debezium Connector メッセージの間に次の違いがあります。

-   現在、TiDB は、GEOMETRY、LINESTRING、POLYGON、MULTIPOINT、MULTILINESTRING、MULTIPOLYGON、GEOMETRYCOLLECTION などの空間データ型をサポートしていません。

-   Varchar、String、VarString、TinyBlob、MediumBlob、BLOB、LongBlob などの文字列のようなデータ型の場合、列に BINARY フラグがある場合、TiCDC はそれを Base64 でエンコードした後、String 型としてエンコードします。列に BINARY フラグがない場合、TiCDC はそれを直接 String 型としてエンコードします。ネイティブ Debezium Connector は、 `binary.handling.mode`に従ってさまざまな方法でエンコードします。

-   `DECIMAL`や`NUMERIC`などの Decimal データ型の場合、TiCDC は float64 型を使用してそれを表します。ネイティブの Debezium Connector は、データ型の異なる精度に応じて、これを float32 または float64 でエンコードします。
