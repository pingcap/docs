---
title: TiDB 4.0.15 Release Notes
category: Releases
---

# TiDB 4.0.15 Release Notes

Release Date: September 27, 2021

TiDB version: 4.0.15

## Improvements

+ TiDB

    - Trigger auto-analyze based on histogram row count [#26706](https://github.com/pingcap/tidb/pull/26706)

+ TiKV

    - separate read write ready to reduce read latency [#10619](https://github.com/tikv/tikv/pull/10619)

## Bug Fixes

+ TiDB

    - Fix wrong charset and collation for case when function [#26671](https://github.com/pingcap/tidb/pull/26671)
    - Fix the issue that greatest(datetime) union null returns empty string [#26564](https://github.com/pingcap/tidb/pull/26564)
    - Fix the issue that sometimes fails to send requests if there are tombstone stores. [#25849](https://github.com/pingcap/tidb/pull/25849)

+ TiFlash

    - Fix the potential issue of data inconsistency after crashes when deployed on multi-disks [#2774](https://github.com/pingcap/tics/pull/2774)
    - Fix the bug that filters unexpected data if the query contains "constant" "<"/"<="/">"/">=" "column" [#2634](https://github.com/pingcap/tics/pull/2634)
    - Fix inaccurate store size on tiflash metric under heavy write scenario [#2596](https://github.com/pingcap/tics/pull/2596)
    - Fix the bug that TiFlash can not restore data under some situations when deployed on multi disks [#2433](https://github.com/pingcap/tics/pull/2433)
    - Fix the potential issue that TiFlash cannot GC the delta data after running for a long time [#2335](https://github.com/pingcap/tics/pull/2335)

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4081](https://github.com/tikv/pd/pull/4081)
    - Fix the bug that PD may panic during scaling out TiKV. [#3909](https://github.com/tikv/pd/pull/3909)

## 以下 note 未分类。请将以下 note 进行分类 (Feature enhancements, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ TiDB

    - executor: fix unexpected behavior when casting invalid string to date [#27935](https://github.com/pingcap/tidb/pull/27935)
    - fix expression rewrite makes between expr infers wrong collation. [#27851](https://github.com/pingcap/tidb/pull/27851)
    - make `group_concat` function consider the collation [#27835](https://github.com/pingcap/tidb/pull/27835)
    - Fix bug that count disctinct on multi-columns return wrong result when new collation is on. [#27830](https://github.com/pingcap/tidb/pull/27830)
    - fix wrong selection push down when having above agg [#27741](https://github.com/pingcap/tidb/pull/27741)
    - expression: fix extract bug when argument is a negative duration [#27369](https://github.com/pingcap/tidb/pull/27369)
    - planner: add missing column for Apply convert to Join [#27282](https://github.com/pingcap/tidb/pull/27282)
    - The undocumented `/debug/sub-optimal-plan` HTTP API has been removed. [#27264](https://github.com/pingcap/tidb/pull/27264)
    - fix range building for binary literal [#26455](https://github.com/pingcap/tidb/pull/26455)
    - Revert #21045 to avoid #24326. [#26240](https://github.com/pingcap/tidb/pull/26240)

+ TiKV

    - Fix the issue that br reports file already exists error when TDE enabled during restoration. [#10917](https://github.com/tikv/tikv/pull/10917)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10871](https://github.com/tikv/tikv/pull/10871)
    - TiKV coprocessor slow log will only consider time spent on processing the request.
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10863](https://github.com/tikv/tikv/pull/10863)
    - Fix delete stale region too frequently. [#10781](https://github.com/tikv/tikv/pull/10781)
    - Support changing CDC configs dynamically [#10684](https://github.com/tikv/tikv/pull/10684)
    - Reduce resolved ts message size to save network bandwidth. [#10677](https://github.com/tikv/tikv/pull/10677)
    - Check stale file information from encryption file dict [#10598](https://github.com/tikv/tikv/pull/10598)
    - fix frequently reconnecting pd client [#9818](https://github.com/tikv/tikv/pull/9818)

+ TiFlash

    - function result name should contain collator info [#3018](https://github.com/pingcap/tics/pull/3018)

+ PD

    - Improved the performance of synchronizing Region information between PDs. [#3932](https://github.com/tikv/pd/pull/3932)

+ Tools

    + Backup & Restore (BR)

        - Retry pd request and TiKV IO timeout error [#1433](https://github.com/pingcap/br/pull/1433)
        - Too many empty region after restoration of many small tables [#1374](https://github.com/pingcap/br/issues/1374)
        - Restore many small tables would be faster now. [#1429](https://github.com/pingcap/br/pull/1429)
        - Merged the rebase auto id operation into create table. [#1424](https://github.com/pingcap/br/pull/1424)
        - Expression index and index depending on virtual generated columns are now valid. Previously these indices are broken when importing through Lightning local or importer backend. [#1418](https://github.com/pingcap/br/pull/1418)
        - fix the bug that the average speed isn't accurate in backup and restore [#1410](https://github.com/pingcap/br/pull/1410)
        - Remove unnecessary speed and concurrent limitation [#1346](https://github.com/pingcap/br/pull/1346)

    + Dumpling

        - fix pending on show table status in some mysql version [#332](https://github.com/pingcap/dumpling/pull/332)
        - Support for backing up MySQL compatible databases that don't support START TRANSACTION  ... WITH CONSISTENT SNAPSHOT
        - Support for backing up MySQL compatible databases that don't support SHOW CREATE TABLE [#329](https://github.com/pingcap/dumpling/pull/329)

    + TiCDC

        - Fix json encoding could panic when processing a string type value in some cases. [#2781](https://github.com/pingcap/ticdc/pull/2781)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2727](https://github.com/pingcap/ticdc/pull/2727)
        - Fix OOM when TiCDC captures too many regions [#2723](https://github.com/pingcap/ticdc/pull/2723)
        - Fix gRPC keepalive error when memory pressure is high. [#2718](https://github.com/pingcap/ticdc/pull/2718)
        - Optimize memory management when unified sorter is using memory to sort. [#2710](https://github.com/pingcap/ticdc/pull/2710)
        - add prometheus metrics for sink execution ddl [#2681](https://github.com/pingcap/ticdc/pull/2681)
        - Fix a bug that causes TiCDC to panic on an unsigned tinyint [#2654](https://github.com/pingcap/ticdc/pull/2654)
        - fix memory leak which may happen in create new changefeed. [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - Fix open protocol, don't output an empty value when there is no change in one transaction. [#2619](https://github.com/pingcap/ticdc/pull/2619)
        - Fixed a bug in DDL handling when the owner restarts. [#2609](https://github.com/pingcap/ticdc/pull/2609)
        - Prohibit operating TiCDC clusters across major and minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)
        - Fix a bug in metadata management [#2557](https://github.com/pingcap/ticdc/pull/2557)
        - Add a global gRPC connection pool and share gRPC connections among kv clients. [#2531](https://github.com/pingcap/ticdc/pull/2531)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2495](https://github.com/pingcap/ticdc/pull/2495)
        - Optimize workerpool for fewer goroutines when concurrency is high. [#2486](https://github.com/pingcap/ticdc/pull/2486)
        - Fix a bug that owner could meet ErrSchemaStorageTableMiss error and reset a changefeed by accident. [#2457](https://github.com/pingcap/ticdc/pull/2457)
        - fix the bug that changefeed cannot be removed if meet GcTTL Exceeded Error [#2455](https://github.com/pingcap/ticdc/pull/2455)
        - fix outdated capture info may appear in capture list command [#2447](https://github.com/pingcap/ticdc/pull/2447)
        - fix a bug where synchronizing large tables to cdclog failed. [#2444](https://github.com/pingcap/ticdc/pull/2444)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2376](https://github.com/pingcap/ticdc/pull/2376)
        - Remove file sorter. [#2325](https://github.com/pingcap/ticdc/pull/2325)
        - Cleanup changefeed metrics when changefeed is removed.
        - Cleanup processor metrics when processor exits. [#2313](https://github.com/pingcap/ticdc/pull/2313)
        - puller,mounter,processor: always pull the old value internally [#2304](https://github.com/pingcap/ticdc/pull/2304)
        - Fix minor runtime panic risk [#2298](https://github.com/pingcap/ticdc/pull/2298)
        - Fix potential DDL loss when owner crashes while executing DDL [#2291](https://github.com/pingcap/ticdc/pull/2291)
        - Don't resolve lock immediately after a region is initialized. [#2264](https://github.com/pingcap/ticdc/pull/2264)
        - Fix deadlock [#2017](https://github.com/pingcap/ticdc/pull/2017)
