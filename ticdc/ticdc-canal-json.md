---
title: TiCDC Canal-JSON Protocol
summary: Learn the concept of TiCDC Canal-JSON Protocol and how to use it.
---

# TiCDC運河-JSONプロトコル {#ticdc-canal-json-protocol}

Canal-JSONは、 [アリババ運河](https://github.com/alibaba/canal)で定義されるデータ交換フォーマットプロトコルです。このドキュメントでは、TiDB拡張フィールド、Canal-JSONデータ形式の定義、公式のCanalとの比較など、Canal-JSONデータ形式がTiCDCでどのように実装されているかを学習できます。

## Canal-JSONを使用する {#use-canal-json}

ダウンストリームシンクとしてメッセージキュー（MQ）を使用する場合、Canal-JSONを`sink-uri`で指定できます。 TiCDCは、イベントを基本単位としてCanal-JSONメッセージをラップおよび構築し、TiDBデータ変更イベントをダウンストリームに送信します。

イベントには次の3つのタイプがあります。

-   DDLイベント：DDL変更レコードを表します。これは、アップストリームDDLステートメントが正常に実行された後に送信されます。 DDLイベントは、インデックスが0のMQパーティションに送信されます。
-   DMLイベント：行データ変更レコードを表します。このタイプのイベントは、行の変更が発生したときに送信されます。変更が発生した後の行に関する情報が含まれています。
-   透かしイベント：特別な時点を表します。これは、このポイントが完了する前に受信したイベントを示します。これはTiDB拡張フィールドにのみ適用され、 `sink-uri`で`enable-tidb-extension`から`true`に設定すると有効になります。

以下は、 `Canal-JSON`の使用例です。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-canal-json" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=canal-json"
```

## TiDB拡張フィールド {#tidb-extension-field}

Canal-JSONプロトコルは、もともとMySQL用に設計されています。 CommitTSトランザクションのTiDB固有の一意の識別子などの重要なフィールドは含まれていません。この問題を解決するために、TiCDCはTiDB拡張フィールドをCanal-JSONプロトコル形式に追加します。 `sink-uri`で`enable-tidb-extension`を`true` （デフォルトでは`false` ）に設定すると、Canal-JSONメッセージを生成するときにTiCDCは次のように動作します。

-   TiCDCは、 `_tidb`という名前のフィールドを含むDMLイベントおよびDDLイベントメッセージを送信します。
-   TiCDCはWATERMARKイベントメッセージを送信します。

次に例を示します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-canal-json-enable-tidb-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.6.0&protocol=canal-json&enable-tidb-extension=true"
```

## メッセージ形式の定義 {#definitions-of-message-formats}

このセクションでは、DDLイベント、DMLイベント、およびWATERMARKイベントの形式と、コンシューマー側でデータがどのように解決されるかについて説明します。

### DDLイベント {#ddl-event}

TiCDCは、DDLイベントを次のCanal-JSON形式にエンコードします。

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

フィールドの説明は次のとおりです。

| 分野        | タイプ | 説明                                                                                             |
| :-------- | :-- | :--------------------------------------------------------------------------------------------- |
| id        | 番号  | TiCDCのデフォルト値は0です。                                                                              |
| データベース    | 弦   | 行が配置されているデータベースの名前                                                                             |
| テーブル      | 弦   | 行が配置されているテーブルの名前                                                                               |
| pkNames   | 配列  | 主キーを構成するすべての列の名前                                                                               |
| isDdl     | ブール | メッセージがDDLイベントであるかどうか                                                                           |
| タイプ       | 弦   | Canal-JSONによって定義されたイベントタイプ                                                                     |
| es        | 番号  | メッセージを生成したイベントが発生したときの13ビット（ミリ秒）のタイムスタンプ                                                       |
| ts        | 番号  | TiCDCがメッセージを生成したときの13ビット（ミリ秒）のタイムスタンプ                                                          |
| sql       | 弦   | isDdlが`true`の場合、対応するDDLステートメントを記録します                                                           |
| sqlType   | 物体  | isDdlが`false`の場合、各列のデータ型がJavaでどのように表されるかを記録します                                                 |
| mysqlType | 物体  | isDdlが`false`の場合、MySQLで各列のデータ型がどのように表されるかを記録します                                                |
| データ       | 物体  | isDdlが`false`の場合、各列の名前とそのデータ値を記録します                                                            |
| 年         | 物体  | メッセージが更新イベントによって生成された場合のみ、更新前の各列の名前とデータ値を記録します                                                 |
| _tidb     | 物体  | TiDB拡張フィールド。 `enable-tidb-extension`から`true`に設定した場合にのみ存在します。値`commitTs`は、行を変更したトランザクションのTSOです。 |

### DMLイベント {#dml-event}

TiCDCは、DMLデータ変更イベントの行を次のようにエンコードします。

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

TiCDCは、 `enable-tidb-extension`から`true`に設定した場合にのみ、透かしイベントを送信します。 `type`フィールドの値は`TIDB_WATERMARK`です。イベントには`_tidb`フィールドが含まれ、フィールドには1つのパラメーター`watermarkTs`のみが含まれます。 `watermarkTs`の値は、イベントが送信されたときに記録されたTSOです。

このタイプのイベントを受信すると、 `commitTs`が`watermarkTs`未満のすべてのイベントが送信されます。 TiCDCは「少なくとも1回」のセマンティクスを提供するため、データが繰り返し送信される可能性があります。 `commitTs`が`watermarkTs`未満の後続のイベントを受信した場合は、このイベントを無視しても問題ありません。

以下は、ウォーターマークイベントの例です。

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

上記の例からわかるように、Canal-JSONのデータ形式は統一されており、イベントタイプごとにフィールド入力ルールが異なります。統一された方法を使用してこのJSON形式のデータを解決し、フィールド値を確認してイベントタイプを判別できます。

-   `isDdl`が`true`の場合、メッセージにはDDLイベントが含まれます。
-   `isDdl`が`false`の場合、 `type`フィールドをさらにチェックする必要があります。 `type`が`TIDB_WATERMARK`の場合、それは透かしイベントです。それ以外の場合は、DMLイベントです。

## フィールドの説明 {#field-descriptions}

Canal-JSON形式は、対応するデータ型を`mysqlType`フィールドと`sqlType`フィールドに記録します。

### MySQLタイプフィールド {#mysql-type-field}

`mysqlType`フィールドでは、Canal-JSON形式が各列にMySQLタイプの文字列を記録します。詳細については、 [TiDBデータ型](/data-type-overview.md)を参照してください。

### SQLタイプフィールド {#sql-type-field}

`sqlType`フィールドには、Canal-JSON形式で各列のJava SQLタイプが記録されます。これは、JDBCのデータに対応するデータ型です。その値は、MySQLタイプと特定のデータ値によって計算できます。マッピングは次のとおりです。

| MySQLタイプ  | JavaSQLタイプコード |
| :-------- | :------------ |
| ブール値      | -6            |
| 浮く        | 7             |
| ダブル       | 8             |
| 10進数      | 3             |
| チャー       | 1             |
| バルチャー     | 12            |
| バイナリ      | 2004年         |
| バイナリ      | 2004年         |
| Tinytext  | 2005年         |
| 文章        | 2005年         |
| ミディアムテキスト | 2005年         |
| ロングテキスト   | 2005年         |
| Tinyblob  | 2004年         |
| ブロブ       | 2004年         |
| ミディアムブロブ  | 2004年         |
| ロングブロブ    | 2004年         |
| 日にち       | 91            |
| 日付時刻      | 93            |
| タイムスタンプ   | 93            |
| 時間        | 92            |
| 年         | 12            |
| 列挙型       | 4             |
| 設定        | -7            |
| 少し        | -7            |
| JSON      | 12            |

## 整数型 {#integer-types}

次の表に示すように、 [整数型](/data-type-numeric.md#integer-types)に`Unsigned`の制約と、それぞれ異なるJavaSQLタイプコードに対応する値のサイズがあるかどうかを考慮する必要があります。

| MySQLタイプ文字列       | 値の範囲                                       | JavaSQLタイプコード |
| :---------------- | :----------------------------------------- | :------------ |
| tinyint           | [-128、127]                                 | -6            |
| tinyint unsigned  | [0、127]                                    | -6            |
| tinyint unsigned  | [128、255]                                  | 5             |
| smallint          | [-32768、32767]                             | 5             |
| smallint unsigned | [0、32767]                                  | 5             |
| smallint unsigned | [32768、65535]                              | 4             |
| ミディアムイント          | [-8388608、8388607]                         | 4             |
| 署名されていないmediumint | [0、8388607]                                | 4             |
| 署名されていないmediumint | [8388608、16777215]                         | 4             |
| int               | [-2147483648、2147483647]                   | 4             |
| int unsigned      | [0、2147483647]                             | 4             |
| int unsigned      | [2147483648、4294967295]                    | -5            |
| bigint            | [-9223372036854775808、9223372036854775807] | -5            |
| bigint unsigned   | [0、9223372036854775807]                    | -5            |
| bigint unsigned   | [9223372036854775808、18446744073709551615] | 3             |

次の表は、TiCDCのJavaSQLタイプとそのコード間のマッピング関係を示しています。

| JavaSQLタイプ | JavaSQLタイプコード |
| :--------- | :------------ |
| CHAR       | 1             |
| 10進数       | 3             |
| 整数         | 4             |
| SMALLINT   | 5             |
| 本物         | 7             |
| ダブル        | 8             |
| VARCHAR    | 12            |
| 日にち        | 91            |
| 時間         | 92            |
| タイムスタンプ    | 93            |
| BLOB       | 2004年         |
| CLOB       | 2005年         |
| BIGINT     | -5            |
| TINYINT    | -6            |
| 少し         | -7            |

Java SQLタイプの詳細については、 [JavaSQLクラスタイプ](https://docs.oracle.com/javase/8/docs/api/java/sql/Types.html)を参照してください。

## TiCDC運河-JSONと公式運河の比較 {#comparison-of-ticdc-canal-json-and-the-official-canal}

TiCDCがCanal-JSONデータ形式を実装する方法（ `Update`イベントと`mysqlType`フィールドを含む）は、公式のCanalとは異なります。次の表に、主な違いを示します。

| アイテム             | TiCDC運河-JSON                    | 運河                                |
| :--------------- | :------------------------------ | :-------------------------------- |
| `Update`種類のイベント  | `old`フィールドには、すべての列データが含まれます     | `old`フィールドには、変更された列データのみが含まれます    |
| `mysqlType`フィールド | パラメータ付きの型の場合、型パラメータの情報は含まれていません | パラメータ付きの型の場合、型パラメータの完全な情報が含まれています |

### <code>Update</code>タイプのイベント {#event-of-code-update-code-type}

`Update`種類のイベントの場合：

-   TiCDCでは、 `old`フィールドにすべての列データが含まれます
-   公式運河では、 `old`フィールドには変更された列データのみが含まれます

次のSQLステートメントがアップストリームTiDBで順番に実行されると想定します。

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

`update`ステートメントの場合、TiCDCは、以下に示すように、 `type`が`UPDATE`のイベントメッセージを出力します。 `update`ステートメントは、 `c_int`列と`c_tinyint`列のみを変更します。出力イベントメッセージの`old`フィールドには、すべての列データが含まれています。

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

公式運河の場合、出力イベントメッセージの`old`フィールドには、以下に示すように、変更された列データのみが含まれます。

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

`mysqlType`フィールドの場合、タイプにパラメーターが含まれている場合、公式の運河にはタイプパラメーターの完全な情報が含まれます。 TiCDCにはそのような情報は含まれていません。

次の例では、テーブルを定義するSQLステートメントに、 `decimal` 、および`char`のパラメーターなど、各列のパラメーターが含まれて`varchar` `enum` 。 TiCDCによって生成されたCanal-JSON形式と公式のCanalを比較すると、TiCDCには`mysqlType`フィールドの基本的なMySQL情報のみが含まれていることがわかります。 typeパラメータの完全な情報が必要な場合は、他の方法で実装する必要があります。

次のSQLステートメントがアップストリームTiDBで順番に実行されると想定します。

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

TiCDCの出力は次のとおりです。

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

## TiCDC運河の変更-JSON {#changes-in-ticdc-canal-json}

### <code>Delete</code>イベントの<code>Old</code>フィールドの変更 {#changes-in-the-code-old-code-field-of-the-code-delete-code-events}

v5.4.0から、 `Delete`のイベントの`old`のフィールドが変更されました。

以下は`Delete`のイベントメッセージです。 v5.4.0より前では、 `old`フィールドには「データ」フィールドと同じ内容が含まれています。 v5.4.0以降のバージョンでは、 `old`フィールドはnullに設定されています。 「データ」フィールドを使用して、削除されたデータを取得できます。

```
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
```
