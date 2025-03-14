---
title: TiDB 7.5.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.6.
---

# TiDB 7.5.6 Release Notes

Release date: March 14, 2025

TiDB version: 7.5.6

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- Support the openEuler 22.03 LTS SP3/SP4 operating system. For more information, see [OS and platform requirements](https://docs.pingcap.com/tidb/v7.5/hardware-and-software-requirements#os-and-platform-requirements).

## Improvements

+ TiDB

    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - Enhance the timestamp validity check [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)
    - Limit the execution of GC for TTL tables and related statistics collection tasks to the owner node, thereby reducing overhead [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - Add the detection mechanism for invalid `max_ts` updates [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - Disable the table-level checksum calculation during full backups by default (`--checksum=false`) to improve backup performance [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)
        - Add a check to verify whether the target cluster contains a table with the same name for non-full restore [#55087](https://github.com/pingcap/tidb/issues/55087) @[RidRisR](https://github.com/RidRisR)

    + TiDB Lightning

        - Add a row width check when parsing CSV files to prevent OOM issues [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that some predicates might be lost when constructing `IndexMerge` [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `ONLY_FULL_GROUP_BY` setting does not take effect on statements in views [#53175](https://github.com/pingcap/tidb/issues/53175) @[mjonss](https://github.com/mjonss)
    - Fix the issue that creating two views with the same name does not report an error [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that converting data from the `BIT` type to the `CHAR` type might cause TiKV panics [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that a TTL job that loses the heartbeat blocks other jobs from getting heartbeats [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that querying partitioned tables using an `IN` condition containing a mismatched value type and a type conversion error leads to incorrect query results [#54746](https://github.com/pingcap/tidb/issues/54746) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the default value of the `BIT` column is incorrect [#57301](https://github.com/pingcap/tidb/issues/57301) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that in the Prepare protocol, an error occurs when the client uses a non-UTF8 character set [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - Fix the issue that using variables or parameters in the `CREATE VIEW` statement does not report errors [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - Fix the issue that loading statistics manually might fail when the statistics file contains null values [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that when querying the `information_schema.cluster_slow_query` table, if the time filter is not added, only the latest slow log file is queried [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that querying temporary tables might trigger unexpected TiKV requests in some cases [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that some TTL jobs might hang when modifying `tidb_ttl_delete_rate_limit` [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using `ORDER BY` when querying `cluster_slow_query table` might generate unordered results [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that when a virtual generated column's dependencies contain a column with the `ON UPDATE` attribute, the data of the updated row and its index data might be inconsistent [#56829](https://github.com/pingcap/tidb/issues/56829) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that TTL jobs cannot be canceled if the TiDB heartbeat is lost [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    - When the parameter is of `Enum`, `Bit`, or `Set` type, the `Conv()` function is no longer pushed down to TiKV [#51877](https://github.com/pingcap/tidb/issues/51877) @[yibin87](https://github.com/yibin87)
    - Fix the issue that after executing `ALTER TABLE ... PLACEMENT POLICY ...` in a cluster with TiFlash nodes in the disaggregated storage and compute architecture, Region peers might be accidentally added to TiFlash Compute nodes [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that job status is overwritten when the DDL owner changes [#52747](https://github.com/pingcap/tidb/issues/52747) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that queries with `is null` conditions on Hash partitioned tables cause a panic [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014/)
    - Fix the issue that an error occurs when querying partitioned tables that contain generated columns [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that TTL jobs might be ignored or processed multiple times [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that incorrect judgment in exchange partition causes execution failure [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - Fix the issue that setting the `tidb_audit_log` variable with multi-level relative paths causes errors in the log directory [#58971](https://github.com/pingcap/tidb/issues/58971) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that different data types on both sides of the equality condition in Join might cause incorrect results in TiFlash [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)

+ TiKV

    - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that time rollback might cause abnormal RocksDB flow control, leading to performance jitter [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the latest written data might not be readable when only one-phase commit (1PC) is enabled and Async Commit is not enabled [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that a deadlock might occur when GC Worker is under heavy load [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - Fix the issue that disk stalls might prevent leader migration, leading to performance jitter [#17363](https://github.com/tikv/tikv/issues/17363) @[hhwyt](https://github.com/hhwyt)
    - Fix the issue that encoding might fail when processing GBK/GB18030 encoded data [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that CDC connections might cause resource leakage when encountering exceptions [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - Fix the issue that Region merge might lead to TiKV abnormal exit due to Raft index mismatch [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - Fix the issue that Resolved-TS monitoring and logs might be abnormal [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - Fix the issue that an incompatibility with the Titan component causes upgrade failure [#18263](https://github.com/tikv/tikv/issues/18263) @[v01dstar](https://github.com/v01dstar) @[LykxSassinator](https://github.com/LykxSassinator)
  
+ PD

    - Fix the issue that the default value of `max-size` for a single log file is not correctly set [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the value of the `flow-round-by-digit` configuration item might be overwritten after a restart [#8980](https://github.com/tikv/pd/issues/8980) @[nolouch](https://github.com/nolouch)
    - Fix the issue that operations in data import or adding index scenarios might fail due to unstable PD network [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - Fix the issue that PD might panic when the `tidb_enable_tso_follower_proxy` system variable is enabled [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - Fix the issue that the `tidb_enable_tso_follower_proxy` system variable might not take effect [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that memory leaks might occur when allocating TSOs [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - Fix the issue that Region syncer might not exit in time during the PD Leader switch [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - Fix the issue that a PD node might still generate TSOs even when it is not the Leader [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that TiFlash might unexpectedly reject processing Raft messages when memory usage is low [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that TiFlash might maintain high memory usage after importing large amounts of data [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that queries on a partitioned table might return errors after executing `ALTER TABLE ... RENAME COLUMN` on that partitioned table [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might fail to print error stack traces when it unexpectedly exits in certain situations [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash startup might be blocked when `profiles.default.init_thread_count_scale` is set to `0` [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a `Not found column` error might occur when a query involves virtual columns and triggers remote reads [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash compute nodes might be incorrectly selected as target nodes for adding Region peers [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that log backup fails to exit properly when encountering a fatal error due to not being able to access PD [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR fails to restore due to getting the `rpcClient is idle` error when sending requests to TiKV [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the `status` field is missing in the result when querying log backup tasks using `br log status --json` [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backup might unexpectedly enter a paused state when the advancer owner switches [#58031](https://github.com/pingcap/tidb/issues/58031) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Fix the issue that enabling TiCDC in scenarios with many small tables might cause TiKV to restart [#18142](https://github.com/tikv/tikv/issues/18142) @[hicqu](https://github.com/hicqu)
        - Fix the issue that after the default value of a newly added column in the upstream is changed from `NOT NULL` to `NULL`, the default values of that column in the downstream are incorrect [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - Fix the issue that out-of-order messages resent by the Sarama client cause Kafka message order to be incorrect [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC uses incorrect table names for filtering during `RENAME TABLE` operations [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - Fix the issue that goroutines leak occurs after a changefeed is deleted [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - Fix the issue that using the `--overwrite-checkpoint-ts` parameter in the `changefeed pause` command might cause the changefeed to be stuck [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that TiCDC reports errors when replicating `default NULL` SQL statements via the Avro protocol [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - Fix the issue that TiCDC fails to properly connect to PD after PD scale-in [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)

    + TiDB Lightning

        - Fix the issue that logs are not properly desensitized [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
