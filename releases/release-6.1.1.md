---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

Release date: 2022-xx-xx

TiDB version: 6.1.1

## Compatibility changes

+ TiDB

    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that `SHOW DATABASES LIKE …` is case-sensitive [#34766](https://github.com/pingcap/tidb/issues/34766)
    - Change the default value of [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) from `1` to `0`, which disables Join Reorder's support for Outer Join is enabled by default.

+ Diagnosis

    - Continuous Profiling is now disabled by default.

## Improvements

- Add some contents in the `TiDB-community-toolkit` binary package. For details, see [TiDB Installation Packages](/binary-package.md).
- Add a document to introduce TiDB's support for different operating systems. See [].

+ TiDB

    <!-- <planner> -->
    (dup: release-6.2.0.md > # Performance)[User document](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323)
    (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966)

    <!-- <transaction> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- Avoid sending requests to unhealthy TiKV nodes to improve availability [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    (dup: release-6.2.0.md > Improvements> TiKV)- Support compressing the metrics response using gzip to reduce the HTTP body size [#12355](https://github.com/tikv/tikv/issues/12355)
    - Support filter useless metrics samples to reduce the metrics data size. [#12355](https://github.com/tikv/tikv/issues/12355)
    (dup: release-6.2.0.md > Improvements> TiKV)- Support dynamically modifying the number of sub-compaction operations performed concurrently in RocksDB (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145)

+ PD

    - 改进 balance region 在空间快均衡阶段的调度速度 [#5320](https://github.com/tikv/pd/pull/5320)

+ Tools

    + TiDB Lightning

        - add retry strategy on `stale command` error [#36877](https://github.com/pingcap/tidb/issues/36877)

    + TiDB Data Migration

        - User can set concurrency for lightning loader [#5505](https://github.com/pingcap/tiflow/issues/5505)

    + TiCDC

        - Add a sink uri parameter `transaction-atomicity` to support splitting the large transaction in a changefeed. This can greatly reduce the lantency and memory consumption of large transactions. [#5231](https://github.com/pingcap/tiflow/issues/5231)
        - Reduce the goroutine number when initializing a capture with lots of regions[#5610](https://github.com/pingcap/tiflow/issues/5610)
        - An enhancement of MySQL sink to turn off safe-mode automatically [#5611](https://github.com/pingcap/tiflow/issues/5611)

## Bug fixes

+ TiDB

    <!-- <execution> -->
    - Fix the issue that IndexLookupHashJoin may hangs when used with limit [#35638](https://github.com/pingcap/tidb/issues/35638)
    - Fix the issue that TiDB may panic during update stmt [#32311](https://github.com/pingcap/tidb/issues/32311)
    - Fix the bug that `show columns` may send cop request [#36496](https://github.com/pingcap/tidb/issues/36496)
    - Fix bug that `show warnings` may return `invalid memory address or nil pointer dereference` error [#31569](https://github.com/pingcap/tidb/issues/31569)
    - Fix the case sensitive issues for `show database like` statement [#34766](https://github.com/pingcap/tidb/issues/34766)
    - Fix bug that static partition prune may return wrong result for agg query if the table is empty [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <planner> -->
    - Fix outer join reorder will push down its outer join condition wrongly [#37238](https://github.com/pingcap/tidb/issues/37238)
    - Fix that cte-schema hashcode is cloned wrongly when cte is referenced more than once [#35404](https://github.com/pingcap/tidb/issues/35404)
    - Fix the wrong join reorder produced by some right outer join [#36912](https://github.com/pingcap/tidb/issues/36912)
    - Fix the wrong nullable value infered for firstrow agg function with EqualAll [#34584](https://github.com/pingcap/tidb/issues/34584)
    - Fix that plan cache cannot work when there's a binding with ignore_plan_cache hint [#34596](https://github.com/pingcap/tidb/issues/34596)
    - Fix the missing exchange between hash-partition window and single-partition window [#35990](https://github.com/pingcap/tidb/issues/35990)
    - Fix that some predicates are wrongly removed after partition pruning [#33966](https://github.com/pingcap/tidb/issues/33966)
    - Fix the wrong default value set for partial aggregation when aggregation is pushed-down [#35295](https://github.com/pingcap/tidb/issues/35295)

    <!-- <sql-infra> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that querying partitioned tables might report "index-out-of-range" and "non used index" errors in some cases [#35181](https://github.com/pingcap/tidb/issues/35181)
    - Fix the issue that when using TiDB with Binlog, the Drainer may crash because the invalid schema version after `ALTER SEQUENCE` statement [#36276](https://github.com/pingcap/tidb/issues/36276)
    - Fix the incorrect TiDB states that may appear on startup under very extreme cases [#36791](https://github.com/pingcap/tidb/issues/36791)
    - Fix the issue that the execution plans for the partition table may show `UnknownPlanID` in TiDB Dashboard. [#35153](https://github.com/pingcap/tidb/issues/35153)

    <!-- <transaction> -->
    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that the column list does not work in the LOAD DATA statement [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    (dup: release-5.3.2.md > Bug Fixes> TiDB)- Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608)
    - Remove the limitation of `tidb_gc_life_time` [#35392](https://github.com/pingcap/tidb/issues/35392)
    - Fix the load data statement dead loop when an empty filed terminator is used [#33298](https://github.com/pingcap/tidb/issues/33298)
    - Fix the long recovery time issue when the hiberate region is used [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - Fix a bug that regions may be overlapped if raftstore is too busy [#13160](https://github.com/tikv/tikv/issues/13160)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue of inconsistent Region size configuration between TiKV and PD [#12518](https://github.com/tikv/tikv/issues/12518)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that encryption keys are not cleaned up when Raft Engine is enabled [#12890](https://github.com/tikv/tikv/issues/12890)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix encryption keys not cleaned up when Raft Engine is enabled [#13123](https://github.com/tikv/tikv/issues/13123)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that the Commit Log Duration of a new Region is too high, which causes QPS to drop [#13077](https://github.com/tikv/tikv/issues/13077)
    - Fix a rare case panic when enabling raft-engine [#12698](https://github.com/tikv/tikv/issues/12698)
    - Avoid redundant log warnings when procfs is not available [#13116](https://github.com/tikv/tikv/issues/13116)
    - Fix the wrong expression of `Unified Read Pool CPU` in dashboard [#13086](https://github.com/tikv/tikv/issues/13086)
    - Make default `region-split-check-diff` not less than bucket size [#12598](https://github.com/tikv/tikv/issues/12598)
    - Fix panics when apply snapshot is aborted and raft engine is enabled [#12470](https://github.com/tikv/tikv/issues/12470)
    - Refactor pd client to avoid potential deadlock(RWR). [#13191](https://github.com/tikv/tikv/issues/13191)

+ PD

    - Fix the issue that the online process is not accurate when having invalid label settings. [#5234](https://github.com/tikv/pd/issues/5234)
    - Fix the problem that grpc handles return errors inappropriately [#5373](https://github.com/tikv/pd/issues/5373)
    - Fix the issue that `/regions/replicated` may return the wrong status [#5095](https://github.com/tikv/pd/issues/5095)
    - 修复 gRPC 处理返回错误不恰当的问题 [#5376](https://github.com/tikv/pd/pull/5376)

+ TiFlash

    (dup: release-5.4.2.md > Bug Fixes> TiFlash)- Fix the issue that TiFlash crashes after dropping a column of a table with clustered indexes in some situations [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - Fix the issue that format throw data truncated error [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - fix the problem that there may be some obsolete data left in storage which cannot be deleted [#5659](https://github.com/pingcap/tiflash/issues/5659)
    - Reduce unnecessary CPU usage in some edge cases [#5409](https://github.com/pingcap/tiflash/issues/5409)
    - Fix a bug that TiFlash can not work in a cluster using ipv6 [#5247](https://github.com/pingcap/tiflash/issues/5247)
    - Fix a panic issue in parallel aggregation when an exception is thrown. [#5356](https://github.com/pingcap/tiflash/issues/5356)

+ Tools

    + TiCDC

        - Fix the wrong maximum compatible version number [#6039](https://github.com/pingcap/tiflow/issues/6039)
        - Fix a bug that may cause cdc server panic if it received a http request before cdc server fully started. [#5639](https://github.com/pingcap/tiflow/issues/5639)
        - Fix ddl sink panic when changefeed syncpoint is enable. [#4934](https://github.com/pingcap/tiflow/issues/4934)
        - Fix a data race in black hole sink. [#5714](https://github.com/pingcap/tiflow/issues/5714)
        - Fix a bug that causes get changefeeds api does not well after cdc server restart. [#5837](https://github.com/pingcap/tiflow/issues/5837)
        - Fix a data race in black hole sink. [#6206](https://github.com/pingcap/tiflow/issues/6206)
        - Fix TiCDC panic issue when disable the old value of changefeed [#6198](https://github.com/pingcap/tiflow/issues/6198)
        - Fix some data consistency problems when enabling redo log  feature.
        [#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859)
        - Fix the performance problem about the redo log by
        writing redo event asynchronously [#6011](https://github.com/pingcap/tiflow/issues/6011)
        - Fix the changefeed stuck problem when enabling sync-point in some special situation [#6827](https://github.com/pingcap/tiflow/issues/6827)
        - Fix the problem when mysql sink connected to ipv6 address[#6135](https://github.com/pingcap/tiflow/issues/6135)

    + Backup & Restore (BR)

        (dup: release-5.4.2.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix a bug that BR reports `ErrRestoreTableIDMismatch` in RawKV mode [#35279](https://github.com/pingcap/tidb/issues/35279)
        - Adjust the backup organization structure and add a store_id related prefix under the backup path. [#30087](https://github.com/pingcap/tidb/issues/30087)
        - Fix the incorrect backup time costs in log [#35553](https://github.com/pingcap/tidb/issues/35553)

    + Dumpling

        - use net.JoinHostPort to generate host-port part of URI [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Lightning

        - fix connect to tidb when using ipv6 host [#35880](https://github.com/pingcap/tidb/issues/35880)
        - add ReadIndexNotReady as retryable ingest error [#36566](https://github.com/pingcap/tidb/issues/36566)
        - hide sensitive log for server mode lightning [#36374](https://github.com/pingcap/tidb/issues/36374)
        - support column starts with slash/number/non-ascii for parquet file [36980](https://github.com/pingcap/tidb/issues/36980)
        - Fix panic when downstream table schema has changed [#37233](https://github.com/pingcap/tidb/pull/37233)

    + TiDB Binlog

        - [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    + TiDB Data Migration

        - Fix the 'txn-entry-size-limit' config is not effective in DM [#6161](https://github.com/pingcap/tiflow/issues/6161)
        - Fix a bug that get tables without using quote schema name [#5895](https://github.com/pingcap/tiflow/issues/5895)
        - Fix the issue of the possible data race in query-status [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - Fix different output format for `operate-schema` command [#5688](https://github.com/pingcap/tiflow/issues/5688)
        - Fix goroutine leak when relay meet error [#6193](https://github.com/pingcap/tiflow/issues/6193)
        - Fix issue of DM Worker may stuck when get DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733)
