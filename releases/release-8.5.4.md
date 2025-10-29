---
title: TiDB 8.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.5.4.
---

# TiDB 8.5.4 Release Notes

Release date: xx xx, 2025

TiDB version: 8.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Compatibility changes

- (dup): release-7.5.7.md > Compatibility changes - TiKV deprecates the following configuration items and replaces them with the new [`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file/#gcauto-compaction) configuration group, which controls automatic compaction behavior [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - Deprecated configuration items: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-interval), [`region-compact-check-step`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-step), [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones), [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent), [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710), and [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710).
    - New configuration items: [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#check-interval-new-in-v757), [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757), [`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757), and [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bottommost-level-force-new-in-v757).

- New system variable: [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl)

## Improvements

+ TiDB <!--tw@Oreoxmt: 11 notes-->

    - (dup): release-9.0.0.md(beta.1) > # SQL 功能 * 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > 改进提升> TiDB - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - 微调了参数 tidb_opt_ordering_index_selectivity_ratio 生效时的估算策略 [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    - 新增配置项 tidb_opt_enable_semi_join_rewrite 去控制 exists 子查询是否需要被改写 [#44850](https://github.com/pingcap/tidb/issues/44850) @[terry1purcell](https://github.com/terry1purcell)
    - 微调了优化器选择逻辑，在某些情况下新索引更容易被选中 [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    - 优化了 NDV 较小的列的查询估算逻辑 [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    - 微调了 limit offset 出现在 Index Join 查询中的估算策略 [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    - 新增 session variable “tidb_opt_enable_no_decorrelate_in_select” 去控制 select list 中的子查询是否需要被解关联  [#51116](https://github.com/pingcap/tidb/issues/51116) @[terry1purcell](https://github.com/terry1purcell)
    - 优化了 Merge join 计算 cost 可能存在遗漏 filter 的情况  [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990)
    - 优化了在统计信息收集不及时情况下，越界估算的策略 [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    - 在执行时间概览中添加 Backoff 时间以便调试 [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    - 在审计日志插件中添加语句 ID 信息 [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)
    - 为审计日志插件添加缓冲日志支持：[#63650](https://github.com/pingcap/tidb/issues/63650) @[bb7133](https://github.com/bb7133)
        - instance.plugin_audit_log_flush_interval：刷新缓冲审计日志的时间间隔
        - instance.plugin_audit_log_buffer_size：插件审计日志的缓冲区大小（字节），默认值为 0（不使用缓冲） 

+ TiKV <!--tw@lilin90: 6 notes-->

    - 将部分 BR 模块的可自动恢复的错误的日志级别从ERROR 调整为 WARN [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    - 将 Raft 模块检查 GC 的流程拆分为两个阶段，提升 Region 冗余 MVCC 版本 GC 的效率。[#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    - 基于 GC safe point 和 Rocksdb 的统计信息计算 MVCC 的冗余读，提升 compaction 的效率和准确性。[#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    - 将部分 TiKV 的错误日志从 ERROR 级别调整为 WARN 级别，避免产生过多不必要的告警。[#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    - 将 Region MVCC 的 GC 处理逻辑改由 GC worker 线程执行，统一 GC 的处理逻辑。 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    - 优化 gRPC 线程池线程数量默认值的计算方式，将原来的固定数据调整为根据总的 CPU 配置动态计算，避免 gRPC 线程数量太小产生的性能瓶颈。 [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.7.md > 改进提升> TiKV - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt: 3 notes-->

    - degrade some unecessary error log [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - upgrade the golang and dependent version[#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - support to distribute table feature, make scatter easier #[8986](https://github.com/tikv/pd/issues/8986)  @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@qiancai: 4 notes-->

    - 跳过不必要读取的数据，优化 TableScan 的读取性能 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 优化 TiFlash 在宽且稀疏的表上 TableScan 的性能 [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化当集群存在大量表时，添加向量索引时的 TiFlash CPU 开销 [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 减少不必要的处理 raft commands 时的日志 [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Data Migration (DM) <!--tw@hfxsd: 1 note-->

        - Support case-insensitive compatibility when retrieving the upstream GTID_MODE [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 14 notes-->

    - 修复当 `tidb_isolation_read_engines` 设置为 "tiflash" 时，`use index` hint 无法生效的问题 [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复了 `max_execution_time` 对 `SELECT FOR UPDATE` 语句不生效的问题. [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.7.md > 错误修复> TiDB - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复预处理语句中处理 decimal 与 mysql 不一致的问题 [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - 修复 `truncate` 函数中短路径处理错误的问题 [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当 `Out Of Quota For Local Temporary Space` 触发时，spill 文件可能未被全部删除的问题 [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复查询`INFORMATION_SCHEMA`表使用正则表达式过滤结果不正确的问题 [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    - 修复从 PD 获取 timestamp 异常时没有返回错误的问题 [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    - 修复modify column时，owner TiDB和非ownerTiDB查询数据不一致的问题 [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    - 修复动态调参后 `ADMIN ALTER DDL JOBS`显示参数不正确的问题 [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    - 修复通过事务加索引时GC savepoint 不推进的问题 [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复过大的 SST 文件 ingest 到 L0 中导致流控的问题 [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复当 CPU 和 memory 比例为 1:2 时阻塞 global sort 的问题 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复超过 16 个 DXF 任务上限时无法 cancel pending 任务的问题 [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    - 修复cancel DXF任务后，其他任务无法退出的问题 [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter) <!--tw@hfxsd: the following 14 notes-->
    - Fix the issue that enabling the `Apply` operator concurrency (`tidb_enable_parallel_apply = on`) causes plan generation failure due to a missing clone implementation [#59863](https://github.com/pingcap/tidb/issues/59863) @[hawkingrei](https://github.com/hawkingrei)    
    - Fix the issue that using the `ATAN2` function might produce incorrect results [#60093](https://github.com/pingcap/tidb/issues/60093) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that `select 1 from duml` cannot use the instance-level plan cache [#63075](https://github.com/pingcap/tidb/issues/63075) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that changing the join order sequence might cause the planner to fail [#61715](https://github.com/pingcap/tidb/issues/61715) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using `set_var` hint with bindings prevents restoring the original variable settings [#59822](https://github.com/pingcap/tidb/issues/59822) @[wddevries](https://github.com/wddevries)
    - Fix the issue that setting `ONLY_FULL_GROUP_BY` to a negative value causes validation failure [#62617](https://github.com/pingcap/tidb/issues/62617) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `ONLY_FULL_GROUP_BY` check is case-insensitive [#62672](https://github.com/pingcap/tidb/issues/62672) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the DP join order algorithm might generate an incorrect plan [#63353](https://github.com/pingcap/tidb/issues/63353) @[winoros](https://github.com/winoros)
    - Fix the issue that rewriting an outer join to an inner join might produce incorrect results [#61327](https://github.com/pingcap/tidb/issues/61327) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that query execution might trigger an internal panic [#58600](https://github.com/pingcap/tidb/issues/58600) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the global index might read incorrect data during certain `ALTER PARTITION` states [#64084](https://github.com/pingcap/tidb/pull/64084) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the global index might return incorrect results in some cases [#61083](https://github.com/pingcap/tidb/issues/61083) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `character_set_results` truncates incorrect characters instead of replacing them [#61085](https://github.com/pingcap/tidb/issues/61085) @[xhebox](https://github.com/xhebox)
    - Fix the issue that running `ADD COLUMN` and `UPDATE` statements concurrently might cause errors [#60047](https://github.com/pingcap/tidb/issues/60047) @[L-maple](https://github.com/L-maple)

+ PD <!--tw@qiancai: 8 notes-->

    - Fix PD Client initial strategy not work well [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - Fix the wrong APIS of the `/config` 和 `/members`  [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024) 
    - Fix the handler way of the tso error #[9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - Fix the bucket split still work even if the bucket doesn't report #[9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - Fix the wrong token allocation of the resource manager #[9455](https://github.com/tikv/pd/issues/9455)  @[JmPotato](https://github.com/JmPotato)
    - Fix the placement rule revert after pd leader changed #[9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - 修复 backoff 初始化错误问题 #[9013](https://github.com/tikv/pd/issues/9013)  @[rleungx](https://github.com/rleungx)
    - Fix the ttl configuration not work #[9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 notes-->

    - Fix the issue that queries might fail when the queried column contains a large number of NULL values [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash generates inaccurate statistics for RU consumption [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might encounter OOM when slow queries occur under the disaggregated storage and compute architecture [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might retry infinitely when it encounters an S3 network partition under the disaggregated storage and compute architecture [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the `FLOOR()` and `CEIL()` functions might return incorrect results when their parameters are of the `DECIMAL` type [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) 

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 notes-->

        - Fix the issue where Zstd compression did not take effect in log backup, resulting in uncompressed output. [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - Fixed a bug that may cause flush operation slow in azure blob storage. [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `log truncate` panic when failed to delete file. [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `stats_meta` be zero when checksumming disabled. [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - Reduced chance of BR restore failure from S3-compatible storage when the S3 server limits bandwidth through traffic shaping. [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the log backup observer loses observation of a region. [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - Fixed a a bug that may cause `restore point` fail when there are some special sized table schemas.   [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@Oreoxmt: 7 notes-->

        - Fix the issue that configuring the column dispatcher with virtual columns might cause a panic. [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - Fix the issue that closing ddl puller might cause a panic. [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - Support discarding unsupported DDL by setting `ignore-txn-start-ts` in filter. [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that using Azure Downstream might cause stuck. [#12277] (https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - Fix the issue that `drop foreign key` is not replicated to downstream [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the panic issue when subscribe the region and meet rollback and prewrite entry [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix a TiKV assertion panic [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)