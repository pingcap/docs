---
title: TiCDC Simple Protocol
summary: TiCDC シンプル プロトコルとデータ形式の実装の使用方法を学習します。
---

# TiCDCシンプルプロトコル {#ticdc-simple-protocol}

TiCDCはv8.0.0以降、シンプルプロトコルをサポートしています。このドキュメントでは、TiCDCシンプルプロトコルの使用方法とデータ形式の実装について説明します。

## TiCDCシンプルプロトコルを使用する {#use-the-ticdc-simple-protocol}

Kafka をダウンストリームとして使用する場合は、changefeed 設定で`protocol`を`"simple"`に指定します。TiCDC は各行変更または DDL イベントをメッセージとしてエンコードし、データ変更イベントをダウンストリームに送信します。

シンプル プロトコルを使用するための設定例は次のとおりです。

`sink-uri`構成:

```shell
--sink-uri = "kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0"
```

Changefeed 構成:

```toml
[sink]
protocol = "simple"

# The following configuration parameters control the sending behavior of bootstrap messages.
# send-bootstrap-interval-in-sec controls the time interval for sending bootstrap messages, in seconds.
# The default value is 120 seconds, which means that a bootstrap message is sent every 120 seconds for each table.
send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count controls the message interval for sending bootstrap, in message count.
# The default value is 10000, which means that a bootstrap message is sent every 10000 row changed messages for each table.
send-bootstrap-in-msg-count = 10000
# Note: If you want to disable the sending of bootstrap messages, set both send-bootstrap-interval-in-sec and send-bootstrap-in-msg-count to 0.

# send-bootstrap-to-all-partition controls whether to send bootstrap messages to all partitions.
# The default value is true, which means that bootstrap messages are sent to all partitions of the corresponding table topic.
# Setting it to false means bootstrap messages are sent to only the first partition of the corresponding table topic.
send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# encoding-format controls the encoding format of the Simple protocol messages. Currently, the Simple protocol message supports "json" and "avro" encoding formats.
# The default value is "json".
encoding-format = "json"
```

## メッセージの種類 {#message-types}

TiCDC シンプル プロトコルには、次のメッセージ タイプがあります。

DDL:

-   `CREATE` : テーブル作成イベント。
-   `RENAME` : テーブルの名前変更イベント。
-   `CINDEX` : インデックス作成イベント。
-   `DINDEX` : インデックス削除イベント。
-   `ERASE` : テーブル削除イベント。
-   `TRUNCATE` : テーブル切り捨てイベント。
-   `ALTER` : 列の追加、列の削除、列の種類の変更、および TiCDC でサポートされているその他の`ALTER TABLE`ステートメントを含む、テーブルの変更イベント。
-   `QUERY` : その他の DDL イベント。

DML:

-   `INSERT` : 挿入イベント。
-   `UPDATE` : 更新イベント。
-   `DELETE` : 削除イベント。

他の：

-   `WATERMARK` : 上流 TiDB クラスターの TSO（64 ビットタイムスタンプ）を含み、テーブルレプリケーションの進行状況を示します。ウォーターマークより前のすべてのイベントは下流に送信されています。
-   `BOOTSTRAP` : ダウンストリームのテーブル スキーマを構築するために使用されるテーブルのスキーマ情報が含まれます。

## メッセージ形式 {#message-format}

Simpleプロトコルでは、各メッセージには1つのイベントのみが含まれます。Simpleプロトコルは、JSON形式とAvro形式のメッセージのエンコードをサポートしています。このドキュメントでは、JSON形式を例として使用します。Avro形式のメッセージの場合、フィールドと意味はJSON形式と同じですが、エンコード形式が異なります。Avro形式の詳細については、 [シンプルプロトコルAvroスキーマ](https://github.com/pingcap/tiflow/blob/release-8.5/pkg/sink/codec/simple/message.json)参照してください。

### DDL {#ddl}

TiCDC は、DDL イベントを次の JSON 形式でエンコードします。

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

上記の JSON データのフィールドについては、次のように説明されています。

| 分野               | タイプ | 説明                                                                                                    |
| ---------------- | --- | ----------------------------------------------------------------------------------------------------- |
| `version`        | 番号  | プロトコルのバージョン番号。現在は`1`です。                                                                               |
| `type`           | 弦   | DDL イベント タイプ ( `CREATE` 、 `RENAME` 、 `CINDEX` 、 `DINDEX` 、 `ERASE` 、 `TRUNCATE` 、 `ALTER` 、 `QUERY` 。 |
| `sql`            | 弦   | DDL ステートメント。                                                                                          |
| `commitTs`       | 番号  | DDL ステートメントの実行がアップストリームで完了したときのコミット タイムスタンプ。                                                          |
| `buildTs`        | 番号  | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。                                                            |
| `tableSchema`    | 物体  | テーブルの現在のスキーマ情報。詳細については、 [TableSchemaの定義](#tableschema-definition)参照してください。                            |
| `preTableSchema` | 物体  | DDL文が実行される前のテーブルのスキーマ情報。1 `CREATE`のDDLイベントを除くすべてのDDLイベントにこのフィールドがあります。                                |

### DML {#dml}

#### 入れる {#insert}

TiCDC は`INSERT`イベントを次の JSON 形式でエンコードします。

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

上記の JSON データのフィールドについては、次のように説明されています。

| 分野              | タイプ | 説明                                              |
| --------------- | --- | ----------------------------------------------- |
| `version`       | 番号  | プロトコルのバージョン番号。現在は`1`です。                         |
| `database`      | 弦   | データベースの名前。                                      |
| `table`         | 弦   | テーブルの名前。                                        |
| `tableID`       | 番号  | テーブルの ID。                                       |
| `type`          | 弦   | DML イベント タイプ`INSERT` 、 `UPDATE` 、 `DELETE`を含む)。 |
| `commitTs`      | 番号  | DML ステートメントの実行がアップストリームで完了したときのコミット タイムスタンプ。    |
| `buildTs`       | 番号  | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。      |
| `schemaVersion` | 番号  | DML メッセージがエンコードされるときのテーブルのスキーマ バージョン番号。         |
| `data`          | 物体  | 挿入されたデータ。フィールド名は列名、フィールド値は列値です。                 |

`INSERT`イベントには`data`フィールドが含まれ、 `old`フィールドは含まれません。

#### アップデート {#update}

TiCDC は`UPDATE`イベントを次の JSON 形式でエンコードします。

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

上記の JSON データのフィールドについては、次のように説明されています。

| 分野              | Type | 説明                                              |
| --------------- | ---- | ----------------------------------------------- |
| `version`       | 番号   | プロトコルのバージョン番号。現在は`1`です。                         |
| `database`      | 弦    | データベースの名前。                                      |
| `table`         | 弦    | テーブルの名前。                                        |
| `tableID`       | 番号   | テーブルの ID。                                       |
| `type`          | 弦    | DML イベント タイプ`INSERT` 、 `UPDATE` 、 `DELETE`を含む)。 |
| `commitTs`      | 番号   | DML ステートメントの実行がアップストリームで完了したときのコミット タイムスタンプ。    |
| `buildTs`       | 番号   | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。      |
| `schemaVersion` | 番号   | DML メッセージがエンコードされるときのテーブルのスキーマ バージョン番号。         |
| `data`          | 物体   | 更新後のデータ。フィールド名は列名、フィールド値は列値です。                  |
| `old`           | 物体   | 更新前のデータ。フィールド名は列名、フィールド値は列値です。                  |

`UPDATE`イベントには、それぞれ更新後のデータと更新前のデータを表す`data`フィールドと`old`フィールドの両方が含まれています。

#### 消去 {#delete}

TiCDC は`DELETE`イベントを次の JSON 形式でエンコードします。

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

上記の JSON データのフィールドについては、次のように説明されています。

| Field           | タイプ | 説明                                              |
| --------------- | --- | ----------------------------------------------- |
| `version`       | 番号  | プロトコルのバージョン番号。現在は`1`です。                         |
| `database`      | 弦   | データベースの名前。                                      |
| `table`         | 弦   | テーブルの名前。                                        |
| `tableID`       | 番号  | テーブルの ID。                                       |
| `type`          | 弦   | DML イベント タイプ`INSERT` 、 `UPDATE` 、 `DELETE`を含む)。 |
| `commitTs`      | 番号  | DML ステートメントの実行がアップストリームで完了したときのコミット タイムスタンプ。    |
| `buildTs`       | 番号  | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。      |
| `schemaVersion` | 番号  | DML メッセージがエンコードされるときのテーブルのスキーマ バージョン番号。         |
| `old`           | 物体  | 削除されたデータ。フィールド名は列名、フィールド値は列値です。                 |

`DELETE`イベントには`old`フィールドが含まれ、 `data`フィールドは含まれません。

### 透かし {#watermark}

TiCDC は`WATERMARK`イベントを次の JSON 形式でエンコードします。

```json
{
   "version":1,
   "type":"WATERMARK",
   "commitTs":447984124732375041,
   "buildTs":1708923816911
}
```

上記の JSON データのフィールドについては、次のように説明されています。

| 分野         | タイプ | 説明                                         |
| ---------- | --- | ------------------------------------------ |
| `version`  | 番号  | プロトコルのバージョン番号。現在は`1`です。                    |
| `type`     | 弦   | `WATERMARK`のイベントタイプ。                       |
| `commitTs` | 番号  | `WATERMARK`のコミット タイムスタンプ。                  |
| `buildTs`  | 番号  | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。 |

### ブートストラップ {#bootstrap}

TiCDC は`BOOTSTRAP`イベントを次の JSON 形式でエンコードします。

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

上記の JSON データのフィールドについては、次のように説明されています。

| 分野            | タイプ | 説明                                                                            |
| ------------- | --- | ----------------------------------------------------------------------------- |
| `version`     | 番号  | プロトコルのバージョン番号。現在は`1`です。                                                       |
| `type`        | 弦   | `BOOTSTRAP`のイベントタイプ。                                                          |
| `commitTs`    | 番号  | `BOOTSTRAP`のうちの`commitTs` `0`です。これはTiCDCによって内部的に生成されるため、 `commitTs`は意味を持ちません。 |
| `buildTs`     | 番号  | TiCDC 内でメッセージが正常にエンコードされたときの UNIX タイムスタンプ。                                    |
| `tableSchema` | 物体  | テーブルのスキーマ情報。詳細については、 [TableSchemaの定義](#tableschema-definition)参照してください。       |

## メッセージ生成と送信ルール {#message-generation-and-sending-rules}

### DDL {#ddl}

-   生成時間: TiCDC は、この DDL イベントの前のすべてのトランザクションが送信された後に DDL イベントを送信します。
-   宛先: TiCDC は、対応するトピックのすべてのパーティションに DDL イベントを送信します。

### DML {#dml}

-   生成時間: TiCDC はトランザクションの`commitTs`順序で DML イベントを送信します。
-   宛先: TiCDC は、ユーザーが設定したディスパッチ ルールに従って、対応するトピックの対応するパーティションに DDL イベントを送信します。

### 透かし {#watermark}

-   生成時間: TiCDC は、変更フィードのレプリケーションの進行状況を示すために、定期的に`WATERMARK`イベントを送信します。現在の間隔は 1 秒です。
-   宛先: TiCDC は、対応するトピックのすべてのパーティションに`WATERMARK`イベントを送信します。

### ブートストラップ {#bootstrap}

-   生成時間:
    -   新しい変更フィードを作成した後、テーブルの最初の DML イベントが送信される前に、TiCDC はテーブル スキーマを構築するために`BOOTSTRAP`イベントをダウンストリームに送信します。
    -   さらに、TiCDCは、新しく参加したコンシューマーがテーブルスキーマを構築できるように、定期的にイベントを`BOOTSTRAP`送信します。デフォルトの送信間隔は120秒または10000メッセージごとです。送信間隔は、 `sink`設定でパラメータ`send-bootstrap-interval-in-sec`と`send-bootstrap-in-msg-count`設定することで調整できます。
    -   テーブルが30分以内に新しいDMLメッセージを受信しない場合、そのテーブルは非アクティブとみなされます。TiCDCは、新しいDMLイベントを受信するまで、そのテーブルへの`BOOTSTRAP`の送信を停止します。
-   送信先: デフォルトでは、TiCDC は対応するトピックのすべてのパーティションに`BOOTSTRAP`イベントを送信します。シンク設定の`send-bootstrap-to-all-partition`番目のパラメータを設定することで、送信戦略を調整できます。

## メッセージの消費方法 {#message-consumption-methods}

TiCDC SimpleプロトコルはDMLメッセージの送信時にテーブルのスキーマ情報を含まないため、ダウンストリームはDMLメッセージを使用する前にDDLまたはBOOTSTRAPメッセージを受信し、テーブルのスキーマ情報をキャッシュする必要があります。ダウンストリームはDMLメッセージを受信すると、DMLメッセージの`table`名前と`schemaVersion`フィールドを検索することで、キャッシュから対応するテーブルスキーマ情報を取得し、DMLメッセージを正しく使用します。

以下では、ダウンストリームがDDLまたはBOOTSTRAPメッセージに基づいてDMLメッセージをどのように処理するかについて説明します。これまでの説明から、以下の情報が判明しています。

-   各 DML メッセージには、DML メッセージに対応するテーブルのスキーマ バージョン番号をマークするための`schemaVersion`フィールドが含まれています。
-   各 DDL メッセージには、DDL イベントの前後のテーブルのスキーマ情報をマークするための`tableSchema`フィールドと`preTableSchema`フィールドが含まれています。
-   各 BOOTSTRAP メッセージには、BOOTSTRAP メッセージに対応するテーブルのスキーマ情報をマークするための`tableSchema`フィールドが含まれています。

消費方法を次の 2 つのシナリオで紹介します。

### シナリオ1: 消費者が最初から消費を始める {#scenario-1-the-consumer-starts-consuming-from-the-beginning}

このシナリオでは、コンシューマーはテーブルの作成から消費を開始するため、テーブルのすべてのDDLメッセージとBOOTSTRAPメッセージを受信できます。この場合、コンシューマーはDMLメッセージの`table`の名前と`schemaVersion`フィールドを通じてテーブルのスキーマ情報を取得できます。詳細なプロセスは以下のとおりです。

![TiCDC Simple Protocol consumer scene 1](/media/ticdc/ticdc-simple-consumer-1.png)

### シナリオ2: 消費者は中間層から消費を始める {#scenario-2-the-consumer-starts-consuming-from-the-middle}

新しいコンシューマーがコンシューマーグループに参加すると、途中から消費を開始する可能性があるため、テーブルの以前のDDLメッセージやBOOTSTRAPメッセージを見逃してしまう可能性があります。この場合、コンシューマーはテーブルのスキーマ情報を取得する前に、いくつかのDMLメッセージを受信する可能性があります。そのため、コンシューマーはテーブルのスキーマ情報を取得するために、DDLメッセージまたはBOOTSTRAPメッセージを受信するまで、一定時間待機する必要があります。TiCDCは定期的にBOOTSTRAPメッセージを送信するため、コンシューマーは常に一定時間内にテーブルのスキーマ情報を取得できます。詳細なプロセスは次のとおりです。

![TiCDC Simple Protocol consumer scene 2](/media/ticdc/ticdc-simple-consumer-2.png)

## 参照 {#reference}

### TableSchemaの定義 {#tableschema-definition}

TableSchemaは、テーブル名、テーブルID、テーブルバージョン番号、列情報、インデックス情報など、テーブルのスキーマ情報を含むJSONオブジェクトです。JSONメッセージの形式は次のとおりです。

```json
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

上記の JSON データの説明は次のとおりです。

| 分野        | タイプ | 説明                                                |
| --------- | --- | ------------------------------------------------- |
| `schema`  | 弦   | データベースの名前。                                        |
| `table`   | 弦   | テーブルの名前。                                          |
| `tableID` | 番号  | テーブルの ID。                                         |
| `version` | 番号  | テーブルのスキーマ バージョン番号。                                |
| `columns` | 配列  | 列名、データ型、null が可能かどうか、デフォルト値などの列情報。                |
| `indexes` | 配列  | インデックス名、インデックスが一意かどうか、主キーかどうか、インデックス列などのインデックス情報。 |

テーブル名とスキーマ バージョン番号によって、テーブルのスキーマ情報を一意に識別できます。

> **注記：**
>
> TiDB の実装上の制限により、 `RENAME TABLE` DDL 操作を実行しても、テーブルのスキーマ バージョン番号は変更されません。

#### カラムの定義 {#column-definition}

カラムは、列名、データ型、null が可能かどうか、デフォルト値など、列のスキーマ情報を含む JSON オブジェクトです。

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

上記の JSON データの説明は次のとおりです。

| 分野         | タイプ  | 説明                                     |
| ---------- | ---- | -------------------------------------- |
| `name`     | 弦    | 列の名前。                                  |
| `dataType` | 物体   | MySQL データ型、文字セット、照合順序、フィールド長などのデータ型情報。 |
| `nullable` | ブール値 | 列が null にできるかどうか。                      |
| `default`  | 弦    | 列のデフォルト値。                              |

#### インデックスの定義 {#index-definition}

インデックスは、インデックス名、インデックスが一意かどうか、主キーかどうか、インデックス列などのインデックスのスキーマ情報を含む JSON オブジェクトです。

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

上記の JSON データの説明は次のとおりです。

| 分野         | タイプ   | 説明                     |
| ---------- | ----- | ---------------------- |
| `name`     | 弦     | インデックスの名前。             |
| `unique`   | ブール値  | インデックスが一意であるかどうか。      |
| `primary`  | ブール値  | インデックスが主キーであるかどうか。     |
| `nullable` | ブール値  | インデックスが null にできるかどうか。 |
| `columns`  | Array | インデックスに含まれる列名。         |

### mysqlType 参照テーブル {#mysqltype-reference-table}

以下の表は、TiCDC Simpleプロトコルの`mysqlType`のフィールドの値の範囲と、TiDB（Golang）およびAvro（Java）におけるその型を示しています。DMLメッセージを解析する必要がある場合は、使用するプロトコルと言語に応じて、この表とDMLメッセージの`mysqlType`のフィールドに従ってデータを正しく解析できます。

**TiDB型（Golang）は、** TiDBおよびTiCDC（Golang）で処理された際の対応する`mysqlType`の型を表します。Avro**型（Java）は、** Avro形式のメッセージにエンコードされた際の対応する`mysqlType`の型を表します。

| mysqlタイプ           | 値の範囲                                        | TiDB型（Golang） | Avro型（Java） |
| ------------------ | ------------------------------------------- | ------------- | ----------- |
| タイニーイント            | [-128, 127]                                 | int64         | 長さ          |
| tinyint 符号なし       | [0, 255]                                    | uint64        | 長さ          |
| スモールインテンス          | [-32768, 32767]                             | int64         | 長さ          |
| 符号なし小整数            | [0, 65535]                                  | uint64        | 長さ          |
| 中程度                | [-8388608, 8388607]                         | int64         | 長さ          |
| mediumint unsigned | [0, 16777215]                               | uint64        | 長さ          |
| 整数                 | [-2147483648, 2147483647]                   | int64         | 長さ          |
| 符号なし整数             | [0, 4294967295]                             | uint64        | 長さ          |
| ビッグインテント           | [-9223372036854775808, 9223372036854775807] | int64         | 長さ          |
| bigint 符号なし        | [0, 9223372036854775807]                    | uint64        | 長さ          |
| bigint 符号なし        | [9223372036854775808, 18446744073709551615] | uint64        | 弦           |
| フロート               | /                                           | float32       | フロート        |
| ダブル                | /                                           | フロート64        | ダブル         |
| 小数点                | /                                           | 弦             | 弦           |
| varchar            | /                                           | []uint8       | 弦           |
| チャー                | /                                           | []uint8       | 弦           |
| varbinary          | /                                           | []uint8       | バイト         |
| バイナリ               | /                                           | []uint8       | バイト         |
| 小さなテキスト            | /                                           | []uint8       | 弦           |
| 文章                 | /                                           | []uint8       | 弦           |
| 中程度のテキスト           | /                                           | []uint8       | 弦           |
| 長文                 | /                                           | []uint8       | 弦           |
| 小さな塊               | /                                           | []uint8       | バイト         |
| ブロブ                | /                                           | []uint8       | バイト         |
| 中くらいの塊             | /                                           | []uint8       | バイト         |
| ロングブロブ             | /                                           | []uint8       | バイト         |
| 日付                 | /                                           | 弦             | 弦           |
| 日時                 | /                                           | 弦             | 弦           |
| タイムスタンプ            | /                                           | 弦             | 弦           |
| 時間                 | /                                           | 弦             | 弦           |
| 年                  | /                                           | int64         | 長さ          |
| 列挙型                | /                                           | uint64        | 長さ          |
| セット                | /                                           | uint64        | 長さ          |
| 少し                 | /                                           | uint64        | 長さ          |
| JSON               | /                                           | 弦             | 弦           |
| ブール                | /                                           | int64         | 長さ          |
| TiDBベクターフロート32     | /                                           | 弦             | 弦           |

### Avroスキーマ定義 {#avro-schema-definition}

Simpleプロトコルは、Avro形式でのメッセージ出力をサポートしています。Avro形式の詳細については、 [シンプルプロトコルAvroスキーマ](https://github.com/pingcap/tiflow/blob/release-8.5/pkg/sink/codec/simple/message.json)参照してください。
