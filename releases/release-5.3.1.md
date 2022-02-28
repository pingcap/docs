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

TiDB

    - The TiDB server now maps a user to an entry in the mysql.user table more consistently. [#30450](https://github.com/pingcap/tidb/issues/30450)

TiKV

    - Reduce CDC recovery time by reduce the number regions that need resolved lock. [#11993](https://github.com/tikv/tikv/issues/11993)
    - Increase the size of write batch for raftlog GC to speed up GC. [#11404](https://github.com/tikv/tikv/issues/11404)

    (dup) - Update the proc filesystem (procfs) to v0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)

PD

    - Improve DR_STATE file content format [#4341](https://github.com/tikv/pd/issues/4341)

Tools

    - TiCDC

        - Expose Kafka producer's configuration parameters can be configured [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - Add pre clean up process when s3 enable [#3878](https://github.com/pingcap/tiflow/issues/3523)
        - TiCDC client works now when cert's common name was not specified [#3882](https://github.com/pingcap/tiflow/pull/3882)
        - HTTP API works as expected now if there are TiCDC nodes of different versions in one cdc cluster. [#3483](https://github.com/pingcap/tiflow/issues/3483)
        - Correct query-staus progress for loader [#3252](https://github.com/pingcap/tiflow/issues/3252)
        - Manage sink checkpoint per table to avoid checkpoint timestamp advance unexpected [#4083](https://github.com/pingcap/tiflow/pull/4083)

        (dup) - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        (dup) - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/tiflow/issues/3337)
        (dup) - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        (dup) - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        (dup) - Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        (dup) - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

    - Lightning

        - Make tidb-lightning pre-check output message clearer [#30395](https://github.com/pingcap/tiflow/issues/30395)

## Bug Fixes

+ TiDB

    - Fix date formate identifies '\n' as invalid separator [#32503](https://github.com/pingcap/tidb/issues/32503)
    - Fix alter column set default wrongly updates the schema [#31074](https://github.com/pingcap/tidb/issues/31074)
    - Fix a bug that turning on tidb_restricted_read_only won't automatically turn on tidb_super_read_only [#31745](https://github.com/pingcap/tidb/issues/31745)
    - Fix greatest and least function with collation get wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - Fix the crash or error when generating an empty mpp task list. [#31636](https://github.com/pingcap/tidb/issues/31636)
    - Fix index join bug caused by innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - Fix double column value are different with MySQL after changing column type from float to double [#31372](https://github.com/pingcap/tidb/issues/31372)
    - Fix a data race that may cause "invalid transaction" error when executing a query using index lookup join. [#30468](https://github.com/pingcap/tidb/issues/30468)
    - Fix a bug when reducing order by clause for the index which leads to the wrong result. [#30271](https://github.com/pingcap/tidb/issues/30271)
    - Fix `MaxDays` and `MaxBackups` not working for slow log. [#25716](https://github.com/pingcap/tidb/issues/25716)

    (dup) - Fix the issue that executing the INSERT ... SELECT ... ON DUPLICATE KEY UPDATE statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)

TiKV

    - Fix a potential panic when snapshot files have been deleted but the peer's status is still Applying. [#11746](https://github.com/tikv/tikv/issues/11746)
    - Fix possible QPS drop when `level0_slowdown_trigger` is set explicitly with flow control enabled. [#11424](https://github.com/tikv/tikv/issues/11424)
    - Fix panic when cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - Fix resolved ts lag increased after stoping a tikv [#11352](https://github.com/tikv/tikv/pull/11352)

    (dup) - Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    (dup) - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    (dup) - Fix a bug that the `any_value` function returns a wrong result when regions are empty [#11735](https://github.com/tikv/tikv/issues/11735)
    (dup) - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
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

    - Fix the problem that `cast(arg as decimal(x,y))` return wrong result when `arg` overflows the range of `decimal(x,y)`
    - Fix the problem of TiFlash crashing when `max_memory_usage` and `max_memory_usage_for_all_queries` are enabled
    - Fix the problem that `cast(string ad real)` returns wrong result
    - Fixed the problem that cast(string as decimal) returns wrong result
    - Fix potential data inconsistency after altering a primary key column to a larger int data type
    - Fix the problem that `select (arg0, arg1) in (x,y)` returns wrong result
    - Fix the problem that tiflash randomly crash when a mpp query is killed
    - Fix the problem that str_to_date return wrong result when the input argument has leading zeros.
    - Fix the problem that query gets wrong results when the filter is like `where <string>`
    - Fix the problem that `cast(string as datetime)` return wrong result when the string is of format `%Y-%m-%d\n%H:%i:%s`

+ PD

    - Fix a bug that the operater steps may contain unnecessary or empty JointConsensus steps in certain conditions [#4362](https://github.com/tikv/pd/issues/4362)
    - Fix a bug that the operator could not be executed when demoting single voter directly [#4444](https://github.com/tikv/pd/issues/4444)
    - Fix data race when updating replication mode configuration [#4325](https://github.com/tikv/pd/issues/4325)
    - Fix a bug that the RLock is not released in certain conditions [#4354](https://github.com/tikv/pd/issues/4354)

    (dup) - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

Tools

    - Backup & Restore (BR)

        - Fix a bug that caused region unbalanced after restoring. [#31034](https://github.com/pingcap/tiflow/issues/31034)

    - TiCDC

        - Fix a bug that long varchar will report error of "Column length too big" [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - Fix a bug that owner exits abnormally when PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Fix the issue that update statement execute error in safemode may cause DM-worker panic [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - Fix kv client cached region metric could be negative [#4290](https://github.com/pingcap/tiflow/pull/4290)
        - Fix the bug that http API panics when the required processor info is not exist [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - Fix a bug that when master and worker restart in a particular order, relay status in DM-master is wrong [#3478](https://github.com/pingcap/tiflow/issues/3478)
        - Fix a bug that DM-worker can't boot up after restart [#3344](https://github.com/pingcap/tiflow/issues/3344)
        - Fix a bug that DM task will failed when PARTITION DDL cost a long time [#3854](https://github.com/pingcap/tiflow/issues/3854)
        - Fix a bug that DM may report "invalid sequence" when upstream is MySQL 8.0 [#3847](https://github.com/pingcap/tiflow/issues/3847)
        - Fix a bug that redo logs are not cleaned up when removing a paused changefeed. [#3919](https://github.com/pingcap/tiflow/pull/3919)
        - Fix a bug of data loss when DM does finer grained retry [#3487](https://github.com/pingcap/tiflow/issues/3487)
        - Fix OOM in container environments. [#3439](https://github.com/pingcap/tiflow/pull/3439)
        - Stopping tasks during load phase won't cause the source to be transfered [#3771](https://github.com/pingcap/tiflow/issues/3771)

        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        (dup) - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        (dup) - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        (dup) - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        (dup) - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)
        (dup) - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        (dup) - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        (dup) - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        (dup) - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        (dup) - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        (dup) - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        (dup) - Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        (dup) - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        (dup) - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        (dup) - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        (dup) - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)

    - TiDB Lightning

        - Fix the bug that lightning may not clean up metadata schema when some of the import contains no source files. [#28144](https://github.com/pingcap/tidb/issues/28144)
        - Fix the bug that lighting return error if gcs url starts with gs:// [#30254](https://github.com/pingcap/tidb/pull/30254)
        - Avoid tikv trigger auto region split by lower the ingest kv count threshold [#30018](https://github.com/pingcap/tiflow/issues/30018)
        - Fix log doesn't output to stdout when passing --log-file="-" [#29876](https://github.com/pingcap/tiflow/issues/29876)

        (dup) - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist #28031 [#30709](https://github.com/pingcap/tiflow/issues/30709)
