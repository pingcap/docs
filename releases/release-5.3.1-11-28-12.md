---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 Release Notes

Release Date: April 18, 2022

TiDB version: 5.2.4

## Improvements

+ PingCAP/TiDB

    - executor: fix wrong result of delete multiple tables using left join [#33121](https://github.com/pingcap/tidb/pull/33121)
    - planner: Fix the issue that TiDB may dispatch duplicated tasks to TiFlash [#32839](https://github.com/pingcap/tidb/pull/32839)
    - lightning: fix checksum encountered “GC life time is shorter than transaction duration” error [#32797](https://github.com/pingcap/tidb/pull/32797)
    - Fix BR failure on backup rawkv. [#32791](https://github.com/pingcap/tidb/pull/32791)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#32388](https://github.com/pingcap/tidb/pull/32388)
    - Fix the crash or error when generating an empty mpp task list. [#31696](https://github.com/pingcap/tidb/pull/31696)
    - Fix index join bug caused by innerWorker panic [#31615](https://github.com/pingcap/tidb/pull/31615)
    - Fix a panic that may happen when using `on duplicate key update`. [#31343](https://github.com/pingcap/tidb/pull/31343)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30875](https://github.com/pingcap/tidb/pull/30875)
    - Fix the but that lightning doesn't report error if s3 storage path not exist. [#30713](https://github.com/pingcap/tidb/pull/30713)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30599](https://github.com/pingcap/tidb/pull/30599)
    - fix a bug when reducing order by clause for the index which leads to the wrong result. [#30551](https://github.com/pingcap/tidb/pull/30551)
    - Fix the bug that TiDB logs many `failed to check the user authplugin` when a user connects to TiDB. [#30046](https://github.com/pingcap/tidb/pull/30046)
    - Fix wrong result for join with enum type [#29515](https://github.com/pingcap/tidb/pull/29515)
    - Fix panic for caseWhen function with enum type [#29511](https://github.com/pingcap/tidb/pull/29511)
    - Fix wrong result of microsecond function in vectorized [#29387](https://github.com/pingcap/tidb/pull/29387)

+ TiKV/TiKV

    - fix tikv panic and peer unexpected destroy due to fake merge target [#12297](https://github.com/tikv/tikv/pull/12297)
    - Fix stale message cause panic [#12288](https://github.com/tikv/tikv/pull/12288)
    - Solve the problem of raft msg memory metrics overflow, which will cause intermittent packet loss and oom. [#12225](https://github.com/tikv/tikv/pull/12225)
    - Fix crash when profiling in Ubuntu 18.04. [#12214](https://github.com/tikv/tikv/pull/12214)
    - Fix logic of error string match in `bad-ssts`. [#12148](https://github.com/tikv/tikv/pull/12148)
    - Pass leader transferee to cdc observer to reduce TiCDC latency spike. [#12135](https://github.com/tikv/tikv/pull/12135)
    - Fix potential linearizability violation in replica reads. [#12118](https://github.com/tikv/tikv/pull/12118)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12084](https://github.com/tikv/tikv/pull/12084)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#12043](https://github.com/tikv/tikv/pull/12043)
    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11999](https://github.com/tikv/tikv/pull/11999)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11863](https://github.com/tikv/tikv/pull/11863)
    - Fix panic when cgroup controller is not mounted [#11580](https://github.com/tikv/tikv/pull/11580)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11567](https://github.com/tikv/tikv/pull/11567)
    - Fix resolved ts lag increased after stoping a tikv [#11539](https://github.com/tikv/tikv/pull/11539)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11512](https://github.com/tikv/tikv/pull/11512)
    - make tikv-ctl detect raft db correctly [#11412](https://github.com/tikv/tikv/pull/11412)
    - fix negative sign when decimal divide to zero [#11335](https://github.com/tikv/tikv/pull/11335)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11292](https://github.com/tikv/tikv/pull/11292)
    - Fix label leaking of thread metrics [#11203](https://github.com/tikv/tikv/pull/11203)

+ PingCAP/TiFlash

    - Fix a bug that MPP tasks may leak threads forever [#4645](https://github.com/pingcap/tiflash/pull/4645)
    - fix error result for function `in` [#4627](https://github.com/pingcap/tiflash/pull/4627)
    - Fix the potential crash issue that occurs when TLS is enabled [#4591](https://github.com/pingcap/tiflash/pull/4591)
    - Fix the problem that empty segments cannot be merged after gc [#4515](https://github.com/pingcap/tiflash/pull/4515)
    - Fix wrong result of cast(float as decimal) when overflow happens [#4386](https://github.com/pingcap/tiflash/pull/4386)
    - Fix cast datetime to decimal wrong result bug [#4158](https://github.com/pingcap/tiflash/pull/4158)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4133](https://github.com/pingcap/tiflash/pull/4133)
    - mpp task handle pingcap exception. [#4113](https://github.com/pingcap/tiflash/pull/4113)
    - Fix cast to decimal overflow bug [#4081](https://github.com/pingcap/tiflash/pull/4081)
    - fix date format identifies '\n' as invalid separator [#4058](https://github.com/pingcap/tiflash/pull/4058)
    - Fix potential query error after add column under heavy read workload [#4026](https://github.com/pingcap/tiflash/pull/4026)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3933](https://github.com/pingcap/tiflash/pull/3933)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3917](https://github.com/pingcap/tiflash/pull/3917)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3756](https://github.com/pingcap/tiflash/pull/3756)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3705](https://github.com/pingcap/tiflash/pull/3705)
    - Fix the problem that obsolete data cannot be reclaimed after set tiflash replica to 0 [#3695](https://github.com/pingcap/tiflash/pull/3695)
    - Increase the max supported depth of expression/plan tree in dag request from 100 to 200. [#3679](https://github.com/pingcap/tiflash/pull/3679)
    - Fixed the inconsistent behavior of CastStringAsDecimal between tiflash and tidb/tikv. [#3676](https://github.com/pingcap/tiflash/pull/3676)
    - Fix potential data inconsistency after altering a primary key column to a larger int data type [#3574](https://github.com/pingcap/tiflash/pull/3574)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3479](https://github.com/pingcap/tiflash/pull/3479)
    - Fix tiflash randomly crash when a mpp query is killed. [#3450](https://github.com/pingcap/tiflash/pull/3450)
    - Fix that coalesce mistakenly removed nullable flag from the result column. [#3399](https://github.com/pingcap/tiflash/pull/3399)
    - Fix bug that collation does not work for nullable type [#3395](https://github.com/pingcap/tiflash/pull/3395)
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)` [#3378](https://github.com/pingcap/tiflash/pull/3378)

+ PD

    - None. [#4665](https://github.com/tikv/pd/pull/4665)
    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4434](https://github.com/tikv/pd/pull/4434)

+ Tools

    + PingCAP/TiCDC

        - Fix column default value type unsupported problem and data inconsistency issue. [#5156](https://github.com/pingcap/tiflow/pull/5156)
        - Fix chengefeed getting stuck when tables are repeatedly scheduled in the same node [#5145](https://github.com/pingcap/tiflow/pull/5145)
        - `Fix a bug that openapi may be stuck when pd is abnormal` [#5110](https://github.com/pingcap/tiflow/pull/5110)
        - Fix stale metrics data when TiCDC owner switches. [#5046](https://github.com/pingcap/tiflow/pull/5046)
        - Add changefeed lag analyze panels [#4905](https://github.com/pingcap/tiflow/pull/4905)
        - `None`. [#4867](https://github.com/pingcap/tiflow/pull/4867)
        - Fix stale metrics caused by owner changes. [#4798](https://github.com/pingcap/tiflow/pull/4798)
        - metrics: support multi-k8s in grafana dashboards [#4707](https://github.com/pingcap/tiflow/pull/4707)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4681](https://github.com/pingcap/tiflow/pull/4681)
        - `None`. [#4673](https://github.com/pingcap/tiflow/pull/4673)
        - Fix a bug that sequence should not be replicated even if force-replication is true. [#4671](https://github.com/pingcap/tiflow/pull/4671)
        - `None`. [#4613](https://github.com/pingcap/tiflow/pull/4613)
        - `None`. [#4593](https://github.com/pingcap/tiflow/pull/4593)
        - `None`. [#4573](https://github.com/pingcap/tiflow/pull/4573)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4531](https://github.com/pingcap/tiflow/pull/4531)
        - allow user set the configuration of Kafka producer dial/write/read timeout [#4525](https://github.com/pingcap/tiflow/pull/4525)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4507](https://github.com/pingcap/tiflow/pull/4507)
        - `None`. [#4470](https://github.com/pingcap/tiflow/pull/4470)
        - Fix column default value panic and data inconsistency [#4442](https://github.com/pingcap/tiflow/pull/4442)
        - `None`. [#4344](https://github.com/pingcap/tiflow/pull/4344)
        - Add exponential backoff mechanism for restarting a changefeed. [#4338](https://github.com/pingcap/tiflow/pull/4338)
        - `None`. [#4322](https://github.com/pingcap/tiflow/pull/4322)
        - Fix kv client cached region metric could be negative. [#4295](https://github.com/pingcap/tiflow/pull/4295)
        - `None` [#4284](https://github.com/pingcap/tiflow/pull/4284)
        - `None`. [#4277](https://github.com/pingcap/tiflow/pull/4277)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#4270](https://github.com/pingcap/tiflow/pull/4270)
        - `None`. [#4208](https://github.com/pingcap/tiflow/pull/4208)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#4182](https://github.com/pingcap/tiflow/pull/4182)
        - Fix the bug that http API panic when the processor info we want to get is not exist. [#4122](https://github.com/pingcap/tiflow/pull/4122)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4119](https://github.com/pingcap/tiflow/pull/4119)
        - Reduce "EventFeed retry rate limited" logs [#4110](https://github.com/pingcap/tiflow/pull/4110)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4098](https://github.com/pingcap/tiflow/pull/4098)
        - `None`. [#4078](https://github.com/pingcap/tiflow/pull/4078)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4062](https://github.com/pingcap/tiflow/pull/4062)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#4015](https://github.com/pingcap/tiflow/pull/4015)
        - Fix syntax error if DDL has a special comment. [#3977](https://github.com/pingcap/tiflow/pull/3977)
        - Fix the owner may be blocked when initializing the changefeed caused by a bad network connection to the sink [#3962](https://github.com/pingcap/tiflow/pull/3962)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3910](https://github.com/pingcap/tiflow/pull/3910)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3864](https://github.com/pingcap/tiflow/pull/3864)
        - Fix mounter default date value not support [#3858](https://github.com/pingcap/tiflow/pull/3858)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#3831](https://github.com/pingcap/tiflow/pull/3831)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#3799](https://github.com/pingcap/tiflow/pull/3799)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3782](https://github.com/pingcap/tiflow/pull/3782)
        - fix kvclient takes too long time to recover [#3662](https://github.com/pingcap/tiflow/pull/3662)
        - The Avro sink was updated to handle JSON columns [#3653](https://github.com/pingcap/tiflow/pull/3653)
        - fix changefeed checkpoint lag negative value error [#3535](https://github.com/pingcap/tiflow/pull/3535)
        - Fix OOM in container environments. [#3438](https://github.com/pingcap/tiflow/pull/3438)
        - Show changefeed checkepoint catch-up ETA in metrics. [#3311](https://github.com/pingcap/tiflow/pull/3311)
        - Fix memory leak after processing DDLs. [#3273](https://github.com/pingcap/tiflow/pull/3273)

## Compatibility Changes

+ PingCAP/TiDB

    - Fix the issue that system variable `max_allowed_packet` does not work. [#34055](https://github.com/pingcap/tidb/pull/34055)
    - Fix an issue that REPLACE statement changing other rows when the auto ID is out of range [#33863](https://github.com/pingcap/tidb/pull/33863)

## Bug Fixes

+ PingCAP/TiDB

    - planner: fix wrong range calculation for Nulleq function on Enum values [#32494](https://github.com/pingcap/tidb/pull/32494)
    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31447](https://github.com/pingcap/tidb/pull/31447)
    - Fix the error that if tidb-lightning doesn't has permission to access mysql.tidb, it will generate kv with wrong format. [#31151](https://github.com/pingcap/tidb/pull/31151)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31070](https://github.com/pingcap/tidb/pull/31070)
    - Fix the data inconsistency caused by invalid usage of lazy existence check and untouch key optimization. [#30911](https://github.com/pingcap/tidb/pull/30911)
    - Fix the bug that sql got cancel if including json column joins char column. [#30776](https://github.com/pingcap/tidb/pull/30776)
    - executor: fix pipelined window invalid memory address [#30459](https://github.com/pingcap/tidb/pull/30459)
    - Fix the problem that window function may return different results when using transaction or not. [#30391](https://github.com/pingcap/tidb/pull/30391)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#30015](https://github.com/pingcap/tidb/pull/30015)
    - expression: fix different results for greatest when vectorized is off. [#29919](https://github.com/pingcap/tidb/pull/29919)

+ PingCAP/TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3624](https://github.com/pingcap/tiflash/pull/3624)
    - fix the issue that comparison between Decimal may cause overflow and report `Can't compare`. [#3367](https://github.com/pingcap/tiflash/pull/3367)
    - Fix the issue of unexpected error that `3rd arguments of function substringUTF8 must be constants.` [#3264](https://github.com/pingcap/tiflash/pull/3264)

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4580](https://github.com/tikv/pd/pull/4580)
