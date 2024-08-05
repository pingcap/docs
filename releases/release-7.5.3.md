---
title: TiDB 7.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.3.
---

# TiDB 7.5.3 Release Notes

Release date: xx xx, 2024

TiDB version: 7.5.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes
<!-- tw: @Oreoxmt (1)-->
- Add a new system table [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) to display the information of all keywords supported by TiDB [#48801](https://github.com/pingcap/tidb/issues/48801) @[dveeden](https://github.com/dveeden)

## Improvements

+ TiDB

    - (dup): release-8.2.0.md > Improvements> TiDB - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing the `TRUNCATE` or `DROP` operation on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV
  <!-- tw: @qiancai (1)-->
    - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)

+ PD
  <!-- tw: @qiancai (0)-->

+ TiFlash

    - (dup): release-8.1.0.md > Improvements> TiFlash - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - (dup): release-8.2.0.md > Improvements> TiFlash - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)
      <!-- tw: @Oreoxmt (1)-->
        - (dup): release-8.2.0.md > Improvements> Tools> Backup & Restore (BR) - Except for the `br log restore` subcommand, all other `br log` subcommands support skipping the loading of the TiDB `domain` data structure to reduce memory consumption [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > Improvements> Tools> Backup & Restore (BR) - Support automatically abandoning log backup tasks when encountering a large checkpoint lag, to avoid prolonged blocking GC and potential cluster issues [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > Improvements> Tools> Backup & Restore (BR) - Increase the number of retries for failures caused by DNS errors [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.1.0.md > Improvements> Tools> Backup & Restore (BR) - Add PITR integration test cases to cover compatibility testing for log backup and adding index acceleration [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.10.md > 改进提升> Tools> Backup & Restore (BR) - 增加因 Region 没有 leader 导致的失败重试次数 [#54017](https://github.com/pingcap/tidb/issues/54017) @[Leavrth](https://github.com/Leavrth)
        - Support setting Alibaba Cloud access credentials through environment variables [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - (dup): release-6.5.10.md > Improvements> Tools> TiCDC - Support directly outputting raw events when the downstream is a Message Queue (MQ) or cloud storage [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB
  <!-- tw: @hfxsd (8)-->
    - Fix the issue that loading index statistics might cause memory leaks [#54022](https://github.com/pingcap/tidb/issues/54022) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that the `UPDATE` operation can cause TiDB OOM in multi-table scenarios [#53742](https://github.com/pingcap/tidb/issues/53742) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that indirect placeholder `?' references in a `GROUP BY` statement cannot find columns [#53872] https://github.com/pingcap/tidb/issues/53872 @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `LENGTH()` condition is unexpectedly removed when the sort rule is `utf8_bin` or `utf8mb4_bin` [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that inserting an overlarge number in scientific notation returns a warning instead of an error, making it consistent with MySQL [#47787](https://github.com/pingcap/tidb/issues/47787) @[qw4990](https://github.com/qw4990)
    - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that statistics do not update the `stats_history` table when encountering primary key duplicates [#47539](https://github.com/pingcap/tidb/issues/47539) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that when queries contain non-correlated subqueries and `LIMIT` clauses, column pruning might be incomplete and result in a less optimal plan [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
  <!-- tw: @lilin90 (9)-->
    - Fix the issue of abnormally high memory usage caused by `memTracker` not being detached when the `HashJoin` or `IndexLookUp` operator is the driven side sub-node of the `Apply` operator [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the recursive CTE operator incorrectly tracks memory usage [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the memory used by transactions might be repeatedly tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - Fix the issue that using `SHOW WARNINGS;` to obtain warnings might cause a panic [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - Fix the issue that updating an `UNSIGNED` type of field to `-1` returns `null` instead of `0` when `sql_mode=''` [#47816](https://github.com/pingcap/tidb/issues/47816) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the Connection Count monitoring metric in Grafana is incorrect when some connections exit before the handshake is complete [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the Connection Count of each resource group is incorrect when using TiProxy and resource groups [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that executing `CREATE OR REPLACE VIEW` concurrently might result in the `table doesn't exist` error [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that TiDB might return incorrect query results when you query tables with virtual columns in transactions that involve data modification operations [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue of incorrect WARNINGS information when using Optimizer Hints [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that the `memory_quota` hint might not work in subqueries [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that JSON-related functions return errors inconsistent with MySQL in some cases [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that certain filter conditions in queries might cause the planner module to report an `invalid memory address or nil pointer dereference` error [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that after a statement within a transaction is killed by OOM, if TiDB continues to execute the next statement within the same transaction, you might get an error `Trying to start aggressive locking while it's already started` and a panic occurs [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that executing `ALTER TABLE ... REMOVE PARTITIONING` might cause data loss [#53385](https://github.com/pingcap/tidb/issues/53385) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that `PREPARE`/`EXECUTE` statements with the `CONV` expression containing a `?` argument might result in incorrect query results when executed multiple times [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the query latency of stale reads increases, caused by information schema cache misses [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the `STATE` field in the `INFORMATION_SCHEMA.TIDB_TRX` table is empty due to the `size` of the `STATE` field not being defined [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that the `tidb_enable_async_merge_global_stats` and `tidb_analyze_partition_concurrency` system variables do not take effect during automatic statistics collection [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that using `CURRENT_DATE()` as the default value for a column results in incorrect query results [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)

+ TiKV
  <!-- tw: @Oreoxmt (1)-->
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that setting the gRPC message compression method via `grpc-compression-type` does not take effect on messages sent from TiKV to TiDB [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that highly concurrent Coprocessor requests might cause TiKV OOM [#16653](https://github.com/tikv/tikv/issues/16653) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that CDC and log-backup do not limit the timeout of `check_leader` using the `advance-ts-interval` configuration, causing the `resolved_ts` lag to be too large when TiKV restarts normally in some cases [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that TiKV might repeatedly panic when applying a corrupted Raft data snapshot [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD
  <!-- tw: @qiancai (8)-->
    - (dup): release-7.1.4.md > Bug fixes> PD - Fix the issue that slots are not fully deleted in a resource group client, which causes the number of the allocated tokens to be less than the specified value [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that a resource group encounters quota limits when requesting tokens for more than 500ms [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - Fix the data race issue of resource groups [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - Fix the data race issue that PD encounters during operator checks [#8263](https://github.com/tikv/pd/issues/8263)](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that deleted nodes still appear in the candidate connection list in etcd client [#8286](https://github.com/tikv/pd/issues/8286) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that setting the TiKV configuration item [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) to a value less than 1 MiB causes PD panic [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the encryption manager is not initialized before use [#8384](https://github.com/tikv/pd/issues/8384) @[releungx](https://github.com/releungx)
    - Fix the issue that PD logs are not fully redacted when the PD configuration item [`redact-info-log`](/pd-configuration-file.md#redact-info-log-new-in-v50) is enabled [#8419](https://github.com/tikv/pd/issues/8419) @[releungx](https://github.com/releungx)
    - Fix the issue that no error is reported when binding a role to a resource group [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)

+ TiFlash
  <!-- tw: @Oreoxmt (4)-->
    - (dup): release-8.2.0.md > Bug fixes> TiFlash - Fix the issue that a large number of duplicate rows might be read in FastScan mode after importing data via BR or TiDB Lightning [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.10.md > Bug fixes> TiFlash - Fix the issue that the `SUBSTRING_INDEX()` function might cause TiFlash to crash in some corner cases [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that some queries might report a type mismatch error after enabling late materialization [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that queries with virtual generated columns might return incorrect results after enabling late materialization [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might panic after executing `RENAME TABLE ... TO ...` on a partitioned table with empty partitions across databases [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)
      <!-- tw: @Oreoxmt (1)-->
        - (dup): release-6.5.10.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup might be paused after the advancer owner migration [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-6.5.10.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR fails to correctly identify errors due to multiple nested retries during the restore process [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.2.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - (dup): release-8.2.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that after pausing, stopping, and rebuilding the log backup task, the task status is normal, but the checkpoint does not advance [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)

    + TiCDC
      <!-- tw: @Oreoxmt (2)-->
        - Fix the issue that the checksum is not correctly set to `0` after splitting Update events [#11402](https://github.com/pingcap/tiflow/issues/11402) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the Processor module might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - (dup): release-6.5.10.md > Bug fixes> Tools> Dumpling - Fix the issue that Dumpling reports an error when exporting tables and views at the same time [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
