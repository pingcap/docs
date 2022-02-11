---
title: TiDB 5.1.4 Release Notes
category: Releases
---

# TiDB 5.1.4 Release Notes

Release Date: xx, 2022

TiDB version: 5.1.4

## Compatibility changes

## Feature enhancements

## __unsorted

+ TiDB

    (dup) - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Set default value of tidb_analyze_version to 1 in v5.1 and v5.2 [#31748](https://github.com/pingcap/tidb/issues/31748)
    - Fix a panic that may happen when using `on duplicate key update`. [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#25716](https://github.com/pingcap/tidb/issues/25716)
    - Fix an issue that adding index panics by chance. [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix wrong result for join with enum type [#27831](https://github.com/pingcap/tidb/issues/27831)
    (dup) - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix a memory leak bug when using @@tidb_analyze_version = 2 [#29305](https://github.com/pingcap/tidb/pull/29305)
    (dup) - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#28345](https://github.com/pingcap/tidb/pull/28345)
    - Fix bug that mpp node availability detect does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - sessionctx: fix data-race bug when alloc task id [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#1791](https://github.com/pingcap/tics/issues/1791)

+ TiKV/TiKV

    - Fixes the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - fix potential high latency caused by destroying a peer [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix wrong `any_value` result when there are regions returning empty result [#11735](https://github.com/tikv/tikv/issues/11735)
    - update procfs to 0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix resolved ts lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix connection abort when too many raft entries are batched into one messages [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - status_server: skip profiling sample in glibc, pthread, libgcc to avoid possible deadlock
    - status_server: upgrade pprof-rs to fix memory leak [#11108](https://github.com/tikv/tikv/issues/11108)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    - make tikv-ctl detect raft db correctly [#11393](https://github.com/tikv/tikv/issues/11393)
    (dup) - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix resource-metering.enabled not working [#11235](https://github.com/tikv/tikv/issues/11235)
    - move verify_checksum to import-thread from apply-thread. [#11239](https://github.com/tikv/tikv/issues/11239)
    - Fix label leaking of thread metrics [#11195](https://github.com/tikv/tikv/issues/11195)
    (dup) - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    (dup) - Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue #9714. Now RaftClient will check the size of RaftMessage.extra_ctx and RaftMessage.message.context size as part of its message size estimate. [#9714](https://github.com/tikv/tikv/issues/9714)
    - resolved_ts: fix coroutine leaking [#10965](https://github.com/tikv/tikv/issues/10965)
    - Hide untouched storage commands' metrics in grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)
    - resolved_ts: fix coroutine leaking [#10965](https://github.com/tikv/tikv/issues/10965)
    - improve raft client error log report [#11959](https://github.com/tikv/tikv/issues/11959)
    - Avoid false "GC can not work" alert under low write flow. [#10664](https://github.com/tikv/tikv/pull/10664)

+ TiFlash

    - Fix cast to decimal overflow bug
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb.
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart.
    - Fix the problem that obsolete data cannot be reclaimed after set tiflash replica to 0
    - Increase the max supported depth of expression/plan tree in dag request from 100 to 200.
    - Fixed the inconsistent behavior of CastStringAsDecimal between tiflash and tidb/tikv.
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type.
    - Fix tiflash randomly crash when a mpp query is killed.
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)`
    - Support INET6_ATON and INET6_NTOA in TiFlash.
    - Support INET_ATON and INET_NTOA in TiFlash.
    - expand streams after aggregation

+ PD

    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4390](https://github.com/tikv/pd/issues/4390)
    - speed scheduler exit [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Add exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Fix kv client cached region metric could be negative. [#4294](https://github.com/pingcap/tiflow/pull/4294)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Reduce "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix syntax error if DDL has a special comment. [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Reduce checkpoint lag when capturing many tables. [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix a bug in EtcdWorker that could hang the owner or processor. [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix mounter default date value not support [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#4054](https://github.com/pingcap/tiflow/issues/4054)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Try to fix owner stuck caused by etcd txn timeout or etcd watch channel blocked in EtcdWorker. [#3615](https://github.com/pingcap/tiflow/issues/3615)
        - Fix kvclient takes too long time to recover [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - The Avro sink was updated to handle JSON columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)
        (dup) - Fix OOM in container environments [#1798](https://github.com/pingcap/tiflow/issues/1798)
        (dup) - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/tiflow/issues/3288)
        (dup) - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/tiflow/issues/3174)
        (dup) - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/tiflow/issues/3111)
        (dup) - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3081](https://github.com/pingcap/tiflow/issues/3081)
        (dup) - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        (dup) - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        (dup) (dup) - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - Nond [#2983](https://github.com/pingcap/tiflow/issues/2983)
        - Add metrics to observe incremental scan remaining time [#2985](https://github.com/pingcap/tiflow/issues/2985)
        (dup) - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)

## Improvements

+ TiDB

    - planner: support column range partition pruning for builtin function IN [#26739](https://github.com/pingcap/tidb/issues/26739)
    - Track the memory usage of IndexJoin more accurate. [#28650](https://github.com/pingcap/tidb/issues/28650)

+ TiFlash

    - support functions of ADDDATE() and DATE_ADD() pushed down to tiflash

## Bug Fixes

+ TiDB

    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization. [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the problem that window function may return different results when using transaction or not. [#29947](https://github.com/pingcap/tidb/issues/29947)
    (dup) - Fix the issue that the length information is wrong when converting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    (dup) - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (`on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    - planner: fix the issue that planner may cache invalid plans for joins in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)

+ TiFlash

    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds
    - Fix the problem of TiFlash crashing when the memory limit is enabled
    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC
    - Fix potential data inconsistency when widen pk column type if pk is handle
    - fix the issue that comparison between Decimal may cause overflow and report `Can't compare`
    - Fix the issue of unexpected error that `3rd arguments of function substringUTF8 must be constants.`
    - Fix the issue that TiFlash fails to start up under platform without library `nsl`
    - release-note

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix panic issue after TiKV node scales in [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)
    - Fix the bug that region statistics are not updated after `flow-round-by-digit` change. [#4295](https://github.com/tikv/pd/issues/4295)
    - Fix the issue that PD may not elect leader as soon as leader step down [#3936](https://github.com/tikv/pd/issues/3936)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4093](https://github.com/tikv/pd/issues/4093)
