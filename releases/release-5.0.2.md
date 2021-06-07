---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

Release date: June 9, 2021

TiDB version: 5.0.2

## Compatibility Changes

+ Tools

    + TiCDC

        - Deprecate `--sort-dir` in the `cdc cli changefeed` command. Instead, set `--sort-dir` in the `cdc server` command [#1795](https://github.com/pingcap/ticdc/pull/1795)

## New Features

+ TiKV

    - Enable hibernate regions by default (i.e. `raftstore.hibernate-regions = true`). [#10266](https://github.com/tikv/tikv/pull/10266)

## Improvements

+ TiDB

    - Avoid frequently reading the `mysql.stats_histograms` table if the cached statistics is up-to-date to avoid high CPU usage [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiKV

    - BR now supports S3-compatible storage using virtual-host addressing style. [#10243](https://github.com/tikv/tikv/pull/10243)
    - Support back pressure CDC scan speed. [#10151](https://github.com/tikv/tikv/pull/10151)
    - Reduce memory usage of CDC initial scan. [#10133](https://github.com/tikv/tikv/pull/10133)
    - Fix sysbench point-get performance regression when TiKV readpool is not busy. [#10115](https://github.com/tikv/tikv/pull/10115)
    - Improve CDC old value cache hit ratio in pessimistic txn [#10089](https://github.com/tikv/tikv/pull/10089)
    - Approximate split range evenly [#10086](https://github.com/tikv/tikv/pull/10086)

+ TiFlash

    - Apply Region snapshots by ingesting files to reduce memory usage
    - Optimize the table lock to prevent reading data and DDL jobs from blocking each other
    - Support casting the `INTEGER` or `REAL` type to `REAL` type

+ Tools

    + TiCDC

        - Add monitoring metrics for the table memory consumption [#1885](https://github.com/pingcap/ticdc/pull/1885)
        - Optimize the memory and CPU usages during the sorting stage [#1863](https://github.com/pingcap/ticdc/pull/1863)
        - Delete some useless log information that might cause confusion [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        - Clarify some ambiguous error message [#1132](https://github.com/pingcap/br/pull/1132)
        - Support checking the cluster version of a backup [#1091](https://github.com/pingcap/br/pull/1091)
        - Support backing up and restoring system tables in the `mysql` schema [#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)

    + Dumpling

        - Fix the issue that no error is output when a backup operation fails [#280](https://github.com/pingcap/dumpling/pull/280)

## Bug Fixes

+ TiDB

    - Fix the panic issue caused by using the prefix index and index join in some cases [#24824](https://github.com/pingcap/tidb/pull/24824)
    - Fix the issue that the prepared plan cache of `point get` is incorrectly used by the `point get` statement in the transaction [#24765](https://github.com/pingcap/tidb/pull/24765)
    - Fix the issue of writing the wrong prefix index value when the collation is `ascii_bin` or `latin1_bin` [#24680](https://github.com/pingcap/tidb/pull/24680)
    - Fix the issue that the ongoing transaction might be aborted by the GC worker [#24652](https://github.com/pingcap/tidb/pull/24652)
    - Fix a bug that the point query might get wrong on the clustered index when `new-collation` is enabled but `new-row-format` is disabled [#24611](https://github.com/pingcap/tidb/pull/24611)
    - Refactor the conversion of partition keys for shuffle hash join [#24490](https://github.com/pingcap/tidb/pull/24490)
    - Fix the panic issue that occurs when building the plan for queries that contain the `HAVING` clause [#24489](https://github.com/pingcap/tidb/pull/24489)
    - Fix the issue that the column pruning improvement causes the `Apply` and `Join` operators' results to go wrong [#24437](https://github.com/pingcap/tidb/pull/24437)
    - Fix a bug that the primary lock fallen back from async commit cannot be resolved [#24397](https://github.com/pingcap/tidb/pull/24397)
    - Fix a GC issue of statistics that might cause duplicated fm-sketch records [#24357](https://github.com/pingcap/tidb/pull/24357)
    - Avoid unnecessary pessimistic rollback when the pessimistic locking receives the `ErrKeyExists` error [#23800](https://github.com/pingcap/tidb/pull/23800)
    - Fix the issue that numeric literals cannot be recognized when the sql_mode contains `ANSI_QUOTES` [#25015](https://github.com/pingcap/tidb/pull/25015)
    - Forbid statements such as `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` to read data from non-listed partitions [#25000](https://github.com/pingcap/tidb/pull/25000)
    - Fix the potential `index out of range` error when a SQL statement contains both `GROUP BY` and `UNION` [#24551](https://github.com/pingcap/tidb/pull/24551)
    - Fix the issue that the `CONCAT` function incorrectly handles the collation [#24301](https://github.com/pingcap/tidb/pull/24301)
    - Fix the issue that the `collation_server` global variable does not take effect in new sessions [#24156](https://github.com/pingcap/tidb/pull/24156)

+ PD

    - Fix offline_stats statistic after merge offline peer [#3615](https://github.com/pingcap/pd/pull/3615)
    - Fix the issue that leader re-election be slow when there are many stores [#3719](https://github.com/tikv/pd/pull/3719)
    - Fix the panic issue about remove evict leader scheduler from a nonexistent store [#3679](https://github.com/tikv/pd/pull/3679)
    - Fix the statistic issue that offline Peer not clean after been merged [#3614](https://github.com/tikv/pd/pull/3614)

+ TiKV

    - Fix CDC OOM issue caused by reading old values. [#10246](https://github.com/tikv/tikv/pull/10246)
    - Allow to read empty value for the clustered primary key column in the secondary index when collation is latin1_bin. [#10239](https://github.com/tikv/tikv/pull/10239)
    - Add `abort-on-panic` config, which allow core dump to be generated when panic. Users still need to correctly config the environment to enable core dump. [#10216](https://github.com/tikv/tikv/pull/10216)

+ TiFlash

    - Fix the issue of incorrect results when cloning shared delta index concurrently
    - Fix the potential issue that TiFlash fails to restart with incomplete data
    - Fix the issue that old dm files are not removed automatically
    - Fix the potential panic that occurs when the Compaction Filter feature is enabled
    - Fix the potential issue that `ExchangeSender` sends duplicated data
    ?- Fix the issue that TiFlash cannot resolve the fallen back Async Commit lock
    - Fix the issue of incorrect results returned when the casted result of the `TIMEZONE` type contains the `TIMESTAMP` type
    - Fix the TiFlash panic issue that occurs during Segment Split
    - Fix the issue that the execution information about the non-root MPP task is not accurate

+ Tools

    + TiCDC

        - Fix the issue that the time zone information is lost in the Avro output [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - Support cleaning up stale temporary files in Unified Sorter and forbids sharing the `sort-dir` directory [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - Fix a deadlock bug in the KV client that occurs when many stale Regions exist [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - Fix the wrong help information in the `cdc server cli` flag of `--cert-allowed-cn` [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - Revert the update for `explicit_defaults_for_timestamp` which requires the `SUPER` privilege when replicating data to MySQL [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - Support the sink flow control to reduce the risk of memory overflow [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - Fix a bug that the replication task might stop when moving a table [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - Fix the issue that the TiKV GC safe point is blocked due to the stagnation of TiCDC changefeed checkpoint [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        ?- Fix the issue that log restore lost delete key during restore [#1083](https://github.com/pingcap/br/pull/1083)
        - Fix a bug that causes BR to send too many useless RPC requests to TiKV [#1037](https://github.com/pingcap/br/pull/1037)
        - Fix the issue that no error is output when a backup operation fails [#1043](https://github.com/pingcap/br/pull/1043)

    + TiDB Lightning

        - Fix the issue of TiDB Lightning panic that occurs when generating KV data [#5739](https://github.com/pingcap/br/pull/5739)
        - Fix the issue that TiDB Lightning in the TiDB-backend mode cannot load any data when autocommit is disabled [#1125](https://github.com/pingcap/br/pull/1125)
        - Fix a bug that the batch split region fails due to total key size exceeding the raft entry limit during the data import [#1065](https://github.com/pingcap/br/pull/1065)
