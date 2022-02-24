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
    (dup) - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the bug that lighting return error if gcs url starts with gs:// [#32591](https://github.com/pingcap/tidb/issues/32591)
    - [#30999](https://github.com/pingcap/tidb/pull/30999)
    - Fix a bug that the `mysql_stmt_field_count` returned to mysql client is incorrect in prepare protocal when handling union statement. [#30971](https://github.com/pingcap/tidb/issues/30971)
    - Make tidb-lightning pre-check output message clearer [#30395](https://github.com/pingcap/tidb/issues/30395)
    - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30018](https://github.com/pingcap/tidb/issues/30018)
    (dup) - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
    - planner: regard NULL as point when accessing composite index [#29650](https://github.com/pingcap/tidb/issues/29650)
    - Fix a bug when reducing order by clause for the index which leads to the wrong result. [#30271](https://github.com/pingcap/tidb/issues/30271)
    - The TiDB server now maps a user to an entry in the mysql.user table more consistently. [#30450](https://github.com/pingcap/tidb/pull/30450)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#30172](https://github.com/pingcap/tidb/pull/30172)
    - Lightning: fix log doesn't output to stdout when passing `--log-file="-"` [#29876](https://github.com/pingcap/tidb/issues/29876)

+ TiKV

    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11993](https://github.com/tikv/tikv/issues/11993)
    - Increase the size of write batch for raftlog GC to speed up GC. [#11404](https://github.com/tikv/tikv/issues/11404)
    (dup) - Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix a potential panic (#11746) when snapshot files have been deleted but the peer's status is still Applying. [#11746](https://github.com/tikv/tikv/issues/11746)
    (dup) - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11424](https://github.com/tikv/tikv/issues/11424)
    - release-note [#11805](https://github.com/tikv/tikv/pull/11805)
    (dup) - Fix a bug that the `any_value` function returns a wrong result when regions are empty [#11735](https://github.com/tikv/tikv/issues/11735)
    (dup) - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    (dup) - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    - Please add a release note.None [#11632](https://github.com/tikv/tikv/pull/11632)
    - Please add a release note. [#11616](https://github.com/tikv/tikv/pull/11616)
    - Fix panic when cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    (dup) - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#11526](https://github.com/tikv/tikv/issues/11526)
    (dup) - Fix the deadlock issue that happens occasionally when coroutines run too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    (dup) - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    (dup) - Fix the issue that TiKV cannot detect the memory lock when TiKV perform a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix the issue that RocksDB flush or compaction causes panic when the disk capacity is full [#11224](https://github.com/tikv/tikv/issues/11224)
    (dup) - Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    (dup) - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)

+ TiFlash

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
    (dup) - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)
    - Improve DR_STATE file content format [#4341](https://github.com/tikv/pd/issues/4341)
    - Fix data race when updating replication mode configuration [#4325](https://github.com/tikv/pd/issues/4325)
    - Fix the issue that the RLock is not released [#4354](https://github.com/tikv/pd/issues/4354)

+ Tools

    + TiCDC

        - `None`. [#4660](https://github.com/pingcap/tiflow/issues/4660)
        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix a bug that long varchar will report error of "Column length too big..." [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - `None`. [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Allow user set the configuration of Kafka producer dial/write/read timeout [#4385](https://github.com/pingcap/tiflow/issues/4385)
        (dup) - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - `None`. [#4404](https://github.com/pingcap/tiflow/issues/4404)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic. [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - None. [#4353](https://github.com/pingcap/tiflow/issues/4353)
        - `None`. [#4159](https://github.com/pingcap/tiflow/issues/4159)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)
        (dup) - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        (dup) - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix kv client cached region metric could be negative. [#4290](https://github.com/pingcap/tiflow/pull/4290)
        - `None` [#4266](https://github.com/pingcap/tiflow/issues/4266)
        - `None`. [#4223](https://github.com/pingcap/tiflow/issues/4223)
        (dup) - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - `None`. [#4159](https://github.com/pingcap/tiflow/issues/4159)
        (dup) - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        (dup) - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - `None`. [#4163](https://github.com/pingcap/tiflow/pull/4163)
        (dup) - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Fix a bug that stop-task during load phase will cause the source always tries to transfer to a worker [#3771](https://github.com/pingcap/tiflow/issues/3771)
        - Fix a bug that wrong progress in query-status for loader [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - Fix the bug that http API panic when the processor info we want to get is not exist. [#3840](https://github.com/pingcap/tiflow/issues/3840)
        (dup) - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        (dup) - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Manage sink checkpoint per table to avoid checkpointTs advances unexpected. [#4083](https://github.com/pingcap/tiflow/pull/4083)
        - `None`. [#4079](https://github.com/pingcap/tiflow/pull/4079)
        (dup) - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        (dup) - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - Fix a bug that when master and worker restart in a particular order, relay status in DM-master is wrong [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - Fix a bug that DM-worker can't boot up after restart [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - Fix a bug that DM task will failed when PARTITION DDL cost a long time [#3854](https://github.com/pingcap/tiflow/issues/3854)
        (dup) - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - release-note [#3976](https://github.com/pingcap/tiflow/pull/3976)
        (dup) - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - `None` [#3953](https://github.com/pingcap/tiflow/pull/3953)
        - Fix a bug that DM may report "invalid sequence" when upstream is MySQL 8.0. Fix a bug that upstream will die on SHOW SLAVE HOSTS [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - Fix a bug that redo logs are not cleaned up when removing a paused changefeed. [#3919](https://github.com/pingcap/tiflow/pull/3919)
        (dup) - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3882](https://github.com/pingcap/tiflow/pull/3882)
        - Add pre clean up process when s3 enable, fix #3523 [#3878](https://github.com/pingcap/tiflow/pull/3878)
        - Add redo log related metric [#3877](https://github.com/pingcap/tiflow/pull/3877)
        (dup) - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix a bug of data loss when DM does finer grained retry [#3487](https://github.com/pingcap/tiflow/issues/3487)
        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        (dup) - Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        (dup) - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        (dup) - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - `None`. [#3765](https://github.com/pingcap/tiflow/pull/3765)
        - `None`. [#3712](https://github.com/pingcap/tiflow/pull/3712)
        (dup) - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)
        (dup) - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix cli don't work when cli cert's common name was not added in config that use for start cdc server. [#3628](https://github.com/pingcap/tiflow/pull/3628)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix HTTP API not working when there are TiCDC nodes of different versions in one cdc cluster. [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - Fix a bug when too often query status is called in Load unit, DM-worker may encounter data race or panic [#3457](https://github.com/pingcap/tiflow/issues/3457)
        - Fix OOM in container environments. [#3439](https://github.com/pingcap/tiflow/pull/3439)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3868](https://github.com/pingcap/tiflow/pull/3868)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3256](https://github.com/pingcap/tiflow/pull/3256)

## Bug Fixes

+ TiDB

    - Planner: fix wrong range calculation for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    (dup) - Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)
    (dup) - Fix the issue that some checks are skipped when TiDB Lightning is restarted [#30772](https://github.com/pingcap/tidb/issues/30772)
    (dup) - Fix the issue of wrong import result that occurs when TiDB Lightning does not have the privilege to access the `mysql.tidb` table [#31088](https://github.com/pingcap/tidb/issues/31088)
    (dup) - Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Add a new config to control whether support incremental import. [#27919](https://github.com/pingcap/tidb/issues/27919)
    - Executor: fix pipelined window invalid memory address [#30326](https://github.com/pingcap/tidb/issues/30326)
    (dup) - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    (dup) - Fix the issue that the SQL statements that contain `cast(integer as char) union string` return wrong results [#29513](https://github.com/pingcap/tidb/issues/29513)
    (dup) - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)

+ TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3625](https://github.com/pingcap/tics/pull/3625)

+ PD

    (dup) - Fix a bug that the schedule generated by the region scatterer might decrease the number of peers [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix incomplete replicate file [#4328](https://github.com/tikv/pd/issues/4328)
    (dup) - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
