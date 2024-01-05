---
title: TiDB 6.5.7 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.7.
---

# TiDB 6.5.7 Release Notes

Release date: xx x, 2024

TiDB version: 6.5.7

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.7#version-list)

## Compatibility changes

<!-- tw@Oreoxmt -->

+ Introduce the system variable [`tidb_opt_fix_control`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_opt_fix_control-new-in-v657) to provide a more fine-grained control over the optimizer and help to prevent performance regression after upgrading caused by behavior changes in the optimizer [#43169](https://github.com/pingcap/tidb/issues/43169) @[qw4990](https://github.com/qw4990)
+ Introduce the TiDB configuration item [`performance.force-init-stats`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#force-init-stats-new-in-v657) to control whether TiDB needs to wait for statistics initialization to finish before providing services during TiDB startup [#43385](https://github.com/pingcap/tidb/issues/43385) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
+ To reduce the overhead of log printing, TiFlash changes the default value of `logger.level` from `"debug"` to `"info"` [#8568](https://github.com/pingcap/tiflash/issues/8568) @[xzhangxian1008](https://github.com/xzhangxian1008)

## Improvements

+ TiDB
    <!-- tw@Oreoxmt -->
    - (dup): release-7.4.0.md > 改进提升> TiDB - Optimize memory usage and performance for `ANALYZE` operations on partitioned tables [#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @[hawkingrei](https://github.com/hawkingrei)
    - Support Plan Cache to cache execution plans with the `PointGet` operator generated during physical optimization using Optimizer Fix Controls [#44830](https://github.com/pingcap/tidb/issues/44830) @[qw4990](https://github.com/qw4990)
    - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash

    <!-- tw@Oreoxmt -->
    - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
+ Tools

    + Backup & Restore (BR)
        <!-- tw@qiancai -->
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - Resolve compatibility issues between EBS-based snapshot backups and TiDB Lightning imports [#46850](https://github.com/pingcap/tidb/issues/46850) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.4.0.md > 改进提升> Tools> Backup & Restore (BR) - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC
        <!-- tw@qiancai -->
        - When the downstream is Kafka, the topic expression allows `schema` to be optional and supports specifying a topic name directly [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 无 release notes

    + TiDB Lightning

        - 无 release notes

    + Dumpling

        - 无 release notes

    + TiUP

        - 无 release notes

    + TiDB Binlog

        - 无 release notes

## Bug fixes

+ TiDB

    - (dup): release-6.6.0.md > 错误修复> TiDB - Fix the issue that `stats_meta` is not created following table creation [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the incorrect error message for `ErrLoadDataInvalidURI` (invalid S3 URI error) [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that queries containing common table expressions (CTEs) unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that queries containing CTEs report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.1.3.md > 错误修复> TiDB - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    <!-- tw@ran-huang -->
    - Fix the issue of possible statistics data errors when importing statistics exported from early versions of TiDB [#42931](https://github.com/pingcap/tidb/issues/42931) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the optimizer incorrectly converts TiFlash selection path to TableDual in specific scenarios [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that parsing invalid values of `ENUM` or `SET` types would directly cause SQL statement errors [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - Fix the issue that `UPDATE` or `DELETE` statements containing 'WITH RECURSIVE' CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - Fix the issue that using the `_` wildcard in `LIKE` when the data contains trailing spaces can result in incorrect query results [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    <!-- tw@hfxsd -->
    - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that in non-strict mode (`sql_mode = ''`), truncation during executing `INSERT` still reports an error [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB panics and reports an error `invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)

+ TiKV

    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复损坏的 SST 文件可能会扩散到其他 TiKV 节点的问题 [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复跟踪大型事务时，Stale Read 中的 Resolved TS 可能导致 TiKV OOM 的问题 [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > 错误修复> TiKV - 修复 TiKV 由于无法 append Raft log 导致报错 `ServerIsBusy` [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - 修复 Placement Rules in SQL 设置的 location-labels 在特定条件下不按预期调度的问题 [#6637](https://github.com/tikv/pd/issues/6637) @[rleungx](https://github.com/rleungx)
    - 修复在不满足副本数量需求时，删除 orphan peer 的问题 [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!-- tw@Oreoxmt -->

    - (dup): release-7.1.3.md > 错误修复> TiFlash - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.1.3.md > 错误修复> TiFlash - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - (dup): Fix incorrect display of maximum percentile time for some panels in Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.1.3.md > 错误修复> Tools> Backup & Restore (BR) - 修复在任务初始化阶段出现与 PD 的连接错误导致日志备份任务虽然启动但无法正常工作的问题 [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复大宽表场景下，日志备份在某些场景中可能卡住的问题 [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!-- tw@qiancai -->

        - Fix the issue that `checkpoint-ts` might get stuck when TiCDC replicates data to downstream MySQL [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)
        - Fix the potential data race issue during `kv-client` initialization [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - 无 release notes

    + TiDB Lightning

        - 无 release notes

    + Dumpling

        - 无 release notes

    + TiUP

        - 无 release notes

    + TiDB Binlog

        - 无 release notes
