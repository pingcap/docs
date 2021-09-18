---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 Release Notes

Release Date: September 27, 2021

TiDB version: 5.1.2

## Improvements

+ TiDB

    - Trigger auto-analyze based on histogram row count [#26708](https://github.com/pingcap/tidb/pull/26708)

+ TiFlash

    - Support pushing down ROUND(X) to TiFlash. [#2611](https://github.com/pingcap/tics/pull/2611)
    - support function DATE() pushed down to tiflash [#2602](https://github.com/pingcap/tics/pull/2602)
    - support functions of ADDDATE() and DATE_ADD() pushed down to tiflash [#2591](https://github.com/pingcap/tics/pull/2591)
    - retry when meeting stablish conn fails [#2570](https://github.com/pingcap/tics/pull/2570)
    - Support pushing down MOD(N, M) to TiFlash. [#2560](https://github.com/pingcap/tics/pull/2560)
    - Add Grafana panels for write throughput per instance [#2544](https://github.com/pingcap/tics/pull/2544)
    -  Cherry-pick #2216 #2460 #2494 & Optimizr read-index retry to release-5.1 [#2345](https://github.com/pingcap/tics/pull/2345)

## Bug Fixes

+ TiDB

    - Fix wrong index hash join when hash col is enum. [#28081](https://github.com/pingcap/tidb/pull/28081)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#27678](https://github.com/pingcap/tidb/pull/27678)
    - Keep the overflow check logic same with mysql [#26725](https://github.com/pingcap/tidb/pull/26725)
    - Fix #26147 that `tidb` returns an `unknow` error with no message while it should return the error that contains `pd is timeout`. [#26682](https://github.com/pingcap/tidb/pull/26682)
    - Fix wrong charset and collation for case when function [#26673](https://github.com/pingcap/tidb/pull/26673)
    - Fix the issue that greatest(datetime) union null returns empty string [#26566](https://github.com/pingcap/tidb/pull/26566)

+ TiFlash

    - Fix the potential issue of data inconsistency after crashes when deployed on multi-disks [#2776](https://github.com/pingcap/tics/pull/2776)
    - fix bug that SharedQueryBlockInputStream may loss block randomly. [#2762](https://github.com/pingcap/tics/pull/2762)
    - Please add a release note, or a 'None' if it is not needed. [#2710](https://github.com/pingcap/tics/pull/2710)
    - Fix concurrency between init store and DDL. [#2693](https://github.com/pingcap/tics/pull/2693)
    - Fix false alert of expected internal DDL error [#2673](https://github.com/pingcap/tics/pull/2673)
    - Fix the bug that filters unexpected data if the query contains "constant" "<"/"<="/">"/">=" "column" [#2635](https://github.com/pingcap/tics/pull/2635)
    - Fix an overflow bug in decimal MOD(N, M). [#2609](https://github.com/pingcap/tics/pull/2609)
    - Fix the potential panic when applying Snapshot with multiple DDL operations [#2606](https://github.com/pingcap/tics/pull/2606)
    - Fix inaccurate store size on tiflash metric under heavy write scenario [#2598](https://github.com/pingcap/tics/pull/2598)
    - Fix the potential issue that TiFlash cannot GC the delta data after running for a long time [#2337](https://github.com/pingcap/tics/pull/2337)

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4083](https://github.com/tikv/pd/pull/4083)
    - Fix an issue where data is not stored when using max-replicas or location-labels to indirectly update default placement rule [#3915](https://github.com/tikv/pd/pull/3915)
    - Fix the bug that PD may panic during scaling out TiKV. [#3911](https://github.com/tikv/pd/pull/3911)

+ Tools

    + Backup & Restore (BR)

        - Fix the bug that in concurrency mode, pd schedulers may not be restored if one or more lightning failed. [#1422](https://github.com/pingcap/br/pull/1422)
        - Fix the bug that lightning local backend may met checksum mismatch error due to data loss. [#1416](https://github.com/pingcap/br/pull/1416)

## __unsorted

+ TiDB

    - Fix `can not found column in Schema column` error for mpp queries [#28148](https://github.com/pingcap/tidb/pull/28148)
    - Fix a bug that TiDB may crash when TiFlash is shutting down. [#28139](https://github.com/pingcap/tidb/pull/28139)
    - This reverts commit d4cd12fe422fb18b6012607ee18b6acca40d9225. [#28091](https://github.com/pingcap/tidb/pull/28091)
    - planner: fix the problem of using `enum like 'x%'` to build the wrong range [#28066](https://github.com/pingcap/tidb/pull/28066)
    - push down mod() to TiFlash. [#27865](https://github.com/pingcap/tidb/pull/27865)
    - fix expression rewrite makes between expr infers wrong collation. [#27549](https://github.com/pingcap/tidb/pull/27549)
    - execution: fix cte dead lock when used with IndexLookupJoin [#27536](https://github.com/pingcap/tidb/pull/27536)
    - Fix a bug that retryable deadlocks are incorrectly recorded into `INFORMATION_SCHEMA.DEADLOCKS` table. [#27535](https://github.com/pingcap/tidb/pull/27535)
    - make `group_concat` function consider the collation [#27529](https://github.com/pingcap/tidb/pull/27529)
    - Fix bug that count disctinct on multi-columns return wrong result when new collation is on. [#27506](https://github.com/pingcap/tidb/pull/27506)
    - Fix an issue that the `TABLESAMPLE` query result from partitioned tables is not sorted as expected. [#27411](https://github.com/pingcap/tidb/pull/27411)
    - expression: fix extract bug when argument is a negative duration [#27367](https://github.com/pingcap/tidb/pull/27367)
    - The undocumented `/debug/sub-optimal-plan`  HTTP API has been removed. [#27265](https://github.com/pingcap/tidb/pull/27265)
    - fix wrong selection push down when having above agg [#27258](https://github.com/pingcap/tidb/pull/27258)
    - fix a bug that query on hash partition table return wrong reslut [#27164](https://github.com/pingcap/tidb/pull/27164)
    - executor: fix unexpected behavior when casting invalid string to date [#27112](https://github.com/pingcap/tidb/pull/27112)
    - fix a bug that creates partition fail if `NO_UNSIGNED_SUBTRACTION` is set. [#27053](https://github.com/pingcap/tidb/pull/27053)
    - planner: add missing distinct flag for Apply convert to join. [#26969](https://github.com/pingcap/tidb/pull/26969)
    - Fix an issue that NO_ZERO_IN_DATE does not work on the default values. [#26904](https://github.com/pingcap/tidb/pull/26904)
    - store/copr: block the tiflash node for a period when it fails before. [#26897](https://github.com/pingcap/tidb/pull/26897)
    - Fix then bug if the CTE is referenced more than once. [#26661](https://github.com/pingcap/tidb/pull/26661)
    - planner: fix CTE bug when MergeJoin is used [#26658](https://github.com/pingcap/tidb/pull/26658)
    - Fix a bug 'select for update' does not correctly lock the data when a normal table join a partition table. [#26631](https://github.com/pingcap/tidb/pull/26631)
    - Fix a panic when select for update on a normal table join a partition table [#26563](https://github.com/pingcap/tidb/pull/26563)
    - Fix the issue that point get does not use lite version resolve lock [#26562](https://github.com/pingcap/tidb/pull/26562)

+ TiKV

    - Fix bug when TiKV upgrade from 3.0 to 4.x and 5.x but there are still some files left by import. [#10912](https://github.com/tikv/tikv/pull/10912)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10873](https://github.com/tikv/tikv/pull/10873)
    - TiKV coprocessor slow log will only consider time spent on processing the request.
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10865](https://github.com/tikv/tikv/pull/10865)
    - Bug fix: fix an unexpected panic when exceeds deadline on processing copr requests. [#10856](https://github.com/tikv/tikv/pull/10856)
    - Fix TiKV panic when enable Titan and upgrade from pre-5.0 version
    - Fix newer TiKV can't rollback to 5.0.x [#10842](https://github.com/tikv/tikv/pull/10842)
    - Fix TiKV delete files before it ingests to RocksDB. [#10741](https://github.com/tikv/tikv/pull/10741)
    - Support changing CDC configs dynamically [#10686](https://github.com/tikv/tikv/pull/10686)
    - Reduce resolved ts message size to save network bandwidth. [#10679](https://github.com/tikv/tikv/pull/10679)
    - Fix the resolve failures caused by the left pessimisic locks. [#10653](https://github.com/tikv/tikv/pull/10653)
    - limit the hotspot report count. [#10621](https://github.com/tikv/tikv/pull/10621)

+ PingCAP/TiFlash

    - function result name should contain collator info [#2819](https://github.com/pingcap/tics/pull/2819)
    - Support INET6_ATON and INET6_NTOA in TiFlash. [#2624](https://github.com/pingcap/tics/pull/2624)
    - Support INET_ATON and INET_NTOA in TiFlash. [#2613](https://github.com/pingcap/tics/pull/2613)
    - update client to fix race bug [#2583](https://github.com/pingcap/tics/pull/2583)
    - expand streams after aggregation [#2537](https://github.com/pingcap/tics/pull/2537)
    - Improve the mpp cancel process to cancel the mpp task ASAP [#2518](https://github.com/pingcap/tics/pull/2518)
    - Fix the bug may cause metrics to display error value. [#2469](https://github.com/pingcap/tics/pull/2469)

+ PD

    - allow empty region to be scheduled and use a sperate tolerance config in scatter range scheduler [#4117](https://github.com/tikv/pd/pull/4117)
    - Improved the performance of synchronizing Region information between PDs. [#3933](https://github.com/tikv/pd/pull/3933)

+ Tools

    + Backup & Restore (BR)

        - fix the bug that the average speed isn't accurate in backup and restore [#1412](https://github.com/pingcap/br/pull/1412)

    + Dumpling

        - fix pending on show table status in some mysql version [#333](https://github.com/pingcap/dumpling/pull/333)
        - Support for backing up MySQL compatible databases that don't support START TRANSACTION  ... WITH CONSISTENT SNAPSHOT
        - Support for backing up MySQL compatible databases that don't support SHOW CREATE TABLE [#328](https://github.com/pingcap/dumpling/pull/328)

    + TiCDC

        - Fix json encoding could panic when processing a string type value in some cases. [#2783](https://github.com/pingcap/ticdc/pull/2783)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2729](https://github.com/pingcap/ticdc/pull/2729)
        - Fix OOM when TiCDC captures too many regions [#2725](https://github.com/pingcap/ticdc/pull/2725)
        - Fix gRPC keepalive error when memory pressure is high. [#2720](https://github.com/pingcap/ticdc/pull/2720)
        - Optimize memory management when unified sorter is using memory to sort. [#2712](https://github.com/pingcap/ticdc/pull/2712)
        - Set compatible version from 5.1.0-alpha to 5.2.0-alpha [#2659](https://github.com/pingcap/ticdc/pull/2659)
        - Fix a bug that causes TiCDC to panic on an unsigned tinyint [#2656](https://github.com/pingcap/ticdc/pull/2656)
        - Fix open protocol, don't output an empty value when there is no change in one transaction. [#2621](https://github.com/pingcap/ticdc/pull/2621)
        - Fixed a bug in DDL handling when the owner restarts. [#2607](https://github.com/pingcap/ticdc/pull/2607)
        - Prohibit operating TiCDC clusters across major and minor versions [#2599](https://github.com/pingcap/ticdc/pull/2599)
        - Fix a bug in metadata management [#2559](https://github.com/pingcap/ticdc/pull/2559)
        - Add a global gRPC connection pool and share gRPC connections among kv clients. [#2534](https://github.com/pingcap/ticdc/pull/2534)
        - Fix a bug that multiple processors could write the same table when this table is re-scheduling [#2493](https://github.com/pingcap/ticdc/pull/2493)
        - Optimize workerpool for fewer goroutines when concurrency is high. [#2488](https://github.com/pingcap/ticdc/pull/2488)
        - Fix a bug that owner could meet ErrSchemaStorageTableMiss error and reset a changefeed by accident. [#2459](https://github.com/pingcap/ticdc/pull/2459)
        - fix the bug that changefeed cannot be removed if meet GcTTL Exceeded Error [#2454](https://github.com/pingcap/ticdc/pull/2454)
        - fix a bug where synchronizing large tables to cdclog failed. [#2446](https://github.com/pingcap/ticdc/pull/2446)
        - Fix CLI back-compatibility [#2414](https://github.com/pingcap/ticdc/pull/2414)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2378](https://github.com/pingcap/ticdc/pull/2378)