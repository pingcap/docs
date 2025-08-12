---
title: TiDB 8.5.2 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 8.5.2.
---

# TiDB 8.5.2 Release Notes

Release date: June 12, 2025

TiDB version: 8.5.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Improvements

+ TiDB 

    - Limit the execution of GC for TTL tables and related statistics collection tasks to the owner node, thereby reducing overhead [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - Support modifying the `import.num-threads` configuration item dynamically [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)

+ Tools

    + Backup & Restore (BR)

        - Remove the check on AWS region names to avoid backup errors caused by newly supported AWS regions failing the validation [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)

    + TiDB Lightning

        - Add a row width check when parsing CSV files to prevent OOM issues [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that TiDB fails to obtain TSO during timestamp verification after setting the `zone` label [#59402](https://github.com/pingcap/tidb/issues/59402) @[ekexium](https://github.com/ekexium)
    - Fix the issue that Hash Join returns incorrect results without reporting an error when execution fails [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiFlash might crash or return incorrect results [#60517](https://github.com/pingcap/tidb/issues/60517) @[wintalker](https://github.com/wintalker)
    - Fix the issue that execution hangs when parallel sorting with `ORDER BY` encounters an error or the query is canceled [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that an error occurs when querying partitioned tables that contain generated columns [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that creating two views with the same name does not report an error [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that different data types on both sides of the equality condition in Join might cause incorrect results in TiFlash [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    - Fix the issue that queries with `is null` conditions on Hash partitioned tables cause a panic [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014/)
    - Fix the issue that after executing `ALTER TABLE ... PLACEMENT POLICY ...` in a cluster with TiFlash nodes in the disaggregated storage and compute architecture, Region peers might be accidentally added to TiFlash Compute nodes [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that loading statistics manually might fail when the statistics file contains null values [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that TTL jobs might be ignored or processed multiple times [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that incorrect judgment in exchange partition causes execution failure [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    - Fix the issue that improper exception handling for statistics causes in-memory statistics to be mistakenly deleted when background tasks time out [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a canceled TTL task might put an uncommitted session to the global session pool [#58900](https://github.com/pingcap/tidb/issues/58900) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that enabling Redact log does not take effect in certain scenarios [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `rowContainer` might cause TiDB to panic in certain scenarios [#59976](https://github.com/pingcap/tidb/issues/59976) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that partition pruning might be incorrect in the `Point_Get` scenario for partitioned tables [#59827](https://github.com/pingcap/tidb/issues/59827) @[mjonss](https://github.com/mjonss)
    - Fix the issue that updating records in partitioned tables during DDL execution might lead to data corruption [#57588](https://github.com/pingcap/tidb/issues/57588) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the performance and stability of `information_schema` are affected in certain scenarios [#58142](https://github.com/pingcap/tidb/issues/58142) [#58363](https://github.com/pingcap/tidb/issues/58363) [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that `tidb_txn_entry_size_limit` cannot be dynamically adjusted in internal TiDB sessions when the Distributed eXecution Framework (DXF) is enabled [#59506](https://github.com/pingcap/tidb/issues/59506) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the `IMPORT INTO` feature fails to properly handle unique key conflicts when Global Sort is enabled [#59650](https://github.com/pingcap/tidb/issues/59650) @[lance6716](https://github.com/lance6716)
    - Fix the issue that injecting network latency errors in the global sorting data path causes the `IMPORT INTO` operation to fail [#50451](https://github.com/pingcap/tidb/issues/50451) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that executing `ADD UNIQUE INDEX` might cause data inconsistency [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the value of the `LABELS` column is incorrectly displayed in the `BINLOG_STATUS` column when querying `INFORMATION_SCHEMA.TIDB_SERVERS_INFO` [#59245](https://github.com/pingcap/tidb/issues/59245) @[lance6716](https://github.com/lance6716)
    - Fix the issue that injecting a kill PD Leader fault during index creation might cause data inconsistency [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB runs out of memory (OOM) after creating approximately 6.5 million tables [#58368](https://github.com/pingcap/tidb/issues/58368) @[lance6716](https://github.com/lance6716)
    - Fix the issue that adding a unique key might fail when importing a large amount of data with the Global Sort feature enabled [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that TiDB returns unreadable error messages after failing to access S3 external storage [#59326](https://github.com/pingcap/tidb/issues/59326) @[lance6716](https://github.com/lance6716)
    - Fix the issue that querying `information_schema.tables` returns mismatched `table_schema` and `table_name` values [#60593](https://github.com/pingcap/tidb/issues/60593) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the DDL notifier might deliver incorrect notifications when internal SQL commits fail [#59055](https://github.com/pingcap/tidb/issues/59055) @[lance6716](https://github.com/lance6716)
    - Fix the issue that `ADD INDEX` DDL operations still split SST files by 96 MiB when the Global Sort feature is enabled, despite the Region size is 256 MiB [#59962](https://github.com/pingcap/tidb/issues/59962) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiDB servers run out of memory (OOM) when memory usage exceeds 80% during data import with the Global Sort feature enabled [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - Fix the issue that a potential deadlock might occur in `txn_status_cache` [#18384](https://github.com/tikv/tikv/issues/18384) @[ekexium](https://github.com/ekexium)
    - Fix the issue that Resolved-TS monitoring and logs might be abnormal [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    - Fix the issue that Region merge might lead to TiKV abnormal exit due to Raft index mismatch [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    - Fix the issue that TiKV cannot report heartbeats to PD when the disk is stuck [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that a deadlock might occur when GC Worker is under heavy load [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - Fix the issue that time rollback might cause abnormal RocksDB flow control, leading to performance jitter [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that CDC connections might cause resource leakage when encountering exceptions [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the latest written data might not be readable when only one-phase commit (1PC) is enabled and Async Commit is not enabled [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)

+ PD

    - Fix the concurrency issue that might arise when forwarding TSO in microservice scenarios [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the result returned by `BatchScanRegions` is not properly limited [#9216](https://github.com/tikv/pd/issues/9216) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that an unexpected election occurs when one follower experiences a network partition from the leader [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that `COOLDOWN` or `SWITCH_GROUP` cannot be triggered when `QUERY_LIMIT` is set in resource control [#60404](https://github.com/pingcap/tidb/issues/60404) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that `StoreInfo` might be incorrectly overridden [#9185](https://github.com/tikv/pd/issues/9185) @[okJiang](https://github.com/okJiang)
    - Fix the issue that operations in data import or adding index scenarios might fail due to unstable PD network [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    - Fix the issue that the default value of `max-size` for a single log file is not correctly set [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    - Fix the issue that memory leaks might occur when allocating TSOs [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the `tidb_enable_tso_follower_proxy` system variable might not take effect [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that a PD node might still generate TSOs even when it is not the Leader [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - Fix the issue that Region syncer might not exit in time during the PD Leader switch [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the default value of `lease` is not correctly set [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that data spill during sorting might cause TiFlash to crash [#9999](https://github.com/pingcap/tiflash/issues/9999) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiFlash might return the `Exception: Block schema mismatch` error when executing SQL statements containing `GROUP BY ... WITH ROLLUP` [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that in the disaggregated storage and compute architecture, TiFlash compute nodes might be incorrectly selected as target nodes for adding Region peers [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might fail to print error stack traces when it unexpectedly exits in certain situations [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might maintain high memory usage after importing large amounts of data [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that TiFlash startup might be blocked when `profiles.default.init_thread_count_scale` is set to `0` [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that queries on a partitioned table might return errors after executing `ALTER TABLE ... RENAME COLUMN` on that partitioned table [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that a `Not found column` error might occur when a query involves virtual columns and triggers remote reads [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash might consume a large amount of memory when tables in a cluster contain a large number of `ENUM` type columns [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might fail to restart after inserting a single row of data larger than 16 MiB [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might not clean some disk data correctly after new data is inserted to tables with vector indexes, causing abnormal disk space consumption [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might delete previously created vector indexes unexpectedly after multiple vector indexes are created on the same table, causing performance degradation [#9971](https://github.com/pingcap/tiflash/issues/9971) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might fail to use vector indexes to accelerate vector search queries in the disaggregated storage and compute architecture [#9847](https://github.com/pingcap/tiflash/issues/9847) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might print a large number of `tag=EnumParseOverflowContainer` logs in the disaggregated storage and compute architecture [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash does not skip Learner Read as expected when executing `SELECT ... AS OF TIMESTAMP` queries [#10046](https://github.com/pingcap/tiflash/issues/10046) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that TiFlash might panic when handling snapshots with irregular Region key-ranges [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that repeated downloading of SST files during data restore could cause TiKV to panic in extreme cases [#18335](https://github.com/tikv/tikv/issues/18335) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the `status` field is missing in the result when querying log backup tasks using `br log status --json` [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that BR fails to restore due to getting the `rpcClient is idle` error when sending requests to TiKV [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - Fix the issue that log backup fails to exit properly when encountering a fatal error due to not being able to access PD [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that PITR fails to restore indexes larger than 3072 bytes [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that the changefeed might get stuck after the replication traffic exceeds the traffic threshold of the downstream Kafka [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the dispatch rule for the Kafka sink does not take effect when the `pulsar+http` or `pulsar+https` protocol is used [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        - Fix the issue that TiCDC fails to observe the PD leader migration in time, causing the replication latency to increase [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that TiCDC reports errors when replicating `default NULL` SQL statements via the Avro protocol [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - Fix the issue that after the default value of a newly added column in the upstream is changed from `NOT NULL` to `NULL`, the default values of that column in the downstream are incorrect [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - Fix the issue that TiCDC fails to properly connect to PD after PD scale-in [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that TiCDC might panic when replicating `CREATE TABLE IF NOT EXISTS` or `CREATE DATABASE IF NOT EXISTS` statements [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Fix the issue that the pre-check of `start-task` fails when both TLS and `shard-mode` are configured [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    + TiDB Lightning

        - Fix the issue that the performance degrades when importing data from a cloud storage in high-concurrency scenarios [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - Fix the issue that the error report output is truncated when importing data using TiDB Lightning [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)
        - Fix the issue that logs are not properly desensitized [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that authentication would fail with a `context canceled` error when using an external account to perform any GCS storage operation [#60155](https://github.com/pingcap/tidb/issues/60155) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning can get stuck for several hours when importing Parquet files from cloud storage into TiDB [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        - Fix the issue that TiDB Lightning could run out of memory (OOM) during writing or ingesting SST files into the TiKV cluster when importing large volumes of data [#59947](https://github.com/pingcap/tidb/issues/59947) @[OliverS929](https://github.com/OliverS929)
        - Fix the issue that low maximum QPS during table creation and slow access to `information_schema.tables` cause TiDB Lightning to dispatch schema jobs slower in scenarios with millions of tables [#58141](https://github.com/pingcap/tidb/issues/58141) @[D3Hunter](https://github.com/D3Hunter)

    + NG Monitoring

        - Fix the issue that DocDB consumes too much memory under high workloads, and use SQLite as an optional backend for DocDB [#267](https://github.com/pingcap/ng-monitoring/issues/267) @[mornyx](https://github.com/mornyx)
        - Fix the issue that TSDB consumes too much memory under high cardinality of time series data, and provide a memory configuration option for TSDB [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
