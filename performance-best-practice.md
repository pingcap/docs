---
title: TiDB Performance Tips
summary: Learn how to make TiDB run faster by adjusting settings and handling edege cases

---

# TiDB Performance Tips

This guide shows you how to make TiDB run as fast as possible. We'll cover:
- How to set up TiDB's settings
- Best practices for common workloads
- Ways to handle tricky performance issues

These tips are great for when you're first trying out TiDB (what we call a Proof of Concept or PoC).

> **Important Note:**
>
> To get the best speed in a PoC, we'll use some settings and features that aren't the default. These aren't meant for stable production use.

# Why This Matters

Making TiDB run its best takes a lot of tweaking. In fact, more than half the time spent on PoCs is usually about improving performance.

When testing TiDB, we usually try to stick to the default settings for stability. But to get really good performance, we often need to change some settings and use experimental features.

To make PoCs faster and easier, we've put together some "out of the box" settings. These are more aggressive than our defaults, based on what we've learned from many PoCs and real-world systems. This guide explains these non-default settings and their pros and cons.

# General Tips

These suggested settings are safe to use when setting up a PoC cluster. They cover the most common tweaks needed during a PoC, including:
- Caching query plans
- Adjusting how TiDB figures out the best way to run queries
- Using TiKV's Titan storage engine more aggressively

## system variables

```SQL 
set global tidb_enable_instance_plan_cache=on;
set global tidb_instance_plan_cache_max_size=2GiB;
set global tidb_enable_non_prepared_plan_cache=on;
set global tidb_ignore_prepared_cache_close_stmt=on;
set global tidb_enable_inl_join_inner_multi_pattern=on;
set global tidb_opt_derive_topn=on;
set global tidb_runtime_filter_mode=LOCAL;
set global tidb_opt_enable_mpp_shared_cte_execution=on;
set global tidb_rc_read_check_ts=on;
set global tidb_guarantee_linearizability=off;
set global pd_enable_follower_handle_region=on;
set global tidb_opt_fix_control = '44262:ON,44389:ON,44823:10000,44830:ON,44855:ON,52869:ON';
```

### Justifications

| variables| Pro | Cons | 
| ---------| ---- | ----|
| tidb_enable_instance_plan_cache tidb_instance_plan_cache_max_size| Instance Plan Cache is to replace the old session-level plan cache. The instance plan cache allows effective use of the plan cache in scenarios with many prepared statements or many connections | The feature is experimental | 
| tidb_enable_non_prepared_plan_cache| Turn on none prepared plan cache for application not using prepared statement to reduce the compile cost | - | 
| tidb_ignore_prepared_cache_close_stmt| Cache plan for application using prepared statements but close the plan after every single execution| - | 
| tidb_enable_inl_join_inner_multi_pattern| Index Join is supported when the inner table has Selection or Projection operators on it | - | 
| tidb_opt_derive_topn| enable the optimization rule of Deriving TopN or Limit from window functions | Only limited to ROW_NUMBER() window function | 
| tidb_runtime_filter_mode| By default enabling runtime filter | The variable is added to v7.2.0, and for safety, it's disabled by default | 
| tidb_opt_enable_mpp_shared_cte_execution| the non-recursive Common Table Expressions (CTE) can be executed on TiFlash MPP | The feature is experimental  | 
| tidb_rc_read_check_ts| for read-committed isolation level, Enabling this variable can avoid the latency and cost of getting the global timestamp, and can optimize the transaction-level read latency. | This feature is incompatible with replica-read. | 
| tidb_guarantee_linearizability| the process of fetching TS for commit TS from the PD server is skipped | with the cost that only causal consistency is guaranteed but not linearizability.  | 
| pd_enable_follower_handle_region| enable the Active PD Follower feature, TiDB evenly distributes requests for Region information to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader| The feature is experimental | 

#### fix control explanation
Use aggressive optimizer controls to enable more possible optimizations.

- 44262:ON: Allow the use of Dynamic pruning mode to access the partitioned table when the GlobalStats are missing.
- 44389:ON: For filters such as c = 10 and (a = 'xx' or (a = 'kk' and b = 1)), this variable enable to try to build more comprehensive scan ranges for IndexRangeScan.
- 44823:10000: To save memory, Plan Cache does not cache queries with parameters exceeding the specified number of this variable. Increased from from 200 to 10000 to make plan cache availabe for query with long in-list;
- 44830:ON: Plan Cache is allowed to cache execution plans with the PointGet operator generated during physical optimization.
- 44855:ON: Enable IndexJoin when the Probe side of an IndexJoin operator contains a Selection operator.
- 52869:ON: Enable indexmerge if the optimizer can choose the single index scan method (other than full table scan) for a query plan

## TiDB Configurations

```toml
[performance]
concurrently-init-stats: true
force-init-stats: true
lite-init-stats: false

[tikv-client]
region-cache-ttl = 1200
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| concurrently-init-stats force-init-stats lite-init-stats| make sure the statistics is full loaded and ready during TiDB startup | need to wait more time during TiDB startup and more memory usage | 
| region-cache-ttl| Increase from 10m to 20m, to reduce the GetRegion request to pd server | Higher possibility for leaders/region miss backoff if the data are changed and moved frequently | 

## TiKV Configurations

```toml
[server]
concurrent-send-snap-limit = 64
concurrent-recv-snap-limit = 64
snap-io-max-bytes-per-sec = "400MB"

[rocksdb.titan]
enabled = true
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
blob-file-compression = "zstd"

[storage.flow-control]
l0-files-threshold = 60
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| concurrent-send-snap-limit concurrent-recv-snap-limit snap-io-max-bytes-per-sec | Increase the bandwidth to speed up tikv scale in/out operations, improve snapshot speed, scale-in/out is frequent operation during PoC| more impact on online traffic during scale operation | 
| rocksdb.titan rocksdb.defaultcf.titan | RocksDB might exhibit high write amplification, and the disk throughput might become the bottleneck for the workload. As a result, the total number of pending compaction bytes grows over time and triggers flow control, which indicates that TiKV lacks sufficient disk bandwidth to keep up with the foreground write flow.  To alleviate the bottleneck caused by limited disk throughput, you can improve performance by enabling Titan. | When Titan is enabled, there might be a slight performance degradation for range scans on the primary key. For more information, see Impact of min-blob-size on performance. | 
| l0-files-threshold | increase the thrshhold to avoid unneccessary flow control | - | 

## TiFlash Congiurations

```toml
[raftstore-proxy.server]
snap-io-max-write-bytes-per-sec = "300MiB"
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| snap-io-max-write-bytes-per-sec | Increase the bandwidth to speed up data replication to TiFlash Nodes | more impact on online traffic during scale operation | 



# Edge Cases and Specific Optimizations

While the general configurations provided earlier offer a good starting point for performance tuning, certain scenarios require more targeted optimizations. This section covers specific cases that may need individual attention and fine-tuning.

## Identifying Edge Cases

1. Analyze query patterns and workload characteristics
2. Monitor system metrics and performance bottlenecks
3. Gather feedback from application teams on specific pain points

## Common Edge Cases and Solutions

1. High TSO wait for High-frequency small queries
2. Choose the proper mak chunk size for different workloads
3. Choose proper tidb_txn_mode and tidb_dml_type for different workloads
4. Optimize Group By and Distinct Operations with TiKV Pushdown
5. Mitigate Too many MVCC versions by in-memory engine
6. Disable auto analyze job during batch processing

Each of these cases may require adjustments to different parameters or usage of specific features in TiDB. The following sections provide more details on how to address these scenarios.

Remember that these optimizations should be applied cautiously and with thorough testing, as their effectiveness can vary depending on your specific use case and data patterns.

## High TSO wait for High-frequency small queries
If the TSO (Timestamp Oracle) wait contributes significantly to the execution plan time, and if the application can tolerate stale reads, you can use the `tidb_low_resolution_tso` setting in TiDB to avoid the TSO wait time and improve query latency. Here's how to enable it:

```SQL
set global tidb_low_resolution_tso=on;
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| tidb_low_resolution_tso| Enable stale read to avoid tso wait to improve the query latency | Application can accept stale read | 

### How to Troubleshooting
Identified by [SQL Execute Time Overview](https://docs.pingcap.com/tidb/stable/performance-tuning-methods#tune-by-color) in the grafana dashboard [performance overview](https://docs.pingcap.com/tidb/stable/grafana-performance-overview-dashboard).

## Choose the proper mak chunk size for different workloads
The tidb_max_chunk_size parameter in TiDB controls the maximum number of rows that can be processed in a single chunk during query execution. Adjusting this parameter based on the workload type can optimize performance:

- For pure OLTP workloads: Lower the default value (e.g., from 1024 to 128) to reduce memory allocation overhead and make limit pushdown more efficient.

- For analytical workloads: Increase the default value to improve processing efficiency for large result sets.

It's important to test different values and monitor performance, as the optimal setting depends on your specific workload characteristics.

```SQL
set global tidb_max_chunk_size=128;
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| tidb_max_chunk_size | Reduce from default 1024 to 128, reduce the memory allocation overhead, make the limit pushdown more efficient | For the analytical workloads on TiKV, By adjusting tidb_max_chunk_size from 1024 to 128, the performance degradation is between 3.3% and 10.9% | 

## Choose proper tidb_txn_mode and tidb_dml_type for different workloads

Here is the guideline how to choose txn mode and dml type

### Justifications

| Type | Variable | Use case | 
| ---------| ---- | ----|
| Pipeline DML | session tidb_dml_type="bulk";  | "bulk" indicates the bulk DML execution mode, which is suitable for scenarios where a large amount of data is written, causing excessive memory usage in TiDB. 1) "bulk" mode is only suitable for scenarios where a large amount of data is written without conflicts. 2) "bulk" mode only takes effect on statements with auto-commit enabled, and requires the pessimistic-auto-commit configuration item to be set to false. | 
| Optimistic mode | Set session tidb_txn_mode="optimistic"; | - begin .. insert..insert..insert...end; - No or a few write conflict - Use optimistic mode | 
| pessimistic mode (by default) | Set session tidb_txn_mode="pessimistic"; | Use pessimistic and  standard for other cases | 

## Optimize Group By and Distinct Operations with TiKV Pushdown

Group by and distinct pushdown can significantly improve query performance by offloading aggregation operations to TiKV, reducing data transfer and processing load on TiDB. However, the effectiveness of this optimization depends on the data characteristics:

- Beneficial for: Columns with low number of distinct values (NDV) and high cardinality (many repeated values)
- May not improve or could slow down: Columns with high NDV and low cardinality (mostly unique values)

To enable these optimizations:

```SQL
set global tidb_opt_agg_push_down=on;
set global tidb_opt_distinct_agg_push_down=on;
```


| variables | Pro | Cons | 
| ---------| ---- | ----|
| tidb_opt_agg_push_down tidb_opt_distinct_agg_push_down| Low NDV (right scenario) | High NDV (bad scenario) | 



## Too many MVCC versions
If too many MVCC versions are observed during the PoC, either due to hot read/write spots or issues with garbage collection and compaction, you can mitigate this problem by enabling the in-memory engine. This feature is available as a hotfix. To enable the in-memory engine in TiKV by adding the following configuration to your TiKV configuration file. 

> **Note:**
>
> The in-memory engine can help reduce the impact of excessive MVCC versions, but it may increase memory usage. Monitor your system closely after enabling this feature.

   ```toml
   [in-memory-engine]
   enabled = true
   gc-interval = "2m"
   hard-limit-threshold = "8GB"
   soft-limit-threshold = "7GB"
   stop-limit-threshold = "5GB"
   mvcc-amplification = 100
   load-evict-interval = "4m"
   ```

### How to Troubleshoot Too Many MVCC Versions

There are two common ways to identify if the system is suffering from too many MVCC versions:

1. From the [execution plan](https://docs.pingcap.com/tidb/stable/identify-slow-queries#fields-description):
   In the TiKV Coprocessor Task fields of the execution plan, compare `Total_keys` and `Process_keys`:
   - `Total_keys`: The number of keys that Coprocessor has scanned.
   - `Process_keys`: The number of keys that Coprocessor has processed.
   A significant difference between `Process_keys` and `Total_keys` indicates the presence of many old versions, as `Process_keys` does not include the old versions of MVCC.

2. From Grafana Metrics [coprocessor-detail](https://docs.pingcap.com/tidb/stable/grafana-tikv-dashboard#coprocessor-detail):
   In the "Total Ops Details (Table Scan)" and "Total Ops Details (Index Scan)" panels, a large difference between `next + prev` and `processed_keys` indicates the existence of many old versions.

Other common symptoms associated with too many MVCC versions include:
1. High TiKV CPU usage on the unified thread pool
2. High number of running tasks on the unified thread pool

To mitigate these issues, consider enabling the in-memory engine as described in the previous section, and monitor your system closely after making any changes.



## Disable Auto Analyze During Batch Processing

During batch processing operations, it's recommended to disable automatic statistics collection and manually gather statistics when needed. This prevents frequent analyze jobs from consuming excessive resources during critical batch operations.

To disable auto analyze:
```SQL
set global tidb_enable_auto_analyze = off;
```