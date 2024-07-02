---
title: TiDB 8.2.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.2.0.
---

# TiDB 8.2.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.2.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.2/quick-start-with-tidb)

8.2.0 introduces the following key features and improvements:

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
    <td><a href="https://docs.pingcap.com/tidb/v8.2/tiproxy-load-balance">TiProxy supports multiple load balancing policies<!--tw@Oreoxmt--></td>
    <td>In TiDB v8.2.0, TiProxy evaluates and ranks TiDB nodes based on various dimensions, such as status, connection counts, health, memory, CPU, and location. According to the load balancing policy specified in the <code>policy</code> configuration item, TiProxy dynamically selects the optimal TiDB node to execute database operations. This optimizes overall resource usage, improves cluster performance, and increases throughput.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v8.2/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800">The parallel HashAgg algorithm of TiDB supports disk spill (GA)<!--tw@Oreoxmt--></td>
    <td>HashAgg is a widely used aggregation operator in TiDB for efficiently aggregating rows with the same field values. TiDB v8.0.0 introduces parallel HashAgg as an experimental feature to further enhance processing speed. When memory resources are insufficient, parallel HashAgg spills temporary sorted data to disk, avoiding potential OOM risks caused by excessive memory usage. This improves query performance while maintaining node stability. In v8.2.0, this feature becomes generally available (GA) and is enabled by default, enabling you to safely configure the concurrency of parallel HashAgg.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.2/tidb-configuration-file#stats-load-concurrency-new-in-v540">Improve statistics loading efficiency by up to 10 times</a><!--tw@hfxsd--></td>
    <td>For clusters with a large number of tables and partitions, such as SaaS or PaaS services, improvement in statistics loading efficiency can solve the problem of slow startup of TiDB instances. This improvement reduces performance rollbacks caused by statistics loading failures and improves cluster stability.</td>
  </tr>
  <tr>
    <td rowspan="1">DB Operations and Observability</td>
    <td><a href=""https://docs.pingcap.com/tidb/v8.2/tidb-resource-control#bind-resource-groups">Introduce privilege control of switching resource groups</a><!--tw@lilin90--></td>
    <td>As resource control is widely used, the privilege control of switching resource groups can prevent database users from abusing resources, strengthen administrators' protection of overall resource usage, and improve cluster stability.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### Performance

* Support pushing down the following string functions to TiKV [#50601](https://github.com/pingcap/tidb/issues/50601) @[dbsid](https://github.com/dbsid) **tw@Oreoxmt** <!--1663-->

    * `JSON_ARRAY_APPEND()`
    * `JSON_MERGE_PATCH()`
    * `JSON_REPLACE()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* TiDB supports parallel sorting [#49217](https://github.com/pingcap/tidb/issues/49217) [#50746](https://github.com/pingcap/tidb/issues/50746) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1665-->

    Before v8.2.0, TiDB only executes Sort operators sequentially, affecting query performance when sorting large amounts of data.

    Starting from v8.2.0, TiDB supports parallel sorting, which significantly improves sorting performance. This feature does not need manual configuration. TiDB automatically determines whether to use parallel sorting based on the value of the [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50) system variable.

    For more information, see [documentation](/system-variables.md#tidb_executor_concurrency-new-in-v50).

* The parallel HashAgg algorithm of TiDB supports disk spill (GA) [#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1842-->

    TiDB v8.0.0 introduces the parallel HashAgg algorithm with disk spill support as an experimental feature. In v8.2.0, this feature becomes generally available (GA). When using the parallel HashAgg algorithm, TiDB automatically triggers data spill based on memory usage, thus balancing query performance and data throughput. This feature is enabled by default. The system variable `tidb_enable_parallel_hashagg_spill`, which controls this feature, will be deprecated in a future release.

    For more information, see [documentation](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800).

### Reliability

* Improve statistics loading efficiency by up to 10 times [#52831](https://github.com/pingcap/tidb/issues/52831) @[hawkingrei](https://github.com/hawkingrei) **tw@hfxsd** <!--1754-->

    SaaS or PaaS applications can have a large number of data tables, which not only slow down the loading speed of the initial statistics, but also increase the failure rate of load synchronization under high loads. The startup time of TiDB and the accuracy of the execution plan can be affected. In v8.2.0, TiDB optimizes the process of loading statistics from multiple perspectives, such as the concurrency model and memory allocation, to reduce latency, improve throughput, and avoid slow loading of statistics that affects business scaling.

    Adaptive concurrent loading is now supported. By default, the configuration item [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) is set to a `0`, and the concurrency of statistics loading is automatically selected based on the hardware specification. 

   For more information, see [documentation](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540).

### Availability

* TiProxy supports multiple load balancing policies [#465](https://github.com/pingcap/tiproxy/issues/465) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@Oreoxmt** <!--1777-->

    TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB. Before v8.2.0, TiProxy defaults to v1.0.0, which only supports status-based and connection count-based load balancing policies for TiDB servers.

    Starting from v8.2.0, TiProxy defaults to v1.1.0 and introduces multiple load balancing policies. In addition to status-based and connection count-based policies, TiProxy supports dynamic load balancing based on health, memory, CPU, and location, improving the stability of the TiDB cluster.

    You can configure the combination and priority of load balancing policies through the [`policy`](/tiproxy/tiproxy-configuration.md#policy) configuration item.

    * `resource`: the resource priority policy performs load balancing based on the following priority order: status, health, memory, CPU, location, and connection count.
    * `location`: the location priority policy performs load balancing based on the following priority order: status, location, health, memory, CPU, and connection count.
    * `connection`: the minimum connection count priority policy performs load balancing based on the following priority order: status and connection count.

  For more information, see [documentation](/tiproxy/tiproxy-load-balance.md).

### SQL

* TiDB supports the JSON schema validation function [#52779](https://github.com/pingcap/tidb/issues/52779) @[dveeden](https://github.com/dveeden) **tw@hfxsd** <!--1840-->

    Before v8.2.0, you need to rely on external tools or customized validation logic for JSON data validation, which increases the complexity of development and maintenance, and reduces development efficiency. Starting from v8.2.0, the `JSON_SCHEMA_VALID()` function is introduced, which lets you verify the validity of JSON data directly in TiDB, improving the integrity and consistency of the data, and increasing the development efficiency.

    For more information, see [documentation](/functions-and-operators/json-functions.md#validation-functions).

### DB operations

* TiUP supports deploying PD microservices [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--1841-->

    Starting from v8.0.0, PD supports the microservice mode. This mode splits the timestamp allocation and cluster scheduling functions of PD into separate microservices that can be deployed independently, thereby improving resource control and isolation, and reducing the impact between different services. Before v8.2.0, PD microservices can only be deployed using TiDB Operator.

    Starting from v8.2.0, PD microservices can also be deployed using TiUP. You can deploy the `tso` microservice and the `scheduling` microservice separately in a cluster to enhance PD performance scalability and address PD performance bottlenecks in large-scale clusters. It is recommended to use this mode when PD becomes a significant performance bottleneck that cannot be resolved by scaling up.

    For more information, see [user documentation](/pd-microservices.md).

* Add privilege control of switching resource groups [#53440](https://github.com/pingcap/tidb/issues/53440) @[glorv](https://github.com/glorv) **tw@lilin90** <!--1740-->

    TiDB lets users switch to other resource groups using the [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) command or the [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) hint, which might lead to resource group abuse by some database users. TiDB v8.2.0 introduces privilege control of switching resource groups. Only database users granted the `RESOURCE_GROUP_ADMIN` or `RESOURCE_GROUP_USER` dynamic privilege can switch to other resource groups, enhancing the protection of system resources.

    To maintain compatibility, the original behavior is retained when upgrading from earlier versions to v8.2.0 or later versions. To enable the enhanced privilege control, set the new variable [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) to `ON`.

    For more information, see [user documentation](/tidb-resource-control.md#bind-resource-groups).

### Observability

* Record the reason why an execution plan is not cached [#50618](https://github.com/pingcap/tidb/issues/50618) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1819-->

    In some scenarios, you might want to cache most execution plans to save execution overhead and reduce latency. Currently, execution plan caching has some limitations on SQL. Execution plans of some SQL statements cannot be cached. It is difficult to identify the SQL statements that cannot be cached and the corresponding reasons. 

    Therefore, starting from v8.2.0, new columns `PLAN_CACHE_UNQUALIFIED` and `PLAN_CACHE_UNQUALIFIED_LAST_REASON` are added to the system table [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) to explain the reason why an execution plan cannot be cached, which can help you tune performance.

    For more information, see [documentation](/statement-summary-tables.md#fields-description).

### Security

* Enhance TiFlash log desensitization [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    TiDB v8.0.0 enhances the log desensitization feature, enabling you to control whether user data in TiDB logs is wrapped in markers `‹ ›`. Based on the marked logs, you can decide whether to redact the marked information when displaying logs, thereby increasing the flexibility of log desensitization. In v8.2.0, TiFlash introduces a similar enhancement for log desensitization. To use this feature, set the TiFlash configuration item `security.redact_info_log` to `marker`.

    For more information, see [documentation](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file).

### Data migration

* Align TiCDC Syncpoints across multiple changefeeds [#11212](https://github.com/pingcap/tiflow/issues/11212) @[hongyunyan](https://github.com/hongyunyan) **tw@lilin90** <!--1869-->

    Before v8.2.0, aligning TiCDC Syncpoints across multiple changefeeds was challenging. The `startTs` of the changefeed had to be carefully selected when the changefeed was created, so it would align with the Syncpoints of other changefeeds. Starting from v8.2.0, Syncpoints for a changefeed are created as a multiple of the changefeed's `sync-point-interval` configuration. This change lets you align Syncpoints across multiple changefeeds that have the same `sync-point-interval` configuration, simplifying and improving the ability to align multiple downstream clusters.

    For more information, see [documentation](/ticdc/ticdc-upstream-downstream-check.md#notes).

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.1.0 to the current version (v8.2.0). If you are upgrading from v8.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* When using TiDB Lightning to import a CSV file, if you set `strict-format = true` to split a large CSV file into multiple small CSV files to improve concurrency and import performance, you need to explicitly specify `terminator`. The values can be `\r`, `\n` or `\r\n`. Failure to specify a line terminator might result in an exception when parsing the CSV file data. [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

* When using `IMPORT INTO` to import a CSV file, if you specify the `SPLIT_FILE` parameter to split a large CSV file into multiple small CSV files to improve concurrency and import performance, you need to explicitly specify the line terminator `LINES_TERMINATED_BY`. The values can be `\r`, `\n` or `\r\n`. Failure to specify a line terminator might result in an exception when parsing the CSV file data. [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

* Before BR v8.2.0, performing [BR data restore](/br/backup-and-restore-overview.md) on a cluster with TiCDC replication tasks is not supported. Starting from v8.2.0, BR relaxes the restrictions on data restoration for TiCDC: if the BackupTS (the backup time) of the data to be restored is earlier than the changefeed [`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts) (the timestamp that indicates the current replication progress), BR can proceed with the data restore normally. Considering that `BackupTS` is usually much earlier, it can be assumed that in most scenarios, BR supports restoring data for a cluster with TiCDC replication tasks.

### MySQL compatibility

* 兼容性 1

* 兼容性 2

### System variables

| Variable name  | Change type   | Description |
|--------|------------------------------|------|
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760) | Modified  |  Changes the minimum value from `1` to `0`. When you set it to `0`, TiDB adaptively adjusts the concurrency based on the cluster size.**tw@hfxsd** <!--xxx--> |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720) | Modified  | Starting from v8.2.0, TiDB does not collect columns of `mediumtext` and `longtext` types by default to avoid potential OOM risks. **tw@hfxsd** <!--1759--> |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | Modified   |  Changes the default value from `ON` to `OFF`, which turns off historical statistics to avoid potential stability issues. **tw@hfxsd** <!--1759--> |
| [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50) | Modified | Add support for setting the concurrency of the `sort` operator. |
| [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) | Newly added | Controls whether privilege control is applied to the [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) statement and the [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) optimizer hint. **tw@lilin90** <!--1740--> |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650) | Modified    | Changes the minimum value from `1` to `0`. When you set it to `0`, TiDB adaptively adjusts the concurrency based on the cluster size.**tw@hfxsd** <!--xxx--> |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) | Modified | Changes the default value from `5` to `0`, and the minimum value from `1` to `0`. The value `0` means the automatic mode, which adjusts concurrency based on the configuration of the server. |
| TiDB | [`token-limit`](/tidb-configuration-file.md#token-limit) | Modified | Changes the maximum value from `18446744073709551615` (64-bit platform) and `4294967295` (32-bit platform) to `1048576`. It means that the number of sessions that can execute requests concurrently can be configured to a maximum of `1048576`. |
| TiKV | [`max-apply-unpersisted-log-limit`](/tikv-configuration-file.md#max-apply-unpersisted-log-limit-new-in-v820) | Newly added | Controls the maximum number of committed but not persisted Raft logs that can be applied。 The default value is `1024`. |
| TiFlash | [`security.redact_info_log`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | Introduces a new value option `marker`. When this option is enabled, all user data in the log is wrapped in `‹ ›`. |

### System tables

### Other changes

    - To improve the TiFlash development experience, the minimum version of LLVM required to compile and build TiDB has been upgraded from 13.0 to 17.0. If you are a TiDB developer, you need to upgrade the version of your LLVM compiler to ensure a smooth build. [#7193](https://github.com/pingcap/tiflash/issues/7193) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

## Offline package changes

## Deprecated features

* The following features are deprecated starting from v8.2.0:

    * Starting from v8.2.0, the [`enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800) configuration item is deprecated. The new version of the Region replica selector is used by default when sending RPC requests to TiKV.
    * Starting from v8.2.0, the BR snapshot restore parameter `--concurrency` is deprecated. As an alternative, you can configure the maximum number of concurrent tasks per TiKV node during snapshot restore using [`--tikv-max-restore-concurrency`](/br/use-br-command-line-tool.md#common-options). **tw@qiancai** <! --1850-->
    * Starting from v8.2.0, the BR snapshot restore parameter `--granularity` is deprecated, and the [coarse-grained Region scattering algorithm](/br/br-snapshot-guide.md#restore-cluster-snapshots) is enabled by default. **tw@qiancai** <! --1850-->

* The following features are planned for deprecation in future versions:

    * In v8.0.0, TiDB introduces the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable to control whether to enable the priority queue to optimize the ordering of automatic statistics collection tasks. In future versions, the priority queue will become the only way to order automatic statistics collection tasks, and the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable will be deprecated.
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * In v7.5.0, TiDB introduces the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable to enable TiDB to merge partition statistics asynchronously to avoid OOM issues. In future versions, partition statistics will be merged asynchronously by default, and the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable will be deprecated.
    * It is planned to redesign [the auto-evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by `conflict.threshold`, which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB <!--tw@hfxsd: 13 条-->

    - Support parallel execution of [logical DDL statements (General DDL)](/ddl-introduction.md#types-of-ddl-statements). Compared with v8.1.0, when you use 10 sessions to submit different DDL statements concurrently, the performance is improved by 3 to 6 times [#53246](https://github.com/pingcap/tidb/issues/53246) @[D3Hunter](https://github.com/D3Hunter)
    - Improve the logic of matching multi-column indexes with expressions like `((a = 1 and b = 2 and c > 3) or (a = 4 and b = 5 and c > 6)) and d > 3` to produce a more accurate `Range` [#41598](https://github.com/pingcap/tidb/issues/41598) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - Optimize the performance of obtaining data distribution information when performing simple queries on tables with large data volumes [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)
    - The aggregated result set can be used as an inner table for IndexJoin, allowing more complex queries to be matched to IndexJoin, thus improving query efficiency through indexing [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520)
    - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing `TRUNCATE` and `DROP` on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - The `CREATE USER` SQL statement supports the `PASSWORD REQUIRE CURRENT DEFAULT` option for compatibility with MySQL [#53305](https://github.com/pingcap/tidb/issues/53305) @[https://github.com/dveeden](dveeden)
    - Upgrade the version of Azure Identity Libraries and Microsoft Authentication Library to enhance security [#53990](https://github.com/pingcap/tidb/issues/53990) @[hawkingrei](https://github.com/hawkingrei)
    - Set the maximum value of `token-limit` to `1048576` to avoid setting it too large and causing TiDB Server OOM [#53312](https://github.com/pingcap/tidb/issues/53312) @[djshow832](https://github.com/djshow832)
    - Improve column pruning for MPP execution plans to improve TiFlash MPP execution performance [#52133](https://github.com/pingcap/tidb/issues/52133) @[yibin87](https://github.com/yibin87)
    - Optimize the performance overhead of the `IndexLookUp` operator when looking up a table with a large amount of data (>1024 rows) 优化 `IndexLookUp` [#53871](https://github.com/pingcap/tidb/issues/53871) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > 改进提升> TiDB - 在 MPP 负载均衡时移除不包含任何 Region 的 Store [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV <!--tw@lilin90: 9 条-->

    - Support pushing down the `json_merge_patch` function to TiKV [#16770](https://github.com/tikv/tikv/issues/16770) @[dbsid](https://github.com/dbsid)
    - Add a metric to show the number of SST files involved in a single compaction job [#16837](https://github.com/tikv/tikv/issues/16837) @[zhangjinpeng87](https://github.com/zhangjinpeng87)
    - Enable the early apply feature by default. With this feature enabled, the Raft leader can apply logs after quorum peers have persisted the logs, without waiting for the leader itself to persist the log, reducing the impact of jitter in a few TiKV nodes on write request latency [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - Introduce a precheck mechanism before generating a snapshot to ensure that the snapshot is sent only when the follower is ready, improving the effectiveness of snapshot generation [#15972](https://github.com/tikv/tikv/issues/15972) @[hbisheng](https://github.com/hbisheng)
    - 在 Raft 日志持久化之前，将 Raft 日志保留在缓存中，以提升 follower 对日志的读取性能 [#16717](https://github.com/tikv/tikv/issues/16717) @[glorv](https://github.com/glorv)
    - 增加 Raft dropped messages 事件的可观测性，以便定位写入慢的根本原因 [#17093](https://github.com/tikv/tikv/issues/17093) @[Connor1996](https://github.com/Connor1996)
    - 增加对 ingest file 的延迟可观测性，以便排查集群的延迟问题 [#17078](https://github.com/tikv/tikv/issues/17078) @[LykxSassinator](https://github.com/LykxSassinator)
    - 利用单独的线程来进行副本清理工作，保证 Raft 读写关键路径的延迟稳定 [#16001](https://github.com/tikv/tikv/issues/16001) @[hbisheng](https://github.com/hbisheng)
    - 提升正在进行 apply 的副本数的可观测性 [#17078](https://github.com/tikv/tikv/issues/17078) @[hbisheng](https://github.com/hbisheng)

+ PD <!--tw@lilin90: 2 条-->

    - 优化提升 Region 心跳处理的性能 [#7897](https://github.com/tikv/pd/issues/7897) @[nolouch](https://github.com/nolouch) @[rleungx](https://github.com/rleungx) @[JmPotato](https://github.com/JmPotato)
    - pd-ctl 支持使用 byte 或 query 维度来进行热点 Region 查询 [#7369](https://github.com/tikv/pd/issues/7369) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 条-->

    - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - Eliminate redundant copies of the Join Key in the `Join` operator [#9057](https://github.com/pingcap/tiflash/issues/9057) @[gengliqi](https://github.com/gengliqi)
    - Concurrently perform the process of converting a two-level hash table in the `HashAgg` operator [#8956](https://github.com/pingcap/tiflash/issues/8956) @[gengliqi](https://github.com/gengliqi)
    - Remove redundant aggregation functions for the `HashAgg` operator to reduce computational overhead [#8891](https://github.com/pingcap/tiflash/issues/8891) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 条-->

        - Optimize the backup feature, improving backup performance and stability during node restarts, cluster scaling-out, and network jitter when backing up large numbers of tables [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer) **tw@qiancai** <!--1844-->
        - Implement fine-grained checks of TiCDC changefeed during data restore. If the changefeed [`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts) is later than the data backup time, the restore operation are not affected, thereby reducing unnecessary wait times and improving user experience [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->
        - Add several commonly used parameters to the [`BACKUP`](/sql-statements/sql-statement-backup.md) statement and the [`RESTORE`](sql-statements/sql-statement-restore.md) statement, such as `CHECKSUM_CONCURRENCY` [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1849-->
        - Except for the `br log restore` subcommand, all other `br log` subcommands support skipping the loading of the TiDB `domain` data structure to reduce memory consumption [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - Support encryption of temporary files generated during log backup [#15083](https://github.com/tikv/tikv/issues/15083) @[YuJuncen](https://github.com/YuJuncen)
        - Add a `tikv_log_backup_pending_initial_scan` monitoring metric in the Grafana dashboard [#16656](https://github.com/tikv/tikv/issues/16656) @[3pointer](https://github.com/3pointer)
        - Optimize the output format of PITR logs and add a `RestoreTS` field in the logs [#53645](https://github.com/pingcap/tidb/issues/53645) @[dveeden](https://github.com/dveeden)

    + TiCDC

        - (dup): release-6.5.10.md > 改进提升> Tools> TiCDC - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB <!--tw@qiancai: 以下 9 条-->

    - Fix the issue that when a SQL statement contains an Outer Join and the Join condition includes the `false IN (column_name)` expression, the query result lacks some data [#49476](https://github.com/pingcap/tidb/issues/49476) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - Fix the issue that statistics for columns in system tables are collected when TiDB collects `PREDICATE COLUMNS` statistics for tables [#53403](https://github.com/pingcap/tidb/issues/53403) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that the `tidb_enable_column_tracking` system variable does not take effect when the `tidb_persist_analyze_options` system variable is set to `OFF` [#53478](https://github.com/pingcap/tidb/issues/53478) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue of potential data races during the execution of `(*PointGetPlan).StatsInfo()` [#49803](https://github.com/pingcap/tidb/issues/49803) [#43339](https://github.com/pingcap/tidb/issues/43339) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB might return incorrect query results when you query tables with virtual columns in transactions that involve data modification operations [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `tidb_enable_async_merge_global_stats` and `tidb_analyze_partition_concurrency` system variables do not take effect during automatic statistics collection [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that TiDB might return the `plan not supported` error when you query `TABLESAMPLE` [#54015](https://github.com/pingcap/tidb/issues/54015) @[tangenta](https://github.com/tangenta)
    - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that queries cannot be terminated after a data read timeout on the client side [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12) **tw@Oreoxmt** <!--1636-->
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `Longlong` 类型在谓词中溢出的问题 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复窗口函数中有某些子查询时可能会 panic 的问题 [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 TopN 算子可能被错误地下推的问题 [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复在聚簇索引作为谓词时 `SELECT INTO OUTFILE` 不生效的问题 [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `YEAR` 类型的列与超出范围的无符号整数进行比较导致错误结果的问题 [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复重启 TiDB 后，主键列统计信息中的直方图和 TopN 未被加载的问题 [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复 Massively Parallel Processing (MPP) 中 `final` AggMode 和 `non-final` AggMode 无法共存的问题 [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复执行谓词总是为 `true` 的 `SHOW ERRORS` 语句导致 TiDB panic 的问题 [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复在递归 CTE 中无法使用视图的问题 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复 TiDB 启动加载统计信息时可能因为 GC 推进报错的问题 [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复将数据从 `FLOAT` 类型转换为 `UNSIGNED` 类型时结果错误的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复创建带有外键的表时，TiDB 未创建对应的统计信息元信息 (`stats_meta`) 的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复关闭 `tidb_enable_async_merge_global_stats` 时，GlobalStats 中的 `Distinct_count` 信息可能错误的问题 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > 错误修复> TiDB - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei) <!--tw@Oreoxmt: 以下 18 条-->
    - Fix the issue that negating a time type results in an incorrect value [#52262](https://github.com/pingcap/tidb/issues/52262) @[solotzg](https://github.com/solotzg)
    - Fix the issue that `REGEXP()` does not explicitly report an error for empty pattern arguments [#53221](https://github.com/pingcap/tidb/issues/53221) @[yibin87](https://github.com/yibin87)
    - Fix the issue that converting JSON to datetime might lose precision in some cases [#53352](https://github.com/pingcap/tidb/issues/53352) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `JSON_QUOTE()` returns incorrect results in some cases [#37294](https://github.com/pingcap/tidb/issues/37294) @[dveeden](https://github.com/dveeden)
    - Fix the issue that `ALTER TABLE ... REMOVE PARTITIONING` might cause data loss [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that JSON-related functions return errors inconsistent with MySQL in some cases [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the `INDEX_LENGTH` field of partitioned tables in `INFORMATION_SCHEMA.PARTITIONS` is displayed incorrectly [#54173](https://github.com/pingcap/tidb/issues/54173) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `TIDB_ROW_ID_SHARDING_INFO` field in the `INFOMATION_SCHEMA.TABLES` table is displayed incorrectly [#52330](https://github.com/pingcap/tidb/issues/52330) @[tangenta](https://github.com/tangenta)
    - Fix the issue that a generated columns returns illegal timestamps [#52509](https://github.com/pingcap/tidb/issues/52509) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that setting `max-index-length` causes TiDB to panic when adding indexes using the Distributed eXecution Framework (DXF) [#53281](https://github.com/pingcap/tidb/issues/53281) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - Fix the issue that using `CURRENT_DATE()` as the default value for a column results in incorrect query results [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `ALTER DATABASE ... SET TIFLASH REPLICA` statement incorrectly adds TiFlash replicas to the `SEQUENCE` table [#51990](https://github.com/pingcap/tidb/issues/51990) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the `REFERENCED_TABLE_SCHEMA` field in the `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` table is displayed incorrectly [#52350](https://github.com/pingcap/tidb/issues/52350) @[wd0517](https://github.com/wd0517)
    - Fix the issue that inserting multiple rows in a single statement causes the `AUTO_INCREMENT` column to be discontinuous when `AUTO_ID_CACHE=1` [#52465](https://github.com/pingcap/tidb/issues/52465) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the format of deprecation warnings [#52515](https://github.com/pingcap/tidb/issues/52515) @[dveeden](https://github.com/dveeden)
    - Fix the issue that the `TRACE` command is missing in `copr.buildCopTasks` [#53085](https://github.com/pingcap/tidb/issues/53085) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that bindings containing `memory_quota` might not work in subqueries [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
+ TiKV <!--tw@lilin90: 以下 10 条-->

    - 修复不稳定测试用例 test_raw_put_key_guard [#16825](https://github.com/tikv/tikv/issues/16825) @[pingyu](https://github.com/pingyu)
    - 修复不稳定测试用例 test_rawkv::test_leader_transfer [#16789](https://github.com/tikv/tikv/issues/16789) @[pingyu](https://github.com/pingyu)
    - 修复 json_array_append panic 问题 [#16930](https://github.com/tikv/tikv/issues/16930) @[dbsid](https://github.com/dbsid)
    - 修复 leader 不及时清理失败的 snapshot 文件的问题 [#16976](https://github.com/tikv/tikv/issues/16976) @[hbisheng](https://github.com/hbisheng)
    - 修复高并发 coprocessor 请求可能导致 TiKV OOM 的问题 [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - 修复在线变更 raftstore.periodic-full-compact-start-time 参数可能会 panic 的问题 [#17066](https://github.com/tikv/tikv/issues/17066) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复 `make docker` 和 `make docker_test` 失败的问题 [#17075](https://github.com/tikv/tikv/issues/17075) @[shunki-fujita](https://github.com/shunki-fujita)
    - 修复 gRPC source duration 在监控中显示错误的问题 [#17133](https://github.com/tikv/tikv/issues/17133) @[King-Dylan](https://github.com/King-Dylan)
    - 修复 gRPC 设置压缩方式对 TiKV 发送到 TiDB 的消息不起作用的问题 [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.2.md > 错误修复> TiKV - 修复 tikv-ctl 的 `raft region` 命令的输出中未包含 Region 状态信息的问题 [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - 修复 CDC 和 log-backup 没有用 `advance-ts-interval` 配置限制 `check_leader` 的 timeout 的问题，这在一些情况下可能导致 TiKV 正常重启时 resolved ts lag 过大 [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - (dup): release-7.5.2.md > 错误修复> PD - 修复 `ALTER PLACEMENT POLICY` 无法修改 placement policy 的问题 [#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.1.5.md > 错误修复> PD - 修复写热点调度可能会违反放置策略 (placement policy) 约束的问题 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-6.5.10.md > 错误修复> PD - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.2.md > 错误修复> PD - 修复取消资源组查询导致大量重试的问题 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.2.md > 错误修复> PD - 修复手动切换 PD leader 可能失败的问题 [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)

+ TiFlash <!--tw@hfxsd: 1 条-->

    - (dup): release-7.5.2.md > 错误修复> TiFlash - 修复在含空分区的分区表上执行查询时，可能会超时的问题 [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.2.md > 错误修复> TiFlash - 修复在存算分离架构下，DDL 新增带有 not null 属性的列后，查询可能返回错误的 null 值的问题 [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.10.md > 错误修复> TiFlash - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that a large number of duplicates might be read in FastScan mode after importing data via br or TiDB Lightning [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 5 条-->

        - (dup): release-7.5.2.md > 错误修复> Tools> Backup & Restore (BR) - 修复由于 `EndKey` 为空导致恢复事务 KV 集群失败的问题 [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PD 连接失败导致日志备份 advancer owner 所在的 TiDB 可能崩溃的问题 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > 错误修复> Tools> Backup & Restore (BR) - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that the connection used to fetch TiKV configurations might not be closed [#52595](https://github.com/pingcap/tidb/issues/52595) @[RidRisR](https://github.com/RidRisR)
       - Fix the issue that the `TestStoreRemoved` test case is unstable [#52791](https://github.com/pingcap/tidb/issues/52791) @[YuJuncen](https://github.com/YuJuncen)
       - Fix the issue that TiFlash crashes during PITR restore [#52628](https://github.com/pingcap/tidb/issues/52628) @[RidRisR](https://github.com/RidRisR)
       - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
       - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@hfxsd: 2 条-->

        - Fix inaccurate display of the **Kafka Outgoing Bytes** panel in Grafana [#10777](https://github.com/pingcap/tiflow/issues/10777) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that data inconsistency might occur when restarting Changefeed repeatedly when performing a large number of `UPDATE` operations in a multi-node environment [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)

    + TiDB Data Migration (DM) <!--tw@Oreoxmt: 1 条-->

        - (dup): release-7.5.2.md > 错误修复> Tools> TiDB Data Migration (DM) - 升级 `go-mysql` 以修复连接阻塞的问题 [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that `SET` statements cause DM to panic when migrating MariaDB data [#10206](https://github.com/pingcap/tiflow/issues/10206) @[dveeden](https://github.com/dveeden)

    + TiDB Lightning <!--tw@Oreoxmt: 1 条-->

        - Fix the issue that TiDB Lightning might report an error when importing zstd compressed files [#53587](https://github.com/pingcap/tidb/issues/53587) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - (dup): release-6.5.10.md > 错误修复> Tools> Dumpling - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog

        - (dup): release-6.5.10.md > 错误修复> Tools> TiDB Binlog - 修复开启 TiDB Binlog 后，在 `ADD COLUMN` 执行过程中删除行可能报错 `data and columnID count not match` 的问题 [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [CabinfeverB](https://github.com/CabinfeverB)
- [DanRoscigno](https://github.com/DanRoscigno) (First-time contributor)
- [ei-sugimoto](https://github.com/ei-sugimoto) (First-time contributor)
- [eltociear](https://github.com/eltociear)
- [jiyfhust](https://github.com/jiyfhust)
- [michaelmdeng](https://github.com/michaelmdeng) (First-time contributor)
- [mittalrishabh](https://github.com/mittalrishabh)
- [onlyacat](https://github.com/onlyacat)
- [qichengzx](https://github.com/qichengzx) (First-time contributor)
- [SeaRise](https://github.com/SeaRise)
- [shawn0915](https://github.com/shawn0915)
- [shunki-fujita](https://github.com/shunki-fujita) (First-time contributor)
- [tonyxuqqi](https://github.com/tonyxuqqi)
- [wwu](https://github.com/wwu) (First-time contributor)
- [yzhan1](https://github.com/yzhan1)
