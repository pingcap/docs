---
title: TiDB 7.2.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.2.0.
---

# TiDB 7.2.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.2.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.2/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.2.0#version-list)

7.2.0 introduces the following key features and improvements:

<!-- key feature placeholder-->

## Feature details

### Performance

* Support pushing down the following two [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) to TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash supports the pipeline execution model (experimental) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    Prior to v7.2.0, each task in the TiFlash engine must individually request thread resources during execution. TiFlash controls the number of tasks to limit thread resource usage and prevent overuse, but this issue could not be completely eliminated. To address this problem, starting from v7.2.0, TiFlash introduces a pipeline execution model. This model centrally manages all thread resources and schedules task execution uniformly, maximizing the utilization of thread resources while avoiding resource overuse. To enable or disable the pipeline execution model, modify the [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720) system variable.

    For more information, see [documentation](/tiflash/tiflash-pipeline-model.md).

* TiFlash reduces the latency of schema replication [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1361-->

    When the schema of a table changes, TiFlash needs to replicate the latest schema from TiKV in a timely manner. Before v7.2.0, when TiFlash accesses table data and detects a table schema change within a database, TiFlash needs to replicate the schemas of all tables in this database again, including those tables without TiFlash replicas. As a result, in a database with a large number of tables, even if you only need to read data from a single table using TiFlash, you might experience significant latency to wait for TiFlash to complete the schema replication of all tables.

    In v7.2.0, TiFlash optimizes the schema replication mechanism and supports only replicating schemas of tables with TiFlash replicas. When a schema change is detected for a table with TiFlash replicas, TiFlash only replicates schema of that table, which reduces the latency of schema replication of TiFlash. This optimization is automatically applied and does not require any manual configuration.

* Improve the performance of statistics collection [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    TiDB v7.2.0 optimizes the statistics collection strategy, skipping some of the duplicate information and information that is of little value to the optimizer. The overall speed of statistics collection has been improved by 30%. This improvement allows TiDB to update the statistics of the database in a more timely manner, making the generated execution plans more accurate, thus improving the overall database performance.

    By default, statistics collection skips the columns of the `json`, `blob`, `mediumblob`, and `longblob` types. You can modify the default behavior by setting the [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720) system variable. TiDB supports skipping the `JSON`, `BLOB`, and `TEXT` types and their subtypes.

    For more information, see [documentation](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720).

* Improve the performance of checking data and index consistency [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    The [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement is used to check the consistency between data in a table and its corresponding indexes. In v7.2.0, TiDB optimizes the method for checking data consistency and improves the execution efficiency of [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) greatly. In scenarios with large amounts of data, this optimization can provide a performance boost of hundreds of times.

    The optimization is enabled by default ([`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720) is `ON` by default) to greatly reduce the time required for data consistency checks in large-scale tables and enhance operational efficiency.

    For more information, see [documentation](/system-variables.md#tidb_enable_fast_table_check-new-in-v720).

### Reliability

* Automatically manage queries that consume more resources than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1411-->

    The most common challenge to database stability is the degradation of overall database performance caused by abrupt SQL performance problems. There are many causes for SQL performance issues, such as new SQL statements that have not been fully tested, drastic changes in data volume, and abrupt changes in execution plans. These issues are difficult to completely avoid at the root. TiDB v7.2.0 provides the ability to manage queries that consume more resources than expected. This feature can quickly reduce the scope of impact when a performance issue occurs.

    To manage these queries, you can set the maximum execution time of queries for a resource group. When the execution time of a query exceeds this limit, the query is automatically deprioritized or cancelled. You can also set a period of time to immediately match identified queries by text. This helps prevent high concurrency of the problematic queries during the identification phase that could consume more resources than expected.

    Automatic management of queries that consume more resources than expected provides you with an effective means to quickly respond to unexpected query performance problems. This feature can reduce the impact of the problem on overall database performance, thereby improving database stability.

    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

* Enhance the capability of creating a binding according to a historical execution plan [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    TiDB v7.2.0 enhances the capability of [creating a binding according to a historical execution plan](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan). This feature improves the parsing and binding process for complex statements, making the bindings more stable, and supports the following new hints:

    - [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    - [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    - [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name)
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name)

  For more information, see [documentation](/sql-plan-management.md).

* Introduce the Optimizer Fix Controls mechanism to provide fine-grained control over optimizer behaviors [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd**

    To generate more reasonable execution plans, the behavior of the TiDB optimizer evolves over product iterations. However, in some particular scenarios, the changes might lead to performance regression. TiDB v7.2.0 introduces Optimizer Fix Controls to let you control some of the fine-grained behaviors of the optimizer. This enables you to roll back or control some new changes.

    Each controllable behavior is described by a GitHub issue corresponding to the fix number. All controllable behaviors are listed in [Optimizer Fix Controls](/optimizer-fix-controls.md). You can set a target value for one or more behaviors by setting the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to achieve behavior control.

    The Optimizer Fix Controls mechanism helps you control the TiDB optimizer at a granular level. It provides a new means of fixing performance issues caused by the upgrade process and improves the stability of TiDB.

    For more information, see [documentation](/optimizer-fix-controls.md).

### SQL

* Support the `CHECK` constraints [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678](https://github.com/fzzf678) **tw@qiancai** <!--1404-->

    Starting from v7.2.0, you can use `CHECK` constraints to restrict the values of one or more columns in a table to meet your specified conditions. When a `CHECK` constraint is added to a table, TiDB checks whether the constraint is satisfied before inserting or updating data in the table. Only the data that satisfies the constraint can be written.

    For more information, see [documentation](/constraints.md#check-constraints).

### DB operations

* DDL jobs support pause and resume operations (experimental) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    Before TiDB v7.2.0, when a DDL job encounters a business peak during execution, you can only manually cancel the DDL job to reduce its impact on the business. In v7.2.0, TiDB introduces pause and resume operations for DDL jobs. These operations let you pause DDL jobs during a peak and resume them after the peak ends, thus avoiding impact on your application workloads.

    For example, you can pause and resume multiple DDL jobs using `ADMIN PAUSE DDL JOBS` or `ADMIN RESUME DDL JOBS`:

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    For more information, see [documentation](/ddl-introduction.md#ddl-related-commands).

### Observability

### Data Migration

* Introduce a new SQL statement `IMPORT INTO` to improve data import efficiency greatly (experimental) [#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1413-->

    The `IMPORT INTO` statement integrates the [Physical Import Mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) capability of TiDB Lightning. With this statement, you can quickly import data in formats such as CSV, SQL, and PARQUET into an empty table in TiDB. This import method eliminates the need for a separate deployment and management of TiDB Lightning, thereby reducing the complexity of data import and greatly improving import efficiency.

    For data files stored in Amazon S3 or GCS, when the [Backend task distributed execution framework](/tidb-distributed-execution-framework.md) is enabled, `IMPORT INTO` also supports splitting the data import task into multiple sub-tasks and scheduling them to multiple TiDB nodes for parallel import, which further enhances import performance.

    For more information, see [documentation](sql-statements/sql-statement-import-into.md).

* TiDB Lightning supports importing source files with the Latin-1 character set into TiDB [#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    With this feature, you can directly import source files with the Latin-1 character set into TiDB using TiDB Lightning. Before v7.2.0, importing such files requires your additional preprocessing or conversion. Starting from v7.2.0, you only need to specify `character-set = "latin1"` when configuring the TiDB Lightning import task. Then, TiDB Lightning automatically handles the character set conversion during the import process to ensure data integrity and accuracy.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.1.0 to the current version (v7.2.0). If you are upgrading from v7.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`last_insert_id`](/system-variables.md#last_insert_id-new-in-v530) | Modified | Changes the maximum value of this variable from  `9223372036854775807` to `18446744073709551615` to be consistent with MySQL. |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the optimizer removes the `ORDER BY` clause in a subquery. |
|  [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)      | Newly added |  This variable controls which types of columns are skipped for statistics collection when executing the `ANALYZE` command to collect statistics. The variable is only applicable for [`tidb_analyze_version = 2`](#tidb_analyze_version-new-in-v510). When using the syntax of `ANALYZE TABLE t COLUMNS c1, ..., cn`, if the type of a specified column is included in `tidb_analyze_skip_column_types`, the statistics of this column will not be collected.   |
| [`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720) | Newly added | Controls whether to use a checksum-based approach to quickly check the consistency of data and indexes in a table. The default value `ON` means this feature is enabled by default. |
| [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720) | Newly added | This variable is used to control whether to enable the new execution model of TiFlash, the [pipeline model](/tiflash/tiflash-pipeline-model.md). The default value is `OFF`, which means the pipeline model is disabled. |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720) | Newly added | Controls the threshold for logging expensive transactions, which is 600 seconds by default. When the duration of a transaction exceeds the threshold, and the transaction is neither committed nor rolled back, it is considered an expensive transaction and will be logged. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710) | Modified | Changes the default value from `false` to `true`, meaning that TiDB waits for statistics initialization to finish before providing services during TiDB startup. |
| TiDB | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) | Modified | Changes the default value from `false` to `true`, meaning that TiDB uses lightweight statistics initialization during TiDB startup. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].optimize-filters-for-memory</code>](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v710) | Newly added | Controls whether to generate Bloom/Ribbon filters that minimize memory internal fragmentation. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ribbon-filter-above-level</code>](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v710) | Newly added | Controls whether to use Ribbon filters for levels greater than or equal to this value and use non-block-based bloom filters for levels less than this value. |
| TiDB Lightning | `send-kv-pairs` | Deprecated | Starting from v7.2.0, the parameter `send-kv-pairs` is deprecated. You can use [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) to control the maximum size of one request when sending data to TiKV in physical import mode.  **tw@hfxsd** <!--1420--> |
| TiDB Lightning | [`character-set`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Modified | Introduces a new value option `latin1` for the supported character sets of data import. You can use this option to import source files with the Latin-1 character set. |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Specify the maximum size of one request when sending data to TiKV in physical import mode. When the size of key-value pairs reaches the specified threshold, TiDB Lightning will immediately send them to TiKV. This avoids the OOM problems caused by TiDB Lightning nodes accumulating too many key-value pairs in memory when importing large wide tables. By adjusting this parameter, you can find a balance between memory usage and import speed, improving the stability and efficiency of the import process. **tw@hfxsd** <!--1420-->|
| Data Migration | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md) | Newly added | This configuration item is used to be compatible with the DDL shard merge behavior in TiDB Data Migration v2.0. You can enable this configuration item in optimistic mode. After this is enabled, the replication task will be interrupted when it encounters a Type 2 DDL statement. In scenarios where there are dependencies between DDL changes in multiple tables, a timely interruption can be made. You need to manually process the DDL statements of each table before resuming the replication task to ensure data consistency between the upstream and the downstream. **tw@ran-huang** <!--1414-->|
| TiCDC | [`sink.protocol`](/ticdc/ticdc-changefeed-config.md) | Modified | Introduces a new value option `"open-protocol"` when the downstream is Kafka. Specifies the protocol format used for encoding messages. |
| TiCDC | [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md) | Newly added | Specifies the output of DELETE events. This parameter is valid only for canal-json and open-protocol protocols. The default value is `false`, which means outputting all columns. When you set it to true, only primary key columns or unique index columns are output. |

## 废弃功能

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB <!--**tw@ran-huang**-->

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @xuyifangreeneyes
    - 为 stale read 新增相关监控指标 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)
    - 当 stale read retry leader 遇到 lock，resolve lock 之后强制走 leader 避免无谓开销 [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
    - 使用估计时间计算 stale read ts，减少 stale read 开销 [#44215](https://github.com/pingcap/tidb/issues/44215) @[you06](https://github.com/you06)
    - 添加 long running 事务日志和系统变量 [#41471](https://github.com/pingcap/tidb/issues/41471) @[crazycs520](https://github.com/crazycs520)
    - 支持通过 MySQL 压缩协议连接 TiDB (在连接时加上  `--compress` 选项），提升数据密集型查询在低网络质量下的性能，并节省带宽成本的开销 [#22605](https://github.com/pingcap/tidb/issues/22605) @[dveeden](https://github.com/dveeden)
    - 支持将utf8和utf8mb3都识别为旧的三字节字符集编码。[#26226](https://github.com/pingcap/tidb/issues/26226) @[dveeden](https://github.com/dveeden)
    - 支持将 := 用于 update 语句中赋值。[#44751](https://github.com/pingcap/tidb/issues/44751) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ TiKV <!--**tw@Oreoxmt**-->

    - 支持配置PDclient的重连间隔 [#14964](https://github.com/tikv/tikv/issues/14964) @[rleungx](https://github.com/rleungx)
    - resource control提高调度算法将全局的资源使用作为调度因素 [#14604](https://github.com/tikv/tikv/issues/14604) @[Connor1996](https://github.com/Connor1996)
    - compaction-guard-min-output-file-size默认值从8MB改为1MB [#14888](https://github.com/tikv/tikv/issues/14888) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 使用 gzip 压缩 check leader 请求减少流量消耗   [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - 添加 check leader 相关 metric [#14658](https://github.com/tikv/tikv/issues/14658) @[you06](https://github.com/you06)
    - 详细记录 write command 处理时间细节 [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD <!--**tw@Oreoxmt**-->

    - PD Leader 选举使用单独的 gRPC 链接，防止受到其他请求的影响 [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)
    - 默认打开 bucket split，改善 Multi-Region 的热点问题 [#6433](https://github.com/tikv/pd/issues/6433) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR) <!--**tw@hfxsd**-->

        - Support access to Azure Blob Storage by shared access signature (SAS) [#44199](https://github.com/pingcap/tidb/issues/44199) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--**tw@hfxsd**-->
        
        - Optimize the structure of the directory where data files are stored when a DDL occurs in the scenario of replication to an object storage service [#8891](https://github.com/pingcap/tiflow/issues/8891) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support the OAUTHBEARER authentication in the scenario of replication to Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/hi-rustin)
        - Add the option of outputting only the handle keys for the `DELETE` operation in the scenario of replication to Kafka [#9143](https://github.com/pingcap/tiflow/issues/9143) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Support using MySQL 8.0 to compress binlogs [#6381](https://github.com/pingcap/tiflow/issues/6381) @[dveeden](https://github.com/dveeden)

    + TiDB Lightning

        - 优化导入时遇到 leader 切换导致的错误的重试机制 [#44478](https://github.com/pingcap/tidb/pull/44478)
        - 导入完成后通过 SQL 的方式校验 checksum，提升检验的稳定性 [#41941](https://github.com/pingcap/tidb/issues/41941)
        - 优化宽表导入下 lightning OOM 的问题 [43853](https://github.com/pingcap/tidb/issues/43853)

## Bug fixes

+ TiDB

    <!--**tw@ran-huang**-->

    - 修复关联子查询中含有 CTE 时可能出现的查询 hang 住的问题 [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复某些情况下 max/min 结果出错的问题 [#43805](https://github.com/pingcap/tidb/issues/43508)@[wshwsh12](https://github.com/wshwsh12)
    - 修复当 query 包含子查询时，information schema 显示中 `TxnStart` 字段为空的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - 修复 cop task 中 txn scope 缺失导致 stale read global optimization 不生效的问题 [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)
    - 修复 follower read 未处理 flashback 错误进行重试导致查询报错的问题 [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    <!--**tw@qiancai**-->
    - 修复 prepared stale read 语句无法读到预期结果机会的问题 [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - 修复 on update 语句没有正确更新 primary key 导致数据索引不一致问题 @[zyguan](https://github.com/zyguan)
    - 修改 UNIX_TIMESTAMP 函数的上限为 `3001-01-19 03:14:07.999999 UTC` 和 MySQL 8.0.28+ 保持一致 [#43987](https://github.com/pingcap/tidb/issues/43987) @[YangKeao](https://github.com/YangKeao)
    - 修复了 add Index 在 ingest 模式下失败的问题 [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
    - 修复了 cancel 处于在 rollback 状态的 DDL 任务导致相关元数据出错的问题 [#44143](https://github.com/pingcap/tidb/issues/44143)  @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了 memtracker 配合 cursor 使用导致内存泄漏的问题 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    - 修复了删除 database 导致 GC 推进慢的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了分区表在 Index join 的 probe 阶段找不到对应行而报错的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[AilinKid](https://github.com/AilinKid) @[mjonss](https://github.com/mjonss)
    - 修复了创建 subpartition 的报错信息 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - 修复了执行时间超过 `MAX_EXECUTION_TIME` 被 kill 的返回值和 MySQL 不一致的问题 [#43031](https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
    - 修复了 Leading Hint 无法支持 query block alias 的问题 [#44645](https://github.com/pingcap/tidb/issues/44645)  @[qw4990](https://github.com/qw4990)
    - last_insert_id函数的返回类型从varchar变更为longlong，与MySQL相同，同时last_insert_id的最大上限也变更为MaxUint64。[#44574](https://github.com/pingcap/tidb/issues/44574)  @[Defined2014](https://github.com/Defined2014)
    - 修复了 CTE 多次被非关联子查询引用的情况下，因过滤条件下推导致的结果错误 [#44051] (https://github.com/pingcap/tidb/issues/44051)  @[winoros](https://github.com/winoros)
    - 修复了 outer join reorder 对 condition 的错误处理导致的结果正确性问题 [#44314] (https://github.com/pingcap/tidb/issues/44314)  @[AilinKid](https://github.com/AilinKid)
    - 修复了 `prepare stmt from "analyze table xxx"` 会被 `tidb_mem_quota_query` kill 掉的问题 [#44320] (https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan)

+ TiKV <!--**tw@Oreoxmt**-->

    - 修复处理stale悲观锁冲突时不正确的事务返回值 [#13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复in-memory pessimistic locks可能导致flashback失败和数据不一致 [#13303](https://github.com/tikv/tikv/issues/13303) @[JmPotato](https://github.com/JmPotato)
    - 修复 fair lock 在出现 stale req 情况下的正确性问题 #[13298](https://github.com/tikv/tikv/issues/13298) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复 autocommit point get 在 follower read 情况下线性一致性可能被破坏的问题 #[14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxkj](https://github.com/cfzjywxk)

+ PD <!--**tw@Oreoxmt**-->

    - 修复在特殊情况下冗余副本无法自动修复的问题 [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)

+ TiFlash <!--**tw@qiancai**-->

    - 修复在 join 的 build 端数据量很大且含有大量短字符串时内存消耗过大的问题 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR) <!--**tw@hfxsd**-->

        - Fix the issue that `checksum mismatch` is falsely reported in some cases [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that `resolved lock timeout` is falsely reported in some cases [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiDB might panic when restoring statistics information [#44490](https://github.com/pingcap/tidb/issues/44490) @[tangenta](https://github.com/tangenta)

    + TiCDC <!--**tw@hfxsd**-->

        - Fix the issue that Resolved TS does not advance properly in some cases [#8963](https://github.com/pingcap/tiflow/issues/8963) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the `UPDATE` operation cannot output old values when the Avro or CSV protocol is used [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue of excessive downstream pressure caused by reading downstream metadata too frequently when replicating data to Kafka [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue of too many downstream logs caused by frequently setting the downstream BDR-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the PD node crashing causes the TiCDC node to restart [#8868](https://github.com/pingcap/tiflow/issues/8868) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC cannot create a changefeed with a downstream KOP [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - Fix the TiDB Lightning panic issue when `experimental.allow-expression-index` is enabled and the default value is UUID [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the TiDB Lightning panic issue when a task exits while dividing a data file [#43195](https://github.com/pingcap/tidb/issues/43195) @[lance6716](https://github.com/lance6716)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [asjdf](https://github.com/asjdf)
- [blacktear23](https://github.com/blacktear23)
- [Cavan-xu](https://github.com/Cavan-xu)
- [darraes](https://github.com/darraes)
- [demoManito](https://github.com/demoManito)
- [dhysum](https://github.com/dhysum)
- [HappyUncle](https://github.com/HappyUncle)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [nyurik](https://github.com/nyurik)
- [SeigeC](https://github.com/SeigeC)
- [tangjingyu97](https://github.com/tangjingyu97)