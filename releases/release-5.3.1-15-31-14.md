---
title: TiDB 5.3.1 Release Notes
category: Releases
---



# TiDB 5.3.1 Release Notes

Release Date: February 24, 2022

TiDB version: 5.3.1

## __unsorted

+ PingCAP/TiDB

    - fix date formate identifies '\n' as invalid separator [#32503](https://github.com/pingcap/tidb/pull/32503)
    - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#32389](https://github.com/pingcap/tidb/pull/32389)
    - fix `alter column set default` wrongly updates the schema [#32264](https://github.com/pingcap/tidb/pull/32264)
    - Fix a bug that caused region unbalanced after restoring. [#32128](https://github.com/pingcap/tidb/pull/32128)
    - Fixed a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31841](https://github.com/pingcap/tidb/pull/31841)
    - fix greatest and least function with collation get wrong result [#31837](https://github.com/pingcap/tidb/pull/31837)
    - Fix the crash or error when generating an empty mpp task list. [#31695](https://github.com/pingcap/tidb/pull/31695)
    - ```release-note [#31667](https://github.com/pingcap/tidb/pull/31667)
    - Fix index join bug caused by innerWorker panic [#31614](https://github.com/pingcap/tidb/pull/31614)
    - Fix double column value are different with MySQL after changing column type from float to double [#31572](https://github.com/pingcap/tidb/pull/31572)
    - planner: make queries with the extra column `_tidb_rowid` can use PointGet [#31552](https://github.com/pingcap/tidb/pull/31552)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#31350](https://github.com/pingcap/tidb/pull/31350)
    - Fix a panic that may happen when using `on duplicate key update`. [#31344](https://github.com/pingcap/tidb/pull/31344)
    - Fix the bug that lighting return error if gcs url starts with gs:// [#31169](https://github.com/pingcap/tidb/pull/31169)
    - ```release-note [#30999](https://github.com/pingcap/tidb/pull/30999)
    - Fix a bug that the `mysql_stmt_field_count` returned to mysql client is incorrect in prepare protocal when handling union statement. [#30997](https://github.com/pingcap/tidb/pull/30997)
    - make tidb-lightning pre-check output message clearer [#30888](https://github.com/pingcap/tidb/pull/30888)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30876](https://github.com/pingcap/tidb/pull/30876)
    - Fix the but that lightning doesn't report error if s3 storage path not exist. [#30714](https://github.com/pingcap/tidb/pull/30714)
    - planner: regard NULL as point when accessing composite index [#30614](https://github.com/pingcap/tidb/pull/30614)
    - fix a bug when reducing order by clause for the index which leads to the wrong result. [#30552](https://github.com/pingcap/tidb/pull/30552)
    - The TiDB server now maps a user to an entry in the mysql.user table more consistently. [#30450](https://github.com/pingcap/tidb/pull/30450)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30172](https://github.com/pingcap/tidb/pull/30172)
    - lightning: fix log doesn't output to stdout when passing `--log-file="-"` [#29939](https://github.com/pingcap/tidb/pull/29939)


+ TiKV/TiKV

    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#12000](https://github.com/tikv/tikv/pull/12000)
    - Increase the size of write batch for raftlog GC to speed up GC. [#11971](https://github.com/tikv/tikv/pull/11971)
    - Fixes the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11913](https://github.com/tikv/tikv/pull/11913)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11908](https://github.com/tikv/tikv/pull/11908)
    - fix potential high latency caused by destroying a peer [#11880](https://github.com/tikv/tikv/pull/11880)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11857](https://github.com/tikv/tikv/pull/11857)
    - ```release-note [#11805](https://github.com/tikv/tikv/pull/11805)
    - Fix wrong `any_value` result when there are regions returning empty result [#11744](https://github.com/tikv/tikv/pull/11744)
    - update procfs to 0.12.0 [#11726](https://github.com/tikv/tikv/pull/11726)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#11637](https://github.com/tikv/tikv/pull/11637)
    - Please add a release note.
None [#11632](https://github.com/tikv/tikv/pull/11632)
    - Please add a release note.
If you don't think this PR needs a release note then fill it with None.
If this PR will be picked to release branch, then a release note is probably required. [#11616](https://github.com/tikv/tikv/pull/11616)
    - Fix panic when cgroup controller is not mounted [#11582](https://github.com/tikv/tikv/pull/11582)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11568](https://github.com/tikv/tikv/pull/11568)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11564](https://github.com/tikv/tikv/pull/11564)
    - Fix resolved ts lag increased after stoping a tikv [#11537](https://github.com/tikv/tikv/pull/11537)
    - Fix connection abort when too many raft entries are batched into one messages [#11535](https://github.com/tikv/tikv/pull/11535)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11513](https://github.com/tikv/tikv/pull/11513)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11456](https://github.com/tikv/tikv/pull/11456)
    - Do not panic when RocksDB flush or compaction hits disk capacity [#11428](https://github.com/tikv/tikv/pull/11428)
    - make tikv-ctl detect raft db correctly [#11413](https://github.com/tikv/tikv/pull/11413)
    - Fix incorrect by-instance gRPC average duration. [#11330](https://github.com/tikv/tikv/pull/11330)


+ PingCAP/TiFlash

    - fix error result for function `in` [#4076](https://github.com/pingcap/tics/pull/4076)
    - Fix cast to decimal overflow bug [#4073](https://github.com/pingcap/tics/pull/4073)
    - fix date format identifies '\n' as invalid separator [#4059](https://github.com/pingcap/tics/pull/4059)
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
    - - fix a bug that operate steps may contain unnecessary or empty JointConsensus steps in certain conditions 
- fix a bug when demoting single voter directly [#4552](https://github.com/tikv/pd/pull/4552)
    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4435](https://github.com/tikv/pd/pull/4435)
    - Improve DR_STATE file content format [#4386](https://github.com/tikv/pd/pull/4386)
    - Fix data race when updating replication mode configuration [#4370](https://github.com/tikv/pd/pull/4370)
    - Fix the issue that the RLock is not released [#4358](https://github.com/tikv/pd/pull/4358)


+ Tools

    + PingCAP/TiCDC

        - `None`. [#4659](https://github.com/pingcap/tiflow/pull/4659)
        - Support more data types with default value attribute, and fix potential data inconsistency caused by default value logic [#4652](https://github.com/pingcap/tiflow/pull/4652)
        - Fix a bug that long varchar will report error of "Column length too big..." [#4645](https://github.com/pingcap/tiflow/pull/4645)
        - `None`. [#4641](https://github.com/pingcap/tiflow/pull/4641)
        - `None`. [#4614](https://github.com/pingcap/tiflow/pull/4614)
        - `None`. [#4594](https://github.com/pingcap/tiflow/pull/4594)
        - `None`. [#4574](https://github.com/pingcap/tiflow/pull/4574)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4532](https://github.com/pingcap/tiflow/pull/4532)
        - allow user set the configuration of Kafka producer dial/write/read timeout [#4526](https://github.com/pingcap/tiflow/pull/4526)
        - Fix a bug that MySQL sink will generate duplicated replace SQL if `batch-replace-enable` is disabled. [#4508](https://github.com/pingcap/tiflow/pull/4508)
        - `None`. [#4465](https://github.com/pingcap/tiflow/pull/4465)
        - `None`. [#4462](https://github.com/pingcap/tiflow/pull/4462)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic. [#4439](https://github.com/pingcap/tiflow/pull/4439)
        - None. [#4430](https://github.com/pingcap/tiflow/pull/4430)
        - `None`. [#4398](https://github.com/pingcap/tiflow/pull/4398)
        - `None`. [#4345](https://github.com/pingcap/tiflow/pull/4345)
        - Add exponential backoff mechanism for restarting a changefeed. [#4339](https://github.com/pingcap/tiflow/pull/4339)
        - Fix a bug that upstream metrics won't update if no query-status [#4332](https://github.com/pingcap/tiflow/pull/4332)
        - `None`. [#4323](https://github.com/pingcap/tiflow/pull/4323)
        - Fix kv client cached region metric could be negative. [#4290](https://github.com/pingcap/tiflow/pull/4290)
        - `None` [#4285](https://github.com/pingcap/tiflow/pull/4285)
        - `None`. [#4278](https://github.com/pingcap/tiflow/pull/4278)
        - Fix the problem that TiCDC cannot send messages when `min.insync.replicas` is less than `replication-factor` [#4271](https://github.com/pingcap/tiflow/pull/4271)
        - `None`. [#4254](https://github.com/pingcap/tiflow/pull/4254)
        - `None`. [#4227](https://github.com/pingcap/tiflow/pull/4227)
        - Support updating table schema when using dmctl binlog to skip some ddls [#4225](https://github.com/pingcap/tiflow/pull/4225)
        - `None`. [#4209](https://github.com/pingcap/tiflow/pull/4209)
        - Fix the potential panic issue that occurs when changefeed info is removed from etcd. [#4183](https://github.com/pingcap/tiflow/pull/4183)
        - `None`. [#4163](https://github.com/pingcap/tiflow/pull/4163)
        - `None`. [#4162](https://github.com/pingcap/tiflow/pull/4162)
        - Fix a bug that stop-task during load phase will cause the source always tries to transfer to a worker [#4145](https://github.com/pingcap/tiflow/pull/4145)
        - `fix a bug that wrong progress in query-status for loader`. [#4143](https://github.com/pingcap/tiflow/pull/4143)
        - Fix the bug that http API panic when the processor info we want to get is not exist. [#4123](https://github.com/pingcap/tiflow/pull/4123)
        - Reduce "EventFeed retry rate limited" logs [#4111](https://github.com/pingcap/tiflow/pull/4111)
        - Fix a bug that can cause changefeed stuck due to a deadlock occurs. [#4099](https://github.com/pingcap/tiflow/pull/4099)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4083](https://github.com/pingcap/tiflow/pull/4083)
        - `None`. [#4079](https://github.com/pingcap/tiflow/pull/4079)
        - Set `max-message-bytes` default to 10M, and use the min value with topic and broker to initialize the producer. [#4063](https://github.com/pingcap/tiflow/pull/4063)
        - Fix nil pointer panic encountered when scheduler cleanup finished operations [#4016](https://github.com/pingcap/tiflow/pull/4016)
        - Fix a bug that when master and worker restart in a particular order, relay status in DM-master is wrong [#4009](https://github.com/pingcap/tiflow/pull/4009)
        - Fix a bug that DM-worker can't boot up after restart [#4005](https://github.com/pingcap/tiflow/pull/4005)
        - Fix a bug that DM task will failed when PARTITION DDL cost a long time [#3995](https://github.com/pingcap/tiflow/pull/3995)
        - Fix syntax error if DDL has a special comment. [#3978](https://github.com/pingcap/tiflow/pull/3978)
        - ```release-note [#3976](https://github.com/pingcap/tiflow/pull/3976)
        - Fix the owner may be blocked when initializing the changefeed caused by a bad network connection to the sink [#3964](https://github.com/pingcap/tiflow/pull/3964)
        - `None` [#3953](https://github.com/pingcap/tiflow/pull/3953)
        - fix a bug that DM may report "invalid sequence" when upstream is MySQL 8.0
fix a bug that upstream will die on SHOW SLAVE HOSTS [#3934](https://github.com/pingcap/tiflow/pull/3934)
        - Fix a bug that redo logs are not cleaned up when removing a paused changefeed. [#3919](https://github.com/pingcap/tiflow/pull/3919)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3906](https://github.com/pingcap/tiflow/pull/3906)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3882](https://github.com/pingcap/tiflow/pull/3882)
        - add pre clean up process when s3 enable, fix #3523 [#3878](https://github.com/pingcap/tiflow/pull/3878)
        - add redo log related metric [#3877](https://github.com/pingcap/tiflow/pull/3877)
        - Fix the issue of changefeed resuming automatically after upgrading cluster [#3865](https://github.com/pingcap/tiflow/pull/3865)
        - Fix a bug of data loss when DM does finer grained retry [#3860](https://github.com/pingcap/tiflow/pull/3860)
        - Fix mounter default date value not support [#3859](https://github.com/pingcap/tiflow/pull/3859)
        - Add an alert rule when ticdc has no owner for more than 10 minutes. [#3832](https://github.com/pingcap/tiflow/pull/3832)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#3795](https://github.com/pingcap/tiflow/pull/3795)
        - Fix the problem that old value is not forced on automatically in `canal-json` and `maxwell` protocols [#3783](https://github.com/pingcap/tiflow/pull/3783)
        - `None`. [#3765](https://github.com/pingcap/tiflow/pull/3765)
        - `None`. [#3712](https://github.com/pingcap/tiflow/pull/3712)
        - Please add a release note.
fix kvclient takes too long time to recover [#3663](https://github.com/pingcap/tiflow/pull/3663)
        - The Avro sink was updated to handle JSON columns [#3649](https://github.com/pingcap/tiflow/pull/3649)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3628](https://github.com/pingcap/tiflow/pull/3628)
        - fix changefeed checkpoint lag negative value error [#3536](https://github.com/pingcap/tiflow/pull/3536)
        - Fix HTTP API not working when there are TiCDC nodes of different versions in one cdc cluster. [#3530](https://github.com/pingcap/tiflow/pull/3530)
        - Fix a bug when too often query status is called in Load unit, DM-worker may encounter data race or panic [#3468](https://github.com/pingcap/tiflow/pull/3468)
        - Fix OOM in container environments. [#3439](https://github.com/pingcap/tiflow/pull/3439)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3389](https://github.com/pingcap/tiflow/pull/3389)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3256](https://github.com/pingcap/tiflow/pull/3256)


## Bug Fixes

+ PingCAP/TiDB

    - planner: fix wrong range calculation for Nulleq function on Enum values [#32495](https://github.com/pingcap/tidb/pull/32495)
    - Fix the bug that indexHashJoin may return the error `send on closed channel`. [#31448](https://github.com/pingcap/tidb/pull/31448)
    - Fix the bug that lightning will skip some precheck items when restart [#31183](https://github.com/pingcap/tidb/pull/31183)
    - Fix the error that if tidb-lightning doesn't has permission to access mysql.tidb, it will generate kv with wrong format. [#31152](https://github.com/pingcap/tidb/pull/31152)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31071](https://github.com/pingcap/tidb/pull/31071)
    - Add a new config to control whether support incremental import. [#30926](https://github.com/pingcap/tidb/pull/30926)
    - executor: fix pipelined window invalid memory address [#30460](https://github.com/pingcap/tidb/pull/30460)
    - Fix the problem that window function may return different results when using transaction or not. [#30392](https://github.com/pingcap/tidb/pull/30392)
    - Fix wrong flen for CastAsString funtion [#30058](https://github.com/pingcap/tidb/pull/30058)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#30016](https://github.com/pingcap/tidb/pull/30016)


+ PingCAP/TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3625](https://github.com/pingcap/tics/pull/3625)


+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4577](https://github.com/tikv/pd/pull/4577)
    - Fix incomplete replicate file [#4394](https://github.com/tikv/pd/pull/4394)
    - Fix panic issue after TiKV node scales in [#4382](https://github.com/tikv/pd/pull/4382)


