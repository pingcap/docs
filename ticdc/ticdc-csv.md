---
title: TiCDC CSV Protocol
summary: Learn the concept of TiCDC CSV Protocol and how to use it.
---

# TiCDC CSV プロトコル {#ticdc-csv-protocol}

クラウドstorageサービスをダウンストリーム シンクとして使用する場合、DML イベントをクラウドstorageサービスに CSV 形式で送信できます。

## CSV を使用 {#use-csv}

以下は、CSV プロトコルを使用する場合の構成の例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="csv-test" --sink-uri="s3://bucket/prefix" --config changefeed.toml
```

`changefeed.toml`ファイルの構成は次のとおりです。

```toml
[sink]
protocol = "csv"
terminator = "\n"

[sink.csv]
delimiter = ','
quote = '"'
null = '\N'
include-commit-ts = true
```

## トランザクションの制約 {#transactional-constraints}

-   1 つの CSV ファイルで、行の`commit-ts`が次の行の 1 より小さいか等しい。
-   1 つのテーブルの同じトランザクションは、同じ CSV ファイルに格納されます。
-   同じトランザクションの複数のテーブルを異なる CSV ファイルに保存できます。

## データ形式の定義 {#definition-of-the-data-format}

CSV ファイルでは、各列は次のように定義されています。

-   カラム1: `I` 、 `U` 、および`D`を含む操作タイプのインジケーター。 `I` `INSERT`を意味し、 `U` `UPDATE`を意味し、 `D` `DELETE`を意味します。
-   カラム2: テーブル名。
-   カラム3: スキーマ名。
-   カラム4: ソース トランザクションの`commit-ts` 。この列はオプションです。
-   5カラムから最後の列: 変更するデータを表す 1 つ以上の列。

表`hr.employee`が次のように定義されているとします。

```sql
CREATE TABLE `employee` (
  `Id` int NOT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `FirstName` varchar(30) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `OfficeLocation` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

このテーブルの DML イベントは、次のように CSV 形式で格納されます。

```shell
"I","employee","hr",433305438660591626,101,"Smith","Bob","2014-06-04","New York"
"U","employee","hr",433305438660591627,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,102,"Alex","Alice","2017-03-14","Shanghai"
"U","employee","hr",433305438660591630,102,"Alex","Alice","2018-06-15","Beijing"
```

## データ型のマッピング {#data-type-mapping}

| MySQL タイプ                                                                     | CSVタイプ | 例                              | 説明                                 |
| ----------------------------------------------------------------------------- | ------ | ------------------------------ | ---------------------------------- |
| `BOOLEAN` / `TINYINT` / `SMALLINT` / `INT` / `MEDIUMINT` / `BIGINT`           | 整数     | `123`                          | <li></li>                          |
| `FLOAT` / `DOUBLE`                                                            | 浮く     | `153.123`                      | <li></li>                          |
| `NULL`                                                                        | ヌル     | `\N`                           | <li></li>                          |
| `TIMESTAMP` / `DATETIME`                                                      | 弦      | `"1973-12-30 15:30:00.123456"` | フォーマット: `yyyy-MM-dd HH:mm:ss.%06d` |
| `DATE`                                                                        | 弦      | `"2000-01-01"`                 | フォーマット: `yyyy-MM-dd`               |
| `TIME`                                                                        | 弦      | `"23:59:59"`                   | フォーマット: `yyyy-MM-dd`               |
| `YEAR`                                                                        | 整数     | `1970`                         | <li></li>                          |
| `VARCHAR` / `JSON` / `TINYTEXT` / `MEDIUMTEXT` / `LONGTEXT` / `TEXT` / `CHAR` | 弦      | `"test"`                       | UTF-8 エンコード                        |
| `VARBINARY` / `TINYBLOB` / `MEDIUMBLOB` / `LONGBLOB` / `BLOB` / `BINARY`      | 弦      | `"6Zi/5pav"`                   | base64 エンコード                       |
| `BIT`                                                                         | 整数     | `81`                           | <li></li>                          |
| `DECIMAL`                                                                     | 弦      | `"129012.1230000"`             | <li></li>                          |
| `ENUM`                                                                        | 弦      | `"a"`                          | <li></li>                          |
| `SET`                                                                         | 弦      | `"a,b"`                        | <li></li>                          |
