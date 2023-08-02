---
title: TiDB 7.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.3.0.
---

# TiDB 7.3.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.3.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.3.0#version-list)

7.3.0 introduces the following major feature as generally available. The rest of the release (detailed in the Details section) was a series of enhancements to query stability in TiDB server and TiFlash. These are more miscellaneous in nature and not user-facing so they are not included in this section dedicated to release highlights:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/stable/partitioned-raft-kv#partitioned-raft-kv">Partitioned Raft KV GA</a></td>
    <td>Every key region will store its key-value data in its own isolated LSM tree (RocksDB).
This drastically improves write performance, reduces I/O amplication, speeds up scale-in/-out operations, and is a huge step toward TiDB handling beyond PB-scale workloads per cluster.
    </td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

* TiFlash supports the replica selection strategy [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    Before v7.3.0, TiFlash uses replicas from all its nodes for data scanning and MPP calculations to maximize performance. Starting from v7.3.0, TiFlash introduces the replica selection strategy and lets you configure it using the [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730) system variable. This strategy supports selecting specific replicas based on the [zone attributes](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb) of nodes and scheduling specific nodes for data scanning and MPP calculations.

    For a cluster that is deployed in multiple data centers and each data center has complete TiFlash data replicas, you can configure this strategy to only select TiFlash replicas from the current data center. This means data scanning and MPP calculations are performed only on TiFlash nodes in the current data center, which avoids excessive network data transmission across data centers.

    For more information，see [documentation](/system-variables.md/system-variables.md#tiflash_replica_read-new-in-v730).

* TiFlash supports Runtime Filter within nodes [#40220](https://github.com/pingcap/tidb/issues/40220) @[elsa0520](https://github.com/elsa0520) **tw@ran-huang** <!--1130-->

    Runtime Filter is a predicate that generates dynamic values during query planning. During the process of table joining, these dynamic predicates can further filter out rows that do not meet the conditions, reducing scan time and network overhead, and improving the efficiency of table joining. Starting from v7.3.0, TiFlash supports Runtime Filter within nodes, improving the overall performance of analytical queries with performance improvements ranging from 10% to 50% in some TPC-DS workloads.

    This feature is disabled by default in v7.3.0. To enable this feature, set the system variable [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) to `LOCAL`.

    For more information, refer to [user documentation](/runtime-filter.md).

* TiFlash supports executing common table expressions (CTEs) (experimental) [#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros) **tw@ran-huang** <!--1244-->

    Before v7.3.0, the MPP engine of TiFlash cannot execute queries that contain CTEs by default. To achieve the best execution performance within the MPP framework, you need to use the system variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-introduced-since-v630) to inline expand CTE.

    Starting from v7.3.0, TiFlash's MPP engine supports executing queries with CTEs without inline expanding them, allowing for optimal query execution within the MPP framework. In TPC-DS benchmark tests, compared to using inline expansion, this feature has shown a 20% improvement in overall query execution speed for queries containing CTE.

    This feature is an experimental feature and is disabled by default. It is controlled by the system variable [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720).

### Reliability

* Add new optimizer hints [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990) **tw@ran-huang** <!--1457-->

    In v7.3.0, TiDB introduces several new optimizer hints to control the join methods between tables, including:

    - [`INDEX_JOIN()`](link) selects index nested loop join, which uses indexes to filter and use the result set as the inner table to join.
    - [`NO_HASH_JOIN()`](link) selects join methods other than hash join.
    - [`NO_INDEX_HASH_JOIN()`](link) selects join methods other than [index nested loop join](/optimizer-hints.md#inl_hash_join).

    For more information, refer to [user documentation](/optimizer-hints).

* Manually mark queries that use resources more than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) **tw@hfxsd** <!--1446-->

    In v7.2.0, TiDB automatically manages runaway queries, where queries that take longer than expected can be automatically demoted or canceled. In practice, it is not possible to cover all cases by relying on rules alone. Therefore, in v7.3.0, TiDB adds the ability to manually mark queries. With the new command [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md), you can mark queries based on SQL text, SQL Digest, or execution plan. Queries that are marked can be downgraded or canceled.

    The ability of manually marking runaway queries provides an effective means of intervening in unexpected performance problems in the database. For query-induced performance problems, the impact on overall performance can be quickly mitigated before the root cause of the problem is found, improving system service quality. 

    For more information, refer to [user documentation](/tidb-resource-control.md#query-watch-parameters)

### SQL

* List and List COLUMNS partitioned tables support default partitions [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133) **tw@qiancai** <!--1342-->

    When you use the `INSERT` statement to insert data into List or List COLUMNS partitioned tables, the data needs to meet the specified partitioning conditions of the table. If the data to be inserted does not meet any partitioning condition, the execution of the statement will fail, or the data that does not meet any partitioning condition will be ignored.

   Starting from v7.3.0, List and List COLUMNS partitioned tables support default partitions. After a default partition is created, if the data to be inserted does not meet any partitioning condition, it will be written to the default partition. The default partition feature improves the usability of List and List COLUMNS partitioning, avoiding the execution failure of the `INSERT` statement or data being ignored due to data that does not meet partitioning conditions.

    Note that this feature is a TiDB extension to MySQL syntax. For a partitioned table with a default partition, the data in the table cannot be directly replicated to MySQL.

    For more information, see [documentation](/partitioned-table.md#list-partition).

### DB operations

- note 1

- note 2

### Observability

* Show the progress of collecting statistics [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1380-->

    Collecting statistics for large tables often takes a long time. In previous versions, you cannot see the progress of collecting statistics, and therefore cannot predict the completion time. TiDB v7.3.0 introduces a feature to show the progress of collecting statistics. You can view the overall workload, current progress, and estimated completion time for each subtask using the system table `mysql.analyze_jobs` or `SHOW ANALYZE STATUS`. In scenarios such as large-scale data import and SQL performance optimization, this feature helps you understand the overall task progress and improves the user experience.

    For more information, see [documentation](/sql-statements/sql-statement-show-analyze-status.md).

* Plan Replayer supports exporting historical statistics [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1445-->

    Starting from v7.3.0, with the newly added [`dump with stats as of timestamp`](/sql-plan-replayer.md) clause, Plan Replayer can export the statistics of specified SQL-related objects at a specific point in time. During the diagnosis of execution plan issues, accurately capturing historical statistics can help analyze more precisely how the execution plan was generated at the time when the issue occurred. This helps identify the root cause of the problem and greatly improves efficiency in diagnosing execution plan issues.

    For more information, refer to [user documentation](/sql-plan-replayer.md).

### Data migration

* TiDB Lightning introduces a new version of conflict data detection and processing capabilities [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716) **tw@hfxsd** <!--1296-->
     
    Previous versions of TiDB Lightning used different conflict detection and handling methods for logical and physical import modes, which were complicated to configure and not easy for users to understand. In addition, when you use physical import mode, conflicting data cannot be handled by the `replace` and `ignore` policies. In the new version of conflict detection and handling, both logical import mode and physical import mode use the same set of conflict detection and handling, that is, reporting error (`error`), replacing (`replace`) or ignoring (`ignore`) conflicting data when encountering conflicting data. It also allows you to set an upper limit on the number of conflict records, such as how many conflict records should be processed before the task is interrupted and exits. You can also let the program record the data in conflict for easy troubleshooting.

    When it is clear that the import data has a high amount of conflicting data, it is recommended to use the new version of the conflict detection and handling strategy for better performance. Note that the new version and the old version of the conflict policy are mutually exclusive, and cannot be used at the same time. The old conflict detection and handling policy will be deprecated in the future.
    
    For more information, refer to [user documentation](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection).

* TiDB Lightning introduces a new parameter `enable-diagnose-log` to print more diagnostic logs and make it easier to pinpoint problems [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1517-->
    
    By default, this feature is not enabled and only prints logs containing `lightning/main`. When enabled, it prints logs for all packages (including `client-go` and `tidb`) to help diagnose problems related to `client-go` and `tidb`.
    
    For more information, refer to [user documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global).

## Compatibility changes

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* TiDB Lightning **tw@hfxsd**

    - `tikv-importer.on-duplicate` is deprecated and replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).
    - The `max-error` parameter for the maximum number of non-fatal errors that can be tolerated before TiDB Lightning stops the migration task no longer contains an upper limit for import data conflicts. A new parameter [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) controls the maximum number of conflicting records that can be tolerated.

* 兼容性 2

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730) | Newly added | Controls the strategy for selecting TiFlash replicas when a query requires the TiFlash engine. |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|TiDB Lightning  | `conflict.max-record-rows` | Newly added | The new version of strategy to handle conflicting data. It controls the maximum number of rows in the `conflict_records` table. The default value is 100. |
|TiDB Lightning  | `conflict.strategy` | Newly added | The new version of strategy to handle conflicting data.  It includes the following options: "" (TiDB Lightning does not detect and process conflicting data), `error` (terminate the import and report an error if a primary or unique key conflict is detected in the imported data), `replace` (when encountering data with conflicting primary or unique keys, the new data is retained and the old data is overwritten.), `ignore` (when encountering data with conflicting primary or unique keys, the old data is retained and the new data is ignored.). The default value is "", that is, TiDB Lightning does not detect and process conflicting data. |
|TiDB Lightning  | `conflict.threshold` | Newly added | Controls the upper limit of the conflicting data. When `conflict.strategy="error"`, the default value is `0`. When `conflict.strategy="replace”` or `conflict.strategy=“ignore"`, you can set it as a maxint. |
|TiDB Lightning  | `enable-diagnose-logs` | Newly added | Controls whether to enable the diagnostic logs. The default value is `false`, that is, only the logs related to the import are output, and the logs of other dependent components are not output. When you set it to `true`, logs from both the import process and other dependent components are output, and GRPC debugging is enabled, which can be used for diagnosis. |
|TiDB Lightning  | `tikv-importer.on-duplicate` | Deprecated | Controls action to do when trying to insert a conflicting record in the logical import mode. Startign from v7.3.0, this parameter is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
| Data Migration | `strict-optimistic-shard-mode` | 新增 | 用于兼容历史版本 2.0 分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断，在多个表的 DDL变更有依赖关系的场景，可以及时中断，用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) | Newly added | Empty by default, which means that when the message size exceeds the limit of Kafka topic, the changefeed fails. When this configuration is set to `"handle-key-only"`, if the message exceeds the size limit, only the handle key will be sent to reduce the message size; if the reduced message still exceeds the limit, then the changefeed fails. |

## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    - 游标 (Cursor) 结果过大时，写入 TiDB 临时磁盘空间从而避免OOM [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao) <!--1430-->
    - Introduce a new system variable `tidb_opt_enable_non_eval_scalar_subquery` to control whether the `EXPLAIN` statement executes subqueries in advance during the optimization phase [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--983-->
    - When [Global Kill](/tidb-configuration-file#enable-global-kill-new-in-v610) is enabled, you can terminate the current session by pressing <kbd>Control+C</kbd> [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - Support a new DTFile format version to reduce the number of physical files (experimental) [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--？-->
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - When backing up data to Azure Blob Storage using BR, you can specify either an encryption scope or an encryption key for server-side encryption [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1385-->
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - Kafka Sink supports sending only handle key data when the message is too large, reducing the size of the message [#9382](https://github.com/pingcap/tiflow/issues/9382) @[3AceShowHand](https://github.com/3AceShowHand) **tw@ran-huang** <!--1406-->
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - 更新 TiDB Lightning 并行导入的参数名称从 "tikv-importer.incremental-import" 变更为 “tikv-importer.parallel-import” ，避免用户误认为是增量导入而误用该参数。 [#45501](https://github.com/pingcap/tidb/issues/45501) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd**
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

- [Contributor GitHub ID](链接)