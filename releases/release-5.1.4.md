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

    - Fix wrong result of microsecond function in vectorized [#32122](https://github.com/pingcap/tidb/pull/32122)
    - Set default value of tidb_analyze_version to 1 in v5.1 and v5.2 [#31826](https://github.com/pingcap/tidb/pull/31826)
    - Fix a panic that may happen when using `on duplicate key update`. [#31342](https://github.com/pingcap/tidb/pull/31342)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30171](https://github.com/pingcap/tidb/pull/30171)
    - Fix an issue that adding index panics by chance. [#30123](https://github.com/pingcap/tidb/pull/30123)
    - Fix wrong result for join with enum type [#29514](https://github.com/pingcap/tidb/pull/29514)
    - Fix panic for caseWhen function with enum type [#29510](https://github.com/pingcap/tidb/pull/29510)
    - Fix a memory leak bug when using @@tidb_analyze_version = 2 [#29305](https://github.com/pingcap/tidb/pull/29305)
    - Fix wrong result of hour function in vectorized expression [#28872](https://github.com/pingcap/tidb/pull/28872)
    - Fix a batch client bug that recycle idle connection may block sending requests in some rare cases. [#28345](https://github.com/pingcap/tidb/pull/28345)
    - Fix bug that mpp node availability detect does not work in some corner cases [#28288](https://github.com/pingcap/tidb/pull/28288)
    - sessionctx: fix data-race bug when alloc task id [#28285](https://github.com/pingcap/tidb/pull/28285)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28279](https://github.com/pingcap/tidb/pull/28279)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28263](https://github.com/pingcap/tidb/pull/28263)

+ TiKV/TiKV

    - Fixes the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11911](https://github.com/tikv/tikv/pull/11911)
    - fix potential high latency caused by destroying a peer [#11878](https://github.com/tikv/tikv/pull/11878)
    - Fix wrong `any_value` result when there are regions returning empty result [#11742](https://github.com/tikv/tikv/pull/11742)
    - update procfs to 0.12.0 [#11722](https://github.com/tikv/tikv/pull/11722)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#11635](https://github.com/tikv/tikv/pull/11635)
    - None. [#11627](https://github.com/tikv/tikv/pull/11627)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11566](https://github.com/tikv/tikv/pull/11566)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11563](https://github.com/tikv/tikv/pull/11563)
    - Fix resolved ts lag increased after stoping a tikv [#11540](https://github.com/tikv/tikv/pull/11540)
    - Fix connection abort when too many raft entries are batched into one messages [#11533](https://github.com/tikv/tikv/pull/11533)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11511](https://github.com/tikv/tikv/pull/11511)
    - Please add a release note. If you don't think this PR needs a release note then fill it with None. [#11477](https://github.com/tikv/tikv/pull/11477)
    - status_server: skip profiling sample in glibc, pthread, libgcc to avoid possible deadlock
    - status_server: upgrade pprof-rs to fix memory leak [#11474](https://github.com/tikv/tikv/pull/11474)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11454](https://github.com/tikv/tikv/pull/11454)
    - make tikv-ctl detect raft db correctly [#11411](https://github.com/tikv/tikv/pull/11411)
    - fix negative sign when decimal divide to zero [#11334](https://github.com/tikv/tikv/pull/11334)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11291](https://github.com/tikv/tikv/pull/11291)
    - Fix resource-metering.enabled not working [#11282](https://github.com/tikv/tikv/pull/11282)
    - move verify_checksum to import-thread from apply-thread. [#11258](https://github.com/tikv/tikv/pull/11258)
    - Fix label leaking of thread metrics [#11202](https://github.com/tikv/tikv/pull/11202)
    - Fix CDC panic due to missing downstream. [#11137](https://github.com/tikv/tikv/pull/11137)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11091](https://github.com/tikv/tikv/pull/11091)
    - Fix the issue #9714. Now RaftClient will check the size of RaftMessage.extra_ctx and RaftMessage.message.context size as part of its message size estimate. [#11065](https://github.com/tikv/tikv/pull/11065)
    - resolved_ts: fix coroutine leaking [#11019](https://github.com/tikv/tikv/pull/11019)
    - Hide untouched storage commands' metrics in grafana dashboard [#11002](https://github.com/tikv/tikv/pull/11002)
    - resolved_ts: fix coroutine leaking [#10984](https://github.com/tikv/tikv/pull/10984)
    - improve raft client error log report [#10982](https://github.com/tikv/tikv/pull/10982)
    - Please add a release note. If you don't think this PR needs a release note then fill it with None. [#10967](https://github.com/tikv/tikv/pull/10967)
    - None. [#10822](https://github.com/tikv/tikv/pull/10822)
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

    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4433](https://github.com/tikv/pd/pull/4433)
    - None. [#4289](https://github.com/tikv/pd/pull/4289)
    - speed scheduler exit [#4198](https://github.com/tikv/pd/pull/4198)

+ Tools

    + TiCDC

        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4506](https://github.com/pingcap/tiflow/pull/4506)
        - `None`. [#4469](https://github.com/pingcap/tiflow/pull/4469)
        - release-note [#4446](https://github.com/pingcap/tiflow/pull/4446)
        - `None`. [#4343](https://github.com/pingcap/tiflow/pull/4343)
        - Add exponential backoff mechanism for restarting a changefeed. [#4337](https://github.com/pingcap/tiflow/pull/4337)
        - Fix kv client cached region metric could be negative. [#4294](https://github.com/pingcap/tiflow/pull/4294)
        - `None` [#4283](https://github.com/pingcap/tiflow/pull/4283)
        - `None`. [#4274](https://github.com/pingcap/tiflow/pull/4274)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#4269](https://github.com/pingcap/tiflow/pull/4269)
        - `None`. [#4207](https://github.com/pingcap/tiflow/pull/4207)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#4181](https://github.com/pingcap/tiflow/pull/4181)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4165](https://github.com/pingcap/tiflow/pull/4165)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4164](https://github.com/pingcap/tiflow/pull/4164)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4150](https://github.com/pingcap/tiflow/pull/4150)
        - Reduce "EventFeed retry rate limited" logs [#4114](https://github.com/pingcap/tiflow/pull/4114)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4097](https://github.com/pingcap/tiflow/pull/4097)
        - `None`. [#4077](https://github.com/pingcap/tiflow/pull/4077)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4061](https://github.com/pingcap/tiflow/pull/4061)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#4014](https://github.com/pingcap/tiflow/pull/4014)
        - None (not released yet) [#4001](https://github.com/pingcap/tiflow/pull/4001)
        - Fix syntax error if DDL has a special comment. [#3982](https://github.com/pingcap/tiflow/pull/3982)
        - Reduce checkpoint lag when capturing many tables. [#3949](https://github.com/pingcap/tiflow/pull/3949)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3909](https://github.com/pingcap/tiflow/pull/3909)
        - Fix a bug in EtcdWorker that could hang the owner or processor. [#3871](https://github.com/pingcap/tiflow/pull/3871)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3863](https://github.com/pingcap/tiflow/pull/3863)
        - Fix mounter default date value not support [#3857](https://github.com/pingcap/tiflow/pull/3857)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#3835](https://github.com/pingcap/tiflow/pull/3835)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#3798](https://github.com/pingcap/tiflow/pull/3798)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3781](https://github.com/pingcap/tiflow/pull/3781)
        - `None`. [#3763](https://github.com/pingcap/tiflow/pull/3763)
        - Try to fix owner stuck caused by etcd txn timeout or etcd watch channel blocked in EtcdWorker. [#3758](https://github.com/pingcap/tiflow/pull/3758)
        - Fix kvclient takes too long time to recover [#3661](https://github.com/pingcap/tiflow/pull/3661)
        - The Avro sink was updated to handle JSON columns [#3652](https://github.com/pingcap/tiflow/pull/3652)
        - fix changefeed checkpoint lag negative value error [#3534](https://github.com/pingcap/tiflow/pull/3534)
        - Fix OOM in container environments. [#3437](https://github.com/pingcap/tiflow/pull/3437)
        - Fix a bug that TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3292](https://github.com/pingcap/tiflow/pull/3292)
        - Fix memory leak after processing DDLs. [#3276](https://github.com/pingcap/tiflow/pull/3276)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3269](https://github.com/pingcap/tiflow/pull/3269)
        - bugfix: fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3136](https://github.com/pingcap/tiflow/pull/3136)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3129](https://github.com/pingcap/tiflow/pull/3129)
        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3108](https://github.com/pingcap/tiflow/pull/3108)
        - fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3101](https://github.com/pingcap/tiflow/pull/3101)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#3092](https://github.com/pingcap/tiflow/pull/3092)
        - fix kafka sink can not send message due to constraint by `max-message-size` option. [#3048](https://github.com/pingcap/tiflow/pull/3048)
        - Nond [#3044](https://github.com/pingcap/tiflow/pull/3044)
        - Add metrics to observe incremental scan remaining time [#3034](https://github.com/pingcap/tiflow/pull/3034)
        - Fix possible deadlocking when Kafka producer reports an error. [#3017](https://github.com/pingcap/tiflow/pull/3017)
        - Set compatible version from 5.1.0-alpha to 5.2.0-alpha [#2659](https://github.com/pingcap/tiflow/pull/2659)

## Improvements

+ TiDB

    - planner: support column range partition pruning for builtin function IN [#31862](https://github.com/pingcap/tidb/pull/31862)
    - Track the memory usage of IndexJoin more accurate. [#30091](https://github.com/pingcap/tidb/pull/30091)

+ TiFlash

    - support functions of ADDDATE() and DATE_ADD() pushed down to tiflash

## Bug Fixes

+ TiDB

    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31446](https://github.com/pingcap/tidb/pull/31446)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization. [#30526](https://github.com/pingcap/tidb/pull/30526)
    - Fix the problem that window function may return different results when using transaction or not. [#30390](https://github.com/pingcap/tidb/pull/30390)
    - release-note [#30050](https://github.com/pingcap/tidb/pull/30050)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#30013](https://github.com/pingcap/tidb/pull/30013)
    - expression: fix different results for greatest when vectorized is off. [#29918](https://github.com/pingcap/tidb/pull/29918)
    - 'None' [#28819](https://github.com/pingcap/tidb/pull/28819)
    - planner: fix the issue that planner may cache invalid plans for joins in some cases [#28446](https://github.com/pingcap/tidb/pull/28446)

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

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4579](https://github.com/tikv/pd/pull/4579)
    - Fix panic issue after TiKV node scales in [#4380](https://github.com/tikv/pd/pull/4380)
    - Fix the issue that operator can get blocked due to down store [#4368](https://github.com/tikv/pd/pull/4368)
    - Fix the bug that region statistics are not updated after `flow-round-by-digit` change. [#4329](https://github.com/tikv/pd/pull/4329)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4217](https://github.com/tikv/pd/pull/4217)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4131](https://github.com/tikv/pd/pull/4131)