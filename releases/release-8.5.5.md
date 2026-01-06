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

    Starting from v8.5.5, TiDB supports using optimizer hints to push the `IndexLookUp` operator down to TiKV nodes. This reduces the number of remote procedure calls (RPCs) and can improve query performance. The actual performance improvement varies depending on the specific workload and requires testing for verification.

    You can use the [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint to explicitly instruct the optimizer to push index lookups down to TiKV for a specific table. It is recommended to combine this hint with the table's AFFINITY attribute. For example, set `AFFINITY="table"` for regular tables and `AFFINITY="partition"` for partitioned tables.

    To disable index lookup pushdown to TiKV for a specific table, use the [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/stable/optimizer-hints#no_index_lookup_pushdownt1_name--new-in-v855) hint.

    For more information, see [documentation](https://docs.pingcap.com/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855).

* Support table-level data affinity to improve query performance (experimental) [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) **tw@qiancai** <!--2317-->

    Starting from v8.5.5, you can set the `AFFINITY` table option to `table` or `partition` when creating or altering a table. When this option is enabled, PD groups Regions that belong to the same table or the same partition into a single affinity group. During scheduling, PD preferentially places the Leaders and Voter replicas of these Regions on the same small set of TiKV nodes. In this scenario, by using the [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint in queries, you can explicitly instruct the optimizer to push index lookups down to TiKV, reducing the latency caused by cross-node scattered queries and improving query performance.

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

* Support dynamically modifying the concurrency and throughput of distributed `ADD INDEX` jobs [#62120](https://github.com/pingcap/tidb/pull/62120) @[joechenrh](https://github.com/joechenrh) **tw@qiancai** <!--2326-->

   In TiDB versions earlier than v8.5.5, when the Distributed eXecution Framework (DXF) [`tidb_enable_dist_task`](/system-variables/#tidb_enable_dist_task-new-in-v710) is enabled, modifying the `THREAD`, `BATCH_SIZE`, or `MAX_WRITE_SPEED` parameters of a running `ADD INDEX` job is not supported. To change these parameters, you have to cancel the running `ADD INDEX` job, reconfigure the parameters, and then resubmit the job, which is inefficient.

    Starting from v8.5.5, you can use the `ADMIN ALTER DDL JOBS` statement to dynamically adjust these parameters of a running distributed `ADD INDEX` job based on the current workload and performance requirements, without interrupting the job. 

    For more information, see [documentation](/sql-statements/sql-statement-admin-alter-ddl.md).

### DB operations

* Support gracefully shutting down TiKV [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0) **tw@qiancai** <!--2297-->

    When shutting down a TiKV server, TiKV attempts to transfer the Leader replicas on the node to other TiKV nodes within a configurable timeout duration before the shutdown. The default timeout duration is 20 seconds, and you can adjust it using the [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855) configuration item. If the timeout is reached and some Leaders have not been successfully transferred, TiKV skips the remaining Leader transfers and proceeds with the shutdown.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-new-in-v855).

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    Starting from v8.5.5, when a log backup task is running, you can still perform a snapshot restore as long as prerequisite conditions are met. This enables ongoing log backups to proceed without having to stop them during the restore process, and the restored data is properly recorded by the ongoing log backup.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore).

* Support table-level restores from log backups [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    Starting from v8.5.5, you can perform point-in-time recovery (PITR) for individual tables from log backups by using filters. Restoring specific tables, rather than the entire cluster, to a target point in time provides more flexible and less disruptive recovery options.

    For more information, see [documentation](/br/br-pitr-manual.md#restore-data-using-filters).

### Observability

* Add storage engine identifiers to statement summary tables and slow query logs [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw) **tw@Oreoxmt**<!--2034 -->

    When both TiKV and TiFlash are deployed in a cluster, users often need to filter SQL statements by storage engine during database diagnostics and performance optimization. For example, if TiFlash is under high load, users might need to identify SQL statements running on TiFlash to locate potential causes. To meet this need, starting from v9.0.0, TiDB adds storage engine identifier fields to statement summary tables and slow query logs.

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

* When using [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) with [Global Sort](/tidb-global-sort.md) enabled, primary key or unique index conflicts are now automatically resolved by removing all conflicting rows (none of the conflicting rows are preserved), instead of causing the task to fail. The number of conflicted rows appears in the `Result_Message` column of `SHOW IMPORT JOBS` output, and detailed conflict information is stored in cloud storage. For more information, see [`IMPORT INTO` conflict resolution](/sql-statements/sql-statement-import-into.md#conflict-resolution).

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| `tidb_advancer_check_point_lag_limit`       | Newly added  | Controls the maximum allowed checkpoint lag for a log backup task. If a task's checkpoint lag exceeds this limit, TiDB Advancer pauses the task. |
| `tidb_cb_pd_metadata_error_rate_threshold_ratio`    | Newly added  | Controls when TiDB triggers the circuit breaker. Setting a value of `0` (default) disables the circuit breaker. Setting a value between `0.01` and `1` enables it, causing the circuit breaker to trigger when the error rate of specific requests sent to PD reaches or exceeds the threshold. |
| `tidb_index_lookup_pushdown_policy` | Newly added | Controls whether and when TiDB pushes the `IndexLookUp` operator down to TiKV. |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### System tables

### Other changes

## Improvements

+ TiDB <!--tw@qiancai: 4 notes-->

    - improve the error message for import into when there are encoding errors [#63763](https://github.com/pingcap/tidb/issues/63763) @[D3Hunter](https://github.com/D3Hunter)
    - change the parser for parquet format to get better performance [#62906](https://github.com/pingcap/tidb/issues/) @[joechenrh](https://github.com/joechenrh)
    - 将 `tidb_analyze_column_options` 的默认值设置为 `all` [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe)
    - 优化 IndexHashJoin 的执行方式，在部分 JOIN 场景下采用增量处理以避免一次性加载大量数据，显著降低内存占用并提升执行性能 [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - (dup): release-9.0.0.md > Improvements> TiDB - Optimize the CPU usage of internal SQL statements in the Distributed eXecution Framework (DXF) [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV <!--tw@lilin90: 3 notes-->

    - Introduces CPU-aware scaling for the unified read pool to avoid CPU starvation under hot read workloads. [#18464](https://github.com/tikv/tikv/issues/18464) @[mittalrishabh](https://github.com/mittalrishabh)
    - Adds network latency awareness to slow score to avoid scheduling leaders on TiKV nodes with unstable network conditions. [#18797](https://github.com/tikv/tikv/issues/18797) @[okJiang](https://github.com/okJiang)
    - Optimizes hibernate behavior by allowing leaders to enter hibernation once a majority vote is reached, without waiting for down non-voter peers. [#19070](https://github.com/tikv/tikv/issues/19070) @[jiadebin](https://github.com/jiadebin)
    - (dup): release-9.0.0.md > Improvements> TiKV - Throttle BR log restore requests when TiKV memory usage is high to prevent TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD <!--tw@Oreoxmt: 4 notes-->

    - 优化了高基数指标 [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - 优化了时间戳推进和选举逻辑 [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies)
    - 支持批量设置 TiKV 的 store limit [#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies)
    - `pd_cluster_status` 增加了 store 标签 [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80)

+ Tools

    + TiCDC <!--tw@qiancai: 1 note-->

        - Add more verification for the changefeed config when creating changefeed.  [#12253](https://github.com/pingcap/tiflow/issues/12253) @[wk989898](https://github.com/wk989898)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 15 notes-->

    - 修复 TiDB 初始化时无法读取最新的 tidb_mem_quota_binding_cache 变量值初始化 binding 的问题 [#65381](https://github.com/pingcap/tidb/issues/65381) @[qw4990](https://github.com/qw4990)
    - 修复了在 `extractBestCNFItemRanges` 中错误地跳过候选项导致查询范围计算不精确的问题 [#62547](https://github.com/pingcap/tidb/issues/62547) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `plan replayer` 无法加载 binding 的问题 [#64811](https://github.com/pingcap/tidb/issues/64811) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `PointGet` 在有足够内存时仍不复用 chunk 导致不必要内存分配的问题 [#63920](https://github.com/pingcap/tidb/issues/63920) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了 `LogicalProjection.DeriveStats` 分配过多内存的问题 [#63810](https://github.com/pingcap/tidb/issues/63810) @[hawkingrei](https://github.com/hawkingrei)
    - 修复了当查询发生 panic 时 `plan replayer` 无法 dump 的问题 [#64835](https://github.com/pingcap/tidb/issues/64835) @[hawkingrei](https://github.com/hawkingrei)
    - 提升了 `expression.Contains` 函数的性能 [#61373](https://github.com/pingcap/tidb/issues/61373) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当计划缓存开启时，关联子查询可能产生非预期的全表扫描的问题 [#64645](https://github.com/pingcap/tidb/issues/64645) @[winoros](https://github.com/winoros)
    - 修复系统表会污染表健康度监控的问题 [#57176](https://github.com/pingcap/tidb/issues/57176), [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - 修复 auto-anlyze 关闭之后 `mysql.tidb_ddl_notifier` 不能被清理的问题 [#64038](https://github.com/pingcap/tidb/issues/64038) @[0xPoe](https://github.com/0xPoe)
    - 修复了在 `newLocalColumnPool` 中重复分配 column 的问题 [#63809](https://github.com/pingcap/tidb/issues/63809) @[hawkingrei](https://github.com/hawkingrei)
    - 减少无效的 sync load 加载失败警告日志 [#63880](https://github.com/pingcap/tidb/issues/63880) @[0xPoe](https://github.com/0xPoe)
    - 修复手动 kill 正在执行事务的 connection 可能导致 tidb 发生 panic 异常退出的问题 [#63956](https://github.com/pingcap/tidb/issues/63956) @[wshwsh12](https://github.com/wshwsh12)
    - 修复缓存表在走 TiFlash 副本读取时可能出现的 goroutine 和内存泄漏问题 [#63329](https://github.com/pingcap/tidb/issues/63329) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - fix the problem that foreign key is not updated after modify column [#issue](https://github.com/pingcap/tidb/issues/59705) @[fzzf678](https://github.com/fzzf678) <!--tw@hfxsd: the following 16 notes-->
    - fix error decoding `RENAME TABLE` job arg from older version TiDB [#issue](https://github.com/pingcap/tidb/issues/64413) @[joechenrh](https://github.com/joechenrh)
    - fix missing rebase auto increment not executed if BR restore failed [#issue](https://github.com/pingcap/tidb/issues/64761) @[joechenrh](https://github.com/joechenrh)
    - fix OOM issue when querying `information_schema` tables [#issue](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)
    - fix the problem that TiDB node may stuck during upgrade [#issue](https://github.com/pingcap/tidb/issues/64539) @[joechenrh](https://github.com/joechenrh)
    - fix unexpected successful admin check when there are no index record [#issue](https://github.com/pingcap/tidb/issues/63698) @[wjhuang2016](https://github.com/wjhuang2016)
    - fix data-index inconsistency when chaning collation with modify column [#issue](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - fix incorrect initialization for foreign key related fields when copying table info [#issue](https://github.com/pingcap/tidb/issues/61668) @[tangenta](https://github.com/tangenta)
    - fix the problem that embedded analyze may be not triggered for multi schema change [#issue](https://github.com/pingcap/tidb/issues/65040) @[joechenrh](https://github.com/joechenrh)
    - fix the problem that the DXF task was not cancelled after canceling the add index job [#issue](https://github.com/pingcap/tidb/issues/64129) @[tangenta](https://github.com/tangenta)
    - fix incorrect check to determing whether to load table info for tables contain foreign key [#issue](https://github.com/pingcap/tidb/issues/60444) @[JQWong7](https://github.com/JQWong7)
    - fix incorrect auto ID setting after cross-database rename table [#issue](https://github.com/pingcap/tidb/issues/64561) @[joechenrh](https://github.com/joechenrh)
    - fix incorrect handling meta key for older version of TiDB [#issue](https://github.com/pingcap/tidb/issues/64323) @[wjhuang2016](https://github.com/wjhuang2016)
    - fix ligtning doesnt' report error for schema files without trailing semicolon [#issue](https://github.com/pingcap/tidb/issues/63414) @[GMHDBJD](https://github.com/GMHDBJD)
    - fix the dead loop when reading files during IMPORT INTO global sort [#issue](https://github.com/pingcap/tidb/issues/61177) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - fix the panic when processing generated columns for IMPORT INTO [#issue](https://github.com/pingcap/tidb/issues/64657) @[D3Hunter](https://github.com/D3Hunter)
    - 修复在一个语句中有多个 `AS OF TIMESTAMP` 表达式时可能误报错的问题 [#issue](https://github.com/pingcap/tidb/issues/65090) @[you06](https://github.com/you06)
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the potential OOM issue when querying `information_schema.tables` by improving memory usage monitoring when quering system tables [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)

+ TiKV <!--tw@Oreoxmt: 7 notes-->

    - Fix the bug that analyze scan kv operation metric is always 0 [#19206](https://github.com/tikv/tikv/issues/19206) @[glorv](https://github.com/glorv)
    - Fix the bug that pd heartbeat may report wrong region size/keys statistics data after leader change. [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - Fixes unsafe recovery getting stuck by removing tombstoned TiFlash learners from the unsafe recovery demotion list. [#18458](https://github.com/tikv/tikv/issues/18458) @[v01dstar](https://github.com/v01dstar)
    - Fixes an issue where snapshots could be canceled indefinitely under continuous writes, blocking replica recovery. [#18872](https://github.com/tikv/tikv/issues/18872) @[exit-code-1](https://github.com/exit-code-1)
    - Fixes compaction slowdowns caused by increased flow-control thresholds. [#18708](https://github.com/tikv/tikv/issues/18708) @[hhwyt](https://github.com/hhwyt)
    - Fix the bug that pd heartbeat may report wrong region size/keys statistics data after leader change. [#19180](https://github.com/tikv/tikv/issues/19180) @[glorv](https://github.com/glorv)
    - Fixes a corner case where Raft peers could enter hibernation prematurely, causing them to remain busy and block leader transfers after TiKV restart. [#19203](https://github.com/tikv/tikv/issues/19203) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!--tw@qiancai: 7 notes-->

    - 修复节点在上线过程中可能无法下线的问题 [#8997](https://github.com/tikv/pd/issues/8997) @[lhy1024](https://github.com/lhy1024)
    - 修复因大量 leader transfer 可能导致 region size 跳变的问题 [#10014](https://github.com/tikv/pd/issues/10014) @[lhy1024](https://github.com/lhy1024)
    - 修复调度过程中可能导致 PD panic 的问题 [#9951](https://github.com/tikv/pd/issues/9951) @[bufferflies](https://github.com/bufferflies)
    - 修复导入过程中数据不均衡的问题 [#9088](https://github.com/tikv/pd/issues/9088) @[GMHDBJD](https://github.com/GMHDBJD)
    - 修复开启 PD follower handle 后遇到错误时，无法将请求回退到 leader 处理的问题 [#64933](https://github.com/pingcap/tidb/issues/64933) @[okJiang](https://github.com/okJiang)
    - 修复微服务请求没有正常转发的问题 [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024) [#9825](https://github.com/tikv/pd/issues/9825) @[lhy1024](https://github.com/lhy1024)
    - 修复微服务 TLS 配置问题 [#9367](https://github.com/tikv/pd/issues/9367) @[rleungx](https://github.com/rleungx)

+ TiFlash <!--tw@hfxsd: 3 notes-->

    - 修复在 BR restore 的过程中，TiFlash 可能 panic 的问题 [#10606](https://github.com/pingcap/tiflash/issues/10606) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复在 BR restore 的过程中，TiFlash 不能充分利用超过 16 核 CPU 进行数据恢复的问题 [#10605](https://github.com/pingcap/tiflash/issues/10605) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 GROUP_CONCAT 触发落盘时可能导致 TiFlash 异常退出的问题 [#10553](https://github.com/pingcap/tiflash/issues/10553) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 7 notes-->

        - Fixed an issue that memory usage may be unacceptable when log backup enabled and many regions in cluster. [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed an issue that Azure SDK cannot found suitable key from environment. [#18206](https://github.com/tikv/tikv/issues/18206) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed an issue that foreign keys cannot be properly fixed during `restore point`. [#61642](https://github.com/pingcap/tidb/issues/61642) @[Leavrth](https://github.com/Leavrth)
        - Fixed an issue that restore cannot be performed if system table collations are incompatible between backup and target cluster by introducing the parameter --sys-check-collation to support restore privileges tables from v6.5 to v7.5 [#64667](https://github.com/pingcap/tidb/issues/64667) @[Leavrth](https://github.com/Leavrth)
        - Fixed an issue that caused `restore log` cannot be performed after a failed `restore point` though the latter is safe to be execued. [#64908](https://github.com/pingcap/tidb/issues/64908) @[RidRisR](https://github.com/RidRisR)
        - Fixed an issue that Azure managed identity is unavailable.[#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR)
        - Fixed an issue that may cause `restore point` from checkpoint panic when the log backup was mixed with a full backup. [#58685](https://github.com/pingcap/tidb/issues/58685) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw@qiancai: 6 notes-->

        - Fix the issue that may cause DML loss while failing to close the writer of the storage sink [#12436](https://github.com/pingcap/tiflow/issues/12436) @[wk989898](https://github.com/wk989898)
        - Fix the issue that causes the changefeed to fail when truncating partition tables [#12430](https://github.com/pingcap/tiflow/issues/12430) @[wk989898](https://github.com/wk989898)
        - Fix the incorrect execution order of split DDLs generated from a multi-table DDL statement [#12449](https://github.com/pingcap/tiflow/issues/12449) @[wlwilliamx](https://github.com/wlwilliamx)
        - Upgrade aws-sdk-go-v2 dependency to fix glue schema registry[#12424](https://github.com/pingcap/tiflow/issues/12424) @[wk989898](https://github.com/wk989898)
        - Fix the issue that may cause the sink memory quota not to be released [#18169](https://github.com/tikv/tikv/issues/18169) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that may cause the sink memory quota not to be released [#18915](https://github.com/tikv/tikv/issues/18915) @[asddongmen](https://github.com/asddongmen)
