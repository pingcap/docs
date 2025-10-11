---
title: TiDB 8.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.3.0.
---

# TiDB 8.3.0 Release Notes

Release date: August 22, 2024

TiDB version: 8.3.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.3/quick-start-with-tidb)

8.3.0 introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">Scalability and Performance</td>
    <td> <a href="https://docs.pingcap.com/tidb/v8.3/partitioned-table#global-indexes">Global indexes for partitioned tables (experimental)</a></td>
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned columns, and remove the restriction that a unique key must contain the partition key. This feature extends the usage scenarios of TiDB partitioned tables and avoids some of the application modification work that might be required for data migration.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/system-variables#tidb_opt_projection_push_down-new-in-v610">Default pushdown of the <code>Projection</code> operator to the storage engine</a></td>
    <td>Pushing the <code>Projection</code> operator down to the storage engine can distribute the load across storage nodes while reducing data transfer between nodes. This optimization helps to reduce the execution time for certain SQL queries and improves the overall database performance.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/statistics#collect-statistics-on-some-columns">Ignoring unnecessary columns when collecting statistics</a></td>
    <td>Under the premise of ensuring that the optimizer can obtain the necessary information, TiDB speeds up statistics collection, improves the timeliness of statistics, and thus ensures that the optimal execution plan is selected, improving the performance of the cluster. Meanwhile, TiDB also reduces the system overhead and improves the resource utilization.</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/tiproxy-overview">Built-in virtual IP management in TiProxy</a></td>
    <td>TiProxy introduces built-in virtual IP management. When configured, it supports automatic virtual IP switching without relying on external platforms or tools. This feature simplifies TiProxy deployment and reduces the complexity of the database access layer.</td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

* The optimizer allows pushing the `Projection` operator down to the storage engine by default [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87)

    Pushing the `Projection` operator down to the storage engine reduces data transfer between the compute engine and the storage engine, thereby improving SQL execution performance. This is particularly effective for queries containing [JSON query functions](/functions-and-operators/json-functions/json-functions-search.md) or [JSON value attribute functions](/functions-and-operators/json-functions/json-functions-return.md). Starting from v8.3.0, TiDB enables the `Projection` operator pushdown feature by default, by changing the default value of the system variable controlling this feature, [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610), from `OFF` to `ON`. When this feature is enabled, the optimizer automatically pushes eligible JSON query functions and JSON value attribute functions down to the storage engine.

    For more information, see [documentation](/system-variables.md#tidb_opt_projection_push_down-new-in-v610).

* Optimize batch processing strategy for KV (key-value) requests [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan)

    TiDB fetches data by sending KV requests to TiKV. Batching and processing KV requests in bulk can significantly improve execution performance. Before v8.3.0, the batching strategy in TiDB is less efficient. Starting from v8.3.0, TiDB introduces several more efficient batching strategies in addition to the existing one. You can configure different batching strategies using the [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830) configuration item to accommodate various workloads.

    For more information, see [documentation](/tidb-configuration-file.md#batch-policy-new-in-v830).
    
* TiFlash introduces HashAgg aggregation calculation modes to improve the performance for high NDV data [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge)

    Before v8.3.0, TiFlash has low aggregation calculation efficiency during the first stage of HashAgg aggregation when handling data with high NDV (number of distinct values). Starting from v8.3.0, TiFlash introduces multiple HashAgg aggregation calculation modes to improve the aggregation performance for different data characteristics. To choose a desired HashAgg aggregation calculation mode, you can configure the [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) system variable.

    For more information, see [documentation](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830).

* Ignore unnecessary columns when collecting statistics [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)

    When the optimizer generates an execution plan, it only needs statistics for some columns, such as columns in the filter conditions, columns in the join keys, and columns used for aggregation. Starting from v8.3.0, TiDB continuously observes the historical records of the columns used in SQL statements. By default, TiDB only collects statistics for columns with indexes and columns that are observed to require statistics collection. This speeds up the collection of statistics and avoids unnecessary resource consumption.

    When you upgrade your cluster from a version earlier than v8.3.0 to v8.3.0 or later, TiDB retains the original behavior by default, that is, collecting statistics for all columns. To enable this feature, you need to manually set the system variable [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to `PREDICATE`. For newly deployed clusters, this feature is enabled by default.

    For analytical systems with many random queries, you can set the system variable [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to `ALL` to collect statistics for all columns, to ensure the performance of random queries. For other types of systems, it is recommended to keep the default setting (`PREDICATE`) of [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to collect statistics for only necessary columns.

    For more information, see [documentation](/statistics.md#collect-statistics-on-some-columns).

* Improve the query performance of some system tables [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)

    In previous versions, querying system tables has poor performance when the cluster size becomes large and there are a large number of tables.

    In v8.0.0, query performance is optimized for the following four system tables:

    - `INFORMATION_SCHEMA.TABLES`
    - `INFORMATION_SCHEMA.STATISTICS`
    - `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`
    - `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`

  In v8.3.0, the query performance is optimized for the following system tables, bringing a multi-fold performance improvement compared to v8.2.0.

    - `INFORMATION_SCHEMA.CHECK_CONSTRAINTS`
    - `INFORMATION_SCHEMA.COLUMNS`
    - `INFORMATION_SCHEMA.PARTITIONS`
    - `INFORMATION_SCHEMA.SCHEMATA`
    - `INFORMATION_SCHEMA.SEQUENCES`
    - `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`
    - `INFORMATION_SCHEMA.TIDB_CHECK_CONSTRAINTS`
    - `INFORMATION_SCHEMA.TiDB_INDEXES`
    - `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`
    - `INFORMATION_SCHEMA.VIEWS`

* Support partition pruning when partition expressions use the `EXTRACT(YEAR_MONTH...)` function to improve query performance [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss)

    In previous versions, when partition expressions use the `EXTRACT(YEAR_MONTH...)` function, partition pruning is not supported, resulting in poor query performance. Starting from v8.3.0, partition pruning is supported when partition expressions use the `EXTRACT(YEAR_MONTH...)` function, which improves query performance.

    For more information, see [documentation](/partition-pruning.md#scenario-three).

* Improve the performance of `CREATE TABLE` by 1.4 times, `CREATE DATABASE` by 2.1 times, and `ADD COLUMN` by 2 times [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter)

    TiDB v8.0.0 introduces the system variable [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) to improve table creation performance in batch table creation scenarios. In v8.3.0, when submitting the DDL statements for table creation concurrently through 10 sessions in a single database, the performance is improved by 1.4 times compared with v8.2.0.

    In v8.3.0, the performance of general DDLs in batch execution has improved compared to v8.2.0. The performance of `CREATE DATABASE` for 10 sessions concurrently improves by 19 times compared with v8.1.0 and 2.1 times compared with v8.2.0. The performance of using 10 sessions to add columns (`ADD COLUMN`) to multiple tables in the same database in batch has improved by 10 times compared with v8.1.0, and 2.1 times compared with v8.2.0. The performance of `ADD COLUMN` with 10 sessions on multiple tables in the same database has improved by 10 times compared with v8.1.0 and 2 times compared with v8.2.0.

    For more information, see [documentation](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

* Partitioned tables support global indexes (experimental) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple)

    In previous versions of partitioned tables, some limitations exist because global indexes are not supported. For example, the unique key must use every column in the table's partitioning expression. If the query condition does not use the partitioning key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.

    Starting with v8.3.0, the global index feature is released as an experimental feature. You can explicitly create a global index for a partitioned table with the keyword `Global` to remove the restriction that the unique key must use every column in the table's partitioning expression, to meet flexible business needs. Global indexes also enhance the performance of queries that do not include partition keys.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

### Reliability

* Support streaming cursor result sets (experimental) [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao)

    When the application code retrieves the result set using [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result), TiDB usually first stores the complete result set in memory, and then returns the data to the client in batches. If the result set is too large, TiDB might temporarily write the result to the hard disk.

    Starting from v8.3.0, if you set the system variable [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) to `ON`, TiDB no longer reads all data to the TiDB node, but gradually reads data to the TiDB node as the client reads. When TiDB processes large result sets, this feature reduces the memory usage of the TiDB node and improves the stability of the cluster.

    For more information, see [documentation](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830).

* Enhance SQL execution plan binding [#55280](https://github.com/pingcap/tidb/issues/55280) [#55343](https://github.com/pingcap/tidb/issues/55343) @[time-and-fate](https://github.com/time-and-fate)

    In OLTP scenarios, the optimal execution plan for most SQL statements is fixed. Implementing SQL execution plan binding for important SQL statements in the application can reduce the probability of the execution plan becoming worse and improve system stability. To meet the requirements of creating a large number of SQL execution plan bindings, TiDB enhances the capability and experience of SQL binding, including:

    - Use a single SQL statement to create SQL execution plan bindings from multiple historical execution plans to improve the efficiency of creating bindings.
    - The SQL execution plan binding supports more optimizer hints, and optimizes the conversion method for complex execution plans, making the binding more stable in restoring the execution plan.

  For more information, see [documentation](/sql-plan-management.md).

### Availability

* TiProxy supports built-in virtual IP management [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832)

    Before v8.3.0, when using primary-secondary mode for high availability, TiProxy requires an additional component to manage the virtual IP address. Starting from v8.3.0, TiProxy supports built-in virtual IP management. In primary-secondary mode, when a primary node fails over, the new primary node will automatically bind to the specified virtual IP, ensuring that clients can always connect to an available TiProxy through the virtual IP.

    To enable virtual IP management, specify the virtual IP address using the TiProxy configuration item [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) and specify the network interface to bind the virtual IP to using [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface). The virtual IP will be bound to a TiProxy instance only when both of these configuration items are set.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB does not support `SELECT LOCK IN SHARE MODE` yet. Starting from v8.3.0, TiDB supports upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks to enable support for `SELECT LOCK IN SHARE MODE`. You can control whether to enable this feature by using the new system variable [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

    For more information, see [documentation](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

### Observability

* Show the progress of loading initial statistics [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei)

    TiDB loads basic statistics when it starts. In scenarios with many tables or partitions, this process can take a long time. When the configuration item [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) is set to `ON`, TiDB does not provide services until the initial statistics are loaded. In this case, you need to observe the loading process to estimate the service start time.

    Starting from v8.3.0, TiDB prints the progress of loading initial statistics in stages in the log, so you can understand the running status. To provide formatted results to external tools, TiDB adds the additional [monitoring API](/tidb-monitoring-api.md) so you can obtain the progress of loading initial statistics at any time during the startup phase.

* Add metrics about Request Unit (RU) settings [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

### Security

* Enhance PD log redaction [#8305](https://github.com/tikv/pd/issues/8305) @[JmPotato](https://github.com/JmPotato)

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with `‹ ›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.

    In v8.3.0, PD implements a similar log redaction enhancement. To use this feature, you can set the value of the PD configuration item `security.redact-info-log` to `"marker"`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-pd-side).

* Enhance TiKV log redaction [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator)

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with `‹ ›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.

    In v8.3.0, TiKV implements a similar log redaction enhancement. To use this feature, you can set the value of the TiKV configuration item `security.redact-info-log` to `"marker"`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-tikv-side).

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen)

    TiCDC v7.6.0 introduced the replication of DDL statements with bi-directional replication configured. Previously, bi-directional replication of DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to execute DDL statements on both TiDB clusters separately. With this feature, after assigning a `PRIMARY` BDR role to a cluster, TiCDC can replicate the DDL statements from that cluster to the `SECONDARY` cluster.

    In v8.3.0, this feature becomes generally available (GA).

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.2.0 to the current version (v8.3.0). If you are upgrading from v8.1.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* To avoid incorrect use of commands, `pd-ctl` cancels the prefix matching mechanism. For example, `store remove-tombstone` cannot be called via `store remove` [#8413](https://github.com/tikv/pd/issues/8413) @[lhy1024](https://github.com/lhy1024)

### System variables

| Variable name  | Change type   | Description |
|--------|------------------------------|------|
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)    | Modified   | Adds the SESSION scope.       |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)  | Modified   | Adds the SESSION scope.    |
| [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540) | Modified | Changes the default value from `OFF` to `ON` after further tests, which means that TiDB collects `PREDICATE COLUMNS` by default. |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) | Modified | Starting from v8.3.0, this variable controls the number of concurrent threads during the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) and [Delete Range](/garbage-collection-overview.md#delete-ranges) steps of the [Garbage Collection (GC)](/garbage-collection-overview.md) process. Before v8.3.0, this variable only controls the number of threads during the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step. |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) | Modified | Adds the GLOBAL scope. |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610) | Modified | Adds the GLOBAL scope and persists the variable value to the cluster. Changes the default value from `OFF` to `ON` after further tests, which means that the optimizer is allowed to push `Projection` down to the TiKV coprocessor. |
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800)    | Modified | The range of values has been modified to either `0` or `[536870912, 9223372036854775807]`. The minimum value is `536870912` bytes (that is, 512 MiB) to avoid setting a cache size that is too small and causing performance degradation. |
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) | Newly added | Controls the behavior of the `ANALYZE TABLE` statement. Setting it to the default value `PREDICATE` means only collecting statistics for [predicate columns](/statistics.md#collect-statistics-on-some-columns); setting it to `ALL` means collecting statistics for all columns. |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) | Newly added | Controls the behavior of the [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) feature. |
| [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830)       | Newly added  | Controls whether to enable the feature of upgrading shared locks to exclusive locks. The default value of this variable is `OFF`, which means that the function of upgrading shared locks to exclusive locks is disabled. |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) | Newly added | Controls the pre-aggregation strategy used during the first stage of two-stage or three-stage HashAgg operations pushed down to TiFlash. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830) | Newly added | Controls the batching strategy for requests from TiDB to TiKV. |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50) |  Modified | Support setting the value of the PD configuration item `security.redact-info-log` to `"marker"` to mark sensitive information in the log with `‹ ›` instead of shielding it directly. With the `"marker"` option, you can customize the redaction rules.  |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)  | Modified | Support setting the value of the TiKV configuration item `security.redact-info-log` to `"marker"` to mark sensitive information in the log with `‹ ›` instead of shielding it directly. With the `"marker"` option, you can customize the redaction rules.  |
| TiFlash   | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Modified |  Support setting the value of the TiFlash Learner configuration item `security.redact-info-log` to `"marker"` to mark sensitive information in the log with `‹ ›` instead of shielding it directly. With the `"marker"` option, you can customize the redaction rules.  |
| BR  | [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#limitations) | Newly added  | Controls whether incremental backups are compatible with subsequent log backups. The default value is `true`, which means that incremental backups are compatible with subsequent log backups. When you keep the default value `true`, the DDLs that need to be replayed are strictly checked before the incremental restore begins. |

### System tables

* The [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) and [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) system tables add the `SESSION_ALIAS` field to show the number of rows currently affected by the DML statement [#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao)

## Deprecated features

* The following features are deprecated starting from v8.3.0:

    * Starting from v7.5.0, [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) replication is deprecated. Starting from v8.3.0, TiDB Binlog is fully deprecated, with removal planned for a future release. For incremental data replication, use [TiCDC](/ticdc/ticdc-overview.md) instead. For point-in-time recovery (PITR), use [PITR](/br/br-pitr-guide.md).
    * Starting from v8.3.0, the [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540) system variable is deprecated. TiDB tracks predicate columns by default. For more information, see [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830).

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.       
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB

    - Support the `SELECT ... STRAIGHT_JOIN ... USING ( ... )` statement [#54162](https://github.com/pingcap/tidb/issues/54162) @[dveeden](https://github.com/dveeden)
    - Construct more precise index access ranges for filter conditions like `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))` [#54337](https://github.com/pingcap/tidb/issues/54337) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - Use index order to avoid extra sorting operations for SQL queries like `WHERE idx_col_1 IS NULL ORDER BY idx_col_2` [#54188](https://github.com/pingcap/tidb/issues/54188) @[ari-e](https://github.com/ari-e)
    - Display analyzed indexes in the `mysql.analyze_jobs` system table [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)
    - Support applying the `tidb_redact_log` setting to the output of `EXPLAIN` statements and further optimize the logic in processing logs [#54565](https://github.com/pingcap/tidb/issues/54565) @[hawkingrei](https://github.com/hawkingrei)
    - Support generating the `Selection` operator on `IndexRangeScan` for multi-valued indexes to improve query efficiency [#54876](https://github.com/pingcap/tidb/issues/54876) @[time-and-fate](https://github.com/time-and-fate)
    - Support killing automatic `ANALYZE` tasks that are running outside the set time window [#55283](https://github.com/pingcap/tidb/issues/55283) @[hawkingrei](https://github.com/hawkingrei)
    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - The TopN operator supports disk spill [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - TiDB node supports executing queries with the `WITH ROLLUP` modifier and the `GROUPING` function [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx)
    - The system variable [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) supports the `GLOBAL` scope [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk)
    - Improve GC (Garbage Collection) efficiency by supporting concurrent range deletion. You can control the number of concurrent threads using [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium)
    - Improve the performance of bulk DML execution mode (`tidb_dml_type = "bulk"`) [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    - Improve the performance of schema information cache-related interface `SchemaByID` [#54074](https://github.com/pingcap/tidb/issues/54074) @[ywqzzy](https://github.com/ywqzzy)
    - Improve the query performance for certain system tables when schema information caching is enabled [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)
    - Optimize error messages for conflicting keys when adding unique indexes [#53004](https://github.com/pingcap/tidb/issues/53004) @[lance6716](https://github.com/lance6716)

+ PD

    - Support modifying the `batch` configuration of the `evict-leader-scheduler` via `pd-ctl` to accelerate the leader eviction process [#8265](https://github.com/tikv/pd/issues/8265) @[rleungx](https://github.com/rleungx)
    - Add the `store_id` monitoring metric to the **Cluster > Label distribution** panel in Grafana to display store IDs corresponding to different labels [#8337](https://github.com/tikv/pd/issues/8337) @[HuSharp](https://github.com/HuSharp)
    - Support fallback to the default resource group when the specified resource group does not exist [#8388](https://github.com/tikv/pd/issues/8388) @[JmPotato](https://github.com/JmPotato)
    - Add the `approximate_kv_size` field to the Region information output by the `region` command in `pd-ctl` [#8412](https://github.com/tikv/pd/issues/8412) @[zeminzhou](https://github.com/zeminzhou)
    - Optimize the message that returns when you call the PD API to delete the TTL configuration [#8450](https://github.com/tikv/pd/issues/8450) @[lhy1024](https://github.com/lhy1024)
    - Optimize the RU consumption behavior of large query read requests to reduce the impact on other requests [#8457](https://github.com/tikv/pd/issues/8457) @[nolouch](https://github.com/nolouch)
    - Optimize the error message that returns when you misconfigure PD microservices [#52912](https://github.com/pingcap/tidb/issues/52912) @[rleungx](https://github.com/rleungx)
    - Add the `--name` startup parameter to PD microservices to more accurately display the service name during deployment [#7995](https://github.com/tikv/pd/issues/7995) @[HuSharp](https://github.com/HuSharp)
    - Support dynamically adjusting `PatrolRegionScanLimit` based on the number of Regions to reduce Region scan time [#7963](https://github.com/tikv/pd/issues/7963) @[lhy1024](https://github.com/lhy1024)

+ TiKV

    - Optimize the batching policy for writing Raft logs when `async-io` is enabled to reduce the consumption of disk I/O bandwidth resources [#16907](https://github.com/tikv/tikv/issues/16907) @[LykxSassinator](https://github.com/LykxSassinator)
    - Redesign the TiCDC delegate and downstream modules to better support Region partial subscription [#16362](https://github.com/tikv/tikv/issues/16362) @[hicqu](https://github.com/hicqu)
    - Reduce the size of a single slow query log [#17294](https://github.com/tikv/tikv/issues/17294) @[Connor1996](https://github.com/Connor1996)
    - Add a new monitoring metric `min safe ts` [#17307](https://github.com/tikv/tikv/issues/17307) @[mittalrishabh](https://github.com/mittalrishabh)
    - Reduce the memory usage of the peer message channel [#16229](https://github.com/tikv/tikv/issues/16229) @[Connor1996](https://github.com/Connor1996)

+ TiFlash

    - Support generating ad hoc heap profiling in SVG format [#9320](https://github.com/pingcap/tiflash/issues/9320) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR)

        - Support checking whether a full backup exists before starting point-in-time recovery (PITR) for the first time. If the full backup is not found, BR terminates the restore and returns an error [#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth)
        - Support checking whether the disk space in TiKV and TiFlash is sufficient before restoring snapshot backups. If the space is insufficient, BR terminates the restore and returns an error [#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR)
        - Support checking whether the disk space in TiKV is sufficient before TiKV downloads each SST file. If the space is insufficient, BR terminates the restore and returns an error [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)
        - Support setting Alibaba Cloud access credentials through environment variables [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - Automatically set the environment variable `GOMEMLIMIT` based on the available memory of the BR process to avoid OOM when using BR for backup and restore [#53777](https://github.com/pingcap/tidb/issues/53777) @[Leavrth](https://github.com/Leavrth)
        - Make incremental backups compatible with point-in-time recovery (PITR) [#54474](https://github.com/pingcap/tidb/issues/54474) @[3pointer](https://github.com/3pointer)
        - Support backing up and restoring the `mysql.column_stats_usage` table [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/Rustin170506)

## Bug fixes

+ TiDB

    - Reset the parameters in the `Open` method of `PipelinedWindow` to fix the unexpected error that occurs when the `PipelinedWindow` is used as a child node of `Apply` due to the reuse of previous parameter values caused by repeated opening and closing operations [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the query might get stuck when terminated because the memory usage exceeds the limit set by `tidb_mem_quota_query` [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the disk spill for the HashAgg operator causes incorrect query results during parallel calculation [#55290](https://github.com/pingcap/tidb/issues/55290) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue of wrong `JSON_TYPE` when casting `YEAR` to JSON format [#54494](https://github.com/pingcap/tidb/issues/54494) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the value range of the `tidb_schema_cache_size` system variable is wrong [#54034](https://github.com/pingcap/tidb/issues/54034) @[lilinghai](https://github.com/lilinghai)
    - Fix the issue that partition pruning does not work when the partition expression is `EXTRACT(YEAR FROM col)` [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    - Fix the issue that `FLASHBACK DATABASE` fails when many tables exist in the database [#54415](https://github.com/pingcap/tidb/issues/54415) @[lance6716](https://github.com/lance6716)
    - Fix the issue that `FLASHBACK DATABASE` enters an infinite loop when handling many databases [#54915](https://github.com/pingcap/tidb/issues/54915) @[lance6716](https://github.com/lance6716)
    - Fix the issue that adding an index in index acceleration mode might fail [#54568](https://github.com/pingcap/tidb/issues/54568) @[lance6716](https://github.com/lance6716)
    - Fix the issue that `ADMIN CANCEL DDL JOBS` might cause DDL to fail [#54687](https://github.com/pingcap/tidb/issues/54687) @[lance6716](https://github.com/lance6716)
    - Fix the issue that table replication fails when the index length of the table replicated from DM exceeds the maximum length specified by `max-index-length` [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the error `runtime error: index out of range` might occur when executing SQL statements with `tidb_enable_inl_join_inner_multi_pattern` enabled [#54535](https://github.com/pingcap/tidb/issues/54535) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that you cannot exit TiDB using <kbd>Control</kbd>+<kbd>C</kbd> during the process of initializing statistics [#54589](https://github.com/pingcap/tidb/issues/54589) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `INL_MERGE_JOIN` optimizer hint returns incorrect results by deprecating it [#54064](https://github.com/pingcap/tidb/issues/54064) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that a correlated subquery that contains `WITH ROLLUP` might cause TiDB to panic and return the error `runtime error: index out of range` [#54983](https://github.com/pingcap/tidb/issues/54983) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that predicates cannot be pushed down properly when the filter condition of a SQL query contains virtual columns and the execution condition contains `UnionScan` [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the error `runtime error: invalid memory address or nil pointer dereference` might occur when executing SQL statements with `tidb_enable_inl_join_inner_multi_pattern` enabled [#55169](https://github.com/pingcap/tidb/issues/55169) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a query statement that contains `UNION` might return incorrect results [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the `tot_col_size` column in the `mysql.stats_histograms` table might be a negative number [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `columnEvaluator` cannot identify the column references in the input chunk, which leads to `runtime error: index out of range` when executing SQL statements [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `STATS_EXTENDED` becomes a reserved keyword [#39573](https://github.com/pingcap/tidb/issues/39573) @[wddevries](https://github.com/wddevries)
    - Fix the issue that when `tidb_low_resolution` is enabled, `select for update` can be executed [#54684](https://github.com/pingcap/tidb/issues/54684) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that internal SQL queries cannot be displayed in the slow query log when `tidb_redact_log` is enabled [#54190](https://github.com/pingcap/tidb/issues/54190) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the memory used by transactions might be tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - Fix the issue that using `SHOW WARNINGS;` to obtain warnings might cause a panic [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - Fix the issue that loading index statistics might cause memory leaks [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that the `LENGTH()` condition is unexpectedly removed when the collation is `utf8_bin` or `utf8mb4_bin` [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that statistics collection does not update the `stats_history` table when encountering duplicate primary keys [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the Connection Count monitoring metric in Grafana is incorrect when some connections exit before the handshake is complete [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the Connection Count of each resource group is incorrect when using TiProxy and resource groups [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when queries contain non-correlated subqueries and `LIMIT` clauses, column pruning might be incomplete, resulting in a less optimal plan [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - Fix the issue of reusing wrong point get plans for `SELECT ... FOR UPDATE` [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that internal SQL statements in the slow log are redacted to null by default [#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that `PointGet` execution plans for `_tidb_rowid` can be generated [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `SHOW IMPORT JOBS` reports an error `Unknown column 'summary'` after upgrading from v7.1 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    - Fix the issue that obtaining the column information using `information_schema.columns` returns warning 1356 when a subquery is used as a column definition in a view definition [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - Fix the issue that RANGE partitioned tables that are not strictly self-incrementing can be created [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `INDEX_HASH_JOIN` cannot exit properly when SQL is abnormally interrupted [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the network partition during adding indexes using the Distributed eXecution Framework (DXF) might cause inconsistent data indexes [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)

+ PD

    - Fix the issue that no error is reported when binding a role to a resource group [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that a resource group encounters quota limits when requesting tokens for more than 500 ms [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the time data type in the `INFORMATION_SCHEMA.RUNAWAY_WATCHES` table is incorrect [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that resource groups could not effectively limit resource usage under high concurrency [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - Fix the issue that an incorrect PD API is called when you retrieve table attributes [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the scaling progress is displayed incorrectly after the `scheduling` microservice is enabled [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the encryption manager is not initialized before use [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - Fix the issue that some logs are not redacted [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - Fix the issue that redirection might panic during the startup of PD microservices [#8406](https://github.com/tikv/pd/issues/8406) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the `split-merge-interval` configuration item might not take effect when you modify its value repeatedly (such as changing it from `1s` to `1h` and back to `1s`) [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that setting `replication.strictly-match-label` to `true` causes TiFlash to fail to start [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - Fix the issue that fetching TSO is slow when analyzing large partitioned tables, causing `ANALYZE` performance degradation [#8500](https://github.com/tikv/pd/issues/8500) @[rleungx](https://github.com/rleungx)
    - Fix the potential data races in large clusters [#8386](https://github.com/tikv/pd/issues/8386) @[rleungx](https://github.com/rleungx)
    - Fix the issue that when determining whether queries are Runaway Queries, TiDB only counts time consumption spent on the Coprocessor side while missing time consumption spent on the TiDB side, resulting in some queries not being identified as Runaway Queries [#51325](https://github.com/pingcap/tidb/issues/51325) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - Fix the issue that TiFlash might panic after executing `RENAME TABLE ... TO ...` on a partitioned table with empty partitions across databases [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that some queries might report a column type mismatch error after late materialization is enabled [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that queries with virtual generated columns might return incorrect results after late materialization is enabled [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might panic when a database is deleted shortly after creation [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a network partition (network disconnection) between TiFlash and any PD might cause read request timeout errors [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash write nodes might fail to restart in the disaggregated storage and compute architecture [#9282](https://github.com/pingcap/tiflash/issues/9282) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that read snapshots of TiFlash write nodes are not released in a timely manner in the disaggregated storage and compute architecture [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)

+ TiKV

    - Fix the issue that cleaning up stale regions might accidentally delete valid data [#17258](https://github.com/tikv/tikv/issues/17258) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that `Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the TiKV dashboard in Grafana [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that `cancel_generating_snap` incorrectly updating `snap_tried_cnt` causes TiKV to panic [#17226](https://github.com/tikv/tikv/issues/17226) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that the information of `Ingest SST duration seconds` is incorrect [#17239](https://github.com/tikv/tikv/issues/17239) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that CPU profiling flag is not reset correctly when an error occurs [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that bloom filters are incompatible between earlier versions (earlier than v7.1) and later versions [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the progress is stuck during backup and restore [#54140](https://github.com/pingcap/tidb/issues/54140) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the checkpoint path of backup and restore is incompatible with some external storage [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that the processor might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Fix the issue that schema tracker incorrectly handles LIST partition tables, causing DM errors [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - Fix the issue that data replication is interrupted when the index length exceeds the default value of `max-index-length` [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - Fix the issue that DM cannot handle `FAKE_ROTATE_EVENT` correctly [#11381](https://github.com/pingcap/tiflow/issues/11381) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning outputs a confusing `WARN` log when it fails to obtain the keyspace name [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the TLS configuration of TiDB Lightning affects cluster certificates [#54172](https://github.com/pingcap/tidb/issues/54172) @[ei-sugimoto](https://github.com/ei-sugimoto)
        - Fix the issue that transaction conflicts occur during data import using TiDB Lightning [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - Fix the issue that large checkpoint files cause performance degradation during the import of numerous databases and tables [#55054](https://github.com/pingcap/tidb/issues/55054) @[D3Hunter](https://github.com/D3Hunter)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [ari-e](https://github.com/ari-e)
- [ei-sugimoto](https://github.com/ei-sugimoto)
- [HaoW30](https://github.com/HaoW30)
- [JackL9u](https://github.com/JackL9u)
- [michaelmdeng](https://github.com/michaelmdeng)
- [mittalrishabh](https://github.com/mittalrishabh)
- [qingfeng777](https://github.com/qingfeng777)
- [SandeepPadhi](https://github.com/SandeepPadhi)
- [yzhan1](https://github.com/yzhan1)
