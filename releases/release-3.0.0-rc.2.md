---
title: TiDB 3.0.0-rc.2 Release Notes
aliases: ['/docs/dev/releases/release-3.0.0-rc.2/','/docs/dev/releases/3.0.0-rc.2/']
---

# TiDB 3.0.0-rc.2 Release Notes

Release date: May 28, 2019

TiDB version: 3.0.0-rc.2

TiDB Ansible version: 3.0.0-rc.2

## Overview

On May 28, 2019, TiDB 3.0.0-rc.2 is released. The corresponding TiDB Ansible version is 3.0.0-rc.2. Compared with TiDB 3.0.0-rc.1, this release has greatly improved the stability, usability, features, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ SQL Optimizer
    - Support Index Join in more scenarios [#10540](https://github.com/pingcap/tidb/pull/10540)
    - Support exporting historical statistics [#10291](https://github.com/pingcap/tidb/pull/10291)
    - Support the incremental `Analyze` operation on monotonically increasing index columns [#10355](https://github.com/pingcap/tidb/pull/10355)
    - Neglect the NULL value in the `Order By` clause [#10488](https://github.com/pingcap/tidb/pull/10488)
    - Fix the wrong schema information calculation of the `UnionAll` logical operator when simplifying the column information [#10384](https://github.com/pingcap/tidb/pull/10384)
    - Avoid modifying the original expression when pushing down the `Not` operator [#10363](https://github.com/pingcap/tidb/pull/10363/files)
    - Support the `dump`/`load` correlation of histograms [#10573](https://github.com/pingcap/tidb/pull/10573)

+ Execution Engine
    - Handle virtual columns with a unique index properly when fetching duplicate rows in `batchChecker` [#10370](https://github.com/pingcap/tidb/pull/10370)
    - Fix the scanning range calculation issue for the `CHAR` column [#10124](https://github.com/pingcap/tidb/pull/10124)
    - Fix the issue of `PointGet` incorrectly processing negative numbers [#10113](https://github.com/pingcap/tidb/pull/10113)
    - Merge `Window` functions with the same name to improve execution efficiency [#9866](https://github.com/pingcap/tidb/pull/9866)
    - Allow the `RANGE` frame in a `Window` function to contain no `OrderBy` clause [#10496](https://github.com/pingcap/tidb/pull/10496)

+ Server
    - Fix the issue that TiDB continuously creates a new connection to TiKV when a fault occurs in TiKV [#10301](https://github.com/pingcap/tidb/pull/10301)
    - Make `tidb_disable_txn_auto_retry` affect all retryable errors instead of only write conflict errors [#10339](https://github.com/pingcap/tidb/pull/10339)
    - Allow DDL statements without parameters to be executed using `prepare`/`execute` [#10144](https://github.com/pingcap/tidb/pull/10144)
    - Add the `tidb_back_off_weight` variable to control the backoff time [#10266](https://github.com/pingcap/tidb/pull/10266)
    - Prohibit TiDB retrying non-automatically committed transactions in default conditions by setting the default value of `tidb_disable_txn_auto_retry` to `on` [#10266](https://github.com/pingcap/tidb/pull/10266)
    - Fix the database privilege judgment of `role` in `RBAC` [#10261](https://github.com/pingcap/tidb/pull/10261)
    - Support the pessimistic transaction model (experimental) [#10297](https://github.com/pingcap/tidb/pull/10297)
    - Reduce the wait time for handling lock conflicts in some cases [#10006](https://github.com/pingcap/tidb/pull/10006)
    - Make the Region cache able to visit follower nodes when a fault occurs in the leader node [#10256](https://github.com/pingcap/tidb/pull/10256)
    - Add the `tidb_low_resolution_tso` variable to control the number of TSOs obtained in batches and reduce the times of transactions obtaining TSO to adapt for scenarios where data consistency is not so strictly required [#10428](https://github.com/pingcap/tidb/pull/10428)

+ DDL
    - Fix the uppercase issue of the charset name in the storage of the old version of TiDB [#10272](https://github.com/pingcap/tidb/pull/10272)
    - Support `preSplit` of table partition, which pre-allocates table Regions when creating a table to avoid write hotspots after the table is created [#10221](https://github.com/pingcap/tidb/pull/10221)
    - Fix the issue that TiDB incorrectly updates the version information in PD in some cases [#10324](https://github.com/pingcap/tidb/pull/10324)
    - Support modifying the charset and collation using the `ALTER DATABASE` statement [#10393](https://github.com/pingcap/tidb/pull/10393)
    - Support splitting Regions based on the index and range of the specified table  to relieve hotspot issues [#10203](https://github.com/pingcap/tidb/pull/10203)
    - Prohibit modifying the precision of the decimal column using the `alter table` statement [#10433](https://github.com/pingcap/tidb/pull/10433)
    - Fix the restriction for expressions and functions in hash partition [#10273](https://github.com/pingcap/tidb/pull/10273)
    - Fix the issue that adding indexes in a table that contains partitions will in some cases cause TiDB panic [#10475](https://github.com/pingcap/tidb/pull/10475)
    - Validate table information before executing the DDL to avoid invalid table schemas [#10464](https://github.com/pingcap/tidb/pull/10464)
    - Enable hash partition by default; and enable range columns partition when there is only one column in the partition definition [#9936](https://github.com/pingcap/tidb/pull/9936)

## PD

- Enable the Region storage by default to store the Region metadata [#1524](https://github.com/pingcap/pd/pull/1524)
- Fix the issue that hot Region scheduling is preempted by another scheduler [#1522](https://github.com/pingcap/pd/pull/1522)
- Fix the issue that the priority for the leader does not take effect [#1533](https://github.com/pingcap/pd/pull/1533)
- Add the gRPC interface for `ScanRegions` [#1535](https://github.com/pingcap/pd/pull/1535)
- Push operators actively [#1536](https://github.com/pingcap/pd/pull/1536)
- Add the store limit mechanism for separately controlling the speed of operators for each store [#1474](https://github.com/pingcap/pd/pull/1474)
- Fix the issue of inconsistent `Config` status [#1476](https://github.com/pingcap/pd/pull/1476)

## TiKV

+ Engine
    - Support multiple column families sharing a block cache [#4563](https://github.com/tikv/tikv/pull/4563)

+ Server
    - Remove `TxnScheduler` [#4098](https://github.com/tikv/tikv/pull/4098)
    - Support pessimistic lock transactions [#4698](https://github.com/tikv/tikv/pull/4698)

+ Raftstore
    - Support hibernate Regions to reduce the consumption of the raftstore CPU [#4591](https://github.com/tikv/tikv/pull/4591)
    - Fix the issue that the leader does not reply to the `ReadIndex` requests for the learner [#4653](https://github.com/tikv/tikv/pull/4653)
    - Fix transferring leader failures in some cases [#4684](https://github.com/tikv/tikv/pull/4684)
    - Fix the dirty read issue in some cases [#4688](https://github.com/tikv/tikv/pull/4688)
    - Fix the issue that a snapshot may lose applied data in some cases [#4716](https://github.com/tikv/tikv/pull/4716)

+ Coprocessor
    - Add more RPN functions
        - `LogicalOr` [#4691](https://github.com/tikv/tikv/pull/4601)
        - `LTReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `LEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `GTReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `GEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `NEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `EQReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        - `IsNull` [#4720](https://github.com/tikv/tikv/pull/4720)
        - `IsTrue` [#4720](https://github.com/tikv/tikv/pull/4720)
        - `IsFalse` [#4720](https://github.com/tikv/tikv/pull/4720)
        - Support comparison arithmetic for `Int` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support comparison arithmetic for `Decimal` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support comparison arithmetic for `String` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support comparison arithmetic for `Time` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support comparison arithmetic for `Duration` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support comparison arithmetic for `Json` [#4625](https://github.com/tikv/tikv/pull/4625)
        - Support plus arithmetic for `Int` [#4733](https://github.com/tikv/tikv/pull/4733)
        - Support plus arithmetic for `Real` [#4733](https://github.com/tikv/tikv/pull/4733)
        - Support plus arithmetic for `Decimal` [#4733](https://github.com/tikv/tikv/pull/4733)
        - Support MOD functions for `Int` [#4727](https://github.com/tikv/tikv/pull/4727)
        - Support MOD functions for `Real` [#4727](https://github.com/tikv/tikv/pull/4727)
        - Support MOD functions for `Decimal` [#4727](https://github.com/tikv/tikv/pull/4727)
        - Support minus arithmetic for `Int` [#4746](https://github.com/tikv/tikv/pull/4746)
        - Support minus arithmetic for `Real` [#4746](https://github.com/tikv/tikv/pull/4746)
        - Support minus arithmetic for `Decimal` [#4746](https://github.com/tikv/tikv/pull/4746)

## Tools

+ TiDB Binlog
    - Add a metric to track the delay of data replication downstream [#594](https://github.com/pingcap/tidb-binlog/pull/594)

+ TiDB Lightning

    - Support merging sharded databases and tables [#95](https://github.com/pingcap/tidb-lightning/pull/95)
    - Add the retry mechanism for KV write failure [#176](https://github.com/pingcap/tidb-lightning/pull/176)
    - Update the default value of `table-concurrency` to 6 [#175](https://github.com/pingcap/tidb-lightning/pull/175)
    - Reduce required configuration items by automatically discovering `tidb.pd-addr` and `tidb.port` if they are not provided [#173](https://github.com/pingcap/tidb-lightning/pull/173)
