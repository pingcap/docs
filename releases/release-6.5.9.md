---
title: TiDB 6.5.9 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.9.
---

# TiDB 6.5.9 Release Notes

Release date: April xx, 2024

TiDB version: 6.5.9

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.9#version-list)

## Compatibility changes <!--tw@qiancai 2 条-->

- 在 TiKV 中提供 RocksDB [`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#track-and-verify-wals-in-manifest-从-v659-版本开始引入) 配置，用于调查 WAL (Write Ahead Log) 可能损坏问题 [#16549](https://github.com/tikv/tikv/issues/16549) @[v01dstar](https://github.com/v01dstar)
- DR Auto-Sync 支持设置 [`wait-recover-timeout`](https://docs.pingcap.com/zh/tidb/v6.5/two-data-centers-in-one-city-deployment#启用自适应同步模式)，用于控制当网络恢复后切换回 `sync-recover` 状态的等待时间 [#6295](https://github.com/tikv/pd/issues/6295) @[disksing](https://github.com/disksing)

## Improvements

+ TiDB <!--tw@hfxsd 1 条-->

    - (dup): release-8.0.0.md > Improvements> TiDB - When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. This setting no longer blocks the startup of HTTP servers, which enables users to continue monitoring [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the issue that the `ANALYZE` statement blocks the metadata lock [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV <!--tw@qiancai 2 条-->

    - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)
    - 在 raftstore 线程中避免进行快照文件的 IO 操作，提高 TiKV 稳定性 [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-8.0.0.md > Improvements> TiKV - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt 3 条-->

        - Optimize the Recovery Point Objective (RPO) for log backup during rolling restarts. Now, the checkpoint lag of log backup tasks will be smaller during rolling restarts [#15410](https://github.com/tikv/tikv/issues/15410) @[YuJuncen](https://github.com/YuJuncen)
        - Enhance the tolerance of log backup to merge operations. When encountering a reasonable long merge operation, log backup tasks are less likely to enter the error state [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - Support automatically abandoning log backup tasks when encountering a large checkpoint lag, to avoid prolonged blocking GC and potential cluster issues [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-7.4.0.md > Improvements> Tools> Backup & Restore (BR) - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Support ingesting SST files in batch during data restore [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.1.4.md > Improvements> Tools> Backup & Restore (BR) - Remove an outdated compatibility check when using Google Cloud Storage (GCS) as the external storage [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Refactor the BR exception handling mechanism to increase tolerance for unknown errors [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

## Bug fixes

+ TiDB <!--tw@qiancai 以下 6 条-->

    - 修复大量创建表时，新表可能缺失 `stats_meta` 信息导致后续的查询估算无法获取准确行数信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复已删除的表仍然会计入到 Grafana 的 `Stats Healthy Distribution` 面板的问题 [#39349](https://github.com/pingcap/tidb/issues/39349) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复当查询涉及 `MemTableScan` 算子时，TiDB 没有处理 SQL 语句中形如 `WHERE column_name` 的过滤条件的问题 [#40937](https://github.com/pingcap/tidb/issues/40937) @[zhongzc](https://github.com/zhongzc)
    - 修复当子查询中的 `HAVING` 子句包含关联列时，查询结果可能出错的问题 [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当使用 CTE（公共表达式）访问缺少统计信息的分区表时，查询结果可能出错的问题 [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - 修复当 SQL 语句中包含 `JOIN` 且 `SELECT` 列表只包含常量时，使用 MPP 执行查询可能导致查询结果出错的问题 [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that the `AUTO_INCREMENT` attribute causes non-consecutive IDs due to unnecessary transaction conflicts when assigning auto-increment IDs [#50819](https://github.com/pingcap/tidb/issues/50819) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that the monitoring metric `tidb_statistics_auto_analyze_total` on Grafana is not displayed as an integer [#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.4.md > Bug fixes> TiDB - Fix the issue that errors might be returned during the concurrent merging of global statistics for partitioned tables [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that getting the default value of a column returns an error if the column default value is dropped [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.6.0.md > Bug fixes> TiDB - Fix the issue that the `INSERT ignore` statement cannot fill in default values when the column is write-only [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that TiDB crashes when `shuffleExec` quits unexpectedly [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the goroutine leak issue that might occur when the `HashJoin` operator fails to spill to disk [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.0.md > Bug fixes> TiDB - Fix the issue that renaming tables does not take effect when committing multiple statements in a transaction [#39664](https://github.com/pingcap/tidb/issues/39664) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that the query result is incorrect when the `IN()` predicate contains `NULL` [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that querying JSON of `BINARY` type might cause an error in some cases [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that parallel `Apply` might generate incorrect results when the table has a clustered index [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that the `init-stats` process might cause TiDB to panic and the `load stats` process to quit [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.4.md > Bug fixes> TiDB - Fix the issue that the `tidb_merge_partition_stats_concurrency` variable does not take effect when `auto analyze` is processing partitioned tables [#47594](https://github.com/pingcap/tidb/issues/47594) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that after the time window for automatic statistics updates is configured, statistics might still be updated outside that time window [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the `approx_percentile` function might cause TiDB panic [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that `BIT` type columns might cause query errors due to decode failures when they are involved in calculations of some functions [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the goroutine leak issue that occurs when the memory usage of CTE queries exceed limits [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that TiDB does not listen to the corresponding port when `force-init-stats` is configured [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that `ALTER TABLE ... COMPACT TIFLASH REPLICA` might incorrectly end when the primary key type is `VARCHAR` [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - (dup): release-8.0.0.md > Bug fixes> TiDB - Fix the issue that the `tidb_gogc_tuner_threshold` system variable is not adjusted accordingly after the `tidb_server_memory_limit` variable is modified [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the `Can't find column ...` error that might occur when aggregate functions are used for group calculations [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990) <!--tw@hfxsd 以下 8 条-->
    - Fix the issue that the `REVERSE` function reports an error when processing columns of the `BIT` type [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that `INSERT IGNORE` reports an error when inserting data in bulk into a table that has a DDL being executed [#50993](https://github.com/pingcap/tidb/issues/50993) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the TiDB server adds a label via the HTTP interface and returns success, but does not take effect [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - Fix the issue that the type returned by the `IFNULL` function is inconsistent with MySQL [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the TiDB server is marked as health before the initialization is complete [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - Fix the issue that when querying the `TIDB_HOT_REGIONS` table, it returns an in-memory table [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `EXCHANGE PARTITION` incorrectly processes foreign keys [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that executing CTE functions causes TiDB to panic [#41688](https://github.com/pingcap/tidb/issues/41688) @[srstack](https://github.com/srstack)

+ TiKV <!--tw@qiancai 3 条-->

    - 修复 Peer 销毁过程被 apply snapshot 操作中断后，没有在 apply snapshot 完成后继续执行销毁操作的问题 [#16561](https://github.com/tikv/tikv/issues/16561) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复 RocksDB 中非活跃的 WAL (Write Ahead Log) 可能损毁数据的问题 [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.0.0.md > Bug fixes> TiKV - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-8.0.0.md > Bug fixes> TiKV - Fix the issue that JSON integers greater than the maximum `INT64` value but less than the maximum `UINT64` value are parsed as `FLOAT64` by TiKV, resulting in inconsistency with TiDB [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - 修复乐观事务被 resolve lock 时，如果事务的 primary 上之前有通过 Async Commit 或 1PC 模式提交的数据，可能有小概率被破坏事务原子性的问题 [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD <!--tw@Oreoxmt 3 条-->

    - Fix the issue that the scaling progress is not correctly displayed [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that data race occurs when the `MergeLabels` function is called [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the deprecated configuration item `trace-region-flow` is incorrectly displayed when executing `SHOW CONFIG` [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash <!--tw@Oreoxmt 3 条-->

    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might crash due to data race in case of remote reads [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - (dup): release-8.0.0.md > Bug fixes> TiFlash - Fix the issue that the `ENUM` column might cause TiFlash to crash during chunk encoding [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - Fix the issue that TiFlash might panic when creating a column with abnormal default values under non-strict sql_mode [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that if Region migration, split, or merge occurs after the precision of a `TIME` column is modified, queries might fail [#8601](https://github.com/pingcap/tiflash/issues/8601) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt 3 条-->

        - Fix the issue that too many logs are printed when a full backup fails [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that removing a log backup task after it is paused does not immediately restore the GC safepoint [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR could not back up the `AUTO_RANDOM` ID allocation progress in a union clustered index that contains an `AUTO_RANDOM` column [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.0.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@hfxsd 3 条-->

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that `snapshot lost caused by GC` is not reported in time when resuming a changefeed and the `checkpoint-ts` of the changefeed is smaller than the GC safepoint of TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that data race in the KV client causes TiCDC to panic [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC cannot access Azure and GCS properly in storage sink scenarios [#10592](https://github.com/pingcap/tiflow/issues/10592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the old value part of `open-protocol` incorrectly outputs the default value according to the `STRING` type instead of the true type [#10803](https://github.com/pingcap/tiflow/issues/10803) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that a changefeed with eventual consistency enabled might fail when the object store encounters a temporary failure [#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that data is lost when the upstream primary key is of binary type [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning reports an error when encountering invalid symbolic link files during file scanning [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)