---
title: ICEBERG_MANIFEST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.709"/>

Returns metadata about manifest files of an Iceberg table, including file paths, partitioning details, and snapshot associations.

## Syntax

```sql
ICEBERG_MANIFEST('<database_name>', '<table_name>');
```

## Output

The function returns a table with the following columns:

- `content` (`INT`): The content type (0 for data files, 1 for delete files).
- `path` (`STRING`): The file path of the data or delete file.
- `length` (`BIGINT`): The file size in bytes.
- `partition_spec_id` (`INT`): The partition specification ID associated with the file.
- `added_snapshot_id` (`BIGINT`): The snapshot ID that added this file.
- `added_data_files_count` (`INT`): The number of new data files added.
- `existing_data_files_count` (`INT`): The number of existing data files referenced.
- `deleted_data_files_count` (`INT`): The number of data files deleted.
- `added_delete_files_count` (`INT`): The number of delete files added.
- `partition_summaries` (`MAP<STRING, STRING>`): Summary of partition values related to the file.

## Examples

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