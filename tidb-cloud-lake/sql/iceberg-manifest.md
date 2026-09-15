---
title: ICEBERG_MANIFEST
summary: 返回 Iceberg 表中 manifest 文件的元信息，包括文件路径、分区详情以及关联的快照。
---

# ICEBERG_MANIFEST

返回 Iceberg 表中 manifest 文件的元信息，包括文件路径、分区详情以及关联的快照。

## 语法 {#syntax}

```sql
ICEBERG_MANIFEST('<database_name>', '<table_name>');
```

## 输出 {#output}

该函数返回一个包含以下列的表：

- `content` (`INT`): 内容类型（0 表示数据文件，1 表示删除文件）。
- `path` (`STRING`): 数据文件或删除文件的文件路径。
- `length` (`BIGINT`): 文件大小，单位为字节。
- `partition_spec_id` (`INT`): 与该文件关联的分区规范 ID。
- `added_snapshot_id` (`BIGINT`): 添加该文件的快照 ID。
- `added_data_files_count` (`INT`): 新增的数据文件数量。
- `existing_data_files_count` (`INT`): 被引用的现有数据文件数量。
- `deleted_data_files_count` (`INT`): 已删除的数据文件数量。
- `added_delete_files_count` (`INT`): 新增的删除文件数量。
- `partition_summaries` (`MAP<STRING, STRING>`): 与该文件相关的分区值摘要。

## 示例 {#examples}

```sql
SELECT * FROM ICEBERG_MANIFEST('tpcds', 'catalog_returns');

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ content │      path      │ length │ partition_spec │ added_snapshot │ added_data_fil │ existing_data_ │ deleted_data_ │ added_delete_ │ existing_dele │ deleted_delet │ partition_sum │
│  Int32  │     String     │  Int64 │       _id      │       _id      │    es_count    │   files_count  │  files_count  │  files_count  │ te_files_coun │ e_files_count │     maries    │
│         │                │        │      Int32     │ Nullable(Int64 │ Nullable(Int32 │ Nullable(Int32 │ Nullable(Int3 │ Nullable(Int3 │       t       │ Nullable(Int3 │ Array(Nullabl │
│         │                │        │                │        )       │        )       │        )       │       2)      │       2)      │ Nullable(Int3 │       2)      │ e(Tuple(Nulla │
│         │                │        │                │                │                │                │               │               │       2)      │               │ ble(Boolean), │
│         │                │        │                │                │                │                │               │               │               │               │ Nullable(Bool │
│         │                │        │                │                │                │                │               │               │               │               │ ean), String, │
│         │                │        │                │                │                │                │               │               │               │               │   String)))   │
├─────────┼────────────────┼────────┼────────────────┼────────────────┼────────────────┼────────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│       0 │ s3://warehouse │   9241 │              0 │ 75657674165904 │              2 │              0 │             0 │             2 │             0 │             0 │ []            │
│         │ /catalog_retur │        │                │          11866 │                │                │               │               │               │               │               │
│         │ ns/metadata/fa │        │                │                │                │                │               │               │               │               │               │
│         │ 1ea4d5-a382-49 │        │                │                │                │                │               │               │               │               │               │
│         │ 7a-9f22-1acb9a │        │                │                │                │                │               │               │               │               │               │
│         │ 74a346-m0.avro │        │                │                │                │                │               │               │               │               │               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```