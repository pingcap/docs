---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 Release Notes

Release date: xx xx, 2022

TiDB version: 6.1.2

## Compatibility changes

## Improvements

+ TiDB

    <!--sql-infra **owner: @wjhuang2016**-->

    - Allow setting Placement Rules and TiFlash replica at the same time in one table [#37171](https://github.com/pingcap/tidb/issues/37171)

    <!--execution **owner: @zanmato1984**-->

    - (dup) Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)

    <!--transaction **owner: @cfzjywxk**-->

    <!--planner **owner: @fixdb**-->

+ TiKV **owner: @ethercflow**

    - (dup) Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054)
    - (dup) Support configuring the RocksDB write stall settings to a value smaller than the flow control threshold [#13467](https://github.com/tikv/tikv/issues/13467)

+ PD **owner: @nolouch**

+ TiFlash

<!--compute **owner: @zanmato1984**-->

<!--storage **owner: @flowbehappy**-->

+ Tools

    + TiDB Lightning **owner: @niubell**

    + TiDB Data Migration (DM) **owner: @niubell**

    + TiCDC **owner: @nongfushanquan**

    + Backup & Restore (BR) **owner: @3pointer**

    + Dumpling

## Bug fixes

+ TiDB

    <!--sql-infra **owner: @wjhuang2016**-->

    - (dup) Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) Fix the issue that when one PD node goes down, the query of `information_schema.TIKV_REGION_STATUS` fails due to not retrying other PD nodes [#35708](https://github.com/pingcap/tidb/issues/35708)
    - (dup) Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903)

    <!--execution **owner: @zanmato1984**-->

    - Database level privileges are cleaned up correctly [#38363](https://github.com/pingcap/tidb/issues/38363)

    <!--transaction **owner: @cfzjywxk**-->

    - Fix the issue that the Region cache is not cleaned up in time when the Region is merged [#37141](https://github.com/pingcap/tidb/issues/37141)
    - Fix the issue that the KV client sends unnecessary ping messages [#36861](https://github.com/pingcap/tidb/issues/36861)
    - (dup) Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373)

    <!--planner **owner: @fixdb**-->

    - Fix the issue that GROUP CONCAT with ORDER BY might fail when the ORDER BY clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - (dup) Fix the issue that `Can't find column` is reported if an `UPDATE` statement contains common table expressions (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758)
    - (dup) Fix the issue that the `EXECUTE` might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)

+ TiKV **owner: @ethercflow**

    - Fix the issue that snapshot might not contain the complete data caused by introduced batch snapshot across regions [#13553](https://github.com/tikv/tikv/issues/13553)
    - (dup) Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - (dup) Fix the issue that causes permission denied error when TiKV gets an error from the web identity provider and fails back to the default provider [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) Fix the issue that the TiKV service is unavailable for several minutes when a TiKV instance is in an isolated network environment [#12966](https://github.com/tikv/tikv/issues/12966)

+ PD **owner: @nolouch**

    - Fix the issue that the statistics of the region tree might be not accurate [#5318](https://github.com/tikv/pd/issues/5318)
    - (dup) Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) Fix the issue that unhealthy Region might cause PD panic [#5491](https://github.com/tikv/pd/issues/5491)

+ TiFlash

    <!--compute **owner: @zanmato1984**-->

    - (dup) Fix the issue that a window function might cause TiFlash to crash when the query is canceled [#5814](https://github.com/pingcap/tiflash/issues/5814)

    <!--storage **owner: @flowbehappy**-->

    - Fix the issue that iolimiter could unexpectedly throttle io throughput of query requests after large volume writes, which slows down query performance [#5801](https://github.com/pingcap/tiflash/issues/5801)
    - (dup) Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell**

    + TiDB Data Migration (DM) **owner: @niubell**

        - DM will try to persist upstream table structure from dump files when firstly switch to sync unit [#5010](https://github.com/pingcap/tiflow/issues/5010)
        - DM will try to persist upstream table structure from dump files when firstly switch to sync unit [#7159](https://github.com/pingcap/tiflow/issues/7159)
        - DM precheck no longer reports lacking privileges of INFORMATION_SCHEMA [#7317](https://github.com/pingcap/tiflow/issues/7317)
        - (dup) Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028)

    + TiCDC **owner: @nongfushanquan**

        - Fix a bug that may cause cdc server panic if it received a http request before cdc server fully started [#6838](https://github.com/pingcap/tiflow/issues/6838)
        - Change log level from info to debug for some logs to avoid too many logs [#7235](https://github.com/pingcap/tiflow/issues/7235)
        - Fix a bug that may cause changefeed's redo log files be deleted wrongly [#6413](https://github.com/pingcap/tiflow/issues/6413)
        - Fix a bug that may cause cdc unavaliable by commit too many operation in a etcd transaction [#7131](https://github.com/pingcap/tiflow/issues/7131)
        - Fix a bug which can lead inconsistency Change if non-reentrant DDLs can be executed twice [#6927](https://github.com/pingcap/tiflow/issues/6927)
        - Enhance the region worker's performance by handling the resolved ts in the batch mode [#7078](https://github.com/pingcap/tiflow/issues/7078)

    + Backup & Restore (BR) **owner: @3pointer**

        - (dup) Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549)
        - (dup) Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469)

    + Dumpling
