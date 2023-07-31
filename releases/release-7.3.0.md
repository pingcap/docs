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

* TiFlash 支持副本选择策略 [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu) **tw@qiancai** <!--1394-->

    在 v7.3.0 之前，当 TiFlash 进行数据扫描和 MPP 计算时，会尽可能使用其所有节点的副本，以提供最强大的性能。从 v7.3.0 起，TiFlash 引入副本选择策略，该策略由系统变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入) 控制，可以根据节点的[区域属性](/schedule-replicas-by-topology-labels.md#设置-tidb-的-labels可选)选择特定的副本，调度部分节点进行数据扫描及 MPP 计算。

    当集群部署在多个机房且每个机房都拥有完整的 TiFlash 数据副本时，你可以设置该策略只选择使用当前机房的 TiFlash 副本，即在当前机房的 TiFlash 节点中进行数据扫描和 MPP 计算，从而避免大量跨机房的网络数据传输。

    更多信息，请参考[用户文档](/system-variables.md/system-variables.md#tiflash_replica_read-从-v730-版本开始引入)。

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

* 手工标记资源使用超出预期的查询 (实验特性) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB) **tw@hfxsd** <!--1446-->

    在 v7.2.0 中，TiDB 对资源使用超出预期的查询 (Runaway Queries) 实施自动管理，运行时间超过预期的查询能够被自动降级或取消。在实际运行时，只依靠规则无法筛覆盖所有情况。 因此，在 v7.3.0 中，TiDB 补充了手工标记查询的能力。 利用新增的命令 [`QUERY WATCH`]()，用户可以根据 SQL 的文本、SQL Digest、或者执行计划对查询进行标记，命中的查询可以被降级或取消。

    手工标记 Runaway Queries 的能力，为数据库中突发的性能问题提供了有效的干预手段。针对由查询引发的性能问题，在找到问题根本原因之前，能够快速缓解其对整体性能的影响，提升系统服务质量。

    更多信息，请参考[用户文档](/tidb-resource-control#管理资源消耗超出预期的查询-runaway-queries)。

### SQL

* List 和 List COLUMNS 分区表支持默认分区 [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133) **tw@qiancai** <!--1342-->

    当使用 `INSERT` 语句向 List 或 List COLUMNS 分区表插入数据时，这些数据需要满足分区表指定的分区条件。如果要插入的数据不匹配任何分区条件，该语句将执行失败或不符合分区条件的数据被忽略。

    在 v7.3.0 中，List 和 List COLUMNS 分区表支持默认分区功能。在创建默认分区后，如果要插入的数据不匹配任何分区条件，则数据将被写入默认分区。默认分区功能可以提升 List 分区和 List COLUMNS 分区的使用便捷性，避免不符合分区条件的数据导致 `INSERT` 语句执行失败或者数据被忽略。该功能默认关闭，可通过 [`tidb_enable_default_list_partition`](/system-variables.md#tidb_enable_default_list_partition-new-in-v730) 变量开启。

    更多信息，请参考[用户文档](/partitioned-table.md#list-分区)。

### DB operations

- note 1

- note 2

### Observability

* 显示统计信息收集的进度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1380-->

    对大表的统计信息收集经常会持续比较长的时间。在过去的版本里，用户无从得知统计信息收集的进度，进而没法预测完成时间。在 v7.3.0 中，TiDB 加入了对统计信息收集进度的信息展示，能够显示各个子任务的总体工作量、当前进度、以及对完成时间的预测。在大规模数据导入、SQL 性能优化等场景下，用户能够了解整体任务进展，提升用户体验。

    更多信息，请参考[用户文档](链接)。

* Plan Replayer supports exporting historical statistics [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1445-->

    Starting from v7.3.0, with the newly added [`dump with stats as of timestamp`](/sql-plan-replayer.md) clause, Plan Replayer can export the statistics of specified SQL-related objects at a specific point in time. During the diagnosis of execution plan issues, accurately capturing historical statistics can help analyze more precisely how the execution plan was generated at the time when the issue occurred. This helps identify the root cause of the problem and greatly improves efficiency in diagnosing execution plan issues.

    For more information, refer to [user documentation](/sql-plan-replayer.md).

### Data migration

* Lightning 引入新版冲突数据检测与处理的能力 [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716) **tw@hfxsd** <!--1296-->

    之前的版本 Lightning 逻辑导入和物理导入模式都有各自的冲突检测和处理的方式，配置较为复杂且不利于用户理解。同时使用物理导入模式，冲突的数据无法通过 replace 和 ignore 策略来处理。新版的冲突检测和处理方式，逻辑导入和物理导入都是用同一套冲突检测和处理方式即遇到冲突数据报错，或者 replace 以及 ignore 掉冲突数据。同时还支持用户设置冲突记录的上限，如处理多少冲突记录后任务中断退出，用户也可以让程序记录哪些数据发生了冲突，方便用户排查。

    在明确所需导入数据有较多的冲突数据时，推荐使用新版的冲突检测和处理策略，会有更好的性能。注意新、旧版冲突策略互斥使用，会在未来废弃掉旧版冲突检测和处理策略。

    更多信息，请参考[用户文档](链接)。

* Lightning 支持 Partitioned Raft KV（实验特性） [#15069](https://github.com/tikv/tikv/pull/15069) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1507-->

    该版本 Lightning 支持了 Partitioned Raft KV ，当用户使用了 Partitioned Raft KV 特性后，能提升 Lightning 导入数据的性能。

    更多信息，请参考[用户文档](链接)。

* Lightning 引入新的参数"enable-diagnose-log" 用于打印更多的诊断日志，方便定位问题 [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1517-->

    默认情况下，此功能未启用，只会打印包含 "lightning/main" 的日志。当启用时，将打印所有包（包括 "client-go" 和 "tidb"）的日志，以帮助诊断与 "client-go" 和 "tidb" 相关的问题。

    更多信息，请参考[用户文档](链接)。

## Compatibility changes

> **注意：**
>
> 以下为从 v7.1.0 升级至当前版本 (v7.2.0) 所需兼容性变更信息。如果从 v7.0.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 release notes 中提到的兼容性变更信息。

### Behavior changes

<!-- 此小节包含 MySQL 兼容性变更-->

* TiDB Lightning **tw@hfxsd**

    - 逻辑导入模式插入冲突数据时执行的操作，默认配置从 on-duplicate = "replace" 改为 on-duplicate = "error" 即遇到冲突数据即报错。
    - TiDB Lightning 停止迁移任务之前能容忍的最大非严重 (non-fatal errors) 错误数的参数 "max-error" 不再包含导入数据冲突的上限。而是由新的参数 "conflict.threshold" 来控制可容忍的最大冲突的记录数。

* 兼容性 2

### System variables

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_remove_orderby_in_subquery`](/system-variables.md#tidb_remove_orderby_in_subquery-从-v610-版本开始引入) | 修改 | 经进一步的测试后，该变量默认值从 `OFF` 修改为 `ON`，即优化器改写会移除子查询中的 `ORDER BY` 子句。 |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
| TiDB Lightning | `send-kv-pairs` | 废弃 | 从 7.2 版本开始 TiDB Lightning 配置文件的参数 "send-kv-pairs" 不再生效，由新的参数 "send-kv-size" 代替。该新参数用于指定 KV 键值对的大小阈值，单位为 KiB 或 MiB，默认值为 "16 KiB"。当 KV 键值对的大小达到设定的阈值时，它们将立即发送到 TiKV，避免在导入大宽表等一些场景因为 Lightning 节点内存积累键值对过多导致 OOM 的问题。**tw@hfxsd** <!--1420--> |
| TiDB Lightning | `send-kv-size` | 新增 | 从 7.2 版本开始在 Lightning 配置文件 "[tikv-importer]" 这个 Session 中引入 `send-kv-size` 参数，用于设置发单次送到 TiKV 的 KV pairs 的大小。当 KV 键值对的大小达到设定的阈值时，它们将被 Lightning 立即发送到 TiKV，避免在导入大宽表的时候 Lightning 节点因为内存积累键值对过多导致 OOM 的问题。通过调整 "send-kv-size" 参数，你可以在内存使用和导入速度之间找到平衡，提高导入过程的稳定性和效率。**tw@hfxsd** <!--1420-->|
| Data Migration | `strict-optimistic-shard-mode` | 新增 | 用于兼容历史版本 2.0 分库分表同步 DDL 的行为。当用户选择乐观模式时，可以启用该参数，开启后，乐观模式下，同步任务遇到二类 DDL 时，整个任务会中断，在多个表的 DDL变更有依赖关系的场景，可以及时中断，用户手动处理完各表的 DDL 后，再继续同步数据，保障上下游数据的一致性。 **tw@ran-huang** <!--1414-->|

## Deprecated features

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## Improvements

+ TiDB

    - 游标 (Cursor) 结果过大时，写入 TiDB 临时磁盘空间从而避免OOM [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao) <!--1430-->
    - EXPLAIN 新增开关用以展示在优化期间被执行的子查询 [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros] **tw@Oreoxmt** <!--983-->
    - 在启用 [`Global Kill`](/tidb-configuration-file#enable-global-kill-从-v610-版本开始引入) 的情况下，可以通过 Ctrl+C 终止当前会话。 [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - 支持新的 DTFile 格式版本，减少物理文件数量（实验特性） [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--？-->
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - 为外部存储 Azure Blob Storage 提供加密范围和加密密钥的支持 [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1385-->
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