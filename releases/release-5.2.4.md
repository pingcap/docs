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
    - (dup: release-5.1.4.md > Compatibility changes> TiDB)- Change the default value of the system variable [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510) from `2` to `1` [#31748](https://github.com/pingcap/tidb/issues/31748)
    - (dup: release-5.3.1.md > Compatibility changes> Tools> TiDB Lightning)- Change the default value of `regionMaxKeyCount` from 1_440_000 to 1_280_000, to avoid too many empty Regions after data import [#30018](https://github.com/pingcap/tidb/issues/30018)

+ Tools

    + Backup & Restore (BR)

        -
        -

## Improvements

+ TiDB

    -

+ TiKV

    - (dup: release-6.0.0-dmr.md > Improvements> TiKV)- Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)
    - (dup: release-6.0.0-dmr.md > Improvements> TiKV)- Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)

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

        - (dup: release-6.0.0-dmr.md > Improvements> Tools> TiCDC)- Add a `Lag analyze` panel in Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - (dup: release-6.0.0-dmr.md > Improvements> Tools> TiCDC)- Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)
        - (dup: release-6.0.0-dmr.md > Improvements> Tools> TiCDC)- Add the exponential backoff mechanism for restarting a changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - (dup: release-5.4.0.md > Improvements> Tools> TiCDC)- Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - (dup: release-5.3.1.md > Improvements> Tools> TiCDC)- Set the default value of `max-message-bytes` to 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)
        - (dup: release-5.3.1.md > Improvements> Tools> TiCDC)- Add more Promethous and Grafana monitoring metrics and alerts, including `no owner alert`, `mounter row`, `table sink total row`, and `buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)

    + Dumpling

        -

    + TiDB Lightning

        - note 1

    + TiDB Binlog

        - note 1

## Bug fixes

+ TiDB

    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix wrong range calculation results for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)
    - (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    - (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that a SQL operation is canceled when its JSON type column joins its `CHAR` type column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - executor: fix pipelined window invalid memory address [#30326](https://github.com/pingcap/tidb/issues/30326)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that window functions might return different results when using a transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that the `Column 'col_name' in field list is ambiguous` error is reported unexpectedly when a SQL statement contains natural join [#25041](https://github.com/pingcap/tidb/issues/25041)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that the length information is wrong when casting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (set to `on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiDB)- Fix a bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix the MPP task list empty error when executing a query [#31636](https://github.com/pingcap/tidb/issues/31636)
    - (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix wrong results of index join caused by an innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)
    - (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement gets panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix wrong query results due to the optimization of `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)
    - (dup: release-5.1.4.md > Bug fixes> TiDB)- Fix the wrong result that might occur when performing `JOIN` on `ENUM` type columns [#27831](https://github.com/pingcap/tidb/issues/27831)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)

+ TiKV

    -
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix the issue of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiKV)- Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the panic issue that occurs when the cgroup controller is not mounted [#11569](https://github.com/tikv/tikv/issues/11569)
    - (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#11526](https://github.com/tikv/tikv/issues/11526)
    - (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the issue that the latency of Resolved TS increases after TiKV stops operating [#11351](https://github.com/tikv/tikv/issues/11351)
    - (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix a bug that tikv-ctl cannot return the correct Region-related information [#11393](https://github.com/tikv/tikv/issues/11393)
    - (dup: release-5.0.6.md > Bug fixes> TiKV)- Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - (dup: release-5.4.0.md > Bug fixes> TiKV)- Fix the issue that retrying prewrite requests in the pessimistic transaction mode might cause the risk of data inconsistency in rare cases [#11187](https://github.com/tikv/tikv/issues/11187)
    - (dup: release-5.3.0.md > Bug Fixes> TiKV)- Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)

+ PD

    - (dup: release-6.0.0-dmr.md > Bug fixes> PD)- Fix the issue that the Region scatterer scheduling lost some peers [#4565](https://github.com/tikv/pd/issues/4565)
    - (dup: release-5.4.0.md > Bug fixes> PD)- Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

+ TiDB Dashboard

    -

+ TiFlash

    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue that casting `INI` to `DECIMAL` might cause overflow [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the issue that the date format identifies `'\n'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)

+ Tools

    + Backup & Restore (BR)

        -

    + TiCDC

        -
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiCDC)- Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiCDC)- Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiCDC)- Fix a bug that MySQL sink generates duplicated `replace` SQL statements when`batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of panic and data inconsistency that occurs when outputting the default column value [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the bug that HTTP API panics when the required processor infomation does not exist [#3840](https://github.com/pingcap/tiflow/issues/3840)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the potential issue that the deadlock causes a replication task to get stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the TiCDC panic issue that occurs when manually cleaning the task status in etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the issue that `stopped` changefeeds resume automatically after a cluster upgrade [#3473](https://github.com/pingcap/tiflow/issues/3473)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the issue of overly frequent warnings caused by MySQL sink deadlock [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the bug that the `enable-old-value` configuration item is not automatically set to `true` on Canal and Maxwell protocols [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the issue that Avro sink does not support parsing JSON type columns [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - (dup: release-5.4.0.md > Bug fixes> Tools> TiCDC)- Fix the OOM issue in the container environment [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - (dup: release-4.0.16.md > Bug fixes> Tools> TiCDC)- Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/tiflow/issues/3174)


    + Dumpling

        -

    + TiDB Lightning

        - (dup: release-5.4.0.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue of wrong import result that occurs when TiDB Lightning does not have the privilege to access the `mysql.tidb` table [#31088](https://github.com/pingcap/tidb/issues/31088)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Lightning)- Fix the checksum error “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        - (dup: release-6.0.0-dmr.md > Bug fixes> Tools> TiDB Lightning)- Fix a bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        - (dup: release-5.1.4.md > Bug fixes> Tools> TiDB Lightning)- Fix the issue that TiDB Lightning does not report errors when the S3 storage path does not exist [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)

    + TiDB Binlog

        -

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#33966](https://github.com/pingcap/tidb/issues/33966)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30571](https://github.com/pingcap/tidb/issues/30571)
    - Fix the bug that TiDB logs many `failed to check the user authplugin` when a user connects to TiDB. [#29709](https://github.com/pingcap/tidb/issues/29709)
    - Fix BR failure on backup rawkv. [#32607](https://github.com/pingcap/tidb/issues/32607)

+ TiKV/TiKV

    - fix tikv panic and peer unexpected destroy due to fake merge target [#12232](https://github.com/tikv/tikv/issues/12232)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12048](https://github.com/tikv/tikv/issues/12048)

+ PingCAP/TiFlash

    - Fix the potential crash issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - Fix the problem that empty segments cannot be merged after gc [#4511](https://github.com/pingcap/tiflash/issues/4511)
    - Fix wrong result of cast(float as decimal) when overflow happens [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - mpp task handle pingcap exception. [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3557](https://github.com/pingcap/tiflash/issues/3557)
    - (dup: release-6.0.0-dmr.md > Bug fixes> TiFlash)- Fix the TiFlash panic issue that occurs when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
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

+ Tools

    + PingCAP/TiCDC

        - Fix chengefeed getting stuck when tables are repeatedly scheduled in the same node [#4464](https://github.com/pingcap/tiflow/issues/4464)
        - `Fix a bug that openapi may be stuck when pd is abnormal` [#4778](https://github.com/pingcap/tiflow/issues/4778)
        - Fix stale metrics data when TiCDC owner switches. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - `None`. [#4858](https://github.com/pingcap/tiflow/issues/4858)
        - Fix stale metrics caused by owner changes. [#4774](https://github.com/pingcap/tiflow/issues/4774)
        - metrics: support multi-k8s in grafana dashboards [#4665](https://github.com/pingcap/tiflow/issues/4665)
        - Fix stability problem in workerpool, which is used by Unified Sorter. [#4447](https://github.com/pingcap/tiflow/issues/4447)
        - `None`. [#4675](https://github.com/pingcap/tiflow/issues/4675)
        - `None`. [#4607](https://github.com/pingcap/tiflow/issues/4607)
        - `None`. [#4588](https://github.com/pingcap/tiflow/issues/4588)
        - `None`. [#4561](https://github.com/pingcap/tiflow/issues/4561)
        - `None`. [#4128](https://github.com/pingcap/tiflow/issues/4128)
        - `None`. [#4135](https://github.com/pingcap/tiflow/issues/4135)
        - Fix kv client cached region metric could be negative. [#4295](https://github.com/pingcap/tiflow/pull/4295)
        - `None` [#4266](https://github.com/pingcap/tiflow/issues/4266)
        - `None`. [#4223](https://github.com/pingcap/tiflow/issues/4223)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3867](https://github.com/pingcap/tiflow/pull/3867)
        - Show changefeed checkepoint catch-up ETA in metrics. [#3311](https://github.com/pingcap/tiflow/pull/3311)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Please add a release note. fix kvclient takes too long time to recover [#3191](https://github.com/pingcap/tiflow/issues/3191)
        - `None`. [#4089](https://github.com/pingcap/tiflow/issues/4089)
