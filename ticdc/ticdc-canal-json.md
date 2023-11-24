---
title: TiCDC Canal-JSON Protocol
summary: Learn the concept of TiCDC Canal-JSON Protocol and how to use it.
---

# TiCDC Canal-JSON プロトコル {#ticdc-canal-json-protocol}

Canal-JSON は、 [アリババ運河](https://github.com/alibaba/canal)によって定義されたデータ交換形式のプロトコルです。このドキュメントでは、TiDB 拡張フィールド、Canal-JSON データ形式の定義、公式 Canal との比較など、Canal-JSON データ形式が TiCDC でどのように実装されているかを学ぶことができます。

## Canal-JSON を使用する {#use-canal-json}

Message Queue (MQ) をダウンストリーム シンクとして使用する場合、 `sink-uri`で Canal-JSON を指定できます。 TiCDC は、Event を基本単位として Canal-JSON メッセージをラップして構築し、TiDB データ変更イベントをダウンストリームに送信します。

イベントには 3 つのタイプがあります。

-   DDL イベント: DDL 変更レコードを表します。これは、上流の DDL ステートメントが正常に実行された後に送信されます。 DDL イベントは、インデックスが 0 の MQ パーティションに送信されます。
-   DML イベント: 行データ変更レコードを表します。このタイプのイベントは、行の変更が発生したときに送信されます。これには、変更が発生した後の行に関する情報が含まれます。
-   WATERMARK イベント: 特別な時点を表します。これは、この時点より前に受信したイベントが完了したことを示します。 TiDB 拡張フィールドにのみ適用され、 `sink-uri`に`enable-tidb-extension` ～ `true`を設定すると有効になります。

以下は`Canal-JSON`の使用例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json"
```

## TiDB 拡張フィールド {#tidb-extension-field}

Canal-JSON プロトコルは、もともと MySQL 用に設計されました。これには、CommitTS トランザクションの TiDB 固有の一意識別子などの重要なフィールドは含まれません。この問題を解決するために、TiCDC は TiDB 拡張フィールドを Canal-JSON プロトコル形式に追加します。 `sink-uri`で`enable-tidb-extension` ～ `true` (デフォルトでは`false` ) を設定すると、TiCDC は Canal-JSON メッセージを生成するときに次のように動作します。

-   TiCDC は、 `_tidb`という名前のフィールドを含む DML イベント メッセージと DDL イベント メッセージを送信します。
-   TiCDC は WATERMARK イベント メッセージを送信します。

以下は例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json-enable-tidb-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json&enable-tidb-extension=true"
```

## メッセージフォーマットの定義 {#definitions-of-message-formats}

このセクションでは、DDL イベント、DML イベント、WATERMARK イベントの形式と、コンシューマー側でデータがどのように解決されるかについて説明します。

### DDLイベント {#ddl-event}

TiCDC は、DDL イベントを次の Canal-JSON 形式にエンコードします。

```json
{
    "id": 0,
    "database": "test",
    "table": "",
    "pkNames": null,
    "isDdl": true,
    "type": "QUERY",
    "es": 1639633094670,
    "ts": 1639633095489,
    "sql": "drop database if exists test",
    "sqlType": null,
    "mysqlType": null,
    "data": null,
    "old": null,
    "_tidb": {     // TiDB extension field
        "commitTs": 163963309467037594
    }
}
```

フィールドについては次のように説明します。

| 分野       | タイプ | 説明                                                                                                      |
| :------- | :-- | :------------------------------------------------------------------------------------------------------ |
| ID       | 番号  | TiCDC のデフォルト値は 0 です。                                                                                    |
| データベース   | 弦   | 行が存在するデータベースの名前                                                                                         |
| テーブル     | 弦   | 行が配置されているテーブルの名前                                                                                        |
| PKNames  | 配列  | 主キーを構成するすべての列の名前                                                                                        |
| はDdl     | ブール | メッセージが DDL イベントであるかどうか                                                                                  |
| タイプ      | 弦   | Canal-JSON で定義されたイベント タイプ                                                                               |
| エス       | 番号  | メッセージを生成したイベントが発生したときの 13 ビット (ミリ秒) のタイムスタンプ                                                            |
| ts       | 番号  | TiCDC がメッセージを生成したときの 13 ビット (ミリ秒) のタイムスタンプ                                                              |
| SQL      | 弦   | isDdl が`true`の場合、対応する DDL ステートメントを記録します                                                                 |
| SQLタイプ   | 物体  | isDdl が`false`の場合、各列のデータ型がJavaでどのように表現されるかを記録します。                                                       |
| mysqlタイプ | 物体  | isDdl が`false`の場合、各列のデータ型が MySQL でどのように表現されるかを記録します。                                                    |
| データ      | 物体  | isDdl が`false`の場合、各列の名前とそのデータ値を記録します。                                                                   |
| 古い       | 物体  | メッセージが更新イベントによって生成された場合のみ、更新前の各列の名前とデータ値が記録されます。                                                        |
| _tidb    | 物体  | TiDB 拡張フィールド。 `enable-tidb-extension` ～ `true`を設定した場合にのみ存在します。値`commitTs`は、行の変更を引き起こしたトランザクションの TSO です。 |

### DMLイベント {#dml-event}

TiCDC は、DML データ変更イベントの行を次のようにエンコードします。

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "c_bigint": -5,
        "c_int": 4,
        "c_mediumint": 4,
        "c_smallint": 5,
        "c_tinyint": -6,
        "id": 4
    },
    "mysqlType": {
        "c_bigint": "bigint",
        "c_int": "int",
        "c_mediumint": "mediumint",
        "c_smallint": "smallint",
        "c_tinyint": "tinyint",
        "id": "int"
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "2147483647",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "127",
            "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB extension field
        "commitTs": 163963314122145239
    }
}
```

### ウォーターマークイベント {#watermark-event}

TiCDC は、 `enable-tidb-extension` ～ `true`に設定した場合にのみ WATERMARK イベントを送信します。 `type`フィールドの値は`TIDB_WATERMARK`です。イベントには`_tidb`フィールドが含まれており、このフィールドにはパラメータ`watermarkTs`が 1 つだけ含まれています。値`watermarkTs`は、イベントの送信時に記録される TSO です。

このタイプのイベントを受信すると、 `watermarkTs`未満の`commitTs`を持つすべてのイベントが送信されています。 TiCDC は「At Least Once」セマンティクスを提供するため、データは繰り返し送信される可能性があります。 `watermarkTs`未満の`commitTs`を含む後続のイベントを受信した場合は、このイベントを無視しても問題ありません。

以下は WATERMARK イベントの例です。

```json
{
    "id": 0,
    "database": "",
    "table": "",
    "pkNames": null,
    "isDdl": false,
    "type": "TIDB_WATERMARK",
    "es": 1640007049196,
    "ts": 1640007050284,
    "sql": "",
    "sqlType": null,
    "mysqlType": null,
    "data": null,
    "old": null,
    "_tidb": {     // TiDB extension field
        "watermarkTs": 429918007904436226
    }
}
```

### 消費者側のデータ解決 {#data-resolution-on-the-consumer-side}

上の例からわかるように、Canal-JSON には統一されたデータ形式があり、イベント タイプごとにフィールド入力ルールが異なります。統一された方法を使用してこの JSON 形式のデータを解決し、フィールド値を確認してイベント タイプを決定できます。

-   `isDdl`が`true`の場合、メッセージには DDL イベントが含まれます。
-   `isDdl`が`false`場合、さらに`type`フィールドを確認する必要があります。 `type`が`TIDB_WATERMARK`の場合、それは WATERMARK イベントです。それ以外の場合は、DML イベントです。

## フィールドの説明 {#field-descriptions}

Canal-JSON 形式では、 `mysqlType`フィールドと`sqlType`フィールドに対応するデータ型が記録されます。

### 「MySQL タイプ」フィールド {#mysql-type-field}

`mysqlType`フィールドには、Canal-JSON 形式で各列に MySQL Type の文字列が記録されます。詳細については、 [TiDB データ型](/data-type-overview.md)を参照してください。

### 「SQL タイプ」フィールド {#sql-type-field}

`sqlType`フィールドには、Canal-JSON 形式で各列のJava SQL Type が記録されます。これは、JDBC のデータに対応するデータ型です。その値は、MySQL タイプと特定のデータ値によって計算できます。マッピングは次のとおりです。

| MySQLのタイプ | Java SQL タイプ コード |
| :-------- | :--------------- |
| ブール値      | -6               |
| 浮く        | 7                |
| ダブル       | 8                |
| 10進数      | 3                |
| シャア       | 1                |
| バーチャー     | 12               |
| バイナリ      | 2004年            |
| ヴァルバイナリ   | 2004年            |
| タイニーテキスト  | 2005年            |
| 文章        | 2005年            |
| ミディアムテキスト | 2005年            |
| 長文        | 2005年            |
| 小さな塊      | 2004年            |
| ブロブ       | 2004年            |
| ミディアムブロブ  | 2004年            |
| ロングブロブ    | 2004年            |
| 日付        | 91               |
| 日付時刻      | 93               |
| タイムスタンプ   | 93               |
| 時間        | 92               |
| 年         | 12               |
| 列挙型       | 4                |
| セット       | -7               |
| 少し        | -7               |
| JSON      | 12               |

## 整数型 {#integer-types}

次の表に示すように、 [整数型](/data-type-numeric.md#integer-types)に`Unsigned`制約があるかどうかと、さまざまなJava SQL タイプ コードにそれぞれ対応する値のサイズを考慮する必要があります。

| MySQLの型文字列    | 値の範囲                                       | Java SQL タイプ コード |
| :------------ | :----------------------------------------- | :--------------- |
| タイニーント        | [-128、127]                                 | -6               |
| tinyint 署名なし  | [0,127]                                    | -6               |
| tinyint 署名なし  | [128、255]                                  | 5                |
| smallint      | [-32768、32767]                             | 5                |
| smallint 署名なし | [0, 32767]                                 | 5                |
| smallint 署名なし | [32768、65535]                              | 4                |
| 中程度の          | [-8388608、8388607]                         | 4                |
| 署名されていない中程度の  | [0, 8388607]                               | 4                |
| 署名されていない中程度の  | [8388608、16777215]                         | 4                |
| 整数            | [-2147483648、2147483647]                   | 4                |
| 符号なし整数        | [0、2147483647]                             | 4                |
| int 符号なし      | [2147483648、4294967295]                    | -5               |
| ビギント          | [-9223372036854775808、9223372036854775807] | -5               |
| bigint 署名なし   | [0, 9223372036854775807]                   | -5               |
| bigint 署名なし   | [9223372036854775808、18446744073709551615] | 3                |

次の表は、TiCDC のJava SQL タイプとそのコード間のマッピング関係を示しています。

| Java SQL タイプ | Java SQL タイプ コード |
| :----------- | :--------------- |
| チャー          | 1                |
| 10進数         | 3                |
| 整数           | 4                |
| スモールント       | 5                |
| 本物           | 7                |
| ダブル          | 8                |
| VARCHAR      | 12               |
| 日付           | 91               |
| 時間           | 92               |
| タイムスタンプ      | 93               |
| BLOB         | 2004年            |
| クロブ          | 2005年            |
| BIGINT       | -5               |
| タイイント        | -6               |
| 少し           | -7               |

Java SQL タイプの詳細については、 [Java SQL クラスの型](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)を参照してください。

## TiCDC Canal-JSON と公式 Canal の比較 {#comparison-of-ticdc-canal-json-and-the-official-canal}

TiCDC が`Update`イベントと`mysqlType`フィールドを含む Canal-JSON データ形式を実装する方法は、公式の Canal とは異なります。次の表に主な違いを示します。

| アイテム             | TiCDC Canal-JSON                                                                                             | 運河                               |
| :--------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `Update`種類のイベント  | デフォルトでは、 `old`フィールドにはすべての列データが含まれます。 `only_output_updated_columns`が`true`の場合、 `old`フィールドには変更された列データのみが含まれます。 | `old`フィールドには、変更された列データのみが含まれます   |
| `mysqlType`フィールド | パラメータ付きの型の場合、型パラメータの情報は含まれません。                                                                               | パラメータ付きの型の場合、型パラメータの完全な情報が含まれます。 |

### <code>Update</code>タイプのイベント {#event-of-code-update-code-type}

`Update`種類のイベントの場合:

-   TiCDC では、 `old`フィールドにすべての列データが含まれます
-   公式 Canal では、 `old`フィールドには変更された列データのみが含まれます

次の SQL ステートメントが上流の TiDB で順次実行されると仮定します。

```sql
create table tp_int
(
    id          int auto_increment,
    c_tinyint   tinyint   null,
    c_smallint  smallint  null,
    c_mediumint mediumint null,
    c_int       int       null,
    c_bigint    bigint    null,
    constraint pk
        primary key (id)
);

insert into tp_int(c_tinyint, c_smallint, c_mediumint, c_int, c_bigint)
values (127, 32767, 8388607, 2147483647, 9223372036854775807);

update tp_int set c_int = 0, c_tinyint = 0 where c_smallint = 32767;
```

`update`ステートメントの場合、TiCDC は、以下に示すように、 `type`を`UPDATE`として持つイベント メッセージを出力します。 `update`ステートメントは`c_int`と`c_tinyint`列のみを変更します。出力イベント メッセージの`old`フィールドには、すべての列データが含まれます。

```json
{
    "id": 0,
    ...
    "type": "UPDATE",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "0",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "0",
            "id": "2"
        }
    ],
    "old": [                              // In TiCDC, this field contains all the column data.
        {
            "c_bigint": "9223372036854775807",
            "c_int": "2147483647",        // Modified column
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "127",           // Modified column
            "id": "2"
        }
    ]
}
```

公式 Canal の場合、以下に示すように、出力イベント メッセージの`old`フィールドには、変更された列データのみが含まれます。

```json
{
    "id": 0,
    ...
    "type": "UPDATE",
    ...
    "sqlType": {
        ...
    },
    "mysqlType": {
        ...
    },
    "data": [
        {
            "c_bigint": "9223372036854775807",
            "c_int": "0",
            "c_mediumint": "8388607",
            "c_smallint": "32767",
            "c_tinyint": "0",
            "id": "2"
        }
    ],
    "old": [                              // In Canal, this field contains only the modified column data.
        {
            "c_int": "2147483647",        // Modified column
            "c_tinyint": "127",           // Modified column
        }
    ]
}
```

### <code>mysqlType</code>フィールド {#code-mysqltype-code-field}

`mysqlType`フィールドの場合、型にパラメータが含まれる場合、公式の Canal には型パラメータの完全な情報が含まれます。 TiCDC にはそのような情報は含まれていません。

次の例では、テーブル定義 SQL ステートメントに、 `decimal` 、 `char` 、 `varchar` 、 `enum`などの各列のパラメーターが含まれています。 TiCDC と公式 Canal によって生成された Canal-JSON 形式を比較すると、TiCDC の`mysqlType`フィールドには基本的な MySQL 情報のみが含まれていることがわかります。 type パラメータの完全な情報が必要な場合は、他の方法で実装する必要があります。

次の SQL ステートメントが上流の TiDB で順次実行されると仮定します。

```sql
create table t (
    id     int auto_increment,
    c_decimal    decimal(10, 4) null,
    c_char       char(16)      null,
    c_varchar    varchar(16)   null,
    c_binary     binary(16)    null,
    c_varbinary  varbinary(16) null,
    c_enum enum('a','b','c') null,
    c_set  set('a','b','c')  null,
    c_bit  bit(64)            null,
    constraint pk
        primary key (id)
);

insert into t (c_decimal, c_char, c_varchar, c_binary, c_varbinary, c_enum, c_set, c_bit)
values (123.456, "abc", "abc", "abc", "abc", 'a', 'a,b', b'1000001');
```

TiCDC の出力は次のとおりです。

```json
{
    "id": 0,
    ...
    "isDdl": false,
    "sqlType": {
        ...
    },
    "mysqlType": {
        "c_binary": "binary",
        "c_bit": "bit",
        "c_char": "char",
        "c_decimal": "decimal",
        "c_enum": "enum",
        "c_set": "set",
        "c_varbinary": "varbinary",
        "c_varchar": "varchar",
        "id": "int"
    },
    "data": [
        {
            ...
        }
    ],
    "old": null,
}
```

公式運河の出力は次のとおりです。

```json
{
    "id": 0,
    ...
    "isDdl": false,
    "sqlType": {
        ...
    },
    "mysqlType": {
        "c_binary": "binary(16)",
        "c_bit": "bit(64)",
        "c_char": "char(16)",
        "c_decimal": "decimal(10, 4)",
        "c_enum": "enum('a','b','c')",
        "c_set": "set('a','b','c')",
        "c_varbinary": "varbinary(16)",
        "c_varchar": "varchar(16)",
        "id": "int"
    },
    "data": [
        {
            ...
        }
    ],
    "old": null,
}
```

## TiCDC Canal-JSON の変更点 {#changes-in-ticdc-canal-json}

### <code>Delete</code>イベントの<code>Old</code>フィールドの変更 {#changes-in-the-code-old-code-field-of-the-code-delete-code-events}

v5.4.0より、 `Delete`イベントのうちの`old`フィールドが変更されました。

以下は`Delete`イベント メッセージです。 v5.4.0 より前では、 `old`フィールドには「データ」フィールドと同じ内容が含まれています。 v5.4.0 以降のバージョンでは、 `old`フィールドは null に設定されます。 「データ」フィールドを使用して、削除されたデータを取得できます。

    {
        "id": 0,
        "database": "test",
        ...
        "type": "DELETE",
        ...
        "sqlType": {
            ...
        },
        "mysqlType": {
            ...
        },
        "data": [
            {
                "c_bigint": "9223372036854775807",
                "c_int": "0",
                "c_mediumint": "8388607",
                "c_smallint": "32767",
                "c_tinyint": "0",
                "id": "2"
            }
        ],
        "old": null,
        // The following is an example before v5.4.0. The `old` field contains the same content as the "data" field.
        "old": [
            {
                "c_bigint": "9223372036854775807",
                "c_int": "0",
                "c_mediumint": "8388607",
                "c_smallint": "32767",
                "c_tinyint": "0",
                "id": "2"
            }
        ]
    }
