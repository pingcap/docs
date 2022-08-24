---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

Release date: 2022-xx-xx

TiDB version: 6.1.1

## Compatibility changes

+ TiDB

    (dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that `SHOW DATABASES LIKE …` is case-sensitive [#34766](https://github.com/pingcap/tidb/issues/34766)

## Improvements

+ TiDB

<!-- <planner> -->
(dup: release-6.2.0.md > # Performance)[User document](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323)
(dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966)

<!-- <transaction> -->
(dup: release-6.2.0.md > Bug fixes> TiDB)- Avoid sending requests to unhealthy TiKV nodes to improve availability [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - In the new backup organization structure, we will see: `./br backup --pd "127.0.0.1:2379" -s "s3://backup/20220621" - After br command finished, we will have the structure below. ➜ backup tree . . └── 20220621 ├── backupmeta ├── store1 │ └── backup-xxx.sst ├── store100 │ └── backup-yyy.sst ├── store2 │ └── backup-zzz.sst ├── store3 ├── store4 └── store5` [#13063](https://github.com/tikv/tikv/issues/13063)
    (dup: release-6.2.0.md > Improvements> TiKV)- Support compressing the metrics response using gzip to reduce the HTTP body size [#12355](https://github.com/tikv/tikv/issues/12355)

## Bug fixes

+ TiDB

<!-- <execution> -->
- executor: fix index_lookup_hash_join hang when used with limit [#35638](https://github.com/pingcap/tidb/issues/35638)

<!-- <planner> -->
- planner: fix outer join reorder will push down its outer join condition [#37238](https://github.com/pingcap/tidb/issues/37238)
- planner: fix cte-schema-clone will clone the old hashcode of its column if any [#35404](https://github.com/pingcap/tidb/issues/35404)

<!-- <sql-infra> -->
(dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that querying partitioned tables might report "index-out-of-range" and "non used index" errors in some cases [#35181](https://github.com/pingcap/tidb/issues/35181)
- ddl: fix alter sequence will generate schemaVer=0 when alter options are the same as the old [#36276](https://github.com/pingcap/tidb/issues/36276)
- Fix that incorrect TiDB states may appear on startup under very, very, very extreme cases [#36791](https://github.com/pingcap/tidb/issues/36791)
- Fix the "UnknownPlanID" issue. [#35153](https://github.com/pingcap/tidb/issues/35153)

<!-- <transaction> -->
(dup: release-6.2.0.md > Bug fixes> TiDB)- Fix the issue that the column list does not work in the LOAD DATA statement [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
(dup: release-5.3.2.md > Bug Fixes> TiDB)- Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608)

+ TiKV

    - Fix a bug that regions may be overlapped if raftstore is too busy [#13160](https://github.com/tikv/tikv/issues/13160)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934)
    - remove call_option to avoid deadlock(RWR). [#13191](https://github.com/tikv/tikv/issues/13191)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue of inconsistent Region size configuration between TiKV and PD [#12518](https://github.com/tikv/tikv/issues/12518)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that encryption keys are not cleaned up when Raft Engine is enabled [#12890](https://github.com/tikv/tikv/issues/12890)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    - Fix potential deadlock in `RpcClient` when two read locks are interleaved by a write lock. [#12933](https://github.com/tikv/tikv/issues/12933)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix encryption keys not cleaned up when Raft Engine is enabled [#13123](https://github.com/tikv/tikv/issues/13123)
    (dup: release-6.2.0.md > Bug fixes> TiKV)- Fix the issue that the Commit Log Duration of a new Region is too high, which causes QPS to drop [#13077](https://github.com/tikv/tikv/issues/13077)
    (dup: release-6.2.0.md > Improvements> TiKV)- Support dynamically modifying the number of sub-compaction operations performed concurrently in RocksDB (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145)

+ PD

    - Fix the issue that the online process is not accurate when having invalid label settings. [#5234](https://github.com/tikv/pd/issues/5234)
    - grpc: fix the wrong error handler [#5373](https://github.com/tikv/pd/issues/5373)
    - Fix the issue that `/regions/replicated` may return the wrong status [#5095](https://github.com/tikv/pd/issues/5095)

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

    + Backup & Restore (BR)

        (dup: release-5.4.2.md > Bug Fixes> Tools> Backup & Restore (BR))- Fix a bug that BR reports `ErrRestoreTableIDMismatch` in RawKV mode [#35279](https://github.com/pingcap/tidb/issues/35279)

    + Dumpling

        - use net.JoinHostPort to generate host-port part of URI [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Lightning

        - support column starts with slash/number/non-ascii for parquet file [#36980](https://github.com/pingcap/tidb/issues/36980)
        - fix connect to tidb when using ipv6 host [#35880](https://github.com/pingcap/tidb/issues/35880)

    + TiDB Binlog

        - [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    + TiDB Data Migration

        - Fix a bug that start DM-worker and `kill` it immediately will not let process stop. [#5836](https://github.com/pingcap/tiflow/issues/5836)
        - use `net.JoinHostPort` to generate host-port part of URI to support ipv6 address. [#6249](https://github.com/pingcap/tiflow/issues/6249)
        - Fix the problem that TiCDC cannot correctly recognize the ipv6 address in SinkURI [#6135](https://github.com/pingcap/tiflow/issues/6135)
        - Fix a bug that relay goroutine and upstream connections may leak when relay meet error [#6193](https://github.com/pingcap/tiflow/issues/6193)
        - Fix the issue of the possible data race that might occur when multiple functions are executing concurrently, some calling Result() and writing into some variables that other functions are trying to read. #4811 [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - `fix a bug that get tables without using quote schema name`. [#5895](https://github.com/pingcap/tiflow/issues/5895)
