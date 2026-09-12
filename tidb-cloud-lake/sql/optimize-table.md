---
title: OPTIMIZE TABLE
summary: 在 {{{ .lake }}} 中优化表涉及压缩或清除历史数据，以节省存储空间并提升查询性能。
---

# OPTIMIZE TABLE

在 {{{ .lake }}} 中优化表涉及压缩或清除历史数据，以节省存储空间并提升查询性能。

<details>
  <summary>为什么要优化？</summary>
    <div>{{{ .lake }}} 使用 Parquet 格式将数据存储在表中，而 Parquet 格式按 block 组织。此外，{{{ .lake }}} 支持 time travel 功能，其中每次对表进行修改的操作都会生成一个 Parquet 文件，用于捕获并反映对表所做的更改。</div><br/>

   <div>随着表随时间累积越来越多的 Parquet 文件，可能会导致性能问题并增加存储需求。为了优化表的性能，当历史 Parquet 文件不再需要时，可以将其删除。此类优化有助于提升查询性能，并减少表占用的存储空间。</div>
</details>

## {{{ .lake }}} 数据存储：Snapshot、Segment 和 Block {#lake-data-storage-snapshot-segment-and-block}

Snapshot、segment 和 block 是 {{{ .lake }}} 用于数据存储的概念。{{{ .lake }}} 使用它们构建用于存储表数据的层次结构。

![Data storage structure](/media/tidb-cloud-lake/storage-structure.PNG)

{{{ .lake }}} 会在数据修改后自动创建表 snapshot。snapshot 表示表 segment 元信息的一个版本。

在使用 {{{ .lake }}} 时，当你通过 [AT](/tidb-cloud-lake/sql/at.md) 子句检索并查询表数据的历史版本时，最可能通过 snapshot ID 来访问某个 snapshot。

snapshot 是一个 JSON 文件，它不保存表数据本身，而是指示该 snapshot 链接到哪些 segment。如果你对某个表执行 [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)，可以查看该表已保存的 snapshots。

segment 是一个 JSON 文件，用于组织存储数据的 blocks（最少 1 个，最多 1,000 个）。如果你针对某个带有 snapshot ID 的 snapshot 执行 [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md)，可以查看该 snapshot 引用了哪些 segments。

{{{ .lake }}} 将实际的表数据保存在 Parquet 文件中，并将每个 Parquet 文件视为一个 block。如果你针对某个带有 snapshot ID 的 snapshot 执行 [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md)，可以查看该 snapshot 引用了哪些 blocks。

{{{ .lake }}} 会为每个数据库和表创建唯一 ID，用于存储 snapshot、segment 和 block 文件，并将它们保存在对象存储路径 `<bucket_name>/<tenant_id>/<db_id>/<table_id>/` 下。每个 snapshot、segment 和 block 文件都以 UUID（32 个字符的小写十六进制字符串）命名。

| 文件 | 格式 | 文件名 | 存储目录 |
|----------|---------|---------------------------------|-----------------------------------------------------|
| Snapshot | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_ss/` |
| Segment  | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_sg/` |
| Block    | parquet | `<32bitUUID>_<version>.parquet` | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_b/`  |

## 表优化 {#table-optimizations}

在 {{{ .lake }}} 中，建议将理想的 block 大小控制为 100MB（未压缩）或 1,000,000 行，并让每个 segment 包含 1,000 个 blocks。为了最大化表优化效果，关键在于清楚了解何时以及如何应用各种优化技术，例如 [Segment Compaction](#segment-compaction) 和 [Block Compaction](#block-compaction)。

- 当使用 COPY INTO 或 REPLACE INTO 命令向包含 cluster key 的表写入数据时，{{{ .lake }}} 会自动启动重新聚簇过程，以及 segment 和 block 的 compact 过程。

- Segment 和 block compaction 支持在集群环境中分布式执行。你可以通过将 ENABLE_DISTRIBUTED_COMPACT 设置为 1 来启用它们。这有助于提升集群环境中的数据查询性能和扩展性。

  ```sql
  SET enable_distributed_compact = 1;
  ```

### Segment Compaction {#segment-compaction}

当表中存在过多小 segment（每个 segment 少于 `100 blocks`）时，执行 segment compaction。

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

**语法**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT SEGMENT [LIMIT <segment_count>]
```

通过将小 segments 合并为更大的 segments 来压缩表数据。

- 选项 LIMIT 用于设置要压缩的最大 segment 数量。在这种情况下，{{{ .lake }}} 会选择并压缩最新的 segments。

**示例**

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

### Block Compaction {#block-compaction}

当表中存在大量小 blocks，或者表中插入、删除或修改的行占比较高时，执行 block compaction。

你可以通过检查每个 block 的未压缩大小是否接近理想值 `100MB` 来判断。

如果大小小于 `50MB`，建议执行 block compaction，因为这表明存在过多小 blocks：

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

> **注意：**
>
> 我们建议先执行 segment compaction，再执行 block compaction。

**语法**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT [LIMIT <segment_count>]
```

通过将小 blocks 和 segments 合并为更大的对象来压缩表数据。

- 此命令会基于最新的表数据创建一个新的 snapshot（以及压缩后的 segments 和 blocks），而不会影响现有存储文件，因此在清除历史数据之前，不会释放存储空间。

- 根据给定表的大小，执行完成可能需要较长时间。

- 选项 LIMIT 用于设置要压缩的最大 segment 数量。在这种情况下，{{{ .lake }}} 会选择并压缩最新的 segments。

- {{{ .lake }}} 会在压缩过程完成后，自动对 clustered table 重新进行聚簇。

**示例**

```sql
OPTIMIZE TABLE my_database.my_table COMPACT LIMIT 50;
```