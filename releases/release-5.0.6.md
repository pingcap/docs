---
title: TiDB 5.0.6 Release Notes
category: Releases
---

# TiDB 5.0.6 Release Notes

Release date: December 28, 2021

TiDB version: 5.0.6

## Compatibility changes

+ Tools

    + TiCDC

        - Output the cdc server cmd error from stdout to stderr. [#3133](https://github.com/pingcap/tiflow/issues/3133)

## Improvements

+ TiDB

    (dup) - Fix the issue that optimistic transaction conflicts might cause transactions to block each other [#11148](https://github.com/tikv/tikv/issues/11148)
    (dup) - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    (dup) - Show the affected SQL statements in the debug log when the coprocessor encounters a lock, which is helpful in diagnosing problems [#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - Move verify_checksum to import-thread from apply-thread. [#11239](https://github.com/tikv/tikv/issues/11239)
    - Add metrics for raft log garbage-collect to locate performance problem. [#11374](https://github.com/tikv/tikv/issues/11374)
    - Hide untouched storage commands' metrics in grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    (dup) - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)
    - Make scatter range scheduler work better by allowing empty region schedule and fix config [#4116](https://github.com/tikv/pd/pull/4116)

+ Tools

    + TiCDC
        (dup) - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)
        - Reduce lock competition in sink module. [#2760](https://github.com/pingcap/tiflow/pull/2760)
        (dup) - Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/tiflow/issues/2470)
        (dup) - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        (dup) - Add a tick frequency limit to EtcdWorker to prevent frequent etcd writes from affecting PD services [#3112](https://github.com/pingcap/ticdc/issues/3112)
        - Support batch messages to reduce EtcdWorker tick. [3112](https://github.com/pingcap/tiflow/issues/3112)
        (dup) - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)
        - Add Kafka sink default configuration config.Metadata.Timeout. [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Change Kafka sink default `MaxMessageBytes` to 1MB. [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Add more monitor metric and alert, including "no owner alert" [#3834](https://github.com/pingcap/tiflow/pull/3834), "mounter row" , "table sink total row" , "buffer sink total row" [#1606](https://github.com/pingcap/tiflow/issues/1606), "go gc" , "go_max_procs" [#2998](https://github.com/pingcap/tiflow/pull/2998), "cached region" [#2733](https://github.com/pingcap/tiflow/pull/2733).

    + (Backup & Restore) BR

        - Retry pd request and TiKV IO timeout error [#27787](https://github.com/pingcap/tidb/issues/27787)

## Bug fixes

+ TiDB

    (dup) - Fix the `privilege check fail` error when performing the `grant` and `revoke` operations to grant and revoke global level privileges [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix the problem that adding index panics by chance [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix the problem that the `enforce-mpp` config item is useless in v5.0.4 [#29252](https://github.com/pingcap/tidb/issues/29252)
    (dup) - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    (dup) - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    (dup) - Fix the issue of incomplete log information from the `auto analyze` result [#29188](https://github.com/pingcap/tidb/issues/29188)
    (dup) - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    (dup) - Fix  the unexpected error like `tidb_cast to Int32 is not supported` when the unsupported `cast` is pushed down to TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)
    (dup) - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    (dup) - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    (dup) - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the problem that TiDB panicks when inserting invalid date values concurrently [#25393](https://github.com/pingcap/tidb/issues/25393)
    - Fix the problem that the error like `can not found column in Schema column` is raised unexpectedly for mpp queries [#28147](https://github.com/pingcap/tidb/pull/28147)
    (dup) - Fix the issue that TiDB might panic when TiFlash is shuting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Fix the problem that the `index out of range` error is raised unexpectly when the planner doing join reorder [#24095](https://github.com/pingcap/tidb/issues/24095).
    (dup) - Fix wrong results of the control functions (such as `IF` and `CASE WHEN`) when using the `ENUM` type data as parameters of such functions [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix the problem the `concat(ifnull(time(3))` returns wrong result [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the problem that `greatest/least(unsigned)` returns wrong result [#30101](https://github.com/pingcap/tidb/issues/30101)
    - Fix the problem that SQL is cancelled when including json column joins char column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the problem that window function may return different results when using transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix the problem that `cast(integer as char) union string` returns wrong result[#29513](https://github.com/pingcap/tidb/issues/29513)
    (dup) - Fix the issue that the length information is wrong when converting `Decimal` to `String` [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the problem that the error `Column 'col_name' in field list is ambiguous` is raised unexpectedly when a SQL contains natural join [#25041](https://github.com/pingcap/tidb/issues/25041)
    (dup) - Fix the issue that the `GREATEST` function returns inconsistent results due to different values of `tidb_enable_vectorized_expression` (`on` or `off`) [#29434](https://github.com/pingcap/tidb/issues/29434)
    (dup) - Fix the issue that planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix the problem that the error `index out of range [1] with length 1` is raised when a SQL tries to evaluates an aggregation result on the result of join in some cases [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - Fix resolved timestamp lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    (dup) - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix a panic issue that occurs when Region merge, ConfChange, and Snapshot happen at the same time in extreme conditions [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    (dup) - Fix the issue of negative sign when the decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Avoid possible OOM due to the accumulation of GC tasks [#11410](https://github.com/tikv/tikv/issues/11410)
    (dup) - Fix the issue that the average latency of the by-instance gRPC requests is inaccurate in TiKV metrics [#11299](https://github.com/tikv/tikv/issues/11299)
    (dup) - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    (dup) - Fix the issue of TiCDC panic that occurs when the downstream database is missing [#11123](https://github.com/tikv/tikv/issues/11123)
    (dup) - Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    (dup) - Fix the issue that the Raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix panic caused by SST NotFound, which is ingested by  Lightning import. [#10438](https://github.com/tikv/tikv/issues/10438)
    (dup) - Fix the issue that TiDB cannot correctly identify whether the `Int64` types in `Max`/`Min` functions are a signed integer or not, which causes the wrong calculation result of `Max`/`Min` [#10158](https://github.com/tikv/tikv/issues/10158)
    - Fix follower meta corruption in rare cases with more than 4 replicas [#10225](https://github.com/tikv/tikv/issues/10225)
    - Fix backup threads leak [#10287](https://github.com/tikv/tikv/issues/10287)
    - copr cast invalid utf8 string to real bug fix [#23322](https://github.com/pingcap/tidb/issues/23322)

+ PD

    (dup) - Fix a panic issue that occurs after the TiKV node is removed [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)
    (dup) - Fix slow leader election caused by stucked Region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    (dup) - Support that the evict leader scheduler can schedule Regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)
    - Fix the issue that there is the store limit of remove peer of the down store [#4090](https://github.com/tikv/pd/issues/4090)
    - Fix the issue that the hot cache cannot be cleared when the heartbeat interval is less than 60 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix potential data inconsistency after widening the integer primary key of a table
    - Fix Tiflash arm build when include `libnsl.so`. Try copy `libnsl.so` to `INSTALL_DIR`
    - Fix store size on `tiflash metrics` is not consistent.Decrease the size of checkpoint file when removing it
    - Fix exception: `GC` removed normal file which just created
    - Fix sync schema exception when user upgrade the TiFlash version
    - Fix tiflash randomly crash when a mpp query is killed
    - Fix the issue of unexpected error that "3rd arguments of function substringUTF8 must be constants"
    - Fix decode DAG request failed.Add retry when decode DAG request failed
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type
    - Fix `main_capacity_quota_` check
    - Fix the inconsistent behavior of `CastStringAsDecimal` between tiflash and tidb/tikv
    - Fix the error "different types: expected Nullable(Int64), got Int64" which causes query failure
    - Fix the error "Unexpected type of column: Nullable(Nothing)" which cases query failure
    - Fix the issue that comparison between Decimal may cause overflow and report Can't compare

+ Tools

    + TiCDC

        (dup) - Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - Fix cdc cli silently truncated user parameters when receiving unexpected parameters, causing the user input parameters to be lost. [#2303](https://github.com/pingcap/tiflow/issues/2303)
        - Fix cdc scheduling tables too early. [#2625](https://github.com/pingcap/tiflow/issues/2625)
        (dup) - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/tiflow/issues/2978)
        (dup) - Fix a possible panic issue when encoding some types of columns into Open Protocol format [#2758](https://github.com/pingcap/tiflow/issues/2758)
        (dup) - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)
        (dup) - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/tiflow/issues/3061)
        (dup) - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/tiflow/issues/2386)
        (dup) - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        (dup) - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix MySQL sink deadlock warning too frequently. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix Avro sink don't support json type column. [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix read error schema snapshot from TiKV when owner restart. [#2603](https://github.com/pingcap/tiflow/issues/2603)
        (dup) - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - Fix old value enabled is not forced on Canal and Maxwell protocols automatically. [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix txn_batch_size metric inaccurate issue for Kafka sink. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        (dup) - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/ticdc/issues/3337)
        (dup) - Change the default value of Kafka Sink `partition-num` to 3 so that TiCDC distributes messages across Kafka partitions more evenly [#3337](https://github.com/pingcap/ticdc/issues/3337)
        - Fix EtcdWorker row metric error. [#4000](https://github.com/pingcap/tiflow/pull/4000)
        (dup) - Fix the issue that `tikv_cdc_min_resolved_ts_no_change_for_1m` keeps alerting when there is no changefeed [#11017](https://github.com/tikv/tikv/issues/11017)
        (dup) - Optimize rate limiting control on TiKV reloads to reduce gPRC congestion during changefeed initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)

    + (Backup & Restore) BR

        (dup) - Improve the robustness of restoring [#27421](https://github.com/pingcap/tidb/issues/27421)
        - Fix failed after importing table with expression index using local backend. [#1404](https://github.com/pingcap/br/issues/1404)
        - Fix the average speed isn't accurate in backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - Fix the bug that dumpling gets very slow when dumping composite primary/unique key tables. [#29386](https://github.com/pingcap/tidb/issues/29386)