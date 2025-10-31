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

- Add the `tidb_opt_enable_no_decorrelate_in_select` system variable to control whether to decorrelate subqueries in the `SELECT` list [#51116](https://github.com/pingcap/tidb/issues/51116) @[terry1purcell](https://github.com/terry1purcell) <!--tw@Oreoxmt -->

- Add the `tidb_opt_enable_semi_join_rewrite` system variable to control whether to rewrite `EXISTS` subqueries [#44850](https://github.com/pingcap/tidb/issues/44850) @[terry1purcell](https://github.com/terry1purcell) <!--tw@Oreoxmt -->

## Improvements

+ TiDB <!--tw@Oreoxmt: 11 notes-->

    - (dup): release-9.0.0.md(beta.1) > # SQL 功能 * 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > 改进提升> TiDB - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    - Optimize the estimation strategy when the `tidb_opt_ordering_index_selectivity_ratio` system variable takes effect [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    - Adjust the optimizer selection logic to make newly created indexes more likely to be chosen in certain scenarios [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    - Optimize the query estimation logic for columns with a small NDV (number of distinct values) [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    - Optimize the estimation strategy for Index Join queries that include `LIMIT OFFSET` [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    - Optimize the scenario where Merge Join might miss filter conditions when calculating costs [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990)
    - Optimize the out-of-range estimation strategy when statistics are not collected in time [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    - Add the backoff time metric to the execution time overview to facilitate debugging [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    - Add statement ID information to the audit log plugin [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)

+ TiKV <!--tw@lilin90: 6 notes-->

    - Change the log level of certain automatically recoverable errors in the BR module from `ERROR` to `WARN` to reduce unnecessary alerts [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    - Change the log level of certain TiKV error messages from `ERROR` to `WARN` to reduce unnecessary alerts [#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    - Split the GC check process in the Raft module into two phases to improve the efficiency of redundant MVCC version GC in Regions [#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    - Calculate redundant MVCC reads based on GC safe points and RocksDB statistics to improve the efficiency and accuracy of compaction [#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    - Change the GC handling logic for Region MVCC to be executed by GC worker threads to make the GC processing workflow consistent [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    - Optimize the calculation of the default gRPC thread pool size by making it dynamically based on total CPU cores instead of a fixed value, preventing performance bottlenecks caused by insufficient gRPC threads [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.5.7.md > 改进提升> TiKV - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD <!--tw@Oreoxmt: 3 notes-->

    - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - Upgrade the Golang version to 1.23.12 and update related dependencies [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - Support scattering Regions at the table level to achieve balanced distribution across `scatter-role` and `engine` dimensions [#8986](https://github.com/tikv/pd/issues/8986) @[bufferflies](https://github.com/bufferflies)

+ TiFlash <!--tw@qiancai: 4 notes-->

    - Skip unnecessary data reads to improve `TableScan` performance [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - Optimize `TableScan` performance on wide tables with many columns and sparse data (that is, lots of `NULL` or empty values) in TiFlash [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Reduce TiFlash CPU overhead caused by adding vector indexes in clusters with many tables [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Minimize unnecessary log output when processing useless Raft commands to reduce log volume [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Improve `TableScan` performance on small partitioned tables in TiFlash [#10487](https://github.com/pingcap/tiflash/issues/10487) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Data Migration (DM) <!--tw@hfxsd: 1 note-->

        - Support case-insensitive compatibility when retrieving the upstream GTID_MODE [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 14 notes-->

    - Fix the issue that the `use index` hint does not take effect when `tidb_isolation_read_engines` is set to `tiflash` [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that `max_execution_time` does not take effect for `SELECT FOR UPDATE` statements [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.7.md > 错误修复> TiDB - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - Fix the issue that the handling of `Decimal` types in prepared statements is inconsistent with MySQL [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - Fix the issue that the short path in the `TRUNCATE()` function is incorrectly processed [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that spilled files are not deleted when `Out Of Quota For Local Temporary Space` is triggered [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that queries using regular expressions on `INFORMATION_SCHEMA` tables might return incorrect results [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    - Fix the issue that TiDB does not return an error when it fails to get a timestamp from PD [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that query results differ between the owner TiDB and non-owner TiDB instances during executing `MODIFY COLUMN` statements [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `ADMIN ALTER DDL JOBS` statement displays incorrect parameters after dynamically changing the parameters [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that the GC safe point does not advance when adding an index within a transaction [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that ingesting large SST files into L0 triggers flow control [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that global sorting is blocked when the CPU-to-memory ratio is 1:2 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that pending Distributed eXecution Framework (DXF) tasks cannot be canceled when the number of tasks exceeds 16 [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that after the DXF task is canceled, other tasks fail to exit [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter) <!--tw@hfxsd: the following 14 notes-->
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

    - Fix the issue that the PD Client retry strategy is not initialized correctly [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the TSO HTTP API `/config` and `/members` return incorrect output [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024)
    - Fix the incorrect error handling logic of TSO Follower Proxy [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - Fix the issue that splitting buckets still works even after bucket reporting is disabled [#9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that the Resource Manager incorrectly allocates tokens, causing queries to be stuck [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that Placement Rules do not take effect after PD leader switches [#9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - Fix the issue that TTL configuration does not take effect [#9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash <!--tw@hfxsd: 5 notes-->

    - Fix the issue that queries might fail when the queried column contains a large number of NULL values [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash generates inaccurate statistics for RU consumption [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash might encounter OOM when slow queries occur under the disaggregated storage and compute architecture [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might retry infinitely when it encounters an S3 network partition under the disaggregated storage and compute architecture [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the `FLOOR()` and `CEIL()` functions might return incorrect results when their parameters are of the `DECIMAL` type [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) 

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 7 notes-->

        - Fix the issue that zstd compression in log backup does not take effect, causing the output to remain uncompressed [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - Fix the issue that flushing might slow down when backing up data to Azure Blob Storage [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that `log truncate` might occur when file deletion fails [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that setting `--checksum` to `false` during backup might result in an empty `stats_meta` table [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - Reduce the possibility of BR failing to restore data from S3-compatible storage services when the bandwidth limits on these services are enabled [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - Fix the issue that `log backup observer` might lose the observation on a Region, resulting in incomplete backup data [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that causes `restore point` creation to fail when backed-up tables includes certain special schemas [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw@Oreoxmt: 7 notes-->

        - Fix a panic that could occur when configuring a Column-type partition dispatcher that includes virtual columns [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - Fix a panic that could occur when closing the DDL puller [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - Support filtering unsupported DDL types through the `ignore-txn-start-ts` parameter in the `filter` configuration [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that Changefeed tasks might get stuck when using Azure Blob Storage as the downstream [#12277](https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - Fix the issue that `DROP FOREIGN KEY` DDL is not replicated to the downstream [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might panic when encountering rollback and prewrite entries during Region subscription [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that assertion errors in TiKV might cause TiCDC to panic [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
