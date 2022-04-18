---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 Release Notes

Release Date: April xx, 2022

TiDB version: 5.2.4

## Compatibility change(s)

+ TiDB

    - Fix the issue that system variable `max_allowed_packet` does not work. [#31422](https://github.com/pingcap/tidb/issues/31422)
    - Fix an issue that REPLACE statement changing other rows when the auto ID is out of range [#29483](https://github.com/pingcap/tidb/issues/29483)

+ Tools

    + Backup & Restore (BR)

        -
        -

## Improvements

+ TiDB

    -

+ TiKV

    -

+ PD

    -

+ TiDB Dashboard

    -

+ TiFlash

    -

+ Tools

    + Backup & Restore (BR)

        -

    + TiCDC

        -

    + Dumpling

        -

    + TiDB Lightning

        - note 1

    + TiDB Binlog

        - note 1

## Bug fixes

+ TiDB

    - planner: fix wrong range calculation for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the error that if tidb-lightning doesn't has permission to access mysql.tidb, it will generate kv with wrong format. [#31088](https://github.com/pingcap/tidb/issues/31088)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Fix the data inconsistency caused by invalid usage of lazy existence check and untouch key optimization. [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the bug that sql got cancel if including json column joins char column. [#29401](https://github.com/pingcap/tidb/issues/29401)
    - executor: fix pipelined window invalid memory address [#30326](https://github.com/pingcap/tidb/issues/30326)
    - Fix the problem that window function may return different results when using transaction or not. [#29947](https://github.com/pingcap/tidb/issues/29947)
    - ```release-note [#25041](https://github.com/pingcap/tidb/issues/25041)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#29417](https://github.com/pingcap/tidb/issues/29417)
    - expression: fix different results for greatest when vectorized is off. [#29434](https://github.com/pingcap/tidb/issues/29434)

+ TiKV

    -

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4565](https://github.com/tikv/pd/issues/4565)

+ TiDB Dashboard

    -

+ TiFlash

    -

+ Tools

    + Backup & Restore (BR)

        -

    + TiCDC

        -

    + Dumpling

        -

    + TiDB Lightning

        - note 1

    + TiDB Binlog

        - note 1

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#33966](https://github.com/pingcap/tidb/issues/33966)
    - ```release-note [#31748](https://github.com/pingcap/tidb/issues/31748)
    - executor: fix wrong result of delete multiple tables using left join [#31321](https://github.com/pingcap/tidb/issues/31321)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32733](https://github.com/pingcap/tidb/issues/32733)
    - Fix BR failure on backup rawkv. [#32607](https://github.com/pingcap/tidb/issues/32607)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#28144](https://github.com/pingcap/tidb/issues/28144)
    - Fix the crash or error when generating an empty mpp task list. [#31636](https://github.com/pingcap/tidb/issues/31636)
    - Fix index join bug caused by innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - Fix a panic that may happen when using `on duplicate key update`. [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30018](https://github.com/pingcap/tidb/issues/30018)
    - Fix the but that lightning doesn't report error if s3 storage path not exist. [#28031](https://github.com/pingcap/tidb/issues/28031)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30571](https://github.com/pingcap/tidb/issues/30571)
    - fix a bug when reducing order by clause for the index which leads to the wrong result. [#30271](https://github.com/pingcap/tidb/issues/30271)
    - - Fix the bug that TiDB logs many `failed to check the user authplugin` when a user connects to TiDB. [#29709](https://github.com/pingcap/tidb/issues/29709)
    - Fix wrong result for join with enum type [#27831](https://github.com/pingcap/tidb/issues/27831)
    - Fix panic for caseWhen function with enum type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong result of microsecond function in vectorized [#29244](https://github.com/pingcap/tidb/issues/29244)


+ TiKV/TiKV

    - fix tikv panic and peer unexpected destroy due to fake merge target [#12232](https://github.com/tikv/tikv/issues/12232)
    - Fix stale message cause panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix crash when profiling in Ubuntu 18.04. [#9765](https://github.com/tikv/tikv/issues/9765)
    - Fix logic of error string match in `bad-ssts`. [#12329](https://github.com/tikv/tikv/issues/12329)
    - Pass leader transferee to cdc observer to reduce TiCDC latency spike. [#12111](https://github.com/tikv/tikv/issues/12111)
    - Fix potential linearizability violation in replica reads. [#12109](https://github.com/tikv/tikv/issues/12109)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12048](https://github.com/tikv/tikv/issues/12048)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#11940](https://github.com/tikv/tikv/issues/11940)
    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11993](https://github.com/tikv/tikv/issues/11993)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11424](https://github.com/tikv/tikv/issues/11424)
    - Fix panic when cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix resolved ts lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - make tikv-ctl detect raft db correctly [#11393](https://github.com/tikv/tikv/issues/11393)
    - fix negative sign when decimal divide to zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix label leaking of thread metrics [#11195](https://github.com/tikv/tikv/issues/11195)


+ PingCAP/TiFlash

    - Fix a bug that MPP tasks may leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - fix error result for function `in` [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - Fix the potential crash issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - Fix the problem that empty segments cannot be merged after gc [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - Fix wrong result of cast(float as decimal) when overflow happens [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - Fix cast datetime to decimal wrong result bug [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - mpp task handle pingcap exception. [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix cast to decimal overflow bug [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - fix date format identifies '\n' as invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - Fix potential query error after add column under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3557](https://github.com/pingcap/tiflash/issues/3557)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3615](https://github.com/pingcap/tiflash/issues/3615)
    - Fix the problem that obsolete data cannot be reclaimed after set tiflash replica to 0 [#3659](https://github.com/pingcap/tiflash/issues/3659)
    - Increase the max supported depth of expression/plan tree in dag request from 100 to 200. [#3354](https://github.com/pingcap/tiflash/issues/3354)
    - Fixed the inconsistent behavior of CastStringAsDecimal between tiflash and tidb/tikv. [#3619](https://github.com/pingcap/tiflash/issues/3619)
    - Fix potential data inconsistency after altering a primary key column to a larger int data type [#3569](https://github.com/pingcap/tiflash/issues/3569)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3447](https://github.com/pingcap/tiflash/issues/3447)
    - Fix tiflash randomly crash when a mpp query is killed. [#3401](https://github.com/pingcap/tiflash/issues/3401)
    - Fix that coalesce mistakenly removed nullable flag from the result column. [#3388](https://github.com/pingcap/tiflash/issues/3388)
    - Fix bug that collation does not work for nullable type [#3391](https://github.com/pingcap/tiflash/issues/3391)
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)` [#3351](https://github.com/pingcap/tiflash/issues/3351)

+ PD

    - None. [#4808](https://github.com/tikv/pd/issues/4808)
    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4390](https://github.com/tikv/pd/issues/4390)

+ Tools

    + PingCAP/TiCDC

        - Fix column default value type unsupported problem and data inconsistency issue. [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix chengefeed getting stuck when tables are repeatedly scheduled in the same node [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - `Fix a bug that openapi may be stuck when pd is abnormal` [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - Fix stale metrics data when TiCDC owner switches. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - Add changefeed lag analyze panels [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - `None`. [#4858](https://github.com/pingcap/tiflow/issues/4858)
        - Fix stale metrics caused by owner changes. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - metrics: support multi-k8s in grafana dashboards [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - `None`. [#4675](https://github.com/pingcap/tiflow/issues/4675)
        - Fix a bug that sequence should not be replicated even if force-replication is true. [#4552](https://github.com/pingcap/tiflow/issues/4552)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - allow user set the configuration of Kafka producer dial/write/read timeout [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - Fix column default value panic and data inconsistency [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)
        - Add exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - `None`. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix kv client cached region metric could be negative. [#4295](https://github.com/pingcap/tiflow/pull/4295)
        - `None` [#4266](https://github.com/pingcap/tiflow/issues/4266)
        - `None`. [#4223](https://github.com/pingcap/tiflow/issues/4223)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - `None`. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the bug that http API panic when the processor info we want to get is not exist. [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Reduce "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - `None`. [#4089](https://github.com/pingcap/tiflow/issues/4089)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix syntax error if DDL has a special comment. [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix the owner may be blocked when initializing the changefeed caused by a bad network connection to the sink [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix mounter default date value not support [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#4054](https://github.com/pingcap/tiflow/issues/4054)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - `None`. [#3764](https://github.com/pingcap/tiflow/pull/3764)
        - Please add a release note.
fix kvclient takes too long time to recover [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - The Avro sink was updated to handle JSON columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - fix changefeed checkpoint lag negative value error [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix OOM in container environments. [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3867](https://github.com/pingcap/tiflow/pull/3867)
        - Show changefeed checkepoint catch-up ETA in metrics. [#3311](https://github.com/pingcap/tiflow/pull/3311)
        - Fix memory leak after processing DDLs. [#3174](https://github.com/pingcap/tiflow/issues/3174)