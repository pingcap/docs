---
title: TiDB 5.2.2 Release Notes
---



# TiDB 5.2.2 Release Notes

Release Date: October 27, 2021

TiDB version: 5.2.2

## Compatibility change(s)

## Feature enhancement(s)

## Improvements

+ PD

    - Add more write query kind in QPS dimension for hot region scheduler [#4028](https://github.com/tikv/pd/pull/4028)
    - Dynamically adjust the retry limit to improve the performance of the balance region scheduler [#4046](https://github.com/tikv/pd/pull/4046)
    - Support scheduling regions with unhealthy peers for the evict leader scheduler [#4132](https://github.com/tikv/pd/pull/4132)
    - Speed up scheduler exit process when receiving the signal [#4199](https://github.com/tikv/pd/pull/4199)

## Bug Fixes

+ TiDB

    - planner: fix the issue that plan-cache cannot be aware of changes of unsigned flags [#28837](https://github.com/pingcap/tidb/pull/28837)
    - 'None' [#28820](https://github.com/pingcap/tidb/pull/28820)
    - planner: fix the issue that planner may cache invalid plans for joins in some cases [#28447](https://github.com/pingcap/tidb/pull/28447)
    - Fix wrong index hash join when hash col is enum. [#28082](https://github.com/pingcap/tidb/pull/28082)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#27688](https://github.com/pingcap/tidb/pull/27688)
    - Fixed Lightning panic when it failed to perform checksum on target cluster. [#27686](https://github.com/pingcap/tidb/pull/27686)
    - Fix the wrong result for date_add and date_sub in some cases. [#27454](https://github.com/pingcap/tidb/pull/27454)

+ TiFlash

    - Fix the issue that TiFlash fails to start up under platform without library `nsl` [#3207](https://github.com/pingcap/tics/pull/3207)

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

## __unsorted

+ TiDB

    - Fix wrong result of hour function in vectorized expression [#28874](https://github.com/pingcap/tidb/pull/28874)
    - Fixed a bug where MySQL 5.1 and older clients had issues authenticating [#28734](https://github.com/pingcap/tidb/pull/28734)
    - fix auto analyze may get triggered out of specified time. [#28725](https://github.com/pingcap/tidb/pull/28725)
    - Fix the bug that setting any session variable will make `tidb_snapshot` unwork. [#28683](https://github.com/pingcap/tidb/pull/28683)
    - Fixed a bug that caused BR get stuck when many missing-peer regions in cluster. [#28680](https://github.com/pingcap/tidb/pull/28680)
    - Fix unexpected error like `tidb_cast to Int32 is not supported` when unsupported cast is pushed down to TiFlash [#28654](https://github.com/pingcap/tidb/pull/28654)
    - Fix error message for DECIMAL overflow is just "ERROR 1690 (22003): %s value is out of range in '%s'" [#28439](https://github.com/pingcap/tidb/pull/28439)
    - Fix bug that mpp node availability detect does not work in some corner cases [#28289](https://github.com/pingcap/tidb/pull/28289)
    - sessionctx: fix data-race bug when alloc task id [#28283](https://github.com/pingcap/tidb/pull/28283)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28280](https://github.com/pingcap/tidb/pull/28280)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28264](https://github.com/pingcap/tidb/pull/28264)
    - Fix `can not found column in Schema column` error for mpp queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix a bug that TiDB may crash when TiFlash is shutting down. [#28140](https://github.com/pingcap/tidb/pull/28140)
    - None. [#27924](https://github.com/pingcap/tidb/pull/27924)
    - Support for 3DES based TLS ciphersuites was removed [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Do not check multi-ingest when store is offline. [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Please add a release note, or a 'None' if it is not needed. [#27727](https://github.com/pingcap/tidb/pull/27727)
    - Fix the issue that pre-check cost too much time when import too many files for tables. [#27623](https://github.com/pingcap/tidb/pull/27623)
    - fix expression rewrite makes between expr infers wrong collation. [#27550](https://github.com/pingcap/tidb/pull/27550)
    - make `group_concat` function consider the collation [#27530](https://github.com/pingcap/tidb/pull/27530)
    - expression: fix extract bug when argument is a negative duration [#27366](https://github.com/pingcap/tidb/pull/27366)
    - fix a bug that creates partition fail if `NO_UNSIGNED_SUBTRACTION` is set. [#27100](https://github.com/pingcap/tidb/pull/27100)

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

+ TiFlash

    - Please add a release note, or a 'None' if it is not needed. [#2820](https://github.com/pingcap/tics/pull/2820)

+ Tools

    + TiCDC

        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3104](https://github.com/pingcap/ticdc/pull/3104)
        - fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3102](https://github.com/pingcap/ticdc/pull/3102)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#3093](https://github.com/pingcap/ticdc/pull/3093)
        - Fix a bug that will lead cdc owner to consume cpu hugely. [#3077](https://github.com/pingcap/ticdc/pull/3077)
        - fix kafka sink can not send message due to constraint by `max-message-size` option. [#3049](https://github.com/pingcap/ticdc/pull/3049)
        - Nond [#3045](https://github.com/pingcap/ticdc/pull/3045)
        - Add metrics to observe incremental scan remaining time [#3035](https://github.com/pingcap/ticdc/pull/3035)
        - Fix possible deadlocking when Kafka producer reports an error. [#3018](https://github.com/pingcap/ticdc/pull/3018)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#2944](https://github.com/pingcap/ticdc/pull/2944)
        - Fix dml is not replicated after adding partition in partition table without valid index [#2866](https://github.com/pingcap/ticdc/pull/2866)
        - `None` [#2861](https://github.com/pingcap/ticdc/pull/2861)
        - Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time. [#2854](https://github.com/pingcap/ticdc/pull/2854)
        - Fix json encoding could panic when processing a string type value in some cases. [#2784](https://github.com/pingcap/ticdc/pull/2784)
