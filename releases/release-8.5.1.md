---
title: TiDB 8.5.1 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 8.5.1.
---

# TiDB 8.5.1 Release Notes

Release date: January xx, 2025

TiDB version: 8.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Operating system and platform requirement changes

Starting from v8.5.1, TiDB resumes the support for CentOS Linux 7. If you plan to deploy TiDB v8.5 or upgrade your cluster to v8.5, ensure you use TiDB v8.5.1 or a later version.

- According to [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/), the upstream support for CentOS Linux 7 ends on June 30, 2024. In v8.4.0 DMR and v8.5.0, TiDB temporarily suspends the support for CentOS 7 and recommends you to use Rocky Linux 9.1 or later. Upgrading a TiDB cluster on CentOS 7 to v8.4.0 or v8.5.0 will cause the risk of cluster unavailability.

- Although TiDB v8.5.1 and later versions resume the support for CentOS Linux 7, due to the CentOS Linux EOL status, it is strongly recommended that you review the [official announcements and security guidance](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol) for CentOS Linux 7 and consider migrating to an [operating system supported by TiDB](/hardware-and-software-requirements.md#os-and-platform-requirements), such as Rocky Linux 9.1 or later.

## Improvements

+ TiDB <!--tw@Oreoxmt: 5 notes-->

    - Support folding read-only user-defined variables into constants [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - Convert Cartesian product Semi Join with nulleq condition to Semi Join with equality condition [#57583](https://github.com/pingcap/tidb/issues/57583) @[hawkingrei](https://github.com/hawkingrei)
    - Adjust the default threshold of statistics memory cache to 20% of total memory [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV <!--tw@Oreoxmt: 1 note-->

    - Add detection mechanism for illegal `max_ts` updates [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)

+ TiFlash

    - (dup): release-7.5.5.md > Improvements> TiFlash - Optimize the retry strategy for TiFlash compute nodes in the disaggregated storage and compute architecture to handle exceptions when downloading files from Amazon S3 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + TiCDC <!--tw@qiancai: 1 note-->

        - Filter out events that are not subscribed to by TiCDC in advance to avoid unnecessary resource consumption [#17877](https://github.com/tikv/tikv/issues/17877) @[hicqu](https://github.com/hicqu)

## Bug fixes

+ TiDB <!--tw@lilin90: the following 10 notes-->

    - (dup): release-7.5.5.md > Bug fixes> TiDB - Fix the issue that the default timeout for querying the TiFlash system table is too short [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.5.md > Bug fixes> TiDB - Fix the issue that when setting `tidb_gogc_tuner_max_value` and `tidb_gogc_tuner_min_value`, if the maximum value is null, an incorrect warning message occurs [#57889](https://github.com/pingcap/tidb/issues/57889) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.5.md > Bug fixes> TiDB - Fix the issue that data indexes are inconsistent because plan cache uses the wrong schema when adding indexes [#56733](https://github.com/pingcap/tidb/issues/56733) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.5.5.md > Bug fixes> TiDB - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复没有收集过统计信息的表的上次 ANALYZE 时间可能不为 NULL 的问题 [#57735](https://github.com/pingcap/tidb/issues/57735) @[winoros](https://github.com/winoros)
    - 正确处理取统计信息的异常，防止后台任务超时时内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行 DROP DATABASE 语句后统计信息未被清理的问题  [#57230](https://github.com/pingcap/tidb/issues/57230) @[Rustin170506](https://github.com/Rustin170506)
    - 修复在构造 IndexMerge 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在超过 3000 维向量类型的列上创建向量搜索索引会失败的问题 [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - 修复 REORGANIZE PARTITION 操作未正确移除被替换的全局索引以及处理非聚簇表唯一索引的问题。[#56822](https://github.com/pingcap/tidb/issues/56822) @[mjonss](https://github.com/mjonss)
    - 修复分区表 Range INTERVAL 语法糖不支持使用 `MINUTE` 做间隔的问题。[#57698](https://github.com/pingcap/tidb/issues/57698) @[mjonss](https://github.com/mjonss)
    - 修复查询慢日志时，由于时区导致的时间范围错误的问题 [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在缩减 TTL 扫描任务工作线程时，任务取消失败可能导致扫描任务泄漏的问题。 [#57708](https://github.com/pingcap/tidb/issues/57708) @[YangKeao](https://github.com/YangKeao) 
    - 增强了时间戳合法性检查。[#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta) <!--tw@hfxsd: the following 10 notes-->
    - 修复在丢失心跳后，若 TTL 表被删除或禁用，TTL 作业仍继续运行的问题 [#57702](https://github.com/pingcap/tidb/issues/57702) @[YangKeao](https://github.com/YangKeao)
    - 修复 TTL 作业被取消后，last_job_finish_time 显示不正确的问题 [#58109](https://github.com/pingcap/tidb/issues/58109) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB 丢失心跳时，TTL 任务无法被取消的问题 [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    - 修复某个 TTL 任务丢失心跳会阻塞其他任务获取心跳的问题 [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    - 修复缩减 TTL 工作线程时，部分过期行未被删除的问题。 [#57990](https://github.com/pingcap/tidb/issues/57990) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当 TTL 删除速率限制器被中断时，剩余行未重试的问题。[#58205](https://github.com/pingcap/tidb/issues/58205) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在某些情况下，TTL 可能生成大量警告日志的问题。[#58305](https://github.com/pingcap/tidb/issues/58305) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在修改 tidb_ttl_delete_rate_limit 时，部分 TTL 任务可能挂起的问题。[#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - 修复执行 REORGANIZE PARTITION 时，数据回填可能导致并发更新被回滚的问题。[#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - 修复查询 cluster_slow_query 表时使用 order by 可能导致结果乱序的问题。[#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)

+ TiKV <!--tw@Oreoxmt: 2 notes-->

    - Fix the issue that encoding might fail when processing GBK/GB18030 encoded data [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that TiKV panics due to uninitialized replicas when the TiKV MVCC In-Memory Engine (IME) preloads them [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus](https://github.com/overvenus)
    - (dup): release-8.1.2.md > Bug fixes> TiKV - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.2.md > Bug fixes> TiKV - Fix the issue that TiKV cannot report heartbeats to PD when the disk is stuck [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!--tw@Oreoxmt: 1 note-->

    - Fix the issue that PD might panic when the `tidb_enable_tso_follower_proxy` system variable is enabled [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.5.md > Bug fixes> PD - Fix the issue that `evict-leader-scheduler` fails to work properly when it is repeatedly created with the same Store ID [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)

+ TiFlash <!--tw@qiancai: 2 notes-->

    - (dup): release-7.5.5.md > Bug fixes> TiFlash - Fix the issue that querying new columns might return incorrect results under the disaggregated storage and compute architecture [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)
    - Fix the issue that TiFlash might unexpectedly reject processing Raft messages when memory usage is low [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that the `POSITION()` function for TiFlash does not support character set collation [#9377](https://github.com/pingcap/tiflash/issues/9377) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 1 note-->

        - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw@qiancai: 5 notes-->

         - Fix the issue that the changefeed might get stuck after new TiKV nodes are added to the cluster [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that the event filter incorrectly uses the new table name instead of the old table name for filtering when processing `RENAME TABLE` DDL statements [#11946](https://github.com/pingcap/tiflow/issues/11946) @[kennytm](https://github.com/kennytm)
        - Fix the issue that goroutines leak occurs after a changefeed is deleted [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - Fix the issue that out-of-order messages resent by the Sarama client cause Kafka message order to be incorrect [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the default value of the NOT NULL timestamp field in the Debezium protocol is incorrect [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)