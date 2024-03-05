---
title: TiDB 7.1.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.4.
---

# TiDB 7.1.4 Release Notes

Release date: March xx, 2024

TiDB version: 7.1.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.4#version-list)

## Compatibility changes <!--tw@qiancai 1 条 -->

- 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)
- (dup): release-6.5.8.md > 兼容性变更 - 新增 TiKV 配置项 [`gc.num-threads`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#num-threads-从-v658-版本开始引入)，用于设置当 `enable-compaction-filter` 为 `false` 时 GC 的线程个数 [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

## Improvements

+ TiDB <!--tw@Oreoxmt 1 条 -->

    - (dup): release-7.5.1.md > Improvements> TiDB - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - When `force-init-stats` is set to `true`, TiDB waits for statistics initialization to finish before providing services during TiDB startup. During this period, TiDB also blocks the startup of HTTP servers [#50854](https://github.com/pingcap/tidb/issues/50854) @[hawkingrei](https://github.com/hawkingrei)

+ PD

    - (dup): release-7.4.0.md > Improvements> PD - Improve the speed of PD automatically updating cluster status when the backup cluster is disconnected [#6883](https://github.com/tikv/pd/issues/6883) @[disksing](https://github.com/disksing)

+ TiFlash

    - (dup): release-7.5.1.md > Improvements> TiFlash - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > Improvements> TiFlash - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR) <!--tw@Oreoxmt 2 条 -->

        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Support creating databases in batch during data restore [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Improve the speed of merging SST files during data restore by using a more efficient algorithm [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.7.md > Improvements> Tools> Backup & Restore (BR) - Resolve compatibility issues between EBS-based snapshot backups and TiDB Lightning imports [#46850](https://github.com/pingcap/tidb/issues/46850) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Support ingesting SST files in batch during data restore [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.5.1.md > Improvements> Tools> Backup & Restore (BR) - Print the information of the slowest Region that affects global checkpoint advancement in logs and metrics during log backups [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - Remove an outdated compatibility check when using Google Cloud Storage (GCS) as the external storage [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)
        - Implement a lock mechanism to prevent executing multiple log backup truncation tasks (`br log truncate`) simultaneously [#49414](https://github.com/pingcap/tidb/issues/49414) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - (dup): release-6.5.7.md > Improvements> Tools> TiCDC - When the downstream is Kafka, the topic expression allows `schema` to be optional and supports specifying a topic name directly [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.5.1.md > Improvements> Tools> TiCDC - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/tidb/v7.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - (dup): release-7.5.1.md > Improvements> Tools> TiCDC - Support searching TiCDC logs in the TiDB Dashboard [#10263](https://github.com/pingcap/tiflow/issues/10263) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning <!--tw@Oreoxmt 1 条 -->

        - Improve the performance in scenarios where multiple tables are imported by canceling the lock operation when executing `ALTER TABLE` [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that errors might be returned during the concurrent merging of global statistics for partitioned tables [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue of wrong query results due to TiDB incorrectly eliminating constant values in `group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that `BIT` type columns might cause query errors due to decode failures when they are involved in calculations of some functions [#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that `LIMIT` in multi-level nested `UNION` queries might become ineffective [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the `Column ... in from clause is ambiguous` error that might occur when a query uses `NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the goroutine leak issue that might occur when the `HashJoin` operator fails to spill to disk [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that executing queries containing the `GROUP_CONCAT(ORDER BY)` syntax might return errors [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that using a multi-valued index to access an empty JSON array might return incorrect results [#50125](https://github.com/pingcap/tidb/issues/50125) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the goroutine leak issue that occurs when the memory usage of CTE queries exceed limits [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that using old interfaces might cause inconsistent metadata for tables [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the `Can't find column ...` error that might occur when aggregate functions are used for group calculations [#50926](https://github.com/pingcap/tidb/issues/50926) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the completion times of two DDL tasks with dependencies are incorrectly sequenced [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that TiDB might panic when using the `EXECUTE` statement to execute `PREPARE STMT` after the `tidb_enable_prepared_plan_cache` system variable is enabled and then disabled [#49344](https://github.com/pingcap/tidb/issues/49344) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that the `COMMIT` or `ROLLBACK` operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timed out [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that illegal optimizer hints might cause valid hints to be ineffective [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.5.1.md > Bug fixes> TiDB - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method incorrectly returns a success message instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990) <!--tw@Oreoxmt 以下 7 条 -->
    - Fix the issue that TiDB might panic when performing a rolling upgrade using `tiup cluster upgrade/start` due to an interaction issue with PD [#50152](https://github.com/pingcap/tidb/issues/50152) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the expected optimization does not take effect when adding an index to an empty table [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - Fix the issue that TiDB might OOM when a large number of tables or partitions are created [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that adding an index might cause inconsistent index data when the network is unstable [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - Fix the execution order of DDL jobs to prevent TiCDC from receiving out-of-order DDLs [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - Fix the issue encountered when using `REVERSE()` on `BIT` type columns [#50850](https://github.com/pingcap/tidb/issues/50850) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the `tidb_gogc_tuner_threshold` system variable is not adjusted accordingly after modifying the `tidb_server_memory_limit` variable [#48180](https://github.com/pingcap/tidb/issues/48180) @[hawkingrei](https://github.com/hawkingrei) <!--tw@qiancai 以下 7 条 -->
    - 修复分区表进行 range 分区裁剪处理 unsigned 类型的列时的一处 bug，该 bug 会生成错误的 TableDual 的查询计划导致查询结果错误 [#50082](https://github.com/pingcap/tidb/issues/50082) @[Defined2014]
    - 修复部分 partition 或者约束的表达式会导致 DDL 卡住的问题 [#50972](https://github.com/pingcap/tidb/issues/50972) @[lcwangchao](https://github.com/lcwangchao)
    - 修复默认值被删除的列获取默认值报错的问题 [#51309](https://github.com/pingcap/tidb/issues/51309) @[crazycs520](https://github.com/crazycs520)
    - 修复 grafana 监控指标 tidb_statistics_auto_analyze_total 不为整数的问题。[#51051](https://github.com/pingcap/tidb/issues/51051) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 auto analyze 在处理分区表时，并发不可用的问题。[#47594](https://github.com/pingcap/tidb/issues/47594) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 join 中可能出现的 index out of range 问题。 [#42588](https://github.com/pingcap/tidb/issues/42588) @[AilinKid](https://github.com/AilinKid)
    - 修复在 TiFlash 延迟物化在处理关联列时结果可能出错的问题 [#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV <!--tw@qiancai 6 条 -->

    - raftstore: 修复休眠region在异常情况下不能及时唤醒的缺陷。[#16368](https://github.com/tikv/tikv/issues/16368) @[LykxSassinator](https://github.com/LykxSassinator)
    - 在执行下线节点操作前，检查该region所有副本的上一次心跳时间，防止下线一个副本后整个region不可用. [#16465](https://github.com/tikv/tikv/issues/16465) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - 修复Titan打开时RocksDB中Table property相关的缺陷。 [#16319](https://github.com/tikv/tikv/issues/16319) @[hicqu](https://github.com/hicqu)
    - 修复当TiFlash打开时tikv-ctl compact-cluster无法工作的缺陷。[#16189](https://github.com/tikv/tikv/issues/16189) @[frew](https://github.com/frew)
    - RocksDB: 记录SST损坏的具体原因。[#16308](https://github.com/tikv/tikv/issues/16308) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that `cast_duration_as_time` might return incorrect results [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.1.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - 修复 JSON 整形数值在大于 int64 最大值但是小于 uint64 最大值时会被解析成 float64 导致结果和 TiDB 不一致的问题 [#16537](https://github.com/tikv/tikv/pull/16537) @[YangKeao](https://github.com/YangKeao)

+ PD <!--tw@hfxsd 7 条 -->

    - 修复 Resource Group 客户端中未删除完全的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 TSO 部分日志没有打印 error 原因的问题 [#7496](https://github.com/tikv/pd/issues/7496) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 Default Resource Group 在 burstable 时累计不必要 tokens 的问题 [#7206](https://github.com/tikv/pd/issues/7206) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复调用 evict-leader 接口时没有输出结果的问题 [#7672](https://github.com/tikv/pd/issues/7672) @[CabinfeverB](https://github.com/CabinfeverB)
    - 修复 watch etcd 没有正确关闭导致内存泄露的问题 [#7807](https://github.com/tikv/pd/issues/7807) @[rleungx](https://github.com/rleungx)
    - 修复 MergeLabels 时存在 datarace 的问题 [#7535](https://github.com/tikv/pd/issues/7535) @[lhy1024](https://github.com/lhy1024)
    - 修复 Dashboard 中在开启 tls 时 tikv profile 获取失败的问题 [#7561](https://github.com/tikv/pd/issues/7561) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that `available_stores` is calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.0.md > Bug fixes> PD - Fix the issue that `canSync` and `hasMajority` might be calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode when the configuration of Placement Rules is complex [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - (dup): release-6.5.6.md > Bug fixes> PD - Fix the issue that the primary AZ cannot add TiKV nodes when the secondary AZ is down for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that querying resource groups in batch might cause PD to panic [#7206](https://github.com/tikv/pd/issues/7206) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that querying a Region without a leader using `pd-ctl` might cause PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that the PD monitoring item `learner-peer-count` does not synchronize the old value after a leader switch [#7728](https://github.com/tikv/pd/issues/7728) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.5.1.md > Bug fixes> PD - Fix the issue that PD cannot read resource limitations when it is started with `systemd` [#7628](https://github.com/tikv/pd/issues/7628) @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@hfxsd 2 条 -->

    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic due to unstable network connections with PD during replica migration [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash incorrectly handles `ENUM` when the `ENUM` value is 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the random invalid memory access issue that might occur with `GREATEST` or `LEAST` functions containing constant string parameters [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that short queries executed successfully print excessive info logs [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.8.md > Bug fixes> TiFlash - Fix the issue that after terminating a query, TiFlash crashes due to concurrent data conflicts when a large number of tasks on TiFlash are canceled at the same time [#7432](https://github.com/pingcap/tiflash/issues/7432) @[SeaRise](https://github.com/SeaRise)
    - 修复 TiFlash 在有大量远程读时，由于并发数据冲突导致 TiFlash 崩溃的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[zanmato1984](https://github.com/zanmato1984)
    - 修复 anti semi join 在有其他不等值连接条件时，结果可能会出错的问题 [#8791](https://github.com/pingcap/tiflash/issues/8791) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that stopping a log backup task causes TiDB to crash [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that data restore is slowed down due to absence of a leader on a TiKV node [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.1.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)

    + TiCDC <!--tw@hfxsd 2 条 -->

        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the Syncpoint table might be incorrectly replicated [#10576](https://github.com/pingcap/tiflow/issues/10576) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that the file sequence number generated by the storage service might not increment correctly when using the storage sink [#10352](https://github.com/pingcap/tiflow/issues/10352) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在 resume changefeed 的时候由于没有检查 changefeed 的 checkpoint-ts 是否小于 TiDB 的 gc safepoint 从而没有及时把 "snapshot lost cased by GC" 错误提示出来 [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - 修复 TiCDC 在开启单行数据正确性校验 (Data Integrity Validation for Single-Row Data) 后由于没有正确考虑时区的问题导致 timestamp 类型 checksum 验证失败的问题 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM) <!--tw@hfxsd 2 条 -->

        - 修复任务配置中错误的 binlog 事件类型导致升级失败的问题 [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复带有 shard_row_id_bits 的表会导致 schema tracker 无法初始化的问题 [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning <!--tw@Oreoxmt 2 条 -->

        - Fix the issue that TiDB Lightning reports an error when encountering invalid symbolic link files during file scanning [#49423](https://github.com/pingcap/tidb/issues/49423) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning fails to correctly parse date values containing `0` when `NO_ZERO_IN_DATE` is not included in `sql_mode` [#50757](https://github.com/pingcap/tidb/issues/50757) @[GMHDBJD](https://github.com/GMHDBJD)
