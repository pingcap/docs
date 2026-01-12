---
title: TiDB 8.5.5 Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB 8.5.5.
---

# TiDB 8.5.5 Release Notes

Release date: xx xx, 2026

TiDB version: 8.5.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Features

### Performance

* Introduce significant performance improvements for certain lossy DDL operations (such as `BIGINT → INT` and `CHAR(120) → VARCHAR(60)`): when no data truncation occurs, the execution time of these operations can be reduced from hours to minutes, seconds, or even milliseconds, delivering performance gains ranging from tens to hundreds of thousands of times [#63366](https://github.com/pingcap/tidb/issues/63366) [@wjhuang2016](https://github.com/wjhuang2016), [@tangenta](https://github.com/tangenta), [@fzzf678](https://github.com/fzzf678) **tw@qiancai** <!--2292-->

    The optimization strategies are as follows:

    - In strict SQL mode, TiDB pre-checks for potential data truncation risks during type conversion.
    - If no data truncation risk is detected, TiDB updates only the metadata and avoids index rebuilding whenever possible.
    - If index rebuilding is required, TiDB uses a more efficient ingest process to significantly improve index rebuild performance.

    The following table shows example performance improvements based on benchmark tests on a table with 114 GiB of data and 600 million rows. The test cluster consists of 3 TiDB nodes, 6 TiKV nodes, and 1 PD node. All nodes are configured with 16 CPU cores and 32 GiB of memory.

    | Scenario | Operation type | Before optimization | After optimization | Performance improvement |
    |----------|----------------|---------------------|--------------------|--------------------------|
     | Non-indexed column | `BIGINT → INT` | 2 hours 34 minutes | 1 minute 5 seconds | 142× faster |
    | Indexed column | `BIGINT → INT` | 6 hours 25 minutes | 0.05 seconds | 460,000× faster |
     | Indexed column | `CHAR(120) → VARCHAR(60)` | 7 hours 16 minutes | 12 minutes 56 seconds | 34× faster |

    Note that the preceding test results are based on the condition that no data truncation occurs during the DDL execution. The optimizations do not apply to tables with TiFlash replicas or to schema changes involving conversions between signed and unsigned integer types (signed ↔ unsigned).

    For more information, see [documentation](/sql-statements/sql-statement-modify-column.md).

* Improve DDL performance in scenarios with a large number of foreign keys, with up to a 25x increase in logical DDL performance [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1896-->

    Before v8.5.5, in scenarios involving ultra-large-scale tables (for example, a cluster with 10 million tables in total, including hundreds of thousands of tables with foreign keys), the performance of logical DDL operations (such as creating tables or adding columns) can drop to approximately 4 QPS. This leads to low operational efficiency in multi-tenant SaaS environments.

    TiDB v8.5.5 optimizes these scenarios. Test results show that in an extreme environment with 10 million tables (including 200,000 tables with foreign keys), the logical DDL processing performance consistently maintains 100 QPS. Compared to previous versions, the performance is improved by 25 times, significantly enhancing the operational responsiveness of ultra-large-scale clusters.

* Support pushing index lookups down to TiKV to improve query performance [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao)

    Starting from v8.5.5, TiDB supports using [optimizer hints](/optimizer-hints.md) to push the `IndexLookUp` operator down to TiKV nodes. This reduces the number of remote procedure calls (RPCs) and can improve query performance. The actual performance improvement varies depending on the specific workload and requires testing for verification.

    To explicitly instruct the optimizer to push index lookups down to TiKV for a specific table, you can use the [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint. It is recommended to combine this hint with the table's AFFINITY attribute. For example, set `AFFINITY="table"` for regular tables and `AFFINITY="partition"` for partitioned tables.

    To disable index lookup pushdown to TiKV for a specific table, use the [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#no_index_lookup_pushdownt1_name--new-in-v855) hint.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855).

* Support table-level data affinity to improve query performance (experimental) [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) **tw@qiancai** <!--2317-->

    Starting from v8.5.5, you can set the `AFFINITY` table option to `table` or `partition` when creating or altering a table. When this option is enabled, PD groups Regions that belong to the same table or the same partition into a single affinity group. During scheduling, PD prioritizes placing the Leaders and Voter replicas of these Regions on the same subset of a few TiKV nodes. In this scenario, by using the [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint in queries, you can explicitly instruct the optimizer to push index lookups down to TiKV, reducing the latency caused by cross-node scattered queries and improving query performance.

    Note that this feature is currently experimental and is disabled by default. To enable it, set the PD configuration item [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855) to a value greater than `0`. This configuration item controls the maximum number of affinity scheduling tasks that PD can perform concurrently.

  For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/table-affinity).

* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    Starting from v8.5.5, the log backup compaction feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

    - **Improved recovery performance**: SST files can be more quickly imported into the cluster.
    - **Reduced storage space consumption**: redundant data is removed during compaction.
    - **Reduced impact on applications**: RPOs (Recovery Point Objective) can be maintained with less frequent full snapshot-based backups.

  For more information, see [documentation](/br/br-compact-log-backup.md).

* Accelerate recovery of system tables from backups [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth) **tw@lilin90** <!--2109-->

    Starting from v8.5.5, for restoring system tables from a backup, BR introduces a new `--fast-load-sys-tables` parameter to use physical restore instead of logical restore. With this parameter enabled, BR fully replaces or overwrites the existing system tables rather than restoring data into them, significantly improving restore performance in large-scale deployments.

    For more information, see [Documentation](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema).

### Reliability

* Improve scheduling stability in TiKV during network jitter [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang) **tw@qiancai** <!--2260-->

    Starting from v8.5.5, TiKV introduces a network slow-node detection and feedback mechanism. When this mechanism is enabled, TiKV probes network latency between nodes, calculates a network slow score, and reports the score to PD. Based on this score, PD evaluates the network status of TiKV nodes and adjusts scheduling accordingly: when a TiKV node is detected to be experiencing network jitter, PD restricts the scheduling of new Leaders to that node; if the network jitter persists, PD proactively evicts existing Leaders from the affected node to other TiKV nodes, thereby reducing the impact of network issues on the cluster.

    For more information, see [documentation](/pd-control.md#scheduler-config-evict-slow-store-scheduler).

### Availability

* Introduce the client circuit breaker pattern for PD [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--2051-->

    To protect the PD leader from overloading during retry storms or similar feedback loops, TiDB now implements a circuit breaker pattern. When the error rate reaches a predefined threshold, the circuit breaker limits incoming traffic to allow the system to recover and stabilize. You can use the `tidb_cb_pd_metadata_error_rate_threshold_ratio` system variable to control the circuit breaker.

    For more information, see [Documentation](/system-variables.md#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855).

### SQL

* Support dynamically modifying the concurrency and throughput of distributed `ADD INDEX` jobs [#64947](https://github.com/pingcap/tidb/issues/64947) @[joechenrh](https://github.com/joechenrh) **tw@qiancai** <!--2326-->

   In TiDB versions earlier than v8.5.5, when the Distributed eXecution Framework (DXF) [`tidb_enable_dist_task`](/system-variables/#tidb_enable_dist_task-new-in-v710) is enabled, modifying the `THREAD`, `BATCH_SIZE`, or `MAX_WRITE_SPEED` parameters of a running `ADD INDEX` job is not supported. To change these parameters, you have to cancel the running `ADD INDEX` job, reconfigure the parameters, and then resubmit the job, which is inefficient.

    Starting from v8.5.5, you can use the `ADMIN ALTER DDL JOBS` statement to dynamically adjust these parameters of a running distributed `ADD INDEX` job based on the current workload and performance requirements, without interrupting the job. 

    For more information, see [documentation](/sql-statements/sql-statement-admin-alter-ddl.md).

### DB operations

* Support gracefully shutting down TiKV [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0) **tw@qiancai** <!--2297-->

    When shutting down a TiKV server, TiKV attempts to transfer the Leader replicas on the node to other TiKV nodes within a configurable timeout duration before the shutdown. The default timeout duration is 20 seconds, and you can adjust it using the [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855) configuration item. If the timeout is reached and some Leaders have not been successfully transferred, TiKV skips the remaining Leader transfers and proceeds with the shutdown.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855).

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    Starting from v8.5.5, when a log backup task is running, you can still perform a snapshot restore as long as prerequisite conditions are met. This enables ongoing log backups to proceed without having to stop them during the restore process, and the restored data is properly recorded by the ongoing log backup.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore).

* Support table-level restores from log backups [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    Starting from v8.5.5, you can perform point-in-time recovery (PITR) for individual tables from log backups by using filters. Restoring specific tables, rather than the entire cluster, to a target point in time provides more flexible and less disruptive recovery options.

    For more information, see [documentation](/br/br-pitr-manual.md#restore-data-using-filters).

### Observability

* Add storage engine identifiers to statement summary tables and slow query logs [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw) **tw@Oreoxmt**<!--2034 -->

    When both TiKV and TiFlash are deployed in a cluster, users often need to filter SQL statements by storage engine during database diagnostics and performance optimization. For example, if TiFlash is under high load, users might need to identify SQL statements running on TiFlash to locate potential causes. To meet this need, starting from v8.5.5, TiDB adds storage engine identifier fields to statement summary tables and slow query logs.

    New fields in [statement summary tables](/statement-summary-tables.md):

    * `STORAGE_KV`: `1` indicates that the SQL statement accesses TiKV.
    * `STORAGE_MPP`: `1` indicates that the SQL statement accesses TiFlash.

    New fields in [slow query logs](/identify-slow-queries.md):

    * `Storage_from_kv`: `true` indicates that the SQL statement accesses TiKV.
    * `Storage_from_mpp`: `true` indicates that the SQL statement accesses TiFlash.

    This feature simplifies workflows in certain diagnostics and performance optimization scenarios and improves issue identification efficiency.

    For more information, see [Statement Summary Tables](/statement-summary-tables.md) and [Identify Slow Queries](/identify-slow-queries.md).

### Security

* Enable Azure Managed Identity (MI) authentication for Backup & Restore (BR) to Azure Blob Storage [#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--2308-->

    Starting from v8.5.5, BR supports Azure Managed Identity (MI) for authenticating to Azure Blob Storage, eliminating the need for static SAS tokens. This enables secure, keyless, and ephemeral authentication that follows Azure security best practices.

    With this feature, BR and the embedded BR worker in TiKV can acquire access tokens directly from Azure Instance Metadata Service (IMDS), reducing credential leakage risk and simplifying credential rotation for self-managed and cloud deployments on Azure.

    This enhancement is particularly useful for enterprise customers running TiDB on Azure Kubernetes Service (AKS) or other Azure environments that require strict security controls for backup and restore operations.

    For more information, see [Documentation](link).

## Compatibility changes

### Behavior changes


### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) | Modified | Changes the default value from `PREDICATE` to `ALL` to improve the completeness of statistics. |
| [`tidb_advancer_check_point_lag_limit`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_advancer_check_point_lag_limit-new-in-v855) | Newly added | Controls the maximum allowed checkpoint lag for a log backup task. The default value is `48h0m0s`. If a task's checkpoint lag exceeds this limit, TiDB Advancer pauses the task. |
| [`tidb_cb_pd_metadata_error_rate_threshold_ratio`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855)    | Newly added  | Controls when TiDB triggers the circuit breaker. The default value is `0`, which means the circuit breaker is disabled. Setting a value between `0.01` and `1` enables it, causing the circuit breaker to trigger when the error rate of specific requests sent to PD reaches or exceeds the threshold. |
| [`tidb_index_lookup_pushdown_policy`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_index_lookup_pushdown_policy-new-in-v855) | Newly added | Controls whether and when TiDB pushes the `IndexLookUp` operator down to TiKV. The default value is `hint-only`, which means TiDB pushes the `IndexLookUp` operator down to TiKV only when the [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint is explicitly specified in the SQL statement. |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| PD | [`schedule.max-affinity-merge-region-size`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#max-affinity-merge-region-size-new-in-v855) | Newly added | Controls the threshold for automatically merging adjacent small Regions within the same [affinity group](https://docs.pingcap.com/tidb/v8.5/table-affinity). The default value is `256`, in MiB. |
| PD  | [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855) | Newly added | Controls the number of [affinity](https://docs.pingcap.com/tidb/v8.5/table-affinity) scheduling tasks that can be performed concurrently. The default value is `0`, which means that affinity scheduling is disabled by default. |
| TiDB | [`performance.enable-async-batch-get`](https://docs.pingcap.com/tidb/v8.5/tidb-configuration-file#enable-async-batch-get-new-in-v855)  | Newly added | Controls whether TiDB uses asynchronous mode to execute the Batch Get operator. The default value is `true`. |
| TiKV | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).level0-slowdown-writes-trigger`](/tikv-configuration-file.md#level0-slowdown-writes-trigger) | Modified | Starting from v8.5.5, when the flow control mechanism is enabled ([`storage.flow-control.enable`](/tikv-configuration-file.md#enable) is set to `true`), this configuration item is overridden by [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold) only if its value is greater than the `storage.flow-control.l0-files-threshold`. This behavior prevents weakening RocksDB’s compaction acceleration mechanism when you increase the flow control threshold. In v8.5.4 and earlier versions, when the flow control mechanism is enabled, this configuration item is directly overridden by `storage.flow-control.l0-files-threshold`. |
| TiKV | [`rocksdb.(defaultcf|writecf|lockcf|raftcf).soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit-1) | Modified | Starting from v8.5.5, when the flow control mechanism is enabled ([`storage.flow-control.enable`](/tikv-configuration-file.md#enable) is set to `true`), this configuration item is overridden by [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit) only if its value is greater than `storage.flow-control.soft-pending-compaction-bytes-limit`. This behavior prevents weakening RocksDB’s compaction acceleration mechanism when you increase the flow control threshold. In v8.5.4 and earlier versions, when the flow control mechanism is enabled, this configuration item is directly overridden by `storage.flow-control.soft-pending-compaction-bytes-limit`. |
| TiKV | [`readpool.cpu-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#cpu-threshold-new-in-v855) | Newly added | Specifies the CPU utilization threshold for the unified read pool. The default value is `0.0`, which means that there is no limit on the CPU usage of the unified read pool. The size of the thread pool is determined solely by the busy thread scaling algorithm, which adjusts the size dynamically based on the number of threads handling current tasks. |
| TiKV | [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855) | Newly added | Controls the timeout duration for graceful shutdown of TiKV. The default value is `20s`. |
| TiKV | [`server.inspect-network-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#inspect-network-interval-new-in-v855) | Newly added | Controls the interval at which the TiKV HealthChecker actively performs network detection to PD and other TiKV nodes. The default value is `100ms`. |
| BR | [`--checkpoint-storage`](/br/br-checkpoint-restore.md#implementation-details-store-checkpoint-data-in-the-downstream-cluster) | Newly added | Specifies an external storage for checkpoint data. |
| BR | [`--fast-load-sys-tables`](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) | Newly added | Supports physical restore of system tables on a new cluster. This parameter is enabled by default. |
| BR | [`--filter`](/br/br-pitr-manual.md#restore-data-using-filters) | Newly added | Specifies patterns to include or exclude specific databases or tables for restore. |

### System tables

### Other changes

## Improvements

+ TiDB <!--tw@qiancai: 4 notes-->

    - Improve error messages for `IMPORT INTO` when encoding errors occur to help users identify issues more accurately [#63763](https://github.com/pingcap/tidb/issues/63763) @[D3Hunter](https://github.com/D3Hunter)
    - Enhance the parsing mechanism for Parquet files to improve the import performance of Parquet-formatted data [#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh)
    - Set the default value of `tidb_analyze_column_options` to `all` to collect statistics for all columns by default [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)
    - Optimize the execution logic of the `IndexHashJoin` operator by using incremental processing in specific JOIN scenarios to avoid loading large amounts of data at once, significantly reducing memory usage and improving performance [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - (dup): release-9.0.0.md > Improvements> TiDB - Optimize the CPU usage of internal SQL statements in the Distributed eXecution Framework (DXF) [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)
    - Improve the performance of the expression.Contains function [#61373](https://github.com/pingcap/tidb/issues/61373) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV <!--tw@lilin90: 3 notes-->

    - Introduce CPU-aware scaling for the unified read pool to avoid CPU starvation under hot read workloads [#18464](https://github.com/tikv/tikv/issues/18464) @[mittalrishabh](https://github.com/mittalrishabh)
    - Add network latency awareness to slow score to avoid scheduling leaders to TiKV nodes with unstable network conditions [#18797](https://github.com/tikv/tikv/issues/18797) @[okJiang](https://github.com/okJiang)
    - Optimize hibernate Region behavior by allowing leaders to enter the hibernation state immediately after receiving a majority of votes, without waiting for offline non-voter peers [#19070](https://github.com/tikv/tikv/issues/19070) @[jiadebin](https://github.com/jiadebin)
    - (dup): release-9.0.0.md > Improvements> TiKV - Throttle BR log restore requests when TiKV memory usage is high to prevent TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD <!--tw@Oreoxmt: 4 notes-->

    - Optimize metrics with high cardinality [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - Optimize the logic for timestamp advancement and leader election [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies)
    - Support batch configuration of TiKV store limits [#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies)
    - Add the `store` label to the `pd_cluster_status` metric [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80)

+ Tools

    + TiCDC <!--tw@qiancai: 1 note-->

        - Enhance the configuration validation logic for changefeeds: when creating or updating a changefeed, if a column referenced in the Dispatcher configuration does not exist, TiCDC returns an error and rejects the operation to prevent execution failures  [#12253](https://github.com/pingcap/tiflow/issues/12253) @[wk989898](https://github.com/wk989898)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 15 notes-->

    - Fix the issue that TiDB fails to read the latest value of the tidb_mem_quota_binding_cache variable for initialization during the startup process [#65381](https://github.com/pingcap/tidb/issues/65381) @[qw4990](https://github.com/qw4990)
    - Fix the issue that candidate items are incorrectly skipped in extractBestCNFItemRanges, leading to inaccurate query range calculation [#62547](https://github.com/pingcap/tidb/issues/62547) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `plan replayer` cannot load the binding [#64811](https://github.com/pingcap/tidb/issues/64811) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `PointGet` fails to reuse chunks even when memory is sufficient, leading to unnecessary memory allocations [#63920](https://github.com/pingcap/tidb/issues/63920) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `LogicalProjection.DeriveStats` consumes excessive memory during allocation [#63810](https://github.com/pingcap/tidb/issues/63810) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB fails to dump the plan replayer when a query panics [#64835](https://github.com/pingcap/tidb/issues/64835) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `SHOW CREATE TABLE` statement might display attributes in an incorrect order for TTL tables in certain cases [#64876](https://github.com/pingcap/tidb/issues/64876) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the execution summary information for a TTL job is empty when the job times out [#61509](https://github.com/pingcap/tidb/issues/61509) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that correlated subqueries might trigger unexpected full table scans when the Plan Cache is enabled [#64645](https://github.com/pingcap/tidb/issues/64645) @[winoros](https://github.com/winoros)
    - Fix the issue that system tables cause incorrect calculation of table health metrics [#57176](https://github.com/pingcap/tidb/issues/57176), [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that the `mysql.tidb_ddl_notifier` table cannot be cleaned up when automatic statistics updates are disabled (`tidb_enable_auto_analyze = OFF`) [#64038](https://github.com/pingcap/tidb/issues/64038) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that columns are redundantly allocated in `newLocalColumnPool` [#63809](https://github.com/pingcap/tidb/issues/63809) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that there are redundant `syncload` failure warning logs [#63880](https://github.com/pingcap/tidb/issues/63880) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that TiDB might panic and exit unexpectedly when a connection that runs an active transaction is manually terminated [#63956](https://github.com/pingcap/tidb/issues/63956) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that goroutine and memory leaks might occur when a cached table reads from a TiFlash replica [#63329](https://github.com/pingcap/tidb/issues/63329) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that foreign key is not updated after running `ALTER TABLE child CHANGE COLUMN` to modify a column [#issue](https://github.com/pingcap/tidb/issues/59705) @[fzzf678](https://github.com/fzzf678) <!--tw@hfxsd: the following 16 notes-->
    - Fix the issue that an error occurs when decoding the `RENAME TABLE` job arg from an earlier version [#64413](https://github.com/pingcap/tidb/issues/64413) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the auto increment is not rebased if BR restore fails [#60804](https://github.com/pingcap/tidb/issues/60804) @[joechenrh](https://github.com/joechenrh)
    - Fix the OOM issue when querying `information_schema` tables [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - Fix the isse that the TiDB node might get stuck during upgrade [#64539](https://github.com/pingcap/tidb/issues/64539) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that admin check does not report errors when there are no index records [#63698](https://github.com/pingcap/tidb/issues/63698) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that data indexes are inconsistent when changing the collation with modify column [#61668](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - Fix the issue that embedded ANALYZE might not be triggered for multiple schema changes [#65040](https://github.com/pingcap/tidb/issues/65040) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the DXF (Distributed eXecution Framework) task is not cancelled after canceling the `ADD INDEX` job [#issue](https://github.com/pingcap/tidb/issues/64129) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the check is incorrect when determining whether to load the table information for tables that contain foreign keys [#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    - Fix the issue that initialization for foreign keys related fields is incorrect when copying the table information [#60044](https://github.com/pingcap/tidb/issues/60044) @[JQWong7](https://github.com/JQWong7)
    - Fix the issue that the auto ID setting is incorrect after renaming a table cross databases [#issue](https://github.com/pingcap/tidb/issues/64561) @[joechenrh](https://github.com/joechenrh)
    - Fix the high CPU usage issue caused by incorrect handling of meta keys [#issue](https://github.com/pingcap/tidb/issues/64323) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that TiDB Ligtning does not report an error when a schema file lacks a trailing semicolon [#63414](https://github.com/pingcap/tidb/issues/63414) @[GMHDBJD](https://github.com/GMHDBJD)
    - Fix the issue that an infinite loop occurs when reading files during an `IMPORT INTO` operation with Global Sort enabled [#61177](https://github.com/pingcap/tidb/issues/61177) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the panic issue when processing generated columns for `IMPORT INTO` [#issue](https://github.com/pingcap/tidb/issues/64657) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that an error might be incorrectly reported when a single SQL statement contains multiple `AS OF TIMESTAMP` expressions [#65090](https://github.com/pingcap/tidb/issues/65090) @[you06](https://github.com/you06)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the potential OOM issue when querying `information_schema.tables` by improving memory usage monitoring when quering system tables [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)

+ TiKV <!--tw@Oreoxmt: 7 notes-->

    - Fix the issue that the `KV Cursor Operations` metric for analyze requests is always `0` [#19206](https://github.com/tikv/tikv/issues/19206) @[glorv](https://github.com/glorv)
    - Fix the issue that Region heartbeats might report incorrect Region size or key statistics to PD after a leader change [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - Fix the issue that unsafe recovery gets stuck by removing tombstone TiFlash learners from the unsafe recovery demotion list [#18458](https://github.com/tikv/tikv/issues/18458) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that snapshots might be canceled indefinitely during continuous writes, which blocks replica recovery [#18872](https://github.com/tikv/tikv/issues/18872) @[exit-code-1](https://github.com/exit-code-1)
    - Fix the issue that compaction slows down due to increased flow-control thresholds [#18708](https://github.com/tikv/tikv/issues/18708) @[hhwyt](https://github.com/hhwyt)
    - Fix the issue that Raft peers might enter hibernation prematurely in a corner case, causing them to remain busy and block leader transfers after a TiKV restart [#19203](https://github.com/tikv/tikv/issues/19203) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!--tw@qiancai: 7 notes-->

    - Fix the issue that a node might not be removable during the process of bringing it online [#8997](https://github.com/tikv/pd/issues/8997) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that a large number of Leader transfers might cause sudden changes in Region size [#10014](https://github.com/tikv/pd/issues/10014) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that might cause PD panic during scheduling [#9951](https://github.com/tikv/pd/issues/9951) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that data might become imbalanced during the import process [#9088](https://github.com/tikv/pd/issues/9088) @[GMHDBJD](https://github.com/GMHDBJD)
    - Fix the issue that, after enabling the Active PD Follower feature, requests that fail on a Follower node cannot correctly fall back to the Leader node for retry [#64933](https://github.com/pingcap/tidb/issues/64933) @[okJiang](https://github.com/okJiang)
    - Fix the issue that some requests are not correctly forwarded in PD microservices mode [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that connections might fail due to incorrect TLS configuration loading in the `tso` and `scheduling` microservices [#9367](https://github.com/tikv/pd/issues/9367) @[rleungx](https://github.com/rleungx)

+ TiFlash <!--tw@hfxsd: 3 notes-->

    - Fix the issue that TiFlash might panic when BR is restoring data [#10606](https://github.com/pingcap/tiflash/issues/10606) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that TiFlash cannot fully utilize more than 16 CPU cores when BR is restoring data [#10605](https://github.com/pingcap/tiflash/issues/10605) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might exit unexpectedly when `GROUP_CONCAT` triggers a disk spill [#10553](https://github.com/pingcap/tiflash/issues/10553) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 7 notes-->

        - Fix the issue that enabling log backup causes excessive memory usage when the cluster contains many Regions [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the Azure SDK cannot find a suitable key from the environment [#18206](https://github.com/tikv/tikv/issues/18206) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that foreign keys cannot be properly restored during `restore point` [#61642](https://github.com/pingcap/tidb/issues/61642) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that restore fails if system table collations are incompatible between the backup and target cluster by adding the `--sys-check-collation` parameter to support restoring privilege tables from v6.5 to v7.5 [#64667](https://github.com/pingcap/tidb/issues/64667) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that `restore log` cannot be performed after a failed `restore point`, even when the operation is safe [#64908](https://github.com/pingcap/tidb/issues/64908) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that `restore point` from a checkpoint might panic when log backup data is mixed with a full backup [#58685](https://github.com/pingcap/tidb/issues/58685) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw@qiancai: 6 notes-->

        - Fix the issue that data might be lost during replication to object storage because Writer close errors are not correctly captured [#12436](https://github.com/pingcap/tiflow/issues/12436) @[wk989898](https://github.com/wk989898)
        - Fix the issue that replicating a `TRUNCATE` operation on a partitioned table might cause changefeed failures [#12430](https://github.com/pingcap/tiflow/issues/12430) @[wk989898](https://github.com/wk989898)
        - Fix the issue that downstream execution order might be incorrect when replicating multi-table `RENAME` DDL statements [#12449](https://github.com/pingcap/tiflow/issues/12449) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the connection errors that might occur when using Glue Schema Registry by upgrading the `aws-sdk-go-v2` dependency version [#12424](https://github.com/pingcap/tiflow/issues/12424) @[wk989898](https://github.com/wk989898)
        - Fix the issue that changefeed tasks might get stuck because the TiKV CDC component fails to release memory quotas correctly after a restart [#18169](https://github.com/tikv/tikv/issues/18169) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that gRPC connections might be unexpectedly closed due to being misjudged as idle when incremental scan tasks accumulate in TiKV CDC [#18915](https://github.com/tikv/tikv/issues/18915) @[asddongmen](https://github.com/asddongmen)
