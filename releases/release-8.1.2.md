---
title: TiDB 8.1.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.1.2.
---

# TiDB 8.1.2 Release Notes

Release date: December 26, 2024

TiDB version: 8.1.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Compatibility changes

- Add the TiKV configuration item [`server.snap-min-ingest-size`](/tikv-configuration-file.md#snap-min-ingest-size-new-in-v812), which specifies the minimum threshold for whether TiKV adopts the ingest method when processing snapshots. The default value is `2MiB`.

    - When the snapshot size exceeds this threshold, TiKV adopts the ingest method, which imports SST files from the snapshot into RocksDB. This method is faster for large files.
    - When the snapshot size does not exceed this threshold, TiKV adopts the direct write method, which writes each piece of data into RocksDB individually. This method is more efficient for small files.

## Improvements

+ TiDB

    - Add metrics about Request Unit (RU) settings [#8444](https://github.com/tikv/pd/issues/8444) @[nolouch](https://github.com/nolouch)

+ TiKV

    - Improve the speed of Region Merge in scenarios with empty tables and small Regions [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize TiKV's `DiskFull` detection to make it compatible with RaftEngine's `spill-dir` configuration, ensuring that this feature works consistently [#17356](https://github.com/tikv/tikv/issues/17356) @[LykxSassinator](https://github.com/LykxSassinator)
    - Optimize the trigger mechanism of RocksDB compaction to accelerate disk space reclamation when handling a large number of DELETE versions [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - Support modifying the `import.num-threads` configuration item dynamically [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)
    - Replace the Rusoto library with AWS Rust SDK to access external storage (such as Amazon S3) for backup and restore, which enhances compatibility with AWS features such as IMDSv2 and EKS Pod Identity [#12371](https://github.com/tikv/tikv/issues/12371) @[akoshchiy](https://github.com/akoshchiy)

+ TiFlash

    - Improve the garbage collection speed of outdated data in the background for tables with clustered indexes [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - Reduce the number of threads that TiFlash needs to create when processing disaggregated storage and compute requests, helping avoid crashes of TiFlash compute nodes when processing a large number of such requests [#9334](https://github.com/pingcap/tiflash/issues/9334) @[JinheLin](https://github.com/JinheLin)
    - Improve the cancel mechanism of the JOIN operator, so that the JOIN operator can respond to cancel requests in a timely manner [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)
    - Optimize the execution efficiency of `LENGTH()` and `ASCII()` functions [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Optimize the retry strategy for TiFlash compute nodes in the disaggregated storage and compute architecture to handle exceptions when downloading files from Amazon S3 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - Reduce unnecessary log printing during backup [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)
        - Disable the table-level checksum calculation (`--checksum=false`) during full backups by default to improve backup performance [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - TiCDC supports querying the status of asynchronously executed DDL tasks after being granted the `SUPER` privilege, preventing execution errors caused by repeatedly executing DDL tasks on the same table [#11521](https://github.com/pingcap/tiflow/issues/11521) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - When the downstream is TiDB with the `SUPER` permission granted, TiCDC supports querying the execution status of `ADD INDEX DDL` from the downstream database to avoid data replication failure due to timeout in retrying executing the DDL statement in some cases [#10682](https://github.com/pingcap/tiflow/issues/10682) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB

    - Fix the issue that existing TTL tasks are executed unexpectedly frequently in a cluster that is upgraded from v6.5 to v7.5 or later [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - Fix the issue that executing `IMPORT INTO` is stuck when Global Sort is enabled and the Region size exceeds 96 MiB [#55374](https://github.com/pingcap/tidb/issues/55374) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the upper bound and lower bound of the histogram are corrupted when `DUMP STATS` is transforming statistics into JSON [#56083](https://github.com/pingcap/tidb/issues/56083) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that execution plan bindings cannot be created for the multi-table `DELETE` statement with aliases [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of memory leaks in TTL tables [#56934](https://github.com/pingcap/tidb/issues/56934) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that partition pruning does not work when the partition expression is `EXTRACT(YEAR FROM col)` [#54210](https://github.com/pingcap/tidb/issues/54210) @[mjonss](https://github.com/mjonss)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing Placement Rules [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query might get stuck when terminated because the memory usage exceeds the limit set by `tidb_mem_quota_query` [#55042](https://github.com/pingcap/tidb/issues/55042) @[yibin87](https://github.com/yibin87)
    - Fix the issue that TiDB queries cannot be canceled during cop task construction [#55957](https://github.com/pingcap/tidb/issues/55957) @[yibin87](https://github.com/yibin87)
    - Fix the issue that reducing the value of `tidb_ttl_delete_worker_count` during TTL job execution makes the job fail to complete [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `CAST` function does not support explicitly setting the character set [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that TTL tasks cannot be canceled when there is a write conflict [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - Fix the data race issue in `IndexNestedLoopHashJoin` [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - Fix the issue that empty `groupOffset` in `StreamAggExec` might cause TiDB to panic [#53867](https://github.com/pingcap/tidb/issues/53867) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiDB might hang or return incorrect results when executing a query containing a correlated subquery and CTE [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue of data index inconsistency caused by retries during index addition [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - Fix the issue that an `out of range` error might occur when a small display width is specified for a column of the integer type [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `LOAD DATA ... REPLACE INTO` operation causes data inconsistency [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that `columnEvaluator` cannot identify the column references in the input chunk, which leads to `runtime error: index out of range` when executing SQL statements [#53713](https://github.com/pingcap/tidb/issues/53713) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue of invalid memory access that might occur when a Common Table Expression (CTE) has multiple data consumers and one consumer exits without reading any data [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - Fix the issue that when canceling a TTL task, the corresponding SQL is not killed forcibly [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TiDB panics when importing temporary tables using the `IMPORT INTO` statement [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the optimizer incorrectly estimates the number of rows as 1 when accessing a unique index with the query condition `column IS NULL` [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the query latency of stale reads increases, caused by information schema cache misses [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the `UPDATE` statement incorrectly updates values of the `ENUM` type [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing foreign keys [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TTL tasks are not canceled after the `tidb_ttl_job_enable` variable is disabled [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when an `UPDATE` or `DELETE` statement contains a recursive CTE, the statement might report an error or not take effect [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the `SUB_PART` value in the `INFORMATION_SCHEMA.STATISTICS` table is `NULL` [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the default timeout for querying the TiFlash system table is too short [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the value of the `default_collation_for_utf8mb4` variable does not work for the `SET NAMES` statement [#56439](https://github.com/pingcap/tidb/issues/56439) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that TTL internal coroutine might panic when you manually delete a timer in the `mysql.tidb_timer` table [#57112](https://github.com/pingcap/tidb/issues/57112) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that enabling acceleration of `ADD INDEX` and `CREATE INDEX` via `tidb_ddl_enable_fast_reorg` might lead to the `Duplicate entry` error [#49233](https://github.com/pingcap/tidb/issues/49233) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the index timestamp is set to `0` when adding indexes to large tables in a non-distributed manner [#57980](https://github.com/pingcap/tidb/issues/57980) @[lance6716](https://github.com/lance6716)

+ TiKV

    - Fix the issue that the configuration `resolved-ts.advance-ts-interval` does not take effect, causing the replication latency of TiCDC and Point-in-time recovery (PITR) to increase dramatically when TiKV restarts [#17107](https://github.com/tikv/tikv/issues/17107) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that some tasks experience high tail latency when triggering resource control [#17589](https://github.com/tikv/tikv/issues/17589) @[glorv](https://github.com/glorv)
    - Fix the issue that merging Regions might cause TiKV to panic in rare cases [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv)
    - Fix the issue that TiKV cannot report heartbeats to PD when the disk is stuck [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that when Raft and RocksDB are deployed on different disks, the slow disk detection does not work for the disk where RocksDB is located [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV might panic when a stale replica processes Raft snapshots, triggered by a slow split operation and immediate removal of the new replica [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)
    - Fix the issue that TiKV might panic when executing queries containing `RADIANS()` or `DEGREES()` functions [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that when a large number of transactions are queuing for lock release on the same key and the key is frequently updated, excessive pressure on deadlock detection might cause TiKV OOM issues [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the panic issue that occurs when read threads access outdated indexes in the MemTable of the Raft Engine [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the flow control issue that might occur after deleting large tables or partitions [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Fix the issue that the PD HTTP client retry logic might be ineffective [#8499](https://github.com/tikv/pd/issues/8499) @[JmPotato](https://github.com/JmPotato)
    - Upgrade the version of Gin Web Framework from v1.9.1 to v1.10.0 to fix potential security vulnerabilities [#8643](https://github.com/tikv/pd/issues/8643) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that PD cannot quickly re-elect a leader during etcd leader transition [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)
    - Fix the issue that setting `replication.strictly-match-label` to `true` causes TiFlash to fail to start [#8480](https://github.com/tikv/pd/issues/8480) @[rleungx](https://github.com/rleungx)
    - Fix the issue that `evict-leader-scheduler` fails to work properly when it is repeatedly created with the same Store ID [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - Fix the performance jitter issue caused by frequent creation of random number generator [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in hotspot cache [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - Fix the memory leak issue in label statistics [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that deleted resource groups still appear in the monitoring panel [#8716](https://github.com/tikv/pd/issues/8716) @[AndreMouche](https://github.com/AndreMouche)
    - Fix the issue that data race might occur in the scheduling server when a PD leader is switched in the microservice mode [#8538](https://github.com/tikv/pd/issues/8538) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that when using a wrong parameter in `evict-leader-scheduler`, PD does not report errors correctly and some schedulers are unavailable [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the resource group selector does not take effect on any panel [#56572](https://github.com/pingcap/tidb/issues/56572) @[glorv](https://github.com/glorv)

+ TiFlash

    - Fix the issue that TiFlash might panic due to spurious Region overlap check failures that occur when multiple Regions are concurrently applying snapshots [#9329](https://github.com/pingcap/tiflash/issues/9329) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that the `SUBSTRING()` function returns incorrect results when the second parameter is negative [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that some queries might report errors when late materialization is enabled [#9472](https://github.com/pingcap/tiflash/issues/9472) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that TiFlash fails to parse the table schema when the table contains Bit-type columns with a default value that contains invalid characters [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that some JSON functions unsupported by TiFlash are pushed down to TiFlash [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the sign in the result of the `CAST AS DECIMAL` function is incorrect in certain cases [#9301](https://github.com/pingcap/tiflash/issues/9301) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that read snapshots of TiFlash write nodes are not released in a timely manner in the disaggregated storage and compute architecture [#9298](https://github.com/pingcap/tiflash/issues/9298) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that the `SUBSTRING()` function does not support the `pos` and `len` arguments for certain integer types, causing query errors [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that when using the `CAST()` function to convert a string to a datetime with a time zone or invalid characters, the result is incorrect [#8754](https://github.com/pingcap/tiflash/issues/8754) @[solotzg](https://github.com/solotzg)
    - Fix the issue that `LPAD()` and `RPAD()` functions return incorrect results in some cases [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that querying new columns might return incorrect results under the disaggregated storage and compute architecture [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that logs might print out encrypted information [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - Fix the issue that snapshot backups based on AWS EBS might fail during the preparation phase, causing the backup to get stuck [#52049](https://github.com/pingcap/tidb/issues/52049) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the checkpoint path of backup and restore is incompatible with some external storage [#55265](https://github.com/pingcap/tidb/issues/55265) @[Leavrth](https://github.com/Leavrth)
        - Fix potential security vulnerabilities by upgrading the `k8s.io/api` library version [#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)
        - Fix the issue that PITR tasks might return the `Information schema is out of date` error when there are a large number of tables in the cluster but the actual data size is small [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - Fix the issue that the Resolved TS latency monitoring in the Puller module displays incorrect values [#11561](https://github.com/pingcap/tiflow/issues/11561) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that when `enable-table-across-nodes` is enabled, some Span replication tasks for a table might be lost during Region splits [#11675](https://github.com/pingcap/tiflow/issues/11675) @[wk989898](https://github.com/wk989898)
        - Fix the issue that the redo module fails to properly report errors [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly discards DDL tasks when the schema versions of DDL tasks become non-incremental during TiDB DDL owner changes [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that the **barrier-ts** monitoring metric for changefeed checkpoints might be inaccurate  [#11553](https://github.com/pingcap/tiflow/issues/11553) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the issue that multiple DM-master nodes might simultaneously become leaders, leading to data inconsistency [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
