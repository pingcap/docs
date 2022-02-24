---
title: TiDB 5.3.1 Release Notes
category: Releases
---

# TiDB 5.3.1 Release Notes

Release Date: xx, 2022

TiDB version: 5.3.1

## Compatibility changes

TiDB

TiKV

PD

TiDB Dashboard

TiFlash

Tools

    - Backup & Restore (BR)

    - TiCDC

    - Dumpling

    - TiDB Binlog

    - TiDB Lightning

## Feature enhancements

## __unsorted

+ TiDB

    - Fix date formate identifies '\n' as invalid separator [#32503](https://github.com/pingcap/tidb/pull/32503)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#28144](https://github.com/pingcap/tidb/issues/28144)
    - Fix `alter column set default` wrongly updates the schema [#31074](https://github.com/pingcap/tidb/issues/31074)
    - Fix a bug that caused region unbalanced after restoring. [#31034](https://github.com/pingcap/tidb/issues/31034)
    - Fix a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31745](https://github.com/pingcap/tidb/issues/31745)
    - Fix greatest and least function with collation get wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - Fix the crash or error when generating an empty mpp task list. [#31636](https://github.com/pingcap/tidb/issues/31636)
    - release-note [#31667](https://github.com/pingcap/tidb/pull/31667)
    - Fix index join bug caused by innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - Fix double column value are different with MySQL after changing column type from float to double [#31372](https://github.com/pingcap/tidb/issues/31372)
    - Planner: make queries with the extra column `_tidb_rowid` can use PointGet [#31543](https://github.com/pingcap/tidb/issues/31543)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#30468](https://github.com/pingcap/tidb/issues/30468)
    - Fix a panic that may happen when using `on duplicate key update`. [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the bug that lighting return error if gcs url starts with gs:// [#32591](https://github.com/pingcap/tidb/issues/32591)
    - [#30999](https://github.com/pingcap/tidb/pull/30999)
    - Fix a bug that the `mysql_stmt_field_count` returned to mysql client is incorrect in prepare protocal when handling union statement. [#30971](https://github.com/pingcap/tidb/issues/30971)
    - Make tidb-lightning pre-check output message clearer [#30395](https://github.com/pingcap/tidb/issues/30395)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30018](https://github.com/pingcap/tidb/issues/30018)
    - Fix the but that lightning doesn't report error if s3 storage path not exist. [#28031](https://github.com/pingcap/tidb/issues/28031)
    - planner: regard NULL as point when accessing composite index [#29650](https://github.com/pingcap/tidb/issues/29650)
    - Fix a bug when reducing order by clause for the index which leads to the wrong result. [#30271](https://github.com/pingcap/tidb/issues/30271)
    - The TiDB server now maps a user to an entry in the mysql.user table more consistently. [#30450](https://github.com/pingcap/tidb/pull/30450)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30172](https://github.com/pingcap/tidb/pull/30172)
    - Lightning: fix log doesn't output to stdout when passing `--log-file="-"` [#29876](https://github.com/pingcap/tidb/issues/29876)

+ TiKV

    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11993](https://github.com/tikv/tikv/issues/11993)
    - Increase the size of write batch for raftlog GC to speed up GC. [#11404](https://github.com/tikv/tikv/issues/11404)
    - Fix the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11746](https://github.com/tikv/tikv/issues/11746)
    - Fix potential high latency caused by destroying a peer [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11424](https://github.com/tikv/tikv/issues/11424)
    - release-note [#11805](https://github.com/tikv/tikv/pull/11805)
    - Fix wrong `any_value` result when there are regions returning empty result [#11735](https://github.com/tikv/tikv/issues/11735)
    - Update procfs to 0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#10533](https://github.com/tikv/tikv/issues/10533)
    - Please add a release note.None [#11632](https://github.com/tikv/tikv/pull/11632)
    - Please add a release note. [#11616](https://github.com/tikv/tikv/pull/11616)
    - Fix panic when cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Fix resolved ts lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix connection abort when too many raft entries are batched into one messages [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    - Do not panic when RocksDB flush or compaction hits disk capacity [#11224](https://github.com/tikv/tikv/issues/11224)
    - Make tikv-ctl detect raft db correctly [#11393](https://github.com/tikv/tikv/issues/11393)
    - Fix incorrect by-instance gRPC average duration. [#11299](https://github.com/tikv/tikv/issues/11299)

+ PingCAP/TiFlash

    - Fix error result for function `in` [#4076](https://github.com/pingcap/tics/pull/4076)
    - Fix cast to decimal overflow bug [#4073](https://github.com/pingcap/tics/pull/4073)
    - Fix date format identifies '\n' as invalid separator [#4059](https://github.com/pingcap/tics/pull/4059)
    - Fix cannot find column error after add column when remote read was triggered in tiflash [#4027](https://github.com/pingcap/tics/pull/4027)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3936](https://github.com/pingcap/tics/pull/3936)
    - Fix the problem of TiFlash crashing when the memory limit is enabled [#3918](https://github.com/pingcap/tics/pull/3918)
    - Fix the bug that castStringAsReal has different behaivor between tiflash and tikv/tidb. [#3757](https://github.com/pingcap/tics/pull/3757)
    - Avoid false alert of `DB::Exception: Encode type of coprocessor response is not CHBlock` [#3740](https://github.com/pingcap/tics/pull/3740)
    - Fix random `EstablishMPPConnection` fail after TiFlash server restart. [#3708](https://github.com/pingcap/tics/pull/3708)
    - Fixed the inconsistent behavior of CastStringAsDecimal between tiflash and tidb/tikv. [#3680](https://github.com/pingcap/tics/pull/3680)
    - Fix potential data inconsistency after altering a primary key column to a larger int data type [#3570](https://github.com/pingcap/tics/pull/3570)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3480](https://github.com/pingcap/tics/pull/3480)
    - Fix tiflash randomly crash when a mpp query is killed. [#3451](https://github.com/pingcap/tics/pull/3451)

+ PD

    - None. [#4663](https://github.com/tikv/pd/pull/4663)
    - Fix a bug that operate steps may contain unnecessary or empty JointConsensus steps in certain conditions 
    - Fix a bug when demoting single voter directly [#4362](https://github.com/tikv/pd/issues/4362)
    - Fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4390](https://github.com/tikv/pd/issues/4390)
    - Improve DR_STATE file content format [#4341](https://github.com/tikv/pd/issues/4341)
    - Fix data race when updating replication mode configuration [#4325](https://github.com/tikv/pd/issues/4325)
    - Fix the issue that the RLock is not released [#4354](https://github.com/tikv/pd/issues/4354)

+ Tools

    + TiCDC

        - `None`. [#4660](https://github.com/pingcap/tiflow/issues/4660)
        - Support more data types with default value attribute, and fix potential data inconsistency caused by default value logic [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix a bug that long varchar will report error of "Column length too big..." [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - `None`. [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Allow user set the configuration of Kafka producer dial/write/read timeout [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - `None`. [#4404](https://github.com/pingcap/tiflow/issues/4404)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic. [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - None. [#4353](https://github.com/pingcap/tiflow/issues/4353)
        - `None`. [#4159](https://github.com/pingcap/tiflow/issues/4159)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)
        - Add exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Fix a bug that upstream metrics won't update if no query-status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        - `None`. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix kv client cached region metric could be negative. [#4290](https://github.com/pingcap/tiflow/pull/4290)
        - `None` [#4266](https://github.com/pingcap/tiflow/issues/4266)
        - `None`. [#4223](https://github.com/pingcap/tiflow/issues/4223)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - `None`. [#4159](https://github.com/pingcap/tiflow/issues/4159)
        - `None`. [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - Support updating table schema when using dmctl binlog to skip some ddls [#4177](https://github.com/pingcap/tiflow/issues/4177)
        - `None`. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - `None`. [#4163](https://github.com/pingcap/tiflow/pull/4163)
        - `None`. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Fix a bug that stop-task during load phase will cause the source always tries to transfer to a worker [#3771](https://github.com/pingcap/tiflow/issues/3771)
        - Fix a bug that wrong progress in query-status for loader [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - Fix the bug that http API panic when the processor info we want to get is not exist. [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - Reduce "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4083](https://github.com/pingcap/tiflow/pull/4083)
        - `None`. [#4079](https://github.com/pingcap/tiflow/pull/4079)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix a bug that when master and worker restart in a particular order, relay status in DM-master is wrong [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - Fix a bug that DM-worker can't boot up after restart [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - Fix a bug that DM task will failed when PARTITION DDL cost a long time [#3854](https://github.com/pingcap/tiflow/issues/3854)
        - Fix syntax error if DDL has a special comment. [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - release-note [#3976](https://github.com/pingcap/tiflow/pull/3976)
        - Fix the owner may be blocked when initializing the changefeed caused by a bad network connection to the sink [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - `None` [#3953](https://github.com/pingcap/tiflow/pull/3953)
        - Fix a bug that DM may report "invalid sequence" when upstream is MySQL 8.0. Fix a bug that upstream will die on SHOW SLAVE HOSTS [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - Fix a bug that redo logs are not cleaned up when removing a paused changefeed. [#3919](https://github.com/pingcap/tiflow/pull/3919)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3882](https://github.com/pingcap/tiflow/pull/3882)
        - Add pre clean up process when s3 enable, fix #3523 [#3878](https://github.com/pingcap/tiflow/pull/3878)
        - Add redo log related metric [#3877](https://github.com/pingcap/tiflow/pull/3877)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix a bug of data loss when DM does finer grained retry [#3487](https://github.com/pingcap/tiflow/issues/3487)
        - Fix mounter default date value not support [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#4054](https://github.com/pingcap/tiflow/issues/4054)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - `None`. [#3765](https://github.com/pingcap/tiflow/pull/3765)
        - `None`. [#3712](https://github.com/pingcap/tiflow/pull/3712)
        - Please add a release note. Fix kvclient takes too long time to recover [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - The Avro sink was updated to handle JSON columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3628](https://github.com/pingcap/tiflow/pull/3628)
        - Fix changefeed checkpoint lag negative value error [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix HTTP API not working when there are TiCDC nodes of different versions in one cdc cluster. [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - Fix a bug when too often query status is called in Load unit, DM-worker may encounter data race or panic [#3457](https://github.com/pingcap/tiflow/issues/3457)
        - Fix OOM in container environments. [#3439](https://github.com/pingcap/tiflow/pull/3439)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3868](https://github.com/pingcap/tiflow/pull/3868)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3256](https://github.com/pingcap/tiflow/pull/3256)

## Bug Fixes

+ TiDB

    - Planner: fix wrong range calculation for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the bug that lightning will skip some precheck items when restart [#30772](https://github.com/pingcap/tidb/issues/30772)
    - Fix the error that if tidb-lightning doesn't has permission to access mysql.tidb, it will generate kv with wrong format. [#31088](https://github.com/pingcap/tidb/issues/31088)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Add a new config to control whether support incremental import. [#27919](https://github.com/pingcap/tidb/issues/27919)
    - Executor: fix pipelined window invalid memory address [#30326](https://github.com/pingcap/tidb/issues/30326)
    - Fix the problem that window function may return different results when using transaction or not. [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix wrong flen for CastAsString funtion [#29513](https://github.com/pingcap/tidb/issues/29513)
    - Expression: Fix the issue that length information is wrong when converting Decimal to String [#29417](https://github.com/pingcap/tidb/issues/29417)

+ PingCAP/TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3625](https://github.com/pingcap/tics/pull/3625)

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix incomplete replicate file [#4328](https://github.com/tikv/pd/issues/4328)
    - Fix panic issue after TiKV node scales in [#4344](https://github.com/tikv/pd/issues/4344)
