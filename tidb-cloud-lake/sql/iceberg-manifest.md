---
title: ICEBERG_MANIFEST
summary: Iceberg テーブルの manifest ファイルに関するメタデータ（ファイルパス、パーティションの詳細、スナップショットとの関連付けなど）を返します。
---

# ICEBERG_MANIFEST

Iceberg テーブルの manifest ファイルに関するメタデータ（ファイルパス、パーティションの詳細、スナップショットとの関連付けなど）を返します。

## 構文 {#syntax}

```sql
ICEBERG_MANIFEST('<database_name>', '<table_name>');
```

## 出力 {#output}

この関数は、次のカラムを持つテーブルを返します。

- `content` (`INT`): コンテンツの種類（データファイルは 0、削除ファイルは 1）。
- `path` (`STRING`): データファイルまたは削除ファイルのファイルパス。
- `length` (`BIGINT`): ファイルサイズ（バイト単位）。
- `partition_spec_id` (`INT`): このファイルに関連付けられたパーティション仕様 ID。
- `added_snapshot_id` (`BIGINT`): このファイルを追加したスナップショット ID。
- `added_data_files_count` (`INT`): 追加された新しいデータファイルの数。
- `existing_data_files_count` (`INT`): 参照されている既存のデータファイルの数。
- `deleted_data_files_count` (`INT`): 削除されたデータファイルの数。
- `added_delete_files_count` (`INT`): 追加された削除ファイルの数。
- `partition_summaries` (`MAP<STRING, STRING>`): このファイルに関連するパーティション値の要約。

## 例 {#examples}

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