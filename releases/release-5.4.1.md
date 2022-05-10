---
title: TiDB 5.4.1 Release Notes
---


# TiDB 5.4.1 Release Notes

Release Date: May xx, 2022

TiDB version: 5.4.1

## Compatibility changes

+ TiDB

    - note 1
    - note 2

+ TiKV

    - note 1
    - note 2

## Improvements

+ TiDB

    - (dup: release-6.0.0-dmr.md > Improvements> TiDB)- Support using the PointGet plan for queries that read the `_tidb_rowid` column [#31543](https://github.com/pingcap/tidb/issues/31543)
    - Add more debug information for `Apply` executor [#33887](https://github.com/pingcap/tidb/issues/33887)
    - Improve the `TopN` pruning logic for Analyze Version 2 used for 
collecting statistics [#34256](https://github.com/pingcap/tidb/issues/34256)
    - Support displaying multiple Kubernetes clusters in the Grafana dashboard [#32593](https://github.com/pingcap/tidb/issues/32593)

+ TiKV

    - Support displaying multiple Kubernetes clusters in the Grafana dashboard [#12104](https://github.com/tikv/tikv/issues/12104)

+ PD

    - Support displaying multiple Kubernetes clusters in the Grafana dashboard [#4673](https://github.com/tikv/pd/issues/4673)

+ TiFlash

    - Support displaying multiple Kubernetes clusters in the Grafana dashboard [#4129](https://github.com/pingcap/tiflash/issues/4129)

+ Tools

    + TiCDC

        - (dup: release-5.2.4.md > Improvements> Tools> TiCDC)- Support multiple Kubernetes clusters in Grafana dashboards [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - (dup: release-5.2.4.md > Improvements> Tools> TiCDC)- Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)

    + TiDB Data Migration (DM)

        - (dup: release-6.0.0-dmr.md > Improvements> Tools> TiDB Data Migration (DM))- Support Syncer using the working directory of the DM-worker rather than `/tmp` to write internal files, and cleaning the directory after the task is stopped [#4107](https://github.com/pingcap/tiflow/issues/4107)

## Bug Fixes

+ TiDB

    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that TiDB writes wrong data due to the wrong encoding of the `ENUM` or `SET` column [#32302](https://github.com/pingcap/tidb/issues/32302)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that the Merge Join operator gets wrong results in certain cases [#33042](https://github.com/pingcap/tidb/issues/33042)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that TiDB gets a wrong result when a correlated subquery returns a constant  [#32089](https://github.com/pingcap/tidb/issues/32089)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that TiDB gets the wrong result when using TiFlash to scan tables with empty range although TiFlash does not support reading tables with empty range yet [#33083](https://github.com/pingcap/tidb/issues/33083)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that the `MAX` or `MIN` function on the `ENUM` or `SET` column returns a wrong result when the new collation is enabled in TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix a bug that CTE might be blocked when a query reports errors [#31302](https://github.com/pingcap/tidb/issues/31302)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix wrong range calculation results for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix TiDB OOM when exporting data using ChunkRPC [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix the issue that `date_format` in TiDB handles `'\n'` in a MySQL-incompatible way [#32232](https://github.com/pingcap/tidb/issues/32232)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#31034](https://github.com/pingcap/tidb/issues/31034)
    - (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix a bug that `tidb_super_read_only` is not automatically enabled when `tidb_restricted_read_only` is enabled [#31745](https://github.com/pingcap/tidb/issues/31745)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix the issue that the `greatest` or `least` function with collation gets a wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix load data panic if the data is broken at an escape character [#31589](https://github.com/pingcap/tidb/issues/31589)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix the `invalid transaction` error when executing a query using index lookup join [#30468](https://github.com/pingcap/tidb/issues/30468)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    - (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix a bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix the issue that granting the `all` privilege might fail in clusters that are upgraded from v4.0 [#33588](https://github.com/pingcap/tidb/issues/33588)
    - Fix the issue of session panic that occurs when executing the prepared statement after table schema change with the MySQL binary protocol [#33509](https://github.com/pingcap/tidb/issues/33509)
    - Fix the issue that executing SQL statements that have the `compress()` expression with `tidb_enable_vectorized_expression` enabled will fail [#33397](https://github.com/pingcap/tidb/issues/33397)
    - Fix the issue of high CPU usage by the `reArrangeFallback` function [#30353](https://github.com/pingcap/tidb/issues/30353)
    - Fix the issue that the table attributes are not indexed when a new partition is added and the issue that the table range information are not updated when the partition changes [#33929](https://github.com/pingcap/tidb/issues/33929)
    - Fix a bug that the `TopN` statistical information of a table during the initialization is not correctly sorted  [#34216](https://github.com/pingcap/tidb/issues/34216)
    - Fix the error reporting that occurs when reading from the `INFORMATION_SCHEMA.ATTRIBUTES` table by skipping the unidentifiable table attributes [#33665](https://github.com/pingcap/tidb/issues/33665)
    - Fix a bug that even if `@@tidb_enable_parallel_apply` is set, the `Apply` operator is not paralleled when an `order` property exists [#34237](https://github.com/pingcap/tidb/issues/34237)
    - Fix a bug that `'0000-00-00 00:00:00'` can be inserted into a `datetime` column despite of the `NO_ZERO_DATE` sql_mode restriction [#34099](https://github.com/pingcap/tidb/issues/34099)
    - Fix the issue that the TiDB server might run out of memory when querying the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table. This issue can be triggered when you check slow queries on the Grafana dashboard. [#33893](https://github.com/pingcap/tidb/issues/33893)
    - Fix a bug that in the `NOWAIT` statement, a transaction being executed does not return immediately when encountering a lock [#32754](https://github.com/pingcap/tidb/issues/32754)
    - Fix a bug that causes a failure when creating a table with the `GBK` charset and `gbk_bin` collation [#31308](https://github.com/pingcap/tidb/issues/31308)
    - Fix a bug that when `enable-new-charset` is `on`, creating a `GBK` charset table with collation fails with the "Unknown character set" error [#31297](https://github.com/pingcap/tidb/issues/31297)

+ TiKV

    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the issue that TiKV panics and destroys peers unexpectedly because the target Region to be merged is invalid [#12232](https://github.com/tikv/tikv/issues/12232)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the issue of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the TiKV panic issue that occurs when the target peer is replaced with the peer that is destroyed without being initialized when merging a Region [#12048](https://github.com/tikv/tikv/issues/12048)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    - (dup: release-5.2.4.md > Improvements> TiKV)- Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the panic issue caused by deleting snapshot files when the peer status is `Applying` [#11746](https://github.com/tikv/tikv/issues/11746)
    - (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix panic invalid assertion in resource metering [#12234](https://github.com/tikv/tikv/issues/12234)
    - Fix the issue that slow score calculation is inaccurate in corner cases [#12254](https://github.com/tikv/tikv/issues/12254)
    - Fix the OOM issue caused by the resolved_ts module and add more metrics [#12159](https://github.com/tikv/tikv/issues/12159)
    - Fix that successfully committed optimistic transactions may report false WriteConflict on network errors [#34066](https://github.com/pingcap/tidb/issues/34066)
    - Fix panicking when replica read is enabled and there is a long time network condition [#12046](https://github.com/tikv/tikv/issues/12046)

+ PD

    - (dup: release-6.0.0-dmr.md > Bug fixes> PD)- Fix the issue that `Duration` fields of `dr-autosync` cannot be dynamically configured [#4651](https://github.com/tikv/pd/issues/4651)
    - Fix the issue that when there exists a store with more than a big free disk (2T for example) no balance operator generated even when one or more stores with its disk full [#4805](https://github.com/tikv/pd/issues/4805)
    - Fix the issue that in the metrics the label distribution has residual labels [#4825](https://github.com/tikv/pd/issues/4825)

+ TiFlash

    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the panic issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix possible metadata corruption caused by Region merge on a lagging Region peer [#4437](https://github.com/pingcap/tiflash/issues/4437)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the issue that a query containing `JOIN` might be hung if an error occurs [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the panic issue that occurs when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the overflow that occurs when casting `FLOAT` to `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue that expired data is recycled slowly [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix a bug that canceled MPP queries might cause tasks to hang forever when the local tunnel is enabled [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue of memory leak that occurs when a query is canceled [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue of memory leak that occurs when a query is canceled [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the potential issue of TiFlash panic when `Snapshot` is applied simultaneously with multiple DDL operations [#4072](https://github.com/pingcap/tiflash/issues/4072)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the issue that casting `INT` to `DECIMAL` might cause overflow [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the issue that the date format identifies `'\n'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - (dup: release-5.2.4.md > Bug fixes> TiFlash)- Fix the panic issue that occurs when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix potential data corruption in DTFiles [#4778](https://github.com/pingcap/tiflash/issues/4778)
    - Fix potential errors when querying on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - Fix a bug that TiFlash reports many "Keepalive watchdog fired" errors randomly [#4192](https://github.com/pingcap/tiflash/issues/4192)
    - Fix a bug that data not matching any region range remains on a TiFlash node [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - Fix a bug that empty segments cannot be merged after GC [#4511](https://github.com/pingcap/tiflash/issues/4511)

+ Tools

    + Backup & Restore (BR)
    
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> Backup & Restore (BR))- Fix a bug that causes the restore operation to fail when the encryption information is lost during backup retry [#32423](https://github.com/pingcap/tidb/issues/32423)
        - (dup: release-5.2.4.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that BR fails to back up RawKV [#32607](https://github.com/pingcap/tidb/issues/32607)
        - Fix duplicate primary keys when inserting a record into a table after incremental restoration [#33596](https://github.com/pingcap/tidb/issues/33596)
        - Fix a bug that BR incremental restore returns errors mistakenly due to DDL jobs with empty query [#33322](https://github.com/pingcap/tidb/issues/33322)
        - Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#31034](https://github.com/pingcap/tidb/issues/31034)
        - Fix the issue that BR does not retry enough times when Regions are not consistent during restoration [#33419](https://github.com/pingcap/tidb/issues/33419)
        - Fix the issue that BR might panic occasionally when merging small files is enabled [#33801](https://github.com/pingcap/tidb/issues/33801)
        - Fix the issue that schedulers do not resume after BR or TiDB Lightning exits abnormally [#33546](https://github.com/pingcap/tidb/issues/33546)

    + TiCDC

        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix incorrect metrics caused by owner changes [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix incorrect metrics caused by owner changes [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiCDC)- Fix the TiCDC panic issue that might occur because `Canal-JSON` does not support nil [#4736](https://github.com/pingcap/tiflow/issues/4736)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix a stability problem in workerpool used by Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiCDC)- Fix the TiCDC panic issue that might occur when `Canal-JSON` incorrectly handles `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiCDC)- Fix a bug that MySQL sink generates duplicated `replace` SQL statements when `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix the DML construct error caused by the `rename tables` DDL [#5059](https://github.com/pingcap/tiflow/issues/5059)
        - Fix the issue that in rare cases replication can be stuck if the owner is changed and the new scheduler is enabled (disabled by default) [#4963](https://github.com/pingcap/tiflow/issues/4963)
        - Fix the issue that the error ErrProcessorDuplicateOperations is reported when the new scheduler is enabled (disabled by default) [#4769](https://github.com/pingcap/tiflow/issues/4769)
        - Fix the issue that TiCDC fails to start when the first PD set in `--pd` is not available after TLS is enabled [#4777](https://github.com/pingcap/tiflow/issues/4777)
        - Fix the issue that the checkpoint metrics is missing when tables are being scheduled [#4714](https://github.com/pingcap/tiflow/issues/4714)

    + TiDB Lightning

        - (dup: release-5.2.4.md > Bug fixes> Tools> TiDB Lightning)- Fix the checksum error “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that TiDB Lightning gets stuck when it fails to check empty tables [#31797](https://github.com/pingcap/tidb/issues/31797)
        - (dup: release-5.2.4.md > Bug fixes> Tools> TiDB Lightning)- Fix a bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        - Fix the issue that Lightning precheck doesn't check local disk resources and cluster available.[#34213](https://github.com/pingcap/tidb/issues/34213)

    + TiDB Data Migration (DM)

        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that hundreds of "checkpoint has no change, skip sync flush checkpoint" print in the log and the replication is very slow [#4619](https://github.com/pingcap/tiflow/issues/4619)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix a bug that long varchars report an error `Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that execution errors of the update statement in safemode may cause the DM-worker panic [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - Fix the issue that manual execute the filtered DDL makes the task failed [#5272](https://github.com/pingcap/tiflow/issues/5272)
        - Fix a bug that no data is return by `query-status` when upstream doesn't turn on binlog [#5121](https://github.com/pingcap/tiflow/issues/5121)
        - Fix the issue that tracker panic when pk of downstream table orders behind [#5159](https://github.com/pingcap/tiflow/issues/5159)
        - Fix the issue that CPU usage may increased and print large amount logs when GTID enabled and task auto resumed. [#5063](https://github.com/pingcap/tiflow/issues/5063)