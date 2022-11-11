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
- 支持[基于 AWS EBS snapshot 的集群备份和恢复](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)。
- 支持在分库分表合并迁移场景中[标记下游表中的数据来自上游哪个分库、分表和数据源](/dm/dm-key-features.md#提取分库分表数据源信息写入合表)。

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

* TiFlash supports the SM4 algorithm for encryption at rest [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu) **tw@ran-huang**

    Add the SM4 algorithm for TiFlash encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the `data-encryption-method` configuration to `sm4-ctr` in the `tiflash-learner.toml` configuration file.

    [User document](/encryption-at-rest.md#tiflash)

### Observability

* Cluster diagnostics becomes GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @[Hawkson-jee](https://github.com/Hawkson-jee) **tw@shichun-0415**

    [Cluster diagnostics](/dashboard/dashboard-diagnostics-access.md) diagnoses the problems that might exist in a cluster within a specified time range, and summarizes the diagnostic results and the cluster-related load monitoring information into [a diagnostic report](/dashboard/dashboard-diagnostics-report.md). This diagnostic report is in the form of a web page. You can browse the page offline and circulate this page link after saving the page from a browser.

    With the diagnostic reports, you can quickly understand the basic health information of the cluster, including the load, component status, latency, and configurations. If the cluster has some common problems, you can further locate the causes in the result of the built-in automatic diagnosis in the [diagnostic information](/dashboard/dashboard-diagnostics-report.md#diagnostic-information) section.

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

* Support backing up a TiDB cluster using EBS volume snapshots [#issue](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1) **tw@shichun-0415**

    If your TiDB cluster is deployed on EKS and uses AWS EBS volumes, and you have the following requirements when backing up TiDB cluster data , you can use TiDB Operator to back up the data by volume snapshots and metadata to AWS S3:

    - Minimize the impact of backup, for example, to keep the impact on QPS and transaction latency less than 5%, and to occupy no cluster CPU and memory.
    - Back up and restore data in a short time. For example, finish backup within 1 hour and restore data in 2 hours.

    For more information, see [User document](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot).

### Data migration

* DM supports writing upstream source data to a merged table in extended columns to the downstream [#37797](https://github.com/pingcap/tidb/issues/37797) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**

    When merging sharded schemas and tables from upstream to TiDB, you can manually add several fields (extended columns) in the target table and specify their values when configuring the DM task. Specifically, if you specify the names of the upstream sharded schema and table in the extended columns, the data written to the downstream by DM will include the schema name and table name. In scenarios with data exceptions, you can use this feature to quickly locate the source information of the data in the target table, such as the schema name and table name.

    For more information, see [Extract table, schema, and source information and write into the merged table](/dm/dm-key-features.md#extract-table-schema-and-source-information-and-write-into-the-merged-table).

* DM optimizes the pre-check mechanism by changing mandatory check items to optional ones [#7333](https://github.com/pingcap/tiflow/issues/7333) @[lichunzhu](https://github.com/lichunzhu) **tw@shichun-0415**

    To run a data migration task smoothly, DM triggers [a precheck](/dm/dm-precheck.md) automatically at the start of the task and returns the check results. DM starts the migration only after the precheck is passed.

    In v6.4.0, DM changes the following three check items from mandatory to optional, which improves the pass rate of the pre-check:

    - Check whether the upstream tables use character sets that are incompatible with TiDB.
    - Check whether the upstream tables have primary key constraints or unique key constraints
    - Check whether the database ID `server_id` for the upstream database has been specified in the primary-secondary configuration.

* DM supports configuring binlog position and GTID as optional parameters for incremental migration tasks [#7393](https://github.com/pingcap/tiflow/issues/7393) @[GMHDBJD](https://github.com/GMHDBJD) **tw@shichun-0415**

    Since v6.4.0, you can perform incremental migration directly without specifying the binlog position or GTID. DM automatically obtains the binlog files generated after the task starts from upstream and migrates these incremental data to the downstream. This relieves users from laborious understanding and complicated configuration.

    For more information, see [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

* DM adds more status indicators for migration tasks [#7343](https://github.com/pingcap/tiflow/issues/7343) @[okJiang](https://github.com/okJiang) **tw@shichun-0415**

    DM provides performance and progress indicators for migration tasks. Such information helps users learn about and control the task progress. In addition, the status information also provides a references for troubleshooting.

    In v6.4.0, DM adds several status indicators. They can help users understand the migration performance and progress more intuitively:

    * Add status indicators (in bytes/s) showing data importing and exporting performance.
    * Rename the performance indicator for writing data to the downstream database from TPS to RPS (in rows/s).
    * Add progress indicators showing the data export progress of DM full migration tasks.

    For more information about these indicators, see [Query Task Status in TiDB Data Migration](/dm/dm-query-status.md).

### TiDB data share subscription

- TiCDC supports replicating data to Kafka of the `3.2.0` version [#7191](https://github.com/pingcap/tiflow/issues/7191) @[3AceShowHand](https://github.com/3AceShowHand) **tw@shichun-0415**

    From v6.4.0, TiCDC supports replicating data to Kafka of the `3.2.0` version and earlier.

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

    - `mysql.tables_priv` 表中新增了 `grantor` 字段 [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 允许修改系统变量 `lc_messages` [#38231](https://github.com/pingcap/tidb/issues/38231) @[djshow832](https://github.com/djshow832)
    - 允许 `AUTO_RANDOM` 列作为聚簇复合索引中的第一列 [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)
    - `CREATE USER` 和 `ALTER USER` 支持 `ATTRIBUTE` 和 `COMMENT` [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 内部事务重试使用悲观模式避免重试失败，降低耗时 [#38136](https://github.com/pingcap/tidb/issues/38136) @[jackysp](https://github.com/jackysp)

+ TiKV

    - raftstore 新增 `apply-yield-write-size` 配置项，以限制 raftstore 的最大单轮 Apply 写入的数据大小，减缓 raftstore 线程在 Apply 写入过大时的阻塞现象。[#13594](https://github.com/tikv/tikv/pull/13594) @[glorv](https://github.com/glorv)
    - 为 Region 的 Leader 迁移前增加缓存预热阶段，减缓 Leader 迁移时造成QPS剧烈抖动现象。[#13556](https://github.com/tikv/tikv/pull/13556) @[cosven](https://github.com/cosven)
    - 新增支持将 `json_contains` 算子下推至 Coprocessor 。[#13592](https://github.com/tikv/tikv/issues/13592) @[lizhenhuan](https://github.com/lizhenhuan)
    - 新增对 `CausalTsProvider` 的异步实现 [#13428](https://github.com/tikv/tikv/issues/13428) @[zeminzhou](https://github.com/zeminzhou)

+ PD

    - 新增热点调度 rank v2 算法，在特定场景下 `v2` 版本算法则可以在两个维度都取得更好的均衡效果，并减少无效调度 [#5021](https://github.com/tikv/pd/issues/5021) @[HundunDM](https://github.com/hundundm)
    - 改进 Operator 超时机制，防止过早超时 [#5596](https://github.com/tikv/pd/issues/5596) @[bufferflies](https://github.com/bufferflies)
    - 新增 Placement rule 支持 witness [#5568](https://github.com/tikv/pd/issues/5568) @[ethercflow](https://github.com/ethercflow)
    - 优化调度器在大集群下的性能 [#5473](https://github.com/tikv/pd/issues/5473)@[bufferflies](https://github.com/bufferflies)
    - 支持 external timestamp [#5637](https://github.com/tikv/pd/issues/5637) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 重构了 MPP 的错误处理逻辑 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - 优化了 Block Sort 以及对 Join 和 Aggregation 的 Key 的处理 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 优化了编解码的内存使用和去除冗余传输列以提升 Join 性能 [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)
    - 重构了 MPP 的错误处理逻辑 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    - 优化了 Block Sort 以及对 Join 和 Aggregation 的 Key 的处理 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - 优化了编解码的内存使用和去除冗余传输列以提升 Join 性能 [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)

+ Tools

    + TiDB Dashboard

        - Monitoring 页面展示 TiFlash 相关指标，并且优化指标的展示方式 [#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @[YiniXu9506](https://github.com/YiniXu9506)
        - 在 Slow Query 列表 和 SQL Statement 列表展示结果行数 [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)
        - 优化 Dashboard 的报错信息。  [#1407](https://github.com/pingcap/tidb-dashboard/pull/1407) @[baurine](https://github.com/baurine)

    + Backup & Restore (BR)

        - 改进加载元数据的机制，仅在需要的时候才会将元数据加载到内存中，显著减少了 PITR 过程中的内存压力 [#38404](https://github.com/pingcap/tidb/issues/38404) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - TiCDC 支持同步 Exchange Partition DDL [#639](https://github.com/pingcap/tiflow/issues/639) @[asddongmen](https://github.com/asddongmen)
        - 提升 MQ sink 非 batch 协议的性能 [#7353](https://github.com/pingcap/tiflow/issues/7353) @[hi-rustin](https://github.com/hi-rustin)
        - 提升单表大量 region 场景下 TiCDC puller 的性能 [#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @[sdojjy](https://github.com/sdojjy)
        - 支持 Kafka 3.x 版 [7191](https://github.com/pingcap/tiflow/issues/7191) @[3AceShowHand](https://github.com/3AceShowHand)
        - 支持 syncpoint 功能与下游 TiDB 集群的 `tidb_enable_external_ts_read`  一起使用  [#7419](https://github.com/pingcap/tiflow/issues/7419) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 封装、暴露 Checker 对应的接口，提升各个入口功能组装、调用的灵活性。[#7116](https://github.com/pingcap/tiflow/issues/7116) @[D3Hunter](https://github.com/D3Hunter)
        - 移除 dmctl 中无用的 operate-source update 指令。[#7246](https://github.com/pingcap/tiflow/issues/7246) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 解决了 TiDB 不兼容上游数据库的建表 SQL 导致 DM 全量迁移报错的问题，当上游的建表 SQL TiDB 不兼容时，用户可以提前在 TiDB 手动创建好目标表，让全量迁移任务继续运行 [#37984](https://github.com/pingcap/tidb/issues/37984) @[lance6716](https://github.com/lance6716) **tw@shichun-0415**

    + TiDB Lightning

        - 优化文件扫描逻辑，提升 Schema 类型文件的扫描速度。[#38598](https://github.com/pingcap/tidb/issues/38598) @[dsdashun](https://github.com/dsdashun)

## Bug fixes

+ TiDB

    - 修复新建索引之后有可能导致的数据索引不一致的问题 [#38165](https://github.com/pingcap/tidb/issues/38165) @[tangenta](https://github.com/tangenta)
    - 修复关于 `information_schema.TIKV_REGION_STATUS` 表的权限问题 [#38407](https://github.com/pingcap/tidb/issues/38407) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复 CTE 在 join 时可能得到错误结果的问题 [#38170](https://github.com/pingcap/tidb/issues/38170) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 CTE 在 union 时可能得到错误结果的问题 [#37928](https://github.com/pingcap/tidb/issues/37928) @[YangKeao](https://github.com/YangKeao)
    - 修复监控 transaction region num panel 信息不准确问题 [#38139](https://github.com/pingcap/tidb/issues/38139) @[jackysp](github.com/jackysp)
    - 修复 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 可能影响内部事务问题，修改该变量作用域为 session [#38766](https://github.com/pingcap/tidb/issues/38766)
    - 修复了条件在某些场景下被错误下推 projection 的问题 [#35623](https://github.com/pingcap/tidb/issues/35623)@[Reminiscent](https://github.com/Reminiscent)
    - 修复了 `AND` `OR` 条件的 `isNullRejected` 的错误导致查询结果错误的问题 [#38304]( https://github.com/pingcap/tidb/issues/38304) @[Yisaer](https://github.com/Yisaer)
    - 修复了外连接消除时没有考虑 `GROUP_CONCAT` 内部的 `order by` 导致查询出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    - 修复了错误下推的条件被 join reorder 丢弃后导致查询结果错误的问题 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)

+ TiKV

    - 修复了当环境中存在多个 `cgroup`s 和 `mountinfo`s 时的启动异常问题 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    - 修复 tikv 监控 tikv_gc_compaction_filtered 表达式错误问题 [#13537](https://github.com/tikv/tikv/issues/13537)
    - 修复了 `delete_files_in_range` 中存在的异常而导致的性能问题 [#13534](https://github.com/tikv/tikv/issues/13534) @[tabokie](https://github.com/tabokie)
    - 修复了获取 Snapshot 时 Lease 过期而引发的异常竞争问题 [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复了第一次 FlashBack 失败时存在异常的问题 [#13695](https://github.com/tikv/tikv/issues/13695) @[HuSharp](https://github.com/HuSharp)

+ PD

    - 修复 Stream 超时问题，加速 Leader 切换的速度 [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - 修复由于 PageStorage GC 未能正确清楚 Page 删除标记引起的 WAL 文件过大从而导致 OOM 的问题 [#6163](https://github.com/pingcap/tiflash/issues/6163) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Dashboard

        - 避免查询 Statement 执行计划的时候造成 TiDB OOM [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)
        - 修复 ng-monitoring 丢失 PD 连接后有概率造成 TopSQL 开关无效的问题 [#164](https://github.com/pingcap/ng-monitoring/issues/164) @[zhongzc](https://github.com/zhongzc)

    + Backup & Restore (BR)
        - 修复由于恢复过程中 PD leader 切换，导致恢复失败的问题。[#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复了日志备份任务无法 pause 的问题。[#38250](https://github.com/pingcap/tidb/issues/38250)@[joccau](https://github.com/joccau)
        - 修复 BR 删除日志备份数据时，会删除不应被删除的数据的问题。[#38939](https://github.com/pingcap/tidb/issues/38939) @[Leavrth](https://github.com/leavrth)
        - 修复 BR 第一次执行删除在 `Azure Storage Blob` 或 `Google Cloud Storage` 的日志备份数据时，会执行失败的问题。[#38229](https://github.com/pingcap/tidb/issues/38229) @[Leavrth](https://github.com/leavrth)

    + TiCDC

        - 修复`changefeed query` 的输出中有`sasl-password` 明文的问题 [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        - 修复可能向 ETCD 提交过多操作的问题 [#7131](https://github.com/pingcap/tiflow/issues/7131)  @[asddongmen](https://github.com/asddongmen)
        - 修复 redo log 文件可能被错误删除的问题 [#7131](https://github.com/pingcap/tiflow/issues/7131)  @[asddongmen](https://github.com/asddongmen)
        - 修复 sink v2 MQ 协议在同步宽表时性能回退的问题 [#7344](https://github.com/pingcap/tiflow/issues/7344) @[hi-rustin](https://github.com/hi-rustin)
        - 修复 checkpoint ts 可能被提前推进的问题 [#7274](https://github.com/pingcap/tiflow/issues/7274) @[hi-rustin](https://github.com/hi-rustin)
        - 修改 mounter 模块的日志级以修复 log 打印太多的问题 [#7235](https://github.com/pingcap/tiflow/issues/7235) @[hi-rustin](https://github.com/hi-rustin)
        - 修复可能存在两个 owner 的问题 [#4051](https://github.com/pingcap/tiflow/issues/4051)  @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - 修复 DM UI 产生错误 allow-list 参数问题。[#7096](https://github.com/pingcap/tiflow/issues/7096) @[zoubingwu](https://github.com/zoubingwu)
        - 修复 DM Worker 在启动、停止时有一定概率触发 data race 的问题。[#6401](https://github.com/pingcap/tiflow/issues/6401) @[liumengya94](https://github.com/liumengya94)
        - 修复当同步 Update、Delete 语句且下游行数据不存在时，DM 静默忽略的问题。[#6383](https://github.com/pingcap/tiflow/issues/6383) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 Query Status 时 secondsBehindMaster 字段未显示的问题。[#7189](https://github.com/pingcap/tiflow/issues/7189) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复更新 Checkpoint 时可能触发大事务的问题。[#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        - 修复从 full 模式进行入 sync 模式且很快失败时可能丢失上游表结构信息的问题。[#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        - 修复开启一致性校验（validator）时可能触发死锁的问题。[#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 修复任务预检查对 INFORMATION_SCHEMA 表需要 SELECT 权限的问题。[#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        - 修复空 TLS 配置导致直接报错的问题。[#7384](https://github.com/pingcap/tiflow/issues/7384) @[liumengya94](https://github.com/liumengya94)

    + TiDB Lightning

        - 修复 Parquet String Column 且 Table 设置了 binary 属性时导致导入性能下降的问题。[#38351](https://github.com/pingcap/tidb/issues/38351) @[dsdashun](https://github.com/dsdashun)

    + TiDB Dumpling

        - 修复导出大量表时可能导致超时的问题。[#36549](https://github.com/pingcap/tidb/issues/36549) @[lance6716](https://github.com/lance6716)
        - 修复加锁模式但是上游不存在对应表时导致加锁报错的问题 [#38683](https://github.com/pingcap/tidb/issues/38683) @[lance6716](https://github.com/lance6716)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [645775992](https://github.com/645775992)
- [An-DJ](https://github.com/An-DJ)
- [AndrewDi](https://github.com/AndrewDi)
- [erwadba](https://github.com/erwadba)
- [fuzhe1989](https://github.com/fuzhe1989)
- [goldwind-ting](https://github.com/goldwind-ting) (First-time contributor)
- [h3n4l](https://github.com/h3n4l)
- [igxlin](https://github.com/igxlin) (First-time contributor)
- [ihcsim](https://github.com/ihcsim)
- [JigaoLuo](https://github.com/JigaoLuo)
- [morgo](https://github.com/morgo)
- [Ranxy](https://github.com/Ranxy)
- [shenqidebaozi](https://github.com/shenqidebaozi) (First-time contributor)
- [taofengliu](https://github.com/taofengliu) (First-time contributor)
- [TszKitLo40](https://github.com/TszKitLo40)
- [wxbty](https://github.com/wxbty) (First-time contributor)
- [zgcbj](https://github.com/zgcbj)