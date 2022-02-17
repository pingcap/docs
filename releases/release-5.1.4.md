---
title: TiDB 5.1.4 Release Notes
category: Releases
---

# TiDB 5.1.4 Release Notes

Release Date: xx, 2022

TiDB version: 5.1.4

## Compatibility changes

+ TiDB

    - Change the default value of the system variable [`tidb_analyze_version`](/system-variables#tidb_analyze_version-new-in-v510) from `2` to `1` [#31748](https://github.com/pingcap/tidb/issues/31748)

+ TiKV

    - TiKV configured with `storage.enable-ttl = true` rejects requests from TiDB. [#27303](https://github.com/pingcap/tidb/issues/27303)

+ Tools

    + TiCDC

        - Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)

## Feature enhancements

+ TiDB

    - Support partition pruning for the built-in `IN` expression in the Range type partition [#26739](https://github.com/pingcap/tidb/issues/26739)
    - Improve the accuracy of tracking memory usage when `IndexJoin` is executed [#28650](https://github.com/pingcap/tidb/issues/28650)

+ TiKV

    - Update procfs to 0.12.0 [#11702](https://github.com/tikv/tikv/issues/11702)
    - Improve raft client error log report [#11959](https://github.com/tikv/tikv/issues/11959)
    - Avoid false "GC can not work" alert under low write flow. [#10664](https://github.com/tikv/tikv/pull/10664)

+ TiFlash

    - support functions of ADDDATE() and DATE_ADD() pushed down to tiflash

+ PD

   (dup) - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - Add the exponential backoff mechanism for restarting a changefeed. [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Reduce checkpoint lag when capturing multiple tables. [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Add metrics for observing the remaining time of incremental scan [#2985](https://github.com/pingcap/tiflow/issues/2985)
        - Reduce the frequency of printing "EventFeed retry rate limited" logs when TiKV encounters OOM errors [#4006](https://github.com/pingcap/tiflow/issues/4006)

        (dup) - Reduce the frequency of CDC reporting "EventFeed retry rate limited" logs when TiKV  encounters OOM error [#4006](https://github.com/pingcap/tiflow/issues/4006)
        (dup)- Optimize checkpoint lag when capturing many tables [#3900](https://github.com/pingcap/tiflow/issues/3900)
        (dup) - Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        (dup) - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)

## Bug fixes

+ TiDB

    - Fix the memory leak bug that occurs when the system variable `tidb_analyze_version` is set to `2` [#29305](https://github.com/pingcap/tidb/pull/29305)
    - Fix the issue that the `MaxDays` and `MaxBackups` configurations do not take effect for the slow log [#25716](https://github.com/pingcap/tidb/issues/25716)
    - Fix a panic issue that might occur when using `ON DUPLICATE KEY UPDATE` [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the wrong result that might occur when performing `JOIN` with `ENUM` type columns [#27831](https://github.com/pingcap/tidb/issues/27831)
    - Fix a bug that `IndexHashJoin` might return the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)
    - Fix the issue that using the [`BatchCommands`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#max-batch-size) might block sending TiDB requests to TiKV in some rare cases [#27678](https://github.com/pingcap/tidb/pull/27678)
    (dup) - Fix the data inconsistency issue caused by incorrect usage of lazy existence check and untouched key optimization [#30410](https://github.com/pingcap/tidb/issues/30410)
    (dup) - Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    (dup) - Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    (dup) - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (set to `on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    (dup) - Fix the issue that the planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    (dup) - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    (dup) - Fix the TiDB panic when executing the `ALTER TABLE.. ADD INDEX` statement in some cases [#27687](https://github.com/pingcap/tidb/issues/27687)
    (dup) - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    (dup) - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    (dup) - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    (dup) - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)
    (dup) - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)

+ TiFlash

    - Fix `str_to_date()` function incorrectly handles leading zeros when parsing Microseconds
    - Fix the problem of TiFlash crashing when the memory limit is enabled
    - Align `unix_timestamp` behavior with TiDB and MySQL when input is earlier than 1970-01-01 00:00:01 UTC
    - Fix potential data inconsistency when widen pk column type if pk is handle
    - Fix the issue that comparison between Decimal may cause overflow and report `Can't compare`
    - Fix the issue of unexpected error that `3rd arguments of function substringUTF8 must be constants.`
    - Fix the issue that TiFlash fails to start up under platform without library `nsl`

+ TiKV

    - Fix the bug that unsafe_destroy_range does not get executed when GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix potential high latency caused by destroying a peer [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix wrong `any_value` result when there are regions returning empty result [#11735](https://github.com/tikv/tikv/issues/11735)
    - Fix the problem that destroying an uninitialized replica may cause a stalled replica be created again. [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix metadata corruption in an unlikely condition that prepare merge is triggered after new election without informing an isolated peer [#11526](https://github.com/tikv/tikv/issues/11526)
    - Fix deadlock in some rare cases that futures get resolved too fast [#11549](https://github.com/tikv/tikv/issues/11549)
    - Skip profiling sample in glibc, pthread, libgcc to avoid possible deadlock and memory leak in profiling [#11108](https://github.com/tikv/tikv/issues/11108)
    - Fix the bug that prewrite request retrying in pessimistic transactions have risk to affect data consistency in some rare cases. [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix resource-metering.enabled config does not work [#11235](https://github.com/tikv/tikv/issues/11235)
    - Fix coroutine leaking in the resolved_ts module.  [#10965](https://github.com/tikv/tikv/issues/10965)
    - Avoid false "GC can not work" alert under low write flow. [#9910](https://github.com/tikv/tikv/issues/9910)
    - Make tikv-ctl detect raft db correctly [#11393](https://github.com/tikv/tikv/issues/11393)

    (dup) - Fix the issue that a down TiKV node causes the resolved timestamp to lag [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    (dup) - Fix the issue that TiKV cannot detect the memory lock when TiKV perform a reverse table scan [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    (dup) - Increase the speed of inserting SST files by moving the verification process to the `Import` thread pool from the `Apply` thread pool [#11239](https://github.com/tikv/tikv/issues/11239)
    (dup) - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    (dup) - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    (dup) - Fix the issue that TiCDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    (dup) - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Collapse some uncommon storage-related metrics in Grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - Fix the bug that the region scatterer may generate the schedule with too few peers. [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix the bug that region statistics are not updated after `flow-round-by-digit` change. [#4295](https://github.com/tikv/pd/issues/4295)

    (dup) - Fix slow leader election caused by stucked region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    (dup) - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)
    (dup) - Fix the issue that the hotspot cache cannot be cleared when the Region heartbeat is less than 60 seconds [#4390](https://github.com/tikv/pd/issues/4390)
    (dup) - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    (dup) - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)

+ Tools

    + TiCDC

        - Fix a bug that MySQL sink generates duplicated `replace` SQL statements if `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix a bug that `kv client cached region metric` might be negative [#4300](https://github.com/pingcap/tiflow/issues/4300)
(dup) - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
(dup) - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
(dup) - Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
 (dup) - Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
 (dup) - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix a bug that EtcdWorker might hang the owner and processor [#3750](https://github.com/pingcap/tiflow/issues/3750)
        - Fix the issue of stopped changefeed resuming automatically after upgrading cluster [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - Fix a data type compatibility issue between TiCDC and TiDB amend mechanism [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix data inconsistency caused by TiCDC default value padding exceptions [#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - Fix a bug that owner get stuck when PD leader shutdowns and transfers to new node [#3615](https://github.com/pingcap/tiflow/issues/3615)
        - Fix kvclient takes too long time to recover when TiKV node shutdown  [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - Nond [#2983](https://github.com/pingcap/tiflow/issues/2983)

        (dup) - Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        (dup) - Fix the timezone error that occurs when the `cdc server` command runs on some Red Hat Enterprise Linux releases (such as 6.8 and 6.9) [#3584](https://github.com/pingcap/tiflow/issues/3584)
        (dup) - Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        (dup) - Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        (dup) - Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        (dup) - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)
        (dup) - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        (dup) - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        (dup) - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        (dup) - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        (dup) - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        (dup) - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)
        (dup) - Fix the issue that Kafka may send excessively large messages by setting the default value of `max-message-bytes` to `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)
        (dup) - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)

    + Backup & Restore (BR)

        - Fix the issue that Regions are unbalanced after restoring [#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)