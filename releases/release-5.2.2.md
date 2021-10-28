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

    - Show information about SQL statement in the debug log about coprocessor encountering lock [#27924](https://github.com/pingcap/tidb/pull/27924)
    - Add backup and restore size for TiDB SQL brie task . [#27727](https://github.com/pingcap/tidb/pull/27727)

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

    - Fix the issue that plan-cache cannot be aware of changes of unsigned flags [#28837](https://github.com/pingcap/tidb/pull/28837)
    - Fix the wrong partition pruning when some conditions are out of range  [#28820](https://github.com/pingcap/tidb/pull/28820)
    - Fix the issue that planner may cache invalid plans for joins in some cases [#28447](https://github.com/pingcap/tidb/pull/28447)
    - Fix wrong index hash join when hash col is enum. [#28082](https://github.com/pingcap/tidb/pull/28082)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#27688](https://github.com/pingcap/tidb/pull/27688)
    - Fixed Lightning panic when it failed to perform checksum on target cluster. [#27686](https://github.com/pingcap/tidb/pull/27686)
    - Fix the wrong result for date_add and date_sub in some cases. [#27454](https://github.com/pingcap/tidb/pull/27454)
    - Fix wrong result of hour function in vectorized expression [#28874](https://github.com/pingcap/tidb/pull/28874)
    - Fixed a bug where MySQL 5.1 and older clients had issues authenticating [#28734](https://github.com/pingcap/tidb/pull/28734)
    - fix auto analyze may get triggered out of specified time. [#28725](https://github.com/pingcap/tidb/pull/28725)
    - Fix the bug that setting any session variable will make `tidb_snapshot` unwork. [#28683](https://github.com/pingcap/tidb/pull/28683)
    - Fixed a bug that caused BR get stuck when many missing-peer regions in cluster. [#28680](https://github.com/pingcap/tidb/pull/28680)
    - Fix unexpected error like `tidb_cast to Int32 is not supported` when unsupported cast is pushed down to TiFlash [#28654](https://github.com/pingcap/tidb/pull/28654)
    - Fix error message for DECIMAL overflow is just "ERROR 1690 (22003): %s value is out of range in '%s'" [#28439](https://github.com/pingcap/tidb/pull/28439)
    - Fix bug that mpp node availability detect does not work in some corner cases [#28289](https://github.com/pingcap/tidb/pull/28289)
    - Fix data-race bug when alloc MPP task ID [#28283](https://github.com/pingcap/tidb/pull/28283)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28280](https://github.com/pingcap/tidb/pull/28280)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28264](https://github.com/pingcap/tidb/pull/28264)
    - Fix `can not found column in Schema column` error for mpp queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix a bug that TiDB may crash when TiFlash is shutting down. [#28140](https://github.com/pingcap/tidb/pull/28140)
    - Support for 3DES based TLS ciphersuites was removed [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Do not check multi-ingest when store is offline. [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Fix the issue that pre-check cost too much time when import too many files for tables. [#27623](https://github.com/pingcap/tidb/pull/27623)
    - Fix expression rewrite makes `between` infers wrong collation. [#27550](https://github.com/pingcap/tidb/pull/27550)
    - Make `group_concat` function consider the collation [#27530](https://github.com/pingcap/tidb/pull/27530)
    - Fix extract bug when argument is a negative duration [#27366](https://github.com/pingcap/tidb/pull/27366)
    - Fix a bug that creates partition fail if `NO_UNSIGNED_SUBTRACTION` is set. [#27100](https://github.com/pingcap/tidb/pull/27100)
    - Avoid expressions with side effects in column pruning and aggregation pushdown. [#27370](https://github.com/pingcap/tidb/pull/27370)
    - Remove useless GRPC log in production.[#27239](https://github.com/pingcap/tidb/pull/27239)
    - Limit the valid decimal length to fix precision-related issues.[#28649](https://github.com/pingcap/tidb/pull/28649)
    - Fix the wrong way to check for overflow in `plus` expression.[#27419](https://github.com/pingcap/tidb/pull/27419)
    - Fix `data too long` error when dumping stats from the table with new collation data.[#27302](https://github.com/pingcap/tidb/pull/27302)
    - Fix retried transactions' statements are not included in TIDB_TRX.[#28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

+ PD

    - Fix the issue that PD would not fix down peers in time [#4084](https://github.com/tikv/pd/pull/4084)
    - Fix the data race issue when setting hot region configuration [#4170](https://github.com/tikv/pd/pull/4170)
    - Fix the issue that key manager cost too much CPU [#4153](https://github.com/tikv/pd/pull/4153)
    - Fix the issue that PD may remove the wrong pending peer if the peer count exceeds the limit [#4075](https://github.com/tikv/pd/pull/4075)
    - Fix the issue that scatter range scheduler cannot schedule the empty region [#4118](https://github.com/tikv/pd/pull/4118)
    - Fix the issue that PD may not elect a new leader as soon as the leader steps down [#4220](https://github.com/tikv/pd/pull/4220)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4220](https://github.com/tikv/pd/pull/4220)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4132](https://github.com/tikv/pd/pull/4132)
    - Fix the bug that PD would not fix down-peer in time. [#4084](https://github.com/tikv/pd/pull/4084)

+ TiFlash

    - Fix the issue that TiFlash fails to start up under platform without library `nsl`

+ Tools

    + TiCDC

## __unsorted

+ TiKV

    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11092](https://github.com/tikv/tikv/pull/11092)
    - Simplify the algorithm of L0 flow control [#11081](https://github.com/tikv/tikv/pull/11081)
    - fix channel full could break the raft connection [#11073](https://github.com/tikv/tikv/pull/11073)
    - Fix the issue #9714. Now RaftClient will check the size of RaftMessage.extra_ctx and RaftMessage.message.context size as part of its message size estimate. [#11066](https://github.com/tikv/tikv/pull/11066)
    - rename config resource-metering.agent_address to resource-metering.receiver_address [#11023](https://github.com/tikv/tikv/pull/11023)
    - resolved_ts: fix coroutine leaking [#11020](https://github.com/tikv/tikv/pull/11020)
    - Hide untouched storage commands' metrics in grafana dashboard [#11003](https://github.com/tikv/tikv/pull/11003)
    - Fix panic in coprocessor when response size exceeds 4GiB [#10993](https://github.com/tikv/tikv/pull/10993)
    - improve raft client error log report [#10983](https://github.com/tikv/tikv/pull/10983)
    - RaftStore Snapshot GC fix: fix the issue that snapshot GC missed GC snapshot files when there's one snapshot file failed to be GC-ed. [#10874](https://github.com/tikv/tikv/pull/10874)
    - TiKV coprocessor slow log will only consider time spent on processing the request. 
    - Drop log instead of blocking threads when slogger thread is overloaded and queue is filled up. [#10866](https://github.com/tikv/tikv/pull/10866)
    - Bug fix: fix an unexpected panic when exceeds deadline on processing copr requests. [#10857](https://github.com/tikv/tikv/pull/10857)
    - None. [#10809](https://github.com/tikv/tikv/pull/10809)
