---
title: TiCDC CSV Protocol
summary: Learn the concept of TiCDC CSV Protocol and how to use it.
---

# TiCDC CSV プロトコル {#ticdc-csv-protocol}

クラウドstorageサービスをダウンストリーム シンクとして使用する場合、DML イベントを CSV 形式でクラウドstorageサービスに送信できます。

## CSVを使用する {#use-csv}

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

-   単一の CSV ファイルでは、行の`commit-ts`次の行の 1 以下になります。
-   1 つのテーブルの同じトランザクションが同じ CSV ファイルに保存されます。
-   同じトランザクションの複数のテーブルを異なる CSV ファイルに保存できます。

## データstorageパス構造 {#data-storage-path-structure}

データのstorageパス構造の詳細については、 [ストレージパス構造](/ticdc/ticdc-sink-to-cloud-storage.md#storage-path-structure)を参照してください。

## データフォーマットの定義 {#definition-of-the-data-format}

CSV ファイルでは、各列は次のように定義されます。

-   カラム1: 操作タイプのインジケーター ( `I` 、 `U` 、および`D`を含む)。 `I` `INSERT`を意味し、 `U` `UPDATE`を意味し、 `D` `DELETE`を意味します。
-   カラム2: テーブル名。
-   カラム3: スキーマ名。
-   カラム4: ソース トランザクションの`commit-ts` 。この列はオプションです。
-   カラム5 から最後の列まで: 変更されるデータを表す 1 つ以上の列。

テーブル`hr.employee`が次のように定義されていると仮定します。

```sql
CREATE TABLE `employee` (
  `Id` int NOT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `FirstName` varchar(30) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `OfficeLocation` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

このテーブルの DML イベントは、次のように CSV 形式で保存されます。

```shell
"I","employee","hr",433305438660591626,101,"Smith","Bob","2014-06-04","New York"
"U","employee","hr",433305438660591627,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,102,"Alex","Alice","2017-03-14","Shanghai"
"U","employee","hr",433305438660591630,102,"Alex","Alice","2018-06-15","Beijing"
```

## データ型マッピング {#data-type-mapping}

| MySQLの種類                                                                      | CSVタイプ | 例                               | 説明                             |
| ----------------------------------------------------------------------------- | ------ | ------------------------------- | ------------------------------ |
| `BOOLEAN` / `TINYINT` / `SMALLINT` / `INT` / `MEDIUMINT` / `BIGINT`           | 整数     | `123`                           | <li></li>                      |
| `FLOAT` / `DOUBLE`                                                            | 浮く     | `153.123`                       | <li></li>                      |
| `NULL`                                                                        | ヌル     | `\N`                            | <li></li>                      |
| `TIMESTAMP` / `DATETIME`                                                      | 弦      | `"1973-12-30 15:30:00.123456"`  | 形式: `yyyy-MM-dd HH:mm:ss.%06d` |
| `DATE`                                                                        | 弦      | `"2000-01-01"`                  | 形式: `yyyy-MM-dd`               |
| `TIME`                                                                        | 弦      | `"23:59:59"`                    | 形式: `yyyy-MM-dd`               |
| `YEAR`                                                                        | 整数     | `1970`                          | <li></li>                      |
| `VARCHAR` / `JSON` / `TINYTEXT` / `MEDIUMTEXT` / `LONGTEXT` / `TEXT` / `CHAR` | 弦      | `"test"`                        | UTF-8エンコード                     |
| `VARBINARY` / `TINYBLOB` / `MEDIUMBLOB` / `LONGBLOB` / `BLOB` / `BINARY`      | 弦      | `"6Zi/5pav"`または`"e998bfe696af"` | Base64 または 16 進エンコード           |
| `BIT`                                                                         | 整数     | `81`                            | <li></li>                      |
| `DECIMAL`                                                                     | 弦      | `"129012.1230000"`              | <li></li>                      |
| `ENUM`                                                                        | 弦      | `"a"`                           | <li></li>                      |
| `SET`                                                                         | 弦      | `"a,b"`                         | <li></li>                      |
