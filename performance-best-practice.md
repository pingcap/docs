---
title: Optimizing TiDB: Key Settings for Maximum Performance
summary: Learn how to optimize TiDB performance by configuring key settings and addressing edge cases
---

# Optimizing TiDB: Key Settings for Maximum Performance

This guide provides essential information on optimizing TiDB for peak performance. We'll explore:
- Performance best practices for common workloads
- Strategies for addressing challenging performance scenarios

> **Important Note:**
>
> These optimization techniques are particularly valuable when pursuing extreme performance in TiDB. However, it's important to note that performance tuning often involves trade-offs between multiple factors, and there is no single "silver bullet" solution. Some of the techniques described here may use experimental features, which are specifically called out. While these optimizations can yield significant performance gains, they may not be suitable for stable production environments and should be used with caution.


# Why This Matters

Optimizing TiDB for peak performance requires careful tuning of various settings. In many cases, achieving optimal performance involves adjusting configurations beyond their default values.

While default settings are chosen for stability, maximizing performance often requires more aggressive configurations and sometimes the use of experimental features. This approach is based on insights gained from numerous real-world deployments and performance optimization efforts.

This guide explains these non-default settings, detailing their benefits and potential trade-offs. It's designed to help you make informed decisions when fine-tuning TiDB for your specific workload requirements.

# Key Settings for Common Workloads

The following suggested settings cover the most common optimizations for improving TiDB performance:

- Enhancing query plan caching
- Optimizing the query optimizer's behavior
- More aggressive use of TiKV's Titan storage engine

These settings can significantly boost performance for many common workloads, but as with any optimization, it's important to test thoroughly in your specific environment.

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

[pessimistic-txn]
in-memory-peer-size-limit = "32MiB"
in-memory-instance-size-limit = "512MiB"

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
| concurrent-send-snap-limit concurrent-recv-snap-limit snap-io-max-bytes-per-sec | Increase the bandwidth to speed up tikv scale in/out operations, improve snapshot speed, scale-in/out is frequent operation during performance tuning | more impact on online traffic during scale operation | 
| in-memory-peer-size-limit in-memory-instance-size-limit | Increases the memory limit for caching pessimistic locks in memory, which improves transaction performance by avoiding lock information being written to disk | Higher memory usage since lock information is cached in memory rather than written to disk. Monitor memory usage carefully when increasing these limits | 
| rocksdb.titan rocksdb.defaultcf.titan | RocksDB might exhibit high write amplification, and the disk throughput might become the bottleneck for the workload. As a result, the total number of pending compaction bytes grows over time and triggers flow control, which indicates that TiKV lacks sufficient disk bandwidth to keep up with the foreground write flow.  To alleviate the bottleneck caused by limited disk throughput, you can improve performance by enabling Titan. | When Titan is enabled, there might be a slight performance degradation for range scans on the primary key, and the space amplification is higher than RocksDB, at worse case, the space usage is 2x of the original data. For more information, see Impact of min-blob-size on performance. | 
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

# Benchmark 

## YCSB workloads on Large record value

### Environment
Environment: Cluster specification: 3 tidb (16c64g) + 3 tikv (16c64g)
TiDB Version: v8.4.0
Workload : [go-ycsb workloada](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

### Throughput Comparison between Baseline and Key Settings
Below result show the throughput improvement of Key Settings comparing to the baseline as OPS(operation per second).

Baseline: the default settings
Key Settings: the settings of variables and configurations in this guide

| Item | Baseline(OPS) | Key Settings(OPS) | diff(%) |
| ---------| ---- | ----| ----|
| load data| 2858.5 | 5074.3 | 77.59% |
| workloada | 2243.0 | 12804.3 | 470.86% |

### Performance Analysis

Titan is enabled by default since v7.6.0 and the default min-blob-size of Titan in TiDB v8.4.0 is 32KB. For the baseline configuration, we use a record size of 31KB to ensure data is stored in RocksDB. In contrast, for the key settings configuration, we set min-blob-size to 1KB, causing data to be stored in Titan.

The performance improvement observed in the Key Settings can be primarily attributed to Titan's ability to reduce RocksDB compactions. As shown in the figures below:

- Baseline: The total throughput of RocksDB compaction exceeds 1GB/s, with peaks over 3GB/s.
- Key Settings: The peak throughput of RocksDB compaction remains below 100MB/s.

This significant reduction in compaction overhead contributes to the overall throughput improvement seen in the Key Settings configuration.
![titan-rocksdb-compactions](/media/key-settings/titan-rocksdb-compactions.png)


### Workload Commands
load data
```
go-ycsb load mysql -P /ycsb/workloads/workloada -p mysql.host=benchbot-gcp-ycsb-tps-7525162-1-147--tiup -p mysql.port=3390 -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```
run workload
```
go-ycsb run mysql -P /ycsb/workloads/workloada -p mysql.host=benchbot-gcp-ycsb-tps-7525162-1-147--tiup -p mysql.port=3390 -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```


# Edge Cases and Specific Optimizations

While the general configurations provided earlier offer a good starting point for performance tuning, certain scenarios require more targeted optimizations. This section covers specific cases that may need individual attention and fine-tuning.

## Identifying Edge Cases

1. Analyze query patterns and workload characteristics
2. Monitor system metrics and performance bottlenecks
3. Gather feedback from application teams on specific pain points

## Common Edge Cases and Solutions

Here are the common edge cases and solutions:

1. High TSO wait for High-frequency small queries
2. Choose the proper mak chunk size for different workloads
3. Tune coprocessor cache for read-heavy workloads
4. Choose proper tidb_txn_mode and tidb_dml_type for different workloads
5. Optimize Group By and Distinct Operations with TiKV Pushdown
6. Mitigate Too many MVCC versions by in-memory engine
7. Disable auto analyze job during batch processing

Each of these cases may require adjustments to different parameters or usage of specific features in TiDB. The following sections provide more details on how to address these scenarios.

Remember that these optimizations should be applied cautiously and with thorough testing, as their effectiveness can vary depending on your specific use case and data patterns.

## High TSO wait for High-frequency small queries
### How to Troubleshooting
When TSO (Timestamp Oracle) waiting time takes up a large percentage of total SQL execution time, it indicates a potential performance bottleneck. This can happen with high-frequency small queries that require frequent TSO requests. It can be Identified by [SQL Execute Time Overview](https://docs.pingcap.com/tidb/stable/performance-tuning-methods#tune-by-color) in the grafana dashboard [performance overview](https://docs.pingcap.com/tidb/stable/grafana-performance-overview-dashboard).

### Solution 1 `tidb_low_resolution_tso`
If the TSO (Timestamp Oracle) wait contributes significantly to the execution plan time, and if the application can tolerate stale reads, you can use the `tidb_low_resolution_tso` setting in TiDB to avoid the TSO wait time and improve query latency. Here's how to enable it:

```SQL
set global tidb_low_resolution_tso=on;
```

### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| tidb_low_resolution_tso| Enables stale reads to avoid TSO wait time, improving query latency | Only suitable for applications that can tolerate reading stale data. Not recommended for scenarios requiring strict data consistency | 

### Solution 2 `tidb_tso_client_rpc_mode`
The default value of `tidb_tso_client_rpc_mode` is `DEFAULT`. When the following conditions are met, you can consider switching `tidb_tso_client_rpc_mode` to `PARALLEL` or `PARALLEL-FAST` for potential performance improvements:

- TSO waiting time constitutes a significant portion of the total execution time of SQL queries.
- The TSO allocation in PD has not reached its bottleneck.
- PD and TiDB nodes have sufficient CPU resources.
- The network latency between TiDB and PD is significantly higher than the time PD takes to allocate TSO (that is, network latency accounts for the majority of TSO RPC duration).
  - To get the duration of TSO RPC requests, check the PD TSO RPC Duration panel in the PD Client section of the Grafana TiDB dashboard.
  - To get the duration of PD TSO allocation, check the PD server TSO handle duration panel in the TiDB section of the Grafana PD dashboard.
- The additional network traffic resulting from more TSO RPC requests between TiDB and PD (twice for PARALLEL or four times for PARALLEL-FAST) is acceptable.

```SQL
set global tidb_tso_client_rpc_mode=PARALLEL;
```

## Tune coprocessor cache for read-heavy workloads

If the workload is read-heavy, you can increase the coprocessor cache size, lower the cache threshold, to coprocess cache hit ratio. Here is the detail document to check the hit ratiofor [coprocessor cache](https://docs.pingcap.com/tidb/stable/coprocessor-cache).

Here are the recommended settings to increase the coprocessor cache size to 4GB and drease the coprocessor cache admission min process time to 0ms:

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

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