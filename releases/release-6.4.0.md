---
title: TiDB 6.4.0 Release Notes
---

# TiDB v6.4.0 Release Notes

Release date: November xx, 2022

TiDB version: 6.4.0-DMR

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/)

In v6.4.0-DMR, the key new features and improvements are as follows:

- 支持通过 FLASHBACK CLUSTER 命令将集群快速回退到过去某一个指定的时间点
- 支持 TiDB 全局内存限制
- TiDB 分区表兼容 Linear Hash 分区。
- 支持高性能、全局单调递增的 AUTO_INCREMENT 列属性。
- 支持对 JSON 类型中的 Array 数据做范围选择。
- 磁盘故障、I/O 无响应等极端情况下的故障恢复加速。
- 增加了动态规划算法来决定表的连接顺序。
- 引入新的优化器提示 `NO_DECORRELATE` 来控制解关联优化。
- 集群诊断功能 GA。
- TiFlash 静态加密支持国密算法 SM4。
- 支持通过 SQL 语句对指定 Partition 的 TiFlash 副本立即触发物理数据整理 (Compaction)。
- 支持对数据库用户增加额外说明。
- 支持基于 AWS EBS snapshot 的集群备份和恢复。

## New features

### SQL

* Support using a SQL statement to compact TiFlash replicas of specified partitions in a table immediately [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen) **tw@qiancai**

    Since v6.2.0, TiDB has supported the feature of [compacting physical data immediately](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) on a full-table replica of TiFlash. You can choose the right time to manually execute SQL statements to immediately compact the physical data in TiFlash, which helps to reduce storage space and improve query performance. In v6.4.0, we refine the granularity of TiFlash replica data to be compacted and support compacting TiFlash replicas of specified partitions in a table immediately.

    BY executing the SQL statement `ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`, you can immediately compact TiFlash replicas of specified partitions in a table.

    [User document](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)

* Support restoring a cluster to a specific point in time by using `FLASHBACK CLUSTER TO TIMESTAMP` [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303)  @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo) **tw@Oreoxmt**

    You can use the `FLASHBACK CLUSTER TO TIMESTAMP` syntax to restore a cluster to a specific point in time quickly with the Garbage Collection lifetime. This feature helps you to easily and quickly undo DML misoperations. For example, `FLASHBACK CLUSTER TO TIMESTAMP` can be used to restore the original cluster in minutes after mistakenly executing a `DELETE` without a `WHERE` clause. This feature does not rely on database backups and supports multiple rollbacks on the timeline to determine when the specific data changes occurred. Note that `FLASHBACK CLUSTER TO TIMESTAMP` cannot replace database backups.

    [User document](/sql-statements/sql-statement-flashback-to-timestamp.md)

* Support restoring a deleted database by using `FLASH DATABASE` [#20463](https://github.com/pingcap/tidb/issues/20463)  @[erwadba](https://github.com/erwadba) **tw@ran-huang**

    By using `FLASHBACK DATABASE`, you can restore a database and its data deleted by `DROP` within the garbage collection (GC) life time. This feature does not depend on any external tools. You can quickly restore data and metadata using SQL statements.

    [User document](/sql-statements/sql-statement-flashback-database.md)

### Security

*  TiFlash supports the SM4 algorithm for encryption at rest [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu) **tw@ran-huang**

    Add the SM4 algorithm for TiFlash encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the `data-encryption-method` configuration to `sm4-ctr` in the `tiflash-learner.toml` configuration file.

    [User document](/encryption-at-rest.md#tiflash)

### Observability

* 集群诊断功能 GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @[Hawkson-jee](https://github.com/Hawkson-jee) **tw@shichun-0415**

    集群诊断功能是在指定的时间范围内，对集群可能存在的问题进行诊断，并将诊断结果和一些集群相关的负载监控信息汇总成一个诊断报告。诊断报告是网页形式，通过浏览器保存后可离线浏览和传阅。

    用户可以通过该报告快速了解集群内的基本诊断信息，包括负载、组件、耗时和配置信息。若用户的集群存在一些常见问题，在[诊断信息](/dashboard/dashboard-diagnostics-report.md#诊断信息)部分可以了解 TiDB 内置自动诊断的结果。

    详细内容见[用户文档](/dashboard/dashboard-diagnostics-access.md)

### Performance

* Introduce the concurrency adaptive mechanism for coprocessor tasks [#37724](https://github.com/pingcap/tidb/issues/37724) @[you06](https://github.com/you06) **tw@ran-huang**

    As the number of coprocessor tasks increases, based on TiKV's processing speed, TiDB automatically increases concurrency (adjust the value of [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)) to reduce the coprocessor task queue and thus reduce latency.

* Add the dynamic planning algorithm to determine table join order [#18969](https://github.com/pingcap/tidb/issues/18969) @[winoros](https://github.com/winoros) **tw@qiancai**

    In earlier versions, TiDB uses the greedy algorithm to determine the join order of tables. In v6.4.0, the TiDB optimizer introduces the [dynamic planning algorithm](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder). The dynamic planning algorithm can enumerate more possible join orders than the greedy algorithm, so it increases the possibility to find a better execution plan and improve the SQL execution efficiency in some scenarios.

    Because the dynamic programming algorithm consumes more time, the selection of the TiDB Join Reorder algorithms is controlled by the [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) variable. If the number of nodes participating in Join Reorder is greater than this threshold, TiDB uses the greedy algorithm. Otherwise, TiDB uses the dynamic programming algorithm.

    [User document](/join-reorder.md)

* The prefix index supports filtering null values. [#21145](https://github.com/pingcap/tidb/issues/21145) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@TomShawn**

    This feature is an optimization for the prefix index. When a column in a table has a prefix index, the `IS NULL` or `IS NOT NULL` condition of the column in the SQL statement can be directly filtered by the prefix, which avoids table lookup in this case and improves the performance of the SQL execution.

    [User document](/system-variables.md#tidb-opt-prefix-index-single-scan-new-in-v640)

* Enhance TiDB chunk reuse mechanism [#38606](https://github.com/pingcap/tidb/issues/38606) @[keeplearning20221](https://github.com/keeplearning20221) **tw@Oreoxmt**

    In previous versions, TiDB only reuses chunk in the `writechunk` function. TiDB v6.4.0 extends the chunk reuse mechanism to execute functions, reducing the frequency of TiDB applications to free memory by reusing Chunk, thus improving the SQL query execution efficiency in some scenarios. You can use the system variable [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640) to control whether to reuse chunk objects, which is enabled by default.

    [User document](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)

* Introduce a new optimizer hint `NO_DECORRELATE` to control whether to perform decorrelation for correlated subqueries [#37789](https://github.com/pingcap/tidb/issues/37789) @[time-and-fate](https://github.com/time-and-fate) **tw@TomShawn**

    By default, TiDB always tries to rewrite correlated subqueries to perform decorrelation, which usually improves execution efficiency. However, in some scenarios, decorrelation reduces the execution efficiency. In v6.4.0, TiDB introduces the optimizer hint `NO_DECORRELATE` to tell the optimizer not to perform decorrelation for specified query blocks to improve query performance in some scenarios.

    [User document](/optimizer-hints.md#no_decorrelate)

* Improve the performance of statistics collection on partitioned tables [#37977](https://github.com/pingcap/tidb/issues/37977) @[Yisaer](https://github.com/Yisaer) **tw@TomShawn**

    In v6.4.0, TiDB optimizes the strategy of collecting statistics on partitioned tables. You can use the system variable [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb-auto-analyze-partitoin-batch-size-new-in-v640) to set the concurrency of collecting statistics on partitioned tables in parallel to speed up the collection and shorten the analysis time.

### Transactions

* 功能简短描述

    功能详细描述（功能是什么，对用户的价值是什么，怎么用） [#issue]() @[贡献者 GitHub ID]()

    [用户文档]()

### Stability

* Accelerate fault recovery in extreme situations such as disk failure and I/O non-response   [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator) **tw@qiancai**

    For enterprise users, database availability is one of the most important metrics. While in complex hardware environments, how to quickly detect and recover from failures has always been one of the challenges of database availability. In v6.4, TiDB fully optimizes the state detection mechanism of TiKV nodes. Even in extreme situations such as disk failures and I/O non-response, TiDB can still report node status quickly and use the active wake-up mechanism to launch Leader election in advance, which accelerates cluster self-healing. Through this optimization, TiDB can shorten the cluster recovery time by about 50% in the case of disk failures.

* Global control on TiDB memory usage [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12) **tw@TomShawn**

    In v6.4.0, TiDB introduces global control of memory usage as an experimental feature that tracks the global memory usage of TiDB instances. You can use the system variable [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) to set the upper limit for the global memory usage. When the memory usage reaches the threshold, TiDB tries to reclaim and release more free memory. When the memory usage exceeds the threshold, TiDB identifies and cancels the SQL operation that has the highest memory usage to avoid system issues caused by excessive memory usage.

    When the memory consumption of TiDB instances has potential risks, TiDB will collect diagnostic information in advance and write it to the specified directory to facilitate the issue diagnosis. At the same time, TiDB provides system table views [`information_schame.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) and [`information_schame.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md) that show the memory usage and operation history to help you better understand the memory usage.

    Global memory control is a milestone in TiDB memory management. It introduces a global view for instances and adopts systematic management for memory, which can greatly enhance database stability and service availability in more key scenarios.

    [User document](/configure-memory-usage.md)

* Control the memory usage of the range-building optimizer [#37176](https://github.com/pingcap/tidb/issues/37176) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@TomShawn**

    In v6.4.0, the system variable [`tidb_opt_range_max_size`](/system-variables.md#tidb-opt-range-max-size-new-in-v640) is introduced to limit the maximum memory usage of the optimizer that builds ranges. When the memory usage exceeds the limit, the optimizer will build more coarse-grained ranges instead of more exact ranges to reduce memory consumption. If a SQL statement has many `IN` conditions, this optimization can significantly reduce the memory usage of compiling and ensure system stability.

    [User document](/system-variables.md#tidb-opt-range-max-size-new-in-v640)

### Ease of use

* TiKV API V2 becomes generally available (GA) [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**

    Before v6.1.0, TiKV only provides basic Key Value read and write capability because it only stores the raw data passed in by the client. In addition, due to different coding methods and no isolation of data ranges, TiDB, Transactional KV, and RawKv cannot be used at the same time in the same TiKV cluster. Therefore, multiple clusters are needed in this case, thus increasing machine and deployment costs.

    TiKV API V2 provides a new Raw Key Value storage format and access interface, including:

    - The data is stored in MVCC and the change timestamp of the data is recorded. Based on this, Change Data Capture is implemented, which is an experimental. For more information, see [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)
    - Data is scoped according to different usage and supports co-existence of a single TiDB cluster, Transactional KV, and RawKV applications.
    - The Key Space field is reserved to support features such as multi-tenancy.

    To enable TiKV API V2, you can set `api-version = 2` in the `[storage]` section of the TiKV configuration file.

    [User documentation](/tikv-configuration-file.md#api-version-new-in-v610)

* Improve the accuracy of TiFlash data replication progress [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen) **tw@qiancai**

    In TiDB, the `PROGRESS` field of the `information_schema.tiflash_replica` table is used to indicate the progress of data replication from the corresponding tables in TiKV to the TiFlash replicas. In earlier TiDB versions, the `PROCESS` field only provides the progress of data replication during the creation of the TiFlash replicas. After a TiFlash replica is created, if new data is imported to a corresponding table in TiKV, this field will not be updated to show the replication progress from TiKV to TiFlash for the new data.

    In v6.4.0, TiDB improves the update mechanism of data replication progress for TiFlash replicas. After a TiFlash replica is created, if new data is imported to a corresponding table in TiKV, the `PROGRESS` value in the [`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md) table will be updated to show the actual replication progress from TiKV to TiFlash for the new data. With this improvement, you can easily view the actual progress of TiFlash data replication.

### MySQL compatibility

* Be compatible with the Linear Hash partitioning syntax [#issue](https://github.com/pingcap/tidb/issues/38450) @[mjonss](https://github.com/mjonss) **tw@qiancai**

    In the earlier version, TiDB has supported the Hash, Range, and List partitioning. Starting from v6.4.0, TiDB can also be compatible with [MySQL Linear Hash partitioning](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html).

    In TiDB, you can execute the existing DDL statements of your MySQL Linear Hash partitions directly, and TiDB will create the corresponding Hash partition tables (note that there is no Linear Hash partition inside TiDB). You can also execute the existing DML statements of your MySQL Linear Hash partitions directly, and TiDB will return the query result of the corresponding TiDB Hash partitions normally. This feature ensures the TiDB syntax compatibility with MySQL Linear Hash partitions and facilitates seamless migration from MySQL-based applications to TiDB.

    [User document](/partitioned-table.md#linear-hash-handling)

* Support a high-performance and globally monotonically increasing `AUTO_INCREMENT` (experimental) [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao) **tw@Oreoxmt**

    TiDB v6.4.0 introduces the `AUTO_INCREMENT` MySQL compatibility mode, which enables monotonically increasing IDs on all TiDB instances by a centralized allocating service. This feature makes it easier to sort query results by auto-increment IDs. To use the MySQL compatibility mode, you can set `AUTO_ID_CACHE` to `1` when creating a table. The following is an example:

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    [User document](/auto-increment.md#mysql-compatibility-mode)

* Support range selection of array data in the JSON type [#13644](https://github.com/tikv/tikv/issues/13644) @[YangKeao](https://github.com/YangKeao) **tw@qiancai**

    Starting from v6.4.0, TiDB supports the [range selection syntax](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths) to be compatible with MySQL.

    - With the keyword `to`, you can specify the start and end positions of array elements and select elements of a continuous range in an array. With `0`, you can specify the position of the first element in an array. For example, using `$[0 to 2]`, you can select the first three elements of an array.

    - With the keyword `last`, you can specify the position of the last element in an array, which allows you to set the position from right to left. For example, using `$[last-2 to last]`, you can select the last three elements of an array.

   This feature simplifies the process of writing SQL statements, further improves the JSON type compatibility, and reduces the difficulty of migrating MySQL applications to TiDB.

* Support adding additional descriptions for database users [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf) **tw@qiancai**

    In TiDB v6.4, you can use the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) to add additional descriptions for database users. TiDB provides two description formats. You can add a text comment using `COMMENT` and add a set of structured attributes in JSON format using `ATTRIBUTE`.

    In addition, TiDB v6.4 adds the [USER_ATTRIBUTES](/information-schema/information-schema-user-attributes.md) table, where you can view the information of user comments and use attributes.

    This feature improves TiDB compatibility with MySQL syntax and makes it easier to integrate TiDB into tools or platforms in the MySQL ecosystem.


### Backup and restore

* 基于 AWS EBS snapshot 的集群备份和恢复 [#issue](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1) **tw@shichun-0415**

    如果你的 TiDB 集群部署在 EKS 上，使用了 AWS EBS 卷，并且对数据备份有以下要求，可考虑使用 TiDB Operator 将 TiDB 集群数据以卷快照以及元数据的方式备份至 AWS S3：

    - 备份的影响降到最小，如备份对 QPS 和事务耗时影响小于 5%，不占用集群 CPU 以及内存。
    - 快速备份和恢复，比如 1 小时内完成备份，2 小时内完成恢复。

    [用户文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)

### Data migration

* 支持在分库分表合并迁移场景，下游合表支持增加扩展列并赋值，用于标记下游表中的记录来自上游哪个分库/分表/数据源。[#37797](https://github.com/pingcap/tidb/issues/37797) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**

    在上游分库分表合并到 TiDB 的场景，用户可以在目标表手动额外增加几个字段（扩展列），并在配置 DM 任务时，对这几个扩展列赋值，如赋予上游分库分表的名称，则通过 DM 写入到下游的记录会带上上游分库分表的名称，在一些数据异常的场景，用户可以通过该功能快速定位目标表的问题数据时来自于上游哪个分库分表。

    [用户文档](/dm/dm-key-features.md#提取分库分表数据源信息写入合表)

* 优化 DM 的前置检查项，将部分必须通过项改为非必须通过项。[#7333](https://github.com/pingcap/tiflow/issues/7333) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**

    将“检查字符集是否存在兼容性差异”、“检查上游表中是否存在主键或唯一键约束”，“数据库主从配置，上游数据库必须设置数据库 ID server_id” 这 3 个前置检查从必须通过项，改为非必须通过项，提升用户前置检查的通过率。

    [用户文档](/dm/dm-precheck.md)

* 配置 DM 增量迁移任务，支持 binlog_name 和 GTID 的参数可作为选配项。[#7393](https://github.com/pingcap/tiflow/issues/7393) @[GMHDBJD](https://github.com/GMHDBJD) **tw@shichun-0415**

    用户只配置 DM 增量迁移任务时，如果不指定 binlog_name 和 GTID 的参数取值，则默认按任务的启动时间去上游获取该时间之后的 binlog file，并将这些增量数据迁移到下游 ，降低了用户的理解成本和配置复杂度。

    [用户文档](/dm/task-configuration-file-full.md)

* DM 任务增加一些状态信息的展示 [#7343](https://github.com/pingcap/tiflow/issues/7343) @[okJiang](https://github.com/okJiang) **tw@shichun-0415**

    * 增加了 DM 任务当前数据导出、数据导入的性能，单位 bytes/s
    * 将当前 DM 写入目标库的性能指标命名 从 TPS 改为 RPS （rows/second）
    * 新增了 DM 全量任务数据导出的进度展示

    [用户文档](/dm/dm-query-status.md)

### TiDB data share subscription

- TiCDC 支持同步数据到 `3.2.0` 版本的 Kafka **tw@shichun-0415**

    TiCDC 下游可支持的 Kafka 的最高版本从 `3.1.0` 变为 `3.2.0`。你可以将通过 TiCDC 将数据同步到不高于 `3.2.0` 版本的 Kafka。

## Compatibility changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-从-v640-版本开始引入) | 新增 | 这个变量是一个只读变量，用来显示上一个语句是否使用了缓存的 Chunk 对象 (Chunk allocation)。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-从-v640-版本开始引入) | 新增 | 该变量用于设置 TiDB [自动 analyze](/statistics.md#自动更新) 分区表（即自动收集分区表上的统计信息）时，每次同时 analyze 分区的个数。 |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) | 新增 | 默认值为 `OFF`。当此变量设置为 `ON` 时，TiDB 会读取 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) 指定时间戳前的历史数据。 |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-从-v640-版本开始引入) | 新增 | 这个变量用来控制 GOGC Tuner 自动调节的最大内存阈值，超过阈值后 GOGC Tuner 会停止工作。 |
| [`tidb_enable_reuse_chunk`](/system-variables.md#last_sql_use_alloc-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 是否启用 Chunk 对象缓存，默认为 `ON`，代表 TiDB 优先使用缓存中的 Chunk 对象，缓存中找不到申请的对象时才会从系统内存中申请。如果为 `OFF`，则直接从系统内存中申请 Chunk 对象。 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 修改 | 这个变量用来控制是否开启 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。v6.4.0 新增了 SESSION 作用域。 |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-从-v640-版本开始引入) | 新增 | 这个变量用来控制是否统计 Prepared Plan Cache 中所缓存的执行计划占用的内存。|
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-从-v640-版本开始引入) | 新增 | 默认值为 `0`。当 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-从-v640-版本开始引入) 设置为 `ON` 时，TiDB 会依据该变量指定的时间戳读取历史数据。 |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-从-v640-版本开始引入) | 新增 | 该变量来用控制是否开启 GOGC Tuner，默认为 ON。 |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-从-v640-版本开始引入) | 新增 | 当 tidb-server 内存占用超过内存报警阈值并触发报警时，TiDB 默认只保留最近 5 次报警时所生成的状态文件。通过该变量可以调整该次数。 |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidboptaggpushdown) | 修改 | 这个变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。本次增加了 Global 的作用域。 |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb-opt-prefix-index-single-scan-从-v640-版本开始引入) | 新增 | 这个变量默认开启，用于控制 TiDB 优化器是否将某些过滤条件下推到前缀索引，尽量避免不必要的回表，从而提高查询性能。 |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb-opt-range-max-size-从-v640-版本开始引入) | 新增 | 该变量用于指定优化器构造扫描范围的内存用量上限。当该变量为 `0` 时，表示对扫描范围没有内存限制。如果构造精确的扫描范围会超出内存用量限制，优化器会使用更宽松的扫描范围。 |
| [`tidb_server_memory_limit`](/system-variables.md#tidb-server-memory-limit-从-v640-版本开始引入) | 新增 | 该变量指定 TiDB 实例的内存限制。TiDB 会在内存用量达到该限制时，对当前内存用量最高的 SQL 语句进行取消 (Cancel) 操作。 |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb-server-memory-limit-gc-trigger-从-v640-版本开始引入) | 新增 | 该变量用于控制 TiDB 尝试触发 GC 的阈值。当 TiDB 的内存使用达到 `tidb_server_memory_limit` 值 \* `tidb_server_memory_limit_gc_trigger` 值时，则会主动触发一次 Golang GC。在一分钟之内只会主动触发一次 GC。|
| [`tidb_server_memory_limit_sess_min_size`](tidb-server-memory-limit-session-min-size-从-v640-版本开始引入) | 新增 | 开启内存限制后，TiDB 会终止当前实例上内存用量最高的 SQL 语句。本变量指定此情况下 SQL 语句被终止的最小内存用量。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-从-v630-版本开始引入) | 修改 | 这个变量从 v6.4.0 开始生效，用来控制 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 的并发数。默认值为 `64`。 |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) | 修改 | 该变量用于设置触发 tidb-server 内存告警的内存使用比率，默认值从 `0.8` 修改为 `0.7`。 |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_enable_prepared_plan_cache-从-v610-版本开始引入) | 修改 | 这个变量用来控制单个 `SESSION` 的 Prepared Plan Cache 最多能够缓存的计划数量。v6.4.0 新增了 SESSION 作用域。|
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-从-v540-版本开始引入) | 修改 | 该变量默认值从 `0` 修改为 `100`，代表 SQL 执行同步加载完整统计信息默认等待 100 毫秒后会超时。 |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-从-v50-版本开始引入) | 修改 | 默认值从 `INT_ONLY` 修改为 `ON`。 |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`tidb_max_reuse_chunk`](/tidb-configuration-file.md#tidb_max_reuse_chunk-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 Chunk 对象数，默认值为 64。配置过大会增加 OOM 的风险。 |
| TiDB | [`tidb_max_reuse_column`](/tidb-configuration-file.md#tidb_max_reuse_column-从-v640-版本开始引入) | 新增 | 用于控制每个连接最多缓存的 column 对象数，默认值为 256。配置过大会增加 OOM 的风险。 |
| TiDB | `tidb_memory_usage_alarm_ratio` | 废弃 | 该配置项在 v6.4.0 之前的版本中用于控制系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 的初始值，自 v6.4.0 起被废弃。|
| TiDB | `memory-usage-alarm-ratio` | 废弃 | 该配置项自 v6.4.0 起被系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 所取代。如果在升级前设置过该配置项，升级后原配置将不再生效。|
| TiKV | [`alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-从-v640-版本开始引入) | 新增 | TiKV 预分配给 TSO 的缓存大小（以时长计算），默认值为 3s。|
| TiKV | [`apply-yield-write-size`](#apply-yield-write-size-从-v640-版本开始引入) | 新增 | Apply 线程每一轮处理单个状态机写入的最大数据量，这是个软限制。 |
| TiKV | [`renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-从-v640-版本开始引入)| 新增 | 单次时间戳请求的最大数量，默认值为 8192。 |
| TiKV | [`raw-min-ts-outlier-threshold`](/tikv-configuration-file.md#raw-min-ts-outlier-threshold-从-v620-版本开始引入) | 废弃 | 废弃对 RawKV 的 Resolved TS 进行异常检测的阈值。|
| PD | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) | 新增 | 这个配置项从 v6.4.0 开始生效，用来控制 TSO 物理时钟更新周期，默认值为 50ms。 |
| TiFlash | [`data-encryption-method`](/tiflash/tiflash-configuration.md#配置文件-tiflash-learnertoml) | 修改 | 扩展可选值范围：增加 sm4-ctr。设置为 sm4-ctr 时，数据将采用国密算法 SM4 加密后进行存储。 |
| DM | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中分表的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |
| DM | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中分库的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |
| DM | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#完整配置文件示例) | 新增 | 可选配置。用于提取分库分表场景中的源信息，提取的信息写入下游合表，用于标识数据来源。如果配置该项，需要提前在下游手动创建合表。 |

### Others

- 从 v6.4.0 开始，TiCDC 使用 Syncpoint 功能需要同步任务拥有下游集群的 `SYSTEM_VARIABLES_ADMIN` 或者 `SUPER` 权限。

## Removed feature

## Improvements

+ TiDB

    - `mysql.tables_priv` 表中新增了 `grantor` 字段. [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 允许修改系统变量 `lc_messages`. [#38231](https://github.com/pingcap/tidb/issues/38231) @[djshow832](https://github.com/djshow832)
    - 允许 `AUTO_RANDOM` 列作为聚簇复合索引中的第一列. [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)
    - `json_path` 支持数组范围选取 [#38583](https://github.com/pingcap/tidb/issues/38583) @[YangKeao](https://github.com/YangKeao)
    - `CREATE USER` 和 `ALTER USER` 支持 `ATTRIBUTE` 和 `COMMENT`. [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 内部事务重试使用悲观模式避免重试失败，降低耗时 [#38136](https://github.com/pingcap/tidb/issues/38136) @[jackysp](https://github.com/jackysp)

+ TiKV

    - raftstore 新增 `apply-yield-write-size` 配置项，以限制 raftstore 的最大单轮 Apply 写入的数据大小，减缓 raftstore 线程在 Apply 写入过大时的阻塞现象。[#13594](https://github.com/tikv/tikv/pull/13594) @[glorv](https://github.com/glorv)
    - 为 Region 的 Leader 迁移前增加缓存预热阶段，减缓 Leader 迁移时造成QPS剧烈抖动现象。[#13556](https://github.com/tikv/tikv/pull/13556) @[cosven](https://github.com/cosven)
    - 新增支持将 `json_contains` 算子下推至 Coprocessor 。[#13592](https://github.com/tikv/tikv/issues/13592) @[lizhenhuan](https://github.com/lizhenhuan)
    - 新增对 `CausalTsProvider` 的异步实现。 [#13428](https://github.com/tikv/tikv/issues/13428) @[zeminzhou](https://github.com/zeminzhou)

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - 重构了 MPP 的错误处理逻辑 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - 优化了 Block Sort 以及对 Join 和 Aggregation 的 Key 的处理 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 优化了编解码的内存使用和去除冗余传输列以提升 Join 性能 [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)
    - 重构了 MPP 的错误处理逻辑 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - 优化了 Block Sort 以及对 Join 和 Aggregation 的 Key 的处理 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 优化了编解码的内存使用和去除冗余传输列以提升 Join 性能 [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)

+ Tools

    + TiDB Dashboard

        - Monitoring 页面展示 TiFlash 相关指标，并且优化指标的展示方式。 [#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @[YiniXu9506](https://github.com/YiniXu9506)
        - 在 Slow Query 列表 和 SQL Statement 列表展示结果行数。 [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)
        - 优化 Dashboard 的报错信息。  [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - 改进加载元数据的机制，仅在需要的时候才会将元数据加载到内存中，显著减少了 PITR 过程中的内存压力。 [#38404](https://github.com/pingcap/tidb/issues/38404) @[YuJuncen](https://github.com/YuJuncen)
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - 解决了 TiDB 不兼容上游数据库的建表 SQL 导致 DM 全量迁移报错的问题。[#37984](https://github.com/pingcap/tidb/issues/37984) @[lance6716](https://github.com/lance6716) **tw@shichun-0415**

        DM 会默认使用上游数据库的建表 SQL 去 TiDB 执行，帮用户创建好目标表。当上游的建表 SQL  TiDB 不兼容时，DM 使用该 SQL 帮用户创建目标表会失败，导致 DM 任务中断。这时候用户可以提前在 TiDB 手动创建好目标表，DM 检查到已存在的目标表时会忽略掉这个建表 SQL 报错，让全量迁移任务继续运行。

        [用户文档](https://github.com/pingcap/docs-cn/pull/11718)

        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## Bug fixes

+ TiDB

    - 修复新建索引之后有可能导致的数据索引不一致的问题. [#38165](https://github.com/pingcap/tidb/issues/38165) @[tangenta](https://github.com/tangenta)
    - 修复关于 `information_schema.TIKV_REGION_STATUS` 表的权限问题. [#38407](https://github.com/pingcap/tidb/issues/38407) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 CTE 在 join 时可能得到错误结果的问题. [#38170](https://github.com/pingcap/tidb/issues/38170) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 CTE 在 union 时可能得到错误结果的问题. [#37928](https://github.com/pingcap/tidb/issues/37928) @[YangKeao](https://github.com/YangKeao)
    - 修复监控 transaction region num panel 信息不准确问题 [#38139](https://github.com/pingcap/tidb/issues/38139) @[jackysp](github.com/jackysp)
    - 修复 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 可能影响内部事务问题，修改该变量作用域为 session [#38766](https://github.com/pingcap/tidb/issues/38766)

+ TiKV

    - 修复了当环境中存在多个 `cgroup`s 和 `mountinfo`s 时的启动异常问题 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - 修复 tikv 监控 tikv_gc_compaction_filtered 表达式错误问题 [#13537](https://github.com/tikv/tikv/issues/13537)

+ PD

    - note [#issue]() @[贡献者 GitHub ID]()
    - note [#issue]() @[贡献者 GitHub ID]()

+ TiFlash

    - 修复由于 PageStorage GC 未能正确清楚 Page 删除标记引起的 WAL 文件过大从而导致 OOM 的问题 [#6163](https://github.com/pingcap/tiflash/issues/6163) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Dashboard

        - 避免查询 Statement 执行计划的时候造成 TiDB OOM。 [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiCDC

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Data Migration (DM)

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiDB Lightning

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

    + TiUP

        - note [#issue]() @[贡献者 GitHub ID]()
        - note [#issue]() @[贡献者 GitHub ID]()

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [goldwind-ting](https://github.com/goldwind-ting)
- [zgcbj](https://github.com/zgcbj)
