---
title: TiDB 7.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.1.0.
---

# TiDB 7.1.0 Release Notes

In v7.1.0, the key new features and improvements are as follows:

## Feature details

### Scalability

### Performance

* TiFlash supports late materialization (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) **tw:qiancai**

     In v7.0.0, TiFlash supports late materialization as an experiment feature for optimizing query performance. This feature is disabled by default (the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable defaults to `OFF`). when processing a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query, and then filters and aggregates the data based on the query conditions. When Late materialization is enabled, TiDB supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down to the TableScan operator, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

    Starting from v7.1.0, the TiFlash late materialization feature is generally available and enabled by default (the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable defaults to `ON`). The TiDB optimizer decides which filters to be pushed down to the TableScan operator based on the statistics and the filter conditions of the query.

    For more information, see [documentation](/tiflash/tiflash-late-materialization.md).

* TiFlash supports automatically choosing an MPP Join algorithm according to the overhead of network transmission [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg) **tw:qiancai**

    The TiFlash MPP mode supports multiple Join algorithms. Before v7.1.0, TiDB determines whether the MPP mode uses the Broadcast Hash Join algorithm based on the [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) variables and the actual data volume.

    In v7.1.0, TiDB introduces the [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) variable, which controls whether to choose the MPP Join algorithm based on the minimum overhead of network transmission. This variable is disabled by default, indicating that the default algorithm selection method remains the same as that before v7.1.0. You can set the variable to `ON` to enable it. When it is enabled, you no longer need to manually adjust the [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-introduced-from-v50-version) and [`tidb_ broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-introduced-from-v50-version) variables (both variables does not take effect at this time), TiDB automatically estimates the threshold of network transmission by different Join algorithms, and then chooses the algorithm with the smallest overhead overall, thus reducing network traffic and improving MPP query performance.

    For more information, see [documentation](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode).

* Support load-based replica read to mitigate read hotspots [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06) **tw:Oreoxmt**

    In a read hotspot scenario, the hotspot TiKV node cannot process read requests in time, resulting in the read requests queuing. However, not all TiKV resources are exhausted at this time. To reduce latency, TiDB v7.1.0 introduces the load-based replica read feature, which allows TiDB to read data from other TiKV nodes without queuing on the hotspot TiKV node. You can control the queue length of read requests using the [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) system variable. When the estimated queue time of the leader node exceeds this threshold, TiDB prioritizes reading data from follower nodes. This feature can improve read throughput by 70% to 200% in a read hotspot scenario compared to not scattering read hotspots.

    For more information, see [documentation](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots).

* Support caching execution plans for non-prepared statements (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990) **tw:Oreoxmt**

    TiDB v7.0.0 introduces non-prepared plan cache as an experimental feature to improve the load capacity of concurrent OLTP. In v7.1.0, this feature is generally available, enabled by default, and supports caching more SQL statements.

    To improve memory utilization, TiDB v7.1.0 merges the cache pools of non-prepared and prepared plan caches. You can control the cache size using the system variable [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710). The [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) and [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) system variables are deprecated.

    To maintain forward compatibility, when you upgrade from an earlier version to a v7.1.0 or later cluster, the cache size `tidb_session_plan_cache_size` remains the same value as `tidb_prepared_plan_cache_size`, and [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) remains the setting before the upgrade. After sufficient performance testing, you can enable non-prepared plan cache using `tidb_enable_non_prepared_plan_cache`. For a newly created cluster, non-prepared plan cache is enabled by default.

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

### Reliability

* 资源管控 GA [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp) **tw:hfxsd**

    TiDB 持续增强资源管控能力，并将这个特性 GA。该特性将会极大地提升 TiDB 集群的资源利用效率和性能表现。资源管控特性的引入对 TiDB 具有里程碑的意义，你可以将一个分布式数据库集群划分成多个逻辑单元，将不同的数据库用户映射到对应的资源组中，并根据需要设置每个资源组的配额。当集群资源紧张时，来自同一个资源组的会话所使用的全部资源将被限制在配额内，避免其中一个资源组过度消耗，从而影响其他资源组中的会话正常运行。

    该特性也可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他应用的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

    在 v7.1.0 中，TiDB 增加了基于实际负载来估算系统容量上限的能力，为客户的容量规划提供了更准确的参考，协助客户更好地管理 TiDB 的资源分配，从而满足企业级场景的稳定性需要。

    For more information, see [documentation](/tidb-resource-control.md).

* Support the checkpoint mechanism for [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) to improve fault tolerance and automatic recovery capability [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta) **tw:ran-huang**

    TiDB v7.1.0 introduces a checkpoint mechanism for [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630), which significantly improves the fault tolerance and automatic recovery capability of Fast Online DDL. Even in the case of TiDB DDL owner switching, TiDB can still periodically record and synchronize the progress of DDL statements, allowing the new TiDB DDL owner to execute the ongoing DDL statements in Fast Online DDL mode without manually canceling and re-executing the statements. The checkpoint mechanism makes the DDL execution more stable and efficient.

    For more information, see [documentation](/ddl-introduction.md).

* Backup & Restore supports supports checkpoint restore [#issue](https://github.com/pingcap/tidb/issues/issue) @[Leavrth](https://github.com/Leavrth) **tw:Oreoxmt**

    Snapshot restore or log restore might be interrupted due to recoverable errors, such as disk exhaustion and node crash. Before TiDB v7.1.0, the recovery progress before the interruption would be invalidated even after the error is addressed, and you need to start the restore from scratch. For large clusters, this incurs considerable extra cost. Starting from TiDB v7.1.0, Backup & Restore (BR) introduces the checkpoint restore feature, which enables you to continue an interrupted restore. This feature can retain most recovery progress of the interrupted restore.

    For more information, see [documentation](/br/br-checkpoint-restore.md).

* 统计信息缓存加载策略优化 [#issue](https://github.com/pingcap/tidb/issues/issue) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw:hfxsd**

    在开启[统计信息同步加载](/statistics.md#统计信息的加载)的前提下，TiDB 大幅减少了启动时必须载入的统计信息的数量，并且在加载完成前不接受用户连接。一方面提升了启动时统计信息的加载速度，另一方面，避免了在启动初始阶段由于统计信息不全而引起的性能回退。提升了 TiDB 在复杂运行环境下的稳定性，降低了个别 TiDB 节点重启对整体服务的影响。

    For more information, see [documentation]().

### Availability

### SQL

* Support saving TiFlash query results using the `INSERT INTO SELECT` statement (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi) **tw:qiancai**

    Starting from v6.5.0, TiDB supports pushing down the `SELECT` clause (analytical query) of the `INSERT INTO SELECT` statement to TiFlash. In this way, you can easily save the TiFlash query result to a TiDB table specified by `INSERT INTO` for further analysis, which takes effect as result caching (that is, result materialization).

    In v7.1.0, this feature is generally available. During the execution of the `SELECT` clause in the `INSERT INTO SELECT` statement, the optimizer can intelligently decide whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. Therefore, the `tidb_enable_tiflash_read_for_write_stmt` system variable introduced during the experimental phase is now deprecated. Note that the computation rules of `INSERT INTO SELECT` statements for TiFlash do not meet the `STRICT SQL Mode` requirement, so TiDB allows the `SELECT` clause in the `INSERT INTO SELECT` statement to be pushed down to TiFlash only when the [SQL Mode](/sql-mode.md) of the current session is not strict, which means that the `sql_mode` value does not contain `STRICT_TRANS_TABLES` and `STRICT_ALL_TABLES`.

    For more information, see [documentation](/tiflash/tiflash-results-materialization.md).

* MySQL-compatible multi-valued indexes become generally available (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao) **tw:ran-huang**

    Filtering the values of an array in a JSON column is a common operation, but normal indexes cannot help speed up such an operation. Creating a multi-valued index on an array can greatly improve filtering performance. If an array in the JSON column has a multi-valued index, you can use the multi-valued index to filter retrieval conditions in `MEMBER OF()`, `JSON_CONTAINS()`, and `JSON_OVERLAPS()` functions, thereby reducing I/O consumption and improving operation speed.

    In v7.1.0, the multi-valued index feature becomes generally available (GA). It supports more complete data types and is compatible with TiDB tools. You can use multi-valued indexes to speed up the search operations on JSON arrays in production environments.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index).

* Improve the partition management for Hash and Key partitioned tables [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss) **tw:qiancai**

    Before v7.1.0, Hash and Key partitioned tables in TiDB only support the `TRUNCATE PARTITION` partition management statement. Starting from v7.1.0, Hash and Key partitioned tables also support `ADD PARTITION` and `COALESCE PARTITION` partition management statements. Therefore, you can flexibly adjust the number of partitions in Hash and Key partitioned tables as needed. For example, you can increase the number of partitions with the `ADD PARTITION` statement, or decrease the number of partitions with the `COALESCE PARTITION` statement.

    For more information, see [documentation](/partitioned-table.md#manage-hash-and-key-partitions).

* `LOAD DATA` SQL 支持从 S3、GCS 导入数据，支持任务管理等功能 GA [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    以下 `LOAD DATA` 新增的功能在 7.1 版本 GA：

    - 支持从 S3、GCS 导入数据
    - 支持导入 Parquet 文件数据
    - 支持解析源文件中 ascii、latin1、binary、gbk、utf8mbd 字符集
    - 支持设置 FIELDS DEFINED NULL BY 将源文件的指定的值转换为 Null 写入目标表。
    - 支持设置一个 bath_size 即 1 个 batch 插入到目标表的行数，提升写入性能。
    - 支持设置 detached，允许该 job 在后台运行。
    - 支持 show load data jobs, show load data jobid, drop load data jobid 来管理任务。

    For more information, see [documentation](https://github.com/pingcap/docs-cn/pull/13344).

* `LOAD DATA` SQL 集成 Lightning local backend（physical import mode） 的导入功能，提升导入性能（实验特性）[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw:hfxsd**

    用户通过 `LOAD DATA` SQL 导入数据时，可以指定 import_mode = physical 来实现 Lightning local backend （physical 导入模式）的导入效果，相比 Load data 原先的 logical 导入模式，可成倍提升导入数据的性能。

    For more information, see [documentation](链接).

* `LOAD DATA` SQL 支持并行导入，提升导入性能（实验特性）[#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716) **tw:hfxsd**

    原先 load data sql 无法并行导入数据，性能较差。在该版本中支持设置并行导入的参数，通过提升并发，来提升导入的性能。在实验室环境，相比上个版本，测试逻辑导入性能有接近 4 倍的提升。

    For more information, see [documentation](https://github.com/pingcap/docs-cn/pull/13676).

* Generated columns become generally available (GA) @[bb7133](https://github.com/bb7133) **tw:ran-huang**

    Generated columns are a valuable feature for database. When creating a table, you can define that the value of a column is calculated based on the values of other columns in the table, rather than being explicitly inserted or updated by users. This generated column can be either a virtual column or a stored column. TiDB has supported MySQL-compatible generated columns since earlier versions, and this feature becomes GA in v7.1.0.

    Using generated columns can improve MySQL compatibility for TiDB, simplifying the process of migrating from MySQL. It also reduces data maintenance complexity and improves data consistency and query efficiency.

    For more information, see [documentation](/generated-columns.md).

### DB operations

* DDL tasks support pause and resume operations (experimental) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) **tw:ran-huang**

    Before TiDB v7.1.0, when a DDL task encounters a business peak period during execution, you can only manually cancel the DDL task to reduce its impact on the business. In v7.1.0, TiDB introduces pause and resume operations for DDL tasks. These operations let you pause DDL tasks during peak periods and resume them after the peak ends, thus avoiding any impact on your application workloads.

    For example, you can pause and resume multiple DDL tasks using [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) or [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md):

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    For more information, see [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) and [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md).

### Observability

* 增加优化器诊断信息 [#issue号](链接) @[time-and-fate](https://github.com/time-and-fate) **tw:hfxsd**

    获取充足的信息是 SQL 性能诊断的关键，在 v7.1.0 中，TiDB 持续向各种诊断工具中添加优化器运行信息，可以更好地解释执行计划如何被选择，协助用户和技术支持对 SQL 性能问题进行定位。其中包括：

    * [`PLAN REPLAYER`](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息) 的输出中增加 `debug_trace.json` 文件。
    * [`EXPLAIN`](/explain-walkthrough.md) 的输出中，为 `operator info` 添加部分统计信息详情。
    * 为[`慢日志`](/identify-slow-queries.md)的 `Stats` 字段添加部分统计信息详情。

  更多信息，请参考[使用 `PLAN REPLAYER` 保存和恢复集群线程信息](/sql-plan-replayer.md#使用-plan-replayer-保存和恢复集群现场信息)，[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)和[`慢日志查询`](/identify-slow-queries.md)。

### Security

* Replace the interface used for querying TiFlash system table information [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy) **tw:qiancai**

    Starting from v7.1.0, when providing the query service of [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) and [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) system tables for TiDB, TiFlash uses the gRPC port instead of the HTTP port, which avoids the security risks of the HTTP service.

### Data migration

* TiCDC optimizes DDL replication operations [#8686](https://github.com/pingcap/tiflow/issues/8686) @[nongfushanquan](https://github.com/nongfushanquan) **tw:ran-huang**

    Before v7.1.0, when you perform a DDL operation that affected all rows on a large table (such as adding or deleting a column), the replication latency of TiCDC would significantly increase. Starting from v7.1.0, TiCDC optimizes this replication operation and reduces the replication latency to less than 10 seconds. This optimization mitigates the impact of DDL operations on downstream latency.

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.0.0 to the current version (v7.1.0). If you are upgrading from v6.6.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

### Behavior changes

* To improve security, TiFlash deprecates the HTTP service port (default `8123`) and uses the gRPC port as a replacement **tw:qiancai**

    If you have upgraded TiFlash to v7.1.0, then during the TiDB upgrade to v7.1.0, TiDB cannot read the TiFlash system tables ([`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information- schema-tiflash-tables.md) and [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)).

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiFlash | `http_port` | 删除 | 废弃 TiFlash HTTP 服务端口（默认 `8123`）。|
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### Others

## Deprecated feature

## Improvements

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

    - Improves TiFlash performance and stability in the disaggregated storage and compute architecture [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin) **tw:qiancai**
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
