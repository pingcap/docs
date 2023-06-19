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

* 新增支持下推两个[窗口函数](/tiflash/tiflash-supported-pushdown-calculations.md) 至 TiFlash [#7427](https://github.com/pingcap/tiflash/issues/7427)  @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@qiancai** <!--1310-->

    * `FIRST_VALUE`
    * `LAST_VALUE`

* TiFlash 支持 pipeline 执行模型（实验特性） [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise) **tw@ran-huang** <!--1440-->

    在 v7.2.0 版本之前，TiFlash 引擎中各个任务在执行时，需要自行申请线程资源。TiFlash 引擎通过控制任务数的方式限制线程资源使用，以避免线程资源超用，但是并不能完全避免。在 v7.2.0 版本中，TiFlash 引入 pipeline 执行模型，对所有线程资源进行统一管理，并对所有任务的执行进行统一调度，充分利用线程资源，同时避免资源超用。新增系统变量 [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model) 用于设定是否启用 pipeline 执行模型。

    更多信息，请参考[用户文档](/tiflash/tiflash-pipeline-model.md)。

* 降低 TiFlash 等待 schema 同步的时延 [#7630](https://github.com/pingcap/tiflash/issues/7630) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1361-->

    当表的 schema 变动时，TiFlash 需要及时和 TiKV 同步表的 schema 信息。在 v7.2.0 版本之前，TiFlash 访问表数据时，如果检测到某张表的 schema 变动时，会同步所有表的 schema 信息。即使一张表没有 TiFlash 副本，TiFlash 也会同步该表的 schema 信息。当数据库中有大量表时，读取一张表的数据需要同步所有表的 schema 信息，schema 同步的时延非常高。在 v7.2.0 版本中，TiFlash 优化 schema 同步机制，只同步包含 TiFlash 副本的表的 schema 信息，并且当检测到某张表的 schema 变动时，只同步该表的 schema 信息，降低 TiFlash 同步 schema 的时延。该优化自动生效，不需要任何设定调整。

* Improve the performance of statistical information collection [#44725](https://github.com/pingcap/tidb/issues/44725) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) **tw@hfxsd** <!--1352-->

    TiDB v7.2.0 optimizes the statistics collection strategy, skipping some of the duplicate information and information that is of little value to the optimizer. The overall speed of statistics collection has been improved by 30%. This improvement allows TiDB to update the statistics of the database in a more timely manner, making the generated execution plans more accurate, thus improving the overall database performance.
    
    For more information, see [documentation](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720).

* 提升表和索引一致性检查的性能 [#43693](https://github.com/pingcap/tidb/issues/43693) @[wjhuang2016](https://github.com/wjhuang2016) **tw@qiancai** <!--1436-->

    TiDB 在新版本中优化了数据一致性校验的方式，大幅提升了 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 的执行效率， 性能提升接近 200 倍。 这个能力可以大幅减少大型表数据一致性检查的时间， 提升运维体验。 设置 [`tidb_enable_fast_table_check`](链接) 为 `TRUE` 启用这个新机制。

    更多信息，请参考[用户文档](链接)

### Reliability

* Automatically manage queries that consume more resources than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) @[glorv](https://github.com/glorv) @[HuSharp](https://github.com/HuSharp) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1411-->

    The most common challenge to database stability is the degradation of overall database performance caused by abrupt SQL performance problems. There are many causes for SQL performance issues, such as new SQL statements that have not been fully tested, drastic changes in data volume, and abrupt changes in execution plans. These issues are difficult to completely avoid at the root. TiDB v7.2.0 provides the ability to manage queries that consume more resources than expected. This feature can quickly reduce the scope of impact when a performance issue occurs.
    
    You can set the maximum execution time of a query for a resource group. When the execution time of a query exceeds the setting, the query is automatically deprioritized or cancelled. You can also set a period of time to immediately match identified queries by text, thus avoiding a situation where the concurrency of the problematic queries is so high that it consumes more resources than expected during the identification phase.
    
    Automatic management of queries that consume more resources than expected provides you with an effective means to quickly respond to unexpected query performance problems. This feature can reduce the impact of the problem on overall database performance, thereby improving database stability.
    
    For more information, see [documentation](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

* Enhance the capability of creating a binding according to a historical execution plan [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1349-->

    TiDB v7.2.0 enhances the capability of creating a binding according to a historical execution plan. This feature improves the parsing and binding process for complex statements and supports new hints including [`AGG_TO_COP()`](/optimizer-hints.md#agg_to_cop), [`LIMIT_TO_COP()`](/optimizer-hints.md#limit_to_cop), [`ORDER_INDEX`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name), and [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name). With this capability, SQL bindings created from historical execution plans provide more stable fixes for execution plans.

    For more information, see [documentation](/sql-plan-management.md).

* The Optimizer Fix Controls mechanism provides fine-grained control over optimizer behaviors [#43169](https://github.com/pingcap/tidb/issues/43169) @[time-and-fate](https://github.com/time-and-fate) **tw@hfxsd**

    To generate more reasonable execution plans, the behavior of the TiDB optimizer evolves over product iterations. However, in some particular scenarios, the changes might lead to performance regression. TiDB v7.2.0 introduces Optimizer Fix Controls to let you control some of the fine-grained behaviors of the optimizer. You can roll back or control some new changes.
    
    Each controllable behavior is described by a GitHub issue corresponding to the fix number. All controllable behaviors are listed in [Optimizer Fix Controls](/optimizer-fix-controls.md). You can set a target value for one or more behaviors by setting the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) system variable to achieve behavior control. 
    
    The Optimizer Fix Controls mechanism helps you control the TiDB optimizer at a granular level. It provides a new means of fixing performance issues caused by the upgrade process and improves the stability of TiDB. 
    
    For more information, see [documentation](/optimizer-fix-controls.md).

### SQL

* 支持 `CHECK` 约束 [#41711](https://github.com/pingcap/tidb/issues/41711) @[fzzf678] (https://github.com/fzzf678) **tw@qiancai** <!--1404-->

    v7.2.0 版本开始，用户可以通过 `CHECK` 约束功能约束表中一个或者多个字段值必须满足特定条件。添加 `CHECK` 约束后，TiDB 会在数据插入或者更新时检查约束条件是否满足，只允许满足约束的数据写入。

    更多信息，请参考[用户文档](链接)。

### DB operations

* DDL 任务支持暂停和恢复操作（实验特性）[#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm) **tw@ran-huang** <!--1185-->

    TiDB v7.2.0 之前的版本中，当 DDL 任务执行期间遇到业务高峰时间点时，为了减少对业务的影响，只能手动取消 DDL 任务。TiDB v7.2.0 引入了 DDL 任务的暂停和恢复功能，你可以在高峰时间点暂停 DDL 任务，等到业务高峰时间结束后再恢复 DDL 任务，从而避免了 DDL 操作对业务负载的影响。

    例如，可以通过如下 `ADMIN PAUSE DDL JOBS` 或 `ADMIN RESUME DDL JOBS` 语句暂停或者恢复多个 DDL 任务：

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;

   更多信息，请参考 [用户文档](/ddl-introduction.md#ddl - 相关的命令介绍)。

### Observability

### 数据迁移

* 引入新的 SQL statement “import into” （实验特性）,该 SQL 集成了 Lightning 物理导入模式（local backend）的能力,大大提升导入数据的效率。[#42930](https://github.com/pingcap/tidb/issues/42930) @[D3Hunter](https://github.com/D3Hunter) **tw@qiancai** <!--1413-->

    "import into " 集成了 Lightning 物理导入模式（local backend）的能力，用户可直接编写 "import into“ SQL 导入数据到 TiDB，同时还支持将数据导入任务拆分成多个子任务调度到多个 TiDB 节点，进行并行导入，提升导入性能。在导入空表的场景，用户无需再部署和管理 Lightning ，降低了导入数据难度的同时，大大提升了导入数据效率。

    更多信息，请参考[用户文档](链接)。

* Lightning 支持将字符集为 latin1 的源文件导入到 TiDB。[#44434](https://github.com/pingcap/tidb/issues/44434) @[lance6716](https://github.com/lance6716) **tw@qiancai** <!--1432-->

    通过此功能，用户现在可以使用 Lightning 数据导入工具直接将字符集为 latin1 的源文件导入到 TiDB 中。这扩展了用户在处理各种字符集时的数据导入选项的兼容性和灵活性。以前，导入这样的文件需要额外的预处理或转换。现在用户只需在运行 Lightning 导入过程时指定源文件的字符集。Lightning 工具会在导入过程中自动处理字符集转换，确保数据的完整性和准确性。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/14172/files)

## Compatibility changes

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

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