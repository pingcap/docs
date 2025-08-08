---
title: TiCDC Canal-JSON Protocol
summary: TiCDC Canal-JSON プロトコルの概念とその使用方法を学びます。
---

# TiCDC Canal- JSON プロトコル {#ticdc-canal-json-protocol}

Canal-JSONは、 [アリババ運河](https://github.com/alibaba/canal)で定義されたデータ交換形式プロトコルです。このドキュメントでは、TiDB拡張フィールド、Canal-JSONデータ形式の定義、公式Canalとの比較など、TiCDCにおけるCanal-JSONデータ形式の実装方法について説明します。

## Canal-JSONを使用する {#use-canal-json}

Message Queue (MQ) を下流の Sink として使用する場合、 `sink-uri`で Canal-JSON を指定できます。TiCDC は、Canal-JSON メッセージを Event を基本単位としてラップして構築し、TiDB データ変更イベントを下流に送信します。

イベントには 3 つの種類があります。

-   DDLイベント: DDL変更レコードを表します。上流のDDL文が正常に実行された後に送信されます。DDLイベントは、インデックスが0のMQパーティションに送信されます。
-   DMLイベント：行データの変更レコードを表します。このタイプのイベントは、行の変更が発生したときに送信されます。変更後の行に関する情報が含まれます。
-   ウォーターマークイベント：特別な時点を表します。この時点より前に受信したイベントが完了していることを示します。これはTiDB拡張フィールドにのみ適用され、 `sink-uri`で`enable-tidb-extension` ～ `true`設定すると有効になります。

以下は`Canal-JSON`使用例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json"
```

## TiDB拡張フィールド {#tidb-extension-field}

Canal-JSONプロトコルは元々MySQL用に設計されており、CommitTSトランザクションのTiDB固有の一意の識別子などの重要なフィールドが含まれていません。この問題を解決するために、TiCDCはCanal-JSONプロトコル形式にTiDB拡張フィールドを追加します`sink-uri`で`enable-tidb-extension`を`true` （デフォルトは`false` ）に設定すると、TiCDCはCanal-JSONメッセージを生成する際に次のように動作します。

-   TiCDC は、 `_tidb`名前のフィールドを含む DML イベント メッセージと DDL イベント メッセージを送信します。
-   TiCDC は WATERMARK イベント メッセージを送信します。

次に例を示します。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-canal-json-enable-tidb-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=canal-json&enable-tidb-extension=true"
```

## メッセージ形式の定義 {#definitions-of-message-formats}

このセクションでは、DDL イベント、DML イベント、ウォーターマーク イベントの形式と、コンシューマー側でデータが解析される方法について説明します。

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

| 分野       | タイプ | 説明                                                                                                    |
| :------- | :-- | :---------------------------------------------------------------------------------------------------- |
| id       | 番号  | TiCDC ではデフォルト値は 0 です。                                                                                 |
| データベース   | 弦   | 行が配置されているデータベースの名前                                                                                    |
| テーブル     | 弦   | 行が配置されているテーブルの名前                                                                                      |
| pkNames  | 配列  | 主キーを構成するすべての列の名前                                                                                      |
| isDdl    | ブール | メッセージがDDLイベントであるかどうか                                                                                  |
| タイプ      | 弦   | Canal-JSONで定義されたイベントタイプ                                                                               |
| es       | 番号  | メッセージを生成したイベントが発生したときの13ビット（ミリ秒）のタイムスタンプ                                                              |
| ts       | 番号  | TiCDC がメッセージを生成した時の 13 ビット (ミリ秒) のタイムスタンプ                                                             |
| SQL      | 弦   | isDdlが`true`場合、対応するDDL文を記録します。                                                                        |
| sqlタイプ   | 物体  | isDdlが`false`場合、各列のデータ型がJavaでどのように表現されるかを記録します。                                                       |
| mysqlタイプ | 物体  | isDdlが`false`場合、各列のデータ型がMySQLでどのように表現されるかを記録します。                                                      |
| データ      | 物体  | isDdlが`false`の場合、各列の名前とそのデータ値を記録します。                                                                  |
| 古い       | 物体  | メッセージが更新イベントによって生成された場合のみ、更新前の各列の名前とデータ値を記録します。                                                       |
| _tidb    | 物体  | TiDB拡張フィールド。1 を`enable-tidb-extension` `true`設定した場合にのみ存在します。5 `commitTs`値は、行の変更を引き起こしたトランザクションのTSOです。 |

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

TiCDCは、 `enable-tidb-extension`を`true`に設定した場合のみ、WATERMARKイベントを送信します。 `type`フィールドの値は`TIDB_WATERMARK`です。イベントには`_tidb`フィールドが含まれており、このフィールドにはパラメータ`watermarkTs`のみが含まれます。 `watermarkTs`の値は、イベント送信時に記録されるTSOです。

このタイプのイベントを受信すると、 `commitTs`が`watermarkTs`より小さいすべてのイベントが送信されています。TiCDC は「少なくとも 1 回」のセマンティクスを提供するため、データが繰り返し送信される可能性があります。その後に`commitTs`が`watermarkTs`より小さいイベントを受信した場合は、このイベントを無視しても問題ありません。

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

### 消費者側でのデータ解析 {#data-parsing-on-the-consumer-side}

上記の例からわかるように、Canal-JSON は統一されたデータ形式を持ち、イベントの種類ごとに異なるフィールドの入力ルールを備えています。コンシューマーは、統一された方法でこの JSON 形式のデータを解析し、フィールド値をチェックすることでイベントの種類を判別できます。

-   `isDdl`が`true`場合、メッセージには DDL イベントが含まれます。
-   `isDdl`が`false`場合、 `type`フィールドをさらに確認する必要があります。7 が`type` `TIDB_WATERMARK`場合、それは WATERMARK イベントです。それ以外の場合は、DML イベントです。

## フィールドの説明 {#field-descriptions}

Canal-JSON 形式では、対応するデータ型が`mysqlType`フィールドと`sqlType`フィールドに記録されます。

### MySQLタイプフィールド {#mysql-type-field}

Canal-JSON形式は、 `mysqlType`フィールドの各列にMySQL Typeの文字列を記録します。詳細については、 [TiDB データ型](/data-type-overview.md)参照してください。

### SQLタイプフィールド {#sql-type-field}

Canal-JSON形式の`sqlType`のフィールドには、各列のJava SQL型が記録されます。これはJDBCのデータに対応するデータ型です。その値は、MySQL型と特定のデータ値から計算できます。マッピングは以下のとおりです。

| MySQLタイプ       | Java SQL 型コード |
| :------------- | :------------ |
| ブール値           | -6            |
| フロート           | 7             |
| ダブル            | 8             |
| 小数点            | 3             |
| チャー            | 1             |
| ヴァルチャール        | 12            |
| バイナリ           | 2004          |
| ヴァーバイナリ        | 2004          |
| タイニーテキスト       | 2005          |
| 文章             | 2005          |
| ミディアムテキスト      | 2005          |
| 長文             | 2005          |
| タイニーブロブ        | 2004          |
| ブロブ            | 2004          |
| ミディアムブロブ       | 2004          |
| ロングブロブ         | 2004          |
| 日付             | 91            |
| 日時             | 93            |
| タイムスタンプ        | 93            |
| 時間             | 92            |
| 年              | 12            |
| 列挙型            | 4             |
| セット            | -7            |
| 少し             | -7            |
| JSON           | 12            |
| TiDBベクターフロート32 | 12            |

## 整数型 {#integer-types}

次の表に示すように、それぞれ異なるJava SQL 型コードに対応する[整数型](/data-type-numeric.md#integer-types) `Unsigned`制約と値のサイズがあるかどうかを考慮する必要があります。

| MySQL 型文字列         | 値の範囲                                        | Java SQL 型コード |
| :----------------- | :------------------------------------------ | :------------ |
| タイニーイント            | [-128, 127]                                 | -6            |
| tinyint 符号なし       | [0, 127]                                    | -6            |
| tinyint 符号なし       | [128、255]                                   | 5             |
| スモールインテンス          | [-32768, 32767]                             | 5             |
| 符号なし小整数            | [0, 32767]                                  | 5             |
| 符号なし小整数            | [32768, 65535]                              | 4             |
| 中程度                | [-8388608, 8388607]                         | 4             |
| mediumint unsigned | [0, 8388607]                                | 4             |
| mediumint unsigned | [8388608, 16777215]                         | 4             |
| 整数                 | [-2147483648, 2147483647]                   | 4             |
| 符号なし整数             | [0, 2147483647]                             | 4             |
| 符号なし整数             | [2147483648, 4294967295]                    | -5            |
| ビッグインテント           | [-9223372036854775808, 9223372036854775807] | -5            |
| bigint 符号なし        | [0, 9223372036854775807]                    | -5            |
| bigint 符号なし        | [9223372036854775808, 18446744073709551615] | 3             |

次の表は、TiCDC のJava SQL タイプとそのコードのマッピング関係を示しています。

| Java SQL型 | Java SQL 型コード |
| :-------- | :------------ |
| チャー       | 1             |
| 小数点       | 3             |
| 整数        | 4             |
| スモールイント   | 5             |
| 本物        | 7             |
| ダブル       | 8             |
| 可変長文字     | 12            |
| 日付        | 91            |
| 時間        | 92            |
| タイムスタンプ   | 93            |
| ブロブ       | 2004          |
| クロブ       | 2005          |
| ビッグイント    | -5            |
| タイニーイント   | -6            |
| 少し        | -7            |

Java SQL 型の詳細については、 [Java SQL クラス型](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)参照してください。

## バイナリ型とBlob型 {#binary-and-blob-types}

TiCDC は、次のように各バイトを文字表現に変換して、 [バイナリ型](/data-type-string.md#binary-type) Canal-JSON 形式でエンコードします。

-   印刷可能な文字は、ISO/IEC 8859-1 文字エンコーディングを使用して表されます。
-   印刷できない文字および HTML で特別な意味を持つ特定の文字は、UTF-8 エスケープ シーケンスを使用して表されます。

次の表に詳細な表現情報を示します。

| 文字の種類            | 値の範囲      | キャラクター表現                          |
| :--------------- | :-------- | :-------------------------------- |
| 制御文字             | [0、31]    | UTF-8エスケープ（ `\u0000`から`\u001F`など） |
| 水平タブ             | [9]       | `\t`                              |
| 改行               | [10]      | `\n`                              |
| キャリッジリターン        | [13]      | `\r`                              |
| 印刷可能な文字          | [32、127]  | リテラル文字（ `A`など）                    |
| アンパサンド           | [38]      | `\u0026`                          |
| 小なり記号            | [60]      | `\u0038`                          |
| 大なり記号            | [62]      | `\u003E`                          |
| 拡張制御文字           | [128、159] | リテラル文字                            |
| ISO 8859-1（ラテン1） | [160、255] | リテラル文字                            |

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

TiCDCにおけるCanal-JSONデータ形式の実装方法（ `Update`イベントと`mysqlType`フィールドを含む）は、公式Canalとは異なります。主な違いは以下の表をご覧ください。

| アイテム             | TiCDC Canal-JSON                                                                                             | 運河                               |
| :--------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `Update`種類のイベント  | デフォルトでは、 `old`フィールドにはすべての列データが含まれます。3が`only_output_updated_columns` `true`場合、 `old`フィールドには変更された列データのみが含まれます。 | `old`フィールドは変更された列データのみを含みます      |
| `mysqlType`フィールド | パラメータを持つ型の場合、型パラメータの情報は含まれません。                                                                               | パラメータを持つ型の場合、型パラメータの完全な情報が含まれます。 |

### 公式Canalとの互換性 {#compatibility-with-the-official-canal}

v6.5.6、v7.1.3、v7.6.0以降、 TiCDC Canal-JSONは公式Canalのデータ形式との互換性をサポートしています。チェンジフィードを作成する際に、 `sink-uri`のうち`content-compatible=true`設定することでこの機能を有効にすることができます。このモードでは、TiCDCは公式Canalと互換性のあるCanal-JSON形式のデータを出力します。具体的な変更点は以下の通りです。

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

`update`ステートメントでは、TiCDCは以下に示すように、 `type`を`UPDATE`としてイベントメッセージを出力します。7 `update`ステートメントは、列番号`c_int`と`c_tinyint`のみを変更します。出力イベントメッセージの`old`フィールドには、すべての列データが含まれます。

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

`mysqlType`フィールドについては、型にパラメータが含まれる場合、公式の Canal には型パラメータの完全な情報が含まれます。TiCDC にはそのような情報は含まれません。

以下の例では、テーブル定義SQL文に、 `decimal` 、 `char` 、 `varchar` 、 `enum`といった各列のパラメータが含まれています。TiCDCによって生成されたCanal-JSON形式と公式Canalを比較すると、TiCDCでは`mysqlType`フィールドにMySQLの基本情報のみが含まれていることがわかります。typeパラメータの完全な情報が必要な場合は、別の方法で実装する必要があります。

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

以下はイベントメッセージ`Delete`です。v5.4.0より前のバージョンでは、フィールド`old`は「data」フィールドと同じ内容です。v5.4.0以降のバージョンでは、フィールド`old` nullに設定されます。「data」フィールドを使用することで、削除されたデータを取得できます。

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
