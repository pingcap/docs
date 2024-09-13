---
title: TiDB 6.5.11 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.11.
---

# TiDB 6.5.11 Release Notes

Release date: xx xx, 2024

TiDB version: 6.5.11

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB

    - (dup): release-8.1.1.md > Improvements> TiDB - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing the `TRUNCATE` or `DROP` operation on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV <!--tw@Oreoxmt: 1 note-->

    - 改进在大量 DELETE 版本存在时的 RocksDB 的 compaction 触发机制，以更快地回收磁盘空间 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)

+ TiFlash <!--tw@qiancai: 1 note-->

    - (dup): release-8.1.1.md > Improvements> TiFlash - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - 优化 `length` 和 `ascii` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + TiCDC <!--tw@hfxsd: 1 note-->

        - 当下游为 TiDB 且授予 Super 权限时，TiCDC 支持从下游数据库查询 ADD INDEX DDL 的执行状态，以避免某些情况下因重试执行 DDL 超时而导致的同步失败。 [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB

    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that the recursive CTE operator incorrectly tracks memory usage [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.3.0.md > Bug fixes> TiDB - Reset the parameters in the `Open` method of `PipelinedWindow` to fix the unexpected error that occurs when the `PipelinedWindow` is used as a child node of `Apply` due to the reuse of previous parameter values caused by repeated opening and closing operations [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that the memory used by transactions might be tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue of abnormally high memory usage caused by `memTracker` not being detached when the `HashJoin` or `IndexLookUp` operator is the driven side sub-node of the `Apply` operator [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that `INDEX_HASH_JOIN` cannot exit properly when SQL is abnormally interrupted [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-8.3.0.md > Bug fixes> TiDB - Fix the issue that table replication fails when the index length of the table replicated from DM exceeds the maximum length specified by `max-index-length` [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that indirect placeholder `?` references in a `GROUP BY` statement cannot find columns [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.3.0.md > Bug fixes> TiDB - Fix the issue that predicates cannot be pushed down properly when the filter condition of a SQL query contains virtual columns and the execution condition contains `UnionScan` [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue of reusing wrong point get plans for `SELECT ... FOR UPDATE` [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that RANGE partitioned tables that are not strictly self-incrementing can be created [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that the network partition during adding indexes using the Distributed eXecution Framework (DXF) might cause inconsistent data indexes [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.3.0.md > Bug fixes> TiDB - Fix the issue that the query might get stuck when terminated because the memory usage exceeds the limit set by `tidb_mem_quota_query` [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.3.0.md > Bug fixes> TiDB - Fix the issue that the `tot_col_size` column in the `mysql.stats_histograms` table might be a negative number [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.1.md > Bug fixes> TiDB - Fix the issue that obtaining the column information using `information_schema.columns` returns warning 1356 when a subquery is used as a column definition in a view definition [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复 TiDB 关闭连接时，在某些情况下会在日志中报错的问题 [#53689](https://github.com/pingcap/tidb/issues/53689) @[jackysp](https://github.com/jackysp)
    - 修复 `SELECT ... WHERE ... ORDER BY ...` 语句在某些情况下执行效率低的性能问题 [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `information_schema`.`statistics` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复 query 被 kill 之后有概率返回错误结果而非报错的问题 [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - 修复查询 information_schema.CLUSTER_SLOW_QUERY 可能导致 TiDB panic 的问题 [#54324](https://github.com/pingcap/tidb/issues/54324) @[tiancaiamao](https://github.com/tiancaiamao) <!--tw@hfxsd: the following 5 notes-->
    - 修复 `StreamAggExec` 中可能会 panic 报错的问题 [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `sort` 算子发生 spill 且 query 出错后，磁盘文件可能没被删除的问题 [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 `IndexNestedLoopHashJoin` 中存在 data race 的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复使用 `SHOW COLUMNS` 查看视图中的列时报错的问题 [#54964](https://github.com/pingcap/tidb/issues/54964) @[lance6716](https://github.com/lance6716)
    - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV <!--tw@Oreoxmt: 3 notes-->

    - 修复在主密钥存储于 KMS 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - 修复因导入已被删除的 sst_importer SST 文件而导致的 TiKV panic 问题 [#15053](https://github.com/tikv/tikv/issues/15053) @[lance6716](https://github.com/lance6716)
    - (dup): release-8.1.1.md > Bug fixes> TiKV - Fix the issue that TiKV might repeatedly panic when applying a corrupted Raft data snapshot [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.1.md > Bug fixes> TiKV - Fix the issue that setting the gRPC message compression method via `grpc-compression-type` does not take effect on messages sent from TiKV to TiDB [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.1.1.md > Bug fixes> TiKV - Fix the issue that CDC and log-backup do not limit the timeout of `check_leader` using the `advance-ts-interval` configuration, causing the `resolved_ts` lag to be too large when TiKV restarts normally in some cases [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - (dup): release-8.1.1.md > Bug fixes> PD - Fix the issue that some logs are not redacted [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.1.1.md > Bug fixes> PD - Fix the issue that setting the TiKV configuration item [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) to a value less than 1 MiB causes PD panic [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-8.3.0.md > Bug fixes> PD - Fix the issue that setting `replication.strictly-match-label` to `true` causes TiFlash to fail to start [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.1.1.md > Bug fixes> PD - Fix the data race issue that PD encounters during operator checks [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@qiancai: 3 notes-->

    - (dup): release-8.3.0.md > Bug fixes> TiFlash - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - (dup): release-8.1.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when a database is deleted shortly after creation [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.1.md > Bug fixes> TiFlash - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.1.md > Bug fixes> TiFlash - Fix the issue that a network partition (network disconnection) between TiFlash and any PD might cause read request timeout errors [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 带有 outer join 的 query 出错时有概率导致 TiFlash crash 的问题 [#9190](https://github.com/pingcap/tiflash/issues/9190) @[windtalker](https://github.com/windtalker)
    - 修复在一些 corner case 下面，cast to decimal 结果可能出错的问题 [#53892](https://github.com/pingcap/tidb/issues/53892) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当集群中长时间存在对表连续执行 EXCHANGE PARTITION 变更及 DROP TABLE 变更时，可能导致 TiFlash 表元信息数据同步以及查询变慢的问题 [#9227](https://github.com/pingcap/tiflash/issues/9227) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt: 3 notes-->

        - (dup): release-8.3.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the checkpoint path of backup and restore is incompatible with some external storage [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - (dup): release-8.1.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - 在注销日志备份任务时，清理该 TiKV 节点上的 `pause-guard-gc-safepoint` [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - 修复备份过程中因为 TiKV 没有响应导致作业无法结束的问题[#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - 避免在 BR 日志中打印 AK/SK  [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@hfxsd: 1 note-->

        - 修复 Sorter 模块读取磁盘数据时可能 Panic 的问题 [#10853](https://github.com/pingcap/tiflow/issues/10853) @[hicqu](https://github.com/hicqu)
        - (dup): release-8.1.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the Processor module might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM) <!--tw@qiancai: 2 notes-->

        - (dup): release-8.1.1.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that data replication is interrupted when the index length exceeds the default value of `max-index-length` [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - (dup): release-8.1.1.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that schema tracker incorrectly handles LIST partition tables, causing DM errors [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - 修复 DM 在同步删除 LIST 分区表中的分区的 DDL 语句时报错的问题 [#54760](https://github.com/pingcap/tidb/issues/54760) @[lance6716](https://github.com/lance6716)
        - 修复 DM 在 `ALTER DATABASE` 中未正常设置默认数据库的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning <!--tw@lilin90: 2 notes-->

        - (dup): release-8.3.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that transaction conflicts occur during data import using TiDB Lightning [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - 修复使用 `IMPORT INTO` 语句导入时删除 sst 文件导致的 TiKV panic 的问题 [#15003](https://github.com/tikv/tikv/issues/15003) [#47694](https://github.com/pingcap/tidb/issues/47694) @[lance6716](https://github.com/lance6716)
        - 修复使用 TiDB Lightning 导入时 TiKV 重启报错的问题 [#15912](https://github.com/tikv/tikv/issues/15912) @[lance6716](https://github.com/lance6716)