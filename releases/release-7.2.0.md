---
title: TiDB 7.2.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.2.0.
---

# TiDB 7.2.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.2.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.2.0#version-list)

7.2.0 introduces the following key features and improvements:

<!-- key feature placeholder-->

## Feature details

### Performance

* Supporting pushing down the following two [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) to TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427)  @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash supports the pipeline execution model (experimental) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    Prior to v7.2.0, each task in the TiFlash engine must individually request thread resources during execution. TiFlash controls the number of tasks to limit thread resource usage and prevent overuse, but this issue could not be completely eliminated. To address this problem, starting from v7.2.0, TiFlash introduces a pipeline execution model. This model centrally manages all thread resources and schedules task execution uniformly, maximizing the utilization of thread resources while avoiding resource overuse. To enable or disable the pipeline execution model, modify the [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720) system variable.

    For more information, see [documentation](/tiflash/tiflash-pipeline-model.md).

* TiFlash reduces latency of schema replication [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1361-->

    When the schema of a table changes, TiFlash needs to replicate the latest schema from TiKV in a timely manner. Before v7.2.0, when TiFlash accesses table data and detects a table schema change within a database, TiFlash needs to replicate the schemas of all tables in this database again, including those tables without TiFlash replicas. As a result, in a database with a large number of tables, even if you only need to read data from a single table using TiFlash, you might experience significant latency to wait for TiFlash to complete the schema replication of all tables.

    In v7.2.0, TiFlash optimizes the schema replication mechanism and supports only replicating schemas of tables with TiFlash replicas. When a schema change is detected for a table with TiFlash replicas, TiFlash only replicates schema of that table, which reduces the latency of schema replication of TiFlash. This optimization is automatically applied and does not require any manual configuration.

* Improve the performance of statistical information collection [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    TiDB v7.2.0 optimizes the statistics collection strategy, skipping some of the duplicate information and information that is of little value to the optimizer. The overall speed of statistics collection has been improved by 30%. This improvement allows TiDB to update the statistics of the database in a more timely manner, making the generated execution plans more accurate, thus improving the overall database performance.
    
    For more information, see [documentation](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720).

* Improve the performance of checking data and index consistency [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    The [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement is used to check the consistency between data in a table and its corresponding indexes. In v7.2.0, TiDB optimizes the method for checking data consistency and improves the execution efficiency of [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) greatly. In scenarios with large amounts of data, this optimization can provide a performance boost of hundreds of times.

    The optimization is enabled by default ([`tidb_enable_fast_table_check`](/system-variables.md#tidb_enable_fast_table_check-new-in-v720) is `ON` by default) to greatly reduce the time required for data consistency checks in large-scale table and enhance operational efficiency.

    For more information, see [documentation](/system-variables.md#tidb_enable_fast_table_check-new-in-v720).

### Reliability

* Automatically manage queries that consume more resources than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1411-->

    The most common challenge to database stability is the degradation of overall database performance caused by abrupt SQL performance problems. There are many causes for SQL performance issues, such as new SQL statements that have not been fully tested, drastic changes in data volume, and abrupt changes in execution plans. These issues are difficult to completely avoid at the root. TiDB v7.2.0 provides the ability to manage queries that consume more resources than expected. This feature can quickly reduce the scope of impact when a performance issue occurs.
    
    You can set the maximum execution time of a query for a resource group. When the execution time of a query exceeds the setting, the query is automatically deprioritized or cancelled. You can also set a period of time to immediately match identified queries by text, thus avoiding a situation where the concurrency of the problematic queries is so high that it consumes more resources than expected during the identification phase.
    
    Automatic management of queries that consume more resources than expected provides you with an effective means to quickly respond to unexpected query performance problems. This feature can reduce the impact of the problem on overall database performance, thereby improving database stability.
    
    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

* Enhance the capability of creating a binding according to a historical execution plan [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    TiDB v7.2.0 enhances the capability of [creating a binding according to a historical execution plan](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan). This feature improves the parsing and binding process for complex statements, making the bindings more stable, and supports the following new hints:

    - [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop)
    - [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop)
    - [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name)
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name).

    For more information, see [documentation](/sql-plan-management.md).

* The Optimizer Fix Controls mechanism provides fine-grained control over optimizer behaviors [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd**

    To generate more reasonable execution plans, the behavior of the TiDB optimizer evolves over product iterations. However, in some particular scenarios, the changes might lead to performance regression. TiDB v7.2.0 introduces Optimizer Fix Controls to let you control some of the fine-grained behaviors of the optimizer. You can roll back or control some new changes.
    
    Each controllable behavior is described by a GitHub issue corresponding to the fix number. All controllable behaviors are listed in [Optimizer Fix Controls](/optimizer-fix-controls.md). You can set a target value for one or more behaviors by setting the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to achieve behavior control. 
    
    The Optimizer Fix Controls mechanism helps you control the TiDB optimizer at a granular level. It provides a new means of fixing performance issues caused by the upgrade process and improves the stability of TiDB. 
    
    For more information, see [documentation](/optimizer-fix-controls.md).

### SQL

* Support the `CHECK` constraints [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678] (https://github.com/fzzf678) **tw@qiancai** <!--1404-->

    Starting from v7.2.0, you can use `CHECK` constraints to restrict the values of one or more columns in a table to meet your specified conditions. When a `CHECK` constraint is added to a table, TiDB checks whether the constraint is satisfied before inserting or updating data in the table. Only the data that satisfies the constraint can be written.

    For more information, please refer to the [user documentation](/constraints.md#check-constraints).

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

* Introduce a new SQL statement `IMPORT INTO` to improve data import efficiency greatly (Experimental [#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1413-->

    The `IMPORT INTO` statement integrates the [Physical Import Mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) capability of TiDB Lightning. With this statement, you can quickly import data in formats such as `CSV`, `SQL`, and `PARQUET` into an empty table in TiDB. This import method eliminates the need for a separate deployment and management of TiDB Lightning, thereby reducing the complexity of data import and greatly improving import efficiency.

    For data files stored in Amazon S3 or GCS, when the [Backend task distributed execution framework](/tidb-distributed-execution-framework.md) is enabled, `IMPORT INTO` also supports splitting the data import task into multiple sub-tasks and scheduling them to multiple TiDB nodes for parallel import, which further enhances import performance.

    For more information, see the [documentation](sql-statements/sql-statement-import-into.md).

* TiDB Lightning supports importing source files with the Latin-1 character set into TiDB [#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    With this feature, you can directly import source files with the Latin-1 character set into TiDB via TiDB Lightning. Before v7.2.0, importing such files requires your additional preprocessing or conversion. Starting from v7.2.0, you only need to specify `character-set = "latin1"` when configuring the TiDB Lightning import task. Then, TiDB Lightning will automatically handle the character set conversion during the import process to ensure data integrity and accuracy.

    For more information, see the [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.1.0 to the current version (v7.2.0). If you are upgrading from v7.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* 兼容性 1

* 兼容性 2

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-new-in-v610) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that the optimizer removes the `ORDER BY` clause in a subquery. |
|  [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)      | Newly added |  This variable controls which types of columns are skipped for statistics collection when executing the `ANALYZE` command to collect statistics. The variable is only applicable for [`tidb_analyze_version = 2`](#tidb_analyze_version-new-in-v510). When using the syntax of `ANALYZE TABLE t COLUMNS c1, ..., cn`, if the type of a specified column is included in `tidb_analyze_skip_column_types`, the statistics of this column will not be collected.   |
| [`tidb_expensive_txn_time_threshold`](/system-variables.md#tidb_expensive_txn_time_threshold-new-in-v720) | Newly added | Controls the threshold for logging expensive transactions, which is 600 seconds by default. When the duration of a transaction exceeds the threshold, and the transaction is neither committed nor rolled back, it is considered an expensive transaction and will be logged. |
|        |                              |      |
| [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720) | Newly added | This variable is used to control whether to enable the new execution model of TiFlash, the [pipeline model](/tiflash/tiflash-pipeline-model.md). The default value is `OFF`, which means the pipeline model is disabled. |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].optimize-filters-for-memory</code>](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v710) | Newly added | Controls whether to generate Bloom/Ribbon filters that minimize memory internal fragmentation. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].ribbon-filter-above-level</code>](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v710) | Newly added | Controls whether to use Ribbon filters for levels greater than or equal to this value and use non-block-based bloom filters for levels less than this value. |
| TiDB Lightning | `send-kv-pairs` | Deprecated | Starting from v7.2.0, the parameter `send-kv-pairs` is deprecated. You can use [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) to control the maximum size of one request when sending data to TiKV in physical import mode.  **tw@hfxsd** <!--1420--> |
| TiDB Lightning | [`send-kv-size`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Specify the maximum size of one request when sending data to TiKV in physical import mode. When the size of KV key-value pairs reaches the specified threshold, they will be immediately sent to TiKV by TiDB Lightning to avoid the OOM problem caused by TiDB Lightning nodes accumulating too many key-value pairs in memory when importing large wide tables. By adjusting this parameter, you can find a balance between memory usage and import speed, improving the stability and efficiency of the import process. **tw@hfxsd** <!--1420-->|
| Data Migration | [`strict-optimistic-shard-mode`](/dm/feature-shard-merge-optimistic.md) | Newly added | This configuration item is used to be compatible with the DDL shard merge behavior in TiDB Data Migration v2.0. You can enable this configuration item in optimistic mode. After this is enabled, the replication task will be interrupted when it encounters a Type 2 DDL statement. In scenarios where there are dependencies between DDL changes in multiple tables, a timely interruption can be made. You need to manually process the DDL statements of each table before resuming the replication task to ensure data consistency between the upstream and the downstream. **tw@ran-huang** <!--1414-->|
｜ TiCDC ｜ [`sink.protocol`](/ticdc/ticdc-changefeed-config.md) ｜ Modified ｜ Introduces a new value option `"open-protocol"` when the downstream is Kafka. Specifies the protocol format used for encoding messages. ｜
｜ TiCDC ｜ [`sink.delete-only-output-handle-key-columns`](/ticdc/ticdc-changefeed-config.md) ｜ Newly added ｜ Specifies the output of DELETE events. This parameter is valid only for canal-json and open-protocol protocols. The default value is `false`, which means outputting all columns. When you set it to true, only primary key columns or unique index columns are output. ｜

## 废弃功能

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    - 优化构造索引扫描范围的逻辑，支持将一些复杂条件转化为索引扫描范围 [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @xuyifangreeneyes
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