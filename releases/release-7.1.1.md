---
title: TiDB 7.1.1 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.1.1.
---

# TiDB 7.1.1 Release Notes

Release date: Jul xx, 2023

TiDB version: 7.1.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.1#version-list)

## Compatibility changes
<!--1 tw:@Oreoxmt-->
- 为减小 RocksDB 中 compaction 任务的数据量，TiKV 配置项 [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].compaction-guard-min-output-file-size</code>](/tikv-configuration-file.md#compaction-guard-min-output-file-size) 的默认值从 `"8MB"` 修改为 `"1MB"` [#14888](https://github.com/tikv/tikv/issues/14888) @[tonyxuqqi](https://github.com/tonyxuqqi)

## Improvements

+ TiDB
    <!--2 tw:@Oreoxmt-->
    - 非 Prepare 语句执行计划缓存支持带有 200 个参数的查询 [#44823](https://github.com/pingcap/tidb/issues/44823) @[qw4990](https://github.com/qw4990)
    - 优化了跟落盘相关的 chunk 读取的性能 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    (dup: release-7.2.0.md > Improvements> TiDB)- Optimize the logic of constructing index scan range so that it supports converting complex conditions into index scan range [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    (dup: release-7.2.0.md > Improvements> TiDB)- When the retry leader of stale read encounters a lock, TiDB forcibly retries with the leader after resolving the lock, which avoids unnecessary overhead [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06) @[you06](https://github.com/you06)

+ TiKV

    (dup: release-6.6.0.md > Improvements> TiKV)- Optimize the default values of some parameters in partitioned-raft-kv mode: the default value of the TiKV configuration item `storage.block-cache.capacity` is adjusted from 45% to 30%, and the default value of `region-split-size` is adjusted from `96MiB` adjusted to `10GiB`. When using raft-kv mode and `enable-region-bucket` is `true`, `region-split-size` is adjusted to 1 GiB by default. [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD
    <!--1 tw:@Oreoxmt-->
    - 默认屏蔽 swagger API 如果编译没有开启 swagger server [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC
        <!--1 tw:@Oreoxmt-->
        - 优化同步到对象存储时对二进制字段的编码格式方式 [#9373](https://github.com/pingcap/tiflow/issues/9373)
        (dup: release-7.2.0.md > Improvements> Tools> TiCDC)- Support the OAUTHBEARER authentication in the scenario of replication to Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/hi-rustin) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning
        <!--1 tw:@Oreoxmt-->
        - 改进 Lightning 在 checksum 阶段针对 PD `ClientTSOStreamClosed` 错误的重试 [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)
        (dup: release-7.2.0.md > Improvements> Tools> TiDB Lightning)- Verify checksum through SQL after the import to improve stability of verification [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Dumpling
        <!--1 tw:@Oreoxmt-->
        - 避免 Dumpling 在 `--sql` 参数时执行表查询语句，从而减少导出开销 [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

    + TiDB Binlog

        - (dup): release-6.5.3.md > 改进提升> Tools> TiDB Binlog - 优化表信息的获取方式，降低 Drainer 的初始化时间和内存占用 [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## Bug fixes

+ TiDB
    <!--10 tw:@ran-huang-->
    - Fix the issue that Stats Collector might cause deadlock when creating a new session [#44502](https://github.com/pingcap/tidb/issues/44502) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the potential memory leak issue in memory tracker [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that batch coprocessor retry might generate incorrect Region information that causes query failure [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - Fix the data race issue in index scan [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that query results are incorrect in parallel apply + MPP mode [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - Fix the hang-up issue when queries with `indexMerge` are killed [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that excessive memory consumption of SQL execution details in statistics causes TiDB OOM in extreme cases [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that `FormatSQL()` method cannot properly truncate extremely long SQL statements in input [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that DDL operations get stuck during cluster upgrade, which causes upgrade failure [#44158](https://github.com/pingcap/tidb/issues/44158) @[zimulala](https://github.com/zimulala)
    - Fix the fault handling issue that TTL tasks fail multiple times without being taken over by other TiDB instances [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    <!--11 tw:@qiancai-->
    - 使用 mysql 的 cursor fetch 协议时，若结果集内存大小超过 `tidb_mem_quota_query` 则自动落盘 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - 修复即使用户没有权限，也能查看 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表信息的问题 [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 "admin show ddl jobs" 的结果中，ROW_COUNT 不准确的问题 [#44044](https://github.com/pingcap/tidb/issues/44044) @[tangenta](https://github.com/tangenta)
    - 修复一处 range columns 分区表查询报错的问题 [#43459](https://github.com/pingcap/tidb/issues/43459) @[mjonss](https://github.com/mjonss)
    - 修复 DDL 任务从暂停状态到恢复时，恢复出错的问题 [#44217](https://github.com/pingcap/tidb/issues/44217) @[dhysum](https://github.com/dhysum)
    - 修复内存中悲观锁导致 flashback 失败并且数据不一致的问题 [#44292](https://github.com/pingcap/tidb/issues/44292) @[JmPotato](https://github.com/JmPotato)
    - 修复表删除之后还能从 `INFORMATION_SCHEMA` 读取到的问题 [#43714](https://github.com/pingcap/tidb/issues/43714) @[tangenta](https://github.com/tangenta)
    - 修复集群升级前，如果有暂停的 DDL，会出现升级失败的问题 [#44225](https://github.com/pingcap/tidb/issues/44225) @[zimulala](https://github.com/zimulala)
    - 修复通过 br 恢复 'AUTO_ID_CACHE=1' 的表时，会出现 'duplicate entry' 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 DDL owner 切换数次之后，触发数据索引不一致的问题 [#44619](https://github.com/pingcap/tidb/issues/44619) @[tangenta](https://github.com/tangenta)
    - 修复对于 none 状态的 add index DDL 任务执行 cancel 时并没有从后端任务队列中清理导致的泄漏问题 [#44205](https://github.com/pingcap/tidb/issues/44205) @[tangenta](https://github.com/tangenta)
    (dup: release-7.1.0.md > Bug fixes> TiDB)- Fix the issue that the proxy protocol reports the `Header read timeout` error when processing certain erroneous data [#43205](https://github.com/pingcap/tidb/issues/43205) @[blacktear23](https://github.com/blacktear23) @[blacktear23](https://github.com/blacktear23)
    - (dup): release-6.5.3.md > 错误修复> TiDB -修复 PD 隔离可能会导致运行的 DDL 阻塞的问题 [#44267](https://github.com/pingcap/tidb/issues/44267) @[wjhuang2016](https://github.com/wjhuang2016)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue that the query result of the `SELECT CAST(n AS CHAR)` statement is incorrect when `n` in the statement is a negative number [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox) @[xhebox](https://github.com/xhebox)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue of excessive memory usage after creating a large number of empty partitioned tables [#44308](https://github.com/pingcap/tidb/issues/44308) @[hawkingrei](https://github.com/hawkingrei) @[hawkingrei](https://github.com/hawkingrei)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that Join Reorder might cause incorrect outer join results [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid) @[AilinKid](https://github.com/AilinKid)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue that queries containing Common Table Expressions (CTEs) might cause insufficient disk space [#44477](https://github.com/pingcap/tidb/issues/44477) @[guo-shaoge](https://github.com/guo-shaoge) @[guo-shaoge](https://github.com/guo-shaoge)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that dropping a database causes slow GC progress [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao) @[tiancaiamao](https://github.com/tiancaiamao)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that adding an index fails in the ingest mode [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta) @[tangenta](https://github.com/tangenta)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue that the `SELECT` statement returns an error for a partitioned table if the table partition definition uses the `FLOOR()` function to round a partitioned column [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust) @[jiyfhust](https://github.com/jiyfhust)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that follower read does not handle flashback errors before retrying, which causes query errors [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06) @[you06](https://github.com/you06)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that using `memTracker` with cursor fetch causes memory leaks [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao) @[YangKeao](https://github.com/YangKeao)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that the `SHOW PROCESSLIST` statement cannot display the TxnStart of the transaction of the statement with a long subquery time [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520) @[crazycs520](https://github.com/crazycs520)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that the `LEADING` hint does not support querying block aliases [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990) @[qw4990](https://github.com/qw4990)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that `PREPARE stmt FROM "ANALYZE TABLE xxx"` might be killed by `tidb_mem_quota_query` [#44320](https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan) @[chrysan](https://github.com/chrysan)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the panic issue caused by empty `processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala) @[zimulala](https://github.com/zimulala)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that data and indexes are inconsistent when the `ON UPDATE` statement does not correctly update the primary key [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan) @[zyguan](https://github.com/zyguan)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue that queries might return incorrect results when `tidb_opt_agg_push_down` is enabled [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid) @[AilinKid](https://github.com/AilinKid)
    (dup: release-6.1.7.md > Bug fixes> TiDB)- Fix the issue that using CTEs and correlated subqueries simultaneously might result in incorrect query results or panic [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    (dup: release-7.2.0.md > Bug fixes> TiDB)- Fix the issue that canceling a DDL task in the rollback state causes errors in related metadata [#44143](https://github.com/pingcap/tidb/issues/44143) @[wjhuang2016](https://github.com/wjhuang2016) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD
    <!--2 tw:@Oreoxmt-->
    - 修复 Resource Manager 重复初始化 default 资源组的问题 [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    - 修复 placement rule in SQL 设置 location labels 在特定条件下不按预期调度的问题 [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    (dup: release-7.2.0.md > Bug fixes> PD)- Fix the issue that redundant replicas cannot be automatically repaired in some corner cases [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch) @[nolouch](https://github.com/nolouch)

+ TiFlash
    <!--2 tw:@Oreoxmt-->
    - 修复 `task_scheduler_active_set_soft_limit` 配置可能不生效的问题 [#7692](https://github.com/pingcap/tiflash/issues/7692) @[windtalker](https://github.com/windtalker)
    - 修复存算分离模式下，TiFlash 计算节点获取的 cpu 核数信息不准确的问题 [#7436](https://github.com/pingcap/tiflash/issues/7436) @[guo-shaoge](https://github.com/guo-shaoge)

+ Tools

    + Backup & Restore (BR)

        (dup: release-7.2.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that `checksum mismatch` is falsely reported in some cases [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth) @[Leavrth](https://github.com/Leavrth)

    + TiCDC
        <!--4 tw:@hfxsd-->
        - Fix the issue that a PD exception might cause the replication task to get stuck [#8808](https://github.com/pingcap/tiflow/issues/8808) [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen) @[fubinzh](https://github.com/fubinzh)
        - Fix the issue of excessive memory consumption when replicating to an object storage service [#8894](https://github.com/pingcap/tiflow/issues/8894) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the replication task might get stuck when the redo log is enabled and there is an exception downstream [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC keeps retrying when there is a downstream failure which causes the retry time to be too long [#9272](https://github.com/pingcap/tiflow/issues/9272) @[asddongmen](https://github.com/asddongmen)
        (dup: release-7.2.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of excessive downstream pressure caused by reading downstream metadata too frequently when replicating data to Kafka [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin) @[hi-rustin](https://github.com/hi-rustin)
        (dup: release-6.5.3.md > Bug fixes> Tools> TiCDC)- Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin) @[hi-rustin](https://github.com/hi-rustin)
        (dup: release-6.5.3.md > Bug fixes> Tools> TiCDC)- Fix the OOM issue caused by excessive memory usage of the sorter component in some special scenarios [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu) @[hicqu](https://github.com/hicqu)
        (dup: release-7.2.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that the `UPDATE` operation cannot output old values when the Avro or CSV protocol is used [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand) @[3AceShowHand](https://github.com/3AceShowHand)
        (dup: release-6.5.3.md > Bug fixes> Tools> TiCDC)- Fix the issue that when replicating data to storage services, the JSON file corresponding to downstream DDL statements does not record the default values of table fields [#9066](https://github.com/pingcap/tiflow/issues/9066) @[CharlesCheung96](https://github.com/CharlesCheung96) @[CharlesCheung96](https://github.com/CharlesCheung96)
        (dup: release-7.2.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of too many downstream logs caused by frequently setting the downstream bidirectional replication-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen) @[asddongmen](https://github.com/asddongmen)
        (dup: release-6.5.3.md > Bug fixes> Tools> TiCDC)- Fix the issue that when a replication error occurs due to an oversized Kafka message, the message body is recorded in the log [#9031](https://github.com/pingcap/tiflow/issues/9031) @[darraes](https://github.com/darraes) @[darraes](https://github.com/darraes)
        (dup: release-6.5.3.md > Bug fixes> Tools> TiCDC)- Fix the issue that TiCDC gets stuck when PD fails such as network isolation or PD Owner node reboot [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)
        <!--1 tw:@hfxsd-->
        - Fix the issue that DM-master exits abnormally when a unique index contains empty columns in the migrated table structure [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning
        <!--2 tw:@hfxsd-->
        - Fix the issue that TiDB Lightning connection to PD fails and cannot be retried, thus increasing the import success rate [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Lightning does not display the error message correctly when writing data to TiKV and returning an out of space error [#44733](https://github.com/pingcap/tidb/issues/44733) @[lance6716](https://github.com/lance6716)
        - Fix the "region is unavailable" error during checksum operation
[#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        (dup: release-7.2.0.md > Bug fixes> Tools> TiDB Lightning)- Fix the TiDB Lightning panic issue when `experimental.allow-expression-index` is enabled and the default value is UUID [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu) @[lichunzhu](https://github.com/lichunzhu)
        (dup: release-6.1.7.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that disk quota might be inaccurate due to competing conditions [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter) @[D3Hunter](https://github.com/D3Hunter)
        (dup: release-6.1.7.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that in Logical Import Mode, deleting tables downstream during import might cause TiDB Lightning metadata not to be updated in time [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun) @[dsdashun](https://github.com/dsdashun)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + Dumpling
        <!--1 tw:@hfxsd-->
        - Fix the issue that Dumpling exits abnormally when the `-sql` query result set is empty [#45200](https://github.com/pingcap/tidb/issues/45200) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog
        <!--2 tw:@hfxsd-->
        - Fix the issue that TiDB cannot correctly query binlog node status via `SHOW PUMP STATUS` or `SHOW DRAINER STATUS` after a complete change of the PD address [#42643](https://github.com/pingcap/tidb/issues/42643) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB cannot write binlogs after a complete change of the PD address [#42643](https://github.com/pingcap/tidb/issues/42643) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.1.7.md > 错误修复> Tools> TiDB Binlog - 修复 etcd client 初始化时没有自动同步最新节点信息的问题 [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
