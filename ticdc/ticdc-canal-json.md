---
title: TiCDC Canal-JSON Protocol
summary: TiCDC Canal-JSON プロトコルの概念とその使用方法を学びます。
---

# TiCDC Canal-JSON プロトコル {#ticdc-canal-json-protocol}

Canal-JSON は、 [アリババ運河](https://github.com/alibaba/canal)で定義されたデータ交換形式プロトコルです。このドキュメントでは、TiDB 拡張フィールド、Canal-JSON データ形式の定義、公式 Canal との比較など、TiCDC で Canal-JSON データ形式がどのように実装されているかについて説明します。

## Canal-JSONを使用する {#use-canal-json}

下流のシンクとしてメッセージキュー（MQ）を使用する場合、 `sink-uri`で Canal-JSON を指定できます。TiCDC は、イベントを基本単位として Canal-JSON メッセージをラップして構築し、TiDB データ変更イベントを下流に送信します。

イベントには 3 つの種類があります。

-   DDL イベント: DDL 変更レコードを表します。上流の DDL ステートメントが正常に実行された後に送信されます。DDL イベントは、インデックスが 0 の状態で MQ パーティションに送信されます。
-   DML イベント: 行データ変更レコードを表します。このタイプのイベントは、行の変更が発生したときに送信されます。変更が発生した後の行に関する情報が含まれます。
-   ウォーターマーク イベント: 特別な時点を表します。この時点より前に受信したイベントが完了していることを示します。これは TiDB 拡張フィールドにのみ適用され、 `sink-uri`で`enable-tidb-extension` ～ `true`設定すると有効になります。

以下は`Canal-JSON`の使用例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json"
```

## TiDB拡張フィールド {#tidb-extension-field}

Canal-JSON プロトコルは、もともと MySQL 用に設計されています。CommitTS トランザクションの TiDB 固有の一意の識別子などの重要なフィールドは含まれていません。この問題を解決するために、TiCDC は Canal-JSON プロトコル形式に TiDB 拡張フィールドを追加します`sink-uri`で`enable-tidb-extension`を`true` (デフォルトは`false` ) に設定すると、TiCDC は Canal-JSON メッセージを生成するときに次のように動作します。

-   TiCDC は、 `_tidb`という名前のフィールドを含む DML イベント メッセージと DDL イベント メッセージを送信します。
-   TiCDC は WATERMARK イベント メッセージを送信します。

次に例を示します。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json-enable-tidb-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json&enable-tidb-extension=true"
```

## メッセージ形式の定義 {#definitions-of-message-formats}

このセクションでは、DDL イベント、DML イベント、ウォーターマーク イベントの形式と、コンシューマー側でデータが解決される方法について説明します。

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
        "commitTs": 429918007904436226  // A TiDB TSO timestamp
    }
}
```

各フィールドの説明は以下のとおりです。

| 分野       | タイプ | 説明                                                                                                      |
| :------- | :-- | :------------------------------------------------------------------------------------------------------ |
| id       | 番号  | TiCDC ではデフォルト値は 0 です。                                                                                   |
| データベース   | 弦   | 行が配置されているデータベースの名前                                                                                      |
| テーブル     | 弦   | 行が配置されているテーブルの名前                                                                                        |
| pkNames  | 配列  | 主キーを構成するすべての列の名前                                                                                        |
| DDl です   | ブール | メッセージがDDLイベントであるかどうか                                                                                    |
| タイプ      | 弦   | Canal-JSON で定義されたイベント タイプ                                                                               |
| es       | 番号  | メッセージを生成したイベントが発生したときの 13 ビット (ミリ秒) のタイムスタンプ                                                            |
| ts       | 番号  | TiCDC がメッセージを生成した 13 ビット (ミリ秒) のタイムスタンプ                                                                 |
| SQL文     | 弦   | isDdlが`true`の場合、対応するDDL文を記録する                                                                           |
| sqlタイプ   | 物体  | isDdlが`false`の場合、各列のデータ型がJavaでどのように表現されるかを記録します。                                                        |
| mysqlタイプ | 物体  | isDdlが`false`の場合、各列のデータ型がMySQLでどのように表現されるかを記録します。                                                       |
| データ      | 物体  | isDdlが`false`の場合、各列の名前とそのデータ値を記録します。                                                                    |
| 古い       | 物体  | メッセージが更新イベントによって生成された場合にのみ、更新前の各列の名前とデータ値を記録します。                                                        |
| _tidb さん | 物体  | TiDB 拡張フィールド。 `enable-tidb-extension` `true`に設定した場合にのみ存在します。 `commitTs`の値は、行の変更を引き起こしたトランザクションの TSO です。 |

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
        "commitTs": 429918007904436226  // A TiDB TSO timestamp
    }
}
```

### ウォーターマークイベント {#watermark-event}

TiCDC は、 `enable-tidb-extension`を`true`に設定した場合にのみ WATERMARK イベントを送信します。 `type`フィールドの値は`TIDB_WATERMARK`です。イベントには`_tidb`フィールドが含まれ、フィールドには 1 つのパラメータ`watermarkTs`のみが含まれます。 `watermarkTs`の値は、イベントが送信されたときに記録される TSO です。

このタイプのイベントを受信すると、 `commitTs`が`watermarkTs`より小さいすべてのイベントが送信されています。TiCDC は「少なくとも 1 回」セマンティクスを提供するため、データが繰り返し送信される可能性があります。5 `watermarkTs` `commitTs`後続のイベントを受信した場合、このイベントを無視しても問題ありません。

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
        "watermarkTs": 429918007904436226  // A TiDB TSO timestamp
    }
}
```

### 消費者側のデータ解決 {#data-resolution-on-the-consumer-side}

上記の例からわかるように、Canal-JSON には統一されたデータ形式があり、イベントの種類ごとに異なるフィールド入力ルールがあります。統一された方法を使用してこの JSON 形式のデータを解決し、フィールド値をチェックしてイベントの種類を判別できます。

-   `isDdl`が`true`場合、メッセージには DDL イベントが含まれます。
-   `isDdl`が`false`場合、 `type`フィールドをさらに確認する必要があります。 `type`が`TIDB_WATERMARK`場合、それは WATERMARK イベントです。それ以外の場合は、DML イベントです。

## フィールドの説明 {#field-descriptions}

Canal-JSON 形式では、対応するデータ型が`mysqlType`フィールドと`sqlType`フィールドに記録されます。

### MySQL タイプフィールド {#mysql-type-field}

`mysqlType`フィールドには、Canal-JSON 形式で各列の MySQL Type の文字列が記録されます。詳細については、 [TiDB データ型](/data-type-overview.md)参照してください。

### SQL タイプ フィールド {#sql-type-field}

Canal-JSON 形式は、 `sqlType`フィールドに各列のJava SQL タイプを記録します。これは、JDBC のデータに対応するデータ型です。その値は、MySQL タイプと特定のデータ値によって計算できます。マッピングは次のとおりです。

| MySQL タイプ | Java SQL 型コード |
| :-------- | :------------ |
| ブール       | -6            |
| フロート      | 7             |
| ダブル       | 8             |
| 小数点       | 3             |
| チャー       | 1             |
| ヴァルチャー    | 12            |
| バイナリ      | 2004          |
| バイナリ      | 2004          |
| 小さなテキスト   | 2005          |
| 文章        | 2005          |
| 中文        | 2005          |
| 長文        | 2005          |
| 小さな塊      | 2004          |
| ブロブ       | 2004          |
| ミディアムブロブ  | 2004          |
| ロングブロブ    | 2004          |
| 日付        | 91            |
| 日時        | 93            |
| タイムスタンプ   | 93            |
| 時間        | 92            |
| 年         | 12            |
| 列挙型       | 4             |
| セット       | -7            |
| 少し        | -7            |
| 翻訳        | 12            |

## 整数型 {#integer-types}

次の表に示すように、それぞれ異なるJava SQL 型コードに対応する[整数型](/data-type-numeric.md#integer-types) `Unsigned`制約と値のサイズがあるかどうかを考慮する必要があります。

| MySQL 型 文字列    | 値の範囲                                       | Java SQL 型コード |
| :------------- | :----------------------------------------- | :------------ |
| ちっちゃい          | [-128, 127]                                | -6            |
| tinyint 符号なし   | [0, 127]                                   | -6            |
| tinyint 符号なし   | [128、255]                                  | 5             |
| 小さい整数          | [-32768, 32767]                            | 5             |
| 符号なし小整数        | [0, 32767]                                 | 5             |
| 符号なし小整数        | [32768, 65535]                             | 4             |
| 中程度            | [-8388608, 8388607]                        | 4             |
| mediumint 符号なし | [0, 8388607]                               | 4             |
| mediumint 符号なし | [8388608, 16777215]                        | 4             |
| 整数             | [-2147483648, 2147483647]                  | 4             |
| 符号なし整数         | [0, 2147483647]                            | 4             |
| 符号なし整数         | [2147483648, 4294967295]                   | -5            |
| ビッグイント         | [-9223372036854775808、9223372036854775807] | -5            |
| bigint 符号なし    | [0, 9223372036854775807]                   | -5            |
| bigint 符号なし    | [9223372036854775808、18446744073709551615] | 3             |

次の表は、TiCDC のJava SQL タイプとそのコード間のマッピング関係を示しています。

| Java SQL タイプ | Java SQL 型コード |
| :----------- | :------------ |
| 文字           | 1             |
| 小数点          | 3             |
| 整数           | 4             |
| スモールイント      | 5             |
| 本物           | 7             |
| ダブル          | 8             |
| バルチャー        | 12            |
| 日付           | 91            |
| 時間           | 92            |
| タイムスタンプ      | 93            |
| ブロブ          | 2004          |
| クローブ         | 2005          |
| ビッグイント       | -5            |
| 小さな          | -6            |
| 少し           | -7            |

Java SQL 型の詳細については、 [Java SQL クラス タイプ](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)参照してください。

## バイナリとBlob型 {#binary-and-blob-types}

TiCDC は、次のように各バイトを文字表現に変換して、Canal-JSON 形式で[バイナリタイプ](/data-type-string.md#binary-type)エンコードします。

-   印刷可能な文字は、ISO/IEC 8859-1 文字エンコーディングを使用して表されます。
-   印刷できない文字や HTML で特別な意味を持つ特定の文字は、UTF-8 エスケープ シーケンスを使用して表されます。

次の表に詳細な表現情報を示します。

| 文字の種類              | 値の範囲      | キャラクター表現                          |
| :----------------- | :-------- | :-------------------------------- |
| 制御文字               | [0, 31]   | UTF-8エスケープ（ `\u0000`から`\u001F`など） |
| 水平タブ               | [9]       | `\t`                              |
| 改行                 | [10]      | `\n`                              |
| キャリッジリターン          | [13]      | `\r`                              |
| 印刷可能な文字            | [32、127]  | リテラル文字（ `A`など）                    |
| アンパサンド             | [38]      | `\u0026`                          |
| 小なり記号              | [60]      | `\u0038`                          |
| 大なり記号              | [62]      | `\u003E`                          |
| 拡張制御文字             | [128、159] | 文字                                |
| ISO 8859-1 (ラテン 1) | [160、255] | 文字                                |

### エンコードの例 {#example-of-the-encoding}

たとえば、 `c_varbinary`という`VARBINARY`列に格納されている次の 16 バイト`[5 7 10 15 36 50 43 99 120 60 38 255 254 45 55 70]` 、Canal-JSON `Update`イベントで次のようにエンコードされます。

```json
{
    ...
    "data": [
        {
            ...
            "c_varbinary": "\u0005\u0007\n\u000f$2+cx\u003c\u0026ÿþ-7F"
        }
    ]
    ...
}
```

## TiCDC Canal-JSONと公式Canalの比較 {#comparison-of-ticdc-canal-json-and-the-official-canal}

TiCDC が Canal-JSON データ形式を実装する方法 ( `Update`イベントと`mysqlType`フィールドを含む) は、公式の Canal とは異なります。次の表に主な違いを示します。

| アイテム             | TiCDC Canal-JSON                                                                                            | 運河                               |
| :--------------- | :---------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `Update`種類のイベント  | デフォルトでは、 `old`フィールドにすべての列データが含まれます。 `only_output_updated_columns`が`true`の場合、 `old`フィールドには変更された列データのみが含まれます。 | `old`フィールドには変更された列データのみが含まれます    |
| `mysqlType`フィールド | パラメータを持つ型の場合、型パラメータの情報は含まれません。                                                                              | パラメータを持つ型の場合、型パラメータの完全な情報が含まれます。 |

### 公式Canalとの互換性 {#compatibility-with-the-official-canal}

v6.5.6、v7.1.3、v7.6.0 以降、 TiCDC Canal-JSON は公式 Canal のデータ形式との互換性をサポートしています。changefeed を作成するときに、 `sink-uri`のうち`content-compatible=true`設定すると、この機能が有効になります。このモードでは、TiCDC は公式 Canal と互換性のある Canal-JSON 形式のデータを出力します。具体的な変更点は次のとおりです。

-   `mysqlType`フィールドには、各タイプのタイプ パラメータの完全な情報が含まれています。
-   `Update`タイプのイベントは、変更された列データのみを出力します。

### <code>Update</code>タイプのイベント {#event-of-code-update-code-type}

`Update`種類のイベントの場合:

-   TiCDCでは、 `old`フィールドにすべての列データが含まれます。
-   公式Canalでは、 `old`フィールドには変更された列データのみが含まれます。

次の SQL ステートメントがアップストリーム TiDB で順番に実行されると仮定します。

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

`update`ステートメントの場合、TiCDC は以下に示すように、 `type` `UPDATE`としてイベント メッセージを出力します。 `update`ステートメントは、 `c_int`列と`c_tinyint`列のみを変更します。出力イベント メッセージの`old`フィールドには、すべての列データが含まれます。

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

公式 Canal の場合、出力イベント メッセージの`old`フィールドには、以下に示すように、変更された列データのみが含まれます。

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

`mysqlType`フィールドの場合、型にパラメータが含まれている場合、公式の Canal には型パラメータの完全な情報が含まれます。TiCDC にはそのような情報は含まれません。

次の例では、テーブル定義 SQL 文に、 `decimal` 、 `char` 、 `varchar` 、 `enum`などの各列のパラメータが含まれています。TiCDC によって生成された Canal-JSON 形式と公式 Canal を比較すると、TiCDC には`mysqlType`フィールドに基本的な MySQL 情報のみが含まれていることがわかります。type パラメータの完全な情報が必要な場合は、他の方法で実装する必要があります。

次の SQL ステートメントがアップストリーム TiDB で順番に実行されると仮定します。

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

## TiCDC Canalの変更 -JSON {#changes-in-ticdc-canal-json}

### <code>Delete</code>イベントの<code>Old</code>フィールドの変更 {#changes-in-the-code-old-code-field-of-the-code-delete-code-events}

v5.4.0 から、 `Delete`イベントのうち`old`フィールドが変更されました。

以下は`Delete`イベント メッセージです。v5.4.0 より前では、 `old`フィールドには「データ」フィールドと同じ内容が含まれています。v5.4.0 以降のバージョンでは、 `old`フィールドは null に設定されています。「データ」フィールドを使用して、削除されたデータを取得できます。

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
