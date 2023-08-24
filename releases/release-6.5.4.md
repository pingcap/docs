---
title: TiDB 6.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.4.
---

# TiDB 6.5.4 Release Notes

Release date: xxxx, 2023

TiDB version: 6.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.4#version-list)

## Improvements

+ TiDB <!-- tw: Oreoxmt 1-->

    - Optimize the performance of `LOAD DATA` statements that contain assignment expressions [#46081](https://github.com/pingcap/tidb/issues/46081) @[gengliqi](https://github.com/gengliqi)
    - (dup): Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)

+ TiKV <!-- tw: Oreoxmt 9-->

    - (dup): Use gzip compression for `check_leader` requests to reduce traffic [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - (dup): Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get_region_read_progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    <!-- tw: ran-huang 1-->
    - Expose some RocksDB configurations in TiKV that allow users to disable features such as TTL and periodic compaction [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!-- tw: ran-huang 5-->

    (dup)- Support blocking the Swagger API by default when the Swagger server is not enabled [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    (dup)- Improve the high availability of etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    (dup)- Reduce the memory consumption of `GetRegions` requests [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - Support reusing HTTP connections [#6913](​https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - Add a new `halt-scheduling` configuration item to suspend PD scheduling [#6493](https://github.com/tikv/pd/issues/6493) @[JmPotato](https://github.com/JmPotato)

+ TiFlash <!-- tw: ran-huang 3-->

    - Improve TiFlash write performance through IO batch optimization [#7735](https://github.com/pingcap/tiflash/issues/7735) @[lidezhu](https://github.com/lidezhu)
    - Improve TiFlash write performance by removing unnecessary fsync operations [#7736](https://github.com/pingcap/tiflash/issues/7736) @[lidezhu](https://github.com/lidezhu)
    - Limit the maximum length of the TiFlash coprocessor task queue to avoid excessive queuing of coprocessor tasks, which impacts TiFlash's service availability [#7747](https://github.com/pingcap/tiflash/issues/7747) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR) <!-- tw: ran-huang 3-->

        - Enhance support for connection reuse by setting `MaxIdleConns` and `MaxIdleConnsPerHost` parameters in the HTTP client [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - Improve fault tolerance of BR when it fails to connect to PD or external S3 storage [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - Add a new restore parameter `WaitTiflashReady`. When this parameter is enabled, the restore operation will be completed after TiFlash replicas are successfully replicated [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC <!-- tw: Oreoxmt 2-->

        - Refine the status message when TiCDC retries after a failure [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)
        - Optimize the way TiCDC handles messages that exceed the limit when synchronizing to Kafka by supporting only sending the primary key to the downstream [#9574](https://github.com/pingcap/tiflow/issues/9574) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): Storage Sink now supports hexadecimal encoding for HEX formatted data, making it compatible with AWS DMS format specifications [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM) <!-- tw: hfxsd 1-->
    
        - Support strict optimistic mode for incompatible DDLs [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + Dumpling <!-- tw: hfxsd 1-->

        - Reduce export overhead by skipping querying all databases and tables when exporting data with the `-sql` parameter [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB <!-- tw: qiancai 7-->

    - Fix the issue that `index out of range` error might be reported when pushing down the `STREAM_AGG()` operator. [#40857](https://github.com/pingcap/tidb/issues/40857) @[Dousir9](https://github.com/Dousir9)
    - Fix the issue that TiDB ignores all partition information and creates a normal table when the `CREATE TABLE` statement contains sub-partition definitions [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - Fix the issue that incorrect `stale_read_ts` setting might cause `PREPARE stmt` to read data incorrectly [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06) 
    - Fix the issue of possible data race in ActivateTxn [#42092](https://github.com/pingcap/tidb/issues/42092) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a batch client does not reconnect in a timely manner [#44431](https://github.com/pingcap/tidb/issues/44431) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.1.7.md > 错误修复> TiDB - 修复 SQL compile 报错的日志未脱敏的问题 [#41831](https://github.com/pingcap/tidb/issues/41831) @[lance6716](https://github.com/lance6716)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复同时使用 CTE 和关联子查询可能导致查询结果出错或者 panic 的问题 [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 TTL 任务不能及时触发统计信息更新的问题 [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 GC resolve lock 可能错过一些悲观锁的问题 [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 memory tracker 潜在的泄露问题 [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.DDL_JOBS` 表中 `QUERY` 列的数据长度可能超出列定义的问题 [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了使用 `Prepare` 或 `Execute` 查询某些虚拟表时无法将表 ID 下推，导致在大量 Region 的情况下 PD OOM 的问题 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复在为分区表添加新的索引之后，该分区表可能无法正确触发统计信息的自动收集的问题 [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复极端情况下，统计 SQL execution detail 的信息占用太多内存导致 TiDB OOM 的问题 [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 batch coprocessor 重试时可能会生成错误 Region 信息导致查询失败的问题 [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复带 `indexMerge` 的查询被 kill 时可能会卡住的问题 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复在创建分区表时使用 `SUBPARTITION` 没有警告提醒的问题 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复当开启 `tidb_enable_parallel_apply` 时，MPP 模式下的查询结果出错的问题 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复开启 `tidb_opt_agg_push_down` 时查询可能返回错误结果的问题 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了由虚拟列引发的 `can't find proper physical plan` 问题 [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.1.7.md > 错误修复> TiDB - 修复某些情况下 TiDB 查询 panic 的问题 [#40857](https://github.com/pingcap/tidb/issues/40857) @[Dousir9](https://github.com/Dousir9)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 `processInfo` 为空导致的 panic 问题 [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 `SELECT CAST(n AS CHAR)` 语句中的 `n` 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复当使用 MySQL 的 Cursor Fetch 协议时，结果集占用的内存超过 `tidb_mem_quota_query` 的限制导致 TiDB OOM 的问题。修复后，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复通过 BR 恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `duplicate entry` 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复当分区表定义中使用了 `FLOOR()` 函数对分区列进行取整时 `SELECT` 语句返回错误的问题 [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了并发视图模式可能会造成 DDL 操作卡住的问题 [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了收集统计信息任务因为错误的 `datetime` 值而失败的问题 [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-6.1.0.md > 错误修复> TiDB - 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 resolve lock 在 PD 时间跳变的情况下可能卡住的问题 [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 index scan 中可能存在的数据竞争问题 [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复对于过长的 SQL 输入，`FormatSQL()` 方法无法正常截断的问题 [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复即使用户没有权限，也能查看 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表信息的问题 [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
<!-- tw: hfxsd 6-->
    - Fix behavior inconsistency with MySQL when comparing `DATETIME` or `TIMESTAMP` columns to a number constant [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - Fix the issue that an error in Index Join might cause the query to get stuck. [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that might cause go coroutine leaks after killing a connection [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - Fix the issue that `tmp-storage-quota` configuration does not take effect [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that TiFlash a replica might be unavailable when a TiFlash node is down in the cluster [#38484](https://github.com/pingcap/tidb/issues/38484) @[hehechen](https://github.com/hehechen)
    - Fix the issue of TiDB crash due to possible data race when reading and writing `Config.Lables` concurrently. [#45561] (https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)

+ TiKV <!-- tw: qiancai 9-->

    - Fix the issue that `ttl-check-poll-interval` configuration item does not work for RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Fix the issue that Online Unsafe Recovery timeout is not terminated [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Region Merge might be blocked after executing `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix the issue that might lead to inconsistent reads when one TiKV node is quarantined and another is restarted [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - 修复自适应同步模式下 sync-recover 阶段 QPS 下降到 0 的问题 [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - 修复部分写入时加密可能导致数据损坏的问题 [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - 减少 Store 心跳重试次数，修复心跳风暴的问题 [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - 修复当待处理的数据整理字节数较高时流量控制可能无效的问题 [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - 修复在启用了 TiCDC 的 Old Value 功能时，TiKV 可能会使用更多内存的问题 [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ TiKV

    <!-- tw: Oreoxmt 6-->
    - Fix the issue that the `ttl-check-poll-interval` configuration item does not take effect on RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Fix the issue that Online Unsafe Recovery does not abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Region Merge might be blocked after executing `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix the data inconsistency issue that might occur when one TiKV node is isolated and another node is restarted [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the QPS drops to zero in the sync-recover phase under the Data Replication Auto Synchronous mode [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - Fix the issue that encryption might cause data corruption during partial write [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
<!-- tw: ran-huang-->
    - Fix the issue of heartbeat storms by reducing the number of store heartbeat retries [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - Fix the issue that traffic control might not work when there is a high amount of pending compaction bytes [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV might consume more memory when the Old Value feature in TiCDC is enabled [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ PD <!-- tw: hfxsd 5-->

    - 修复 `unsafe recovery` 中失败的 learner peer 在 `auto-detect` 模式中被忽略的问题 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)
    - 修复当 etcd 已经启动，但 client 尚未连接上 etcd 时，调用 client 会导致 PD panic 的问题 [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - 修复 leader 长时间无法退出的问题 [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - 修复 Placement Rule 在使用 `LOCATION_LABLES` 时，SQL 和 Rule Checker 不兼容的问题 [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.1.4.md > Bug 修复> PD - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复 `unsafe recovery` 中失败的 learner peer 在 `auto-detect` 模式中被忽略的问题 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)

+ TiFlash <!-- tw: hfxsd-->

    - 修复在更改 `DATETIME`、`TIMESTAMP`、`TIME` 数据类型的 `fsp` 之后查询失败的问题 [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复由于 Region 的边界的 Key 不合法导致 TiFlash 数据不一致的问题 [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - (dup): release-7.3.0.md > 错误修复> TiFlash - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.1.1.md > 错误修复> TiFlash - 修复 TiFlash 在使用 Online Unsafe Recovery 之后重启时间过长的问题 [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)
    - 修复 TiFlash 在进行除法运算时对 `DECIMAL` 结果 round 进位错误的问题 [#6462](https://github.com/pingcap/tiflash/issues/6462) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR) <!-- tw: ran-huang 7-->

        - Fix the issue of restore failures by increasing the default values of the global parameters `TableColumnCountLimit` and `IndexLimit` used by BR to their maximum values [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of rewrite failures when processing ddl meta information in PITR [#43184](https://github.com/pingcap/tidb/issues/43184) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of panic caused by not checking function returns during PITR execution [#45853](https://github.com/pingcap/tidb/issues/45853) @[Leavrth](https://github.com/Leavrth) 
        - Fix the issue of obtaining invalid region ID when using S3-compatible storage other than AWS S3 [#41916](https://github.com/pingcap/tidb/issues/41916) [#42033](https://github.com/pingcap/tidb/issues/42033) @[3pointer](https://github.com/3pointer) 
        - Fix the potential error in fine-grained backup phase [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - (dup)- Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup)- Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!-- tw: Oreoxmt 8-->

        - Fix the issue that the replication task might get stuck when the downstream encounters an error and retries [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the replication task fails due to short retry intervals when synchronizing to Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might cause synchronization write conflicts when modifying multiple unique key rows in one transaction on the upstream [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC might incorrectly synchronize rename DDL operations [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the replication task might get stuck when the downstream encounters a short-term failure [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - (dup): Fix the panic issue that might occur when the TiCDC node status changes [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - (dup): Fix the issue that when Kafka Sink encounters errors it might indefinitely block changefeed progress [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - (dup): Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): Fix the data inconsistency issue that might occur when some TiCDC nodes are isolated from the network [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): Fix the issue that the replication task might get stuck when the redo log is enabled and there is an exception downstream [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): Fix the issue that changefeeds would fail due to the temporary unavailability of PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - (dup): Fix the issue of too many downstream logs caused by frequently setting the downstream bidirectional replication-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - (dup): Fix the issue that Avro protocol incorrectly identifies `Enum` type values [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM) <!-- tw: hfxsd 3-->

        - 修复唯一键列名为空时导致 panic 问题 [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)
        - 修复 validator 处理错误时可能死锁的问题，并优化了 retry 机制 [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - 修复计算 causality key 时未考虑 collation 的问题 [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)

    + TiDB Lightning <!-- tw: hfxsd 10-->

        - 修复当存在正在导入数据的 engine 时 disk quota 检查可能阻塞的问题 [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当目标集群启用 SSL 时 checksum 报错 `Region is unavailable` 的问题 [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - 修复无法正确输出编码错误的问题 [#44321](https://github.com/pingcap/tidb/issues/44321) @[lyzx2001](https://github.com/lyzx2001)
        - 修复 CSV 数据导入时，route 可能 panic 的问题 [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)
        - 修复逻辑导入模式下导入 A 表时可能误报 B 表不存在的问题 [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)
        - 修复保存 `NEXT_GLOBAL_ROW_ID` 时类型错误问题 [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - 修复 `checksum = "optional"` 时 Checksum 阶段仍然报错的问题 [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - 修复当 PD 集群地址变更时数据导入失败的问题 [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - 修复部分 PD 节点失败导致数据导入失败的问题 [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - 修复当表使用 `AUTO_ID_CACHE=1` 且使用自增列时，ID 分配器 base 值错误的问题 [#46100](https://github.com/pingcap/tidb/issues/46100) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling  <!-- tw: hfxsd 1-->

        - 修复导出到 S3 时 file writer 关闭报错未处理导致导出文件丢失的问题 [#45353](https://github.com/pingcap/tidb/issues/45353) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Binlog <!-- tw: hfxsd 1-->

        - 修复 etcd client 初始化时没有自动同步最新节点信息的问题 [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
