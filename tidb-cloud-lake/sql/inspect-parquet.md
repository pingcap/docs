---
title: INSPECT_PARQUET
summary: stage 上の Parquet ファイルから包括的なメタデータのテーブルを取得します。取得されるカラムは以下のとおりです。
---

# INSPECT_PARQUET

stage 上の Parquet ファイルから包括的なメタデータのテーブルを取得します。取得されるカラムは以下のとおりです。

| カラム                           | 説明                                                    |
|----------------------------------|----------------------------------------------------------------|
| created_by                       | Parquet ファイルの作成元となるエンティティまたはソース |
| num_columns                      | Parquet ファイル内のカラム数 |
| num_rows                         | Parquet ファイル内の行またはレコードの総数 |
| num_row_groups                   | Parquet ファイル内の row group の数 |
| serialized_size                  | ディスク上の Parquet ファイルのサイズ（圧縮後） |
| max_row_groups_size_compressed   | 最大の row group のサイズ（圧縮後） |
| max_row_groups_size_uncompressed | 最大の row group のサイズ（非圧縮） |

## 構文 {#syntax}

```sql
INSPECT_PARQUET('@<path-to-file>')
```

## 例 {#examples}

この例では、[books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) という名前の stage 上のサンプル Parquet ファイルからメタデータを取得します。このファイルには 2 件のレコードが含まれています。

```text title='books.parquet'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

```sql
-- Show the staged file
LIST @my_internal_stage;

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │        md5       │         last_modified         │      creator     │
├───────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ books.parquet │    998 │ NULL             │ 2023-04-19 19:34:51.303 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────┘

-- Retrieve metadata from the staged file
SELECT * FROM INSPECT_PARQUET('@my_internal_stage/books.parquet');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│             created_by             │ num_columns │ num_rows │ num_row_groups │ serialized_size │ max_row_groups_size_compressed │ max_row_groups_size_uncompressed │
├────────────────────────────────────┼─────────────┼──────────┼────────────────┼─────────────────┼────────────────────────────────┼──────────────────────────────────┤
│ parquet-cpp version 1.5.1-SNAPSHOT │           3 │        2 │              1 │             998 │                            332 │                              320 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```