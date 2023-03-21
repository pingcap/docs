---
title: TiDB 7.0.0 Release Notes
---

# TiDB 7.0.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.0.0-[DMR](/releases/versioning.md#development-milestone-releases)

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb) | [Installation package](https://www.pingcap.com/download/?version=v7.0.0#version-list)

In v7.0.0-DMR, the key new features and improvements are as follows:

@yiwen92

## Feature details

### Scalability

* TiFlash 引擎支持存算分离和对象存储（实验特性）[#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy) **tw:qiancai**

    在 v7.0.0 之前的版本中，TiFlash 引擎以存算一体的方式部署，即 TiFlash 节点即是存储节点，也是计算节点；同时，TiFlash 节点只能使用本地存储。存算一体的部署方式使得 TiFlash 的计算能力和存储能力无法独立扩展。在 v7.0.0 版本中，TiFlash 引擎新增存算分离架构，并在存算分离架构下，支持兼容 S3 API 的对象存储。在 TiFlash 存算分离架构下，TiFlash 节点分为计算节点和写节点。这两种节点都可以单独扩缩容，独立调整计算或数据存储能力。TiFlash 引擎的存算分离架构不能和存算一体架构混合使用、相互转换，需要在部署 TiFlash 时进行相应的配置设定，确定使用存算分离架构或者存算一体架构。

    For more information, see [documentation](/tiflash/tiflash-disaggregated-and-s3.md).

### Performance

* Achieve compatibility between [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) and PITR [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth) **tw:ran-huang**

    In TiDB v6.5.0, Fast Online DDL is not fully compatible with [PITR](/br/backup-and-restore-overview.md). To ensure full data backup, it is recommended to first stop the PITR background backup task, quickly add indexes using Fast Online DDL, and then resume the PITR backup task.

    Starting from TiDB v7.0.0, Fast Online DDL and PITR are fully compatible. When restoring cluster data through PITR, the index operations added via Fast Online DDL during log backup will be automatically replayed to achieve compatibility.

    For more information, see [documentation](/ddl-introduction.md).

* TiFlash 引擎支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子 [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi) **tw:Oreoxmt**

    `IN`、`NOT IN`、`=ANY`、`!= ALL` 算子引导的关联子查询会转化为 `Semi Join` 或 `Anti Semi Join`，从而提升计算性能。当转换后的 JOIN KEY 的列可能为 NULL 时，需要具有 Null-Aware 特性的 Join 算法，即需要 [`Null-Aware Semi Join`](/explain-subqueries#null-aware-semi-joinin-和--any-子查询) 和 [`Null-Aware Anti Semi Join`](/explain-subqueries#null-aware-anti-semi-joinnot-in-和--all-子查询) 算子。

    在 v7.0.0 之前的版本中，TiFlash 引擎不支持 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子，所以这几种子查询无法直接下推至 TiFlash 引擎进行计算。在 v7.0.0 版本中，TiFlash 引擎支持了 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子。当 SQL 包含这几种关联子查询，查询的表包含 TiFlash 副本，且启用 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md)时，优化器将自动判断是否将 `Null-Aware Semi Join` 和 `Null-Aware Anti Semi Join` 算子下推至 TiFlash 引擎进行计算以提升整体性能。

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations).

* TiFlash 引擎支持 FastScan 功能 [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan) **tw:Oreoxmt**

    TiFlash 引擎从 v6.3.0 版本发布了实验特性的快速扫描功能 (FastScan)。在 v7.0.0 版本中，该功能正式 GA。通过使用系统变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-从-v630-版本开始引入) 可以启用快速扫描功能。快速扫描功能通过牺牲强一致性保证，可以大幅提升扫表性能。如果对应的表只有 INSERT 操作，没有 UPDATE/DELETE 操作，则快速扫描功能在提升扫表性能的同时，不会损失强一致性。

    For more information, see [documentation](/develop/dev-guide-use-fastscan.md).

* TiFlash 引擎支持 Selection 延迟物化功能（实验特性） [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

    当 SELECT 语句中包含过滤条件（WHERE子句）时，普通的处理方式是扫描所有数据后进行过滤。Selection 延迟物化功能可以先扫描过滤条件相关列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少扫描 IO 和数据解析的计算量。在 v7.0.0 中，TiFlash 引擎支持 Selection 延迟物化功能，并通过 variable 控制是否启用该功能。当功能启用时，优化器会根据过滤条件的信息，自动判断选择哪些过滤条件下推到 TableScan 算子。

    For more information, see [documentation](/tiflash/tiflash-late-materialization.md).

* 非 prepared 语句的执行计划可以被缓存（实验特性）[#issue号](链接) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    执行计划缓存是提升并发 OLTP 负载能力的重要手段， TiDB 已经支持对 [prepared 语句的计划进行缓存](/sql-prepared-plan-cache.md)。 在 v7.0.0 中， 非 prepared 语句的执行计划也能够被缓存，使得执行计划缓存能够被应用在更广泛场景下，进而提升 TiDB 的并发处理能力。

    这个功能目前默认关闭， 用户通过变量 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 打开。 出于稳定性考虑，在当前版本中，TiDB 开辟了一块新的区域用于缓存非 prepare 语句的执行计划，通过变量 [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) 设置缓存大小；另外，对 SQL 的模式也有一定的限制，具体参见[文档](/sql-non-prepared-plan-cache.md#限制)。

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

* 解除执行计划缓存对子查询的限制 [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw:Oreoxmt**

    TiDB v7.0.0 移除了计划缓存对子查询的限制，带有子查询的 SQL 语句的执行计划可以被缓存，比如 " `select * from t where a > (select ...)` "。 这进一步扩大了执行计划缓存的应用范围，提升 SQL 的执行效率。

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* TiKV enables Raft log recycling by default [#14379](https://github.com/tikv/tikv/issues/14379) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    In v6.3.0, TiKV introduced the [Raft log recycling](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) feature to reduce long-tail latency caused by write load. In v7.0.0, this feature is enabled by default.

    For more information, see [documentation](/tikv-configuration-file.md#enable-log-recycle-new-in-v630).

* TiKV supports automatically generating empty log files for log recycling [#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    In v6.3.0, TiKV introduced the [Raft log recycling](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) feature to reduce long-tail latency caused by write load. However, log recycling can only take effect when the number of Raft log files reaches a certain threshold, making it difficult for users to directly experience the throughput improvement brought by this feature.

    In v7.0.0, a new configuration item called `raft-engine.prefill-for-recycle` was introduced to improve user experience. This item controls whether empty log files are generated for recycling when the process starts. When this configuration is enabled, TiKV automatically fills a batch of empty log files during initialization, ensuring that log recycling takes effect immediately after initialization.

    For more information, see [documentation](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700).

* 新增从[窗口函数](/functions-and-operators/expressions-pushed-down.md)中推导出 TopN/Limit 的优化规则，提升窗口函数的性能 [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker) **tw:qiancai**

* Support creating unique indexes through Fast Online DDL [#40730](https://github.com/pingcap/tidb/issues/40730) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v6.5.0 supports creating ordinary secondary indexes via Fast Online DDL. TiDB v7.0.0 supports creating unique indexes via Fast Online DDL. Compared to v6.1.0, adding unique indexes to large tables is expected to be several times faster with improved performance.

    For more information, see [documentation](/ddl-introduction.md).

### Reliability

* 支持基于资源组的资源管控 [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 正式发布了基于资源组的资源管控特性，该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，它允许用户将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    我们不仅提供了内置视图展示资源的实际使用情况，协助用户更合理地配置资源，还支持基于会话和语句级别（HINT）的动态资源管控能力。这些功能的引入将帮助用户更精确地掌控 TiDB 集群的资源使用情况，并根据实际需要动态调整配额。

    启用资源管控特性需要同时打开 TiDB 的全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 及 TiKV 的配置项 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)。当前支持的限额方式基于“[用量](/tidb-resource-control.md#什么是-request-unit-ru)”（Request Unit，即 RU），RU 是 TiDB 对 CPU、I/O 等系统资源的统一抽象单位。

    用户可以通过以下方式生效资源组：

    - 用户级别。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句将用户绑定到特定的资源组。将资源组绑定用户后，使用对应的用户创建的会话会自动绑定对应的资源组。
    - 会话级别。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话的资源组。
    - 语句级别。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 设置当前语句使用的资源组。

  For more information, see [documentation](/tidb-resource-control.md).

* Support a checkpoint mechanism for Fast Online DDL, improving fault tolerance and automatic recovery capability [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v7.0.0 introduces a checkpoint mechanism for [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630), which significantly improves its fault tolerance and automatic recovery capabilities. By periodically recording and synchronizing the DDL progress, ongoing DDL operations can continue to be executed in Fast Online DDL mode even if there is a TiDB DDL Owner failure or switch. This makes the execution of DDL more stable and efficient.

    For more information, see [documentation](/ddl-introduction.md).

* TiFlash supports spill-to-disk [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker) **tw:ran-huang**

    To improve execution performance, TiFlash runs data entirely in memory as much as possible. When the amount of data exceeds the total size of memory, TiFlash will terminate the query to avoid system crashes caused by running out of memory. Therefore, the amount of data that TiFlash can handle is limited by the available memory size.

    Starting from v7.0.0, TiFlash supports the spill-to-disk feature. By adjusting the threshold of memory usage for operators ([`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700), [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700), and [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)), you can control the maximum amount of memory that an operator can use. When the memory used by the operator exceeds the threshold, it will automatically write data to disk. This sacrifices some performance but allows for processing of more data.

    For more information, see [documentation](/tiflash/tiflash-spill-disk.md).

* Improve the efficiency of collecting statistics [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:ran-huang**

    In v7.0.0, TiDB further optimizes the logic of collecting statistics, reducing the collection time by about 25%. This optimization improves the operational efficiency and stability of large database clusters, reducing the impact of statistics collection on cluster performance.

* Add new optimizer hints for MPP optimization [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent) **tw:ran-huang**

    In v7.0.0, TiDB added a series of optimizer hints to influence the generation of MPP execution plans.

    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name-tl_name): takes effect on MPP. It hints the optimizer to use the Shuffle Join algorithm for the specified table.
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name-tl_name): takes effect on MPP. It hints the optimizer to use the Broadcast Join algorithm for the specified table.
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): takes effect on MPP. It hints the optimizer to use the one-phase aggregation algorithm for all aggregate functions in the specified query block.
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): takes effect on MPP. It hints the optimizer to use the two-phase aggregation algorithm for all aggregate functions in the specified query block.

  MPP optimizer Hint can help you intervene in HTAP queries, improving performance and stability for HTAP workload.

  For more information, see [documentation](/optimizer-hints.md).

* Optimizer hints are compatible with specified join methods and join orders. [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)

    In v7.0.0, the optimizer hint [`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-) can be used in conjunction with hints that affect the join method, and their behaviors are compatible. In the case of multi-table joins, you can effectively specify the optimal join method and join order, thereby enhancing the control of optimizer hints over execution plans.

    There will be slight changes in the new Hint behavior. To ensure forward compatibility, TiDB introduces the system variable [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700). When this variable is set to `OFF`, the optimizer hint behavior is compatible with earlier versions. When you upgrade your cluster from earlier versions to v7.0.0 or later versions, this variable will be set to `OFF`. To obtain more flexible hint behavior, if you ensure that the behavior does not bring about performance regression, it is strongly recommended to set this variable to `ON`.

    For more information, see [documentation](/optimizer-hints.md).

### Availability

* Support the `prefer-leader` option, which provides higher availability for read operations and reduces response latency in unstable network conditions [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    You can control TiDB's data reading behavior through the system variable [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40). In v7.0.0, this variable adds the `prefer-leader` option. When the variable is set to `prefer-leader`, TiDB prioritizes selecting the leader replica to perform read operations. When the processing speed of the leader replica slows down significantly, such as due to disk or network performance fluctuations, TiDB selects other available follower replicas to perform read operations, providing higher availability and reducing response latency.

    For more information, see [documentation](/develop/dev-guide-use-follower-read.md).

### SQL

* Time to live (TTL) is generally available [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    TTL provides row-level lifecycle control policies. In TiDB, tables with TTL attributes set automatically checks and deletes expired row data based on the configuration. The goal of TTL is to help users periodically clean up unnecessary data in time while minimizing the impact on cluster workloads.

    For more information, see [documentation](/time-to-live.md).

* 支持 `ALTER TABLE…REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    TiDB 支持 `ALTER TABLE…REORGANIZE PARTITION` 语法。通过该语法，你可以对表的部分或所有分区进行重新组织，包括合并、拆分、或者其他修改，并且不丢失数据。

    For more information, see [documentation](/partitioned-table.md#重组分区).

* 支持 Key Partitioning [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin) **tw:qiancai**

    TiDB 支持 Key 分区。Key 分区与 Hash 分区都可以保证将数据均匀地分散到一定数量的分区里面，区别是 Hash 分区只能根据一个指定的整数表达式或字段进行分区，而 Key 分区可以根据字段列表进行分区，且 Key 分区的分区字段不局限于整数类型。

    For more information, see [documentation](/partitioned-table.md#key-分区).

### DB operations

* TiCDC 支持 storage sink，可输出变更数据至 cloud storage (GA) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu) **tw:hfxsd**

    TiCDC 支持将 changed log 输出到 Amazon S3、Azure Blob Storage、NFS，以及兼容 Amazon S3 协议的存储服务中。Cloud storage 价格便宜，使用方便。对于不使用 Kafka 的用户，可以选择使用 storage sink。使用该功能，TiCDC 会将 changed log 保存到文件，发送到存储系统中。用户自研的消费程序定时从存储系统读取新产生的 changed log 进行数据处理。

    Storage sink 支持格式为 canal-json 和 csv 的 changed log。

    For more information, see [documentation](https://docs.pingcap.com/zh/tidb/stable/ticdc-sink-to-cloud-storage).

* TiCDC Open API V2 GA @[sdojjy](https://github.com/sdojjy) **tw:hfxsd**

    TiCDC 提供 OpenAPI 功能，用户可以通过 OpenAPI v2 对 TiCDC 集群进行查询和运维操作。OpenAPI 的功能是 [`cdc cli` 工具](/ticdc/ticdc-manage-changefeed.md)的一个子集。用户可以通过 OpenAPI 完成 TiCDC 集群的如下运维操作：

    - [获取 TiCDC 节点状态信息](#获取-ticdc-节点状态信息)
    - [检查 TiCDC 集群的健康状态](#检查-ticdc-集群的健康状态)
    - [创建同步任务](#创建同步任务)
    - [删除同步任务](#删除同步任务)
    - [更新同步任务配置](#更新同步任务配置)
    - [查询同步任务列表](#查询同步任务列表)
    - [查询特定同步任务](#查询特定同步任务)
    - [暂停同步任务](#暂停同步任务)
    - [恢复同步任务](#恢复同步任务)
    - [查询同步子任务列表](#查询同步子任务列表)
    - [查询特定同步子任务](#查询特定同步子任务)
    - [查询 TiCDC 服务进程列表](#查询-ticdc-服务进程列表)
    - [驱逐 owner 节点](#驱逐-owner-节点)
    - [动态调整 TiCDC Server 日志级别](#动态调整-ticdc-server-日志级别)

  For more information, see [documentation](https://github.com/pingcap/docs-cn/pull/13224).

### Observability

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    For more information, see [documentation](链接).

### Security

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    For more information, see [documentation](链接).

### Data migration

* Load data 语句集成 Lightning ，用户可以使用 Load data 命令完成原先需要单独使用 Lightning 才能完成的数据导入任务。    [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    在集成 Lightning 之前，Load data 语句只能用于导入位于客户端的数据文件，如果用户要从云存储导入数据，就得借助 Lightning 来实现。但是单独部署 Lightning 又会带来额外的部署成本和管理成本。将 Lightning 逻辑导入能力（TiDB backend ）集成到 Load data 命令后，不仅可以省去 Lightning 的部署和管理成本。还可以借助 Lightning 的功能大大扩展 load data 语句的能力。 部分增强的功能举例说明如下：

    - 支持从 S3 导入数据到 TiDB，且支持通配符一次性匹配多个源文件导入到 TiDB 。
    - 支持 CSV、TSV、Parquet、SQL(mydumper/dumpling) 格式的源文件。
    - 支持 precheck ，可在导入之前将所有不满足导入数据的问题检测出来，用户根据检测结果优化后，再次提交任务。提升任务配置体验。
    - 支持将任务设置为 Detached，让任务在后台执行。
    - 支持任务管理，可通过 show load data jobid 查询任务状态和进展详情。方便用户管理和维护。

  For more information, see [documentation](待补充).

* TiDB Lightning 向 TiKV 传输键值对时支持启用压缩传输 [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky) **tw:qiancai**

    自 v6.6.0 起，TiDB Lightning 支持将本地编码排序后的键值对在网络传输时进行压缩再发送到 TiKV，从而减少网络传输的数据量，降低网络带宽开销。之前版本不支持该功能，在数据量较大的情况下，TiDB Lightning 对网络带宽要求相对较高，且会产生较高的流量费。

    该功能默认关闭，你可以通过将 TiDB Lightning 配置项 compress-kv-pairs 设置为 "gzip" 或者 "gz" 开启此功能。

    For more information, see [documentation](https://docs.pingcap.com/zh/tidb/v6.6/tidb-lightning-configuration#tidb-lightning-%E4%BB%BB%E5%8A%A1%E9%85%8D%E7%BD%AE).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v6.6.0 to the current version (v7.0.0). If you are upgrading from v6.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

* TiDB removes the constraint that the auto-increment column must be an index [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao) **tw:ran-huang**

    TiDB v7.0.0 开始支持移除自增列必须是索引或索引前缀的限制。这意味着用户现在可以更灵活地定义表的主键，并方便地使用自增列实现排序分页，同时避免自增列带来的写入热点问题，并通过使用 Cluster Indexed Table 提高查询性能。之前，TiDB 的行为与 MySQL 一致，要求自增列必须是索引或索引前缀。现在，通过此次更新，您可以使用以下语法创建表并成功移除自增列约束：

    Starting from v7.0.0, TiDB removes the constraint that the auto-increment column must be an index or index prefix. This means that users can now define the primary key of a table more flexibly and use the auto-increment column to implement sorting and pagination more conveniently. This also avoids the write hotspot problem caused by the auto-increment column and improves query performance by using Cluster Indexed Table. Previously, TiDB's behavior was consistent with MySQL, requiring the auto-increment column to be an index or index prefix. With the new release, you can create a table using the following syntax and successfully remove the auto-increment column constraint:

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    This feature does not affect TiCDC data replication.

    For more information, see [documentation](/mysql-compatibility.md#auto-increment-id).

* 兼容性 2

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified | Takes effect starting from v7.0.0 and controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature. |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that TiDB applies Null-Aware Hash Join when Anti Join is generated by subqueries led by special set operators `NOT IN` and `!= ALL` by default. |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | Modified | Takes effect starting from v7.0.0 and controls the maximum number of execution plans that can be cached by [Non-prepared plan cache](/sql-non-prepared-plan-cache.md). |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) | Newly added | This variable controls whether Index Join is supported when the inner table has `Selection` or `Projection` operators on it. |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700) | Newly added | This variable controls whether Prepared Plan Cache caches queries that contain subqueries. |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) | Newly added | This variable is used to set the threshold for triggering load-based replica read. The feature controlled by this variable is not fully functional in TiDB v7.0.0. Do not change the default value. |
|[`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-从-v700-版本开始引入) |  新增  | 这个变量用来控制用于控制连接算法的 Join Method Hint 是否会影响 Join Reorder 的优化过程。 默认值为 `ON`，即采用新的兼容控制模式；`OFF` 则与 v7.0.0 以前的行为保持一致。为了向前兼容，从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。|
|[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入) | 新增 | 是否对悲观锁启用加强的悲观锁唤醒模型，以降低单行冲突场景下事务的尾延迟。默认值为 `ON`，从旧版本升级到 v7.0.0 或之后版本，该变量会被设置成 `OFF` |
|[`tidb_pessimistic_txn_aggressive_locking`] | 删除 | 更名为 [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-从-v700-版本开始引入) |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### Others

## Deprecated feature

## Improvements

+ TiDB

    - 加强的悲观锁唤醒模型的开关变量由 `tidb_pessimistic_txn_aggressive_locking` 更名为 `tidb_pessimistic_txn_fair_locking`，并在新集群中默认启用 [#42147](https://github.com/pingcap/tidb/issues/42147) @[MyonKeminta](https://github.com/MyonKeminta)
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

        - TiCDC 在 v7.0.0 版本支持在 Kafka 为下游的场景中将单个大表的数据改变分布到多个 TiCDC 节点，从而解决用户在大规模 TiDB 集群的数据集成场景下的单表扩展性问题。

            用户可以通过设置 TiCDC 配置 `enable_table_across_nodes` 为 `true` 来启用这个功能，并通过设置`region_threshold` 来指定当一张表的 region 个数超过阀值时 TiCDC 开始将对应的表上的数据改变分布到多个 TiCDC 节点。

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - 优化 Data Migration（DM）检查下游数据库账号权限的前置检查项 [#issue](链接-待补充) @[maxshuang](https://github.com/maxshuang)

            在之前的版本，Data Migration 进行前置检查，检查用户提供的下游数据库账号是具备所需的权限时，是非必须通过项，现改为必须通过项，避免该账号权限不足导致任务失败。

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - Lightning local backend 支持导入数据和索引分离导入，提升导入速度和稳定性 [#42132](https://github.com/pingcap/tidb/issues/42132) @[gozssky](https://github.com/gozssky)

            Lightning 增加 add-index-by-sql 参数。默认取值为 true，表示在物理导入模式（ local backend）下，会在导入数据完成后，通过 add index 的 SQL 语句帮用户建索引，提升导入数据的速度和稳定性。取值为 false，和历史版本保存一致，表示仍然会用 Lightning  将行数据以及索引数据编码成 kv pairs 后再一同导入到 TiKV。

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

- [Contributor GitHub ID]()
