---
title: TiCDC CSV Protocol
summary: TiCDC CSVプロトコルの概念と使用方法を学びましょう。
---

# TiCDC CSVプロトコル {#ticdc-csv-protocol}

クラウドstorageサービスをダウンストリームのシンクとして使用する場合、DMLイベントをCSV形式でクラウドstorageサービスに送信できます。

## CSVを使用する {#use-csv}

以下は、CSVプロトコルを使用する場合の設定例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="csv-test" --sink-uri="s3://bucket/prefix" --config changefeed.toml
```

`changefeed.toml`ファイルの設定は以下のとおりです。

```toml
[sink]
protocol = "csv"
terminator = "\n"

[sink.csv]
delimiter = ',' # Before v7.6.0, you can only set the delimiter to a single character. Starting from v7.6.0, you can set it to 1-3 characters. For example, `$^` or `|@|`.
quote = '"'
null = '\N'
include-commit-ts = true
output-old-value = false
output-field-header = false # New in v8.5.6 (only available in the TiCDC new architecture)
```

## 取引上の制約 {#transactional-constraints}

-   単一のCSVファイルでは、ある行の`commit-ts`は、次の行の{{B-PLACEHOLDER-E}}と同じかそれ以下です。
-   同一テーブルの同じトランザクションは、同じCSVファイルに保存されます。
-   同じトランザクションの複数のテーブルを、異なるCSVファイルに保存することができます。

## データstorageパス構造 {#data-storage-path-structure}

データのstorageパス構造の詳細については、 [ストレージパス構造](/ticdc/ticdc-sink-to-cloud-storage.md#storage-path-structure)参照してください。

## データ形式の定義 {#definition-of-the-data-format}

CSVファイルでは、各列は次のように定義されています。

-   カラム1: 操作タイプインジケータ。 `I` 、 `U` 、 `D`を含む。 `I`は`INSERT`を意味し、 `U`は`UPDATE`を意味し、 `D`は`DELETE`を意味する。
-   2カラム：テーブル名。
-   3カラム：スキーマ名。
-   4カラム：ソーストランザクションの`commit-ts` 。この列は省略可能です。
-   カラム5: `is-update`列は`output-old-value`の値が true の場合にのみ存在し、行データの変更が UPDATE イベント (列の値が true の場合) によるものか、INSERT/DELETE イベント (値が false の場合) によるものかを識別するために使用されます。
-   6カラムから最終列まで：データが変更された列が1つ以上あります。

[TiCDCの新アーキテクチャ](/ticdc/ticdc-architecture.md)の場合、 `output-field-header = true`の場合、CSV ファイルにはヘッダー行が含まれます。ヘッダー行の列名は次のとおりです。

| 1カラム                   | 2カラム               | 3カラム                | 4カラム（任意）               | 5カラム（任意）               | 第6カラム         | ... | 最後の列          |
| ---------------------- | ------------------ | ------------------- | ---------------------- | ---------------------- | ------------- | --- | ------------- |
| `ticdc-meta$operation` | `ticdc-meta$table` | `ticdc-meta$schema` | `ticdc-meta$commit-ts` | `ticdc-meta$is-update` | データが変更された最初の列 | ... | データが変更された最後の列 |

テーブル`hr.employee`は次のように定義されていると仮定します。

```sql
CREATE TABLE `employee` (
  `Id` int NOT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `FirstName` varchar(30) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `OfficeLocation` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`include-commit-ts = true`と`output-old-value = false`の場合、このテーブルの DML イベントは、次のように CSV 形式で保存されます。

```shell
"I","employee","hr",433305438660591626,101,"Smith","Bob","2014-06-04","New York"
"U","employee","hr",433305438660591627,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,102,"Alex","Alice","2017-03-14","Shanghai"
"U","employee","hr",433305438660591630,102,"Alex","Alice","2018-06-15","Beijing"
```

`include-commit-ts = true`と`output-old-value = true`の場合、このテーブルの DML イベントは、次のように CSV 形式で保存されます。

    "I","employee","hr",433305438660591626,false,101,"Smith","Bob","2014-06-04","New York"
    "D","employee","hr",433305438660591627,true,101,"Smith","Bob","2015-10-08","Shanghai"
    "I","employee","hr",433305438660591627,true,101,"Smith","Bob","2015-10-08","Los Angeles"
    "D","employee","hr",433305438660591629,false,101,"Smith","Bob","2017-03-13","Dallas"
    "I","employee","hr",433305438660591630,false,102,"Alex","Alice","2017-03-14","Shanghai"
    "D","employee","hr",433305438660591630,true,102,"Alex","Alice","2017-03-14","Beijing"
    "I","employee","hr",433305438660591630,true,102,"Alex","Alice","2018-06-15","Beijing"

`include-commit-ts = true` 、 `output-old-value = true` 、および`output-field-header = true`の場合、このテーブルのDMLイベントは、次のようにCSV形式で保存されます。

```csv
ticdc-meta$operation,ticdc-meta$table,ticdc-meta$schema,ticdc-meta$commit-ts,ticdc-meta$is-update,Id,LastName,FirstName,HireDate,OfficeLocation
"I","employee","hr",433305438660591626,false,101,"Smith","Bob","2014-06-04","New York"
"D","employee","hr",433305438660591627,true,101,"Smith","Bob","2015-10-08","Shanghai"
"I","employee","hr",433305438660591627,true,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,false,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,false,102,"Alex","Alice","2017-03-14","Shanghai"
"D","employee","hr",433305438660591630,true,102,"Alex","Alice","2017-03-14","Beijing"
"I","employee","hr",433305438660591630,true,102,"Alex","Alice","2018-06-15","Beijing"
```

## データ型マッピング {#data-type-mapping}

| MySQLタイプ                                                                      | CSV形式 | 例                               | 説明                             |
| ----------------------------------------------------------------------------- | ----- | ------------------------------- | ------------------------------ |
| `BOOLEAN` / `TINYINT` / `SMALLINT` / `INT` / `MEDIUMINT` / `BIGINT`           | 整数    | `123`                           | -                              |
| `FLOAT` / `DOUBLE`                                                            | フロート  | `153.123`                       | -                              |
| `NULL`                                                                        | ヌル    | `\N`                            | -                              |
| `TIMESTAMP` / `DATETIME`                                                      | 弦     | `"1973-12-30 15:30:00.123456"`  | 形式: `yyyy-MM-dd HH:mm:ss.%06d` |
| `DATE`                                                                        | 弦     | `"2000-01-01"`                  | 形式: `yyyy-MM-dd`               |
| `TIME`                                                                        | 弦     | `"23:59:59"`                    | 形式: `yyyy-MM-dd`               |
| `YEAR`                                                                        | 整数    | `1970`                          | -                              |
| `VARCHAR` / `JSON` / `TINYTEXT` / `MEDIUMTEXT` / `LONGTEXT` / `TEXT` / `CHAR` | 弦     | `"test"`                        | UTF-8エンコード                     |
| `VARBINARY` / `TINYBLOB` / `MEDIUMBLOB` / `LONGBLOB` / `BLOB` / `BINARY`      | 弦     | `"6Zi/5pav"`または`"e998bfe696af"` | Base64または16進数エンコード             |
| `BIT`                                                                         | 整数    | `81`                            | -                              |
| `DECIMAL`                                                                     | 弦     | `"129012.1230000"`              | -                              |
| `ENUM`                                                                        | 弦     | `"a"`                           | -                              |
| `SET`                                                                         | 弦     | `"a,b"`                         | -                              |
| `TiDBVectorFloat32`                                                           | 弦     | `"[1.23, -0.4]"`                | -                              |
