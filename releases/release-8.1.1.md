---
title: TiDB 8.1.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.1.1.
---

# TiDB 8.1.1 Release Notes

Release date: xx xx, 2024

TiDB version: 8.1.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Compatibility changes

- (dup): release-6.5.10.md > Compatibility changes - Must set the line terminator when using TiDB Lightning `strict-format` to import CSV files [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

## Improvements

+ TiDB

    - (dup): release-7.5.3.md > Improvements> TiDB - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing the `TRUNCATE` or `DROP` operation on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.10.md > Improvements> TiDB - Remove stores without Regions during MPP load balancing [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-8.0.0.md > Improvements> TiDB - Temporarily adjust the priority of statistics synchronously loading tasks to high to avoid widespread timeouts during TiKV high loads, as these timeouts might result in statistics not being loaded [#50332](https://github.com/pingcap/tidb/issues/50332) @[winoros](https://github.com/winoros)

+ PD <!--tw:hfxsd 1 条-->

    - Improve the retry logic of the HTTP client [#8142](https://github.com/tikv/pd/issues/8142) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - (dup): release-7.5.3.md > 改进提升> TiFlash - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.5.3.md > Improvements> TiFlash - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR) <!--tw:qiancai 1 条-->

        - (dup): release-7.1.5.md > 改进提升> Tools> Backup & Restore (BR) - 增加 PITR 集成测试用例，覆盖对日志备份与添加索引加速功能的兼容性测试 [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.2.0.md > Improvements> Tools> Backup & Restore (BR) - Support encryption of temporary files generated during log backup [#15083](https://github.com/tikv/tikv/issues/15083) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.5.3.md > Improvements> Tools> Backup & Restore (BR) - Except for the `br log restore` subcommand, all other `br log` subcommands support skipping the loading of the TiDB `domain` data structure to reduce memory consumption [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.3.md > Improvements> Tools> Backup & Restore (BR) - Support setting Alibaba Cloud access credentials through environment variables [#45551](https://github.com/pingcap/tidb/issues/45551) @[RidRisR](https://github.com/RidRisR)
        - 在 tikv 下载 sst 文件之前，增加剩余空间是否够用的检查 [#17224](https://github.com/tikv/tikv/issues/17224) @[RidRisR](https://github.com/RidRisR)

    + TiCDC <!--tw:qiancai 1 条-->

        - 支持 simple protocol 在 changefeed 启动时一次性发送所有表的 Bootstrap 消息 [#11315](https://github.com/pingcap/tiflow/issues/11315) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-6.5.10.md > Improvements> Tools> TiCDC - Support directly outputting raw events when the downstream is a Message Queue (MQ) or cloud storage [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB <!--tw:hfxsd 以下 7 条-->

    - Fix the issue that `INDEX_HASH_JOIN` cannot exit properly when SQL is abnormally interrupted [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that RANGE partitioned tables that are not strictly self-incrementing can be created [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that PointGet execution plans for `_tidb_rowid` can be generated [#54583](https://github.com/pingcap/tidb/issues/54583) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that SQL statements in internal statements in the slow log are redacted to null by default [#54190](https://github.com/pingcap/tidb/issues/54190) [#52743](https://github.com/pingcap/tidb/issues/52743) [#53264](https://github.com/pingcap/tidb/issues/53264) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the `UPDATE` operation can cause TiDB OOM in multi-table scenarios [#53742](https://github.com/pingcap/tidb/issues/53742) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.5.md > Bug fixes> TiDB - Fix the issue that the Window function might panic when there is a related subquery in it [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the `LENGTH()` condition is unexpectedly removed when the collation is `utf8_bin` or `utf8mb4_bin` [#53730](https://github.com/pingcap/tidb/issues/53730) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that after a statement within a transaction is killed by OOM, if TiDB continues to execute the next statement within the same transaction, you might get an error `Trying to start aggressive locking while it's already started` and a panic occurs [#53540](https://github.com/pingcap/tidb/issues/53540) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that `PREPARE`/`EXECUTE` statements with the `CONV` expression containing a `?` argument might result in incorrect query results when executed multiple times [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the recursive CTE operator incorrectly tracks memory usage [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that using `SHOW WARNINGS;` to obtain warnings might cause a panic [#48756](https://github.com/pingcap/tidb/issues/48756) @[xhebox](https://github.com/xhebox)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the TopN operator might be pushed down incorrectly [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that TiDB panics when executing the `SHOW ERRORS` statement with a predicate that is always `true` [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the `STATE` field in the `INFORMATION_SCHEMA.TIDB_TRX` table is empty due to the `size` of the `STATE` field not being defined [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that DDL statements incorrectly use etcd and cause tasks to queue up [#52335](https://github.com/pingcap/tidb/issues/52335) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the `Distinct_count` information in GlobalStats might be incorrect [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the `tidb_enable_async_merge_global_stats` and `tidb_analyze_partition_concurrency` system variables do not take effect during automatic statistics collection [#53972](https://github.com/pingcap/tidb/issues/53972) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the Connection Count monitoring metric in Grafana is incorrect when some connections exit before the handshake is complete [#54428](https://github.com/pingcap/tidb/issues/54428) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the Connection Count of each resource group is incorrect when using TiProxy and resource groups [#54545](https://github.com/pingcap/tidb/issues/54545) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that using a view does not work in recursive CTE [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that the `final` AggMode and the `non-final` AggMode cannot coexist in Massively Parallel Processing (MPP) [#51362](https://github.com/pingcap/tidb/issues/51362) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue of incorrect WARNINGS information when using Optimizer Hints [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue of abnormally high memory usage caused by `memTracker` not being detached when the `HashJoin` or `IndexLookUp` operator is the driven side sub-node of the `Apply` operator [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue of potential data races during the execution of `(*PointGetPlan).StatsInfo()` [#49803](https://github.com/pingcap/tidb/issues/49803) [#43339](https://github.com/pingcap/tidb/issues/43339) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that JSON-related functions return errors inconsistent with MySQL in some cases [#53799](https://github.com/pingcap/tidb/issues/53799) @[dveeden](https://github.com/dveeden)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that TiDB does not create corresponding statistics metadata (`stats_meta`) when creating a table with foreign keys [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the `memory_quota` hint might not work in subqueries [#53834](https://github.com/pingcap/tidb/issues/53834) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that TiDB might report an error due to GC when loading statistics at startup [#53592](https://github.com/pingcap/tidb/issues/53592) @[you06](https://github.com/you06)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that executing `CREATE OR REPLACE VIEW` concurrently might result in the `table doesn't exist` error [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that the query latency of stale reads increases, caused by information schema cache misses [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that `SELECT INTO OUTFILE` does not work when clustered indexes are used as predicates [#42093](https://github.com/pingcap/tidb/issues/42093) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that comparing a column of `YEAR` type with an unsigned integer that is out of range causes incorrect results [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that TiDB might return incorrect query results when you query tables with virtual columns in transactions that involve data modification operations [#53951](https://github.com/pingcap/tidb/issues/53951) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that when queries contain non-correlated subqueries and `LIMIT` clauses, column pruning might be incomplete, resulting in a less optimal plan [#54213](https://github.com/pingcap/tidb/issues/54213) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that non-BIGINT unsigned integers might produce incorrect results when compared with strings/decimals [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - (dup): release-8.2.0.md > Bug fixes> TiDB - Fix the issue that setting `max-index-length` causes TiDB to panic when adding indexes using the Distributed eXecution Framework (DXF) [#53281](https://github.com/pingcap/tidb/issues/53281) @[zimulala](https://github.com/zimulala)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the issue that certain filter conditions in queries might cause the planner module to report an `invalid memory address or nil pointer dereference` error [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.10.md > Bug fixes> TiDB - Fix the overflow issue of the `Longlong` type in predicates [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that indirect placeholder `?` references in a `GROUP BY` statement cannot find columns [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that the memory used by transactions might be tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue that using `CURRENT_DATE()` as the default value for a column results in incorrect query results [#53746](https://github.com/pingcap/tidb/issues/53746) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the performance is unstable when adding indexes using global sorting [#54147](https://github.com/pingcap/tidb/issues/54147) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `SHOW IMPORT JOBS` reports an error `Unknow column `summary`` after upgrading from v7.1 [#54241](https://github.com/pingcap/tidb/issues/54241) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `root` user cannot query `tidb_mdl_view` [#53292](https://github.com/pingcap/tidb/issues/53292) @[tangenta](https://github.com/tangenta) <!--tw:lilin90 以下 8 条-->
    - 修复使用分布式框架添加索引期间出现网络分区可能导致数据索引不一致的问题 [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - 修复 local backend 初始化期间报错可能导致资源泄露的问题 [#53659](https://github.com/pingcap/tidb/issues/53659) @[D3Hunter](https://github.com/D3Hunter)
    - 修复当 view 定义中使用子查询作为列定义时，无法通过 information_schema.columns 获取列信息的问题 [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - 修复使用索引加速添加唯一索引在遇到 owner 切换时可能导致 duplicate entry 的问题 [#49233](https://github.com/pingcap/tidb/issues/49233) @[lance6716](https://github.com/lance6716)
    - 修复设置 global.tidb_cloud_storage_uri 报错信息不清晰的问题 [#54096](https://github.com/pingcap/tidb/issues/54096) @[lance6716](https://github.com/lance6716)
    - 支持在多值索引的 `IndexRangeScan` 上生成 `Selection [#55012](https://github.com/pingcap/tidb/issues/55012)@[time-and-fate](https://github.com/time-and-fate)
    - 修复 sync load 监控不正确的问题 [#53558](https://github.com/pingcap/tidb/issues/53558)@[hawkingrei](https://github.com/hawkingrei)
    - 修复 concurrency init stats 可能遗漏加载的问题 [#53607](https://github.com/pingcap/tidb/issues/53607) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.3.md > Bug fixes> TiDB - Fix the issue of reusing wrong point get plans for `SELECT ... FOR UPDATE` [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)

+ TiKV <!--tw:qiancai 1 条-->

    - (dup): release-7.5.3.md > Bug fixes> TiKV - Fix the issue that CDC and log-backup do not limit the timeout of `check_leader` using the `advance-ts-interval` configuration, causing the `resolved_ts` lag to be too large when TiKV restarts normally in some cases [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-7.5.3.md > Bug fixes> TiKV - Fix the issue that setting the gRPC message compression method via `grpc-compression-type` does not take effect on messages sent from TiKV to TiDB [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the failure of `make docker` and `make docker_test` [#17075](https://github.com/tikv/tikv/issues/17075) @[shunki-fujita](https://github.com/shunki-fujita)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that the **gRPC request sources duration** metric is displayed incorrectly in the monitoring dashboard [#17133](https://github.com/tikv/tikv/issues/17133) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that the output of the `raft region` command in tikv-ctl does not include the Region status information [#17037](https://github.com/tikv/tikv/issues/17037) @[glorv](https://github.com/glorv)
    - (dup): release-8.2.0.md > Bug fixes> TiKV - Fix the issue that changing the `raftstore.periodic-full-compact-start-times` configuration item online might cause TiKV to panic [#17066](https://github.com/tikv/tikv/issues/17066) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - (dup): release-7.5.3.md > Bug fixes> TiKV - Fix the issue that TiKV might repeatedly panic when applying a corrupted Raft data snapshot [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)
    - 修复 evict 未被持久化 entries 的问题 [#17040](https://github.com/tikv/tikv/issues/17040) @[glorv](https://github.com/glorv)

+ PD <!--tw:Oreoxmt 9 条-->

    - Fix the issue that an incorrect PD API is called when you retrieve table attributes [#55188](https://github.com/pingcap/tidb/issues/55188) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the time data type in the `INFORMATION_SCHEMA.RUNAWAY_WATCHES` table is incorrect [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that some logs are not redacted [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - Fix the issue of missing data in the `Filter` monitoring item [#8098](https://github.com/tikv/pd/issues/8098) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the HTTP client might panic when TLS is enabled [#8237](https://github.com/tikv/pd/issues/8237) @[okJiang](https://github.com/okJiang)
    - Fix the issue that the encryption manager is not initialized before use [#8384](https://github.com/tikv/pd/issues/8384) @[rleungx](https://github.com/rleungx)
    - Fix the issue that Resource Group could not effectively limit resource usage under high concurrency [#8435](https://github.com/tikv/pd/issues/8435) @[nolouch](https://github.com/nolouch)
    - Fix the data race issue related to `store limit` [#8253](https://github.com/tikv/pd/issues/8253) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the scaling progress is displayed incorrectly after the `scheduling` microservice is enabled [#8331](https://github.com/tikv/pd/issues/8331) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the TSO node could not be dynamically updated after the `tso` microservice is enabled [#8154](https://github.com/tikv/pd/issues/8154) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复资源组遇到的数据竞争问题 [#8267](https://github.com/tikv/pd/issues/8267) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复资源组在请求 token 超过 500 ms 时遇到超出配额限制的问题 [#8349](https://github.com/tikv/pd/issues/8349) @[nolouch](https://github.com/nolouch)
    - (dup): release-8.2.0.md > 错误修复> PD - 修复手动切换 PD leader 可能失败的问题 [#8225](https://github.com/tikv/pd/issues/8225) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复 etcd client 中已经删除的节点仍然出现在候选连接列表中的问题 [#8286](https://github.com/tikv/pd/issues/8286) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-8.2.0.md > 错误修复> PD - 修复 `ALTER PLACEMENT POLICY` 无法修改 placement policy 的问题 [#52257](https://github.com/pingcap/tidb/issues/52257) [#51712](https://github.com/pingcap/tidb/issues/51712) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.1.5.md > 错误修复> PD - 修复写热点调度可能会违反放置策略 (placement policy) 约束的问题 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-6.5.10.md > 错误修复> PD - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - (dup): release-8.2.0.md > 错误修复> PD - 修复取消资源组查询导致大量重试的问题 [#8217](https://github.com/tikv/pd/issues/8217) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复 PD 在进行 operator 检查时遇到的数据竞争问题 [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复将角色 (role) 绑定到资源组时未报错的问题 [#54417](https://github.com/pingcap/tidb/issues/54417) @[JmPotato](https://github.com/JmPotato)
    - (dup): release-7.5.3.md > 错误修复> PD - 修复将 TiKV 配置项 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 设置为小于 1 MiB 的值会导致 PD panic 的问题 [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)

+ TiFlash <!--tw:qiancai 1 条-->

    - 修复 TiFlash 与任意 PD 发生网络分区后，可能导致读请求超时报错的问题 [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.10.md > Bug fixes> TiFlash - Fix the issue that the `SUBSTRING_INDEX()` function might cause TiFlash to crash in some corner cases [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that a large number of duplicate rows might be read in FastScan mode after importing data via BR or TiDB Lightning [#9118](https://github.com/pingcap/tiflash/issues/9118) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic when a database is deleted shortly after creation [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.2.0.md > Bug fixes> TiFlash - Fix the issue that in the disaggregated storage and compute architecture, null values might be incorrectly returned in queries after adding non-null columns in DDL operations [#9084](https://github.com/pingcap/tiflash/issues/9084) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that TiFlash might panic after executing `RENAME TABLE ... TO ...` on a partitioned table with empty partitions across databases [#9132](https://github.com/pingcap/tiflash/issues/9132) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.2.0.md > Bug fixes> TiFlash - Fix the issue of query timeout when executing queries on partitioned tables that contain empty partitions [#9024](https://github.com/pingcap/tiflash/issues/9024) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that some queries might report a column type mismatch error after late materialization is enabled [#9175](https://github.com/pingcap/tiflash/issues/9175) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.5.3.md > Bug fixes> TiFlash - Fix the issue that queries with virtual generated columns might return incorrect results after late materialization is enabled [#9188](https://github.com/pingcap/tiflash/issues/9188) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - (dup): release-7.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.10.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR fails to correctly identify errors due to multiple nested retries during the restore process [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-8.2.0.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR fails to restore a transactional KV cluster due to an empty `EndKey` [#52574](https://github.com/pingcap/tidb/issues/52574) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.10.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup might be paused after the advancer owner migration [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - (dup): release-7.5.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.10.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that a PD connection failure could cause the TiDB instance where the log backup advancer owner is located to panic [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw:qiancai 2 条-->

        - 修复 region 变更导致下游 panic 的问题 [#17233](https://github.com/tikv/tikv/issues/17233) @[hicqu](https://github.com/hicqu)
        - 修复 当上游未启用新的排序规则时，TiCDC 无法正确解码具有聚集索引的表的主键的问题 [#11371](https://github.com/pingcap/tiflow/issues/11371)@[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that the checksum is not correctly set to `0` after splitting `UPDATE` events [#11402](https://github.com/pingcap/tiflow/issues/11402) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-8.2.0.md > Bug fixes> Tools> TiCDC - Fix the issue that data inconsistency might occur when restarting Changefeed repeatedly when performing a large number of `UPDATE` operations in a multi-node environment [#11219](https://github.com/pingcap/tiflow/issues/11219) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.5.3.md > Bug fixes> Tools> TiCDC - Fix the issue that the Processor module might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM) <!--tw:qiancai 2 条-->

        - (dup): release-8.2.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that `SET` statements cause DM to panic during the migration of MariaDB data [#10206](https://github.com/pingcap/tiflow/issues/10206) @[dveeden](https://github.com/dveeden)
        - (dup): release-8.2.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the connection blocking issue by upgrading `go-mysql` [#11041](https://github.com/pingcap/tiflow/issues/11041) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当索引长度超过默认 max-index-length 时导致同步中断的问题 [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - 修复 schema tracker 无法正确处理 LIST 分区表的问题 [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)"

    + TiDB Lightning  <!--tw:qiancai 1 条-->

        - (dup): release-6.5.10.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that the Region fetched from PD does not have a Leader when restoring data using BR or importing data using TiDB Lightning in physical import mode [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复 lightning 获取 keyspace name 时输出的 WARN 日志可能引起混淆的问题 [#54232](https://github.com/pingcap/tidb/issues/54232) @[kennytm](https://github.com/kennytm)

    + Dumpling

        - (dup): release-6.5.10.md > Bug fixes> Tools> Dumpling - Fix the issue that Dumpling reports an error when exporting tables and views at the same time [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog

        - (dup): release-6.5.10.md > Bug fixes> Tools> TiDB Binlog - Fix the issue that deleting rows during the execution of `ADD COLUMN` might report an error `data and columnID count not match` when TiDB Binlog is enabled [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)