---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 Release Notes

Release Date: September 27, 2021

TiDB version: 5.1.2

## Compatibility changes

+ Tools

    + TiCDC

        - Set compatible version from 5.1.0-alpha to 5.2.0-alpha [#2659](https://github.com/pingcap/ticdc/pull/2659)
        - Prohibit operating TiCDC clusters across major and minor versions [#2599](https://github.com/pingcap/ticdc/pull/2599)
        - Fix the CLI compatibility issue with 4.0.x clusters on the default sort-engine option [#2373](https://github.com/pingcap/ticdc/issues/2373)

## Feature enhancements

+ Tools

    + Dumpling

        - Support for backing up MySQL compatible databases that do not support `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` and `SHOW CREATE TABLE`  [#328](https://github.com/pingcap/dumpling/pull/328)
        - Add a global `gRPC` connection pool and share `gRPC` connections among `kv` clients [#2534](https://github.com/pingcap/ticdc/pull/2534)

## Improvements

+ TiDB

    - Trigger auto-analyze by histogram row count, increase the accuracy of this trigger action  [#24237](https://github.com/pingcap/tidb/issues/24237)
    - Push down mod() to TiFlash, increase the query performance. [#2318](https://github.com/pingcap/tics/issues/2318)
+ TiKV

    - Support dynamically modifying CDC (Change Data Capture) configurations [#10645](https://github.com/tikv/tikv/issues/10645)
    - Reduce the size of Resolved TS message to save network bandwidth [#2448](https://github.com/pingcap/ticdc/issues/2448)
    - Limit the counts of peer states (PeerStat) in the heartbeat message reported by a single store [#10621](https://github.com/tikv/tikv/pull/10621)

+ PD

    - Allow empty regions to be scheduled and use a separate tolerance configuration in scatter range scheduler [#4117](https://github.com/tikv/pd/pull/4117)
    - Improve the performance of synchronizing Region information between PDs [#3933](https://github.com/tikv/pd/pull/3933)
    - Support dynamically adjusting the retry limit of a store based on generated Operator [#4048](https://github.com/tikv/pd/pull/4048)

+ TiFlash

    - Support the `DATE()` function
    - Add write throughput per instance to Grafana panels
    - Optimize the performance of the `leader-read` process
    - Accelerate the process of canceling `MPP` tasks

+ Tools

    + TiCDC

        - Optimize memory management when the Unified Sorter is using memory to sort [#2712](https://github.com/pingcap/ticdc/pull/2712)
        - Optimize workerpool for fewer goroutines when concurrency is high [#2488](https://github.com/pingcap/ticdc/pull/2488)
        - Reduce goroutine usage when a table's region transfer away from a TiKV node [#2284](https://github.com/pingcap/ticdc/issues/2284)

## Bug Fixes

+ TiDB

    - Fix  the potential wrong results of index hash join when the hash column is in the ENUM type [#27893](https://github.com/pingcap/tidb/issues/27893)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases [#27678](https://github.com/pingcap/tidb/pull/27678)
    - Fix the compatibility issue of the overflow check by keeping the same logic as MySQL [#23897](https://github.com/pingcap/tidb/issues/23897)
    - Fix the issue that TiDB returns an `unknow` error while it should return the `pd is timeout` error [#26147](https://github.com/pingcap/tidb/issues/26147)
    - Fix the error of the case when function caused by the wrong charset and collation [#26662](https://github.com/pingcap/tidb/issues/26662)
    - Fix the issue that `greatest(datetime) union null` returns an empty string [#26532](https://github.com/pingcap/tidb/issues/26532)
    - Fix the potential `can not found column in Schema column` error for MPP queries [#28148](https://github.com/pingcap/tidb/pull/28148)
    - Fix a bug that TiDB may panic when TiFlash is shutting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Fix the issue of wrong range caused by using `enum like 'x%'` [#27130](https://github.com/pingcap/tidb/issues/27130)
    - Fix the issue that the `between` expression infers wrong collation. [#27146](https://github.com/pingcap/tidb/issues/27146)
    - Fix the Common Table Expression (CTE) dead lock issue when used with IndexLookupJoin [#27410](https://github.com/pingcap/tidb/issues/27410)
    - Fix a bug that retryable deadlocks are incorrectly recorded into the `INFORMATION_SCHEMA.DEADLOCKS` table [#27400](https://github.com/pingcap/tidb/issues/27400)
    - Fix a bug that `GROUP_CONCAT` function does not consider the collation [#27429](https://github.com/pingcap/tidb/issues/27429)
    - Fix a bug that the COUNT(DISTINCT) function on multiple columns returns wrong results when New Collation is on [#27091](https://github.com/pingcap/tidb/issues/27091)
    - Fix an issue that the `TABLESAMPLE` query result from partitioned tables is not sorted as expected [#27349](https://github.com/pingcap/tidb/issues/27349)
    - Fix a bug that the EXTRACT function returns wrong results when the argument is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
    - Remove the unused `/debug/sub-optimal-plan`  HTTP API  [#27265](https://github.com/pingcap/tidb/pull/27265)
    - Fix the issue that a wrong selection is pushed down when the HAVING condition is used in the aggregate function [#26496](https://github.com/pingcap/tidb/issues/26496)
    - Fix a bug that the query may return wrong results when the hash partition table deals with unsigned data [#26569](https://github.com/pingcap/tidb/issues/26569)
    - Fix the unexpected behavior when casting an invalid string to DATE [#26762](https://github.com/pingcap/tidb/issues/26762)
    - Fix a bug that creating partition fails if `NO_UNSIGNED_SUBTRACTION` is set [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Fix the issue that the distinct flag is missing when Apply is converted to Join [#26958](https://github.com/pingcap/tidb/issues/26958)
    - Fix the issue that NO_ZERO_IN_DATE does not work on the default values [#26766](https://github.com/pingcap/tidb/issues/26766)
    -  Set a block duration for the newly recovered TiFlash node to avoid blocking queries during this time [#26897](https://github.com/pingcap/tidb/pull/26897)
    - Fix a bug that might occur when the CTE is referenced more than once [#26212](https://github.com/pingcap/tidb/issues/26212)
    - Fix a CTE bug when MergeJoin is used [#25474](https://github.com/pingcap/tidb/issues/25474)
    - Fix a bug that the 'SELECT FOR UPDATE' statement does not correctly lock the data when a normal table joins a partition table [#26251](https://github.com/pingcap/tidb/issues/26251)
    - Fix the issue that the 'SELECT FOR UPDATE' statement returns an error when a normal table joins a partition table [#26250](https://github.com/pingcap/tidb/issues/26250)
    - Fix the issue that `PointGet` does not use the lite version of resolve lock [#26562](https://github.com/pingcap/tidb/pull/26562)

+ TiKV

    - Fix bug when TiKV upgrade from 3.0 to 4.x and 5.x but there are still some files left by import. [#10902](https://github.com/tikv/tikv/issues/10902)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10813](https://github.com/tikv/tikv/issues/10813)
    - TiKV coprocessor slow log will only consider time spent on processing the request. Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10865](https://github.com/tikv/tikv/pull/10865)
    - Bug fix: fix an unexpected panic when exceeds deadline on processing copr requests. [#10852](https://github.com/tikv/tikv/issues/10852)
    - Fix TiKV panic when enable Titan and upgrade from pre-5.0 version. Fix newer TiKV can't rollback to 5.0.x [#10842](https://github.com/tikv/tikv/pull/10842)
    - Fix TiKV delete files before it ingests to RocksDB. [#10438](https://github.com/tikv/tikv/issues/10438)
    - Fix the resolve failures caused by the left pessimisic locks. [#26404](https://github.com/pingcap/tidb/issues/26404)

+ TiFlash

    - Fix the issue of unexpected results when TiFlash fails to establish MPP connections
    - Fix the potential issue of data inconsistency that occurs when TiFlash is deployed on multiple disks
    - Fix a bug that MPP queries get wrong results when TiFlash server is under high load
    - Fix a potential bug that MPP queries hang forever
    - Fix the issue of concurrency problem between store initialization and `DDL`
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN`
    - Fix the potential panic issue when `Snapshot` is applied simultaneously with with multiple DDL operations
    - Fix the issue that the store size in metrics is inaccurate under heavy writing
    - Fix the potential issue that TiFlash cannot perform GC for the delta data after running for a long time
    - Fix the issue of wrong results when `new collation` is enabled
    - Fix the potential panic issue that occurs during lock resolving
    - Fix a bug that metrics display wrong value

+ PD

    - Fix the bug that PD would not fix down-peer in time. [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix an issue where data is not stored when using max-replicas or location-labels to indirectly update default placement rule [#3886](https://github.com/tikv/pd/issues/3886)
    - Fix the bug that PD may panic during scaling out TiKV. [#3911](https://github.com/tikv/pd/pull/3911)
    - Fix the bug that hot region scheduler can not work when the cluster has evict leader scheduler. [#3697](https://github.com/tikv/pd/pull/3697)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the average speed is not accurate during data backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - Fix the issue that Dumpling is pending when `show table status` returns incorrect results in some MySQL versions (8.0.3, 8.0.23) [#333](https://github.com/pingcap/dumpling/pull/333)

    + TiCDC

        - Fix a bug that json encoding may cause panic when processing a string type value that is `string` or `[]byte`. [#2783](https://github.com/pingcap/ticdc/pull/2783)
        - Reduce gRPC window size to avoid OOM [#2725](https://github.com/pingcap/ticdc/pull/2725)
        - Fix gRPC keepalive error under high memory pressure. [#2720](https://github.com/pingcap/ticdc/pull/2720)
        - Fix a bug that an unsigned tinyint causes TiCDC to panic. [#2656](https://github.com/pingcap/ticdc/pull/2656)
        - Fix empty value issue in open protocol. An empty value is no longer output when there is no change in one transaction. [#2612](https://github.com/pingcap/ticdc/issues/2612)
        - Fix a bug in DDL handling during manual restarts. [#2607](https://github.com/pingcap/ticdc/pull/2607)
        - Fix the issue that EtcdWorker's snapshot isolation might be wrongly violated when managing the metadata [#2559](https://github.com/pingcap/ticdc/pull/2559)
        - Fix the issue that multiple processors could write in the same table when re-scheduling this table [#2230](https://github.com/pingcap/ticdc/issues/2230)
        - Fix the issue of the ErrSchemaStorageTableMiss error and that a changefeed is reset by accident. [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - Fix the issue that changefeed cannot be removed when the GcTTL Exceeded Error occors [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - Fix the issue that replicating large tables to `cdclog` fails [#2446](https://github.com/pingcap/ticdc/pull/2446)
