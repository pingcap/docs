---
title: TiDB 2.1 RC4 Release Notes
aliases: ['/docs/dev/releases/release-2.1-rc.4/','/docs/dev/releases/21rc4/']
---

# TiDB 2.1 RC4 Release Notes

On October 23, 2018, TiDB 2.1 RC4 is released. Compared with TiDB 2.1 RC3, this release has great improvement in stability, SQL optimizer, statistics information, and execution engine.

## TiDB

+ SQL Optimizer
    - Fix the issue that column pruning of `UnionAll` is incorrect in some cases [#7941](https://github.com/pingcap/tidb/pull/7941)
    - Fix the issue that the result of the `UnionAll` operator is incorrect in some cases [#8007](https://github.com/pingcap/tidb/pull/8007)
+ SQL Execution Engine
    - Fix the precision issue of the `AVG` function [#7874](https://github.com/pingcap/tidb/pull/7874)
    - Support using the `EXPLAIN ANALYZE` statement to check the runtime statistics including the execution time and the number of returned rows of each operator during the query execution process [#7925](https://github.com/pingcap/tidb/pull/7925)
    - Fix the panic issue of the `PointGet` operator when a column of a table appears multiple times in the result set [#7943](https://github.com/pingcap/tidb/pull/7943)
    - Fix the panic issue caused by too large values in the `Limit` subclause [#8002](https://github.com/pingcap/tidb/pull/8002)
    - Fix the panic issue during the execution process of the `AddDate`/`SubDate` statement in some cases [#8009](https://github.com/pingcap/tidb/pull/8009)
+ Statistics
    - Fix the issue of judging the prefix of the histogram low-bound of the combined index as out of range [#7856](https://github.com/pingcap/tidb/pull/7856)
    - Fix the memory leak issue caused by statistics collecting [#7873](https://github.com/pingcap/tidb/pull/7873)
    - Fix the panic issue when the histogram is empty [#7928](https://github.com/pingcap/tidb/pull/7928)
    - Fix the issue that the histogram bound is out of range when the statistics is being uploaded [#7944](https://github.com/pingcap/tidb/pull/7944)
    - Limit the maximum length of values in the statistics sampling process [#7982](https://github.com/pingcap/tidb/pull/7982)
+ Server
    - Refactor Latch to avoid misjudgment of transaction conflicts and improve the execution performance of concurrent transactions [#7711](https://github.com/pingcap/tidb/pull/7711)
    - Fix the panic issue caused by collecting slow queries in some cases [#7874](https://github.com/pingcap/tidb/pull/7847)
    - Fix the panic issue when `ESCAPED BY` is an empty string in the `LOAD DATA` statement [#8005](https://github.com/pingcap/tidb/pull/8005)
    - Complete the “coprocessor error” log information [#8006](https://github.com/pingcap/tidb/pull/8006)
+ Compatibility
    - Set the `Command` field of the `SHOW PROCESSLIST` result to `Sleep` when the query is empty [#7839](https://github.com/pingcap/tidb/pull/7839)
+ Expressions
    - Fix the constant folding issue of the `SYSDATE` function [#7895](https://github.com/pingcap/tidb/pull/7895)
    - Fix the issue that `SUBSTRING_INDEX` panics in some cases [#7897](https://github.com/pingcap/tidb/pull/7897)
+ DDL
    - Fix the stack overflow issue caused by throwing the `invalid ddl job type` error [#7958](https://github.com/pingcap/tidb/pull/7958)
    - Fix the issue that the result of `ADMIN CHECK TABLE` is incorrect in some cases [#7975](https://github.com/pingcap/tidb/pull/7975)

## PD

- Fix the issue that the tombstone TiKV is not removed from Grafana [#1261](https://github.com/pingcap/pd/pull/1261)
- Fix the data race issue when grpc-go configures the status [#1265](https://github.com/pingcap/pd/pull/1265)
- Fix the issue that the PD server gets stuck caused by etcd startup failure [#1267](https://github.com/pingcap/pd/pull/1267)
- Fix the issue that data race might occur during leader switching [#1273](https://github.com/pingcap/pd/pull/1273)
- Fix the issue that extra warning logs might be output when TiKV becomes tombstone [#1280](https://github.com/pingcap/pd/pull/1273)

## TiKV

- Optimize the RocksDB Write stall issue caused by applying snapshots [#3606](https://github.com/tikv/tikv/pull/3606)
- Add raftstore `tick` metrics [#3657](https://github.com/tikv/tikv/pull/3657)
- Upgrade RocksDB and fix the Write block issue and that the source file might be damaged by the Write operation when performing `IngestExternalFile` [#3661](https://github.com/tikv/tikv/pull/3661)
- Upgrade grpcio and fix the issue that “too many pings” is wrongly reported [#3650](https://github.com/tikv/tikv/pull/3650)