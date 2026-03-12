---
title: OPTIMIZE TABLE
sidebar_position: 8
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.395"/>

import DetailsWrap from '@site/src/components/DetailsWrap';

Optimizing a table in Databend involves compacting or purging historical data to save storage space and enhance query performance.

<DetailsWrap>

<details>
  <summary>Why Optimize?</summary>
    <div>Databend stores data in tables using the Parquet format, which is organized into blocks. Additionally, Databend supports time travel functionality, where each operation that modifies a table generates a Parquet file that captures and reflects the changes made to the table.</div><br/>

   <div>As a table accumulates more Parquet files over time, it can lead to performance issues and increased storage requirements. To optimize the table's performance, historical Parquet files can be deleted when they are no longer needed. This optimization can help to improve query performance and reduce the amount of storage space used by the table.</div>
</details>

</DetailsWrap>

## Databend Data Storage: Snapshot, Segment, and Block

Snapshot, segment, and block are the concepts Databend uses for data storage. Databend uses them to construct a hierarchical structure for storing table data.

![](/img/sql/storage-structure.PNG)

Databend automatically creates table snapshots upon data updates. A snapshot represents a version of the table's segment metadata.

When working with Databend, you're most likely to access a snapshot with the snapshot ID when you retrieve and query a previous version of the table's data with the [AT](../../20-query-syntax/03-query-at.md) clause.

A snapshot is a JSON file that does not save the table's data but indicate the segments the snapshot links to. If you run [FUSE_SNAPSHOT](../../../20-sql-functions/16-system-functions/fuse_snapshot.md) against a table, you can find the saved snapshots for the table.

A segment is a JSON file that organizes the storage blocks (at least 1, at most 1,000) where the data is stored. If you run [FUSE_SEGMENT](../../../20-sql-functions/16-system-functions/fuse_segment.md) against a snapshot with the snapshot ID, you can find which segments are referenced by the snapshot.

Databends saves actual table data in parquet files and considers each parquet file as a block. If you run [FUSE_BLOCK](../../../20-sql-functions/16-system-functions/fuse_block.md) against a snapshot with the snapshot ID, you can find which blocks are referenced by the snapshot.

Databend creates a unique ID for each database and table for storing the snapshot, segment, and block files and saves them to your object storage in the path `<bucket_name>/<tenant_id>/<db_id>/<table_id>/`. Each snapshot, segment, and block file is named with a UUID (32-character lowercase hexadecimal string).

| File     | Format  | Filename                        | Storage Folder                                      |
|----------|---------|---------------------------------|-----------------------------------------------------|
| Snapshot | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_ss/` |
| Segment  | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_sg/` |
| Block    | parquet | `<32bitUUID>_<version>.parquet` | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_b/`  |

## Table Optimizations

In Databend, it's advisable to aim for an ideal block size of either 100MB (uncompressed) or 1,000,000 rows, with each segment consisting of 1,000 blocks. To maximize table optimization, it's crucial to gain a clear understanding of when and how to apply various optimization techniques, such as [Segment Compaction](#segment-compaction) and [Block Compaction](#block-compaction).
- When using the COPY INTO or REPLACE INTO command to write data into a table that includes a cluster key, Databend will automatically initiate a re-clustering process, as well as a segment and block compact process.

- Segment & block compactions support distributed execution in cluster environments. You can enable them by setting ENABLE_DISTRIBUTED_COMPACT to 1. This helps enhance data query performance and scalability in cluster environments.

  ```sql
  SET enable_distributed_compact = 1;
  ```

### Segment Compaction

Compact segments when a table has too many small segments (less than `100 blocks` per segment).
```sql
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('your-database', 'your-table')
    LIMIT 1;
```

**Syntax**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT SEGMENT [LIMIT <segment_count>]    
```

Compacts the table data by merging small segments into larger ones.

- The option LIMIT sets the maximum number of segments to be compacted. In this case, Databend will select and compact the latest segments.

**Example**

```sql
-- Check whether need segment compact
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('hits', 'hits');

+-------------+---------------+-------------------------------------+
| block_count | segment_count | advice                              |
+-------------+---------------+-------------------------------------+
|         751 |            32 | The table needs segment compact now |
+-------------+---------------+-------------------------------------+
    
-- Compact segment
OPTIMIZE TABLE hits COMPACT SEGMENT;
    
-- Check again
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('hits', 'hits')
    LIMIT 1;

+-------------+---------------+---------------------------------------------+
| block_count | segment_count | advice                                      |
+-------------+---------------+---------------------------------------------+
|         751 |             1 | The table does not need segment compact now |
+-------------+---------------+---------------------------------------------+
```

### Block Compaction

Compact blocks when a table has a large number of small blocks or when the table has a high percentage of inserted, deleted, or updated rows.

You can check it with if the uncompressed size of each block is close to the perfect size of `100MB`. 

If the size is less than `50MB`, we suggest doing block compaction, as it indicates too many small blocks:

```sql
SELECT
  block_count,
  humanize_size(bytes_uncompressed / block_count) AS per_block_uncompressed_size,
  IF(
              bytes_uncompressed / block_count / 1024 / 1024 < 50,
              'The table needs block compact now',
              'The table does not need block compact now'
    ) AS advice
FROM
  fuse_snapshot('your-database', 'your-table')
    LIMIT 1;
```

:::info
We recommend performing segment compaction first, followed by block compaction.
:::

**Syntax**
```sql
OPTIMIZE TABLE [database.]table_name COMPACT [LIMIT <segment_count>]    
```
Compacts the table data by merging small blocks and segments into larger ones.

- This command creates a new snapshot (along with compacted segments and blocks) of the most recent table data without affecting the existing storage files, so the storage space won't be released until you purge the historical data.

- Depending on the size of the given table, it may take quite a while to complete the execution.

- The option LIMIT sets the maximum number of segments to be compacted. In this case, Databend will select and compact the latest segments.

- Databend will automatically re-cluster a clustered table after the compacting process.

**Example**
```sql
OPTIMIZE TABLE my_database.my_table COMPACT LIMIT 50;
```
