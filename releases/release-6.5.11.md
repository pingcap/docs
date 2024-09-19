---
title: TiDB 6.5.11 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.11.
---

# TiDB 6.5.11 Release Notes

Release date: September 20, 2024

TiDB version: 6.5.11

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## Improvements

+ TiDB

    - By batch deleting TiFlash placement rules, improve the processing speed of data GC after performing the `TRUNCATE` or `DROP` operation on partitioned tables [#54068](https://github.com/pingcap/tidb/issues/54068) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV

    - Optimize the compaction trigger mechanism of RocksDB to accelerate disk space reclamation when handling a large number of DELETE versions [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)

+ TiFlash

    - Reduce lock conflicts under highly concurrent data read operations and optimize short query performance [#9125](https://github.com/pingcap/tiflash/issues/9125) @[JinheLin](https://github.com/JinheLin)
    - Optimize the execution efficiency of `LENGTH()` and `ASCII()` functions [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + TiCDC

        - When the downstream is TiDB with the `SUPER` permission granted, TiCDC supports querying the execution status of `ADD INDEX DDL` from the downstream database to avoid data replication failure due to timeout in retrying executing the DDL statement in some cases [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB

    - Fix the issue that the recursive CTE operator incorrectly tracks memory usage [#54181](https://github.com/pingcap/tidb/issues/54181) @[guo-shaoge](https://github.com/guo-shaoge)
    - Reset the parameters in the `Open` method of `PipelinedWindow` to fix the unexpected error that occurs when the `PipelinedWindow` is used as a child node of `Apply` due to the reuse of previous parameter values caused by repeated opening and closing operations [#53600](https://github.com/pingcap/tidb/issues/53600) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the memory used by transactions might be tracked multiple times [#53984](https://github.com/pingcap/tidb/issues/53984) @[ekexium](https://github.com/ekexium)
    - Fix the issue of abnormally high memory usage caused by `memTracker` not being detached when the `HashJoin` or `IndexLookUp` operator is the driven side sub-node of the `Apply` operator [#54005](https://github.com/pingcap/tidb/issues/54005) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that `INDEX_HASH_JOIN` cannot exit properly when SQL is abnormally interrupted [#54688](https://github.com/pingcap/tidb/issues/54688) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that table replication fails when the index length of the table replicated from DM exceeds the maximum length specified by `max-index-length` [#55138](https://github.com/pingcap/tidb/issues/55138) @[lance6716](https://github.com/lance6716)
    - Fix the issue that indirect placeholder `?` references in a `GROUP BY` statement cannot find columns [#53872](https://github.com/pingcap/tidb/issues/53872) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the illegal column type `DECIMAL(0,0)` can be created in some cases [#53779](https://github.com/pingcap/tidb/issues/53779) @[tangenta](https://github.com/tangenta)
    - Fix the issue that predicates cannot be pushed down properly when the filter condition of a SQL query contains virtual columns and the execution condition contains `UnionScan` [#54870](https://github.com/pingcap/tidb/issues/54870) @[qw4990](https://github.com/qw4990)
    - Fix the issue that executing the `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...` query might return incorrect results [#53726](https://github.com/pingcap/tidb/issues/53726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of reusing wrong point get plans for `SELECT ... FOR UPDATE` [#54652](https://github.com/pingcap/tidb/issues/54652) @[qw4990](https://github.com/qw4990)
    - Fix the issue that RANGE partitioned tables that are not strictly self-incrementing can be created [#54829](https://github.com/pingcap/tidb/issues/54829) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `TIMESTAMPADD()` function goes into an infinite loop when the first argument is `month` and the second argument is negative [#54908](https://github.com/pingcap/tidb/issues/54908) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiDB fails to reject unauthenticated user connections in some cases when using the `auth_socket` authentication plugin [#54031](https://github.com/pingcap/tidb/issues/54031) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the network partition during adding indexes using the Distributed eXecution Framework (DXF) might cause inconsistent data indexes [#54897](https://github.com/pingcap/tidb/issues/54897) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the query might get stuck when terminated because the memory usage exceeds the limit set by `tidb_mem_quota_query` [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - Fix the issue that recursive CTE queries might result in invalid pointers [#54449](https://github.com/pingcap/tidb/issues/54449) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `tot_col_size` column in the `mysql.stats_histograms` table might be a negative number [#55126](https://github.com/pingcap/tidb/issues/55126) @[qw4990](https://github.com/qw4990)
    - Fix the issue that obtaining the column information using `information_schema.columns` returns warning 1356 when a subquery is used as a column definition in a view definition [#54343](https://github.com/pingcap/tidb/issues/54343) @[lance6716](https://github.com/lance6716)
    - Fix the issue that TiDB reports an error in the log when closing the connection in some cases [#53689](https://github.com/pingcap/tidb/issues/53689) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the performance of the `SELECT ... WHERE ... ORDER BY ...` statement execution is poor in some cases [#54969](https://github.com/pingcap/tidb/issues/54969) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `SUB_PART` value in the `INFORMATION_SCHEMA.STATISTICS` table is `NULL` [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the query might return incorrect results instead of an error after being killed [#50089](https://github.com/pingcap/tidb/issues/50089) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that querying the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table might cause TiDB to panic [#54324](https://github.com/pingcap/tidb/issues/54324) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that empty `groupOffset` in `StreamAggExec` might cause TiDB to panic [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that disk files might not be deleted after the `Sort` operator spills and a query error occurs [#55061](https://github.com/pingcap/tidb/issues/55061) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the data race issue in `IndexNestedLoopHashJoin` [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - Fix the issue that an error occurs when using `SHOW COLUMNS` to view columns in a view [#54964](https://github.com/pingcap/tidb/issues/54964) @[lance6716](https://github.com/lance6716)
    - Fix the issue that an error occurs when a DML statement contains nested generated columns [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - Fix the issue that prevents master key rotation when the master key is stored in a Key Management Service (KMS) [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - Fix a traffic control issue that might occur after deleting large tables or partitions [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that TiKV might panic due to importing deleted `sst_importer` SST files [#15053](https://github.com/tikv/tikv/issues/15053) @[lance6716](https://github.com/lance6716)
    - Fix the issue that TiKV might panic when processing Raft snapshots with stale replicas, particularly during slow replica split operations followed by immediate deletion of the new replica [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that TiKV might repeatedly panic when applying a corrupted Raft data snapshot [#15292](https://github.com/tikv/tikv/issues/15292) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that setting the gRPC message compression method via `grpc-compression-type` does not take effect on messages sent from TiKV to TiDB [#17176](https://github.com/tikv/tikv/issues/17176) @[ekexium](https://github.com/ekexium)
    - Fix the issue that CDC and log-backup do not limit the timeout of `check_leader` using the `advance-ts-interval` configuration, causing the `resolved_ts` lag to be too large when TiKV restarts normally in some cases [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue that some logs are not redacted [#8419](https://github.com/tikv/pd/issues/8419) @[rleungx](https://github.com/rleungx)
    - Fix the issue that setting the TiKV configuration item [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) to a value less than 1 MiB causes PD panic [#8323](https://github.com/tikv/pd/issues/8323) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that setting `replication.strictly-match-label` to `true` causes TiFlash to fail to start [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - Fix the data race issue that PD encounters during operator checks [#8263](https://github.com/tikv/pd/issues/8263) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - Fix the issue that TiFlash might panic when a database is deleted shortly after creation [#9266](https://github.com/pingcap/tiflash/issues/9266) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that setting the SSL certificate configuration to an empty string in TiFlash incorrectly enables TLS and causes TiFlash to fail to start [#9235](https://github.com/pingcap/tiflash/issues/9235) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a network partition (network disconnection) between TiFlash and any PD might cause read request timeout errors [#9243](https://github.com/pingcap/tiflash/issues/9243) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash might crash when processing queries containing an outer join [#9190](https://github.com/pingcap/tiflash/issues/9190) @[windtalker](https://github.com/windtalker)
    - Fix the issue that converting data types to `DECIMAL` might cause incorrect query results in some corner cases [#53892](https://github.com/pingcap/tidb/issues/53892) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that frequent `EXCHANGE PARTITION` and `DROP TABLE` operations over a long period in a cluster might slow down the replication of TiFlash table metadata and degrade the query performance [#9227](https://github.com/pingcap/tiflash/issues/9227) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the checkpoint path of backup and restore is incompatible with some external storage [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - Fix the inefficiency issue in scanning DDL jobs during incremental backups [#54139](https://github.com/pingcap/tidb/issues/54139) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the backup performance during checkpoint backups is affected due to interruptions in seeking Region leaders [#17168](https://github.com/tikv/tikv/issues/17168) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that DDLs requiring backfilling, such as `ADD INDEX` and `MODIFY COLUMN`, might not be correctly recovered during incremental restore [#54426](https://github.com/pingcap/tidb/issues/54426) @[3pointer](https://github.com/3pointer)
        - Fix the issue that after a log backup PITR task fails and you stop it, the safepoints related to that task are not properly cleared in PD [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that backup tasks might get stuck if TiKV becomes unresponsive during the backup process [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that BR logs might print sensitive credential information when log backup is enabled [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - Fix the issue that TiCDC might panic when the Sorter module reads disk data [#10853](https://github.com/pingcap/tiflow/issues/10853) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the Processor module might get stuck when the downstream Kafka is inaccessible [#11340](https://github.com/pingcap/tiflow/issues/11340) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Fix the issue that data replication is interrupted when the index length exceeds the default value of `max-index-length` [#11459](https://github.com/pingcap/tiflow/issues/11459) @[michaelmdeng](https://github.com/michaelmdeng)
        - Fix the issue that schema tracker incorrectly handles LIST partition tables, causing DM errors [#11408](https://github.com/pingcap/tiflow/issues/11408) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM returns an error when replicating the `ALTER TABLE ... DROP PARTITION` statement for LIST partitioned tables [#54760](https://github.com/pingcap/tidb/issues/54760) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM does not set the default database when processing the `ALTER DATABASE` statement, which causes a replication error [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that transaction conflicts occur during data import using TiDB Lightning [#49826](https://github.com/pingcap/tidb/issues/49826) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiKV data might be corrupted when importing data after disabling the import mode of TiDB Lightning [#15003](https://github.com/tikv/tikv/issues/15003) [#47694](https://github.com/pingcap/tidb/issues/47694) @[lance6716](https://github.com/lance6716)
        - Fix the issue that during importing data using TiDB Lightning, an error occurs when restarting TiKV [#15912](https://github.com/tikv/tikv/issues/15912) @[lance6716](https://github.com/lance6716)
