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
    <td>HashAgg is a widely used aggregation operator in TiDB for efficiently aggregating rows with the same field values. TiDB v8.0.0 introduces parallel HashAgg as an experimental feature to further enhance processing speed. When memory resources are insufficient, parallel HashAgg spills temporary sorted data to disk, avoiding potential OOM risks caused by excessive memory usage. This improves performance while maintaining node stability. In v8.2.0, this feature becomes generally available (GA), enabling you to safely configure the concurrency of parallel HashAgg.</td>
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

    TiDB v8.0.0 introduces the parallel HashAgg algorithm with disk spill support as an experimental feature. In v8.2.0, this feature becomes generally available (GA). When using the parallel HashAgg algorithm, TiDB automatically triggers data spill based on memory usage, thus balancing performance and data throughput. This feature is enabled by default. The system variable `tidb_enable_parallel_hashagg_spill`, which controls this feature, will be deprecated in a future release.

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

* 记录执行计划没有被缓存的原因 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1819-->

    在一些场景下，用户希望多数执行计划能够被缓存，以节省执行开销，并降低延迟。目前执行计划缓存对 SQL 有一定限制，部分形态 SQL 的执行计划无法被缓存，但是用户很难识别出无法被缓存的 SQL 以及对应的原因。因此，在新版本中，我们向系统表 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 中增加了新的列，解释计划无法被缓存的原因，协助用户做性能调优。

    更多信息，请参考[用户文档](/statement-summary-tables.md#表的字段介绍)。

### Security

* Enhance TiFlash log desensitization [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    TiDB v8.0.0 enhances the log desensitization feature. You can control whether to desensitize log information to enable secure use of TiDB logs in different scenarios, enhancing the security and flexibility of using log desensitization. In v8.2.0, TiFlash introduces a similar enhancement for log desensitization. To use this feature, set the TiFlash configuration item `security.redact_info_log` to `marker`.

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

* TiDB Lightning，从 v8.2.0 开始当用户设置 strict-format = true，来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需要显式指定行结束符 terminator 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。
* Import Into SQL 语法，从 v8.2.0 开始，当用户导入 CSV 文件，且指定 split 参数来切分大的 CSV 文件为多个小的 CSV 文件来提升并发和导入性能时，需显式指定行结束符 LINES_TERMINATED_BY 参数的取值为  \r，\n 或 \r\n 。否则可能导致 CSV 文件数据解析异常。

* 行为变更 2

### MySQL compatibility

* 兼容性 1

* 兼容性 2

### System variables

| Variable name  | Change type   | Description |
|--------|------------------------------|------|
| [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) | 废弃 | **tw@Oreoxmt** <!--1842--> |
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

- Before BR v8.2.0, performing [BR data restore](/br/backup-and-restore-overview.md) on a cluster with TiCDC replication tasks is not supported. Starting from v8.2.0, BR relaxes the restrictions on data restoration for TiCDC: if the BackupTS (the backup time) of the data to be restored is earlier than the changefeed [`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts) (the timestamp that indicates the current replication progress), BR can proceed with the data restore normally. Considering that `BackupTS` is usually much earlier, it can be assumed that in most scenarios, BR supports restoring data for a cluster with TiCDC replication tasks.

## Offline package changes

## Deprecated features

* The following features are deprecated starting from v8.2.0:

    * Starting from v8.2.0, the [`enable-replica-selector-v2`](/tidb-configuration-file.md#enable-replica-selector-v2-new-in-v800) configuration item is deprecated. The new version of the Region replica selector is used by default when sending RPC requests to TiKV.
    * Starting from v8.2.0, the BR snapshot restore parameter `--concurrency` is deprecated. As an alternative, you can configure the maximum number of concurrent tasks per TiKV node during snapshot restore using [`--tikv-max-restore-concurrency`](/br/use-br-command-line-tool.md#common-options). **tw@qiancai** <! --1850-->
    * Starting from v8.2.0, the BR snapshot restore parameter `--granularity` is deprecated, and the [coarse-grained Region scattering algorithm](/br/br-snapshot-guide.md#restore-cluster-snapshots) is enabled by default. **tw@qiancai** <! --1850-->

* The following features are planned for deprecation in future versions:

    * In v8.0.0, TiDB introduces the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable to control whether to enable the priority queue to optimize the ordering of automatic statistics collection tasks. In future versions, the priority queue will become the only way to order automatic statistics collection tasks, and the [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) system variable will be deprecated.
    * In v7.5.0, TiDB introduces the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable to enable TiDB to merge partition statistics asynchronously to avoid OOM issues. In future versions, partition statistics will be merged asynchronously by default, and the [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) system variable will be deprecated.
    * It is planned to redesign [the auto-evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by `conflict.threshold`, which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - Improve the performance when retrieving data distribution information for simple queries on tables with a large amount of data [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06) **tw@Oreoxmt** <!--1561-->
    - The aggregated result set can be used as an inner table for IndexJoin, allowing more complex queries to match with IndexJoin, thus improving query efficiency through the indices [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@hfxsd** <!--1510-->

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

        - Optimize the backup feature, improving backup stability and performance during node restarts, cluster scaling-out, and network jitter when backing up large numbers of tables [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer) **tw@qiancai** <!--1844-->
        - Implement fine-grained checks of TiCDC changefeed during data restore. If the changefeed [`CheckpointTS`](/ticdc/ticdc-architecture.md#checkpointts) is later than the data backup time, the restore operation are not affected, thereby reducing unnecessary wait times and improving user experience [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->
        - Add several commonly used parameters to the [`BACKUP`](/sql-statements/sql-statement-backup.md) statement and the [`RESTORE`](sql-statements/sql-statement-restore.md) statement, such as `CHECKSUM_CONCURRENCY` [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1849-->
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

## Bug fixes

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - Fix the issue that queries cannot be terminated after a data read timeout on the client side [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12) **tw@Oreoxmt** <!--1636-->

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
