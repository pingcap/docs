---
title: TiCDC Debezium Protocol
summary: TiCDC Debezium プロトコルの概念とその使用方法を学びます。
---

# TiCDC Debeziumプロトコル {#ticdc-debezium-protocol}

TiCDC [Debezium](https://debezium.io/) 、データベースの変更をキャプチャするためのツールです。キャプチャされたデータベースの変更はそれぞれ「イベント」と呼ばれるメッセージに変換され、Kafka に送信されます。v8.0.0以降、TiCDCはDebezium形式でTiDBの行データ変更（DMLイベント）をKafkaに直接送信することをサポートしているため、これまでDebeziumのMySQL統合を使用していたユーザーにとって、MySQLデータベースからの移行が簡素化されます。[TiCDC v8.5.4-release.1](https://github.com/pingcap/ticdc/releases/tag/v8.5.4-release.1)（[新しい TiCDC アーキテクチャ](/ticdc/ticdc-architecture.md)）以降、TiCDC は Debezium 形式で DDL イベントと WATERMARK イベントを送信することもサポートしています。

## Debeziumメッセージ形式を使用する {#use-the-debezium-message-format}

Kafkaをダウンストリームシンクとして使用する場合は、 `sink-uri`設定で`protocol`フィールドを`debezium`に指定します。TiCDCはイベントに基づいてDebeziumメッセージをカプセル化し、TiDBデータ変更イベントをダウンストリームに送信します。

<SimpleTab>
<div label="New TiCDC architecture">

新しい TiCDC アーキテクチャを使用するには、TiCDC 設定項目 [`newarch`](/ticdc/ticdc-server-config.md#newarch-new-in-v854-release1) を `true` に設定します。

新しい TiCDC アーキテクチャでは、Debezium プロトコルは次の種類のイベントをサポートします。

- DDL event: DDL 変更レコードを表します。アップストリームの DDL ステートメントが正常に実行された後、DDL イベントはすべての Message Queue (MQ) パーティションに送信されます。

- DML event: 行データ変更レコードを表します。DML イベントは行変更が発生したときに送信されます。変更後の行に関する情報が含まれます。

- WATERMARK event: 特定の時点を表します。この時点より前に受信したイベントが完全であることを示します。WATERMARK イベントは TiDB 拡張フィールドにのみ適用され、`sink-uri` で [`enable-tidb-extension`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) を `true` に設定した場合に有効になります。

</div>
<div label="Classic TiCDC architecture">

従来の TiCDC アーキテクチャでは、Debezium プロトコルは行変更イベントのみをサポートし、DDL イベントと WATERMARK イベントは無視されます。行変更イベントは、行のデータ変更を表します。行が変更されると、行変更イベントが送信され、変更前後の行に関する情報が含まれます。WATERMARK イベントはテーブルのレプリケーションの進行状況を示し、ウォーターマークより前のすべてのイベントが下流に送信済みであることを示します。

</div>
</SimpleTab>

Debezium メッセージ形式を使用するための構成例は次のとおりです。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-debezium" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=debezium"
```

Debeziumの出力形式には、下流のコンシューマーが現在の行のデータ構造をより適切に理解できるように、現在の行のスキーマ情報が含まれています。スキーマ情報が不要なシナリオでは、changefeed設定ファイルで`debezium-disable-schema`パラメータを`true`または`sink-uri`に設定することで、スキーマ出力を無効にすることもできます。

さらに、元の Debezium 形式には、TiDB の `CommitTS` の一意なトランザクション識別子などの重要なフィールドが含まれていません。データの整合性を確保するために、TiCDC は Debezium 形式に `CommitTs` と `ClusterID` の 2つのフィールドを追加し、TiDB データ変更の関連情報を識別します。

## メッセージ形式の定義 {#message-format-definition}

このセクションでは、DDL イベント、DML イベント、および WATERMARK イベントのメッセージ形式について説明します。

### DDL イベント（新しい TiCDC アーキテクチャ） {#ddl-event-new-ticdc-architecture}

> **Note:**
>
> DDL イベントは、[新しい TiCDC アーキテクチャ](/ticdc/ticdc-architecture.md) でのみサポートされます。[従来の TiCDC アーキテクチャ](/ticdc/ticdc-classic-architecture.md) では、DDL イベントは無視されます。

TiCDC は、キーと値の両方を Debezium 形式でエンコードして、DDL イベントを Kafka メッセージにエンコードします。

#### キーフォーマット {#key-format}

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

キーのフィールドには、データベース名のみが含まれます。各フィールドの説明は以下のとおりです。

| フィールド名                | 型     | 説明                                                                                                                                                        |
| :---------------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `payload`         | JSON    | データベース名に関する情報。 |
| `schema.fields`   | JSON    | payload内の各フィールドの型情報。                                                                                                                   |
| `schema.type`     | String  | フィールドのデータ型。                                                                                                                                               |
| `schema.optional` | Boolean | フィールドがオプションかどうかを示します。`true`の場合、フィールドはオプションです。                                                                        |
| `schema.version`  | String  | スキーマのバージョン。                                                                                                                                               |

#### 値の形式 {#value-format}

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

前述の JSON データの主要フィールドの説明は以下のとおりです。

| フィールド名      | 型   | 説明                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.ts_ms`     | Number | TiCDC がこのメッセージを生成した時点のタイムスタンプ（ミリ秒）。 |
| `payload.ddl`    | String   | DDL イベントの SQL ステートメント。     |
| `payload.databaseName`     | String   | イベントが発生したデータベースの名前。     |
| `payload.source.commit_ts`     | Number  | イベントの `CommitTs` 値。       |
| `payload.source.db`     | String   | イベントが発生したデータベースの名前。    |
| `payload.source.table`     | String  |  イベントが発生したテーブルの名前。   |
| `payload.tableChanges` | Array | スキーマ変更後のテーブルスキーマ全体の構造化表現。`tableChanges` フィールドには、テーブルの各カラムのエントリを含む配列が含まれます。構造化表現は JSON または Avro 形式でデータを表すため、コンシューマーは DDL パーサーで事前処理しなくてもメッセージを簡単に読み取れます。 |
| `payload.tableChanges.type`     | String   | 変更の種類を示します。値は次のいずれかです。`CREATE` はテーブルが作成されたこと、`ALTER` はテーブルが変更されたこと、`DROP` はテーブルが削除されたことを示します。 |
| `payload.tableChanges.id`     | String   | 作成、変更、または削除されたテーブルの完全識別子。テーブル名変更の場合、この識別子は `<old>` と `<new>` のテーブル名を連結したものです。 |
| `payload.tableChanges.table.defaultCharsetName` | string   | イベントが発生したテーブルの文字セット。 |
| `payload.tableChanges.table.primaryKeyColumnNames` | string   | テーブルの主キーを構成するカラムの一覧。 |
| `payload.tableChanges.table.columns` | Array   | 変更されたテーブルの各カラムのメタデータ。 |
| `payload.tableChanges.table.columns.name` | String   | カラム名。 |
| `payload.tableChanges.table.columns.jdbcType` | Number | カラムの JDBC 型。 |
| `payload.tableChanges.table.columns.comment` | String | カラムのコメント。 |
| `payload.tableChanges.table.columns.defaultValueExpression` | String | カラムのデフォルト値。 |
| `payload.tableChanges.table.columns.enumValues` | String | カラムの列挙値。形式は `['e1', 'e2']` です。 |
| `payload.tableChanges.table.columns.charsetName` | String | カラムの文字セット。 |
| `payload.tableChanges.table.columns.length` | Number | カラムの長さ。 |
| `payload.tableChanges.table.columns.scale` | Number | カラムのスケール。 |
| `payload.tableChanges.table.columns.position` | Number | カラムの位置。 |
| `payload.tableChanges.table.columns.optional` | Boolean | カラムがオプションかどうかを示します。`true` の場合、カラムはオプションです。 |
| `schema.fields`     | JSON   | payload 内の各フィールドの型情報。変更されたテーブル内のカラムのスキーマ情報も含みます。   |
| `schema.name`     | String  | スキーマの名前。形式は `"{cluster-name}.{schema-name}.{table-name}.SchemaChangeValue"` です。 |
| `schema.optional` | Boolean | フィールドがオプションかどうかを示します。`true` の場合、フィールドはオプションです。  |
| `schema.type`     | String  | フィールドのデータ型。 |

### DML イベント {#dml-event}

TiCDC は、キーと値の両方を Debezium 形式でエンコードして、DML イベントを Kafka メッセージにエンコードします。

#### キーフォーマット {#key-format}

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

キーのフィールドには、主キーまたは一意インデックス列のみが含まれます。各フィールドの説明は以下のとおりです。

| フィールド名            | 型    | 説明                                                                 |
|:------------------|:--------|:----------------------------------------------------------------------------|
| `payload`       | JSON    | 主キーまたは一意インデックス列に関する情報。各フィールドのキーと値は、それぞれカラム名とその現在の値を表します。 |
| `schema.fields`  | JSON    | payload 内の各フィールドの型情報。変更前後の行データのスキーマ情報を含みます。 |
| `schema.name`   | String  | スキーマの名前。形式は `"{cluster-name}.{schema-name}.{table-name}.Key"` です。 |
| `schema.optional` | Boolean | フィールドがオプションかどうかを示します。`true` の場合、フィールドはオプションです。  |
| `schema.type`    | String  | フィールドのデータ型。                                      |

#### 値の形式 {#value-format}

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

前述のJSONデータの主要なフィールドの説明は以下のとおりです。

| フィールド名                   | 型    | 説明                                                                                                                               |
| :------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------- |
| `payload.op`             | String | 変更イベントのタイプ。`"c"`は`INSERT`イベント、 `"u"`は`UPDATE`イベント、 `"d"`は`DELETE`イベントを示します。                                                    |
| `payload.ts_ms`          | Number     | TiCDC がこのメッセージを生成したときのタイムスタンプ (ミリ秒単位)。                                                                                           |
| `payload.before`         | JSON   | ステートメントの変更イベント前のデータ値。イベントが`"c"`の場合、フィールド`before`の値は`null`になります。                                                                    |
| `payload.after`               | JSON   | ステートメントの変更イベント後のデータ値。イベントが`"d"`の場合、フィールド`after`の値は`null`になります。                |
| `payload.source.commit_ts`    | Number     | イベントの`CommitTs`値。                                                                                             |
| `payload.source.db`         | String      | イベントが発生したデータベースの名前。                                                                                                              |
| `payload.source.table` | String      | イベントが発生するテーブルの名前。                                                                                                                |
| `schema.fields`        | JSON   | ペイロード内の各フィールドの型情報。変更前後の行データのスキーマ情報を含みます。 |
| `schema.fields[1].fields[n].tidb_type` | String | `payload.after` 内の各カラムの TiDB 型。このフィールドは `enable-tidb-extension = true` の場合にのみ存在します。 |
| `schema.name`              | String      | スキーマの名前（形式は`"{cluster-name}.{schema-name}.{table-name}.Envelope"` 。                                                              |
| `schema.optional`          | Boolean   | フィールドがオプションかどうかを示します。 `true`の場合、フィールドはオプションです。                                                                                   |
| `schema.type`              | String      | フィールドのデータ型。                                                                                                                      |

### WATERMARK イベント（新しい TiCDC アーキテクチャ） {#watermark-event-new-ticdc-architecture}

> **Note:**
>
> WATERMARK イベントは、[新しい TiCDC アーキテクチャ](/ticdc/ticdc-architecture.md) でのみサポートされます。[従来の TiCDC アーキテクチャ](/ticdc/ticdc-classic-architecture.md) では、WATERMARK イベントは無視されます。

TiCDC は WATERMARK イベントを Kafka メッセージにエンコードし、キーと値の両方を Debezium 形式でエンコードします。

#### キーフォーマット {#key-format}

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

フィールドの説明は以下のとおりです。

| フィールド名            | 型    | 説明                                                                 |
|:------------------|:--------|:----------------------------------------------------------------------------|
| `schema.name`   | String  | スキーマの名前。形式は `"{cluster-name}.watermark.Key"` です。 |

#### 値の形式 {#value-format}

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

前述の JSON データの主要なフィールドの説明は以下のとおりです。

| フィールド名      | 型   | 説明                                            |
|:----------|:-------|:-------------------------------------------------------|
| `payload.op`        | String | 変更イベントのタイプ。`"m"` は watermark イベントを示します。  |
| `payload.ts_ms`     | Number | TiCDC がこのメッセージを生成した時点のタイムスタンプ（ミリ秒単位）。 |
| `payload.source.commit_ts`     | Number  | イベントの `CommitTs` 値。      |
| `payload.source.db`     | String   | イベントが発生するデータベースの名前。    |
| `payload.source.table`     | String  |  イベントが発生するテーブルの名前。   |
| `schema.fields`     | JSON   | payload 内の各フィールドの型情報。変更前後の行データのスキーマ情報を含みます。   |
| `schema.name`    | String  | スキーマの名前。形式は `"{cluster-name}.watermark.Envelope"` です。 |
| `schema.optional` | Boolean | フィールドがオプションかどうかを示します。`true` の場合、そのフィールドはオプションです。  |
| `schema.type`    | String  | フィールドのデータ型。          |

### Data type mapping {#data-type-mapping}

TiCDC Debeziumメッセージのデータ形式マッピングは基本的に[Debeziumデータ型マッピングルール](https://debezium.io/documentation/reference/stable/connectors/mysql.html#mysql-data-types)に準拠しており、これはMySQL用Debeziumコネクタのネイティブメッセージと概ね一致しています。ただし、一部のデータ型については、TiCDC DebeziumメッセージとDebeziumコネクタメッセージの間に以下の違いがあります。

-   現在、TiDB は、GEOMETRY、LINESTRING、POLYGON、MULTIPOINT、MULTILINESTRING、MULTIPOLYGON、GEOMETRYCOLLECTION などの空間データ型をサポートしていません。

-   Varchar、String、VarString、TinyBlob、MediumBlob、BLOB、LongBlobなどの文字列型データ型の場合、列にBINARYフラグが付いている場合、TiCDCはBase64でエンコードした後、String型としてエンコードします。列にBINARYフラグが付いていない場合は、TiCDCは直接String型としてエンコードします。ネイティブDebeziumコネクタは、 `binary.handling.mode`に従って異なる方法でエンコードします。

-   TiCDCは、 DECIMALとNUMERIC含むDecimalデータ型をfloat64型で表現します。ネイティブのDebeziumコネクタは、データ型の精度に応じて、float32またはfloat64でエンコードします。

- TiCDC は REAL を DOUBLE に変換し、長さが 1 の場合は BOOLEAN を TINYINT(1) に変換します。

- TiCDC では、BLOB、TEXT、GEOMETRY、または JSON カラムにはデフォルト値がありません。

- Debezium は FLOAT データ `"5.61"` を `"5.610000133514404"` に変換しますが、TiCDC は変換しません。

- TiCDC は FLOAT の `flen` を誤って出力します [tidb#57060](https://github.com/pingcap/tidb/issues/57060)。

- カラムの照合順序が `"utf8_unicode_ci"` で文字セットが null の場合、Debezium は `charsetName` を `"utf8mb4"` に変換しますが、TiCDC は変換しません。

- TiCDC は ENUM 要素内の `\` をエスケープされた引用符として扱いますが、Debezium は扱いません。たとえば、TiCDC は `("c,\'d','g,''h")` のような ENUM 要素を `('c,'d', 'g,''h')` にエンコードします。

- TiCDC は `'1000-00-00 01:00:00.000'` のような TIME のデフォルト値を `"1000-00-00"` に変換しますが、Debezium は変換しません。
