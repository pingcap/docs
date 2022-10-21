---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 Release Notes

Release date: xx xx, 2022

TiDB version: 6.1.2

## Compatibility changes

## Improvements

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @wjhuang2016**-->

    - Allow setting placement rules and TiFlash replicas at the same time in one table [#37171](https://github.com/pingcap/tidb/issues/37171)

    <!--execution **owner: @zanmato1984**-->

    <!--transaction **owner: @cfzjywxk**-->

    <!--planner **owner: @fixdb**-->

+ TiKV **owner: @ethercflow TW: @Oreoxmt**

    - (dup) Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054)
    - (dup) Support configuring the RocksDB write stall settings to a value smaller than the flow control threshold [#13467](https://github.com/tikv/tikv/issues/13467)

+ PD **owner: @nolouch TW: @Oreoxmt**

+ TiFlash

<!--compute **owner: @zanmato1984**-->

<!--storage **owner: @flowbehappy**-->

+ Tools

    + TiDB Lightning **owner: @niubell TW: @shichun-0415**

        - Add retryable errors during checksum to improve robustness [#37690](https://github.com/pingcap/tidb/issues/37690)

    + TiDB Data Migration (DM) **owner: @niubell**

    + TiCDC **owner: @nongfushanquan**

        - Enhance the performance of the region worker by handling resolved TS in a batch [#7078](https://github.com/pingcap/tiflow/issues/7078)

    + Backup & Restore (BR) **owner: @3pointer**

    + Dumpling

## Bug fixes

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @wjhuang2016**-->

    - Fix the issue that database-level privileges are incorrectly cleaned up [#38363](https://github.com/pingcap/tidb/issues/38363)
    - (dup) Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) Fix the issue that when one PD node goes down, the query of `information_schema.TIKV_REGION_STATUS` fails due to not retrying other PD nodes [#35708](https://github.com/pingcap/tidb/issues/35708)
    - (dup) Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903)

    <!--execution **owner: @zanmato1984**-->

    - (dup) Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)

    <!--transaction **owner: @cfzjywxk**-->

    - Fix the issue that the Region cache is not cleaned up in time when the Region is merged [#37141](https://github.com/pingcap/tidb/issues/37141)
    - Fix the issue that the KV client sends unnecessary ping messages [#36861](https://github.com/pingcap/tidb/issues/36861)
    - (dup) Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373)

    <!--planner **owner: @fixdb**-->

    - Fix the issue that `GROUP CONCAT` with `ORDER BY` might fail when the `ORDER BY` clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - (dup) Fix the issue that `Can't find column` is reported if an `UPDATE` statement contains common table expressions (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758)
    - (dup) Fix the issue that the `EXECUTE` might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)

+ TiKV **owner: @ethercflow TW: @Oreoxmt**

    - Fix the issue that the snapshot data might be incomplete caused by batch snapshot across Regions [#13553](https://github.com/tikv/tikv/issues/13553)
    - (dup) Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - (dup) Fix the issue that causes permission denied error when TiKV gets an error from the web identity provider and fails back to the default provider [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) Fix the issue that the TiKV service is unavailable for several minutes when a TiKV instance is in an isolated network environment [#12966](https://github.com/tikv/tikv/issues/12966)

+ PD **owner: @nolouch TW: @Oreoxmt**

    - Fix the issue that the statistics of the Region tree might be inaccurate [#5318](https://github.com/tikv/pd/issues/5318)
    - (dup) Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) Fix the issue that unhealthy Region might cause PD panic [#5491](https://github.com/tikv/pd/issues/5491)

+ TiFlash **TW: @Oreoxmt**

    <!--compute **owner: @zanmato1984**-->

    - (dup) Fix the issue that a window function might cause TiFlash to crash when the query is canceled [#5814](https://github.com/pingcap/tiflash/issues/5814)

    <!--storage **owner: @flowbehappy**-->

    - Fix the issue that I/O Limiter might incorrectly throttle the I/O throughput of query requests after bulk writes, which reduces the query performance [#5801](https://github.com/pingcap/tiflash/issues/5801)
    - (dup) Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell TW: @shichun-0415**

        - Fix panic of TiDB Lightning caused by invalid metric counters [#37338](https://github.com/pingcap/tidb/issues/37338)

    + TiDB Data Migration (DM) **owner: @niubell TW: @shichun-0415**

        - Fix the issue that upstream table structure information is lost when DM tasks enter the sync unit and are interrupted [#7159](https://github.com/pingcap/tiflow/issues/7159)
        - Fix large transaction errors by splitting SQL statements when saving checkpoints [#5010](https://github.com/pingcap/tiflow/issues/5010)
        - Fix the issue that DM precheck requires the `SELECT` privilege on `INFORMATION_SCHEMA` [#7317](https://github.com/pingcap/tiflow/issues/7317)
        - Fix the issue that DM-worker triggers a deadlock error after running DM tasks with fast/full validators [#7241](https://github.com/pingcap/tiflow/issues/7241)
        - (dup) Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028)

    + TiCDC **owner: @nongfushanquan TW: @hfxsd**

        - Fix the issue that the cdc server might panic if it receives an HTTP request before the cdc server fully starts [#6838](https://github.com/pingcap/tiflow/issues/6838)
        - Fix the log flooding issue during upgrade [#7235](https://github.com/pingcap/tiflow/issues/7235)
        - Fix the issue that changefeed's redo log files might be deleted by mistake [#6413](https://github.com/pingcap/tiflow/issues/6413)
        - Fix the issue that TiCDC might become unavailable when too many operations in an etcd transaction are committed  [#7131](https://github.com/pingcap/tiflow/issues/7131)
        - Fix the issue that data inconsistency might occur when non-reentrant DDL statements in redo logs are executed twice [#6927](https://github.com/pingcap/tiflow/issues/6927)

    + Backup & Restore (BR) **owner: @3pointer TW: @shichun-0415**

        - (dup) Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549)
        - (dup) Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469)

    + Dumpling
