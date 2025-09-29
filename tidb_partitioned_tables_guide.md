# Best Practices for Using TiDB Partitioned Tables

## Introduction

Partitioned tables in TiDB offer a versatile approach to managing large datasets, improving query efficiency, facilitating bulk data deletion, and alleviating write hotspot issues. By dividing data into logical segments, TiDB can leverage **partition pruning** to skip irrelevant data during query execution, reducing resource consumption and accelerating performance—particularly in OLAP workloads with massive datasets.

A common use case is **range partitioning combined with local indexes**, which enables efficient historical data cleanup through operations like DROP PARTITION. This method not only removes obsolete data almost instantly but also retains high query efficiency when filtering by the partition key. However, after migrating from non-partitioned to partitioned tables, queries that cannot benefit from partition pruning—such as those lacking partition key filters—may experience degraded performance. In such cases, [**global indexes**](https://docs.pingcap.com/tidb/stable/partitioned-table/#global-indexes) can be introduced to mitigate the performance impact by providing a unified index structure across all partitions.

Another frequent scenario is using **hash or key partitioning** to address write hotspot issues, especially in workloads relying on AUTO_INCREMENT-style IDs where sequential inserts can overload specific TiKV regions. Distributing writes across partitions helps balance load, but similar to range partitioning, queries without partition-pruning conditions may suffer performance drawbacks—again, a situation where global indexes can help.

While partitioning offers clear benefits, it also presents **common challenges**, such as **hotspots caused by newly created range partitions**. To address this, TiDB provides techniques for automatic or manual region pre-splitting, ensuring balanced data distribution and avoiding bottlenecks.

This document examines partitioned tables in TiDB from multiple angles, including query optimization, data cleanup, write scalability, and index management. Through detailed scenarios and best practices, it aims to equip you with the knowledge to make informed decisions about when and how to adopt partitioning strategies in your TiDB environment.

## Agenda

- Improving query efficiency
  - Partition pruning
  - Query performance comparison: Non-Partitioned Table vs. Local Index vs. Global Index
- Facilitating bulk data deletion
  - Data cleanup efficiency: TTL vs. Direct Partition Drop
  - Partition drop efficiency: Local Index vs Global Index
- Mitigating write hotspot issues
- Partition management challenge
  - How to avoid hotspots caused by new range partitions
- Converting between partitioned and non-partitioned tables

By understanding these aspects, you can make informed decisions on whether and how to implement partitioning in your TiDB environment.

> **Note:** If you're new to partitioned tables in TiDB, we recommend reviewing the [Partitioned Table User Guide](https://docs.pingcap.com/tidb/stable/partitioned-table) first to better understand key concepts like partition pruning, global vs. local indexes, and partition strategies.

## Improving query efficiency

### Partition Pruning

**Partition pruning** is an optimization technique that allows TiDB to reduce the amount of data scanned when executing queries against partitioned tables. Instead of scanning all partitions, TiDB analyzes the query's filter conditions and determines which partitions may contain relevant data, scanning only those partitions. This significantly improves query performance by reducing I/O and computation overhead.

#### Applicable Scenarios

Partition pruning is most beneficial in scenarios where query predicates match the partitioning strategy. Common use cases include:

- **Time-series data queries**: When data is partitioned by time ranges (e.g., daily, monthly), queries restricted to a specific time period can quickly skip unrelated partitions.
- **Multi-tenant or category-based datasets**: Partitioning by tenant ID or category enables queries to focus on a small subset of partitions.
- **Hybrid Transactional/Analytical Processing (HTAP)**: Especially for range partitioning, TiDB can leverage partition pruning in analytical workloads on TiFlash to skip irrelevant partitions and scan only the necessary subset, preventing **full table scans** on large datasets.

For more use cases, see [Partition Pruning](https://docs.pingcap.com/tidb/stable/partition-pruning/).

### Query Performance on Secondary Index: Non-Partitioned Table vs. Local Index vs. Global Index

In TiDB, local indexes are the default indexing strategy for partitioned tables. Each partition maintains its own set of indexes, while a Global Index refers to an index that spans all partitions in a partitioned table. Unlike Local Indexes, which are partition-specific and stored separately within each partition, a Global Index maintains a single, unified index across the entire table. This index includes references to all rows, regardless of which partition they belong to, and thus can provide global queries and operations, such as joins or lookups, with faster access.

#### What Did We Test

We evaluated query performance across three table configurations in TiDB:
- Non-Partitioned Table
- Partitioned Table with Global Index
- Partitioned Table with Local Index

#### Test Setup

- The query **accesses data via a secondary index** and uses IN conditions across multiple values.
- The **partitioned table** had **366 partitions**, defined by **range partitioning on a datetime column**.
- Each matching key could return **multiple rows**, simulating a **high-volume OLTP-style query pattern**.
- We also evaluated the **impact of different partition counts** to understand how partition granularity influences latency and index performance.

#### Schema

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `yeardate` int NOT NULL,
  PRIMARY KEY (`id`,`yeardate`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1284046228560811404
PARTITION BY RANGE (`yeardate`)
(PARTITION `fa_2024001` VALUES LESS THAN (2024001),
PARTITION `fa_2024002` VALUES LESS THAN (2024002),
PARTITION `fa_2024003` VALUES LESS THAN (2024003),
...
...
PARTITION `fa_2024366` VALUES LESS THAN (2024366))
```

#### SQL

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

- Query filters on secondary index, but does **not include the partition key**.
- Causes **Local Index** to scan across all partitions due to lack of pruning.
- Table lookup tasks are significantly higher for partitioned tables.

#### Findings

Data came from a table with **366 range partitions** (e.g., by date).
- The **Average Query Time** was obtained from the statement_summary view.
- The query used a **secondary index** and returned **400 rows**.

Metrics collected:
- **Average Query Time**: from statement_summary
- **Cop Tasks** (Index Scan + Table Lookup): from execution plan

#### Test Results

| Configuration | Average Query Time | Cop task for index range scan | Cop task for table lookup | Total Cop tasks | Key Takeaways |
|---|---|---|---|---|---|
| Non-Partitioned Table | 12.6 ms | 72 | 79 | 151 | Delivering the best performance with the fewest Cop tasks — ideal for most OLTP use cases. |
| Partitioned Table with Local Index | 108 ms | 600 | 375 | 975 | When the partition key is not used in the query condition, local index queries will scan all partitions. |
| Partitioned Table with Global Index | 14.8 ms | 69 | 383 | 452 | Improving index scan efficiency, but table lookups can still be expensive if many rows match. |

#### Execution Plan Examples

**Non-partitioned table**

```yaml
| id                        | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory   | disk |
|---------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_7             | 398.73  | 787052.13 | 400     | root      |                                      | time:11.5ms, loops:2, index_task:{total_time:3.34ms, fetch_handle:3.34ms, build:600ns, wait:2.86µs}, table_task:{total_time:7.55ms, num:1, concurrency:5}, next:{wait_index:3.49ms, wait_table_lookup_build:492.5µs, wait_table_lookup_resp:7.05ms} |  | 706.7 KB | N/A  |
| IndexRangeScan_5(Build)   | 398.73  | 90633.86  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:3.16ms, loops:3, cop_task:{num:72, max:780.4µs, min:394.2µs, avg:566.7µs, p95:748µs, max_proc_keys:20, p95_proc_keys:10, tot_proc:3.66ms, tot_wait:18.6ms, copr_cache_hit_ratio:0.00, build_task_duration:94µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:72, total_time:40.1ms}}, tikv_task:{proc max:1ms, min:0s, avg:27.8µs, p80:0s, p95:0s, iters:72, tasks:72}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:480, get_snapshot_time:17.7ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:160}}}, time_detail:{total_process_time:3.66ms, total_wait_time:18.6ms, total_kv_read_wall_time:2ms, tikv_wall_time:27.4ms} | range:[1696125963161,1696125963161], …, [1696317134004,1696317134004], keep order:false | N/A | N/A |
| TableRowIDScan_6(Probe)   | 398.73  | 166072.78 | 400     | cop[tikv] | table:fa                             | time:7.01ms, loops:2, cop_task:{num:79, max:4.98ms, min:0s, avg:514.9µs, p95:3.75ms, max_proc_keys:10, p95_proc_keys:5, tot_proc:15ms, tot_wait:21.4ms, copr_cache_hit_ratio:0.00, build_task_duration:341.2µs, max_distsql_concurrency:1, max_extra_concurrency:7, store_batch_num:62}, rpc_info:{Cop:{num_rpc:17, total_time:40.5ms}}, tikv_task:{proc max:0s, min:0s, avg:0s, p80:0s, p95:0s, iters:79, tasks:79}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:20.8ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1600}}}, time_detail:{total_process_time:15ms, total_wait_time:21.4ms, tikv_wall_time:10.9ms} | keep order:false | N/A | N/A |
```

**Partition table with global index**
```yaml
| id                     | estRows | estCost   | actRows | task      | access object                                   | execution info | operator info | memory   | disk |
|------------------------|---------|-----------|---------|-----------|-------------------------------------------------|----------------|---------------|----------|------|
| IndexLookUp_8          | 398.73  | 786959.21 | 400     | root      | partition:all                                   | time:12.8ms, loops:2, index_task:{total_time:2.71ms, fetch_handle:2.71ms, build:528ns, wait:3.23µs}, table_task:{total_time:9.03ms, num:1, concurrency:5}, next:{wait_index:3.27ms, wait_table_lookup_build:1.49ms, wait_table_lookup_resp:7.53ms} |  | 693.9 KB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 102593.43 | 400     | cop[tikv] | table:fa, index:index_fa_on_sid_global(sid, id)| time:2.49ms, loops:3, cop_task:{num:69, max:997µs, min:213.8µs, avg:469.8µs, p95:986.6µs, max_proc_keys:15, p95_proc_keys:10, tot_proc:13.4ms, tot_wait:1.52ms, copr_cache_hit_ratio:0.00, build_task_duration:498.4µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:69, total_time:31.8ms}}, tikv_task:{proc max:1ms, min:0s, avg:101.4µs, p80:0s, p95:1ms, iters:69, tasks:69}, scan_detail:{total_process_keys:400, total_process_keys_size:31200, total_keys:480, get_snapshot_time:679.9µs, rocksdb:{key_skipped_count:400, block:{cache_hit_count:189, read_count:54, read_byte:347.7 KB, read_time:6.17ms}}}, time_detail:{total_process_time:13.4ms, total_wait_time:1.52ms, total_kv_read_wall_time:7ms, tikv_wall_time:19.3ms} | range:[1696125963161,1696125963161], …, keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.64 | 400     | cop[tikv] | table:fa                                        | time:7.47ms, loops:2, cop_task:{num:383, max:4.07ms, min:0s, avg:488.5µs, p95:2.59ms, max_proc_keys:2, p95_proc_keys:1, tot_proc:203.3ms, tot_wait:429.5ms, copr_cache_hit_ratio:0.00, build_task_duration:1.3ms, max_distsql_concurrency:1, max_extra_concurrency:31, store_batch_num:305}, rpc_info:{Cop:{num_rpc:78, total_time:186.3ms}}, tikv_task:{proc max:3ms, min:0s, avg:517µs, p80:1ms, p95:1ms, iters:383, tasks:383}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:2.99ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1601, read_count:799, read_byte:10.1 MB, read_time:131.6ms}}}, time_detail:{total_process_time:203.3ms, total_suspend_time:6.31ms, total_wait_time:429.5ms, total_kv_read_wall_time:198ms, tikv_wall_time:163ms} | keep order:false, stats:partial[...] | N/A | N/A |
```

**Partition table with local index**
```yaml
| id                     | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory  | disk  |
|------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|---------|-------|
| IndexLookUp_7          | 398.73  | 784450.63 | 400     | root      | partition:all                        | time:290.8ms, loops:2, index_task:{total_time:103.6ms, fetch_handle:7.74ms, build:133.2µs, wait:95.7ms}, table_task:{total_time:551.1ms, num:217, concurrency:5}, next:{wait_index:179.6ms, wait_table_lookup_build:391µs, wait_table_lookup_resp:109.5ms} |  | 4.30 MB | N/A  |
| IndexRangeScan_5(Build)| 398.73  | 90633.73  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:10.8ms, loops:800, cop_task:{num:600, max:65.6ms, min:1.02ms, avg:22.2ms, p95:45.1ms, max_proc_keys:5, p95_proc_keys:3, tot_proc:6.81s, tot_wait:4.77s, copr_cache_hit_ratio:0.00, build_task_duration:172.8ms, max_distsql_concurrency:3}, rpc_info:{Cop:{num_rpc:600, total_time:13.3s}}, tikv_task:{proc max:54ms, min:0s, avg:13.9ms, p80:20ms, p95:30ms, iters:600, tasks:600}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:29680, get_snapshot_time:2.47s, rocksdb:{key_skipped_count:400, block:{cache_hit_count:117580, read_count:29437, read_byte:104.9 MB, read_time:3.24s}}}, time_detail:{total_process_time:6.81s, total_suspend_time:1.51s, total_wait_time:4.77s, total_kv_read_wall_time:8.31s, tikv_wall_time:13.2s}} | range:[1696125963161,...,1696317134004], keep order:false, stats:partial[...] | N/A | N/A |
| TableRowIDScan_6(Probe)| 398.73  | 165221.49 | 400     | cop[tikv] | table:fa                             | time:514ms, loops:434, cop_task:{num:375, max:31.6ms, min:0s, avg:1.33ms, p95:1.67ms, max_proc_keys:2, p95_proc_keys:2, tot_proc:220.7ms, tot_wait:242.2ms, copr_cache_hit_ratio:0.00, build_task_duration:27.8ms, max_distsql_concurrency:1, max_extra_concurrency:1, store_batch_num:69}, rpc_info:{Cop:{num_rpc:306, total_time:495.5ms}}, tikv_task:{proc max:6ms, min:0s, avg:597.3µs, p80:1ms, p95:1ms, iters:375, tasks:375}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:158.3ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:3197, read_count:803, read_byte:10.2 MB, read_time:113.5ms}}}, time_detail:{total_process_time:220.7ms, total_suspend_time:5.39ms, total_wait_time:242.2ms, total_kv_read_wall_time:224ms, tikv_wall_time:430.5ms}} | keep order:false, stats:partial[...] | N/A | N/A |
```
[Similar detailed execution plans for partitioned tables with global and local indexes would follow...]

#### How to Create a Global Index on a Partitioned Table in TiDB

**Option 1: Add via ALTER TABLE**

```sql
ALTER TABLE <table_name>
ADD UNIQUE INDEX <index_name> (col1, col2) GLOBAL;
```

- Adds a global index to an existing partitioned table.
- GLOBAL must be explicitly specified.
- You can also use ADD INDEX for non-unique global indexes.

**Option 2: Define Inline on Table Creation**

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

#### Summary

The performance overhead of partitioned tables in TiDB depends significantly on the number of partitions and the type of index used.

- The more partitions you have, the more severe the potential performance degradation.
- With a smaller number of partitions, the impact may not be as noticeable, but it's still workload-dependent.
- For local indexes, if a query does not include effective partition pruning conditions, the number of partitions directly correlates with the number of RPCs triggered. This means more partitions will likely result in more RPCs, leading to higher latency.
- For global indexes, the number of RPCs and the degree of performance regression depend on both the number of partitions involved and how many rows need to be retrieved (i.e., the number of rows requiring table lookups).

#### Recommendation

- Avoid partitioned tables unless truly necessary. For most OLTP workloads, a well-indexed non-partitioned table performs better and is easier to manage.
- If you must use partitioned tables, benchmark both global index and local index strategies under your workload.
- Use global indexes when query performance across partitions is critical.
- Choose local indexes only if your main concern is DDL efficiency, such as fast DROP PARTITION, and the performance side effect from the partition table is acceptable.

## Facilitating Bulk Data Deletion

### Data Cleanup Efficiency: TTL vs. Direct Partition Drop

In TiDB, historical data cleanup can be handled either by **TTL (Time-to-Live)** or **manual partition drop**. While both methods serve the same purpose, they differ significantly in performance. Our tests show that dropping partitions is generally faster and less resource-intensive, making it a better choice for large datasets and frequent purging needs.

#### What's the difference?

- **TTL**: Automatically removes data based on its age, but may be slower due to the need to scan and clean data over time.
- **Partition Drop**: Deletes an entire partition at once, making it much faster, especially when dealing with large datasets.

#### What Did We Test

To compare the performance of TTL and partition drop, we configured TTL to execute every 10 minutes and created a partitioned version of the same table, dropping one partition at the same interval for comparison. Both approaches were tested under background write loads of 50 and 100 concurrent threads. We measured key metrics such as execution time, system resource utilization, and the total number of rows deleted.

#### Findings

**TTL Performance:**
- On a high-write table, TTL runs every 10 minutes.
- With 50 threads, each TTL job took 8–10 minutes, deleting 7–11 million rows.
- With 100 threads, it handled up to 20 million rows, but execution time increased to 15–30 minutes, with greater variance.
- TTL jobs impacted system performance under high load due to extra scanning and deletion activity, reducing overall QPS.

**Partition Drop Performance:**
- DROP PARTITION removes an entire data segment instantly, with minimal resource usage.
- DROP PARTITION is a metadata-level operation, making it much faster and more predictable than TTL, especially when managing large volumes of historical data.

#### How to Use TTL and Partition Drop in TiDB

In this experiment, the table structures have been anonymized. For more detailed information on the usage of TTL (Time To Live), please refer to the official documentation at https://docs.pingcap.com/tidb/stable/time-to-live/.

**TTL schema**

```sql
CREATE TABLE `ad_cache` (
  `session` varchar(255) NOT NULL,
  `ad_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `data` mediumblob DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `is_delete` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`session`, `ad_id`, `create_time`, `suffix`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
TTL=`expire_time` + INTERVAL 0 DAY TTL_ENABLE='ON'
TTL_JOB_INTERVAL='10m'
```

**Drop Partition (Range INTERVAL partitioning)**

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
LAST PARTITION LESS THAN ('2025-02-19 20:00:00')
```

It's required to run DDL alter table partition ... to change the FIRST PARTITION and LAST PARTITION periodically. These two DDL statements can drop the old partitions and create new ones.

```sql
ALTER TABLE ad_cache FIRST PARTITION LESS THAN ("${nextTimestamp}")
ALTER TABLE ad_cache LAST PARTITION LESS THAN ("${nextTimestamp}")
```

#### Recommendation

For workloads with **large or time-based data cleanup**, prefer using **partitioned tables with DROP PARTITION**. It offers better performance, lower system impact, and simpler management. TTL is still useful for finer-grained or background cleanup but may not be optimal under high write pressure or when deleting large volumes of data quickly.

### Partition Drop Efficiency: Local Index vs Global Index

Partition table with Global Index requires synchronous updates to the global index, potentially increasing significant execution time for DDL operations, such as DROP PARTITION, TRUNCATE PARTITION, or REORG PARTITION. In this section, the tests show that DROP PARTITION is much slower when using a **Global Index** compared to a **Local Index**. This should be considered when designing partitioned tables.

#### What Did We Test

We created a table with **366 partitions** and tested the DROP PARTITION performance using both **Global Index** and **Local Index**. The total number of rows was **1 billion**.

| Index Type | Duration (drop partition) |
|---|---|
| Global Index | 1 min 16.02 s |
| Local Index | 0.52 s |

#### Findings

Dropping a partition on a table with a Global Index took **76 seconds**, while the same operation with a Local Index took only **0.52 seconds**. The reason is that Global Indexes span all partitions and require more complex updates, while Local Indexes are limited to individual partitions and are easier to handle.

**Global Index**

```sql
mysql> alter table A drop partition A_2024363;
Query OK, 0 rows affected (1 min 16.02 sec)
```

**Local Index**

```sql
mysql> alter table A drop partition A_2024363;
Query OK, 0 rows affected (0.52 sec)
```

#### Recommendation

When a partitioned table contains global indexes, performing certain DDL operations such as DROP PARTITION, TRUNCATE PARTITION, or REORG PARTITION requires synchronously updating the global index values. This can significantly increase the execution time of these DDL operations.

If you need to drop partitions frequently and minimize the performance impact on the system, it's better to use **local indexes** for faster and more efficient operations.

## Mitigating Write Hotspot Issues

### Background

In TiDB, **write hotspots** occur when incoming write traffic is unevenly distributed across Regions.

This is common when the primary key is **monotonically increasing**—for example, an AUTO_INCREMENT primary key with AUTO_ID_CACHE=1, or secondary index on datetime column with default value set to CURRENT_TIMESTAMP—because new rows and index entries are always appended to the "rightmost" Region. Over time, this can lead to:

- A single Region handling most of the write workload, while other Regions remain idle.
- Higher write latency and reduced throughput.
- Limited performance gains from scaling out TiKV nodes, as the bottleneck remains concentrated on one Region.

**Partitioned tables** can help mitigate this problem. By applying **hash** or **key** partitioning on the primary key, TiDB can spread inserts across multiple partitions (and therefore multiple Regions), reducing hotspot contention.

### How It Works

TiDB stores table data in **Regions**, each covering a continuous range of row keys.

When the primary key is AUTO_INCREMENT and the secondary indexes on datetime columns are monotonically increasing:

**Without Partitioning:**
- New rows always have the highest key values and are inserted into the same "last Region."
- That Region is served by one TiKV node at a time, becoming a single write bottleneck.

**With Hash/Key Partitioning:**
- The table and the secondary indexes are split into multiple partitions using a hash or key function on the primary key or indexed columns.
- Each partition has its own set of Regions, often distributed across different TiKV nodes.
- Inserts are spread across multiple Regions in parallel, improving load distribution and throughput.

### Use Case

If a table with an AUTO_INCREMENT primary key experiences heavy bulk inserts and suffers from write hotspot issues, applying **hash** or **key** partitioning on the primary key can help distribute the write load more evenly.

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

### Pros

- **Balanced Write Load** — Hotspots are spread across multiple partitions, reducing contention and improving insert performance.
- **Query Optimization via Partition Pruning** — If queries already filter by the partition key, TiDB can prune unused partitions, scanning less data and improving query speed.

### Cons

**Potential Query Performance Drop Without Partition Pruning**

When converting a non-partitioned table to a partitioned table, TiDB creates a separate Region for each partition. This may significantly increase the total Region count. Queries that do not filter by the partition key cannot take advantage of partition pruning, forcing TiDB to scan all partitions. This increases the number of coprocessor (cop) tasks and can slow down queries. Example:

```sql
select * from server_info where `serial_no` = ?
```

**Mitigation**: Add a **global index** on the filtering columns used by these queries to reduce scanning overhead. While creating a global index can significantly slow down DROP PARTITION operations, **hash and key partitioned tables do not support DROP PARTITION**. In practice, such partitions are rarely removed, making global indexes a feasible solution in these scenarios. Example:

```sql
ALTER TABLE server_info ADD UNIQUE INDEX(serial_no, id) GLOBAL;
```

## Partition Management Challenge

### How to Avoid Hotspots Caused by New Range Partitions

#### Overview

New range partitions in a partitioned table can easily lead to hotspot issues in TiDB. This section outlines common scenarios and mitigation strategies to avoid read and write hotspots caused by range partitions.

#### Common Hotspot Scenarios

**Read Hotspot**

When using **range-partitioned tables**, if queries do **not** filter data using the partition key, new empty partitions can easily become read hotspots.

**Root Cause:**
By default, TiDB creates an empty region for each partition when the table is created. If no data is written for a while, multiple empty partitions' regions may be merged into a **single region**.

**Impact:**
When a query does **not filter by partition key**, TiDB will **scan all partitions** (as seen in the execution plan partition:all). As a result, the single region holding multiple empty partitions will be scanned repeatedly, leading to a **read hotspot**.

**Write Hotspot**

When using a time-based field as the partition key, a write hotspot may occur when switching to a new partition:

**Root Cause:**
In TiDB, any newly created table or partition initially contains only **one region** (data block), which is randomly placed on a single TiKV node. As data begins to be written, this region will eventually **split** into multiple regions, and PD will schedule these new regions to other TiKV nodes.

However, if the initial write traffic to this new partition is **very high**, the TiKV node hosting that single initial region will be under heavy write pressure. In such cases, it may not have enough spare resources (I/O capacity, CPU cycles) to handle both the application writes and the scheduling of newly split regions to other TiKV nodes. This can delay region distribution, keeping most writes concentrated on the same node for longer than desired.

**Impact:**
This imbalance can cause that TiKV node to trigger **flow control**, leading to a sharp drop in QPS, a spike in write latency, and increased CPU usage on the affected node, which in turn may impact the overall read and write performance of the cluster.

#### Solutions

**1. NONCLUSTERED Partitioned Table**

**Pros:**
- When a new partition is created in a **NONCLUSTERED Partitioned Table** configured with SHARD_ROW_ID_BITS and [PRE_SPLIT_REGIONS](https://docs.pingcap.com/tidb/stable/sql-statement-split-region/#pre_split_regions), the regions can be **automatically pre-split**, significantly reducing manual intervention.
- Lower operational overhead.

**Cons:**
- Queries using **Point Get** or **Table Range Scan** will require **more table lookups**, which can degrade read performance for such query types.

**Recommendation:**
- Suitable for workloads where write scalability and operational ease are more critical than low-latency reads.

**Best Practices**

Create a partitioned table with SHARD_ROW_ID_BITS and PRE_SPLIT_REGIONS to pre-split table regions. The value of PRE_SPLIT_REGIONS must be less than or equal to that of SHARD_ROW_ID_BITS. The number of pre-split Regions for each partition is 2^(PRE_SPLIT_REGIONS).

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
)SHARD_ROW_ID_BITS = 2 PRE_SPLIT_REGIONS=2
PARTITION BY RANGE ( YEAR(hired) ) (
  PARTITION p0 VALUES LESS THAN (1991),
  PARTITION p1 VALUES LESS THAN (1996),
  PARTITION p2 VALUES LESS THAN (2001),
  PARTITION p3 VALUES LESS THAN (2006)
);
```

Adding the [merge_option=deny](https://docs.pingcap.com/tidb/stable/table-attributes/#control-the-region-merge-behavior-using-table-attributes) attribute to a table or partition can prevent the merging of empty regions. However, when a partition is dropped, the regions belonging to that partition will still be merged automatically.

```sql
-- table
ALTER TABLE employees ATTRIBUTES 'merge_option=deny';
-- partition
ALTER TABLE employees PARTITION `p3` ATTRIBUTES 'merge_option=deny';
```

**Determining split boundaries based on existing business data**

To avoid hotspots when a new table or partition is created, it is often beneficial to **pre-split** regions before heavy writes begin. To make pre-splitting effective, configure the **lower and upper boundaries** for region splitting based on the **actual business data distribution**. Avoid setting excessively wide boundaries, as this can result in real data not being effectively distributed across TiKV nodes, defeating the purpose of pre-splitting.

**Identify the minimum and maximum values** from existing production data so that incoming writes are more likely to target different pre-allocated regions. Example query for existing data:

```sql
SELECT MIN(id), MAX(id) FROM employees;
```

- If the table is **new** and has no historical data, estimate the min/max values based on your business logic and expected data range.
- For **composite primary keys** or **composite indexes**, only the **leftmost column** needs to be considered when deciding split boundaries.
- If the leftmost column is a **string**, take string length and distribution into account to ensure even data spread.

**Pre-split and scatter regions**

A common practice is to split the number of regions to **match** the number of TiKV nodes, or to be **twice** the number of TiKV nodes. This helps ensure that data is more evenly distributed across the cluster from the start.

**Splitting regions for the primary key of all partitions**

To split regions for the primary key of all partitions in a partitioned table, you can use a command like:

```sql
SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "1970-01-01") AND (100000, "9999-12-31") REGIONS <tikv_num * 1 or 2>;
```

This example will split each partition's primary key range into `<tikv_num * 1 or 2>` regions between the specified boundary values.

**Splitting Regions for the secondary index of all partitions.**

```sql
SPLIT PARTITION TABLE employees INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <tikv_num * 1 or 2>;
```

**(Optional) When adding a new partition, you MUST manually split regions for its primary key and indices.**

```sql
ALTER TABLE employees ADD PARTITION (PARTITION p4 VALUES LESS THAN (2011));

SHOW TABLE employees PARTITION (p4) regions;

SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "2006-01-01") AND (100000, "2011-01-01") REGIONS <tikv num * 1 or 2>;

SPLIT PARTITION TABLE employees PARTITION (p4) INDEX `idx_employees2_on_store_id` BETWEEN (1) AND (1000) REGIONS <tikv num * 1 or 2>;

SHOW TABLE employees PARTITION (p4) regions;
```

**2. CLUSTERED Partitioned Table**

**Pros:**
- Queries using **Point Get** or **Table Range Scan** do **not** need additional lookups, resulting in better **read performance**.

**Cons:**
- **Manual region splitting** is required when creating new partitions, increasing operational complexity.

**Recommendation:**
- Ideal when low-latency point queries are important and operational resources are available to manage region splitting.

**Best Practices**

Create a CLUSTERED partitioned table.

```sql
CREATE TABLE employees2 (
  id INT NOT NULL,
  fname VARCHAR(30),
  lname VARCHAR(30),
  hired DATE NOT NULL DEFAULT '1970-01-01',
  separated DATE DEFAULT '9999-12-31',
  job_code INT,
  store_id INT,
  PRIMARY KEY (`id`,`hired`) CLUSTERED,
  KEY `idx_employees2_on_store_id` (`store_id`)
)
PARTITION BY RANGE ( YEAR(hired) ) (
  PARTITION p0 VALUES LESS THAN (1991),
  PARTITION p1 VALUES LESS THAN (1996),
  PARTITION p2 VALUES LESS THAN (2001),
  PARTITION p3 VALUES LESS THAN (2006)
);
```

Adding the [merge_option=deny](https://docs.pingcap.com/tidb/stable/table-attributes/#control-the-region-merge-behavior-using-table-attributes) attribute to a table or partition can prevent the merging of empty regions. However, when a partition is dropped, the regions belonging to that partition will still be merged automatically.

```sql
ALTER TABLE employees2 ATTRIBUTES 'merge_option=deny';
```

**Determining split boundaries based on existing business data**

To avoid hotspots when a new table or partition is created, it is often beneficial to **pre-split** regions before heavy writes begin. To make pre-splitting effective, configure the **lower and upper boundaries** for region splitting based on the **actual business data distribution**. Avoid setting excessively wide boundaries, as this can result in real data not being effectively distributed across TiKV nodes, defeating the purpose of pre-splitting.

**Identify the minimum and maximum values** from existing production data so that incoming writes are more likely to target different pre-allocated regions. Example query for existing data:

```sql
SELECT MIN(id), MAX(id) FROM employees2;
```

- If the table is **new** and has no historical data, estimate the min/max values based on your business logic and expected data range.
- For **composite primary keys** or **composite indexes**, only the **leftmost column** needs to be considered when deciding split boundaries.
- If the leftmost column is a **string**, take string length and distribution into account to ensure even data spread.

**Pre-split and scatter regions**

A common practice is to split the number of regions to **match** the number of TiKV nodes, or to be **twice** the number of TiKV nodes. This helps ensure that data is more evenly distributed across the cluster from the start.

**Splitting regions for all partitions**

```sql
SPLIT PARTITION TABLE employees2 BETWEEN (1,"1970-01-01") AND (100000,"9999-12-31") REGIONS <tikv_num * 1 or 2>;
```

**Splitting regions for the secondary index of all partitions.**

```sql
SPLIT PARTITION TABLE employees2 INDEX `idx_employees2_on_store_id` BETWEEN (1) AND (1000) REGIONS <tikv_num * 1 or 2>;
```

**(Optional) When adding a new partition, you MUST manually split regions for the specific partition and its indices.**

```sql
ALTER TABLE employees2 ADD PARTITION (PARTITION p4 VALUES LESS THAN (2011));

show table employees2 PARTITION (p4) regions;

SPLIT PARTITION TABLE employees2 PARTITION (p4) BETWEEN (1,"2006-01-01") AND (100000,"2011-01-01") REGIONS <tikv_num * 1 or 2>;

SPLIT PARTITION TABLE employees2 PARTITION (p4) INDEX `idx_employees2_on_store_id` BETWEEN (1) AND (1000) REGIONS <tikv_num * 1 or 2>;

show table employees2 PARTITION (p4) regions;
```

**3. CLUSTERED Non-partitioned Table**

**Pros:**
- **No hotspot risk from new partitions**.
- Provides **good read performance** for point and range queries.

**Cons:**
- **Cannot use DROP PARTITION** to clean up large volumes of old data.

**Recommendation:**
- Best suited for use cases that require stable performance and do not benefit from partition-based data management.

### Summary Table

| Approach | Read Hotspot Risk | Write Hotspot Risk | Operational Complexity | Query Performance | Data Cleanup |
|---|---|---|---|---|---|
| NONCLUSTERED Partitioned | Low (with merge_option=deny) | Low (auto pre-split) | Low | Moderate (extra lookups) | Fast (DROP PARTITION) |
| CLUSTERED Partitioned | Medium (manual intervention) | Medium (manual split) | High | High (direct access) | Fast (DROP PARTITION) |
| CLUSTERED Non-partitioned | None | Medium (single table) | Low | High | Slow (DELETE/TTL) |

## Converting Between Partitioned and Non-Partitioned Tables

When working with large tables (e.g., 120 million rows), transforming between partitioned and non-partitioned schemas is sometimes required for performance tuning or schema design changes. TiDB supports several main approaches for such transformations:

1. Batch DML: `INSERT INTO ... SELECT ...`
2. Pipeline DML: `INSERT INTO ... SELECT ...`
3. `IMPORT INTO`: `IMPORT INTO ... FROM SELECT ...`
4. Online DDL: Direct schema transformation via `ALTER TABLE`

This section compares the efficiency and implications of these methods in both directions of conversion, and provides best practice recommendations.

### Method 1: Batch DML INSERT INTO ... SELECT ...

**By Default**

```sql
SET tidb_mem_quota_query = 0;
INSERT INTO fa_new SELECT * FROM fa;
-- 120 million rows copied in 1h 52m 47s
```

### Method 2: Pipeline DML INSERT INTO ... SELECT ...

```sql
SET tidb_dml_type = "bulk";
SET tidb_mem_quota_query = 0;
SET tidb_enable_mutation_checker = OFF;
INSERT INTO fa_new SELECT * FROM fa;
-- 120 million rows copied in 58m 42s
```

### Method 3: IMPORT INTO ... FROM SELECT ...

```sql
mysql> import into fa_new from select * from fa with thread=32,disable_precheck;
Query OK, 120000000 rows affected, 1 warning (16 min 49.90 sec)
Records: 120000000, ID: c1d04eec-fb49-49bb-af92-bf3d6e2d3d87
```

### Method 4: Online DDL

**From partition table to non-partitioned table**

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;

mysql> alter table fa REMOVE PARTITIONING;
-- real 170m12.024s (≈ 2h 50m)
```

**From non-partition table to partitioned table**

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
ALTER TABLE fa PARTITION BY RANGE (`yearweek`)
(PARTITION `fa_2024001` VALUES LESS THAN (2024001),
PARTITION `fa_2024002` VALUES LESS THAN (2024002),
...
PARTITION `fa_2024365` VALUES LESS THAN (2024365),
PARTITION `fa_2024366` VALUES LESS THAN (2024366));

Query OK, 0 rows affected, 1 warning (2 hours 31 min 57.05 sec)
```

### Findings

| Method | Time Taken |
|---|---|
| Method 1: Batch DML INSERT INTO ... SELECT | 1h 52m 47s |
| Method 2: Pipeline DML: INSERT INTO ... SELECT ... | 58m 42s |
| Method 3: IMPORT INTO ... FROM SELECT ... | 16m 59s |
| Method 4: Online DDL (From partition table to non-partitioned table) | 2h 50m |
| Method 4: Online DDL (From non-partition table to partitioned table) | 2h 31m |

### Recommendation

TiDB offers two approaches for converting tables between partitioned and non-partitioned states:

- Choose an offline method like `IMPORT INTO` when your system can accommodate a maintenance window, as it delivers much better performance. Use online DDL only when zero downtime is a strict requirement.