---
title: TiDB 7.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.3.0.
---

# TiDB 7.3.0 Release Notes

Release date: xx xx, 2023

TiDB version: 7.3.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.3.0#version-list)

7.3.0 introduces the following major features. The rest of the release (detailed in the Details section) was a series of enhancements to query stability in TiDB server and TiFlash. These are more miscellaneous in nature and not user-facing so they are not included in this section dedicated to release highlights:

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
    <td>TiDB Lightning supports Partitioned Raft KV </td>
    <td>TiDB Lightning now supports the new Partitioned Raft KV architecture, as part of the near-term GA of the architecture.
    </td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection">Add automatic conflict detection and resolution on imports</a></td>
    <td>The TiDB Lightning Physical Import Mode supports the new version of conflict detection and implementing the semantics of replacing (`replace`) or ignoring (`ignore`) conflicting data when encountering conflicts. It automatically handles conflicting data for you while improving the performance of conflict resolution.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-resource-control.md#query-watch-parameters">Manual management of runaway queries </a>(experimental)</td>
    <td>Query timeouts exist on a per-TiKV node basis but now Resource Groups can manage queries by global parallel execution time and either deprioritize or kill them. Allowing operators to mark target queries by SQL manually Text, SQL Digest or Plan Digest and what do with the queries at a Resource Group level, gives them much more control over the impact unexpected large queries may have on the cluster.</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/optimizer-hints">Enhanced operator control over query stability by adding more complex optimizer hints to the query planner</a></td>
    <td>Added hints: <code>NO_INDEX_JOIN()</code>, <code>NO_MERGE_JOIN()</code>, <code>NO_INDEX_MERGE_JOIN()</code>, <code>NO_HASH_JOIN()</code>,  <code>NO_INDEX_HASH_JOIN()</code>
    </td>
  </tr>
  <tr>
    <td>DB Operations and Observability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">Show the progress of statistics collection tasks</a></td>
    <td>Support viewing the progress of <code>ANALYZE</code> tasks using <code>SHOW ANALYZE STATUS</code> or through the system table <code>mysql.analyze_jobs</code>.</td>
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

    Runtime Filter is a **dynamic predicate** generated during the query planning phase. In the process of table joining, these dynamic predicates can effectively filter out rows that do not meet the join conditions, reducing scan time and network overhead, and improving the efficiency of table joining. Starting from v7.3.0, TiFlash supports Runtime Filter within nodes, improving the overall performance of analytical queries. In some TPC-DS workloads, the performance can be improved by 10% to 50%.

    This feature is disabled by default in v7.3.0. To enable this feature, set the system variable [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) to `LOCAL`.

    For more information, refer to [user documentation](/runtime-filter.md).

* TiFlash supports executing common table expressions (CTEs) (experimental) [#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros) **tw@ran-huang** <!--1244-->

    Before v7.3.0, the MPP engine of TiFlash cannot execute queries that contain CTEs by default. To achieve the best execution performance within the MPP framework, you need to use the system variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-introduced-since-v630) to enforce inlining CTE.

    Starting from v7.3.0, TiFlash's MPP engine supports executing queries with CTEs without inlining them, allowing for optimal query execution within the MPP framework. In TPC-DS benchmark tests, compared with inlining CTEs, this feature has shown a 20% improvement in overall query execution speed for queries containing CTE.

    This feature is experimental and is disabled by default. It is controlled by the system variable [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720).

### Reliability

* Add new optimizer hints [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990) **tw@ran-huang** <!--1457-->

    In v7.3.0, TiDB introduces several new optimizer hints to control the join methods between tables, including:

    - [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) selects join methods other than merge join.
    - [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-) selects join methods other than index nested loop join.
    - [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-) selects join methods other than index nested loop merge join.
    - [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) selects join methods other than hash join.
    - [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) selects join methods other than [index nested loop hash join](/optimizer-hints.md#inl_hash_join).

    For more information, refer to [user documentation](/optimizer-hints).

* Manually mark queries that use resources more than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) **tw@hfxsd** <!--1446-->

    In v7.2.0, TiDB automatically manages queries that use resources more than expected (Runaway Query) by automatically downgrading or canceling runaway queries. In actual practice, rules alone cannot cover all cases. Therefore, TiDB v7.3.0 introduces the ability to manually mark runaway queries. With the new command [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md), you can mark runaway queries based on SQL text, SQL Digest, or execution plan, and the marked runaway queries can be downgraded or cancelled.

    This feature provides an effective intervention method for sudden performance issues in the database. For performance issues caused by queries, before identifying the root cause, this feature can quickly alleviate its impact on overall performance, thereby improving system service quality.

    For more information, see [documentation](/tidb-resource-control.md#query-watch-parameters).

### SQL

* List and List COLUMNS partitioned tables support default partitions [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133) **tw@qiancai** <!--1342-->

    Before v7.3.0, when you use the `INSERT` statement to insert data into List or List COLUMNS partitioned tables, the data needs to meet the specified partitioning conditions of the table. If the data to be inserted does not meet any of these conditions, either the execution of the statement will fail or the non-compliant data will be ignored.

   Starting from v7.3.0, List and List COLUMNS partitioned tables support default partitions. After a default partition is created, if the data to be inserted does not meet any partitioning condition, it will be written to the default partition. This feature improves the usability of List and List COLUMNS partitioning, avoiding the execution failure of the `INSERT` statement or data being ignored due to data that does not meet partitioning conditions.

    Note that this feature is a TiDB extension to MySQL syntax. For a partitioned table with a default partition, the data in the table cannot be directly replicated to MySQL.

    For more information, see [documentation](/partitioned-table.md#list-partition).

### DB operations

- note 1

- note 2

### Observability

* Show the progress of collecting statistics [#44033](https://github.com/pingcap/tidb/issues/44033) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1380-->

    Collecting statistics for large tables often takes a long time. In previous versions, you cannot see the progress of collecting statistics, and therefore cannot predict the completion time. TiDB v7.3.0 introduces a feature to show the progress of collecting statistics. You can view the overall workload, current progress, and estimated completion time for each subtask using the system table `mysql.analyze_jobs` or `SHOW ANALYZE STATUS`. In scenarios such as large-scale data import and SQL performance optimization, this feature helps you understand the overall task progress and improves the user experience.

    For more information, see [documentation](/sql-statements/sql-statement-show-analyze-status.md).

* Plan Replayer supports exporting historical statistics [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1445-->

    Starting from v7.3.0, with the newly added [`dump with stats as of timestamp`](/sql-plan-replayer.md) clause, Plan Replayer can export the statistics of specified SQL-related objects at a specific point in time. During the diagnosis of execution plan issues, accurately capturing historical statistics can help analyze more precisely how the execution plan was generated at the time when the issue occurred. This helps identify the root cause of the issue and greatly improves efficiency in diagnosing execution plan issues.

    For more information, refer to [user documentation](/sql-plan-replayer.md).

### Data migration

* TiDB Lightning introduces a new version of conflict data detection and handling strategy [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716) **tw@hfxsd** <!--1296-->

    In previous versions, TiDB Lightning uses different conflict detection and handling methods for Logical Import Mode and Physical Import Mode, which are complex to configure and not easy for users to understand. In addition, Physical Import Mode cannot handle conflicts using the `replace` or `ignore` strategy. Starting from v7.3.0, TiDB Lightning introduces a unified conflict detection and handling strategy for both Logical Import Mode and Physical Import Mode. You can choose to report an error (`error`), replace (`replace`) or ignore (`ignore`) conflicting data when encountering conflicts. You can limit the number of conflict records, such as the task is interrupted and terminated after processing a specified number of conflict records. Furthermore, the system can record conflicting data for troubleshooting.

    For import data with many conflicts, it is recommended to use the new version of the conflict detection and handling strategy for better performance. In the lab environment, the new version strategy can improve the performance of conflict detection and handling up to three times faster than the old version. This performance value is for reference only. The actual performance might vary depending on your configuration, table structure, and the percentage of conflicting data. Note that the new version and the old version of the conflict strategy cannot be used at the same time. The old conflict detection and handling strategy will be deprecated in the future.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection).

* TiDB Lightning supports Partitioned Raft KV (experimental) [#14916](https://github.com/tikv/tikv/issues/14916) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1507-->

    TiDB Lightning now supports Partitioned Raft KV. This feature helps improve the data import performance of TiDB Lightning.

* TiDB Lightning introduces a new parameter `enable-diagnose-log` to enhance troubleshooting by printing more diagnostic logs [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1517-->

    By default, this feature is disabled and TiDB Lightning only prints logs containing `lightning/main`. When enabled, TiDB Lightning prints logs for all packages (including `client-go` and `tidb`) to help diagnose issues related to `client-go` and `tidb`.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global).

## Compatibility changes

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* TiDB Lightning **tw@hfxsd**

    - `tikv-importer.on-duplicate` is deprecated and replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).
    - The `max-error` parameter, which controls the maximum number of non-fatal errors that TiDB Lightning can tolerate before stopping the migration task, no longer limits import data conflicts. The [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter now controls the maximum number of conflicting records that can be tolerated.

* TiCDC **tw@ran-huang**

    - When Kafka sink uses Avro protocol, if the `force-replicate` parameter is set to `true`, TiCDC reports an error when creating a changefeed.
    - Due to incompatibility between `delete-only-output-handle-key-columns` and `force-replicate` parameters, when both parameters are enabled, TiCDC reports an error when creating a changefeed.
    - When the output protocol is Open Protocol, the `UPDATE` events only output the changed columns.

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | Newly added | Controls whether the `EXPLAIN` statement disables the execution of constant subqueries that can be expanded at the optimization stage.  |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) | Newly added | This variable controls the generation of GlobalStats when partition statistics are missing. |
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730) | Newly added | Controls the strategy for selecting TiFlash replicas when a query requires the TiFlash engine. |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) | Newly added | Controls whether to enable the 32-bit connection ID feature. |
| TiKV | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610) | Modified | Changes the default value from `96MiB` to `50MiB`. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].compaction-guard-min-output-file-size</code>](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | Modified | Changes the default value from `"1MB"` to `"8MB"` to resolve the issue that compaction speed cannot keep up with the write speed during large data writes. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].format-version</code>](/tikv-configuration-file.md#format-version-new-in-v620) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), Ribbon filter is used. Therefore, TiKV changes the default value from `2` to `5`. |
| TiKV | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), Ribbon filter is used. Therefore, TiKV changes the default value from `2` to `5`. |
| TiKV | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV skips writing WAL. Therefore, TiKV changes the default value from `"4GB"` to `1`, meaning that WAL is disabled. |
| TiKV | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV skips writing WAL. Therefore, TiKV changes the default value from `"4GB"` to `1`, meaning that WAL is disabled. |
| TiKV | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to disable redundant log printing, changes the default value from `"10m"` to `"0"`. |
| TiKV | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to compensate for the memory overhead of memtables, TiKV changes the default value from 45% to 30% of the size of total system memory. |
| TiKV | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660) | Modified | To reduce the memory overhead of memtables, when `storage.engine="raft-kv"`, TiKV changes the default value from 25% of the memory of the machine to `0`, which means no limit. When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV changes the default value from 25% to 20% of the memory of the machine. |
| TiKV | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to speed up compaction on lockcf, TiKV changes the default value from `"32MB"` to `"4MB"`. |
|TiDB Lightning  | `conflict.max-record-rows` | Newly added | The new version of strategy to handle conflicting data. It controls the maximum number of rows in the `conflict_records` table. The default value is 100. |
|TiDB Lightning  | `conflict.strategy` | Newly added | The new version of strategy to handle conflicting data.  It includes the following options: "" (TiDB Lightning does not detect and process conflicting data), `error` (terminate the import and report an error if a primary or unique key conflict is detected in the imported data), `replace` (when encountering data with conflicting primary or unique keys, the new data is retained and the old data is overwritten.), `ignore` (when encountering data with conflicting primary or unique keys, the old data is retained and the new data is ignored.). The default value is "", that is, TiDB Lightning does not detect and process conflicting data. |
|TiDB Lightning  | `conflict.threshold` | Newly added | Controls the upper limit of the conflicting data. When `conflict.strategy="error"`, the default value is `0`. When `conflict.strategy="replace”` or `conflict.strategy=“ignore"`, you can set it as a maxint. |
|TiDB Lightning  | `enable-diagnose-logs` | Newly added | Controls whether to enable the diagnostic logs. The default value is `false`, that is, only the logs related to the import are output, and the logs of other dependent components are not output. When you set it to `true`, logs from both the import process and other dependent components are output, and GRPC debugging is enabled, which can be used for diagnosis. |
|TiDB Lightning  | `tikv-importer.on-duplicate` | Deprecated | Controls action to do when trying to insert a conflicting record in the logical import mode. Startign from v7.3.0, this parameter is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
|TiDB Lightning  | `tikv-importer.incremental-import` | Deleted | TiDB Lightning parallel import parameter. Because it could easily be mistaken as an incremental import parameter, this parameter is now renamed to `tikv-importer.parallel-import`. If a user passes in the old parameter name, it will be automatically converted to the new one. |
|TiDB Lightning  | `tikv-importer.parallel-import` | Newly added | TiDB Lightning parallel import parameter. It replaces the existing `tikv-importer.incremental-import` parameter, which could be mistaken as an incremental import parameter and misused.  **tw:qiancai** <!--1516--> |
| Data Migration | `strict-optimistic-shard-mode` | 新增 | 用于兼容历史版本 2.0 分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断，在多个表的 DDL变更有依赖关系的场景，可以及时中断，用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) | Newly added | Empty by default, which means that when the message size exceeds the limit of Kafka topic, the changefeed fails. When this configuration is set to `"handle-key-only"`, if the message exceeds the size limit, only the handle key will be sent to reduce the message size; if the reduced message still exceeds the limit, then the changefeed fails. |
| TiCDC | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | The encoding method of binary data, which can be `'base64'` or `'hex'`. The default value is `'base64'`. |

### 系统表

- 新增系统表 `mysql.tidb_timers` 用来存储系统内部定时器的元信息。
	
## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    <!-- Oreoxmt -->
    - Introduce a new system variable [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) to control whether the `EXPLAIN` statement executes subqueries in advance during the optimization phase [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros) **tw@Oreoxmt** <!--983-->
    - When [Global Kill](/tidb-configuration-file#enable-global-kill-new-in-v610) is enabled, you can terminate the current session by pressing <kbd>Control+C</kbd> [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu) **tw@Oreoxmt**
    - Support the `IS_USED_LOCK()` locking function [#44493](https://github.com/pingcap/tidb/issues/44493) @[dveeden](https://github.com/dveeden)
    - Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    <!-- Oreoxmt -->
    - Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get_region_read_progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) [@ekexium](https://github.com/ekexium)

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

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## Bug fixes

+ TiDB

    <!-- Oreoxmt -->
    - Fix the issue that when the MySQL Cursor Fetch protocol is used, the memory consumption of result sets might exceed the `tidb_mem_quota_query` limit and causes TiDB OOM. After the fix, TiDB will automatically write result sets to the disk to release memory [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao) <!--1430-->
    - Fix the TiDB panic issue caused by data race [#45561](https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)
    - Fix the hang-up issue that occurs when queries with `indexMerge` are killed [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that query results in MPP mode are incorrect when `tidb_enable_parallel_apply` is enabled [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - Fix the issue that `resolve lock` might hang when there is a sudden change in PD time [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the GC Resolve Locks step might miss some pessimistic locks [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the query with `ORDER BY` returns incorrect results in dynamic pruning mode [#45007](https://github.com/pingcap/tidb/issues/45007) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    <!-- Oreoxmt -->
    - Fix the issue that in some rare cases, reading data during GC might cause TiKV panic [#15109](https://github.com/tikv/tikv/issues/15109) [@MyonKeminta](https://github.com/MyonKeminta)

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