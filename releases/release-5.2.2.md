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
    - Add backup and restore size for TiDB SQL brie task . [#27247](https://github.com/pingcap/tidb/issues/27247)

+ PD

    - Add more write query kind in QPS dimension for hot region scheduler [#4028](https://github.com/tikv/pd/pull/4028)
    - Dynamically adjust the retry limit to improve the performance of the balance region scheduler [#4046](https://github.com/tikv/pd/pull/4046)
    - Update TiDB Dashboard to v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - Support scheduling regions with unhealthy peers for the evict leader scheduler [#4132](https://github.com/tikv/pd/pull/4132)
    - Speed up scheduler exit process when receiving the signal [#4199](https://github.com/tikv/pd/pull/4199)

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
    - Fix bug that mpp node availability detect does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix data-race bug when alloc MPP task ID [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28264](https://github.com/pingcap/tidb/pull/28264)
    - Fix `can not found column in Schema column` error for mpp queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix a bug that TiDB may crash when TiFlash is shutting down. [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Support for 3DES based TLS ciphersuites was removed [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Do not check multi-ingest when store is offline. [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Fix the issue that pre-check cost too much time when import too many files for tables. [#27605](https://github.com/pingcap/tidb/issues/27605)
    - Fix expression rewrite makes `between` infers wrong collation. [#27146](https://github.com/pingcap/tidb/issues/27146)
    - Make `group_concat` function consider the collation [#27429](https://github.com/pingcap/tidb/issues/27429)
    - Fix extract bug when argument is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
    - Fix a bug that creates partition fail if `NO_UNSIGNED_SUBTRACTION` is set. [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Avoid expressions with side effects in column pruning and aggregation pushdown. [#27106](https://github.com/pingcap/tidb/issues/27106)
    - Remove useless GRPC log in production.[#27239](https://github.com/pingcap/tidb/pull/27239)
    - Limit the valid decimal length to fix precision-related issues.[#3091](https://github.com/pingcap/tics/issues/3091)
    - Fix the wrong way to check for overflow in `plus` expression.[#26977](https://github.com/pingcap/tidb/issues/26977)
    - Fix `data too long` error when dumping stats from the table with new collation data.[#27024](https://github.com/pingcap/tidb/issues/27024)
    - Fix retried transactions' statements are not included in TIDB_TRX.[#28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

+ PD

    - Fix the issue that PD would not fix down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the data race issue when setting hot region configuration [#4170](https://github.com/tikv/pd/pull/4170)
    - Fix the issue that key manager cost too much CPU [#4071](https://github.com/tikv/pd/issues/4071)
    - Fix the issue that PD may remove the wrong pending peer if the peer count exceeds the limit [#4045](https://github.com/tikv/pd/issues/4045)
    - Fix the issue that scatter range scheduler cannot schedule the empty region [#4118](https://github.com/tikv/pd/pull/4118)
    - Fix the issue that PD may not elect a new leader as soon as the leader steps down [#3936](https://github.com/tikv/pd/issues/3936)
    - Fix the issue that PD may not elect leader as soon as leader step down [#3936](https://github.com/tikv/pd/issues/3936)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4132](https://github.com/tikv/pd/pull/4132)
    - Fix the bug that PD would not fix down-peer in time. [#4077](https://github.com/tikv/pd/issues/4077)

+ TiFlash

    - Fix the issue that TiFlash fails to start up under platform without library `nsl`

+ Tools

    + TiCDC

## __unsorted

+ TiKV

    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11082](https://github.com/tikv/tikv/issues/11082)
    - Simplify the algorithm of L0 flow control [#10879](https://github.com/tikv/tikv/issues/10879)
    - fix channel full could break the raft connection [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue #9714. Now RaftClient will check the size of RaftMessage.extra_ctx and RaftMessage.message.context size as part of its message size estimate. [#9714](https://github.com/tikv/tikv/issues/9714)
    - rename config resource-metering.agent_address to resource-metering.receiver_address [#11023](https://github.com/tikv/tikv/pull/11023)
    - resolved_ts: fix coroutine leaking [#10965](https://github.com/tikv/tikv/issues/10965)
    - Hide untouched storage commands' metrics in grafana dashboard [#11003](https://github.com/tikv/tikv/pull/11003)
    - Fix panic in coprocessor when response size exceeds 4GiB [#9012](https://github.com/tikv/tikv/issues/9012)
    - improve raft client error log report [#10983](https://github.com/tikv/tikv/pull/10983)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10813](https://github.com/tikv/tikv/issues/10813)
    - TiKV coprocessor slow log will only consider time spent on processing the request. 
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10866](https://github.com/tikv/tikv/pull/10866)
    - Bug fix: fix an unexpected panic when exceeds deadline on processing copr requests. [#10852](https://github.com/tikv/tikv/issues/10852)
    - None. [#10507](https://github.com/tikv/tikv/issues/10507)
