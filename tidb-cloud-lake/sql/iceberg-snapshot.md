---
title: ICEBERG_SNAPSHOT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.709"/>

Returns metadata about snapshots of an Iceberg table, including information about data changes, operations, and summary statistics.

## Syntax

```sql
ICEBERG_SNAPSHOT('<database_name>', '<table_name>');
```

## Output

The function returns a table with the following columns:

- `committed_at` (`TIMESTAMP`): The timestamp when the snapshot was committed.
- `snapshot_id` (`BIGINT`): The unique identifier of the snapshot.
- `parent_id` (`BIGINT`): The parent snapshot ID, if applicable.
- `operation` (`STRING`): The type of operation performed (e.g., append, overwrite, delete).
- `manifest_list` (`STRING`): The file path of the manifest list associated with the snapshot.
- `summary` (`MAP<STRING, STRING>`): A JSON-like structure containing additional metadata, such as:
    - `added-data-files`: Number of newly added data files.
    - `added-records`: Number of new records added.
    - `total-records`: Total number of records in the snapshot.
    - `total-files-size`: Total size of all data files (in bytes).
    - `total-data-files`: Total number of data files in the snapshot.
    - `total-delete-files`: Total number of delete files in the snapshot.

## Examples

```sql
SELECT * FROM ICEBERG_SNAPSHOT('tpcds', 'catalog_returns');
 
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│        committed_at        │     snapshot_id     │ parent_id │ operation │                     manifest_list                    │                       summary                       │
├────────────────────────────┼─────────────────────┼───────────┼───────────┼──────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 2025-03-12 23:18:26.626000 │ 7565767416590411866 │         0 │ append    │ s3://warehouse/catalog_returns/metadata/snap-7565767 │ {'spark.app.id':'local-1741821433430','added-data-f │
│                            │                     │           │           │ 416590411866-1-fa1ea4d5-a382-497a-9f22-1acb9a74a346. │ iles':'2','added-records':'144067','total-equality- │
│                            │                     │           │           │ avro                                                 │ deletes':'0','changed-partition-count':'1','total-r │
│                            │                     │           │           │                                                      │ ecords':'144067','total-files-size':'7679811','tota │
│                            │                     │           │           │                                                      │ l-data-files':'2','added-files-size':'7679811','tot │
│                            │                     │           │           │                                                      │ al-delete-files':'0','total-position-deletes':'0'}  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```