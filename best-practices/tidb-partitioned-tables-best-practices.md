---
title: Best Practices for Using TiDB Partitioned Tables
summary: Learn best practices for using TiDB partitioned tables to improve performance, simplify data management, and handle large-scale datasets efficiently.
---

# Best Practices for Using TiDB Partitioned Tables

This guide describes how to use partitioned tables in TiDB to improve performance, simplify data management, and handle large-scale datasets efficiently.

Partitioned tables in TiDB provide a versatile approach to managing large datasets, improving query efficiency, facilitating bulk data deletion, and alleviating write hotspot issues. By dividing data into logical segments, TiDB can leverage partition pruning to skip irrelevant data during query execution. This reduces resource consumption and improves performance, particularly in Online Analytical Processing (OLAP) workloads with large datasets.

A common use case is combining [Range partitioning](/partitioned-table.md#range-partitioning) with local indexes to efficiently clean up historical data through operations such as [`ALTER TABLE ... DROP PARTITION`](/sql-statements/sql-statement-alter-table.md). This method removes obsolete data almost instantly and preserves high query efficiency when filtering by the partition key. However, after migrating from non-partitioned tables to partitioned tables, queries that cannot benefit from partition pruning, such as those lacking partition key filters, might experience degraded performance. In such cases, you can use [global indexes](/partitioned-table.md#global-indexes) to mitigate the performance impact by providing a unified index structure across all partitions.

Another scenario is using Hash or Key partitioning to address write hotspot issues, especially in workloads that use [`AUTO_INCREMENT`](/auto-increment.md) IDs where sequential inserts can overload specific TiKV Regions. Distributing writes across partitions helps balance workload, but similar to Range partitioning, queries without partition-pruning conditions might suffer performance drawbacks again, a situation where global indexes can help.

Although partitioning provides clear benefits, it also introduces challenges. For example, newly created Range partitions can create temporary hotspots. To address this issue, TiDB supports automatic or manual Region pre-splitting to balance data distribution and avoid bottlenecks.

This document examines partitioned tables in TiDB from several perspectives, including query optimization, data cleanup, write scalability, and index management. It also provides practical guidance on how to optimize partitioned table design and tune performance in TiDB through detailed scenarios and best practices.

> **Note:** 
>
> To get started with the fundamentals, see [Partitioning](/partitioned-table.md), which explains key concepts such as partition pruning, index types, and partitioning methods.

## Improve query efficiency

This section describes how to improve query efficiency by the following methods:

- [Partition pruning](#partition-pruning)
- [Query performance on secondary indexes](#query-performance-on-secondary-indexes-non-partitioned-tables-vs-local-indexes-vs-global-indexes)

### Partition pruning

Partition pruning is an optimization technique that reduces the amount of data TiDB scans when querying partitioned tables. Instead of scanning all partitions, TiDB evaluates the query filter conditions to identify the partitions that might contain matching data and scans only those partitions. This approach reduces I/O and computation overhead, which significantly improves query performance.

Partition pruning is most effective when query predicates align with the partitioning strategy. Typical use cases include the following:

- Time-series data queries: when data is partitioned by time ranges (for example, daily or monthly), queries limited to a specific time window can quickly skip unrelated partitions.
- Multi-tenant or category-based datasets: partitioning by tenant ID or category enables queries to focus on a small subset of partitions.
- Hybrid Transactional and Analytical Processing (HTAP): especially for Range partitioning, TiDB can apply partition pruning to analytical workloads on TiFlash. This optimization skips irrelevant partitions and avoids full table scans on large datasets.

For more use cases, see [Partition Pruning](/partition-pruning.md).

### Query performance on secondary indexes: Non-partitioned tables vs. local indexes vs. global indexes

In TiDB, partitioned tables use local indexes by default, where each partition maintains its own set of indexes. In contrast, a global index covers the entire table in one index and tracks rows across all partitions.

For queries that access data from multiple partitions, global indexes generally provide better performance. This is because a query using local indexes requires separate index lookups in each relevant partition, while a query using a global index performs a single lookup across the entire table.

#### Tested table types

This test compares query performance across the following table configurations:

- Non-partitioned table
- Partitioned table with local indexes
- Partitioned table with global indexes

#### Test setup

The test uses the following configuration:

- The partitioned table contains 365 Range partitions, defined on a `date` column.
- The workload simulates a high-volume OLTP query pattern, where each index key matches multiple rows.
- The test also evaluates different partition counts to measure how partition granularity affects query latency and index efficiency.

#### Schema

The following schema is used in the example.

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)(
  PARTITION `fa_2024001` VALUES LESS THAN (2025001),
  PARTITION `fa_2024002` VALUES LESS THAN (2025002),
  PARTITION `fa_2024003` VALUES LESS THAN (2025003),
  ...
  PARTITION `fa_2024365` VALUES LESS THAN (2025365)
);
```

#### SQL

The following SQL statement filters on the secondary index (`sid`) without including the partition key (`date`):

```sql
SELECT `fa`.*
FROM `fa`
WHERE `fa`.`sid` IN (
  1696271179344,
  1696317134004,
  1696181972136,
  ...
  1696159221765
);
```

This query pattern is representative because it:

- Filters on a secondary index without the partition key.
- Triggers a local index lookup for each partition due to lack of pruning.
- Generates significantly more table lookup tasks for partitioned tables.

#### Test results

The following table shows results for a query returning 400 rows from a table with 365 Range partitions.

| Configuration | Average query time | Cop tasks (index scan) | Cop tasks (table lookup) | Total Cop tasks |
|---|---|---|---|---|
| Non-partitioned table | 12.6 ms | 72 | 79 | 151 |
| Partitioned table with local indexes | 108 ms | 600 | 375 | 975 |
| Partitioned table with global indexes | 14.8 ms | 69 | 383 | 452 |

- **Non-partitioned table**: provides the best performance with the fewest tasks. Suitable for most OLTP workloads.
- **Partitioned table with global indexes**: improve index scan efficiency, but table lookups remain expensive when many rows match.
- **Partitioned table with local indexes**: when the query condition does not include the partition key, local index queries scan all partitions.
> **Note:**
>
> - **Average query time** is sourced from the `statement_summary` view.
> - **Cop tasks** metrics are derived from the execution plan.

#### Execution plan examples

The following examples show the execution plans for each configuration.

<details>
<summary><b>Non-partitioned table</b></summary>

```
| id                        | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory   | disk |
|---------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_7             | 398.73  | 787052.13 | 400     | root      |                                      | time:11.5ms, loops:2, index_task:{total_time:3.34ms, fetch_handle:3.34ms, build:600ns, wait:2.86µs}, table_task:{total_time:7.55ms, num:1, concurrency:5}, next:{wait_index:3.49ms, wait_table_lookup_build:492.5µs, wait_table_lookup_resp:7.05ms} |  | 706.7 KB | N/A  |
| IndexRangeScan_5(Build)   | 398.73  | 90633.86  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:3.16ms, loops:3, cop_task:{num:72, max:780.4µs, min:394.2µs, avg:566.7µs, p95:748µs, max_proc_keys:20, p95_proc_keys:10, tot_proc:3.66ms, tot_wait:18.6ms, copr_cache_hit_ratio:0.00, build_task_duration:94µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:72, total_time:40.1ms}}, tikv_task:{proc max:1ms, min:0s, avg:27.8µs, p80:0s, p95:0s, iters:72, tasks:72}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:480, get_snapshot_time:17.7ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:160}}}, time_detail:{total_process_time:3.66ms, total_wait_time:18.6ms, total_kv_read_wall_time:2ms, tikv_wall_time:27.4ms} | range:[1696125963161,1696125963161], …, [1696317134004,1696317134004], keep order:false | N/A | N/A |
| TableRowIDScan_6(Probe)   | 398.73  | 166072.78 | 400     | cop[tikv] | table:fa                             | time:7.01ms, loops:2, cop_task:{num:79, max:4.98ms, min:0s, avg:514.9µs, p95:3.75ms, max_proc_keys:10, p95_proc_keys:5, tot_proc:15ms, tot_wait:21.4ms, copr_cache_hit_ratio:0.00, build_task_duration:341.2µs, max_distsql_concurrency:1, max_extra_concurrency:7, store_batch_num:62}, rpc_info:{Cop:{num_rpc:17, total_time:40.5ms}}, tikv_task:{proc max:0s, min:0s, avg:0s, p80:0s, p95:0s, iters:79, tasks:79}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:20.8ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1600}}}, time_detail:{total_process_time:15ms, total_wait_time:21.4ms, tikv_wall_time:10.9ms} | keep order:false | N/A | N/A |
```

</details>

<details>
<summary><b>Partitioned table with global indexes</b></summary>

```
| id                     | estRows | estCost   | actRows | task      | access object                                   | execution info | operator info | memory   | disk |
|------------------------|---------|-----------|---------|-----------|-------------------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_8          | 398.73  | 786959.21 | 400     | root      | partition:all                                   | time:12.8ms, loops:2, index_task:{total_time:2.71ms, fetch_handle:2.71ms, build:528ns, wait:3.23µs}, table_task:{total_time:9.03ms, num:1, concurrency:5}, next:{wait_index:3.27ms, wait_table_lookup_build:1.49ms, wait_table_lookup_resp:7.53ms} |  | 693.9 KB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 102593.43 | 400     | cop[tikv] | table:fa, index:index_fa_on_sid_global(sid, id)| time:2.49ms, loops:3, cop_task:{num:69, max:997µs, min:213.8µs, avg:469.8µs, p95:986.6µs, max_proc_keys:15, p95_proc_keys:10, tot_proc:13.4ms, tot_wait:1.52ms, copr_cache_hit_ratio:0.00, build_task_duration:498.4µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:69, total_time:31.8ms}}, tikv_task:{proc max:1ms, min:0s, avg:101.4µs, p80:0s, p95:1ms, iters:69, tasks:69}, scan_detail:{total_process_keys:400, total_process_keys_size:31200, total_keys:480, get_snapshot_time:679.9µs, rocksdb:{key_skipped_count:400, block:{cache_hit_count:189, read_count:54, read_byte:347.7 KB, read_time:6.17ms}}}, time_detail:{total_process_time:13.4ms, total_wait_time:1.52ms, total_kv_read_wall_time:7ms, tikv_wall_time:19.3ms} | range:[1696125963161,1696125963161], …, keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.64 | 400     | cop[tikv] | table:fa                                        | time:7.47ms, loops:2, cop_task:{num:383, max:4.07ms, min:0s, avg:488.5µs, p95:2.59ms, max_proc_keys:2, p95_proc_keys:1, tot_proc:203.3ms, tot_wait:429.5ms, copr_cache_hit_ratio:0.00, build_task_duration:1.3ms, max_distsql_concurrency:1, max_extra_concurrency:31, store_batch_num:305}, rpc_info:{Cop:{num_rpc:78, total_time:186.3ms}}, tikv_task:{proc max:3ms, min:0s, avg:517µs, p80:1ms, p95:1ms, iters:383, tasks:383}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:2.99ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1601, read_count:799, read_byte:10.1 MB, read_time:131.6ms}}}, time_detail:{total_process_time:203.3ms, total_suspend_time:6.31ms, total_wait_time:429.5ms, total_kv_read_wall_time:198ms, tikv_wall_time:163ms} | keep order:false, stats:partial[...] | N/A | N/A |
```

</details>

<details>
<summary><b>Partitioned table with local indexes</b></summary>

```
| id                     | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory  | disk  |
|------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|---------|-------|
| IndexLookUp_7          | 398.73  | 784450.63 | 400     | root      | partition:all                        | time:290.8ms, loops:2, index_task:{total_time:103.6ms, fetch_handle:7.74ms, build:133.2µs, wait:95.7ms}, table_task:{total_time:551.1ms, num:217, concurrency:5}, next:{wait_index:179.6ms, wait_table_lookup_build:391µs, wait_table_lookup_resp:109.5ms} |  | 4.30 MB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 90633.73  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:10.8ms, loops:800, cop_task:{num:600, max:65.6ms, min:1.02ms, avg:22.2ms, p95:45.1ms, max_proc_keys:5, p95_proc_keys:3, tot_proc:6.81s, tot_wait:4.77s, copr_cache_hit_ratio:0.00, build_task_duration:172.8ms, max_distsql_concurrency:3}, rpc_info:{Cop:{num_rpc:600, total_time:13.3s}}, tikv_task:{proc max:54ms, min:0s, avg:13.9ms, p80:20ms, p95:30ms, iters:600, tasks:600}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:29680, get_snapshot_time:2.47s, rocksdb:{key_skipped_count:400, block:{cache_hit_count:117580, read_count:29437, read_byte:104.9 MB, read_time:3.24s}}}, time_detail:{total_process_time:6.81s, total_suspend_time:1.51s, total_wait_time:4.77s, total_kv_read_wall_time:8.31s, tikv_wall_time:13.2s}} | range:[1696125963161,...,1696317134004], keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.49 | 400     | cop[tikv] | table:fa                             | time:514ms, loops:434, cop_task:{num:375, max:31.6ms, min:0s, avg:1.33ms, p95:1.67ms, max_proc_keys:2, p95_proc_keys:2, tot_proc:220.7ms, tot_wait:242.2ms, copr_cache_hit_ratio:0.00, build_task_duration:27.8ms, max_distsql_concurrency:1, max_extra_concurrency:1, store_batch_num:69}, rpc_info:{Cop:{num_rpc:306, total_time:495.5ms}}, tikv_task:{proc max:6ms, min:0s, avg:597.3µs, p80:1ms, p95:1ms, iters:375, tasks:375}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:158.3ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:3197, read_count:803, read_byte:10.2 MB, read_time:113.5ms}}}, time_detail:{total_process_time:220.7ms, total_suspend_time:5.39ms, total_wait_time:242.2ms, total_kv_read_wall_time:224ms, tikv_wall_time:430.5ms}} | keep order:false, stats:partial[...] | N/A | N/A |
```

</details>

#### Create a global index on a partitioned table

You can create a global index on a partitioned table using one of the following methods.

> **Note:**
>
> - In TiDB v8.5.3 and earlier versions, you can only create global indexes on unique columns. Starting from v8.5.4, TiDB supports global indexes on non-unique columns. This limitation will be removed in a future LTS version.
> - For non-unique global indexes, use `ADD INDEX` instead of `ADD UNIQUE INDEX`.
> - You must explicitly specify the `GLOBAL` keyword.

##### Option 1: Use `ALTER TABLE`

To add a global index to an existing partitioned table, use `ALTER TABLE`:

```sql
ALTER TABLE <table_name>
ADD UNIQUE INDEX <index_name> (col1, col2) GLOBAL;
```

##### Option 2: Define the index at table creation

To create a global index when creating a table, define the global index inline in the `CREATE TABLE` statement:

```sql
CREATE TABLE t (
  id BIGINT NOT NULL,
  col1 VARCHAR(50),
  col2 VARCHAR(50),
  -- other columns...
  UNIQUE GLOBAL INDEX idx_col1_col2 (col1, col2)
)
PARTITION BY RANGE (id) (
  PARTITION p0 VALUES LESS THAN (10000),
  PARTITION p1 VALUES LESS THAN (20000),
  PARTITION pMax VALUES LESS THAN MAXVALUE
);
```

#### Performance summary

The performance overhead of TiDB partitioned tables depends on the number of partitions and the index type.

- **Partition count**: Performance degrades as the number of partitions increases. While the impact might be negligible for a small number of partitions, this varies based on the workload.
- **Local indexes**: if a query does not include an effective partition pruning condition, the number of partitions directly determines the number of [Remote Procedure Calls (RPCs)](https://docs.pingcap.com/tidb/stable/glossary/#remote-procedure-call-rpc). This means more partitions typically lead to more RPCs and higher latency.
- **Global indexes**: the performance depends on both the number of partitions involved and the number of rows that require table lookups. For very large tables where data is distributed across multiple Regions, accessing data through a global index provides performance similar to that of a non-partitioned table, because both scenarios involve multiple cross-Region RPCs.

#### Recommendations

Use the following guidelines when you design partitioned tables and indexes in TiDB:

- Use partitioned tables only when necessary. For most OLTP workloads, a well-indexed, non-partitioned table provides better performance and simpler management.
- Use local indexes when all queries include an effective partition pruning condition that matches a small number of partitions.
- Use global indexes for critical queries that lack effective partition pruning conditions and match a large number of partitions.
- Use local indexes only when DDL operation efficiency (such as fast `DROP PARTITION`) is a priority and any potential performance impact is acceptable.

## Facilitate bulk data deletion

In TiDB, you can remove historical data by using [TTL (Time to Live)](/time-to-live.md) or by manually dropping partitions. Although both methods delete data, their performance characteristics differ significantly. The following test results show that dropping partitions is generally faster and consumes fewer resources, making it a better option for large datasets and frequent data purging.

### Differences between TTL and `DROP PARTITION`

- TTL: automatically deletes data based on its age. This method might be slower because it scans and deletes rows incrementally over time.
- `DROP PARTITION`: deletes an entire partition in a single operation. This approach is typically much faster, especially for large datasets.

#### Test case

This test compares the performance of TTL and `DROP PARTITION`.

- TTL configuration: runs every 10 minutes.
- Partition configuration: drops one partition every 10 minutes.
- Workload: background write workloads with 50 and 100 concurrent threads.

The test measures execution time, system resource usage, and the total number of rows deleted.

#### Findings

> **Note:**
>
> The performance benefits described in this section only apply to partitioned tables without global indexes. 

The following are findings about the TTL performance:

- With 50 threads, each TTL job takes 8 to 10 minutes, deleting 7 to 11 million rows.
- With 100 threads, TTL handles up to 20 million rows, but execution time increases to 15 to 30 minutes and shows higher variance.
- Under heavy workloads, TTL jobs reduce overall QPS due to additional scanning and deletion overhead.

The following are findings about the `DROP PARTITION` performance:

- The `ALTER TABLE ... DROP PARTITION` statement removes an entire partition almost immediately.
- The operation uses minimal resources because it occurs at the metadata level.
- `DROP PARTITION` is faster and more predictable than TTL, especially for large historical datasets.

#### Use TTL and `DROP PARTITION` in TiDB

The following examples use anonymized table structures. For more information about TTL, see [Periodically Delete Data Using TTL (Time to Live)](/time-to-live.md).

The following example shows a TTL-enabled table schema:

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`session_id`, `external_id`, `create_time`, `id_suffix`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
TTL=`expire_time` + INTERVAL 0 DAY TTL_ENABLE='ON'
TTL_JOB_INTERVAL='10m';
```

The following example shows a partitioned table that uses Range INTERVAL partitioning:

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (
    `session_id`, `external_id`,
    `create_time`, `id_suffix`
  ) NONCLUSTERED
)
SHARD_ROW_ID_BITS=7
PRE_SPLIT_REGIONS=2
PARTITION BY RANGE COLUMNS (create_time)
INTERVAL (10 MINUTE)
FIRST PARTITION LESS THAN ('2025-02-19 18:00:00')
...
LAST PARTITION LESS THAN ('2025-02-19 20:00:00');
```

To update `FIRST PARTITION` and `LAST PARTITION` periodically, run DDL statements similar to the following. These statements drop old partitions and create new ones.

```sql
ALTER TABLE ad_cache FIRST PARTITION LESS THAN ("${nextTimestamp}");
ALTER TABLE ad_cache LAST PARTITION LESS THAN ("${nextTimestamp}");
```

#### Recommendations

- Use partitioned tables with `DROP PARTITION` for large-scale or time-based data cleanup. This approach provides better performance, lower system impact, and simpler operational behavior.
- Use TTL for fine-grained or background data cleanup. TTL is less suitable for workloads with high write throughput or rapid deletion of large data volumes.

### Partition drop efficiency: local indexes vs. global indexes

For partitioned tables with global indexes, DDL operations such as `DROP PARTITION`, `TRUNCATE PARTITION`, and `REORGANIZE PARTITION` must update global index entries synchronously. These updates can significantly increase DDL execution time.

This section shows that `DROP PARTITION` is substantially slower on tables with global indexes than on tables with local indexes. Consider this behavior when you design partitioned tables.

#### Test case

This test creates a table with 365 partitions and approximately 1 billion rows. It compares `DROP PARTITION` performance when using global indexes and local indexes.

| Index type   | Drop partition duration |
|--------------|---------------------------|
| Global index | 76.02 seconds             |
| Local index  | 0.52 seconds              |

#### Findings

Dropping a partition on a table with a global index takes **76.02 seconds**, whereas the same operation on a table with a local index takes only **0.52 seconds**. This difference occurs because global indexes span all partitions and require additional index updates, while local indexes are dropped together with the partition data.

You can use the following SQL statement to drop a partition:

```sql
ALTER TABLE A DROP PARTITION A_2024363;
```

#### Recommendations

- If a partitioned table uses global indexes, expect longer execution times for DDL operations such as `DROP PARTITION`, `TRUNCATE PARTITION`, and `REORGANIZE PARTITION`.
- If you need to drop partitions frequently and minimize performance impact, use local indexes to achieve faster and more efficient partition management.

## Mitigate hotspot issues

In TiDB, hotspots can occur when incoming read or write traffic is unevenly distributed across Regions. This is common when the primary key is monotonically increasing, for example, an `AUTO_INCREMENT` primary key with `AUTO_ID_CACHE=1`, or a secondary index on the datetime column with the default value set to `CURRENT_TIMESTAMP`. Because new rows and index entries are always appended to the "rightmost" Region, over time, this can lead to:

- A single [Region](https://docs.pingcap.com/tidb/stable/tidb-storage/#region) handling most of the write workload, while other Regions remain idle.
- Higher read or write latency and reduced throughput.
- Limited performance gains from scaling out TiKV nodes, as the bottleneck remains concentrated on one Region.

Partitioned tables can help mitigate this problem. By applying hash or key partitioning on the primary key, TiDB can spread inserts across multiple partitions (and therefore multiple Regions), reducing hotspot contention.

> **Note:** 
>
> This section uses partitioned tables as an example for mitigating read and write hotspots. TiDB also provides other features such as [`AUTO_INCREMENT`](/auto-increment.md) and [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) for hotspot mitigation. When using partitioned tables in certain scenarios, you might need to set `merge_option=deny` to maintain partition boundaries. For more details, see [issue #58128](https://github.com/pingcap/tidb/issues/58128).

### How it works

TiDB stores table data and indexes in Regions, each covering a continuous range of row keys. When the primary key is [`AUTO_INCREMENT`](/auto-increment.md) and the secondary indexes on datetime columns are monotonically increasing:

**Without partitioning:**

- New rows always have the highest key values and are inserted into the same "last Region."
- That Region is served by one TiKV node at a time, becoming a single write bottleneck.

**With hash or key partitioning:**

- The table and the secondary indexes are split into multiple partitions using a hash or key function on the primary key or indexed columns.
- Each partition has its own set of Regions, often distributed across different TiKV nodes.
- Inserts are spread across multiple Regions in parallel, improving workload distribution and throughput.

### Use cases

If a table with an [`AUTO_INCREMENT`](/auto-increment.md) primary key experiences heavy bulk inserts and suffers from write hotspot issues, applying hash or key partitioning on the primary key can help distribute the write workload more evenly.

```sql
CREATE TABLE server_info (
  id bigint NOT NULL AUTO_INCREMENT,
  serial_no varchar(100) DEFAULT NULL,
  device_name varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  device_type varchar(50) DEFAULT NULL,
  modified_ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id) /*T![clustered_index] CLUSTERED */,
  KEY idx_serial_no (serial_no),
  KEY idx_modified_ts (modified_ts)
) /*T![auto_id_cache] AUTO_ID_CACHE=1 */
PARTITION BY KEY (id) PARTITIONS 16;
```

### Advantages

- Balanced write workload: hotspots are spread across multiple partitions, and therefore multiple Regions, reducing contention and improving insert performance.
- Query optimization via partition pruning: if queries already filter by the partition key, TiDB can prune unused partitions, scanning less data and improving query speed.

### Disadvantages

There are some risks when using partitioned tables.

- When converting a non-partitioned table to a partitioned table, TiDB creates separate Regions for each partition. This might significantly increase the total Region count. Queries that do not filter by the partition key cannot take advantage of partition pruning, forcing TiDB to scan all partitions or do index lookups in all partitions. This increases the number of coprocessor (cop) tasks and can slow down queries. For example, `serial_no` is not the partition key, which will cause the query performance regression:

    ```sql
    SELECT * FROM server_info WHERE `serial_no` = ?;
    ```

- Add a global index on the filtering columns used by these queries to reduce scanning overhead. While creating a global index can significantly slow down `DROP PARTITION` operations, hash and key partitioned tables do not support `DROP PARTITION`. In practice, such partitions are rarely truncated, making global indexes a feasible solution in these scenarios. For example:

    ```sql
    ALTER TABLE server_info ADD UNIQUE INDEX(serial_no, id) GLOBAL;
    ```

## Partition management challenges

New range partitions in a partitioned table can easily lead to hotspot issues in TiDB. This section outlines common scenarios and mitigation strategies to avoid read and write hotspots caused by new range partitions.

### Read hotspots

When using range-partitioned tables, if queries do not filter data using the partition key, new empty partitions can easily become read hotspots.

**Root cause:**

By default, TiDB creates an empty region for each partition when the table is created. If no data is written for a while, multiple empty partitions' regions might be merged into a single region.

**impact:**

When a query does not filter by partition key, TiDB scans all partitions (as seen in the execution plan `partition:all`). As a result, the single region holding multiple empty partitions is scanned repeatedly, leading to a read hotspot.

### Write hotspots

When using a time-based field as the partition key, a write hotspot might occur when switching to a new partition.

**Root cause:**

In TiDB, newly created partitions initially contain only one region on a single TiKV node. As writes concentrate on this single region, it must split into multiple regions before writes can be distributed across multiple TiKV nodes. This splitting process is the main cause of the temporary write hotspot. 

However, if the initial write traffic to this new partition is very high, the TiKV node hosting that single initial region will be under heavy write pressure. In such cases, it might not have enough spare resources (such as I/O capacity and CPU cycles) to handle both the application writes and the scheduling of newly split regions to other TiKV nodes. This can delay region distribution, keeping most writes concentrated on the same node for longer than desired.

**Impact:**

This imbalance can cause the TiKV node to trigger flow control, leading to a sharp drop in QPS, a spike in write latency, and increased CPU usage on the affected node, which in turn might impact the overall read and write performance of the cluster.

### Summary

The following table shows the summary information for non-clustered and clustered partitioned tables.

| Table type                      | Region pre-splitting | Read performance     | Write scalability | Data cleanup via partition |
|---|---|---|---|---|
| Non-clustered partitioned table | Automatic            | Lower (more lookups) | High              | Supported          | 
| Clustered partitioned table     | Manual               | High (fewer lookups) | High (if managed) | Supported          | 
| Clustered non-partitioned table | N/A                  | High                 | Stable            | Not supported      |

### Solutions for non-clustered partitioned tables

#### Advantages

- When a new partition is created in a non-clustered partitioned table configured with [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) and [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions), the regions can be automatically pre-split, significantly reducing manual intervention.
- Lower operational overhead.

#### Disadvantages

Queries using **Point Get** or **Table Range Scan** require more table lookups, which can degrade read performance for such query types.

#### Suitable scenarios

It is suitable for workloads where write scalability and operational ease are more critical than low-latency reads.

#### Best practices

To address hotspot issues caused by new range partitions, you can perform the following steps.

##### Step 1. Use `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS`

Create a partitioned table with [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) and [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) to pre-split table regions. The value of `PRE_SPLIT_REGIONS` must be less than or equal to that of `SHARD_ROW_ID_BITS`. The number of pre-split Regions for each partition is `2^(PRE_SPLIT_REGIONS)`.

```sql
CREATE TABLE employees (
  id INT NOT NULL,
  fname VARCHAR(30),
  lname VARCHAR(30),
  hired DATE NOT NULL DEFAULT '1970-01-01',
  separated DATE DEFAULT '9999-12-31',
  job_code INT,
  store_id INT,
  PRIMARY KEY (`id`,`hired`) NONCLUSTERED,
  KEY `idx_employees_on_store_id` (`store_id`)
) SHARD_ROW_ID_BITS = 2 PRE_SPLIT_REGIONS=2
PARTITION BY RANGE ( YEAR(hired) ) (
  PARTITION p0 VALUES LESS THAN (1991),
  PARTITION p1 VALUES LESS THAN (1996),
  PARTITION p2 VALUES LESS THAN (2001),
  PARTITION p3 VALUES LESS THAN (2006)
);
```

##### Step 2. Add the `merge_option=deny` attribute

Adding the [`merge_option=deny`](/table-attributes.md#control-the-region-merge-behavior-using-table-attributes) attribute to a table or partition can prevent the merging of empty regions. However, when a partition is dropped, the regions belonging to that partition will still be merged automatically.

```sql
-- table
ALTER TABLE employees ATTRIBUTES 'merge_option=deny';
-- partition
ALTER TABLE employees PARTITION `p3` ATTRIBUTES 'merge_option=deny';
```

##### Step 3. Determine split boundaries based on existing business data

To avoid hotspots when a new table or partition is created, it is often beneficial to pre-split regions before heavy writes begin. To make pre-splitting effective, configure the lower and upper boundaries for region splitting based on the actual business data distribution. Avoid setting excessively wide boundaries, as this can result in real data not being effectively distributed across TiKV nodes, defeating the purpose of pre-splitting.

Identify the minimum and maximum values from existing production data so that incoming writes are more likely to target different pre-allocated regions. The following is an example query for the existing data:

```sql
SELECT MIN(id), MAX(id) FROM employees;
```

- If the table is new and has no historical data, estimate the minimum and maximum values based on your business logic and expected data range.
- For composite primary keys or composite indexes, only the leftmost column needs to be considered when deciding split boundaries.
- If the leftmost column is a string, take string length and distribution into account to ensure even data spread.

##### Step 4. Pre-split and scatter regions

A common practice is to split the number of regions to match the number of TiKV nodes, or to be twice the number of TiKV nodes. This helps ensure that data is more evenly distributed across the cluster from the start.

##### Step 5. Split regions for the primary key and the secondary index of all partitions if needed

To split regions for the primary key of all partitions in a partitioned table, use the following SQL statement:

```sql
SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "1970-01-01") AND (100000, "9999-12-31") REGIONS <number_of_regions>;
```

This example splits each partition's primary key range into `<number_of_regions>` regions between the specified boundary values.

To split regions for the secondary index of all partitions in a partitioned table, use the following SQL statement:

```sql
SPLIT PARTITION TABLE employees INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;
```

##### Step 6. (Optional) When adding a new partition, you need to manually split regions for its primary key and indexes

```sql
ALTER TABLE employees ADD PARTITION (PARTITION p4 VALUES LESS THAN (2011));

SHOW TABLE employees PARTITION (p4) regions;

SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "2006-01-01") AND (100000, "2011-01-01") REGIONS <number_of_regions>;

SPLIT PARTITION TABLE employees PARTITION (p4) INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;

SHOW TABLE employees PARTITION (p4) regions;
```

### Solutions for clustered partitioned tables

#### Advantages

Queries using **Point Get** or **Table Range Scan** do not need additional lookups, resulting in better read performance.

#### Disadvantages

Manual region splitting is required when creating new partitions, increasing operational complexity.

#### Suitable scenarios

It is suitable when low-latency point queries are important and operational resources are available to manage region splitting.

#### Best practices

To address hotspot issues caused by new range partitions, you can perform the steps described in [Best practices for non-clustered partitioned tables](#best-practices).

### Solutions for clustered non-partitioned tables

#### Advantages

- No hotspot risks from new range partitions.
- Provides good read performance for point and range queries.

#### Disadvantages

You cannot use `DROP PARTITION` to clean up large volumes of old data to improve deletion efficiency.

#### Suitable scenarios

It is suitable for scenarios that require stable performance and do not benefit from partition-based data management.

## Convert between partitioned and non-partitioned tables

When working with large tables (for example, a table with 120 million rows), transforming between partitioned and non-partitioned schemas is sometimes required for performance tuning or schema design changes. TiDB supports several main approaches for such transformations:

- [Pipelined DML](/pipelined-dml.md): `INSERT INTO ... SELECT ...`
- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md): `IMPORT INTO ... FROM SELECT ...`
- [Online DDL](/dm/feature-online-ddl.md): Direct schema transformation via `ALTER TABLE`

This section compares the efficiency and implications of these methods in both directions of conversion, and provides best practice recommendations.

### Table schema for a partitioned table: `fa`

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
PARTITION `fa_2024003` VALUES LESS THAN (2025003),
...
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365));
```

### Table schema for a non-partitioned table: `fa_new`

```sql
CREATE TABLE `fa_new` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

These examples show converting a partitioned table to a non-partitioned table, but the same methods also work for converting a non-partitioned table to a partitioned table.

### Method 1: Pipelined DML `INSERT INTO ... SELECT`

```sql
SET tidb_dml_type = "bulk";
SET tidb_mem_quota_query = 0;
SET tidb_enable_mutation_checker = OFF;
INSERT INTO fa_new SELECT * FROM fa;
-- 120 million rows copied in 58m 42s
```

### Method 2: `IMPORT INTO ... FROM SELECT`

```sql
IMPORT INTO fa_new FROM SELECT * FROM fa WITH thread = 32, disable_precheck;
```

```
Query OK, 120000000 rows affected, 1 warning (16 min 49.90 sec)
Records: 120000000, ID: c1d04eec-fb49-49bb-af92-bf3d6e2d3d87
```

### Method 3: Online DDL

The following SQL statement converts from a partition table to a non-partitioned table:

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa REMOVE PARTITIONING;
-- real 170m12.024 s (≈ 2 h 50 m)
```

The following SQL statement converts from a non-partition table to a partitioned table:

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa_new PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365),
PARTITION `fa_2024366` VALUES LESS THAN (2025366));

Query OK, 0 rows affected, 1 warning (2 hours 31 min 57.05 sec)
```

### Findings

The following table show the time taken by each method.

| Method | Time Taken |
|--------|------------|
| Method 1: Pipelined DML: `INSERT INTO ... SELECT ...`                  | 58 m 42 s     |
| Method 2: `IMPORT INTO ... FROM SELECT ...`                            | 16 m 59 s     |
| Method 3: Online DDL (From partition table to non-partitioned table)   | 2 h 50 m      |
| Method 3: Online DDL (From non-partition table to partitioned table)   | 2 h 31 m      |
