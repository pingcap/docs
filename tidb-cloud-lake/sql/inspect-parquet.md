---
title: INSPECT_PARQUET
summary: 从 stage 中的 Parquet 文件检索包含完整元信息的表，其中包括以下列。
---

# INSPECT_PARQUET

从 stage 中的 Parquet 文件检索包含完整元信息的表，其中包括以下列：

| 列 | 描述 |
|----------------------------------|----------------------------------------------------------------|
| created_by                       | 负责创建 Parquet 文件的实体或来源 |
| num_columns                      | Parquet 文件中的列数 |
| num_rows                         | Parquet 文件中的总行数或记录数 |
| num_row_groups                   | Parquet 文件中的行组数量 |
| serialized_size                  | Parquet 文件在磁盘上的大小（压缩后） |
| max_row_groups_size_compressed   | 最大行组的大小（压缩后） |
| max_row_groups_size_uncompressed | 最大行组的大小（未压缩） |

## 语法 {#syntax}

```sql
INSPECT_PARQUET('@<path-to-file>')
```

## 示例 {#examples}

以下示例从 stage 中名为 [books.parquet](https://lakesql-bin.tidbcloud.com/datasets/books.parquet) 的示例 Parquet 文件中检索元信息。该文件包含两条记录：

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