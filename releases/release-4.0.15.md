---
title: TiDB 4.0.15 Release Notes
category: Releases
---

# TiDB 4.0.15 Release Notes

Release Date: September 27, 2021

TiDB version: 4.0.15

## Compatibility changes

+ TiDB

    - Revert [#21045](https://github.com/pingcap/tidb/pull/21045) to avoid show session variables is very slow on first run. [#24326](https://github.com/pingcap/tidb/issues/24326).[26240]

## Improvements

+ TiDB

    - Trigger auto-analyze based on histogram row count [#26706](https://github.com/pingcap/tidb/pull/26706)

+ TiKV

    - separate read write ready to reduce read latency [#10619](https://github.com/tikv/tikv/pull/10619)
    - TiKV coprocessor slow log will only consider time spent on processing the request. [#10863](https://github.com/tikv/tikv/pull/10863)
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10863](https://github.com/tikv/tikv/pull/10863)
    - Support changing CDC configs dynamically [#10684](https://github.com/tikv/tikv/pull/10684)
    - Reduce resolved ts message size to save network bandwidth. [#10677](https://github.com/tikv/tikv/pull/10677)

+ PD

    - Improved the performance of synchronizing Region information between PDs. [#3932](https://github.com/tikv/pd/pull/3932)

+ Tools

    + Backup & Restore (BR)

        - Make split and scatter regions exeuction concurrently, improve the restore speed from 2h to 30 min in our testing [#1429](https://github.com/pingcap/br/pull/1429)
        - Retry on PD request error or TiKV IO timeout error [#1433](https://github.com/pingcap/br/pull/1433)
        - Reduce empty regions when restoration of many small tables [#1374](https://github.com/pingcap/br/issues/1374) [#1432](https://github.com/pingcap/br/pull/1432)
        - Rebase auto id operation while create table, Save the separate rebase ddl operations to speed up restore [#1424](https://github.com/pingcap/br/pull/1424)

    + Dumpling

        - Filter skipped database before traversing the tables, save soma traverse operations [#337](https://github.com/pingcap/dumpling/pull/337)
        - Use `show full tables` to traverse the tables because `show table status` can't work in some mysql version [#332](https://github.com/pingcap/dumpling/pull/332)
        - Support export MySQL compatible databases that don't support `START TRANSACTION  ... WITH CONSISTENT SNAPSHOT` or `SHOW CREATE TABLE` [#329](https://github.com/pingcap/dumpling/pull/329)
        - Refine dumpling warn log to avoid misunderstand that dump is failed [#340](https://github.com/pingcap/dumpling/pull/340)

    + TiDB Lightning

        - Support import into table that has expression index or index depending on virtual generated columns [#1418](https://github.com/pingcap/br/pull/1418)

    + TiCDC

        - Solve the new collation and TiCDC compatibility issue: TiCDC always pull the old value from TiKV internally [#2304](https://github.com/pingcap/ticdc/pull/2304)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2376](https://github.com/pingcap/ticdc/pull/2376)
        - Optimize workerpool for fewer goroutines when concurrency is high [#2486](https://github.com/pingcap/ticdc/pull/2486)
            - Make DDL asynchronous execution to avoid affecting other changefeeds [#2471](https://github.com/pingcap/ticdc/pull/2471)
        - Add a global gRPC connection pool and share gRPC connections among kv clients [#2531](https://github.com/pingcap/ticdc/pull/2531)
        - Fail-fast for unrecoverable DML errors [2315](https://github.com/pingcap/ticdc/pull/2315)
        - Optimize memory management when unified sorter is using memory to sort [#2710](https://github.com/pingcap/ticdc/pull/2710)
        - add prometheus metrics for sink execution ddl [#2681](https://github.com/pingcap/ticdc/pull/2681)
        - Prohibit operating TiCDC clusters across major and minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)
        - Remove file sorter whichi is taked place by unify sorter [#2325](https://github.com/pingcap/ticdc/pull/2325)
        - Cleanup changefeed metrics when changefeed is removed, and processor metrics when processor exits [#2313](https://github.com/pingcap/ticdc/pull/2313)
        - Optimize the resolve lock algorithm after a region is initialized [#2264](https://github.com/pingcap/ticdc/pull/2264)

## Bug Fixes

+ TiDB

    - Fix wrong charset and collation for case when function [#26671](https://github.com/pingcap/tidb/pull/26671)
    - Fix the issue that greatest(datetime) union null returns empty string [#26564](https://github.com/pingcap/tidb/pull/26564)
    - Fix the issue that sometimes fails to send requests if there are tombstone stores. [#25849](https://github.com/pingcap/tidb/pull/25849)
    - Fix range building for binary literal.[26455](https://github.com/pingcap/tidb/pull/26455)
    - Fix "index out of range" error when a SQL contains both group by and union.[26553](https://github.com/pingcap/tidb/pull/26553)
    - executor: fix unexpected behavior when casting invalid string to date.[27935](https://github.com/pingcap/tidb/pull/27935)
    - planner: add missing column for Apply convert to Join.[27282](https://github.com/pingcap/tidb/pull/27282)
    - Fix bug that count disctinct on multi-columns return wrong result when new collation is on.[27830](https://github.com/pingcap/tidb/pull/27830)
    - expression: fix extract bug when argument is a negative duration.[27369](https://github.com/pingcap/tidb/pull/27369)
    - Make `group_concat` function consider the collation.[27835](https://github.com/pingcap/tidb/pull/27835)
    - Fix expression rewrite makes between expr infers wrong collation.[27851](https://github.com/pingcap/tidb/pull/27851)
    - Fix wrong selection push down when having above agg.[27741](https://github.com/pingcap/tidb/pull/27741)
    - Remove the undocumented `/debug/sub-optimal-plan` HTTP API. [#27264](https://github.com/pingcap/tidb/pull/27264)

+ TiKV

    - Fix the issue that br reports file already exists error when TDE enabled during restoration. [#10917](https://github.com/tikv/tikv/pull/10917)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10871](https://github.com/tikv/tikv/pull/10871)
    - Fix delete stale region too frequently. [#10781](https://github.com/tikv/tikv/pull/10781)
    - fix frequently reconnecting pd client [#9818](https://github.com/tikv/tikv/pull/9818)
    - Check stale file information from encryption file dict [#10598](https://github.com/tikv/tikv/pull/10598)

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4081](https://github.com/tikv/pd/pull/4081)
    - Fix the bug that PD may panic during scaling out TiKV. [#3909](https://github.com/tikv/pd/pull/3909)

+ TiFlash

    - Fix the potential issue of data inconsistency after crashes when deployed on multi-disks
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN`
    - Fix the inaccurate store size on tiflash metric under heavy write scenario
    - Fix a bug that TiFlash can not restore data under some situations when deployed on multi disks
    - Fix the potential issue that TiFlash cannot GC the delta data after running for a long time

+ Tools

    + Backup & Restore (BR)

        - Fix the bug that the average speed isn't accurate in backup and restore [#1410](https://github.com/pingcap/br/pull/1410)

    + TiCDC

        - Fix a bug that owner could meet ErrSchemaStorageTableMiss error and reset a changefeed by accident [#2457](https://github.com/pingcap/ticdc/pull/2457)
        - Fix the bug that changefeed cannot be removed if meet GcTTL Exceeded Error [#2455](https://github.com/pingcap/ticdc/pull/2455)
        - Fix outdated capture info may appear in capture list command [#2447](https://github.com/pingcap/ticdc/pull/2447)
        - Fix deadlock in cdc processor [#2017](https://github.com/pingcap/ticdc/pull/2017)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2495](https://github.com/pingcap/ticdc/pull/2495)[#2727](https://github.com/pingcap/ticdc/pull/2727)
        - Fix a bug in metadata management: EtcdWorker snapshot isolation [#2557](https://github.com/pingcap/ticdc/pull/2557)
        - Fix ddl sink error don't stop changefeed [#2556](https://github.com/pingcap/ticdc/pull/2556)
        - Fix open protocol issue: output an empty value when there is no change in one transaction [#2619](https://github.com/pingcap/ticdc/pull/2619)
        - Fix a bug that causes TiCDC to panic on an unsigned tinyint [#2654](https://github.com/pingcap/ticdc/pull/2654)
        - Fix gRPC keepalive error when memory pressure is high [#2718](https://github.com/pingcap/ticdc/pull/2718)
        - Fix OOM when TiCDC captures too many regions [#2723](https://github.com/pingcap/ticdc/pull/2723)
        - Fix json encoding could panic when processing a string type value in some cases [#2781](https://github.com/pingcap/ticdc/pull/2781)
        - fix memory leak which may happen in create new changefeed [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - Fixed a bug in DDL handling when the owner restarts [#2609](https://github.com/pingcap/ticdc/pull/2609)
        - Fix potential DDL loss when owner crashes while executing DDL [#2291](https://github.com/pingcap/ticdc/pull/2291)
        - Fix runtime panic bug [#2298](https://github.com/pingcap/ticdc/pull/2298)
