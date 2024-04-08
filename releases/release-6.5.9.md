---
title: TiDB 6.5.9 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.9.
---

# TiDB 6.5.9 Release Notes

Release date: February 2, 2024

TiDB version: 6.5.9

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.9#version-list)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB <!--tw@hfxsd 1 条-->

    - (dup): release-8.0.0.md > Improvements> TiDB - When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. This setting no longer blocks the startup of HTTP servers, which enables users to continue monitoring [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)
    - 优化了 Analyze 语句卡住 Metadata Lock 的问题 [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV <!--tw@qiancai TBD 条-->

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.0.0.md > Improvements> TiKV - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@qiancai 1 条-->

    - DR Auto-Sync 支持设置 `wait-recover-timeout` [#6295](https://github.com/tikv/pd/issues/6295) @[disksing](https://github.com/disksing)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt 3 条-->

        - 优化了在滚动重启场景 Log Backup 的备份时间点目标（RPO），现在滚动重启时 Log Backup Task 会有更小的 Checkpoint Lag。 [#15410](https://github.com/tikv/tikv/issues/15410) @[YuJuncen](https://github.com/YuJuncen)
        - 优化了 Log Backup 对 Merge 的容忍度，现在在遇到合理的长时间 Merge 的时候 Log Backup Task 不容易进入 Error 状态。[#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - 新增了 Log Backup 在遇到较大的 Checkpoint Lag 的时候自动放弃任务的功能，这样可以防止 Log Backup 意外长时间阻塞 GC 导致集群出现问题。[#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-7.4.0.md > Improvements> Tools> Backup & Restore (BR) - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Support ingesting SST files in batch during data restore [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.1.4.md > Improvements> Tools> Backup & Restore (BR) - Remove an outdated compatibility check when using Google Cloud Storage (GCS) as the external storage [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Refactor the BR exception handling mechanism to increase tolerance for unknown errors [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

## Bug fixes

+ TiDB <!--tw@qiancai 以下 6 条-->

    - 修复大量创建表时，新表可能缺失 stats_meta 信息导致后续估算无法获取准确行数信息的问题 [#36004](https://github.com/pingcap/tidb/issues/36004) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复已经 drop 的表依然会被计入 Grafana 的 Stats Healthy Distribution 面板的问题 [#39349](https://github.com/pingcap/tidb/issues/39349) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复涉及 `MemTableScan` 算子的查询丢失 SQL 中形如 `WHERE column_name` 的过滤条件的问题 [#40937](https://github.com/pingcap/tidb/issues/40937) @[zhongzc](https://github.com/zhongzc)
    - 修复子查询中的 `HAVING` 子句包含关联列时查询结果可能错误的问题 [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在 CTE 中访问分区表，且该分区表缺少统计信息时，查询结果可能错误的问题 [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - 修复当 SQL 中包含 `JOIN` 且 `SELECT` 列表只包含常量，且使用 MPP 执行时，查询结果可能错误的问题 [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
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
    - 修复 `reverse` 函数在处理 `bit` 类型列时报错的问题 [#50850](https://github.com/pingcap/tidb/issues/50850), [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 `insert ignore` 向正在执行 ddl 的表中批量插入时报错的问题 [#50993](https://github.com/pingcap/tidb/issues/50993) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 通过 HTTP 接口添加 label 返回成功但不生效的问题 [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - 修复 `ifnull` 函数返回的类型和 MySQL 不一致的问题 [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB Server 在初始化完成之前就标记为 Health 的问题 [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - 修复查询 `TIDB_HOT_REGIONS` 表结果会返回内存表的问题 [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - 修复 `exchange partition` 在处理外键时判断错误的问题 [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - 修复执行 CTE 函数会 panic 的问题 [#41688](https://github.com/pingcap/tidb/issues/41688) @[srstack](https://github.com/srstack)

+ TiKV <!--tw@qiancai 1 + TBD 条-->

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.0.0.md > Bug fixes> TiKV - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-8.0.0.md > Bug fixes> TiKV - Fix the issue that JSON integers greater than the maximum `INT64` value but less than the maximum `UINT64` value are parsed as `FLOAT64` by TiKV, resulting in inconsistency with TiDB [#16512](https://github.com/tikv/tikv/issues/16512) @[YangKeao](https://github.com/YangKeao)
    - 修复乐观事务被 resolve lock 时，如果事务的 primary 上之前有通过 Async Commit 或 1PC 模式提交的数据，可能有小概率被破坏事务原子性的问题 [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD <!--tw@Oreoxmt 3 条-->

    - 修复扩缩容进度展示不准确的问题 [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复调用 `MergeLabels` 函数时存在数据竞争的问题 [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复执行 SQL `show config` 时错误显示 `trace-region-flow` 的问题 [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash <!--tw@Oreoxmt 3 条-->

    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 发生远程读时可能会 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[solotzg](https://github.com/solotzg)
    - (dup): release-8.0.0.md > Bug fixes> TiFlash - Fix the issue that the `ENUM` column might cause TiFlash to crash during chunk encoding [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - 修复在非严格 sql_mode 下创建带异常默认值的列可能导致 TiFlash panic 的问题 [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在 `TIME` 类型的列精度修改之后，当 Region 迁移、分裂或者合并后，可能导致查询出错的问题 [#8601](https://github.com/pingcap/tiflash/issues/8601) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt 3 条-->

        - 修复了使用 Coarse-grained Split Region 策略 Restore 失败时日志太过繁冗的问题。 [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - 修复了在 Log Backup Task 被暂停之后，移除 Task 不能马上恢复 GC Safepoint 的问题。 [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - 修复了在联合聚簇索引中包含 AUTO_RANDOM 列的时候，BR 不会备份 AUTO_RANDOM ID 分配进度的问题。[#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.0.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)

    + TiCDC <!--tw@hfxsd 3 条-->

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that `snapshot lost caused by GC` is not reported in time when resuming a changefeed and the `checkpoint-ts` of the changefeed is smaller than the GC safepoint of TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.0.0.md > Bug fixes> Tools> TiCDC - Fix the issue that data race in the KV client causes TiCDC to panic [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 storage sink 场景下无法正常访问 azure 和 gcs 对象存储的问题 [#10592](https://github.com/pingcap/tiflow/issues/10592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 open-protocol 的 old value 部分错误的按照 string 类型而非真正类型输出默认值的问题 [#10803](https://github.com/pingcap/tiflow/issues/10803)，@[3AceShowHand](https://github.com/3AceShowHand)
        - 修复了当对象存储遇到暂时故障时，启用了最终一致性功能的 changefeed 可能直接失败的问题，[#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that data is lost when the upstream primary key is of binary type [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - (dup): release-8.0.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning reports an error when encountering invalid symbolic link files during file scanning [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)