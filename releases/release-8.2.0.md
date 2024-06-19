---
title: TiDB 8.2.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.2.0.
---

# TiDB 8.2.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.2.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.2/quick-start-with-tidb)

8.2.0 introduces the following key features and improvements:

## Feature details

### Scalability

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### Performance

* 支持下推以下字符串函数到 TiKV [#50601](https://github.com/pingcap/tidb/issues/50601) @[dbsid](https://github.com/dbsid)  **tw@Oreoxmt** <!--1663-->

    * `JSON_ARRAY_APPEND()`
    * `JSON_MERGE_PATCH()`
    * `JSON_REPLACE()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* TiDB 支持并行排序功能 [#49217](https://github.com/pingcap/tidb/issues/49217) [#50746](https://github.com/pingcap/tidb/issues/50746) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1665-->

    在 v8.2.0 版本之前，TiDB 进行排序计算时只能以非并行的方式进行处理，当需要对大量数据进行排序时，查询性能受到影响。

    在 v8.2.0 版本中，TiDB 支持并行排序功能，所有的排序计算性能都将得到提升。该功能不需要单独开启，TiDB 将根据变量 [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入) 的设定，确定使用并行方式或非并行方式进行排序。

* TiDB 的并发 HashAgg 算法支持数据落盘（GA）[#35637](https://github.com/pingcap/tidb/issues/35637) @[xzhangxian1008](https://github.com/xzhangxian1008)  **tw@Oreoxmt** <!--1842-->

    在 v8.0.0 中，TiDB 以实验特性发布了并发 HashAgg 算法支持数据落盘功能。

    在 v8.2.0 中，TiDB 正式发布该功能。TiDB 在使用并发 HashAgg 算法时，将根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。该功能默认打开，变量 `tidb_enable_concurrent_hashagg_spill` 将被废弃。

* 提升备份百万表场景的备份稳定性以及性能。解决备份过程中因为各种原因(节点重启/扩容/网络问题)带来的长尾问题。 [#52534](https://github.com/pingcap/tidb/issues/52534) @[3pointer](https://github.com/3pointer) **tw@qiancai** <!--1844-->

### Reliability

* Improve statistics loading efficiency by up to 10 times [#52831](https://github.com/pingcap/tidb/issues/52831) @[hawkingrei](https://github.com/hawkingrei) **tw@hfxsd** <!--1754-->

    SaaS or PaaS applications can have a large number of data tables, which not only slow down the loading speed of the initial statistics, but also increase the failure rate of synchronizing loads under high loads. The startup time of TiDB and the accuracy of the execution plan can be affected. In v8.2.0, TiDB optimizes the process of loading statistics from multiple perspectives, such as concurrency model and memory allocation, to reduce latency, improve throughput, and avoid slow loading of statistics that affects business scaling.

    Adaptive concurrent loading is now supported. By default, the configuration item [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) is set to a `0`, and the concurrency of statistics loading is automatically selected based on the hardware specification. 

   For more information, see [documentation](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540).

### Availability

* TiProxy 支持多种负载均衡策略 [#465](https://github.com/pingcap/tiproxy/issues/465) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)  **tw@Oreoxmt** <!--1777-->

    TiProxy 是 TiDB 的官方代理组件，位于客户端和 TiDB server 之间，为 TiDB 集群提供负载均衡、连接保持功能。在 v8.2.0 之前，TiProxy 默认使用 v1.0.0 版本，只能基于状态和连接数进行负载均衡。
    在 v8.2.0 中，TiProxy 默认使用 v1.1.0 版本，引入了多种负载均衡策略，除了状态和连接数，还可以根据健康度、资源、地理位置等信息，对 TiDB 集群的连接进行动态负载均衡调度，使整个 TiDB 集群更加稳定。

    TiProxy 的负载均衡策略可以通过配置项进行配置，具体策略包括：
    * `resource`: 资源优先策略，优先级顺序依次为基于状态、健康度、内存、CPU、地理位置、连接数的负载均衡。
    * `location`: 地理优先策略，优先级顺序依次为基于状态、地理位置、健康度、内存、CPU、连接数的负载均衡。
    * `connection`: 最小连接数策略，优先级顺序依次为基于状态、连接数的负载均衡。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-load-balance.md)。

### SQL

* TiDB 支持 JSON Schema Validation 函数 [#52780](https://github.com/pingcap/tidb/pull/52780) @[dveeden](https://github.com/dveeden) **tw@hfxsd** <!--1840-->

    Before v8.2.0, you need to rely on external tools or customized validation logic for JSON data validation, which increases the complexity of development and maintenance, and reduces development efficiency. Starting from v8.2.0, the `JSON_SCHEMA_VALID()` function is introduced, which allows you to verify the validity of JSON data directly in TiDB, improving the integrity and consistency of the data, and increasing the development efficiency.

    For more information, see [documentation](/functions-and-operators/json-functions.md#validation-functions).

### DB operations

* TiUP 支持部署 PD 微服务 [#5766](https://github.com/tikv/pd/issues/5766) @[rleungx](https://github.com/rleungx) **tw@qiancai** <!--1841-->

   通过将 PD 拆分成多个单独的服务，独立部署进行管理，可以更好地控制资源的使用和隔离，减少不同服务相互之间的影响。从 v8.2.0 开始，TiUP 支持将 PD 以微服务的模式进行部署，用户可以将 TSO 微服务和 Scheduling 微服务，单独进行部署，实现资源隔离以及快速迭代的目的。 

    更多信息，请参考[用户文档]()。

* 为切换资源组的操作增加权限控制 [#issue号](链接) @[glorv](https://github.com/glorv) **tw@lilin90** <!--1740-->

    TiDB 允许用户利用命令 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 或 Hint [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 切换到其他资源组，这可能会造成部分数据库用户对资源组的滥用。TiDB v8.2.0 增加了对资源组切换行为的管控，只有被授予动态权限 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 的数据库用户，才能切换到其他资源组，加强对系统资源的保护。

    为了维持兼容性，从旧版本升级的集群维持原行为不变。通过设置新增变量 [`tidb_resource_control_strict_mode`](/system-variables.md) 为 `ON` ，开启上述的增强权限控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#绑定资源组)。

### Observability

* 记录执行计划没有被缓存的原因 [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@hfxsd** <!--1819-->

    在一些场景下，用户希望多数执行计划能够被缓存，以节省执行开销，并降低延迟。目前执行计划缓存对 SQL 有一定限制，部分形态 SQL 的执行计划无法被缓存，但是用户很难识别出无法被缓存的 SQL 以及对应的原因。因此，在新版本中，我们向系统表 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 中增加了新的列，解释计划无法被缓存的原因，协助用户做性能调优。

    更多信息，请参考[用户文档](/statement-summary-tables.md#表的字段介绍)。

### Security

* 增强 TiFlash 日志脱敏 [#8977](https://github.com/pingcap/tiflash/issues/8977) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@Oreoxmt** <!--1818-->

    在 v8.0.0 版本，TiDB 增强了日志脱敏功能，可以控制是否对日志信息进行脱敏，以实现在不同场景下安全使用 TiDB 日志，提升了使用日志脱敏能力的安全性和灵活性。在 v8.2.0 版本中，TiFlash 进行了类似的日志脱敏功能增强。要使用此功能，需要将 tiflash-server 中 `security.redact_info_log` 配置项的值设为 `MARKER`。

    更多信息，请参考[用户文档](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。

### Data migration

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
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760) | Modified  |  Changes the minimum value from `1` to `0`. When you set it to `0`, it adapts the concurrency based on the cluster size.**tw@hfxsd** <!--xxx--> |
| [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720) | Modified  | Starting from v8.2.0, TiDB does not collect columns of `mediumtext` and `longtext` types by default to avoid potential OOM risks. **tw@hfxsd** <!--1759--> |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | Modified   |  Changes the default value from `ON` to `OFF`, which turns off historical statistics to avoid potential stability issues. **tw@hfxsd** <!--1759--> |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650) | Modified    | Changes the minimum value from `1` to `0`. When you set it to `0`, it adapts the concurrency based on the cluster size.**tw@hfxsd** <!--xxx--> |
|        |                              |      |
|        |                              |      |

### Configuration file parameters
| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) | Modified | Changes the default value from `5` to `0`, and the minimum value from `1` to `0`. The value `0` means the automatic mode, which adjusts concurrency based on the configuration of the server. |

### System tables

### Other changes

## Offline package changes

## Deprecated features

* 从 v8.0.0 开始，变量 [`tidb_enable_concurrent_hashagg_spill`](/system-variables.md#tidb_enable_concurrent_hashagg_spill-从-v800-版本开始引入) 被废弃。
* 从 v8.0.0 开始，BR 快照恢复参数 [`concurrency`](/use-br-command-line-tool#常用选项) 被废弃。 **tw@qiancai** <!--1850-->
* 从 v8.0.0 开始，BR 快照恢复参数 [`granularity`](/br-snapshot-guide#快照恢复的性能与影响) 被废弃。**tw@qiancai** <!--1850-->

## Improvements

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - 优化客户端读取数据超时无法终止查询的问题 [#44009](https://github.com/pingcap/tidb/issues/44009) @[wshwsh12](https://github.com/wshwsh12)  **tw@Oreoxmt** <!--1636-->
    - 优化对大数据量的表进行简单查询的性能 [#53850](https://github.com/pingcap/tidb/issues/53850) @[you06](https://github.com/you06)  **tw@Oreoxmt** <!--1561-->
    - The aggregated result set can be used as an inner table for IndexJoin, allowing more complex queries to be matched to IndexJoin, thus improving query efficiency through the indices [#37068](https://github.com/pingcap/tidb/issues/37068) @[elsa0520](https://github.com/elsa0520) **tw@hfxsd** <!--1510-->

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

        - 优化恢复过程中对 Changefeed 的细粒度检查，如果 Changefeed 的检查点时间（Checkpoint）大于备份时间，则不会影响正常的恢复操作，减少恢复的不必要等待时间，提升用户体验 [#53131](https://github.com/pingcap/tidb/issues/53131) @[YuJuncen](https://github.com/YuJuncen) **tw@qiancai** <!--1843-->
        - 为 [`BACKUP`](/sql-statements/sql-statement-backup.md) 语句和 [`RESTORE`](sql-statements/sql-statement-restore.md) 语句添加了若干常用的参数选项，例如 `CHECKSUM_CONCURRENCY` [#53040](https://github.com/pingcap/tidb/issues/53040) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--1849-->
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