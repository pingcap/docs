---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

Release date: June 9, 2021

TiDB version: 5.0.2

## Compatibility Changes

+ Tools

    + TiCDC

        - `--sort-dir` in changefeed command is deprecated, please set `--sort-dir` in server command instead [#1795](https://github.com/pingcap/ticdc/pull/1795)

## New Features

## Improvements

+ TiDB

    - Skip reading mysql.stats_histograms if cached stats is up-to-date [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiFlash

    - Apply Region snapshots by ingesting files to reduce memory usage
    - Optimize the table lock to avoid reading and DDL jobs blocking each other
    - Support casting the integer or real type to real type

+ Tools

    + TiCDC

        - Add metrics for table memory consumption [#1885](https://github.com/pingcap/ticdc/pull/1885)
        - Reduce memory malloc in sort heap to avoid too much CPU overhead. [#1863](https://github.com/pingcap/ticdc/pull/1863)
        - Modified the update strategy of gcSafePoint. Fix the problem that TiKV GC safe point is blocked indefinitely due to TiCDC changefeed checkpoint stagnation. [#1759](https://github.com/pingcap/ticdc/pull/1759)
        - Deleted useless log info that may cause confusion for users. [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        - Clarify some ambiguous error message. [#1132](https://github.com/pingcap/br/pull/1132)
        - Checks cluster version of a backup. [#1091](https://github.com/pingcap/br/pull/1091)
        - Support backup and restore system tables in the `mysql` database.[#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)

    + Dumpling

        - Fix a bug that caused, when backup failed, nothing would be printed to terminal. [#280](https://github.com/pingcap/dumpling/pull/280)

## Bug Fixes

+ TiDB

    - Fix index join panic on prefix index on some cases [#24824](https://github.com/pingcap/tidb/pull/24824)
    - Fix the issue point get cached plan of prepared statement is incorrectly used by in transaction point get statement. [#24765](https://github.com/pingcap/tidb/pull/24765)
    - Fix write wrong prefix index value when collation is ascii_bin/latin1_bin [#24680](https://github.com/pingcap/tidb/pull/24680)
    - Fix the issue that ongoing transaction could be aborted by the gc worker. [#24652](https://github.com/pingcap/tidb/pull/24652)
    - Fix bug that point query maybe get wrong on the clustered index when new-collation enabled but new-row-format disabled [#24611](https://github.com/pingcap/tidb/pull/24611)
    - Refactor converting partition keys for shuffle hash join [#24490](https://github.com/pingcap/tidb/pull/24490)
    - Fix panic when building plan for a query containing HAVING clause. [#24489](https://github.com/pingcap/tidb/pull/24489)
    - Planner: fix column pruning bug for Apply and Join [#24437](https://github.com/pingcap/tidb/pull/24437)
    - Fix the bug that primary lock fallen back from async commit cannot be resolved. [#24397](https://github.com/pingcap/tidb/pull/24397)
    - Statistics: fix a statistics GC problem that can cause duplicated fm-sketch records [#24357](https://github.com/pingcap/tidb/pull/24357)
    - Avoid unnecessary pessimistic rollback when pessimistic locking receives ErrKeyExists [#23800](https://github.com/pingcap/tidb/pull/23800)
    - Fix numeric literals cannot be recognized when set 'ANSI_QUOTES' sql_mode [#25015](https://github.com/pingcap/tidb/pull/25015)
    - No longer allowing `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` to read from non-listed partitions [#25000](https://github.com/pingcap/tidb/pull/25000)
    - Fix "index out of range" error when a SQL contains both group by and union. [#24551](https://github.com/pingcap/tidb/pull/24551)
    - Fix wrong collation for concat function [#24301](https://github.com/pingcap/tidb/pull/24301)
    - Fix global variable collation_server does not take effect in new session [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiFlash

    - Fix the issue of incorrect results when cloning shared delta index concurrently
    - Fix the potential issue that TiFlash fails to restart with incomplete data
    - Fix the issue that old dm files are not removed atomically
    - Fix the potential panic that occurs when feature `compaction filter` is enabled
    - Fix the potential issue that `ExchangeSender` will send duplicated chunks
    - Fix the issue that TiFlash can not resolve fallen back `async commit` lock
    - Fix the issue of incorrect results when the return columns of casting timezone contains timestamp type
    - Fix the issue that TiFlash panics during Segment Split
    - Fix the issue that execution information about non root MPP task is not accurate

+ Tools

    + TiCDC

        - Fix time zone lost in Avro output. [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - Add stale temporary files clean-up in Unified Sorter, and forbids sharing sort-dir. [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - Fix a deadlock bug in the kv client that deadlock happens when large stale regions exist. [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - Fix wrong usage in cdc server cli flag, `--cert-allowed-cn` [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - Revert the update for explicit_defaults_for_timestamp which requires `SUPER` privilege when replicating to MySQL. [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - Support sink flow control to reduce OOM [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - Fix a bug about resolved ts stopped when move a table. [#1828](https://github.com/pingcap/ticdc/pull/1828)

    + Backup & Restore (BR)

        - Fix the issue that log restore lost delete key during restore. [#1083](https://github.com/pingcap/br/pull/1083)
        - Fix a bug that caused BR send too many useless RPCs to TiKV [#1037](https://github.com/pingcap/br/pull/1037)
        - Fix a bug that caused, when backup failed, nothing would be printed to terminal. [#1043](https://github.com/pingcap/br/pull/1043)

    + TiDB Lightning

        - Fix the issue that lightning panic due to batch kv greater than 4 GB. [#5739](https://github.com/pingcap/br/pull/5739)
        - Fix the bug that lightning tidb backend cannot load any data when autocommit is disabled [#1125](https://github.com/pingcap/br/pull/1125)
        - Fix the bug that batch split region fails due to total key size exceeds raft entry limit [#1065](https://github.com/pingcap/br/pull/1065)

## 以下 note 未分类。请将以下 note 进行分类 (New feature, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ TiKV

    - release-note [#10278](https://github.com/tikv/tikv/pull/10278)
    - Enable hibernate regions by default (i.e. `raftstore.hibernate-regions = true`). [#10266](https://github.com/tikv/tikv/pull/10266)
    - Fix CDC OOM issue caused by reading old values. [#10246](https://github.com/tikv/tikv/pull/10246)
    - BR now supports S3-compatible storage using virtual-host addressing style. [#10243](https://github.com/tikv/tikv/pull/10243)
    - Fix read empty value for the clustered primary key column in the secondary index when collation is latin1_bin. [#10239](https://github.com/tikv/tikv/pull/10239)
    - Add `abort-on-panic` config, which allow core dump to be generated when panic. Users still need to correctly config the environment to enable core dump. [#10216](https://github.com/tikv/tikv/pull/10216)
    - Support ingesting default-cf and write-cf sst in one raft command. [#10202](https://github.com/tikv/tikv/pull/10202)
    - Support back pressure CDC scan speed. [#10151](https://github.com/tikv/tikv/pull/10151)
    - Reduce memory usage of CDC initial scan. [#10133](https://github.com/tikv/tikv/pull/10133)
    - Fix sysbench point-get performance regression when TiKV readpool is not busy. [#10115](https://github.com/tikv/tikv/pull/10115)
    - Improve CDC old value cache hit ratio in pessimistic txn [#10089](https://github.com/tikv/tikv/pull/10089)
    - Approximate split range evenly [#10086](https://github.com/tikv/tikv/pull/10086)

+ PD

    - Fix offline_stats statistic after merge offline peer [#3615](https://github.com/pingcap/pd/pull/3615)
