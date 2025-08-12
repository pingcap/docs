---
title: TiDB 7.5.5 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.5.
---

# TiDB 7.5.5 Release Notes

Release date: December 31, 2024

TiDB version: 7.5.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Compatibility changes

- Add a new system variable [`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512-and-v755) to limit the maximum speed of the ingest phase when adding indexes [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)
- Change the default value of the TiKV configuration item [`raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size) from `8192` to `16384` [#17101](https://github.com/tikv/tikv/issues/17101) @[Connor1996](https://github.com/Connor1996)

## Improvements

+ TiDB

    - Adjust estimation results from 0 to 1 for equality conditions that do not hit TopN when statistics are entirely composed of TopN and the modified row count in the corresponding table statistics is non-zero [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)

+ TiKV

    - Fix the issue that when Raft and RocksDB are deployed on different disks, the slow disk detection does not work for the disk where RocksDB is located [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add slow logs for peer and store messages [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - Optimize the jittery access delay when restarting TiKV due to waiting for the log to be applied, improving the stability of TiKV [#15874](https://github.com/tikv/tikv/issues/15874) @[LykxSassinator](https://github.com/LykxSassinator)

+ TiFlash

    - Mitigate the issue that TiFlash might panic due to updating certificates after TLS is enabled [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)
    - Improve the garbage collection speed of outdated data in the background for tables with clustered indexes [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Optimize the retry strategy for TiFlash compute nodes in the disaggregated storage and compute architecture to handle exceptions when downloading files from Amazon S3 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - Reduce unnecessary log printing during backup [#55902](https://github.com/pingcap/tidb/issues/55902) @[Leavrth](https://github.com/Leavrth)

    + TiDB Data Migration (DM)

        - Lower the log level for unrecognized MariaDB binlog events [#10204](https://github.com/pingcap/tiflow/issues/10204) @[dveeden](https://github.com/dveeden)

## Bug fixes

+ TiDB

    - Fix the issue that TiDB cannot resume Reorg DDL tasks from the previous progress after the DDL owner node is switched [#56506](https://github.com/pingcap/tidb/issues/56506) @[tangenta](https://github.com/tangenta)
    - Fix the issue that invalid `NULL` values can be inserted in non-strict mode (`sql_mode = ''`) [#56381](https://github.com/pingcap/tidb/issues/56381) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the data in the **Stats Healthy Distribution** panel of Grafana might be incorrect [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of illegal memory access that might occur when a Common Table Expression (CTE) has multiple data consumers and one consumer exits without reading any data [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - Fix the issue that existing TTL tasks are executed unexpectedly frequently in a cluster that is upgraded from v6.5 to v7.5 or later [#56539](https://github.com/pingcap/tidb/issues/56539) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TTL tasks are not canceled after the `tidb_ttl_job_enable` variable is disabled [#57404](https://github.com/pingcap/tidb/issues/57404) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the query latency of stale reads increases, caused by information schema cache misses [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that stale read does not strictly verify the timestamp of the read operation, resulting in a small probability of affecting the consistency of the transaction when an offset exists between the TSO and the real physical time [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the `AUTO_INCREMENT` field is not correctly set after importing data using the `IMPORT INTO` statement [#56476](https://github.com/pingcap/tidb/issues/56476) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that two DDL Owners might exist at the same time [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - Fix the issue that TTL might fail if TiKV is not selected as the storage engine [#56402](https://github.com/pingcap/tidb/issues/56402) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TiDB does not check the index length limitation when executing `ADD INDEX` [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that when canceling a TTL task, the corresponding SQL is not killed forcibly [#56511](https://github.com/pingcap/tidb/issues/56511) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that execution plan bindings cannot be created for the multi-table `DELETE` statement with aliases [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that when using `ANALYZE` to collect statistics for a table, if the table contains expression indexes of virtually generated columns, the execution reports an error [#57079](https://github.com/pingcap/tidb/issues/57079) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing Placement Rules [#54961](https://github.com/pingcap/tidb/issues/54961) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that when parsing a database name in CTE, it returns a wrong database name [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the `INSERT ... ON DUPLICATE KEY` statement is not compatible with `mysql_insert_id` [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that improper use of metadata locks might lead to writing anomalous data when using the plan cache under certain circumstances [#53634](https://github.com/pingcap/tidb/issues/53634) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the performance is unstable when adding indexes using Global Sort [#54147](https://github.com/pingcap/tidb/issues/54147) @[tangenta](https://github.com/tangenta)
    - Fix the issue that Plan Replayer might report an error when importing a table structure containing foreign keys [#56456](https://github.com/pingcap/tidb/issues/56456) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that using the `RANGE COLUMNS` partition function and the `utf8mb4_0900_ai_ci` collation at the same time could result in incorrect query results [#57261](https://github.com/pingcap/tidb/issues/57261) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that using subqueries after the `NATURAL JOIN` or `USING` clause might result in errors [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - Fix the issue that TTL tasks cannot be canceled when there is a write conflict [#56422](https://github.com/pingcap/tidb/issues/56422) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that if a CTE contains the `ORDER BY`, `LIMIT`, or `SELECT DISTINCT` clause and is referenced by the recursive part of another CTE, it might be incorrectly inlined and result in an execution error [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the `UPDATE` statement incorrectly updates values of the `ENUM` type [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - Fix the issue that executing `RECOVER TABLE BY JOB JOB_ID;` might cause TiDB to panic [#55113](https://github.com/pingcap/tidb/issues/55113) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the `read_from_storage` hint might not take effect when the query has an available Index Merge execution plan [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `INDEX_HASH_JOIN` might hang during an abnormal exit [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that querying system tables related to the Distributed eXecution Framework (DXF) might lead to upgrade failures [#49263](https://github.com/pingcap/tidb/issues/49263) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that the DDL internal transaction error `GC life time is shorter than transaction duration` causes index addition to fail [#57043](https://github.com/pingcap/tidb/issues/57043) @[tangenta](https://github.com/tangenta)
    - Fix the issue that when executing `EXCHANGE PARTITION` and encountering invalid rows, InfoSchema is fully loaded and the error `failed to load schema diff` is reported [#56685](https://github.com/pingcap/tidb/issues/56685) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that collation is not handled correctly when `tidb_ddl_enable_fast_reorg` and `new_collations_enabled_on_first_bootstrap` are enabled, resulting in inconsistent data indexes [#58036](https://github.com/pingcap/tidb/issues/58036) @[djshow832](https://github.com/djshow832)
    - Fix the issue that data indexes are inconsistent because plan cache uses the wrong schema when adding indexes [#56733](https://github.com/pingcap/tidb/issues/56733) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that executing `ALTER TABLE TIFLASH REPLICA` during upgrade causes the TiDB node to crash [#57863](https://github.com/pingcap/tidb/issues/57863) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the performance of querying `INFORMATION_SCHEMA.columns` degrades [#58184](https://github.com/pingcap/tidb/issues/58184) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the default timeout for querying the TiFlash system table is too short [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the value of the `default_collation_for_utf8mb4` variable does not work for the `SET NAMES` statement [#56439](https://github.com/pingcap/tidb/issues/56439) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that TTL internal coroutine might panic when you manually delete a timer in the `mysql.tidb_timer` table [#57112](https://github.com/pingcap/tidb/issues/57112) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that when converting a normal table to a partitioned table using the `ALTER TABLE` statement, insufficient checks might result in incorrect data [#55721](https://github.com/pingcap/tidb/issues/55721) @[mjonss](https://github.com/mjonss)
    - Fix the issue that when setting `tidb_gogc_tuner_max_value` and `tidb_gogc_tuner_min_value`, if the maximum value is null, an incorrect warning message occurs [#57889](https://github.com/pingcap/tidb/issues/57889) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the potential data race issue that might occur in TiDB's internal coroutine [#57798](https://github.com/pingcap/tidb/issues/57798) [#56053](https://github.com/pingcap/tidb/issues/56053) @[fishiu](https://github.com/fishiu) @[tiancaiamao](https://github.com/tiancaiamao)
    - Update `golang-jwt` and `jwt` to prevent potential security risks [#57135](https://github.com/pingcap/tidb/issues/57135) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that concurrent writes might result in duplicate data when converting a table with clustered indexes to a partitioned table using the `ALTER TABLE` statement [#57510](https://github.com/pingcap/tidb/issues/57510) @[mjonss](https://github.com/mjonss)

+ TiKV

    - Fix the issue that merging Regions might cause TiKV to panic in rare cases [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv)
    - Fix the issue that when Raft and RocksDB are deployed on different disks, the slow disk detection does not work for the disk where RocksDB is located [#17884](https://github.com/tikv/tikv/issues/17884) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that the output of jprof is not correctly captured and processed when the `log-file` parameter is not specified [#17607](https://github.com/tikv/tikv/issues/17607) @[Hexilee](https://github.com/Hexilee)
    - Fix the issue that latency might increase when hibernated Regions are awake [#17101](https://github.com/tikv/tikv/issues/17101) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that TiKV might panic when executing queries containing `RADIANS()` or `DEGREES()` functions [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - Fix the panic issue that occurs when read threads access outdated indexes in the MemTable of the Raft Engine [#17383](https://github.com/tikv/tikv/issues/17383) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that when a large number of transactions are queuing for lock release on the same key and the key is frequently updated, excessive pressure on deadlock detection might cause TiKV OOM issues [#17394](https://github.com/tikv/tikv/issues/17394) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that write jitter might occur when all hibernated Regions are awakened [#17101](https://github.com/tikv/tikv/issues/17101) @[hhwyt](https://github.com/hhwyt)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that CPU profiling flag is not reset correctly when an error occurs [#17234](https://github.com/tikv/tikv/issues/17234) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that large batch writes cause performance jitter when `raft-entry-max-size` is set too high [#17701](https://github.com/tikv/tikv/issues/17701) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that improper error handling in the conflict detection interface of the import module might cause TiKV to panic [#17830](https://github.com/tikv/tikv/issues/17830) @[joccau](https://github.com/joccau)

+ PD

    - Fix the issue that when creating `evict-leader-scheduler` or `grant-leader-scheduler` encounters an error, the error message is not returned to pd-ctl [#8759](https://github.com/tikv/pd/issues/8759) @[okJiang](https://github.com/okJiang)
    - Fix the issue that PD cannot quickly re-elect a leader during etcd leader transition [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in label statistics [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that `evict-leader-scheduler` fails to work properly when it is repeatedly created with the same Store ID [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - Fix the issue that slots are not fully deleted in a resource group client, which causes the number of the allocated tokens to be less than the specified value [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that when using a wrong parameter in `evict-leader-scheduler`, PD does not report errors correctly and some schedulers are unavailable [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in hotspot cache [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - Fix the performance jitter issue caused by frequent creation of random number generator [#8674](https://github.com/tikv/pd/issues/8674) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the TiFlash panic issue when TiFlash encounters conflicts during concurrent DDL execution [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that `LPAD()` and `RPAD()` functions return incorrect results in some cases [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `SUBSTRING()` function returns incorrect results when the second parameter is negative [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash fails to parse the table schema when the table contains Bit-type columns with a default value that contains invalid characters [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that querying new columns might return incorrect results under the disaggregated storage and compute architecture [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that when resuming from a checkpoint after data restore fails, an error `the target cluster is not fresh` occurs [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that log backups cannot resolve residual locks promptly, causing the checkpoint to fail to advance [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - Fix the issue that logs might print out encrypted information [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the `TestStoreRemoved` test case is unstable [#52791](https://github.com/pingcap/tidb/issues/52791) @[YuJuncen](https://github.com/YuJuncen)
        - Fix potential security vulnerabilities by upgrading the `k8s.io/api` library version [#57790](https://github.com/pingcap/tidb/issues/57790) @[BornChanger](https://github.com/BornChanger)
        - Fix the issue that PITR tasks might return the `Information schema is out of date` error when there are a large number of tables in the cluster but the actual data size is small [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC

        - Fix the issue that TiCDC might report an error when replicating a `TRUNCATE TABLE` DDL on a table without valid index [#11765](https://github.com/pingcap/tiflow/issues/11765) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the `tableID` for partitioned tables is not correctly set in Simple Protocol messages [#11846](https://github.com/pingcap/tiflow/issues/11846) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the redo module fails to properly report errors [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly discards DDL tasks when the schema versions of DDL tasks become non-incremental during TiDB DDL owner changes [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM)

        - Fix the issue that automatically generated IDs in a table might have significant jumps after data import in physical import mode [#11768](https://github.com/pingcap/tiflow/issues/11768) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that the pre-check of `start-task` fails when both TLS and `shard-mode` are configured [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)
        - Fix the issue that connecting to MySQL 8.0 fails when the password length exceeds 19 characters [#11603](https://github.com/pingcap/tiflow/issues/11603) @[fishiu](https://github.com/fishiu)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning fails to receive oversized messages sent from TiKV [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - Fix the issue that the `AUTO_INCREMENT` value is set too high after importing data using the physical import mode [#56814](https://github.com/pingcap/tidb/issues/56814) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that TiDB Lightning does not automatically retry when encountering `Lock wait timeout` errors during metadata updates [#53042](https://github.com/pingcap/tidb/issues/53042) @[guoshouyan](https://github.com/guoshouyan)
        - Fix the issue that the performance degrades when importing data from a cloud storage in high-concurrency scenarios [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - Fix the issue that TiDB Lightning might get stuck for a long time during the preparation phase when importing a large number of Parquet files [#56104](https://github.com/pingcap/tidb/issues/56104) @[zeminzhou](https://github.com/zeminzhou)
        - Fix the issue that the error report output is truncated when importing data using TiDB Lightning [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - Fix the issue that Dumpling fails to retry properly when receiving a 503 error from Google Cloud Storage (GCS) [#56127](https://github.com/pingcap/tidb/issues/56127) @[OliverS929](https://github.com/OliverS929)
