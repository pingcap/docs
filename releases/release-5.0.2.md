---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

Release date: June 9, 2021

TiDB version: 5.0.2

## Compatibility Changes

## New Features

## Improvements

+ TiDB

    - Skip reading mysql.stats_histograms if cached stats is up-to-date [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiFlash

    - Support push down filter on timestamp type column to storage layer. [#1906](https://github.com/pingcap/tics/pull/1906)
    - Apply Region snapshots by ingesting files to greatly reduce the memory usage [#1867](https://github.com/pingcap/tics/pull/1867)
    - Optimize the table lock to avoid reading and DDL jobs from blocking each other [#1858](https://github.com/pingcap/tics/pull/1858)

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

+ TiFlash

    - Fix the potential concurrency problem when clone the shared delta index. [#2033](https://github.com/pingcap/tics/pull/2033)
    - Fix the bug that incomplete data may make TiFlash fail to restart [#2003](https://github.com/pingcap/tics/pull/2003)
    - Fix the problem that old dmfile is not removed atomically [#1925](https://github.com/pingcap/tics/pull/1925)
    - Fix the issue that TiFlash may panic when `compaction filter` is enabled [#1891](https://github.com/pingcap/tics/pull/1891)
    - Fix problem ExchangeSender will sometimes send duplicated data chunks [#1883](https://github.com/pingcap/tics/pull/1883)
    - Fix problem that TiFlash can not resolve fallen back async commit lock [#1870](https://github.com/pingcap/tics/pull/1870)
    - Fix unexpected timezone cast which may cause wrong result if the return column contains timestamp column [#1827](https://github.com/pingcap/tics/pull/1827)
    - Fix a bug that TiFlash crash during Segment Split. [#1823](https://github.com/pingcap/tics/pull/1823)
    - Fix bug that execution info for non root mpp task is not accurate enough [#1840](https://github.com/pingcap/tics/pull/1840)
    - Fix the problem that obsolete data may not be removed when there is no more write to the storage [#1828](https://github.com/pingcap/tics/pull/1828)

+ Tools

    - Backup & Restore (BR)

        + Fix the bug that batch split region fails due to total key size exceeds raft entry limit [#1148](https://github.com/pingcap/br/pull/1148)

## 以下 note 未分类。请将以下 note 进行分类 (New feature, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ TiDB

    - Update parser to fix lexer bug [#25015](https://github.com/pingcap/tidb/pull/25015)
    - Fixed issue-24746, no longer allowing `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` to read from non-listed partitions [#25000](https://github.com/pingcap/tidb/pull/25000)
    - Fix "index out of range" error when a SQL contains both group by and union. [#24551](https://github.com/pingcap/tidb/pull/24551)
    - Fix wrong collation for concat function [#24301](https://github.com/pingcap/tidb/pull/24301)
    - Fix global variable collation_server does not take effect in new session [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiKV

    - release-note [#10278](https://github.com/tikv/tikv/pull/10278)
    - No release notes [#10273](https://github.com/tikv/tikv/pull/10273)
    - Enable hibernate regions by default (i.e. `raftstore.hibernate-regions = true`). [#10266](https://github.com/tikv/tikv/pull/10266)
    - Fix CDC OOM issue caused by reading old values. [#10246](https://github.com/tikv/tikv/pull/10246)
    - BR now supports S3-compatible storage using virtual-host addressing style. [#10243](https://github.com/tikv/tikv/pull/10243)
    - Fix read empty value for the clustered primary key column in the secondary index when collation is latin1_bin. [#10239](https://github.com/tikv/tikv/pull/10239)
    - Add `abort-on-panic` config, which allow core dump to be generated when panic. Users still need to correctly config the environment to enable core dump. [#10216](https://github.com/tikv/tikv/pull/10216)
    - No release note. (The bug is not released yet.) [#10214](https://github.com/tikv/tikv/pull/10214)
    - Support ingesting default-cf and write-cf sst in one raft command. [#10202](https://github.com/tikv/tikv/pull/10202)
    - Support back pressure CDC scan speed. [#10151](https://github.com/tikv/tikv/pull/10151)
    - Reduce memory usage of CDC initial scan. [#10133](https://github.com/tikv/tikv/pull/10133)
    - Fix sysbench point-get performance regression when TiKV readpool is not busy. [#10115](https://github.com/tikv/tikv/pull/10115)
    - Improve CDC old value cache hit ratio in pessimistic txn [#10089](https://github.com/tikv/tikv/pull/10089)
    - Approximate split range evenly [#10086](https://github.com/tikv/tikv/pull/10086)

+ PD

    - Fix offline_stats statistic after merge offline peer [#3615](https://github.com/pingcap/pd/pull/3615)

+ TiFlash

    - Support int/real as real [#1928](https://github.com/pingcap/tics/pull/1928)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that restore from `mysql` schema would failed. [#1143](https://github.com/pingcap/br/pull/1143)
        - BR would check cluster version of backup now. [#1091](https://github.com/pingcap/br/pull/1091)
        - Fix the issue that log restore lost delete key during restore. [#1083](https://github.com/pingcap/br/pull/1083)
        - BR now support backing up user tables created in the `mysql` schema. [#1078](https://github.com/pingcap/br/pull/1078)
        - Fix a bug that caused, when backup failed, nothing would be printed to terminal. [#1043](https://github.com/pingcap/br/pull/1043)
        - Fix a bug that caused BR send too many useless RPCs to TiKV [#1037](https://github.com/pingcap/br/pull/1037)

    - TiCDC

        - Add metrics for table memory consumption [#1885](https://github.com/pingcap/ticdc/pull/1885)
        - Owner:  When tikv_gc_life_time is greater than gcttl, use tikv_gc_life_time to calculate the lower bound of gcSafePoint. [#1872](https://github.com/pingcap/ticdc/pull/1872)
        - Reduce memory malloc in sort heap to avoid too much CPU overhead. [#1863](https://github.com/pingcap/ticdc/pull/1863)
        - Flow Control bug fix (no released version affected) [#1859](https://github.com/pingcap/ticdc/pull/1859)
        - Support sink flow control to reduce OOM [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - Fix a bug about resolved ts stopped when move a table. [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - Fix a deadlock bug in the kv client that deadlock happens when large stale regions exist. [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - Modified the update strategy of gcSafePoint.  Fix the problem that TiKV GC safe point is blocked indefinitely due to TiCDC changefeed checkpoint stagnation. [#1759](https://github.com/pingcap/ticdc/pull/1759)
        - Revert the update for explicit_defaults_for_timestamp which requires `SUPER` privilege when replicating to MySQL. [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - Add stale temporary files clean-up in Unified Sorter, and forbids sharing sort-dir. [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - Add http handler for failpoint [#1733](https://github.com/pingcap/ticdc/pull/1733)
        - Fix time zone lost in Avro output. [#1712](https://github.com/pingcap/ticdc/pull/1712)
