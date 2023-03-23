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

* TiFlash supports the disaggregated storage and compute architecture and supports object storage in this architecture (experimental) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy) **tw:qiancai**

    Before v7.0.0, TiFlash only supports the coupled storage and compute architecture. In this architecture, each TiFlash node acts as both storage and compute node, and its computing and storage capabilities cannot be independently expanded. In addition, TiFlash nodes can only use local storage.

    Starting from v7.0.0, TiFlash also supports the disaggregated storage and compute architecture. In this architecture, TiFlash nodes are divided into two types (Compute Nodes and Write Nodes) and support object storage that is compatible with S3 API. Both types of nodes can be independently scaled for computing or storage capacities. The **disaggregated storage and compute architecture** and  **coupled storage and compute architecture** cannot be used in the same cluster or converted to each other. You can configure which architecture to use when you deploy TiFlash.

    For more information, see [documentation](/tiflash/tiflash-disaggregated-and-s3.md).

### Performance

* Achieve compatibility between Fast Online DDL and PITR [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth) **tw:ran-huang**

    In TiDB v6.5.0, [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is not fully compatible with [PITR](/br/backup-and-restore-overview.md). To ensure a full data backup, it is recommended to first stop the PITR background backup task, quickly add indexes using Fast Online DDL, and then resume the PITR backup task.

    Starting from TiDB v7.0.0, Fast Online DDL and PITR are fully compatible. When restoring cluster data through PITR, the index operations added via Fast Online DDL during log backup will be automatically replayed to achieve compatibility.

    For more information, see [documentation](/ddl-introduction.md).

* TiFlash supports null-aware semi join and null-aware anti semi join operators [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi) **tw:Oreoxmt**

    When using `IN`, `NOT IN`, `= ANY`, or `!= ALL` operators in correlated subqueries, TiDB optimizes the computing performance by converting them to semi join or anti semi join. If the join key column might be `NULL`, a null-aware join algorithm is required, such as [Null-aware semi join](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries) and [Null-aware anti semi join](/explain-subqueries#null-aware-anti-semi-join-not-in-and--all-subqueries).

    Before v7.0.0, TiFlash does not support null-aware semi join and null-aware anti semi join operators, preventing these subqueries from being directly pushed down to TiFlash. Starting from v7.0.0, TiFlash supports null-aware semi join and null-aware anti semi join operators. If a SQL statement contains these correlated subqueries, the tables in the query have TiFlash replicas, and [MPP mode](/tiflash/use-tiflash-mpp-mode.md) is enabled, the optimizer automatically determines whether to push down null-aware semi join and null-aware anti semi join operators to TiFlash to improve overall performance.

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* TiFlash supports using FastScan (GA) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan) **tw:Oreoxmt**

    Starting from v6.3.0, TiFlash introduces FastScan as an experimental feature. In v7.0.0, this feature becomes generally available. You can enable FastScan using the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630). By sacrificing strong consistency, this feature significantly improves table scan performance. If the corresponding table only involves `INSERT` operations without any `UPDATE`/`DELETE` operations, FastScan can keep strong consistency and improve the scan performance.

    For more information, see [documentation](/tiflash/use-fastscan.md).

* TiFlash supports late materialization [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

    When processing a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query by default, and then filters and aggregates the data based on the query conditions. Late materialization is an optimization method that supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

    The TiFlash late materialization feature is not enabled by default. You can enable it by setting the `tidb_opt_enable_late_materialization` system variable to `OFF`. When the feature is enabled, the TiDB optimizer will determine which filter conditions to be pushed down based on statistics and filter conditions.

    For more information, see [documentation](/tiflash/tiflash-late-materialization.md).

* Support caching execution plans for non-prepared statements (experimental) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    The execution plan cache is important for improving the load capacity of concurrent OLTP and TiDB already supports [Prepared execution plan cache](/sql-prepared-plan-cache.md). In v7.0.0, TiDB can also cache execution plans for non-Prepare statements, expanding the scope of execution plan cache and improving the concurrent processing capacity of TiDB.

    This feature is disabled by default. You can enable it by setting the system variable [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) to `ON`. For stability reasons, TiDB v7.0.0 allocates a new area for caching non-prepared execution plans and you can set the cache size using the system variable [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size). Additionally, this feature has certain restrictions on SQL statements. For more information, see [Restrictions](/sql-non-prepared-plan-cache.md#restrictions).

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

* TiDB removes the execution plan cache constraint for subqueries [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678) **tw:Oreoxmt**

    TiDB v7.0.0 removes the execution plan cache constraint for subqueries. This means that the execution plan of SQL statements with subqueries can now be cached, such as `SELECT * FROM t WHERE a > (SELECT ...)`. This feature further expands the application scope of execution plan cache and improves the execution efficiency of SQL queries.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* TiKV enables Raft log recycling by default [#14379](https://github.com/tikv/tikv/issues/14379) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    In v6.3.0, TiKV introduced the [Raft log recycling](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) feature to reduce long-tail latency caused by write load. In v7.0.0, this feature is enabled by default.

    For more information, see [documentation](/tikv-configuration-file.md#enable-log-recycle-new-in-v630).

* TiKV supports automatically generating empty log files for log recycling [#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    In v6.3.0, TiKV introduced the [Raft log recycling](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) feature to reduce long-tail latency caused by write load. However, log recycling can only take effect when the number of Raft log files reaches a certain threshold, making it difficult for users to directly experience the throughput improvement brought by this feature.

    In v7.0.0, a new configuration item called `raft-engine.prefill-for-recycle` was introduced to improve user experience. This item controls whether empty log files are generated for recycling when the process starts. When this configuration is enabled, TiKV automatically fills a batch of empty log files during initialization, ensuring that log recycling takes effect immediately after initialization.

    For more information, see [documentation](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700).

* Support deriving the TopN or Limit operator from [window functions](/functions-and-operators/expressions-pushed-down.md) to improve window function performance [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker) **tw:qiancai**

    This feature is disabled by default. To enable it, you can set the session variable [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) to `ON`.

    For more information, see [documentation](derive-topn-from-window.md).

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

* TiFlash supports spilling to disk [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker) **tw:ran-huang**

    To improve execution performance, TiFlash runs data entirely in memory as much as possible. When the amount of data exceeds the total size of memory, TiFlash terminates the query to avoid system crashes caused by running out of memory. Therefore, the amount of data that TiFlash can handle is limited by the available memory.

    Starting from v7.0.0, TiFlash supports spilling to disk. By adjusting the threshold of memory usage for operators ([`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700), [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700), and [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)), you can control the maximum amount of memory that an operator can use. When the memory used by the operator exceeds the threshold, it automatically writes data to disk. This sacrifices some performance but allows for processing of more data.

    For more information, see [documentation](/tiflash/tiflash-spill-disk.md).

* Improve the efficiency of collecting statistics [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:ran-huang**

    In v7.0.0, TiDB further optimizes the logic of collecting statistics, reducing the collection time by about 25%. This optimization improves the operational efficiency and stability of large database clusters, reducing the impact of statistics collection on cluster performance.

* Add new optimizer hints for MPP optimization [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent) **tw:ran-huang**

    In v7.0.0, TiDB adds a series of optimizer hints to influence the generation of MPP execution plans.

    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name-tl_name): takes effect on MPP. It hints the optimizer to use the Shuffle Join algorithm for the specified table.
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name-tl_name): takes effect on MPP. It hints the optimizer to use the Broadcast Join algorithm for the specified table.
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): takes effect on MPP. It hints the optimizer to use the one-phase aggregation algorithm for all aggregate functions in the specified query block.
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): takes effect on MPP. It hints the optimizer to use the two-phase aggregation algorithm for all aggregate functions in the specified query block.

  MPP optimizer hints can help you intervene in HTAP queries, improving performance and stability for HTAP workloads.

  For more information, see [documentation](/optimizer-hints.md).

* Optimizer hints support specifying join methods and join orders [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)  **tw:ran-huang**

    In v7.0.0, the optimizer hint [`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-) can be used in conjunction with hints that affect the join method, and their behaviors are compatible. In the case of multi-table joins, you can effectively specify the optimal join method and join order, thereby enhancing the control of optimizer hints over execution plans.

    The new hint behavior has minor changes. To ensure forward compatibility, TiDB introduces the system variable [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700). When this variable is set to `OFF`, the optimizer hint behavior is compatible with earlier versions. When you upgrade your cluster from earlier versions to v7.0.0 or later versions, this variable will be set to `OFF`. To obtain more flexible hint behavior, after you confirm that the behavior does not cause a performance regression, it is strongly recommended to set this variable to `ON`.

    For more information, see [documentation](/optimizer-hints.md).

### Availability

* Support the `prefer-leader` option, which provides higher availability for read operations and reduces response latency in unstable network conditions [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator) **tw:ran-huang**

    You can control TiDB's data reading behavior through the system variable [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40). In v7.0.0, this variable adds the `prefer-leader` option. When the variable is set to `prefer-leader`, TiDB prioritizes selecting the leader replica to perform read operations. When the processing speed of the leader replica slows down significantly, such as due to disk or network performance fluctuations, TiDB selects other available follower replicas to perform read operations, providing higher availability and reducing response latency.

    For more information, see [documentation](/develop/dev-guide-use-follower-read.md).

### SQL

* Time to live (TTL) is generally available [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    TTL provides row-level lifecycle control policies. In TiDB, tables with TTL attributes set automatically checks and deletes expired row data based on the configuration. The goal of TTL is to help users periodically clean up unnecessary data in time while minimizing the impact on cluster workloads.

    For more information, see [documentation](/time-to-live.md).

* Support `ALTER TABLE…REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    TiDB supports the `ALTER TABLE...REORGANIZE PARTITION` syntax. Using this syntax, you can reorganize some or all of the partitions of a table, including merging, splitting, or other modifications, without losing data.

    For more information, see [documentation](/partitioned-table.md#reorganize-partitions).

* Support Key partitioning [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin) **tw:qiancai**

    Now TiDB supports Key partitioning. Both Key partitioning and Hash partitioning can evenly distribute data into a certain number of partitions. The difference is that Hash partitioning only supports distributing data based on a specified integer expression or an integer column, while Key partitioning supports distributing data based on a column list, and partitioning columns of Key partitioning are not limited to the integer type.

    For more information, see [documentation](/partitioned-table.md#key-partitioning).

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

* TiDB Lightning supports enabling compressed transfers when sending key-value pairs to TiKV (GA) [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky)

    Starting from v6.6.0, TiDB Lightning supports compressing locally encoded and sorted key-value pairs for network transfer when sending them to TiKV, thus reducing the amount of data transferred over the network and lowering the network bandwidth overhead. In the earlier TiDB versions before this feature is supported, TiDB Lightning requires relatively high network bandwidth and incurs high traffic charges in case of large data volumes.

    In v7.7.0, this feature becomes GA and is disabled by default. To enable it, you can set the `compress-kv-pairs` configuration item of TiDB Lightning to `"gzip"` or `"gz"`.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v6.6.0 to the current version (v7.0.0). If you are upgrading from v6.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

* TiDB removes the constraint that the auto-increment column must be an index [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao) **tw:ran-huang**

    Before v7.0.0, TiDB's behavior is consistent with MySQL, requiring the auto-increment column to be an index or index prefix. Starting from v7.0.0, TiDB removes the constraint that the auto-increment column must be an index or index prefix. Now you can define the primary key of a table more flexibly and use the auto-increment column to implement sorting and pagination more conveniently. This also avoids the write hotspot problem caused by the auto-increment column and improves query performance by using the table with clustered indexes. With the new release, you can create a table using the following syntax:

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

* TiDB supports Key partitions, as shown in the following example: **tw:qiancai**

    ```sql
    CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT) PARTITION BY KEY(store_id) PARTITIONS 4;
    ```

    Starting from v7.0.0, TiDB supports Key partitions and can parse the MySQL `PARTITION BY LINEAR KEY` syntax. However, TiDB ignores the `LINEAR` keyword and uses a non-linear hash algorithm instead. Currently, the `KEY` partition type does not support partition statements with an empty partition column list.

    For more information, see [documentation](/partitioned-table.md#key-partitioning).

### TiCDC compatibility

* TiCDC fixes the issue of incorrect encoding of `FLOAT` data in Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand) **tw:ran-huang**

    When upgrading the TiCDC cluster to v7.0.0, if a table replicated using Avro contains the `FLOAT` data type, you need to manually adjust the compatibility policy of Confluent Schema Registry to `None` before upgrading so that the changefeed can successfully update the schema. Otherwise, after upgrading, the changefeed will be unable to update the schema and enter an error state.

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| `tidb_pessimistic_txn_aggressive_locking` | Deleted | Renamed to [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700). |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified | Takes effect starting from v7.0.0 and controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature. |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that TiDB applies Null-Aware Hash Join when Anti Join is generated by subqueries led by special set operators `NOT IN` and `!= ALL` by default. |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) | Modified | The default value of this variable is changed from `OFF` to `ON`, meaning that the cluster isolates resources by resource group by default. |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | Modified | Takes effect starting from v7.0.0 and controls the maximum number of execution plans that can be cached by [Non-prepared plan cache](/sql-non-prepared-plan-cache.md). |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) | Modified | Starting from v7.0.0, this variable is no longer effective for cursor fetch read in the prepared statement protocol. |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) | Newly added | This variable controls whether Index Join is supported when the inner table has `Selection` or `Projection` operators on it. |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700) | Newly added | This variable controls whether Prepared Plan Cache caches queries that contain subqueries. |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) | Newly added | This variable is used to set the threshold for triggering load-based replica read. The feature controlled by this variable is not fully functional in TiDB v7.0.0. Do not change the default value. |
| [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700) | Newly added | This variable controls whether the join method hint influences the optimization of join reorder. The default value is `ON`, which means the new compatible control mode is used. The value `OFF` means the behavior before v7.0.0 is used. For forward compatibility, the value of this variable is set to `OFF` when the cluster is upgraded from an earlier version to v7.0.0 or later. |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700) | Newly added | This variable controls whether to enable the [Derive TopN or Limit from Window Functions](/derive-topn-from-window.md) optimization rule. The default value is `OFF`, which means the optimization rule is not enabled. |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) | Newly added | This variable controls whether to enable the [TiFlash Late Materialization](/tiflash/tiflash-late-materialization.md) feature. The default value is `OFF`, which means the feature is not enabled. |
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | Newly added | This variable controls how the optimizer selects indexes when the SQL statement contains `ORDER BY` and `LIMIT` clauses and have filtering conditions. |
| [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700) | Newly added | Controls whether to enable the enhanced pessimistic lock-waking model to reduce the tail latency of transactions under single-row conflict scenarios. The default value is `ON`. When the cluster is upgraded from an earlier version to v7.0.0 or later, the value of this variable is set to `OFF`. |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700) | Newly added | This variable is used to limit the concurrency of TTL tasks across the entire cluster. The default value `-1` means that the TTL tasks are the same as the number of TiKV nodes. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | `server.snap-max-write-bytes-per-sec` | Deleted | Renamed to [`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec). |
| TiKV | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) | Modified | Default value changed from `false` to `true`. |
| TiKV | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval) | Modified | Default value changed from `1s` to `20s`. This modification can increase the interval of the regular advancement of Resolved TS and reduce the traffic consumption between TiKV nodes. |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | Modified | Default value changed from `false` to `true`. |
| TiKV | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700) | Newly added | Determines whether to generate empty log files for log recycling in Raft Engine. The default value is `false`. |
| PD | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the waiting time for triggering the degraded mode. The default value is `0s`. |
| PD | [`read-base-cost`](/pd-configuration-file.md#read-base-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the coefficient for converting read requests to RU. The default value is `0.25`. |
| PD | [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the coefficient for converting read traffic to RU. The default value is `1/ (64 * 1024)`. |
| PD | [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the coefficient for converting CPU to RU. The default value is `1/3`. |
| PD | [`write-base-cost`](/pd-configuration-file.md#write-base-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the coefficient for converting write requests to RU. The default value is `1`. |
| PD | [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the coefficient for converting write traffic to RU. The default value is `1/1024`. |
| TiFlash | [`flash.disaggregated_mode`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | In the disaggregated architecture of TiFlash, it indicates whether this TiFlash node is a write node or a compute node. The value can be `tiflash_write` or `tiflash_compute`. |
| TiFlash | [`storage.s3.endpoint`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | S3 endpoint address |
| TiFlash | [`storage.s3.bucket`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The bucket where TiFlash stores all data. |
| TiFlash | [`storage.s3.root`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The root directory of data storage in S3 bucket. |
| TiFlash | [`storage.s3.access_key_id`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | `ACCESS_KEY_ID` for accessing S3. |
| TiFlash | [`storage.s3.secret_access_key`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | `SECRET_ACCESS_KEY` for accessing S3. |
| TiFlash | [`storage.remote.cache.dir`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The local data cache directory of TiFlash compute node. |
| TiFlash | [`storage.remote.cache.capacity`](tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The size of the local data cache directory of TiFlash compute node. |
| TiDB Lightning | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls whether to use SQL to add indexes in physical import mode. The default value is automatically selected according to the TiDB version. The advantage of adding indexes using SQL is to separate the import of data and the import of indexes, which can quickly import data. Even if the index creation fails after the data is imported, the data consistency is not affected. |
| TiCDC | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Determines whether to divide a table into multiple sync ranges according to the number of Regions. These ranges can be replicated by multiple TiCDC nodes. |
| TiCDC      | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | When `enable-table-across-nodes` is enabled, this feature only takes effect on tables with more than `region-threshold` Regions.      |

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
