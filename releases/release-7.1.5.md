---
title: TiDB 7.1.5 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.5.
---

# TiDB 7.1.5 Release Notes

Release date: April 26, 2024

TiDB version: 7.1.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## Compatibility changes

- Add a TiKV configuration item [`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659-and-v715) for RocksDB, which helps you investigate possible corruption of Write Ahead Log (WAL) [#16549](https://github.com/tikv/tikv/issues/16549) @[v01dstar](https://github.com/v01dstar)

## Improvements

+ TiDB

    - Support loading Regions in batch from PD to speed up the conversion process from the KV range to Regions when querying large tables [#51326](https://github.com/pingcap/tidb/issues/51326) @[SeaRise](https://github.com/SeaRise)
    - Optimize the issue that the `ANALYZE` statement blocks the metadata lock [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)
    - Add a timeout mechanism for LDAP authentication to avoid the issue of resource lock (RLock) not being released in time [#51883](https://github.com/pingcap/tidb/issues/51883) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - Avoid performing IO operations on snapshot files in raftstore threads to improve TiKV stability [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Upgrade the etcd version to v3.4.30 [#7904](https://github.com/tikv/pd/issues/7904) @[JmPotato](https://github.com/JmPotato)

+ Tools

    + Backup & Restore (BR)

        - Support automatically abandoning log backup tasks when encountering a large checkpoint lag, to avoid prolonged blocking GC and potential cluster issues [#50803](https://github.com/pingcap/tidb/issues/50803) @[RidRisR](https://github.com/RidRisR)
        - Add PITR integration test cases to cover compatibility testing for log backup and adding index acceleration [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - Remove the invalid verification for active DDL jobs when log backup starts [#52733](https://github.com/pingcap/tidb/issues/52733) @[Leavrth](https://github.com/Leavrth)

## Bug fixes

+ TiDB

    - Fix the issue that querying JSON of `BINARY` type might cause an error in some cases [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that query execution using MPP might lead to incorrect query results when a SQL statement contains `JOIN` and the `SELECT` list in the statement contains only constants [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `init-stats` process might cause TiDB to panic and the `load stats` process to quit [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the TiDB server is marked as health before the initialization is complete [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - Fix the issue that `ALTER TABLE ... COMPACT TIFLASH REPLICA` might incorrectly end when the primary key type is `VARCHAR` [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - Fix the issue that TiDB crashes when `shuffleExec` quits unexpectedly [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `SURVIVAL_PREFERENCES` attribute might not appear in the output of the `SHOW CREATE PLACEMENT POLICY` statement under certain conditions [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that after the time window for automatic statistics updates is configured, statistics might still be updated outside that time window [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that query results might be incorrect when the `HAVING` clause in a subquery contains correlated columns [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `approx_percentile` function might cause TiDB panic [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the query result is incorrect when the `IN()` predicate contains `NULL` [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - Fix the issue that the configuration file does not take effect when it contains an invalid configuration item [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `EXCHANGE PARTITION` incorrectly processes foreign keys [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that querying the `TIDB_HOT_REGIONS` table might incorrectly return `INFORMATION_SCHEMA` tables [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the type returned by the `IFNULL` function is inconsistent with MySQL [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the TTL feature causes data hotspots due to incorrect data range splitting in some cases [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TiDB keeps sending probe requests to a TiFlash node that has been offline [#46602](https://github.com/pingcap/tidb/issues/46602) @[zyguan](https://github.com/zyguan)
    - Fix the issue that AutoID Leader change might cause the value of the auto-increment column to decrease in the case of `AUTO_ID_CACHE=1` [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that executing `INSERT IGNORE` might result in inconsistency between the unique index and the data [#51784](https://github.com/pingcap/tidb/issues/51784) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that adding a unique index might cause TiDB to panic [#52312](https://github.com/pingcap/tidb/issues/52312) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the Window function might panic when there is a related subquery in it [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/Rustin170506)
    - Fix the issue that the `init-stats` process might cause TiDB to panic and the `load stats` process to quit [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the performance regression issue caused by disabling predicate pushdown in TableDual [#50614](https://github.com/pingcap/tidb/issues/50614) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that query results might be incorrect when the `HAVING` clause in a subquery contains correlated columns [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `EXPLAIN` statement might display incorrect column IDs in the result when statistics for certain columns are not fully loaded [#52207](https://github.com/pingcap/tidb/issues/52207) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - Fix the issue that resolve-ts is blocked when a stale Region peer ignores the GC message [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that inactive Write Ahead Logs (WALs) in RocksDB might corrupt data [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the monitoring metric `tikv_unified_read_pool_thread_count` has no data in some cases [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that during the execution of an optimistic transaction, if other transactions initiate the resolving lock operation on it, there is a small chance that the atomicity of the transaction might be broken if the transaction's primary key has data that was previously committed in Async Commit or 1PC mode [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue that the scheduling of write hotspots might break placement policy constraints [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the query result of `SHOW CONFIG` includes the deprecated configuration item `trace-region-flow` [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the scaling progress is not correctly displayed [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)

+ TiFlash

    - Fix incorrect `local_region_num` values in logs [#8895](https://github.com/pingcap/tiflash/issues/8895) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that querying generated columns returns an error [#8787](https://github.com/pingcap/tiflash/issues/8787) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `ENUM` column might cause TiFlash to crash during chunk encoding [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - Fix the issue that TiFlash might panic when you insert data to columns with invalid default values in non-strict `sql_mode` [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that if Region migration, split, or merge occurs after the precision of a `TIME` column is modified, queries might fail [#8601](https://github.com/pingcap/tiflash/issues/8601) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that removing a log backup task after it is paused does not immediately restore the GC safepoint [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)
        - Fix the issue that too many logs are printed when a full backup fails [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that BR could not back up the `AUTO_RANDOM` ID allocation progress if the `AUTO_RANDOM` column is in a composite clustered index [#52255](https://github.com/pingcap/tidb/issues/52255) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that TiKV panics when a full backup fails to find a peer in some extreme cases [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that a PD connection failure could cause the TiDB instance where the log backup advancer owner is located to panic [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - Fix an unstable test case [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the global checkpoint of log backup is advanced ahead of the actual backup file write point due to TiKV restart, which might cause a small amount of backup data loss [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - Fix a rare issue that special event timing might cause the data loss in log backup [#16739](https://github.com/tikv/tikv/issues/16739) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that TiCDC fails to execute the `Exchange Partition ... With Validation` DDL downstream after it is written upstream, causing the changefeed to get stuck [#10859](https://github.com/pingcap/tiflow/issues/10859) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that `snapshot lost caused by GC` is not reported in time when resuming a changefeed and the `checkpoint-ts` of the changefeed is smaller than the GC safepoint of TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC panics when scheduling table replication tasks [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that data is written to a wrong CSV file due to wrong BarrierTS in scenarios where DDL statements are executed frequently [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that a changefeed with eventual consistency enabled might fail when the object storage sink encounters a temporary failure [#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the old value part of `open-protocol` incorrectly outputs the default value according to the `STRING` type instead of its actual type [#10803](https://github.com/pingcap/tiflow/issues/10803) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning panics when importing an empty table of Parquet format [#52518](https://github.com/pingcap/tidb/issues/52518) @[kennytm](https://github.com/kennytm)
        - Fix the issue that sensitive information in logs is printed in server mode [#36374](https://github.com/pingcap/tidb/issues/36374) @[kennytm](https://github.com/kennytm)
