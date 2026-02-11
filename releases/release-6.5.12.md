---
title: TiDB 6.5.12 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.12.
---

# TiDB 6.5.12 Release Notes

Release date: February 27, 2025

TiDB version: 6.5.12

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## Compatibility changes

- Support the openEuler 22.03 LTS SP3/SP4 operating system. For more information, see [OS and platform requirements](https://docs.pingcap.com/tidb/v6.5/hardware-and-software-requirements#os-and-platform-requirements).
- Set a default limit of 2048 for DDL historical tasks retrieved through the [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-6.5/docs/tidb_http_api.md) to prevent OOM issues caused by excessive historical tasks [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
- Add a new system variable [`tidb_ddl_reorg_max_write_speed`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_ddl_reorg_max_write_speed-new-in-v6512) to limit the maximum speed of the ingest phase when adding indexes [#57156](https://github.com/pingcap/tidb/issues/57156) @[CbcWestwolf](https://github.com/CbcWestwolf)

## Improvements

+ TiDB

    - Enhance the validity check for read timestamps [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiKV

    - Add the detection mechanism for invalid `max_ts` updates [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)

+ TiFlash

    - Improve the garbage collection speed of outdated data in the background for tables with clustered indexes [#9529](https://github.com/pingcap/tiflash/issues/9529) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Add a check to verify whether the target cluster is an empty cluster for full restore [#35744](https://github.com/pingcap/tidb/issues/35744) @[3pointer](https://github.com/3pointer)
        - Add a check to verify whether the target cluster contains a table with the same name for non-full restore [#55087](https://github.com/pingcap/tidb/issues/55087) @[RidRisR](https://github.com/RidRisR)
        - Except for the `br log restore` subcommand, all other `br log` subcommands support skipping the loading of the TiDB `domain` data structure to reduce memory consumption [#52088](https://github.com/pingcap/tidb/issues/52088) @[Leavrth](https://github.com/Leavrth)
        - Disable the table-level checksum calculation during full backups by default (`--checksum=false`) to improve backup performance [#56373](https://github.com/pingcap/tidb/issues/56373) @[Tristan1900](https://github.com/Tristan1900)

    + TiDB Lightning

        - Add a row width check when parsing CSV files to prevent OOM issues [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## Bug fixes

+ TiDB

    - Fix the issue that using subqueries after the `NATURAL JOIN` or `USING` clause might result in errors [#53766](https://github.com/pingcap/tidb/issues/53766) @[dash12653](https://github.com/dash12653)
    - Fix the issue that the `CAST` function does not support explicitly setting the character set [#55677](https://github.com/pingcap/tidb/issues/55677) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `LOAD DATA ... REPLACE INTO` operation causes data inconsistency [#56408](https://github.com/pingcap/tidb/issues/56408) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that TiDB does not check the index length limitation when executing `ADD INDEX` [#56930](https://github.com/pingcap/tidb/issues/56930) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue of illegal memory access that might occur when a Common Table Expression (CTE) has multiple data consumers and one consumer exits without reading any data [#55881](https://github.com/pingcap/tidb/issues/55881) @[windtalker](https://github.com/windtalker)
    - Fix the issue that some predicates might be lost when constructing `IndexMerge` [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that converting data from the `BIT` type to the `CHAR` type might cause TiKV panics [#56494](https://github.com/pingcap/tidb/issues/56494) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that using variables or parameters in the `CREATE VIEW` statement does not report errors [#53176](https://github.com/pingcap/tidb/issues/53176) @[mjonss](https://github.com/mjonss)
    - Fix the issue that unreleased session resources might lead to memory leaks [#56271](https://github.com/pingcap/tidb/issues/56271) @[lance6716](https://github.com/lance6716)
    - Fix the issue that executing `ADD INDEX` might fail after modifying the PD member in the distributed execution framework [#48680](https://github.com/pingcap/tidb/issues/48680) @[lance6716](https://github.com/lance6716)
    - Fix the issue that using `ORDER BY` when querying `cluster_slow_query table` might generate unordered results [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that stale read does not strictly verify the timestamp of the read operation, resulting in a small probability of affecting the consistency of the transaction when an offset exists between the TSO and the real physical time [#56809](https://github.com/pingcap/tidb/issues/56809) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the performance of querying `INFORMATION_SCHEMA.columns` degrades [#58184](https://github.com/pingcap/tidb/issues/58184) @[lance6716](https://github.com/lance6716)
    - Fix the issue that the `INSERT ... ON DUPLICATE KEY` statement is not compatible with `mysql_insert_id` [#55965](https://github.com/pingcap/tidb/issues/55965) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the optimizer incorrectly estimates the number of rows as 1 when accessing a unique index with the query condition `column IS NULL` [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that part of the memory of the `IndexLookUp` operator is not tracked [#56440](https://github.com/pingcap/tidb/issues/56440) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the potential data race issue that might occur in TiDB's internal coroutine [#57798](https://github.com/pingcap/tidb/issues/57798) [#56053](https://github.com/pingcap/tidb/issues/56053) @[fishiu](https://github.com/fishiu) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `read_from_storage` hint might not take effect when the query has an available Index Merge execution plan [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that execution plan bindings cannot be created for the multi-table `DELETE` statement with aliases [#56726](https://github.com/pingcap/tidb/issues/56726) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that `INDEX_HASH_JOIN` might hang during an abnormal exit [#54055](https://github.com/pingcap/tidb/issues/54055) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that two DDL Owners might exist at the same time [#54689](https://github.com/pingcap/tidb/issues/54689) @[joccau](https://github.com/joccau)
    - Fix the issue that when querying the `information_schema.cluster_slow_query` table, if the time filter is not added, only the latest slow log file is queried [#56100](https://github.com/pingcap/tidb/issues/56100) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that `duplicate entry` might occur when adding unique indexes [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the error message is incorrect in certain type conversion errors [#41730](https://github.com/pingcap/tidb/issues/41730) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the CTE defined in `VIEW` is incorrectly inlined [#56582](https://github.com/pingcap/tidb/issues/56582) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the `UPDATE` statement incorrectly updates values of the `ENUM` type [#56832](https://github.com/pingcap/tidb/issues/56832) @[xhebox](https://github.com/xhebox)
    - Fix the issue that executing the `UPDATE` statement after adding a `DATE` column results in the error `Incorrect date value: '0000-00-00'` in some cases [#59047](https://github.com/pingcap/tidb/issues/59047) @[mjonss](https://github.com/mjonss)
    - Fix the issue that in the Prepare protocol, an error occurs when the client uses a non-UTF8 character set [#58870](https://github.com/pingcap/tidb/issues/58870) @[xhebox](https://github.com/xhebox)
    - Fix the issue that querying temporary tables might trigger unexpected TiKV requests in some cases [#58875](https://github.com/pingcap/tidb/issues/58875) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `ONLY_FULL_GROUP_BY` setting does not take effect on statements in views [#53175](https://github.com/pingcap/tidb/issues/53175) @[mjonss](https://github.com/mjonss)
    - Fix the issue that querying partitioned tables using an `IN` condition containing a mismatched value type and a type conversion error leads to incorrect query results [#54746](https://github.com/pingcap/tidb/issues/54746) @[mjonss](https://github.com/mjonss)
    - Fix the issue that querying slow logs might fail when certain fields contain empty values [#58147](https://github.com/pingcap/tidb/issues/58147) @[yibin87](https://github.com/yibin87)
    - Fix the issue that the `RADIANS()` function computes values in an incorrect order [#57671](https://github.com/pingcap/tidb/issues/57671) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the default value of the `BIT` column is incorrect [#57301](https://github.com/pingcap/tidb/issues/57301) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that an inline error might occur if a CTE contains `ORDER BY`, `LIMIT`, or `SELECT DISTINCT` clauses and is referenced by the recursive part of another CTE [#56603](https://github.com/pingcap/tidb/issues/56603) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the timeout that occurs when loading statistics synchronically might not be handled correctly [#57710](https://github.com/pingcap/tidb/issues/57710) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that an incorrect database name might be returned when parsing the database name in a CTE [#54582](https://github.com/pingcap/tidb/issues/54582) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that TiDB might panic during startup due to invalid data binding [#58016](https://github.com/pingcap/tidb/issues/58016) @[qw4990](https://github.com/qw4990)
    - Fix the issue that cost estimation might generate invalid INF/NaN values in certain extreme cases, which could lead to incorrect Join Reorder results [#56704](https://github.com/pingcap/tidb/issues/56704) @[winoros](https://github.com/winoros)
    - Fix the issue that loading statistics manually might fail when the statistics file contains null values [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that creating two views with the same name does not report an error [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that when a virtual generated column's dependencies contain a column with the `ON UPDATE` attribute, the data of the updated row and its index data might be inconsistent [#56829](https://github.com/pingcap/tidb/issues/56829) @[joechenrh](https://github.com/joechenrh)
    - Fix the issue that the `INFORMATION_SCHEMA.TABLES` system table returns incorrect results [#57345](https://github.com/pingcap/tidb/issues/57345) @[tangenta](https://github.com/tangenta)

+ TiKV

    - Fix the issue that Follower Read might read stale data [#17018](https://github.com/tikv/tikv/issues/17018) @[glorv](https://github.com/glorv)
    - Fix the issue that TiKV might panic when destroying a peer [#18005](https://github.com/tikv/tikv/issues/18005) @[glorv](https://github.com/glorv)
    - Fix the issue that time rollback might cause abnormal RocksDB flow control, leading to performance jitter [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that disk stalls might prevent leader migration, leading to performance jitter [#17363](https://github.com/tikv/tikv/issues/17363) @[hhwyt](https://github.com/hhwyt)
    - Fix the issue that the latest written data might not be readable when only one-phase commit (1PC) is enabled and Async Commit is not enabled [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    - Fix the issue that a deadlock might occur when GC Worker is under heavy load [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the **Storage async write duration** monitoring metric on the TiKV panel in Grafana is inaccurate [#17579](https://github.com/tikv/tikv/issues/17579) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV might panic when executing queries containing `RADIANS()` or `DEGREES()` functions [#17852](https://github.com/tikv/tikv/issues/17852) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that merging Regions might cause TiKV to panic in rare cases [#17840](https://github.com/tikv/tikv/issues/17840) @[glorv](https://github.com/glorv)
    - Fix the issue that the leader could not be quickly elected after Region split [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that encoding might fail when processing GBK/GB18030 encoded data [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)

+ PD

    - Fix the issue that memory leaks might occur when allocating TSOs [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the `tidb_enable_tso_follower_proxy` system variable might not take effect [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    - Fix a potential issue that might cause PD to panic [#8915](https://github.com/tikv/pd/issues/8915) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that memory leaks might occur in long-running clusters [#9047](https://github.com/tikv/pd/issues/9047) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that a PD node might still generate TSOs even when it is not the Leader [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    - Fix the issue that Region syncer might not exit in time during the PD Leader switch [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    - Fix the issue that when creating `evict-leader-scheduler` or `grant-leader-scheduler` encounters an error, the error message is not returned to pd-ctl [#8759](https://github.com/tikv/pd/issues/8759) @[okJiang](https://github.com/okJiang)
    - Fix the memory leak issue in hotspot cache [#8698](https://github.com/tikv/pd/issues/8698) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that PD's Region API cannot be requested when a large number of Regions exist [#55872](https://github.com/pingcap/tidb/issues/55872) @[rleungx](https://github.com/rleungx)
    - Fix the issue that `evict-leader-scheduler` fails to work properly when it is repeatedly created with the same Store ID [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)
    - Upgrade the version of Gin Web Framework from v1.9.1 to v1.10.0 to fix potential security vulnerabilities [#8643](https://github.com/tikv/pd/issues/8643) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that when using a wrong parameter in `evict-leader-scheduler`, PD does not report errors correctly and some schedulers are unavailable [#8619](https://github.com/tikv/pd/issues/8619) @[rleungx](https://github.com/rleungx)
    - Fix the memory leak issue in label statistics [#8700](https://github.com/tikv/pd/issues/8700) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that TiDB Dashboard cannot read PD `trace` data correctly [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - Fix the memory leak issue in Region statistics [#8710](https://github.com/tikv/pd/issues/8710) @[rleungx](https://github.com/rleungx)
    - Fix the issue that PD cannot quickly re-elect a leader during etcd leader transition [#8823](https://github.com/tikv/pd/issues/8823) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that the `SUBSTRING()` function does not support the `pos` and `len` arguments for certain integer types, causing query errors [#9473](https://github.com/pingcap/tiflash/issues/9473) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that some JSON functions unsupported by TiFlash are pushed down to TiFlash [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `SUBSTRING()` function returns incorrect results when the second parameter is negative [#9604](https://github.com/pingcap/tiflash/issues/9604) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that `LPAD()` and `RPAD()` functions return incorrect results in some cases [#9465](https://github.com/pingcap/tiflash/issues/9465) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that executing `DROP TABLE` on large tables might cause TiFlash OOM [#9437](https://github.com/pingcap/tiflash/issues/9437) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash fails to start due to a division by zero error when retrieving the number of CPU cores [#9212](https://github.com/pingcap/tiflash/issues/9212) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiFlash might maintain high memory usage after importing large amounts of data [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that BR fails to restore due to getting the `rpcClient is idle` error when sending requests to TiKV [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        - Fix the issue that the `status` field is missing in the result when querying log backup tasks using `br log status --json` [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that PD Leader I/O latency during log backup might increase checkpoint latency [#58574](https://github.com/pingcap/tidb/issues/58574) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the `tiup br restore` command omits checking whether the target cluster table already exists during database or table restoration, which might overwrite existing tables [#58168](https://github.com/pingcap/tidb/issues/58168) @[RidRisR](https://github.com/RidRisR)
        - Fix the issue that log backup might unexpectedly enter a paused state when the advancer owner switches [#58031](https://github.com/pingcap/tidb/issues/58031) @[3pointer](https://github.com/3pointer)
        - Fix the issue that log backups cannot resolve residual locks promptly, causing the checkpoint to fail to advance [#57134](https://github.com/pingcap/tidb/issues/57134) @[3pointer](https://github.com/3pointer)
        - Fix the issue that BR integration test cases are unstable, and add a new test case to simulate snapshot or log backup file corruption [#53835](https://github.com/pingcap/tidb/issues/53835) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that logs might print out encrypted information [#57585](https://github.com/pingcap/tidb/issues/57585) @[kennytm](https://github.com/kennytm)
        - Fix the issue that PITR tasks might return the `Information schema is out of date` error when there are a large number of tables in the cluster but the actual data size is small [#57743](https://github.com/pingcap/tidb/issues/57743) @[Tristan1900](https://github.com/Tristan1900)

    + TiCDC
    
        - Fix the issue that TiCDC uses incorrect table names for filtering during `RENAME TABLE` operations [#11946](https://github.com/pingcap/tiflow/issues/11946) @[wk989898](https://github.com/wk989898)
        - Fix the issue that TiCDC reports errors when replicating `default NULL` SQL statements via the Avro protocol [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        - Fix the issue that TiCDC fails to properly connect to PD after PD scale-in [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that Initial Scan is not canceled after the changefeed is stopped or deleted [#11638](https://github.com/pingcap/tiflow/issues/11638) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that after the default value of a newly added column in the upstream is changed from `NOT NULL` to `NULL`, the default values of that column in the downstream are incorrect [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        - Fix the issue that using the `--overwrite-checkpoint-ts` parameter in the `changefeed pause` command might cause the changefeed to be stuck [#12055](https://github.com/pingcap/tiflow/issues/12055) @[hongyunyan](https://github.com/hongyunyan)
        - Fix the issue that TiCDC might panic when replicating `CREATE TABLE IF NOT EXISTS` or `CREATE DATABASE IF NOT EXISTS` statements [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC might report an error when replicating a `TRUNCATE TABLE` DDL on a table without valid index [#11765](https://github.com/pingcap/tiflow/issues/11765) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC mistakenly discards DDL tasks when the schema versions of DDL tasks become non-incremental during TiDB DDL owner changes [#11714](https://github.com/pingcap/tiflow/issues/11714) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that the changefeed might get stuck after new TiKV nodes are added to the cluster [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that out-of-order messages resent by the Sarama client cause Kafka message order to be incorrect [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the Resolved TS latency monitoring in the Puller module displays incorrect values [#11561](https://github.com/pingcap/tiflow/issues/11561) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that the redo module fails to properly report errors [#11744](https://github.com/pingcap/tiflow/issues/11744) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - Fix the issue that multiple DM-master nodes might simultaneously become leaders, leading to data inconsistency [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that connecting to MySQL 8.0 fails when the password length exceeds 19 characters [#11603](https://github.com/pingcap/tiflow/issues/11603) @[fishiu](https://github.com/fishiu)
        - Fix the issue that the pre-check of `start-task` fails when both TLS and `shard-mode` are configured [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    + TiDB Lightning

        - Fix the issue that logs are not properly desensitized [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that the lack of caching in the encoding phase causes performance regression [#56705](https://github.com/pingcap/tidb/issues/56705) @[OliverS929](https://github.com/OliverS929)
        - Fix the issue that the performance degrades when importing data from a cloud storage in high-concurrency scenarios [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        - Fix the issue that TiDB Lightning does not automatically retry when encountering `Lock wait timeout` errors during metadata updates [#53042](https://github.com/pingcap/tidb/issues/53042) @[guoshouyan](https://github.com/guoshouyan)
        - Fix the issue that TiDB Lightning fails to receive oversized messages sent from TiKV [#56114](https://github.com/pingcap/tidb/issues/56114) @[fishiu](https://github.com/fishiu)
        - Fix the issue that the error report output is truncated when importing data using TiDB Lightning [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)

    + Dumpling

        - Fix the issue that Dumpling fails to retry properly when receiving a 503 error from Google Cloud Storage (GCS) [#56127](https://github.com/pingcap/tidb/issues/56127) @[OliverS929](https://github.com/OliverS929)
