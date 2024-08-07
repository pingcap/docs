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
    <th>分类</th>
    <th>功能/增强</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">可扩展性和性能</td>
    <td> <a href="https://docs.pingcap.com/zh/tidb/v8.3/partitioned-table#全局索引">分区表全局索引（实验特性）</a></td> **tw@hfxsd** <!--1531-->
    <td>全局索引能够有效提升对非分区键的检索效率，同时也解除了分区键一定要包含唯一键 (Unique Key) 的限制，扩展了 TiDB 分区表的使用场景，也能够避免数据迁移可能遇到的部分应用改造工作。</td>
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

* 提升了一些系统表的查询性能 [#]() @[tangenta](https://github.com/tangenta) **tw@hfxsd** <!--1865-->

    在之前的版本，当集群规模变大，表数量较多时，查询系统表性能较慢。

    在 v8.0.0 优化了以下 4 个系统表的查询性能:
    
    - INFORMATION_SCHEMA.TABLES
    - INFORMATION_SCHEMA.STATISTICS
    - INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    - INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS

    在 v8.3.0 版本优化了以下系统表的查询性能，相比 v8.2.0 性能有数倍的提升:

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

    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。

* 分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，支持分区裁剪，提升查询性能 [#54209](https://github.com/pingcap/tidb/pull/54209) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1885-->

    之前的版本，当分区表达式使用 `EXTRACT(YEAR_MONTH...)` 函数时，不支持分区裁剪，导致查询性能较差。从 v8.3.0 开始，当分区表达式使用该函数时，支持分区裁剪，提升了查询性能。

    更多信息，请参考[用户文档](/partition-pruning.md#场景三)。
    
* 批量建表 (`CREATE TABLE`) 的性能提升了 2.75 倍，批量建库 (`CREATE DATABASE`) 的性能提升了 2.1 倍 [#54436](https://github.com/pingcap/tidb/issues/54436) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1863-->

    v8.0.0 引入了系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)，用于在批量建表的场景中提升建表的性能。在 v8.3.0 中，通过 10 个 session 在单个库内并发提交建表的 DDL，相比 v8.2.0 性能有 2.75 倍的提升。
    
    从 v8.3.0 开始，该变量也优化了批量建库的性能，相比 v8.2.0，通过 10 个 session 并发提交建库的 DDL ，性能有 2.1 倍的提升。 

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_fast_create_table-从-v800-版本开始引入)。    

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

* 支持 `Shared Lock` 升级为 `Exclusive Lock` [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->

    TiDB 暂不支持 `Shared Lock`. 在 v8.3.0 版本中，TiDB 支持将 `Shared Lock` 升级为 `Exclusive Lock`，实现对 `Shared Lock` 语法的支持。通过新增的变量 [tidb_enable_shared_lock_upgrade](/system-variables.md#tidb_enable_shared_lock_upgrade-从-v830-版本开始引入) 控制是否启用该功能。

* 分区表支持全局索引 (Global Index)（实验特性） [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) **tw@hfxsd** <!--1531-->

    之前版本的分区表，因为不支持全局索引有较多的限制，比如唯一键必须包含分区建，如果查询条件不带分区建，查询时会扫描所有分区，导致性能较差。从 v7.6.0 开始，引入了参数 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 用于开启全局索引特性，但该功能当时处于开发中，不够完善，不建议开启。
    
    从 v8.3.0 开始，全局索引作为实验特性正式发布了。你在创建不包含全部分区建的唯一键时，TiDB 会隐式的创建全局索引，去除了唯一建必须包含全部分区键的限制，满足灵活的业务需求。同时基于全局索引也提升了不带分区建的索引的查询性能。

    更多信息，请参考[用户文档](/partitioned-table.md#全局索引)。

### DB operations

### Observability

* 展示初始统计信息加载的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@lilin90** <!--1792-->

    TiDB 在启动时要对基础统计信息进行加载，在表或者分区数量很多的情况下，这个过程要耗费一定时间，当配置项 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-从-v657-和-v710-版本开始引入) 为 `ON` 时，初始统计信息加载完成前 TiDB 不会对外提供服务。在这种情况下，用户需要对加载过程进行观测，从而能够预期服务开启时间。自 v8.3.0，TiDB 会在日志中分阶段打印初始统计信息加载的进度，让客户了解运行情况。为了给外部工具提供格式化的结果，TiDB 增加了额外的监控 [API](/tidb-monitoring-api.md)，能够在启动阶段随时获取初始统计信息的加载进度。

### Security

* 增强 PD 日志脱敏 [#51306](https://github.com/pingcap/tidb/issues/51306) @[xhe](https://github.com/xhebox) **tw@hfxsd** <!--1861-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。
    
    在 v8.3.0 中，PD 实现了类似的日志脱敏功能增强，要使用该功能，可以将 PD 配置项 `security.redact-info-log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md#pd-组件日志脱敏)。

* 增强 TiKV 日志脱敏 [#17206](https://github.com/tikv/tikv/issues/17206) @[lucasliang](https://github.com/LykxSassinator) **tw@hfxsd** <!--1862-->

    TiDB v8.0.0 增强了日志脱敏功能，支持控制是否使用标记符号 `‹ ›` 包裹 TiDB 日志中的用户数据。基于标记后的日志，你可以在展示日志时决定是否对被标记信息进行脱敏处理，从而提升日志脱敏功能的灵活性。在 v8.2.0 中，TiFlash 实现了类似的日志脱敏功能增强。
    
    在 v8.3.0 中，TiKV 实现了类似的日志脱敏功能增强，要使用该功能，可以将 TiKV 配置项 `security.redact-info-log` 的值设置为 `marker`。

    更多信息，请参考[用户文档](/log-redaction.md#tikv-组件日志脱敏)。

### Data migration

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
| [`tidb_enable_shared_lock_upgrade`](/system-variables.md#tidb_enable_shared_lock_upgrade-从-v830-版本开始引入)       | 新增  | 控制是否启用共享锁升级为排他锁的功能。默认值为 `OFF`，表示不启用共享锁升级为排他锁的功能。  |
| [`tidb_opt_projection_push_down`](/system-variables.md#tidb_opt_projection_push_down-new-in-v610) | Modified | Adds the GLOBAL scope and the variable value persists to the cluster. Changes the default value from `OFF` to `ON` after further tests, which means that the optimizer is allowed to push `Projection` down to the TiKV coprocessor. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| PD   |  [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v50-版本开始引入) |  修改 | 支持将 PD 配置项 `security.redact-info-log` 的值设置为 `marker`，使用单角形引号 `‹›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。  |
| TiKV  | [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入)  | 修改 | 支持将 TiKV 配置项 `security.redact-info-log` 的值设置为 `marker`，使用单角形引号 `‹›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
| TiFlash   | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)  | 修改 | 支持将 TiFlash Server 配置项 `security.redact-info-log` 的值设置为 `marker`，使用单角形引号 `‹›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。    |
| TiFlash   | [`security.redact-info-log`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 支持将 TiFlash Learner 配置项 `security.redact-info-log` 的值设置为 `marker`，使用单角形引号 `‹›` 标记出敏感信息，而不是直接隐藏，以便你能够自定义脱敏规则。   |
|    |   |   |   |

### System tables

* 在系统表 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 和 [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) 中新增 `ROWS_AFFECTED` 字段，用于显示当前 DML 语句已经写入的数据行数。[#46889](https://github.com/pingcap/tidb/issues/46889) @[lcwangchao](https://github.com/lcwangchao) **tw@qiancai** <!--1903-->

### Other changes

## Offline package changes

## Deprecated features

* The following features are deprecated starting from v8.3.0:

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。

## Improvements

+ TiDB

    - The TopN operator supports disk spill [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB supports using the `WITH ROLLUP` modifier and the `GROUPING` function [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->

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