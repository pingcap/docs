---
title: TiDB 8.5.1 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 8.5.1.
---

# TiDB 8.5.1 Release Notes

Release date: January xx, 2025

TiDB version: 8.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Operating system and platform requirement changes

Starting from v8.5.1, TiDB resumes testing of CentOS Linux 7 and is compatible with it. If you plan to deploy TiDB v8.5 or upgrade your cluster to v8.5, ensure you use TiDB v8.5.1 or a later version.

- TiDB v8.4.0 DMR and v8.5.0 releases dropped support and testing with CentOS Linux 7 because it reaches [EOL status on June 30, 2024](https://www.redhat.com/en/topics/linux/centos-linux-eol). Upgrading a TiDB cluster on CentOS 7 to v8.4.0 or v8.5.0 will cause the risk of cluster unavailability.

- To assist users still running CentOS Linux 7, we resumed testing of CentOS Linux 7 starting from v8.5.1. However, due to the EOL status of CentOS Linux, it is strongly recommended that you review the [official announcements and security guidance](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol) for CentOS Linux 7 and migrate to an [operating system supported by TiDB](/hardware-and-software-requirements.md#os-and-platform-requirements) for production use, such as Rocky Linux 9.1 or later.

As CentOS Linux 7 has reached EOL, testing of this distribution will be stopped in a future release.

## Improvements

+ TiDB <!--tw@Oreoxmt: 5 notes-->

    - Support folding read-only user-defined variables into constants [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - Convert Cartesian product Semi Join with nulleq condition to Semi Join with equality condition [#57583](https://github.com/pingcap/tidb/issues/57583) @[hawkingrei](https://github.com/hawkingrei)
    - Adjust the default threshold of statistics memory cache to 20% of total memory [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    - Enhance the timestamp validity check [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)

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
    - Fix the issue that the last `ANALYZE` time of tables without collected statistics might not be NULL [#57735](https://github.com/pingcap/tidb/issues/57735) @[winoros](https://github.com/winoros)
    - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that statistics are not cleared after executing the `DROP DATABASE` statement [#57230](https://github.com/pingcap/tidb/issues/57230) @[Rustin170506](https://github.com/Rustin170506)
    - Fix the issue that some predicates might be lost when constructing `IndexMerge` [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that creating a vector search index on a column with more than 3000 dimensions causes the `KeyTooLong` error [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - Fix the issue that the `REORGANIZE PARTITION` operation does not correctly clean up replaced global indexes and handles unique indexes on non-clustered tables [#56822](https://github.com/pingcap/tidb/issues/56822) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the Range INTERVAL syntax sugar of partitioned tables does not support using `MINUTE` as the interval [#57698](https://github.com/pingcap/tidb/issues/57698) @[mjonss](https://github.com/mjonss)
    - Fix the issue that changing the timezone causes incorrect query results when querying slow logs [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that task cancellation failure might cause the task to leak when shrinking the TTL workers of scan tasks [#57708](https://github.com/pingcap/tidb/issues/57708) @[YangKeao](https://github.com/YangKeao) <!--tw@hfxsd: the following 10 notes-->
    - Fix the issue that after a heartbeat is lost and the TTL table is deleted or disabled, TTL jobs keep running [#57702](https://github.com/pingcap/tidb/issues/57702) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `last_job_finish_time` is displayed incorrectly after a TTL job is canceled [#58109](https://github.com/pingcap/tidb/issues/58109) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TTL jobs cannot be canceled if the TiDB heartbeat is lost [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that a TTL job that loses the heartbeat blocks other jobs from getting heartbeats [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when shrinking the TTL workers, some expired rows are not deleted [#57990](https://github.com/pingcap/tidb/issues/57990) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the remaining rows are not retried when the TTL delete rate limiter is interrupted [#58205](https://github.com/pingcap/tidb/issues/58205) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TTL might generate a large number of warning logs in certain cases [#58305](https://github.com/pingcap/tidb/issues/58305) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that some TTL jobs might hang when modifying `tidb_ttl_delete_rate_limit` [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that data backfill during `REORGANIZE PARTITION` might cause concurrent updates to be rolled back [#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - Fix the issue that using `ORDER BY` when querying `cluster_slow_query table` might generate unordered results [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)

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