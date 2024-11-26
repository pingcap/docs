---
title: Configure TiDB for Optimal Performance
summary: Learn how to optimize TiDB performance by configuring key settings and addressing edge cases.
---

## Configure TiDB for Optimal Performance

This guide provides essential information on optimizing TiDB for maximum performance. We'll explore:
- Performance best practices for common workloads
- Strategies for addressing challenging performance scenarios

> **Note:**
>
> These optimization techniques are particularly valuable when pursuing extreme performance in TiDB. However, it's important to note that performance tuning often involves trade-offs between multiple factors, and there is no single "silver bullet" solution. Some of the techniques described here may use experimental features, which are specifically called out. While these optimizations can yield significant performance gains, they may not be suitable for stable production environments and should be used with caution.

## Why This Matters

Optimizing TiDB for peak performance requires careful tuning of various settings. In many cases, achieving optimal performance involves adjusting configurations beyond their default values.

While default settings are chosen for stability, maximizing performance often requires more aggressive configurations and sometimes the use of experimental features. This approach is based on insights gained from numerous real-world deployments and performance optimization efforts.

This guide explains these non-default settings, detailing their benefits and potential trade-offs. It's designed to help you make informed decisions when fine-tuning TiDB for your specific workload requirements.

## Key Settings for Common Workloads

The following suggested settings cover the most common optimizations for improving TiDB performance:

- Enhancing query plan caching
- Optimizing the query optimizer's behavior
- More aggressive use of TiKV's Titan storage engine

These settings can significantly boost performance for many common workloads, but as with any optimization, it's essential to test thoroughly in your specific environment.

### System variables

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

#### Justifications

| variables| Pro | Cons | 
| ---------| ---- | ----|
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840) [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-new-in-v840)| Introduces instance-level plan caching to replace session-level caching, significantly improving performance for workloads with high connection counts or frequent prepared statement usage | As an experimental feature, carefully evaluate in non-production environments first. Monitor memory usage as plan cache size increases |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)| Turns on none prepared plan cache for applications not using prepared statement to reduce the compile cost | - | 
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)| Caches plan for applications using prepared statements but close the plan after every single execution | - | 
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700)| Index Join is supported when the inner table has Selection or Projection operators on it | - | 
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700)| Enables the optimization rule of Deriving TopN or Limit from window functions | Only limited to ROW_NUMBER() window function | 
| [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)| Enables runtime filter to improve the hash join efficiency | The variable is added to v7.2.0, and for safety, it's disabled by default | 
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)| Enables non-recursive Common Table Expressions (CTE) pushdown to TiFlash | The feature is experimental  | 
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)| For read-committed isolation level, Enables this variable can avoid the latency and cost of getting the global timestamp, and can optimize the transaction-level read latency. | This feature is incompatible with repeatable-read | 
| [`tidb_guarantee_linearizability`](/system-variables.md#tidb_guarantee_linearizability-new-in-v50)| Improves performance by skipping the commit timestamp fetch from PD server | Trades linearizability for performance - only causal consistency is guaranteed. Not suitable for scenarios requiring strict linearizability |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)| Activates the PD Follower feature, allowing PD followers to process Region requests, which helps distribute load evenly across all PD servers and reduces CPU pressure on the PD leader | This feature is experimental and should be tested in non-production environments |
| [`tidb_opt_fix_control`](/optimizer-fix-controls.md#tidb_opt_fix_control) | Enables advanced query optimization strategies to improve performance through additional optimization rules and heuristics | Test thoroughly in your environment as benefits vary by workload |

#### fix control explanation

Use aggressive optimizer controls to enable more possible optimizations.

- [`44262`](/optimizer-fix-controls.md#44262-new-in-v653-and-v720):ON: Allow the use of Dynamic pruning mode to access the partitioned table when the GlobalStats are missing.
- [`44389`](/optimizer-fix-controls.md#44389-new-in-v653-and-v720):ON: For filters such as c = 10 and (a = 'xx' or (a = 'kk' and b = 1)), this variable enable to try to build more comprehensive scan ranges for IndexRangeScan.
- [`44823`](/optimizer-fix-controls.md#44823-new-in-v730):10000: To save memory, Plan Cache does not cache queries with parameters exceeding the specified number of this variable. Increased from from 200 to 10000 to make plan cache availabe for query with long in-list;
- [`44830`](/optimizer-fix-controls.md#44830-new-in-v730):ON: Plan Cache is allowed to cache execution plans with the PointGet operator generated during physical optimization.
- [`44855`](/optimizer-fix-controls.md#44855-new-in-v730):ON: Enable IndexJoin when the Probe side of an IndexJoin operator contains a Selection operator.
- [`52869`](/optimizer-fix-controls.md#52869-new-in-v810):ON: Enable indexmerge if the optimizer can choose the single index scan method (other than full table scan) for a query plan

### TiDB Configurations

```toml
[performance]
concurrently-init-stats = true
force-init-stats = true
lite-init-stats = false
```
#### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| [`concurrently-init-stats`](/tidb-configuration-file.md#concurrently-init-stats-new-in-v810-and-v752) [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) | Ensures comprehensive and concurrent loading of table statistics during TiDB startup, improving query optimization readiness | Potentialy increases startup time and memory consumption |

### TiKV Configurations

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

#### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| [`concurrent-send-snap-limit`](/tikv-configuration-file.md#concurrent-send-snap-limit) [`concurrent-recv-snap-limit`](/tikv-configuration-file.md#concurrent-recv-snap-limit) [`snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec) | Configures concurrent snapshot transfer limits and I/O bandwidth for TiKV scaling operations. Higher limits reduce scaling time by allowing faster data migration | Consider the trade-off between scaling speed and online transaction performance when adjusting these limits |
| [`in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840) [`in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) | Controls the memory allocation for pessimistic lock caching at peer and instance levels. Keeping locks in memory reduces disk I/O and improves transaction performance | Requires careful memory monitoring and tuning. Higher limits increase memory usage but reduce disk writes for lock information |
| [`rocksdb.titan`](/tikv-configuration-file.md#rocksdbtitan) [`rocksdb.defaultcf.titan`](/tikv-configuration-file.md#rocksdbdefaultcftitan) [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Enables Titan storage engine to reduce write amplification and alleviate disk I/O bottlenecks. Particularly effective when RocksDB compaction cannot keep up with write workload, leading to accumulated pending compaction bytes | Trade-offs include: 1) Potential performance impact on primary key range scans 2) Increased space amplification (up to 2x in worst case) 3) Additional memory usage for blob cache. Consider enabling when write amplification is the primary bottleneck |
| [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold) | Controls when write flow control is triggered based on L0 file count. Increasing the threshold reduces write stalls during high write workloads | Higher thresholds may lead to more aggressive compactions when there are many L0 files |

### TiFlash configurations

```toml
[raftstore-proxy.server]
snap-io-max-write-bytes-per-sec = "300MiB"
```

#### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| `snap-io-max-write-bytes-per-sec` | Controls maximum write bandwidth for TiKV to TiFlash data replication. Higher limits accelerate initial data loading and catch-up replication | Higher bandwidth consumption may impact online transaction performance. Balance between replication speed and system stability |

## Benchmark 

### Sysbench workloads on 1000 tables

#### Environment

Environment: Cluster specification: 3 tidb (16c64g) + 3 tikv (16c64g)

TiDB Version: v8.4.0

Workload : [sysbench oltp_read_only](https://github.com/akopytov/sysbench/blob/master/src/lua/oltp_read_only.lua)

#### Performance Comparison

The following results illustrate the throughput enhancements achieved with the Key Settings in comparison to the baseline, measured in operations per second (OPS), latency, and plan cache hit ratio.

Baseline: the default settings
Key Settings: the settings of variables and configurations in this guide

| Item | Baseline | Key Settings | Diff(%) |
| ---------| ---- | ----| ----|
| QPS | 89,100 | 100,128 | 12.38% |
| Avg Latency（ms）|35.87 | 31.92 | -11.01% |
| P95 Latency（ms）| 58.92 | 51.02 | -13.41% |
| Plan Cache Hit Ratio (%) | 56.89% | 87.51% | 53.82% |
| Plan cache Memory Usage (MiB) | 95.3 | 70.2 | -26.34% |

#### Key Benefits

The instance plan cache demonstrates significant performance improvements over the baseline configuration:

- Higher Hit Ratio: Increased from 56.89% to 87.51% (+53.82%)
- Lower Memory Usage: Reduced from 95.3 MiB to 70.2 MiB (-26.3%)
- Better Performance:
    - QPS increased by 12.38%
    - Average latency reduced by 11.01%
    - P95 latency reduced by 13.41%
#### How It Works

- Caches execution plans for SELECT statements in memory
- Shares cached plans across all connections (up to 200) on the same TiDB instance
- Can effectively store plans for up to 5,000 SELECT statements across 1,000 tables
- Cache misses primarily occur only for BEGIN and COMMIT statements

#### Real-World Impact

While our benchmark using simple sysbench oltp_read_only queries (14KB per plan) showed modest improvements, real-world applications often see much more dramatic benefits:

- Up to 20x latency improvement for complex queries
- Significantly better memory efficiency compared to session-level plan cache

Instance plan cache is particularly effective when your system has:

- Large tables with many columns
- Complex SQL queries
- High concurrent connections
- Diverse query patterns

#### Memory Efficiency

Instance plan cache provides better memory efficiency than session-level plan cache because:

- Plans are shared across all connections
- No need to duplicate plans for each session
- More efficient memory utilization while maintaining higher hit ratios

In scenarios with multiple connections and complex queries, session-level plan cache would require significantly more memory to achieve similar hit ratios, making instance plan cache the more efficient choice.

![instance-plan-cache](/media/key-settings/instance-plan-cache.png)

#### Workload Commands
Load data
```
sysbench oltp_read_only prepare --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=100 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

Run workload
```
sysbench oltp_read_only run --mysql-host={host} --mysql-port={port} --mysql-user=root --db-driver=mysql --mysql-db=test --threads=200 --time=900 --report-interval=10 --tables=1000 --table-size=10000
```

### YCSB workloads on Large record value

#### Environment

Environment: Cluster specification: 3 tidb (16c64g) + 3 tikv (16c64g)
TiDB Version: v8.4.0
Workload : [go-ycsb workloada](https://github.com/pingcap/go-ycsb/blob/master/workloads/workloada)

#### Performance Comparison

Below result show the throughput improvement of Key Settings comparing to the baseline as OPS(operation per second).

Baseline: the default settings
Key Settings: the settings of variables and configurations in this guide

| Item | Baseline(OPS) | Key Settings(OPS) | Diff(%) |
| ---------| ---- | ----| ----|
| load data| 2858.5 | 5074.3 | 77.59% |
| workloada | 2243.0 | 12804.3 | 470.86% |

#### Performance Analysis

Titan is enabled by default since v7.6.0 and the default min-blob-size of Titan in TiDB v8.4.0 is 32KB. For the baseline configuration, we use a record size of 31KB to ensure data is stored in RocksDB. In contrast, for the key settings configuration, we set min-blob-size to 1KB, causing data to be stored in Titan.

The performance improvement observed in the Key Settings is primarily attributed to Titan's ability to reduce RocksDB compactions. As shown in the figures below:

- Baseline: The total throughput of RocksDB compaction exceeds 1GB/s, with peaks over 3GB/s.
- Key Settings: The peak throughput of RocksDB compaction remains below 100MB/s.

This significant reduction in compaction overhead contributes to the overall throughput improvement seen in the Key Settings configuration.
![titan-rocksdb-compactions](/media/key-settings/titan-rocksdb-compactions.png)


#### Workload Commands

Load data

```
go-ycsb load mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -p requestdistribution=uniform -pfieldcount=31 -p fieldlength=1024
```

Run workload
```
go-ycsb run mysql -P /ycsb/workloads/workloada -p {host} -p mysql.port={port} -p mysql.db=test -p threadcount=100 -p recordcount=5000000 -p operationcount=5000000 -p workload=core -prequestdistribution=uniform -p fieldcount=31 -p fieldlength=1024
```
## Edge Cases and Specific Optimizations

While the general configurations provided earlier offer a good starting point for performance tuning, certain scenarios require more targeted optimizations. This section covers specific cases that may need individual attention and fine-tuning.

### Identifying Edge Cases

1. Analyze query patterns and workload characteristics
2. Monitor system metrics and performance bottlenecks
3. Gather feedback from application teams on specific pain points

### Common Edge Cases and Solutions

Here are the common edge cases and solutions:

1. High TSO wait for high-frequency small queries
2. Choose the proper max chunk size for different workloads
3. Tune coprocessor cache for read-heavy workloads
4. Optimize chunk size for workload characteristics
5. Optimize transaction mode and DML type for different workloads
6. Optimize group by and distinct operations with TiKV pushdown
7. Mitigate MVCC version accumulation using in-memory engine
8. Optimize statistics collection during batch operations
9. Optimize thread pool settings for different instance types

Each of these cases may require adjustments to different parameters or usage of specific features in TiDB. The following sections provide more details on how to address these scenarios.

Remember that these optimizations should be applied cautiously and with thorough testing, as their effectiveness can vary depending on your specific use case and data patterns.

### High TSO wait for high-frequency small queries

#### How to Troubleshooting

TSO (Timestamp Oracle) waiting time can become a significant performance bottleneck, particularly in workloads with high-frequency small transactions or queries that require frequent timestamp allocation. This bottleneck can be identified through the [SQL Execute Time Overview](https://docs.pingcap.com/tidb/stable/performance-tuning-methods#tune-by-color) panel in the [Performance Overview Dashboard](https://docs.pingcap.com/tidb/stable/grafana-performance-overview-dashboard). If TSO waiting time constitutes a large percentage of total SQL execution time, consider these optimizations:

- Use [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) for read operations that don't require strict consistency
- Enable [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml) to reduce TSO requests for batch operations
- Consider batching small transactions into larger ones where possible

#### Solution 1 `tidb_low_resolution_tso`

The `tidb_low_resolution_tso` setting allows TiDB to use cached timestamps for read operations, significantly reducing TSO wait time at the cost of potentially stale reads. This optimization is particularly effective for:

- Read-heavy workloads where slight staleness is acceptable
- Scenarios where reducing query latency is more critical than absolute consistency
- Applications that can tolerate reads that may be a few seconds behind the latest committed state

To enable this optimization:

```sql
set global tidb_low_resolution_tso=on;
```

##### Justifications

| configurations | Pro | Cons | 
| ---------| ---- | ----|
| [`tidb_low_resolution_tso`](system-variables.md#tidb_low_resolution_tso)| Reduces query latency by enabling stale reads with cached TSO, eliminating the need to request new timestamps | Trades consistency for performance - only suitable for scenarios that can tolerate stale reads. Not recommended when strict data consistency is required | 

#### Solution 2 `tidb_tso_client_rpc_mode`

The default value of `tidb_tso_client_rpc_mode` is `DEFAULT`. When the following conditions are met, you can consider switching `tidb_tso_client_rpc_mode` to `PARALLEL` or `PARALLEL-FAST` for potential performance improvements:

- TSO waiting time constitutes a significant portion of the total execution time of SQL queries.
- The TSO allocation in PD has not reached its bottleneck.
- PD and TiDB nodes have sufficient CPU resources.
- The network latency between TiDB and PD is significantly higher than the time PD takes to allocate TSO (that is, network latency accounts for the majority of TSO RPC duration).
  - To get the duration of TSO RPC requests, check the PD TSO RPC Duration panel in the PD Client section of the TiDB dashboard.
  - To get the duration of PD TSO allocation, check the PD server TSO handle duration panel in the TiDB section of the Grafana PD dashboard.
- The additional network traffic resulting from more TSO RPC requests between TiDB and PD (twice for PARALLEL or four times for PARALLEL-FAST) is acceptable.

```sql
set global tidb_tso_client_rpc_mode=PARALLEL;
```

### Tune coprocessor cache for read-heavy workloads

For read-heavy workloads, optimizing the coprocessor cache can significantly improve query performance. The [coprocessor cache](https://docs.pingcap.com/tidb/stable/coprocessor-cache) stores the results of coprocessor requests, reducing the need to recompute frequently accessed data. To optimize cache performance:

1. Monitor the current cache hit ratio using the metrics described in the [coprocessor cache documentation](https://docs.pingcap.com/tidb/stable/coprocessor-cache)
2. Consider increasing the cache size for better hit rates on larger working sets
3. Adjust the admission threshold based on your query patterns

Here are the recommended settings for a read-heavy workload:

```toml
[tikv-client.copr-cache]
capacity-mb = 4096
admission-max-ranges = 5000
admission-max-result-mb = 10
admission-min-process-ms = 0
```

### Optimize chunk size for workload characteristics

The [`tidb_max_chunk_size`](system-variables.md#tidb_max_chunk_size) controls how many rows TiDB processes in a single iteration during query execution. Optimizing this value based on your workload can significantly impact performance:

#### Workload-Specific Recommendations

- **OLTP Workloads** (high concurrency, small transactions):
  - Recommended range: 128-256 rows (default is 1024)
  - Benefits: Reduced memory overhead, faster limit query processing
  - Use case: Point queries, small range scans

  ```sql
  SET GLOBAL tidb_max_chunk_size = 128;
  ```

- **OLAP/Analytical Workloads** (complex queries, large result sets):
  - Recommended range: 1024-4096 rows
  - Benefits: Improved throughput for large scans
  - Use case: Aggregations, large table scans

  ```sql
  SET GLOBAL tidb_max_chunk_size = 4096;
  ```

### Optimize transaction mode and DML type for different workloads

TiDB provides different transaction modes and DML execution types to optimize performance for various workload patterns:

#### Transaction Modes

- **Pessimistic Mode** (Default):
  - Best for general workloads with potential write conflicts
  - Provides better consistency guarantees
  ```sql
  SET SESSION tidb_txn_mode = "pessimistic";
  ```

- **Optimistic Mode**:
  - Suitable for workloads with minimal write conflicts
  - Better performance for multi-statement transactions
  - Example: `begin; insert...; insert...; commit;`
  ```sql
  SET SESSION tidb_txn_mode = "optimistic";
  ```

#### DML Types

`tidb_dml_type = "bulk"` indicates the bulk DML execution mode, which is suitable for scenarios where a large amount of data is written, causing excessive memory usage in TiDB.

- **Pipeline DML** (New in v8.0.0):
  - Ideal for bulk data loading with no conflicts
  - Reduces TiDB memory usage during large writes
  - Requirements:
    - Auto-commit must be enabled
    - `pessimistic-auto-commit` must be false
  ```sql
  SET SESSION tidb_dml_type = "bulk";
  ```

### Optimize group by and distinct operations with TiKV pushdown

TiDB can push down aggregation operations to TiKV to optimize query performance by reducing data transfer and processing overhead. The effectiveness depends on your data characteristics:

#### When to Use Pushdown

- **Ideal Scenarios** (High Performance Gain):
  - Columns with low number of distinct values (NDV)
  - Data with high repetition (many duplicate values)
  - Example: Status columns, category codes, date parts

- **Non-Ideal Scenarios** (Potential Performance Loss):
  - Columns with high NDV (mostly unique values)
  - Unique identifiers or timestamps
  - Example: User IDs, transaction IDs

#### Configuration

Enable pushdown optimizations at the session or global level:

```sql
-- Enable regular aggregation pushdown
SET GLOBAL tidb_opt_agg_push_down = ON;

-- Enable distinct aggregation pushdown
SET GLOBAL tidb_opt_distinct_agg_push_down = ON;
```

### Mitigate MVCC version accumulation using in-memory engine
If you observe excessive MVCC versions during performance testing (caused by either hot read/write spots or garbage collection/compaction issues), you can enable the in-memory engine feature to alleviate this problem. This feature is available since v8.4.0 and can be enabled by adding the following configuration to your TiKV configuration file.

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

### Optimize statistics collection during batch operations

Statistics collection is crucial for query optimization but can impact performance during batch operations. Here's how to manage it effectively:

#### When to Disable Auto Analyze

- During large data imports
- Bulk update operations
- Time-sensitive batch processing
- When you want full control over statistics collection timing

#### Best Practices

1. **Before Batch Operation**:
   ```sql
   -- Disable auto analyze
   SET GLOBAL tidb_enable_auto_analyze = OFF;
   ```

2. **After Batch Operation**:
   ```sql
   -- Manually collect statistics
   ANALYZE TABLE your_table;
   
   -- Re-enable auto analyze
   SET GLOBAL tidb_enable_auto_analyze = ON;
   ```

### Optimize thread pool settings for different instance types

TiKV's performance can be significantly improved by properly configuring thread pools based on your instance's CPU resources. Here's how to optimize these settings:

#### Thread Pool Recommendations

| Instance Size | Description | Recommended Settings |
|--------------|-------------|---------------------|
| 8-16 cores | Default settings usually sufficient | Use system defaults |
| 32+ cores | Increase pool sizes for better resource utilization | Adjust as shown below |

#### Configuration for 32 Core Instances

```toml
[server]
# Increase gRPC thread pool 
grpc-concurrency = 10

[raftstore]
# Optimize for write-intensive workloads
apply-pool-size = 4
store-pool-size = 4
store-io-pool-size = 2
```