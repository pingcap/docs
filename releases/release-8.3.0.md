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
    <td> <a href="https://docs.pingcap.com/zh/tidb/v8.3/partitioned-table#global-indexes">Global indexes for partitioned tables (experimental)</a></td> **tw@hfxsd** <!--1531-->
    <td>Global indexes can effectively improve the efficiency of retrieving non-partitioned keys, and remove the restriction that partitioned keys must contain a unique key. This feature extends the usage scenarios of TiDB partitioned tables and avoids some of the application modification work that might be required for data migration.</td>
  </tr>
  <tr>
    <td>Default pushdown of the <code>Projection</code> operator to the storage engine</td>**tw@Oreoxmt** <!--1872-->
    <td>Pushing the <code>Projection</code> operator down to the storage engine can distribute the load across storage nodes while reducing data transfer between nodes. This optimization helps to reduce the execution time for certain SQL queries and improves the overall database performance.</td>
  </tr>
  <tr>
    <td>统计信息收集忽略不必要的列</td>**tw@lilin90** <!--1753-->
    <td>在保证优化器能够获取到必要信息的前提下，加快了统计信息收集的速度，提升统计信息的时效性，进而保证最优的执行计划的选择，提升集群性能。同时也降低的系统开销，改善资源利用率。</td>
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

* 统计信息收集忽略不必要的列 [#53567](https://github.com/pingcap/tidb/issues/53567) @[hi-rustin](https://github.com/hi-rustin) **tw@lilin90** <!--1753-->

    当优化器生成执行计划时，只需要部分列的统计信息，例如过滤条件上的列，连接键上的列，聚合目标用到的列。从 v8.3.0 起，TiDB 会持续观测 SQL 语句对列的使用历史，默认只收集有索引的列，以及被观测到的有必要收集统计信息的列。这将会提升统计信息的收集速度，避免不必要的资源浪费。

    从旧版本升级到 v8.3.0 或更高版本的用户，默认保留原有行为，收集所有列的统计信息，需要手工设置变量 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `PREDICATE` 来启用，新部署默认开启。
    
    对于随机查询比较多的偏分析型系统，可以设置 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `ALL` 收集所有列的统计信息，保证随机查询的性能。其余类型的系统推荐保留 [`tidb_analyze_column_options`](/system-variables.md#tidb_analyze_column_options-从-v830-版本开始引入) 为 `PREDICATE` 只收集必要的列。

    更多信息，请参考[用户文档](/statistics.md#收集部分列的统计信息)。

* Improve the query performance of some system tables  [#50305](https://github.com/pingcap/tidb/issues/50305) @[tangenta](https://github.com/tangenta) **tw@hfxsd** <!--1865-->

    In previous versions, querying system tables has slow performance when the cluster size becomes large and the number of tables is high.

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

* Support for partition pruning when partition expressions use the `EXTRACT(YEAR_MONTH...)` function to support partition pruning and improve query performance [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1885-->

    In previous versions, when partition expressions used the `EXTRACT(YEAR_MONTH...)` function, partition pruning is not supported, resulting in poor query performance. Starting from v8.3.0, partition pruning is supported when partition expressions use the `EXTRACT(YEAR_MONTH...)` function, which improves query performance.

    For more information, see [documentation](/partition-pruning.md#scenario-three).
    
* The performance of `CREATE TABLE` is improved by 1.4 times, `CREATE DATABASE` is improved by 2.1 times, and `ADD COLUMN` is improved by 2 times [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1863-->

    TiDB v8.0.0 introduces the system variable [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) to improve table creation performance in batch table creation scenarios. In v8.3.0, when submitting the DDL statements for table creation concurrently through 10 sessions in a single database, the performance is improved by 1.4 times compared with v8.2.0.
   
    In v8.3.0, the performance of general DDLs in batch execution has improved compared to v8.2.0. The performance of `CREATE DATABASE` for 10 sessions concurrently improves by 19 times compared to v8.1.0 and 2.1 times compared to v8.2.0. The performance of using10 sessions for adding columns (`ADD COLUMN`) to multiple tables in the same database in batch has improved by 10 times compared to v8.1.0, and 2.1 times compared to v8.2.0. The performance of `ADD COLUMN` with 10 sessions on multiple tables in the same database is 10 times better than v8.1.0 and 2 times better than v8.2.0.

    For more information, see [documentation](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).    

### Reliability

* 新增以流式获取游标的结果集 （实验特性） [#54526](https://github.com/pingcap/tidb/issues/54526) @[YangKeao](https://github.com/YangKeao) **tw@lilin90** <!--1891-->

    当应用代码通过 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#使用-streamingresult-流式获取执行结果) 获取结果集时，TiDB 通常会将完整结果保存至 TiDB ，再分批返回给客户端。如果结果集过大，可能会触发临时落盘。自 v8.3.0 开始，通过设置系统变量[`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入) 为 `ON`，TiDB 不再把所有数据读取到 TiDB 节点，而是会随着客户端的读取逐步将数据传送至 TiDB 节点。在处理较大结果集时，这将会减少 TiDB 节点的内存使用，提升集群的稳定性。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_lazy_cursor_fetch-从-v830-版本开始引入)。

* SQL 绑定的增强 [#issue号](链接) @[time-and-fate](https://github.com/time-and-fate) **tw@lilin90** <!--1760-->

    在 OLTP 负载环境中，绝大部分 SQL 的最优执行计划是固定的，因此对业务中的重要 SQL 实施执行计划绑定，可以减少执行计划变差的机会，提升系统稳定性。为了满足客户创建大量 SQL 绑定的需求，TiDB 对 SQL 绑定的能力和体验进行了增强，其中包括：

    - 用单条 SQL 从多个历史执行计划中创建 SQL 绑定
    - 从历史执行计划创建绑定不再受表数量的限制
    - SQL 绑定支持更多的优化器提示，能够更稳定重现原执行计划

    更多信息，请参考[用户文档](/sql-plan-management.md)。

### Availability

* TiProxy supports built-in virtual IP management [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    Before v8.3.0, when using primary-secondary mode for high availability, TiProxy requires an additional component to manage the virtual IP. Starting from v8.3.0, TiProxy supports built-in virtual IP management. In primary-secondary mode, when a primary node fails over, the new primary node will automatically bind to the specified virtual IP, ensuring that clients can always connect to an available TiProxy through the virtual IP.

    To enable virtual IP management, specify the virtual IP address using the TiProxy configuration item [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) and specify the network interface to bind the virtual IP to using [`ha.interface`](/tiproxy/tiproxy-configuration.md#interface). If neither of these configuration items is set, this feature is disabled.
    
    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* Support upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1871-->

    TiDB does not support `SELECT LOCK IN SHARE MODE` yet. Starting from v8.3.0, TiDB supports upgrading `SELECT LOCK IN SHARE MODE` to exclusive locks to enable support for `SELECT LOCK IN SHARE MODE`. You can control whether to enable this feature by the new variable [`tidb_enable_shared_lock_upgrade`](/system-variables.md#tidb_enable_shared_lock_upgrade-new-in-v830).
    
    For more information, see [documentation](/system-variables.md#tidb_enable_shared_lock_upgrade-new-in-v830).

* Partitioned tables support global indexes (experimental) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    In previous versions of partitioned tables, there are more limitations because global indexes are not supported, for example, the unique key must contain a partition key, and if the query condition does not have a partition key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature is under development at that time and it is not recommended to enable it.
    
    Starting with v8.3.0, the global indexes feature has been released as an experimental feature. When you create a unique key that does not contain all partition keys, TiDB implicitly creates a global index, removing the restriction that the unique key must contain all partition keys, to meet flexible business needs. Global indexes also improve the query performance of indexes without partitioned keys.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

### DB operations

### Observability

* 展示初始统计信息加载的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB 在启动时要对基础统计信息进行加载，在表或者分区数量很多的情况下，这个过程要耗费一定时间，当配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 为 `ON` 时，初始统计信息加载完成前 TiDB 不会对外提供服务。在这种情况下，用户需要对加载过程进行观测，从而能够预期服务开启时间。自 v8.3.0，TiDB 会在日志中分阶段打印初始统计信息加载的进度，让客户了解运行情况。为了给外部工具提供格式化的结果，TiDB 增加了额外的监控 [API](/tidb-monitoring-api.md)，能够在启动阶段随时获取初始统计信息的加载进度。

### Security

* Enhance PD log redaction [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhe]l(https://github.com/xhebox) **tw@hfxsd** <!--1861-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, PD implements a similar log redaction enhancement. To use this feature, you can set the value of the PD configuration item `security.redact-info-log` to `marker`.

    For more information, see [documentation](/log-redaction.md#log-redaction-in-pd-side).

* Enhance TiKV log redaction [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator) **tw@hfxsd** <!--1862-->

    TiDB v8.0.0 enhances log redaction and supports marking user data in TiDB logs with single-angle quotation marks `‹›`. Based on the marked logs, you can decide whether to redact the marked information when displaying the logs, thus increasing the flexibility of log redaction. In v8.2.0, TiFlash implements a similar log redaction enhancement.
    
    In v8.3.0, TiKV implements a similar log redaction enhancement. To use this feature, you can set the value of the PD configuration item `security.redact-info-log` to `marker`.
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

* 在系统表 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 和 [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) 中新增 `ROWS_AFFECTED` 字段，用于显示当前 DML 语句已经写入的数据行数。[#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao) **tw@qiancai** <!--1903-->

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
    - Optimize MemDB implementation to reduce write transaction latency [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
    - GC（垃圾回收）支持并发 Delete Range（删除区间）以提升处理效率，可以通过 [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-从-v50-版本开始引入) 控制并发线程数 [#54570](https://github.com/pingcap/tidb/issues/54570) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->
    
+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

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
