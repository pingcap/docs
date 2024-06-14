---
title: TiDB 6.5.10 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.10.
---

# TiDB 6.5.10 Release Notes

Release date: June xx, 2024

TiDB version: 6.5.10

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## Compatibility changes

<!-- tw:@hfxsd 1-->
- (dup): release-7.5.2.md > Compatibility changes - In earlier versions, when processing a transaction containing `UPDATE` changes, if the primary key or non-null unique index value is modified in an `UPDATE` event, TiCDC splits this event into `DELETE` and `INSERT` events. Starting from v6.5.2, when using the MySQL sink, TiCDC splits an `UPDATE` event into `DELETE` and `INSERT` events if the transaction `commitTS` for the `UPDATE` change is less than TiCDC `thresholdTS` (which is the current timestamp fetched from PD when TiCDC starts replicating the corresponding table to the downstream). This behavior change addresses the issue of downstream data inconsistencies caused by the potentially incorrect order of `UPDATE` events received by TiCDC, which can lead to an incorrect order of split `DELETE` and `INSERT` events. For more information, see [documentation](https://docs.pingcap.com/tidb/v6.5/ticdc-behavior-change#mysql-sink). [#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)
- TiDB Lightning 使用严格格式 `strict-format` 导入 CSV 文件时必须设置行分隔符 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

## Improvements

+ TiDB

    - (dup): release-8.1.0.md > Improvements> TiDB - Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.5.2.md > Improvements> TiDB - Remove stores without Regions during MPP load balancing [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - (dup): release-8.1.0.md > Improvements> TiKV - Accelerate the shutdown speed of TiKV [#16680](https://github.com/tikv/tikv/issues/16680) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.2.md > Improvements> TiKV - Add monitoring metrics for the queue time for processing CDC events to facilitate troubleshooting downstream CDC event latency issues [#16282](https://github.com/tikv/tikv/issues/16282) @[hicqu](https://github.com/hicqu)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-8.1.0.md > Improvements> Tools> Backup & Restore (BR) - BR cleans up empty SST files during data recovery [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.2.md > Improvements> Tools> Backup & Restore (BR) - Increase the number of retries for failures caused by DNS errors [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC
      <!-- tw:@Oreoxmt 1-->
        - Support directly outputting raw events when the downstream is a Message Queue (MQ) or cloud storage [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.1.0.md > Improvements> Tools> TiCDC - Improve memory stability during data recovery using redo logs to reduce the probability of OOM [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.1.0.md > Improvements> Tools> TiCDC - Significantly improve the stability of data replication in transaction conflict scenarios, with up to 10 times performance improvement [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB
  <!-- tw:@qiancai 6-->
    - 修复一些情况下对元数据查询会导致内存使用过大的问题 [#52219](https://github.com/pingcap/tidb/issues/52219) @[hawkingrei](https://github.com/hawkingrei)
    - 修复表结构中设置 AUTO_ID_CACHE=1 时，使用非默认的 @@auto_increment_increment 和 @@auto_increment_offset 会导致错误 ID 分配的问题 [#52622](https://github.com/pingcap/tidb/issues/52622) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复表结构中设置 AUTO_ID_CACHE=1 时，使用 RESTORE 命令恢复表数据后 ID 分配可能错误的问题 [#52680](https://github.com/pingcap/tidb/issues/52680) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 infoschema `tidb_trx` 表 txn size 字段未定义的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复创建带有外键的表时，TiDB 不会创建对应的统计信息元信息（stats_meta）的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在查询并发较高时，统计信息同步加载机制可能在没有发生错误时意外加载失败的问题。 [#52294](https://github.com/pingcap/tidb/issues/52294) @[hawkingrei](https://github.com/hawkingrei)
  <!-- tw:@lilin90 6-->
    - 修复 tidb_enable_async_merge_global_stats 被关闭时，GlobalStats 中的 NDV 信息可能错误的问题。 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - 修复重启 TiDB 后，主键列统计信息中的直方图和 TopN 可能不会被加载的问题。 [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询中的某些过滤条件可能导致 planner 模块“invalid memory address or nil pointer dereference”报错的问题。 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 ? 参数时，多次执行可能导致查询结果错误的问题。 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题。 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 information schema 缓存未命中导致的 stale read 延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
  <!-- tw:@hfxsd 3-->
    - 修复 DDL 错误使用 etcd 导致任务排队等问题 [#52335](https://github.com/pingcap/tidb/issues/52335) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复重命名表达式索引残留内部列的问题 [#51431](https://github.com/pingcap/tidb/issues/51431) @[ywqzzy](https://github.com/ywqzzy)
    - 修复并发执行 CREATE OR REPLACE VIEW 可能报错 “table doesn't exist” 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.2.md > 错误修复> TiDB - 修复在 `AUTO_ID_CACHE=1` 时，AutoID Leader 发生变更可能造成自增列的值减少的问题 [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that TiDB might panic when the JOIN condition contains an implicit type conversion [#46556](https://github.com/pingcap/tidb/issues/46556) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that DDL operations get stuck due to network problems [#47060](https://github.com/pingcap/tidb/issues/47060) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that IndexJoin produces duplicate rows when calculating hash values in the Left Outer Anti Semi type [#52902](https://github.com/pingcap/tidb/issues/52902) @[yibin87](https://github.com/yibin87)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that subqueries included in the `ALL` function might cause incorrect results [#52755](https://github.com/pingcap/tidb/issues/52755) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that the `TIMESTAMPADD()` function returns incorrect results [#41052](https://github.com/pingcap/tidb/issues/41052) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-8.1.0.md > Bug fixes> TiDB - Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that subqueries in an `UPDATE` list might cause TiDB to panic [#52687](https://github.com/pingcap/tidb/issues/52687) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the overflow issue of the `Longlong` type in predicates [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue of inconsistent data indexes caused by concurrent DML operations when adding a unique index [#52914](https://github.com/pingcap/tidb/issues/52914) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that TiDB might panic when parsing index data [#47115](https://github.com/pingcap/tidb/issues/47115) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that column pruning without using shallow copies of slices might cause TiDB to panic [#52768](https://github.com/pingcap/tidb/issues/52768) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that using a view does not work in recursive CTE [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.2.0.md > Bug fixes> TiDB - Fix the issue that the `LEADING` hint does not support querying block aliases [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.0.md > Bug fixes> TiDB - Fix the incorrect result of the TopN operator in correlated subqueries [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that unstable unique IDs of columns might cause the `UPDATE` statement to return errors [#53236](https://github.com/pingcap/tidb/issues/53236) @[winoros](https://github.com/winoros)
    - (dup): release-7.1.5.md > Bug fixes> TiDB - Fix the issue that TiDB keeps sending probe requests to a TiFlash node that has been offline [#46602](https://github.com/pingcap/tidb/issues/46602) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that comparing a column of `YEAR` type with an unsigned integer that is out of range causes incorrect results [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.1.5.md > Bug fixes> TiDB - Fix the issue that AutoID Leader change might cause the value of the auto-increment column to decrease in the case of `AUTO_ID_CACHE=1` [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.0.0.md > 错误修复> TiDB - Fix the issue that non-BIGINT unsigned integers might produce incorrect results when compared with strings/decimals [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - (dup): release-7.5.2.md > 错误修复> TiDB - Fix the issue that data conversion from the `FLOAT` type to the `UNSIGNED` type returns incorrect results [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that `VAR_SAMP()` cannot be used as a window function [#52933](https://github.com/pingcap/tidb/issues/52933) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that a wrong TableDual plan causes empty query results [#50051](https://github.com/pingcap/tidb/issues/50051) @[onlyacat](https://github.com/onlyacat)
    - (dup): release-8.1.0.md > Bug fixes> TiDB - Fix the issue that the TiDB synchronously loading statistics mechanism retries to load empty statistics indefinitely and prints the `fail to get stats version for this histogram` log [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that an empty projection causes TiDB to panic [#49109](https://github.com/pingcap/tidb/issues/49109) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that the TopN operator might be pushed down incorrectly [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.2.md > Bug fixes> TiDB - Fix the issue that TiDB panics when executing the `SHOW ERRORS` statement with a predicate that is always `true` [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-8.1.0.md > Bug fixes> TiDB - Fix the issue that the metadata lock fails to prevent DDL operations from executing in the plan cache scenario [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - (dup): release-7.5.2.md > Bug fixes> TiKV - Fix the issue that slow `check-leader` operations on one TiKV node cause `resolved-ts` on other TiKV nodes to fail to advance normally [#15999](https://github.com/tikv/tikv/issues/15999) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-7.5.2.md > Bug fixes> TiKV - Fix the issue that the `CONV()` function in queries might overflow during numeric system conversion, leading to TiKV panic [#16969](https://github.com/tikv/tikv/issues/16969) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.2.md > Bug fixes> TiKV - Fix the issue of unstable test cases, ensuring that each test uses an independent temporary directory to avoid online configuration changes affecting other test cases [#16871](https://github.com/tikv/tikv/issues/16871) @[glorv](https://github.com/glorv)
    - (dup): release-7.5.2.md > Bug fixes> TiKV - Fix the issue that the decimal part of the `DECIMAL` type is incorrect in some cases [#16913](https://github.com/tikv/tikv/issues/16913) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-8.1.0.md > Bug fixes> TiKV - Fix the issue that resolve-ts is blocked when a stale Region peer ignores the GC message [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)

+ PD

    - (dup): release-8.1.0.md > Bug fixes> PD - Fix the issue that the Leader fails to transfer when you switch it between two deployed data centers [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - (dup): release-7.5.2.md > Bug fixes> PD - Fix the issue that down peers might not recover when using the placement policy [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.1.0.md > Bug fixes> PD - Fix the issue that the `Filter target` monitoring metric for PD does not provide scatter range information [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)

+ TiFlash
  <!-- tw:@hfxsd 3-->
    - 修复跨 database 之间执行 `ALTER TABLE ... EXCHANGE PARTITION` 后可能导致 TiFlash 同步 schema 失败的问题 [#7296](https://github.com/pingcap/tiflash/issues/7296) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复收到空的 Region key-range 查询可能导致 TiFlash 查询被阻塞的问题 [#9108](https://github.com/pingcap/tiflash/issues/9108) @[JinheLin](https://github.com/JinheLin)
    - 修复函数 `SUBSTRING_INDEX` 可能导致 Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-8.1.0.md > Bug fixes> TiFlash - Fix the issue that TiFlash metadata might become corrupted and cause the process to panic when upgrading a cluster from a version earlier than v6.5.0 to v6.5.0 or later [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > Bug fixes> TiFlash - Fix the issue that TiFlash might return transiently incorrect results in high-concurrency read scenarios [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)
      <!-- tw:@Oreoxmt 1-->
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the test case `TestGetTSWithRetry` takes too long to execute [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the Region fetched from PD does not have a Leader when restoring data using BR or importing data using TiDB Lightning in physical import mode [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that a PD connection failure could cause the TiDB instance where the log backup advancer owner is located to panic [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that after pausing, stopping, and rebuilding the log backup task, the task status is normal, but the checkpoint does not advance [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that data restore is slowed down due to absence of a leader on a TiKV node [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the global checkpoint of log backup is advanced ahead of the actual backup file write point due to TiKV restart, which might cause a small amount of backup data loss [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.2.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the transfer of PD leaders might cause BR to panic when restoring data [#53724](https://github.com/pingcap/tidb/issues/53724) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that TiKV might panic when resuming a paused log backup task with unstable network connections to PD [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that log backup might pause after the advancer owner migration [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)

    + TiCDC
      <!-- tw:@Oreoxmt 1-->
        - Fix the issue that the creation of a changefeed job with Syncpoint enabled fails when the downstream database password is Base64 encoded [#10516](https://github.com/pingcap/tiflow/issues/10516) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.1.0.md > Bug fixes> Tools> TiCDC - Fix the issue that `DROP PRIMARY KEY` and `DROP UNIQUE KEY` statements are not replicated correctly [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.1.0.md > Bug fixes> Tools> TiCDC - Fix the issue that the default value of `TIMEZONE` type is not set according to the correct time zone [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning
      <!-- tw:@Oreoxmt 1-->
        - (dup): release-8.1.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that killing the PD Leader causes TiDB Lightning to report the `invalid store ID 0` error during data import [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue of missing data in the TiDB Lightning Grafana dashboard [#43357](https://github.com/pingcap/tidb/issues/43357) @[lichunzhu](https://github.com/lichunzhu)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiDB Lightning - Fix the issue that TiDB Lightning might print sensitive information to logs in server mode [#36374](https://github.com/pingcap/tidb/issues/36374) @[kennytm](https://github.com/kennytm)
        - 在 SHARD_ROW_ID_BITS 与 AUTO_ID_CACHE=1 功能时正确设置 AUTO ID [#52654](https://github.com/pingcap/tidb/issues/52654) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling
      <!-- tw:@Oreoxmt 1-->
        - Fix the issue that Dumpling reports an error when exporting tables and views at the same time [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog
      <!-- tw:@Oreoxmt 1-->
        - Fix the issue that deleting rows in `ADD COLUMN` might report an error `data and columnID count not match` when TiDB Binlog is enabled [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)
