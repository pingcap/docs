---
title: TiDB 5.1.4 Release Notes
category: Releases
---

# TiDB 5.1.4 Release Notes

Release Date: February 22, 2022

TiDB version: 5.1.4

## Compatibility changes

## Feature enhancements

## __unsorted

+ TiDB

    - Fix wrong result of microsecond function in vectorized [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Set default value of tidb_analyze_version to 1 in v5.1 and v5.2 [#31748](https://github.com/pingcap/tidb/issues/31748)
    - Fix a panic that may happen when using `on duplicate key update`. [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30171](https://github.com/pingcap/tidb/pull/30171)
    - Fix an issue that adding index panics by chance. [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix wrong result for join with enum type [#27831](https://github.com/pingcap/tidb/issues/27831)
    - Fix panic for caseWhen function with enum type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix a memory leak bug when using @@tidb_analyze_version = 2 [#29305](https://github.com/pingcap/tidb/pull/29305)
    - Fix wrong result of hour function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#28345](https://github.com/pingcap/tidb/pull/28345)
    - Fix bug that mpp node availability detect does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - sessionctx: fix data-race bug when alloc task id [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28263](https://github.com/pingcap/tidb/pull/28263)

+ TiKV/TiKV

    - Fixes the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - fix potential high latency caused by destroying a peer [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix wrong `any_value` result when there are regions returning empty result [#11735](https://github.com/tikv/tikv/issues/11735)
    - update procfs to 0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#10533](https://github.com/tikv/tikv/issues/10533)
    - None. [#11627](https://github.com/tikv/tikv/pull/11627)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix resolved ts lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix connection abort when too many raft entries are batched into one messages [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - Please add a release note. If you don't think this PR needs a release note then fill it with None. [#11477](https://github.com/tikv/tikv/pull/11477)
    - status_server: skip profiling sample in glibc, pthread, libgcc to avoid possible deadlock
    - status_server: upgrade pprof-rs to fix memory leak [#11108](https://github.com/tikv/tikv/issues/11108)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    - make tikv-ctl detect raft db correctly [#11393](https://github.com/tikv/tikv/issues/11393)
    - fix negative sign when decimal divide to zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11291](https://github.com/tikv/tikv/pull/11291)
    - Fix resource-metering.enabled not working [#11235](https://github.com/tikv/tikv/issues/11235)
    - move verify_checksum to import-thread from apply-thread. [#11239](https://github.com/tikv/tikv/issues/11239)
    - Fix label leaking of thread metrics [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix CDC panic due to missing downstream. [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue #9714. Now RaftClient will check the size of RaftMessage.extra_ctx and RaftMessage.message.context size as part of its message size estimate. [#9714](https://github.com/tikv/tikv/issues/9714)
    - resolved_ts: fix coroutine leaking [#10965](https://github.com/tikv/tikv/issues/10965)
    - Hide untouched storage commands' metrics in grafana dashboard [#11002](https://github.com/tikv/tikv/pull/11002)
    - resolved_ts: fix coroutine leaking [#10984](https://github.com/tikv/tikv/pull/10984)
    - improve raft client error log report [#10982](https://github.com/tikv/tikv/pull/10982)
    - Please add a release note. If you don't think this PR needs a release note then fill it with None. [#10967](https://github.com/tikv/tikv/pull/10967)
    - None. [#10584](https://github.com/tikv/tikv/issues/10584)
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
    - None. [#4289](https://github.com/tikv/pd/pull/4289)
    - speed scheduler exit [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - release-note [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)
        - Add exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Fix kv client cached region metric could be negative. [#4294](https://github.com/pingcap/tiflow/pull/4294)
        - `None` [#4266](https://github.com/pingcap/tiflow/issues/4266)
        - `None`. [#4223](https://github.com/pingcap/tiflow/issues/4223)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - `None`. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4165](https://github.com/pingcap/tiflow/pull/4165)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4164](https://github.com/pingcap/tiflow/pull/4164)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4150](https://github.com/pingcap/tiflow/pull/4150)
        - Reduce "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - `None`. [#4077](https://github.com/pingcap/tiflow/pull/4077)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - None (not released yet) [#4001](https://github.com/pingcap/tiflow/pull/4001)
        - Fix syntax error if DDL has a special comment. [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Reduce checkpoint lag when capturing many tables. [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix a bug in EtcdWorker that could hang the owner or processor. [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix mounter default date value not support [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#4054](https://github.com/pingcap/tiflow/issues/4054)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - `None`. [#3763](https://github.com/pingcap/tiflow/pull/3763)
        - Try to fix owner stuck caused by etcd txn timeout or etcd watch channel blocked in EtcdWorker. [#3758](https://github.com/pingcap/tiflow/pull/3758)
        - Fix kvclient takes too long time to recover [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - The Avro sink was updated to handle JSON columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - fix changefeed checkpoint lag negative value error [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix OOM in container environments. [#3437](https://github.com/pingcap/tiflow/pull/3437)
        - Fix a bug that TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - Fix memory leak after processing DDLs. [#3276](https://github.com/pingcap/tiflow/pull/3276)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3269](https://github.com/pingcap/tiflow/pull/3269)
        - bugfix: fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - fix kafka sink can not send message due to constraint by `max-message-size` option. [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - Nond [#2983](https://github.com/pingcap/tiflow/issues/2983)
        - Add metrics to observe incremental scan remaining time [#2985](https://github.com/pingcap/tiflow/issues/2985)
        - Fix possible deadlocking when Kafka producer reports an error. [#3017](https://github.com/pingcap/tiflow/pull/3017)
        - Set compatible version from 5.1.0-alpha to 5.2.0-alpha [#2659](https://github.com/pingcap/tiflow/pull/2659)

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
    - release-note [#25041](https://github.com/pingcap/tidb/issues/25041)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#29417](https://github.com/pingcap/tidb/issues/29417)
    - expression: fix different results for greatest when vectorized is off. [#29434](https://github.com/pingcap/tidb/issues/29434)
    - 'None' [#28233](https://github.com/pingcap/tidb/issues/28233)
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