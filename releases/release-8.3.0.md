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
    <td rowspan="4">Scalability and Performance</td>
    <td> <a href="https://docs.pingcap.com/tidb/v8.3/partitioned-table#global-indexes">Global indexes for partitioned tables (experimental)</a></td> **tw@hfxsd** <!--1531-->
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned keys, and remove the restriction that partitioned keys must contain a unique key. This feature extends the usage scenarios of TiDB partitioned tables and avoids some of the application modification work that might be required for data migration.</td>
  </tr>
  <tr>
    <td>Default pushdown of the <code>Projection</code> operator to the storage engine</td>**tw@Oreoxmt** <!--1872-->
    <td>Pushing the <code>Projection</code> operator down to the storage engine can distribute the load across storage nodes while reducing data transfer between nodes. This optimization helps to reduce the execution time for certain SQL queries and improves the overall database performance.</td>
  </tr>
  <tr>
    <td>Ignoring unnecessary columns when collecting statistics</td>**tw@lilin90** <!--1753-->
    <td>Under the premise of ensuring that the optimizer can obtain the necessary information, TiDB speeds up statistics collection, improves the timeliness of statistics, and thus ensures that the optimal execution plan is selected, improving the performance of the cluster. Meanwhile, TiDB also reduces the system overhead and improves the resource utilization.</td>
  </tr>
  <tr>
    <td>读写性能的细粒度优化</td>**tw@qiancai** <!--1893-->
    <td>通过优化 KV 请求的策略，增加获取 TSO 的模式等多重手段，进一步提升 TiDB 的读写性能，降低业务的执行时间，改善延迟。</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and Availability</td>
    <td>Built-in virtual IP management in TiProxy</td>**tw@Oreoxmt** <!--1887-->
    <td>In TiDB v8.3.0, TiProxy introduces built-in virtual IP management, which enables automatic virtual IP switching without relying on external platforms or tools. This feature simplifies TiProxy deployment and reduces the complexity of the database access layer.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability


### Performance

* The optimizer pushes the `Projection` operator down to the storage engine by default [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--1872-->

    Pushing the `Projection` operator down to the storage engine reduces data transfer between the compute engine and the storage engine. This is particularly effective when handling [JSON query functions](/functions-and-operators/json-functions/json-functions-search.md) or [JSON value attribute functions](/functions-and-operators/json-functions/json-functions-return.md). Starting from v8.3.0, TiDB enables the `Projection` operator pushdown feature by default, and changes the default value of the system variable controlling this feature, [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610), from `OFF` to `ON`. When this feature is enabled, the optimizer automatically pushes eligible JSON query functions and JSON value attribute functions down to the storage engine.

    For more information, see [documentation](/system-variables.md#tidb_opt_projection_push_down-new-in-v610).

* Optimize batch processing strategy for KV requests [#55206](https://github.com/pingcap/tidb/issues/55206) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1897-->

    TiDB fetches data by sending KV requests. Batching and processing KV requests in bulk can significantly improve execution performance. Before v8.3.0, the batch processing strategy in TiDB is less efficient. Starting from v8.3.0, TiDB introduces a more efficient batch strategy on top of the existing one. You can configure different batch processing strategies using the [`tikv-client.batch-policy`](/tidb-configuration-file.md#batch-policy-new-in-v830) configuration item to accommodate various workloads.

    For more information, see [documentation](/tidb-configuration-file.md#batch-policy-new-in-v830).
    
* 增加获取 TSO 的 RPC 模式，降低获取 TSO 的延迟 [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    TiDB 在向 PD 请求 TSO 时，会汇总一定时间段的请求并以同步的方式进行批处理以减少 RPC 请求数量、降低 PD 负载。对于延迟敏感的场景，这种模式的性能并不理想。在 v8.3.0 版本中，TiDB 新增 TSO 请求的异步批处理模式，并提供不同的并发能力，以增加相应的 PD 负载为代价，降低获取 TSO 的延迟。通过新增的变量 [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入) 设定获取 TSO 的 RPC 模式。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入)。

* TiFlash introduces HashAgg aggregation calculation modes to improve the performance for high NDV data [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1855-->

    Before v8.3.0, TiFlash has low aggregation calculation efficiency during the first stage of HashAgg aggregation when handling data with high NDV (number of distinct rows). Starting from v8.3.0, TiFlash introduces multiple HashAgg aggregation calculation modes to improve the performance of data with different characteristics. You can configure the HashAgg aggregation calculation mode using the system variable [`tiflash_hashagg_preaggregation_mode`](/system-variables.md#tiflash_hashagg_preaggregation_mode-new-in-v830).

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

### Reliability

* Support streaming cursor result sets (experimental) [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1891-->

    When the application code retrieves the result set using [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result), TiDB usually first stores the complete result set in memory, and then returns the data to the client in batches. If the result set is too large, TiDB might temporarily write the result to the hard disk.

    Starting from v8.3.0, if you set the system variable [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) to `ON`, TiDB no longer reads all data to the TiDB node, but gradually reads data to the TiDB node as the client reads. When TiDB processes large result sets, this feature reduces the memory usage of the TiDB node and improves the stability of the cluster.

    For more information, see [documentation](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830).

* Enhance SQL execution plan binding [#55280](https://github.com/pingcap/tidb/issues/55280) [#issue2](to-be-added) @[time-and-fate](https://github.com/time-and-fate) **tw@lilin90** <!--1760-->

    In OLTP scenarios, the optimal execution plan for most SQL statements is fixed. Implementing SQL execution plan binding for important SQL statements in the application can reduce the probability of the execution plan becoming worse and improve system stability. To meet the requirements of creating a large number of SQL execution plan bindings, TiDB enhances the capability and experience of SQL binding, including:

    - Use a single SQL statement to create SQL execution plan bindings from multiple historical execution plans to improve the efficiency of creating bindings.
    - The SQL execution plan binding supports more optimizer hints, and optimizes the conversion method for complex execution plans, making the binding more stable in restoring the execution plan.

    For more information, see [documentation](/sql-plan-management.md).

### Availability

* TiProxy supports built-in virtual IP management [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    Before v8.3.0, when using primary-secondary mode for high availability, TiProxy requires an additional component to manage the virtual IP. Starting from v8.3.0, TiProxy supports built-in virtual IP management. In primary-secondary mode, when a primary node fails over, the new primary node will automatically bind to the specified virtual IP, ensuring that clients can always connect to an available TiProxy through the virtual IP.

    To enable virtual IP management, specify the virtual IP address using the TiProxy configuration item [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) and specify the network interface to bind the virtual IP to using [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface). If neither of these configuration items is set, this feature is disabled.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1871-->

    TiDB does not support `SELECT LOCK IN SHARE MODE` yet. Starting from v8.3.0, TiDB supports upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks to enable support for `SELECT LOCK IN SHARE MODE`. You can control whether to enable this feature by the new variable [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

    For more information, see [documentation](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830).

* Partitioned tables support global indexes (experimental) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    In previous versions of partitioned tables, there are some limitations because global indexes are not supported. For example, the unique key must contain a partition key. If the query condition does not have a partition key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.
    
    Starting with v8.3.0, the global index feature has been released as an experimental feature. When you create a unique key that does not contain all partition keys, TiDB implicitly creates a global index, removing the restriction that the unique key must contain all partition keys, to meet flexible business needs. Global indexes also improve the query performance of unique indexes without partitioned keys.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

### DB operations

### Observability

* Show the progress of loading initial statistics [#53564](https://github.com/pingcap/tidb/issues/53564) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB loads basic statistics when it starts. In scenarios with many tables or partitions, this process can take a long time. When the configuration item [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) is set to `ON`, TiDB does not provide services until the initial statistics are loaded. In this case, you need to observe the loading process to estimate the service start time.

    Starting from v8.3.0, TiDB prints the progress of loading initial statistics in stages in the log, so you can understand the running status. To provide formatted results to external tools, TiDB adds the additional [monitoring API](/tidb-monitoring-api.md) so you can obtain the progress of loading initial statistics at any time during the startup phase.

### Security

* Enhance PD log redaction [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhe](https://github.com/xhebox) **tw@hfxsd** <!--1861-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, PD implements a similar log redaction enhancement. To use this feature, you can set the value of the PD configuration item `security.redact-info-log` to `marker`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-pd-side).

* Enhance TiKV log redaction [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator) **tw@hfxsd** <!--1862-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, TiKV implements a similar log redaction enhancement. To use this feature, you can set the value of the TiKV configuration item `security.redact-info-log` to `marker`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-tikv-side).

### Data migration

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (GA) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @okJiang @asddongmen **tw@hfxsd** <!--1689-->

    TiCDC v7.6.0 introduced the replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the PRIMARY BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.
    
    In v8.3.0, this feature becomes generally available (GA).

    For more information, see [documentation](/ticdc-bidirectional-replication.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.2.0 to the current version (v8.3.0). If you are upgrading from v8.1.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### MySQL compatibility

### System variables


| Variable name  | Change type   | Description |
|--------|------------------------------|------|
| [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) | 新增 | 控制 `ANALYZE TABLE` 语句默认收集的列。将其设置为 `PREDICATE` 表示仅收集 [predicate columns](/statistics.md#收集部分列的统计信息) 的统计信息；将其设置为 `ALL` 表示收集所有列的统计信息。 |
| [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) | 新增 | 这个变量用于控制 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 功能的行为。|
| [`tidb_enable_shared_lock_upgrade`](/system-variables.md#tidb_enable_shared_lock_upgrade-new-in-v830)       | Newly added  | controls whether to enable the function of upgrading shared locks to exclusive locks. The default value of this variable is `OFF`, which means that the function of upgrading shared locks to exclusive locks is disabled. |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610) | Modified | Adds the GLOBAL scope and the variable value persists to the cluster. Changes the default value from `OFF` to `ON` after further tests, which means that the optimizer is allowed to push `Projection` down to the TiKV coprocessor. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50) |  Modified | Support setting the value of the PD configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules.  |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-new-in-v408)  | Modified | Support setting the value of the TiKV configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules.  |
| TiFlash   | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)  | Modified | Support setting the value of the TiFlash Server configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules.   |
| TiFlash   | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Modified |  Support setting the value of the TiFlash Learner configuration item `security.redact-info-log' to `marker` to mark sensitive information in the log with single-angle quotation marks `‹›` instead of shielding it directly. With the `marker` option, you can customize the redaction rules  |
|    |   |   |   |

### System tables

* The [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) and [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) system tables add the `SESSION_ALIAS` field to show the number of rows written by the DML statement [#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao) **tw@qiancai** <!--1903-->

### Other changes

## Offline package changes

## Deprecated features **tw@hfxsd**

* The following features are deprecated starting from v8.3.0:

    *  TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in- v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.

## Improvements

+ TiDB

    - The TopN operator supports disk spill [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB supports using the `WITH ROLLUP` modifier and the `GROUPING` function [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->
    - The system variable [`tidb_low_resolution_tso`](/system-variables.md#tidb_low_resolution_tso-new-in-v830) supports `GLOBAL` scope [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->
    - Improve GC (Garbage Collection) efficiency by supporting concurrent range deletion. You can control the number of concurrent threads using [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->
    
+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)
    
        - Support checking whether a full backup exists before starting point-in-time recovery (PITR) for the first time. If the full backup is not found, BR terminates the restore and returns an error [#54418](https://github.com/pingcap/tidb/issues/54418) @[Leavrth](https://github.com/Leavrth) **tw@qiancai** <!--1915-->
        - Support checking whether the disk space in TiKV is sufficient before restoring snapshot backups. If the space is insufficient, BR terminates the restore and returns an error [#54316](https://github.com/pingcap/tidb/issues/54316) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->
        - Support checking whether the disk space in TiKV is sufficient before TiKV downloads SST files. If the space is insufficient, BR terminates the restore and returns an error [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1890-->

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

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

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

## Contributors

We would like to thank the following contributors from the TiDB community:

- [贡献者 GitHub ID](链接)
