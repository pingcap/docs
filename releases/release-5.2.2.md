---
title: TiDB 5.2.2 Release Notes
---

# TiDB 5.2.2 Release Notes

Release Date: October 27, 2021

TiDB version: 5.2.2

## Compatibility change(s)

## Feature enhancement(s)

## Improvements

+ TiDB

    - Show information about SQL statement in the debug log about coprocessor encountering lock [#27718](https://github.com/pingcap/tidb/issues/27718)
    - Add backup and restore size for TiDB SQL backup/restore task . [#27247](https://github.com/pingcap/tidb/issues/27247)

+ TiKV

    - Simplify the algorithm of L0 flow control [#10879](https://github.com/tikv/tikv/issues/10879)
    - Improve the error log report in raft client module [#10983](https://github.com/tikv/tikv/pull/10983)
    - Make the slow log of TiKV coprocessor only consider the time spent on processing requests [#10841](https://github.com/tikv/tikv/issues/10841)
    - Drop log instead of blocking threads when the slogger thread is overloaded and the queue is filled up [#10841](https://github.com/tikv/tikv/issues/10841)
    - Add more statistics types of write queries (https://github.com/tikv/tikv/issues/10507)

+ PD

    - Add more types of write queries to QPS dimensions in the hotspot scheduler [#3869](https://github.com/tikv/pd/issues/3869)
    - Support dynamically adjusting the retry limit of the balance region scheduler to improve the performance of the scheduler [#3744 (https://github.com/tikv/pd/issues/3744)
    - Update TiDB Dashboard to v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093 (https://github.com/tikv/pd/issues/4093) 
    - Speed up the exit process of a scheduler after receiving an end-of-process signal [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

## Bug Fixes

+ TiDB

    - Fix the issue that plan-cache cannot be aware of changes of unsigned flags [#28254](https://github.com/pingcap/tidb/issues/28254)
    - Fix the wrong partition pruning when some conditions are out of range  [#28233](https://github.com/pingcap/tidb/issues/28233)
    - Fix the issue that planner may cache invalid plans for joins in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix wrong index hash join when hash col is enum. [#27893](https://github.com/pingcap/tidb/issues/27893)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#27688](https://github.com/pingcap/tidb/pull/27688)
    - Fixed Lightning panic when it failed to perform checksum on target cluster. [#27686](https://github.com/pingcap/tidb/pull/27686)
    - Fix the wrong result for date_add and date_sub in some cases. [#27232](https://github.com/pingcap/tidb/issues/27232)
    - Fix wrong result of hour function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fixed a bug where MySQL 5.1 and older clients had issues authenticating [#27855](https://github.com/pingcap/tidb/issues/27855)
    - fix auto analyze may get triggered out of specified time. [#28698](https://github.com/pingcap/tidb/issues/28698)
    - Fix the bug that setting any session variable will make `tidb_snapshot` unwork. [#28683](https://github.com/pingcap/tidb/pull/28683)
    - Fixed a bug that caused BR get stuck when many missing-peer regions in cluster. [#27534](https://github.com/pingcap/tidb/issues/27534)
    - Fix unexpected error like `tidb_cast to Int32 is not supported` when unsupported cast is pushed down to TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)
    - Fix error message for DECIMAL overflow is just "ERROR 1690 (22003): %s value is out of range in '%s'" [#27964](https://github.com/pingcap/tidb/issues/27964)
    - Fix bug that MPP node availability detect does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix data-race bug when alloc MPP task ID [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix index out of bound bug when empty dual table is remove for MPP query [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    - Fix the issue of error log `can not found column in Schema column` for MPP queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix the issue that TiDB might crash when TiFlash shuts down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Remove the support for insecure 3DES (Triple Data Encryption Algorithm) based TLS ciphersuites [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Fix the issue that Lightning connects to  offline TiKV nodes during pre-check and causes import failures [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Fix the issue that pre-check cost too much time when importing many files to tables [#27605](https://github.com/pingcap/tidb/issues/27605)
    - Fix the issue that rewriting expressions makes `between` infer wrong collation [#27146](https://github.com/pingcap/tidb/issues/27146)
    - Fix the issue that `group_concat` function did not consider the collation [#27429](https://github.com/pingcap/tidb/issues/27429)
    - Fix the issue that `extract` function gives wrong results when argument is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
    - Fix the issue that creating partition fails if `NO_UNSIGNED_SUBTRACTION` is set [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Avoid expressions with side effects in column pruning and aggregation pushdown [#27106](https://github.com/pingcap/tidb/issues/27106)
    - Remove useless GRPC log in production [#24190](https://github.com/pingcap/tidb/issues/24190)
    - Limit the valid decimal length to fix precision-related issues [#3091](https://github.com/pingcap/tics/issues/3091)
    - Fix the issue of a wrong way to check for overflow in `plus` expression [#26977](https://github.com/pingcap/tidb/issues/26977)
    - Fix the issue of `data too long` error when dumping statistics from the table with new collation data [#27024](https://github.com/pingcap/tidb/issues/27024)
    - Fix the issue that the retried transactions' statements are not included in TIDB_TRX [#28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

    - Fix the issue that CDC add scan retries frequently due to Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix that the raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix the issue that concurrent leaks in `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)
    - Fix a panic issue that occurs to coprocessor when response size exceeds 4 GiB [#9012](https://github.com/tikv/tikv/issues/9012)
     - Fix the issue that snapshot Garbage Collection (GC) misses GC snapshot files when snapshot files cannot be garbage collected [#10813](https://github.com/tikv/tikv/issues/10813)
     - Fix a panic issue that occurs when processing coprocessor requests times out [#10852](https://github.com/tikv/tikv/issues/10852)

+ PD

    - Fix the issue that PD incorrectly delete the peers with data and in pending status because the number of peers exceeds the number of configured peers [#4045](https://github.com/tikv/pd/issues/4045)
    - Fix the issue that PD does not fix down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the issue that the scatter range scheduler cannot schedule empty regions [#4118](https://github.com/tikv/pd/pull/4118)
    - Fix the issue that the key manager cost too much CPU [#4071](https://github.com/tikv/pd/issues/4071)
    - Fix the data race issue that might occur when setting configurations of hot region scheduler [#4170](https://github.com/tikv/pd/pull/4170)
   - Fix slow leader election caused by stucked region syncer[#3936](https://github.com/tikv/pd/issues/3936)

+ TiFlash

    - Fix the issue that TiFlash fails to start up under platform without library `nsl`

+ Tools

    + TiCDC

