---
title: TiDB 8.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.3.0.
---

# TiDB 8.3.0 Release Notes

Release date: xx xx, 2024

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
    <td> <a href="https://docs.pingcap.com/tidb/v8.3/partitioned-table#global-indexes">Global indexes for partitioned tables (experimental)</a></td> **tw@hfxsd** <!--1531-->
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned keys, and remove the restriction that partitioned keys must contain a unique key. This feature extends the usage scenarios of TiDB partitioned tables and avoids some of the application modification work that might be required for data migration.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/system-variables#tidb_opt_projection_push_down-new-in-v610">Default pushdown of the <code>Projection</code> operator to the storage engine</a></td>**tw@Oreoxmt** <!--1872-->
    <td>Pushing the <code>Projection</code> operator down to the storage engine can distribute the load across storage nodes while reducing data transfer between nodes. This optimization helps to reduce the execution time for certain SQL queries and improves the overall database performance.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/statistics#collect-statistics-on-some-columns">Ignoring unnecessary columns when collecting statistics</a></td>**tw@lilin90** <!--1753-->
    <td>Under the premise of ensuring that the optimizer can obtain the necessary information, TiDB speeds up statistics collection, improves the timeliness of statistics, and thus ensures that the optimal execution plan is selected, improving the performance of the cluster. Meanwhile, TiDB also reduces the system overhead and improves the resource utilization.</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v8.3/tiproxy-overview">Built-in virtual IP management in TiProxy</a></td>**tw@Oreoxmt** <!--1887-->
    <td>TiProxy introduces built-in virtual IP management. When configured, it supports automatic virtual IP switching without relying on external platforms or tools. This feature simplifies TiProxy deployment and reduces the complexity of the database access layer.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability


### Performance

* The optimizer allows pushing the `Projection` operator down to the storage engine by default [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--1872-->

    Pushing the `Projection` operator down to the storage engine reduces data transfer between the compute engine and the storage engine, thereby improving SQL execution performance. This is particularly effective for queries containing [JSON query functions](/functions-and-operators/json-functions/json-functions-search.md) or [JSON value attribute functions](/functions-and-operators/json-functions/json-functions-return.md). Starting from v8.3.0, TiDB enables the `Projection` operator pushdown feature by default, by changing the default value of the system variable controlling this feature, [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610), from `OFF` to `ON`. When this feature is enabled, the optimizer automatically pushes eligible JSON query functions and JSON value attribute functions down to the storage engine.

    For more information, see [documentation](/system-variables.md#tidb_opt_projection_push_down-new-in-v610).

* Optimize batch processing strategy for KV (key-value) requests [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1897-->

    TiDB fetches data by sending KV requests to TiKV. Batching and processing KV requests in bulk can significantly improve execution performance. Before v8.3.0, the batching strategy in TiDB is less efficient. Starting from v8.3.0, TiDB introduces several more efficient batching strategies in addition to the existing one. You can configure different batching strategies using the [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830) configuration item to accommodate various workloads.

    For more information, see [documentation](/tidb-configuration-file.md#batch-policy-new-in-v830).
    
* TiFlash introduces HashAgg aggregation calculation modes to improve the performance for high NDV data [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1855-->

    Before v8.3.0, TiFlash has low aggregation calculation efficiency during the first stage of HashAgg aggregation when handling data with high NDV (number of distinct values). Starting from v8.3.0, TiFlash introduces multiple HashAgg aggregation calculation modes to improve the aggregation performance for different data characteristics. To choose a desired HashAgg aggregation calculation mode, you can configure the [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) system variable.

    For more information, see [documentation](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830).

* Ignore unnecessary columns when collecting statistics [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin) **tw@lilin90** <!--1753-->

    When the optimizer generates an execution plan, it only needs statistics for some columns, such as columns in the filter conditions, columns in the join keys, and columns used for aggregation. Starting from v8.3.0, TiDB continuously observes the historical records of the columns used in SQL statements. By default, TiDB only collects statistics for columns with indexes and columns that are observed to require statistics collection. This speeds up the collection of statistics and avoids unnecessary resource consumption.

    When you upgrade your cluster from a version earlier than v8.3.0 to v8.3.0 or later, TiDB retains the original behavior by default, that is, collecting statistics for all columns. To enable this feature, you need to manually set the system variable [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to `PREDICATE`. For newly deployed clusters, this feature is enabled by default.

    For analytical systems with many random queries, you can set the system variable [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to `ALL` to collect statistics for all columns, to ensure the performance of random queries. For other types of systems, it is recommended to keep the default setting (`PREDICATE`) of [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-new-in-v830) to collect statistics for only necessary columns.

    For more information, see [documentation](/statistics.md#collect-statistics-on-some-columns).

* Improve the query performance of some system tables [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta) **tw@hfxsd** <!--1865-->

    In previous versions, querying system tables has slow performance when the cluster size becomes large and there are a large number of tables.

    In v8.0.0, query performance is optimized for the following four system tables.
    
    - INFORMATION_SCHEMA.TABLES
    - INFORMATION_SCHEMA.STATISTICS
    - INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    - INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS

    The following query performance of system tables has been optimized in v8.3.0, resulting in a multi-fold performance improvement compared to v8.2.0.

    - INFORMATION_SCHEMA.CHECK_CONSTRAINTS
    - INFORMATION_SCHEMA.COLUMNS
    - INFORMATION_SCHEMA.PARTITIONS
    - INFORMATION_SCHEMA.SCHEMATA
    - INFORMATION_SCHEMA.SEQUENCES
    - INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    - INFORMATION_SCHEMA.TIDB_CHECK_CONSTRAINTS
    - INFORMATION_SCHEMA.TiDB_INDEXES
    - INFORMATION_SCHEMA.TIDB_INDEX_USAGE
    - INFORMATION_SCHEMA.VIEWS

* Support for partition pruning when partition expressions use the `EXTRACT(YEAR_MONTH...)` function to improve query performance [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1885-->

    In previous versions, when partition expressions use the `EXTRACT(YEAR_MONTH...)` function, partition pruning is not supported, resulting in poor query performance. Starting from v8.3.0, partition pruning is supported when partition expressions use the `EXTRACT(YEAR_MONTH...)` function, which improves query performance.

    For more information, see [documentation](/partition-pruning.md#scenario-three).
    
* The performance of `CREATE TABLE` is improved by 1.4 times, `CREATE DATABASE` by 2.1 times, and `ADD COLUMN` by 2 times [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1863-->

    TiDB v8.0.0 introduces the system variable [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) to improve table creation performance in batch table creation scenarios. In v8.3.0, when submitting the DDL statements for table creation concurrently through 10 sessions in a single database, the performance is improved by 1.4 times compared with v8.2.0.
   
    In v8.3.0, the performance of general DDLs in batch execution has improved compared to v8.2.0. The performance of `CREATE DATABASE` for 10 sessions concurrently improves by 19 times compared with v8.1.0 and 2.1 times compared with v8.2.0. The performance of using 10 sessions to add columns (`ADD COLUMN`) to multiple tables in the same database in batch has improved by 10 times compared with v8.1.0, and 2.1 times compared with v8.2.0. The performance of `ADD COLUMN` with 10 sessions on multiple tables in the same database has improved by 10 times compared with v8.1.0 and 2 times compared with v8.2.0.

    For more information, see [documentation](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).    

* Partitioned tables support global indexes (experimental) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    In previous versions of partitioned tables, there are some limitations because global indexes are not supported. For example, the unique key must use every column in the table's partitioning expression. If the query condition does not use every column, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.
    
    Starting with v8.3.0, the global index feature is released as an experimental feature. You can explicitly create a global index for a partitioned table with the keyword `Global` to remove the restriction that the unique key must use every column in the table's partitioning expression, to meet flexible business needs. Global indexes also improve the query performance of unique indexes without partition keys.

    For more information, see [documentation](/partitioned-table.md#global-indexes).
 
### Reliability

* Support streaming cursor result sets (experimental) [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1891-->

    When the application code retrieves the result set using [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result), TiDB usually first stores the complete result set in memory, and then returns the data to the client in batches. If the result set is too large, TiDB might temporarily write the result to the hard disk.

    Starting from v8.3.0, if you set the system variable [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) to `ON`, TiDB no longer reads all data to the TiDB node, but gradually reads data to the TiDB node as the client reads. When TiDB processes large result sets, this feature reduces the memory usage of the TiDB node and improves the stability of the cluster.

    For more information, see [documentation](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830).

* Enhance SQL execution plan binding [#55280](https://github.com/pingcap/tidb/issues/55280) [#55343](https://github.com/pingcap/tidb/issues/55343) @[time-and-fate](https://github.com/time-and-fate) **tw@lilin90** <!--1760-->

    In OLTP scenarios, the optimal execution plan for most SQL statements is fixed. Implementing SQL execution plan binding for important SQL statements in the application can reduce the probability of the execution plan becoming worse and improve system stability. To meet the requirements of creating a large number of SQL execution plan bindings, TiDB enhances the capability and experience of SQL binding, including:

    - Use a single SQL statement to create SQL execution plan bindings from multiple historical execution plans to improve the efficiency of creating bindings.
    - The SQL execution plan binding supports more optimizer hints, and optimizes the conversion method for complex execution plans, making the binding more stable in restoring the execution plan.

  For more information, see [documentation](/sql-plan-management.md).

### Availability

* TiProxy supports built-in virtual IP management [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    Before v8.3.0, when using primary-secondary mode for high availability, TiProxy requires an additional component to manage the virtual IP address. Starting from v8.3.0, TiProxy supports built-in virtual IP management. In primary-secondary mode, when a primary node fails over, the new primary node will automatically bind to the specified virtual IP, ensuring that clients can always connect to an available TiProxy through the virtual IP.

    To enable virtual IP management, specify the virtual IP address using the TiProxy configuration item [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) and specify the network interface to bind the virtual IP to using [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface). The virtual IP will be bound to a TiProxy instance only when both of these configuration items are set.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1871-->

    TiDB does not support `SELECT LOCK IN SHARE MODE` yet. Starting from v8.3.0, TiDB supports upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks to enable support for `SELECT LOCK IN SHARE MODE`. You can control whether to enable this feature by the new variable [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

    For more information, see [documentation](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

### DB operations

### Observability

* Show the progress of loading initial statistics [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB loads basic statistics when it starts. In scenarios with many tables or partitions, this process can take a long time. When the configuration item [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) is set to `ON`, TiDB does not provide services until the initial statistics are loaded. In this case, you need to observe the loading process to estimate the service start time.

    Starting from v8.3.0, TiDB prints the progress of loading initial statistics in stages in the log, so you can understand the running status. To provide formatted results to external tools, TiDB adds the additional [monitoring API](/tidb-monitoring-api.md) so you can obtain the progress of loading initial statistics at any time during the startup phase.

* Display metrics about resource groups [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

### Security

* Enhance PD log redaction [#8305](https://github.com/tikv/pd/issues/8305) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1861-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, PD implements a similar log redaction enhancement. To use this feature, you can set the value of the PD configuration item `security.redact-info-log` to `marker`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-pd-side).

* Enhance TiKV log redaction [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator) **tw@hfxsd** <!--1862-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, TiKV implements a similar log redaction enhancement. To use this feature, you can set the value of the TiKV configuration item `security.redact-info-log` to `marker`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-tikv-side).

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @okJiang @asddongmen **tw@hfxsd** <!--1689-->

    TiCDC v7.6.0 introduced the replication of DDL statements with bi-directional replication configured. Previously, bi-directional replication of DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to execute DDL statements on both TiDB clusters separately. With this feature, after assigning a `PRIMARY` BDR role to a cluster, TiCDC can replicate the DDL statements from that cluster to the `SECONDARY` cluster.
    
    In v8.3.0, this feature becomes generally available (GA).

    For more information, see [documentation](/ticdc-bidirectional-replication.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.2.0 to the current version (v8.3.0). If you are upgrading from v8.1.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* To avoid incorrect use of commands, pd-ctl cancels the prefix matching mechanism. For example, `store remove-tombstone` cannot be called via `store remove` [#8413](https://github.com/tikv/pd/issues/8413) @[lhy1024](https://github.com/lhy1024)

### MySQL compatibility

### System variables

| Variable name  | Change type   | Description |
|--------|------------------------------|------|
| [`tidb_analyze_column_options`](#tidb_analyze_column_options-new-in-v830) | Newly added | Controls the behavior of the `ANALYZE TABLE` statement. Setting it to the default value `PREDICATE` means only collecting statistics for [predicate columns](/statistics.md#collect-statistics-on-some-columns); setting it to `ALL` means collecting statistics for all columns. |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) | Newly added | Controls the behavior of the [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) feature. |
| [`tidb_enable_shared_lock_upgrade`](/system-variables.md#tidb_enable_shared_lock_upgrade-new-in-v830)       | Newly added  | Controls whether to enable the function of upgrading shared locks to exclusive locks. The default value of this variable is `OFF`, which means that the function of upgrading shared locks to exclusive locks is disabled. |
| [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso) | Modified | Adds the GLOBAL scope. |
| [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830) | Newly added | Controls the pre-aggregation strategy used in the first stage of two-stage or three-stage HashAgg operations pushed down to TiFlash. |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610) | Modified | Adds the GLOBAL scope and the variable value persists to the cluster. Changes the default value from `OFF` to `ON` after further tests, which means that the optimizer is allowed to push `Projection` down to the TiKV coprocessor. |
| [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)    | Modified   | Adds the SESSION scope.       |
| [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)  | Modified   | Adds the SESSION scope.    |
| [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) | Modified | Starting from v8.3.0, this variable controls the number of concurrent threads during the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) and [Delete Range](/garbage-collection-overview.md#Delete-Ranges) steps of the [Garbage Collection (GC)](/garbage-collection-overview.md) process. Before v8.3.0, this variable only controls the number of threads during the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830) | Newly added | Controls the batching strategy for requests from TiDB to TiKV. |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50) |  Modified | Support setting the value of the PD configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules.  |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)  | Modified | Support setting the value of the TiKV configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules.  |
| TiFlash   | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Modified |  Support setting the value of the TiFlash Learner configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules  |
|  BR  |  [`--allow-pitr-from-incremental`](/br/br-incremental-guide.md#limitations) | Newly added  |   Controls whether incremental backups are compatible with subsequent log backups. The default value is `true`, which means that incremental backups are compatible with subsequent log backups. In the case of compatibility, the DDL to be played back is scrutinized before the incremental restore starts. |

### System tables

* The [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) and [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) system tables add the `SESSION_ALIAS` field to show the number of rows currently affected by the DML statement [#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao) **tw@qiancai** <!--1903-->

### Other changes

## Offline package changes

## Deprecated features **tw@hfxsd**

* The following features are deprecated starting from v8.3.0:

    * Starting from v8.3.0, the [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540) system variable is deprecated. TiDB tracks predicate columns by default. For more information, see [`tidb_analyze_column_options`](#tidb_analyze_column_options-new-in-v830).

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in- v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.

## Improvements

+ TiDB <!--tw@Oreoxmt: 13 notes-->

    - Support the `SELECT ... STRAIGHT_JOIN ... USING ( ... )` statement [#54162](https://github.com/pingcap/tidb/issues/54162) @[dveeden](https://github.com/dveeden)
    - Construct more precise index access ranges for filter conditions like `((idx_col_1 > 1) or (idx_col_1 = 1 and idx_col_2 > 10)) and ((idx_col_1 < 10) or (idx_col_1 = 10 and idx_col_2 < 20))` [#54337](https://github.com/pingcap/tidb/issues/54337) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - Use index order to avoid extra sorting operations for SQL queries like `WHERE idx_col_1 IS NULL ORDER BY idx_col_2` [#54188](https://github.com/pingcap/tidb/issues/54188) @[ari-e](https://github.com/ari-e)
    - Display analyzed indexes in the `analyze_jobs` table [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin)
    - Support applying the `tidb_redact_log` setting to the output of `EXPLAIN` statements [#54565](https://github.com/pingcap/tidb/issues/54565) @[hawkingrei](https://github.com/hawkingrei)
    - Support backing up and restoring the `mysql.column_stats_usage` table [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin)
    - Support generating the `Selection` operator on `IndexRangeScan` for multi-valued indexes [#54876](https://github.com/pingcap/tidb/issues/54876) @[time-and-fate](https://github.com/time-and-fate)
    - Support killing running automatic `ANALYZE` tasks outside the set time window [#55283](https://github.com/pingcap/tidb/issues/55283) @[hawkingrei](https://github.com/hawkingrei)
    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - The TopN operator supports disk spill [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB node supports executing queries with the `WITH ROLLUP` modifier and the `GROUPING` function [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->
    - The system variable [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso-new-in-v830) supports `GLOBAL` scope [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->
    - Improve GC (Garbage Collection) efficiency by supporting concurrent range deletion. You can control the number of concurrent threads using [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->
    - Improve the performance of bulk DML execution mode (`tidb_dml_type = "bulk"`) [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    - Improve the performance of schema information cache-related interface schema `SchemaByID` [#54074](https://github.com/pingcap/tidb/issues/54074) @[ywqzzy](https://github.com/ywqzzy)
    - Improve the query performance for certain system tables when schema information caching is enabled [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta)
    - Optimize error messages for conflicting keys when adding unique indexes [#53004](https://github.com/pingcap/tidb/issues/53004) @[lance6716](https://github.com/lance6716)

+ TiKV

+ PD

+ TiKV <!--tw@hfxsd: 5 notes-->

    - Optimize `async-io` batching mechanism to reduce I/O bandwidth usage [#16907](https://github.com/tikv/tikv/issues/16907) @[LykxSassinator](https://github.com/LykxSassinator)
    - Redesigned TiCDC's delegate and downstream modules to better support partial subscription [#16362](https://github.com/tikv/tikv/issues/16362) @[hicqu](https://github.com/hicqu)
    - Reduce the size of a single slow log [#17294](https://github.com/tikv/tikv/issues/17294) @(Connor1996)[https://github.com/Connor1996]
    - Add a new monitoring metric `min safe ts` [#17307](https://github.com/tikv/tikv/issues/17307) @[mittalrishabh](https://github.com/mittalrishabh)
    - Reduce the memory usage of the peer message channel [#16229](https://github.com/tikv/tikv/issues/16229) @[Connor1996](https://github.com/Connor1996)

+ TiFlash

+ Tools

    + Backup & Restore (BR)
    
        - Support checking whether a full backup exists before starting point-in-time recovery (PITR) for the first time. If the full backup is not found, BR terminates the restore and returns an error [#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1915-->
        - Support checking whether the disk space in TiKV and TiFlash is sufficient before restoring snapshot backups. If the space is insufficient, BR terminates the restore and returns an error [#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->
        - Support checking whether the disk space in TiKV is sufficient before TiKV downloads each SST file. If the space is insufficient, BR terminates the restore and returns an error [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->

        + TiCDC

            - note [#issue](链接) @[贡献者 GitHub ID](链接)
            - note [#issue](链接) @[贡献者 GitHub ID](链接)

        + TiDB Data Migration (DM)

            - note [#issue](链接) @[贡献者 GitHub ID](链接)
            - note [#issue](链接) @[贡献者 GitHub ID](链接)

        + TiDB Lightning

            - note [#issue](链接) @[贡献者 GitHub ID](链接)
            - note [#issue](链接) @[贡献者 GitHub ID](链接)

        + TiUP

            - note [#issue](链接) @[贡献者 GitHub ID](链接)
            - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 11 notes-->

    - 重置 pipelinedwindow 的 Open 方法中的参数，以避免当 pipelinedwindow 作为 apply 的子节点使用时，由于重复的打开和关闭操作导致重用先前的参数值而发生的意外错误 [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复了由于超出 tidb_mem_quota_query 而导致查询被终止时可能卡住的问题 [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - 修复了触发 HashAgg 落盘时计算错误结果的问题 [#55290](https://github.com/pingcap/tidb/issues/55290) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复从 `YEAR` 转换为 JSON 格式时的 `json_type` 错误的问题 [#54027](https://github.com/pingcap/tidb/issues/54027) @[YangKeao](https://github.com/YangKeao)
    - 修复系统变量 `tidb_schema_cache_size` 的取值范围错误的问题 [#54034](https://github.com/pingcap/tidb/issues/54034) @[lilinghai](https://github.com/lilinghai)
    - 修复当分区表达式为 `EXTRACT(YEAR FROM col)` 时不会分区裁剪的问题 [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    - 修复了表数量较多情况下 `FLASHBACK DATABASE` 失败的问题 [#54415](https://github.com/pingcap/tidb/issues/54415) @[lance6716](https://github.com/lance6716)
    - 修复了使用 fast_reorg 模式添加索引可能失败的问题 [#54568](https://github.com/pingcap/tidb/issues/54568) @[lance6716](https://github.com/lance6716)
    - 修复了 `ADMIN CANCEL DDL JOBS` 可能导致 DDL 失败的问题 [#54687](https://github.com/pingcap/tidb/issues/54687) @[lance6716](https://github.com/lance6716)
    - 修复了库数量较多情况下 `FLASHBACK DATABASE` 死循环的问题 [#54915](https://github.com/pingcap/tidb/issues/54915) @[lance6716](https://github.com/lance6716)
    - 修复了来自 DM 同步的超过索引列最大长度的表时同步失败的问题 [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716) <!--tw@hfxsd: the following 12 notes-->
    - Fix the issue that the error `runtime error: index out of range` might occur when executing SQL statements with `tidb_enable_inl_join_inner_multi_pattern` enabled [#54535](https://github.com/pingcap/tidb/issues/54535) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that you cannot exit TiDB by `CTRL+C` during statistics initialization in TiDB [#54589](https://github.com/pingcap/tidb/issues/54589) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `INL_MERGE_JOIN` optimizer hint returns incorrect results by deprecating it [#54064](https://github.com/pingcap/tidb/issues/54064) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that a correlated subquery that contains `WITH ROLLUP` might cause TiDB to panic and return an error `runtime error: index out of range` [#54983](https://github.com/pingcap/tidb/issues/54983) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that predicates cannot be pushed down properly when the filter condition of a SQL query contains virtual columns and the execution condition contains `UnionScan` [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the error `runtime error: invalid memory address or nil pointer dereference` might occur when executing SQL statements with `tidb_enable_inl_join_inner_multi_pattern` enabled [#55169](https://github.com/pingcap/tidb/issues/55169) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a query statement that contains `UNION` might return incorrect results [#52985](https://github.com/pingcap/tidb/issues/52985) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that `tot_col_size` column in the `mysql.stats_histograms` table might be a negative number [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `columnEvaluator` cannot identify the column references in the input chunk, which leads to `runtime error: index out of range` when executing SQL [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `STATS_EXTENDED` becomes a reserved keyword [#39573](https://github.com/pingcap/tidb/issues/39573) @[wddevries](https://github.com/wddevries)
    - Fix the issue that when `tidb_low_resolution` is enabled, `select for update` can be executed [#54684](https://github.com/pingcap/tidb/issues/54684) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that internal SQL cannot be displayed in the slow log when `tidb_redact_log` is enabled [#54190](https://github.com/pingcap/tidb/issues/54190) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复事务占用的内存可能被多次重复统计的问题 [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复使用 `SHOW WARNINGS;` 获取警告时可能导致 panic 的问题 [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复加载索引统计信息可能会造成内存泄漏的问题 [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复当排序规则为 `utf8_bin` 或 `utf8mb4_bin` 时意外消除 `LENGTH()` 条件的错误 [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复统计数据在遇到主键重复时没有更新 `stats_history` 表的问题 [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复递归 CTE 查询可能导致无效指针的问题 [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复某些连接在握手完成之前退出导致 Grafana 监控指标中的连接数 (Connection Count) 不正确的问题 [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复使用 TiProxy 和资源组 (Resource Group) 功能时，每个资源组的连接数 (Connection Count) 显示不正确的问题 [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复当查询包含非关联子查询和 `LIMIT` 子句时，列剪裁可能不完善导致计划不优的问题 [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复针对 `SELECT ... FOR UPDATE` 复用了错误点查询计划的问题 [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > 错误修复> TiDB - 修复当第一个参数是 `month` 并且第二个参数是负数时，`TIMESTAMPADD()` 函数会进入无限循环的问题 [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复慢日志中内部语句中的 SQL 默认被脱敏为空的问题 [#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复可以生成 `_tidb_rowid` 的点查 (`PointGet`) 执行计划的问题 [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复从 v7.1 升级后 `SHOW IMPORT JOBS` 报错 `Unknown column 'summary'` 的问题 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复当视图定义中使用子查询作为列定义时，通过 `information_schema.columns` 获取列信息返回告警 Warning 1356 的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复可以创建非严格自增的 RANGE 分区表的问题 [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复当 SQL 异常中断时，`INDEX_HASH_JOIN` 无法正常退出的问题 [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-8.1.1.md > 错误修复> TiDB - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)

+ PD <!--tw@qiancai: 6 notes-->

    - (dup): release-7.5.3.md > 错误修复> PD - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 表中时间类型不正确的问题 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复资源组 (Resource Group) 在高并发场景下无法有效限制资源使用的问题 [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复获取表属性时错误调用 PD API 的问题 [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复开启 `scheduling` 微服务后，扩缩容进度显示错误的问题 [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复加密管理器在使用前未初始化的问题 [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.1.1.md > 错误修复> PD - 修复部分日志未脱敏的问题 [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - 修复在 PD 开启微服务时，重定向可能发生 panic 的问题 [#8406](https://github.com/tikv/pd/issues/8406) @[HuSharp](https://github.com/HuSharp)
    - 修复了 split-merge-interval 不生效的问题 [#8404](https://github.com/tikv/pd/issues/8404) @[lhy1024](https://github.com/lhy1024)
    - 修复了开启 replication.strictly-match-label=true 时启动 TiFlash 失败的问题 [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - 修复极端场景下可能导致获取 TSO 慢的问题 [#8500](https://github.com/tikv/pd/issues/8500) @[rleungx](https://github.com/rleungx)
    - 修复了大规模集群下可能发生数据竞争的问题 [#8386](https://github.com/tikv/pd/issues/8386) @[rleungx](https://github.com/rleungx)
    - 修复 runaway 只统计 coprocessor 过程时间消耗的 bug，增加 TiDB 侧的时间统计 [#51325](https://github.com/pingcap/tidb/issues/51325) @[HuSharp](https://github.com/HuSharp)
    
+ TiFlash <!--tw@hfxsd: 4 notes-->

    - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - Fix the issue that when TiFlash is network partitioned with any PD, read request timeout errors might occur [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-7.5.3.md > 错误修复> TiFlash - 修复跨数据库对含空分区的分区表执行 `RENAME TABLE ... TO ...` 后，TiFlash 可能 panic 的问题 [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.3.md > 错误修复> TiFlash - 修复开启延迟物化后，部分查询在执行时可能报列类型不匹配错误的问题 [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.3.md > 错误修复> TiFlash - 修复开启延迟物化后，带有虚拟生成列的查询可能返回错误结果的问题 [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.3.md > 错误修复> TiFlash - 修复将 TiFlash 中 SSL 证书配置项设置为空字符串会错误开启 TLS 并导致 TiFlash 启动失败的问题 [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.3.md > 错误修复> TiFlash - 修复数据库创建后短时间内被删除时，TiFlash 可能 panic 的问题 [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.1.md > 错误修复> TiFlash - 修复 TiFlash 与任意 PD 之间发生网络分区（即网络连接断开），可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash write nodes might fail to restart in the disaggregated storage and compute architecture [#9282](https://github.com/pingcap/tiflash/issues/9282) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that read snapshots of TiFlash write nodes are not released in a timely manner in the disaggregated storage and compute architecture [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)

+ TiKV <!--tw@hfxsd: 5 notes-->

    - Fix the issue that 'Ingestion picked level` and `Compaction Job Size(files)` are displayed incorrectly in the Grafana TiKV component [#15990](https://github.com/tikv/tikv/issues/15990) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that `cancel_generating_snap` incorrectly updating `snap_tried_cnt` causes TiKV to panic [#17226](https://github.com/tikv/tikv/issues/17226) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that the information of `Ingest SST duration seconds` in correct [#17239](https://github.com/tikv/tikv/issues/17239) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that CPU profiling flag is not reset correctly in case of an error [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    - Fix the incompatibility issue of the bloom filter in earlier versions (earlier than v7.1) and later versions [#17272](https://github.com/tikv/tikv/issues/17272) @[v01dstar](https://github.com/v01dstar)
    
+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.5.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复增量恢复过程中 `ADD INDEX`、`MODIFY COLUMN` 等需要回填的 DDL 可能无法正确恢复的问题 [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)

    + TiCDC <!--tw@lilin90: 1 note-->

        - 修复当下游 Kafka 无法访问时，Processor 模块可能卡住的问题 [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM) <!--tw@hfxsd: 1 note-->

        - (dup): release-8.1.1.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 schema tracker 无法正确处理 LIST 分区表导致 DM 报错的问题 [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - (dup): release-8.1.1.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复当索引长度超过 `max-index-length` 默认值时数据同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - Fix the issue that DM cannot handle `FAKE_ROTATE_EVENT` correctly [#11381](https://github.com/pingcap/tiflow/issues/11381) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning <!--tw@Oreoxmt: 3 notes-->

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.1.1.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 获取 keyspace 失败时输出的 `WARN` 日志可能引起用户混淆的问题 [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the TLS configuration of TiDB Lightning affects cluster certificates [#54172](https://github.com/pingcap/tidb/issues/54172) @[ei-sugimoto](https://github.com/ei-sugimoto)
        - Fix the issue that transaction conflicts occur when importing data using TiDB Lightning [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - Fix the issue that large checkpoint files cause performance degradation when importing numerous databases and tables [#55054](https://github.com/pingcap/tidb/issues/55054) @[D3Hunter](https://github.com/D3Hunter)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [ari-e](https://github.com/ari-e)
- [ei-sugimoto](https://github.com/ei-sugimoto)
- [HaoW30](https://github.com/HaoW30)
- [JackL9u](https://github.com/JackL9u)
- [michaelmdeng](https://github.com/michaelmdeng)
- [mittalrishabh](https://github.com/mittalrishabh)
- [qingfeng777](https://github.com/qingfeng777)
- [renovate](https://github.com/apps/renovate)
- [SandeepPadhi](https://github.com/SandeepPadhi)
- [yzhan1](https://github.com/yzhan1)
