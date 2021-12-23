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

    - Prevent conflicted optimistic transactions from locking each other [#11148](https://github.com/tikv/tikv/issues/11148)
    - Avoid confusing error log like `invalid cop task execution summaries length` when running MPP query [#1791](https://github.com/pingcap/tics/issues/1791)
    - The debug log on coprocessor doesn't print out the statement when encountering a lock, which makes it difficult to know what statement was affected by the lock. This fix tries to add the statement.[#27718](https://github.com/pingcap/tidb/issues/27718)

+ TiKV

    - Move verify_checksum to import-thread from apply-thread. [#11239](https://github.com/tikv/tikv/issues/11239)
    - Add metrics for raft log garbage-collect to locate performance problem. [#11374](https://github.com/tikv/tikv/issues/11374)
    - Hide untouched storage commands' metrics in grafana dashboard [#11681](https://github.com/tikv/tikv/issues/11681)

+ PD

    - Speed scheduler exit after transfer PD leader [#4146](https://github.com/tikv/pd/issues/4146)
    - Make scatter range scheduler work better by allowing empty region schedule and fix config [#4116](https://github.com/tikv/pd/pull/4116)

+ Tools

    + TiCDC
        - Optimize the rate limit control when TiKV reloads. [#3110](https://github.com/pingcap/tiflow/issues/3110)
        - Reduce lock competition in sink module. [#2760](https://github.com/pingcap/tiflow/pull/2760)
        - Extend creating service gc safepoint ttl to 1 hour to support creating changefeeds that needs long initialization time. [#2470](https://github.com/pingcap/tiflow/issues/2470)
        - Changefeed supports fast fail when occur ErrGCTTLExceeded error. [#3111](https://github.com/pingcap/tiflow/issues/3111)
        - Add rate limiter to limit EtcdWorker tick frequency. [#3112](https://github.com/pingcap/tiflow/issues/3112)
        - Support batch messages to reduce EtcdWorker tick. [3112](https://github.com/pingcap/tiflow/issues/3112)
        - Support unified sorter cgroup aware. [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Add Kafka sink default configuration config.Metadata.Timeout. [#3352](https://github.com/pingcap/tiflow/issues/3352)
        - Change Kafka sink default `MaxMessageBytes` to 1MB. [#3081](https://github.com/pingcap/tiflow/issues/3081)
        - Add more monitor metric and alert, including "no owner alert" [#3834](https://github.com/pingcap/tiflow/pull/3834), "mounter row" , "table sink total row" , "buffer sink total row" [#1606](https://github.com/pingcap/tiflow/issues/1606), "go gc" , "go_max_procs" [#2998](https://github.com/pingcap/tiflow/pull/2998), "cached region" [#2733](https://github.com/pingcap/tiflow/pull/2733).

    + (Backup & Restore) BR

        - Retry pd request and TiKV IO timeout error [#27787](https://github.com/pingcap/tidb/issues/27787)

## Bug fixes

+ TiDB

    - Fix the problem that error is raised when a grant/revoke SQL contains global level identifier [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix the problem that adding index panics by chance [#27687](https://github.com/pingcap/tidb/issues/27687)
    - Fix the problem that the `enforce-mpp` config item is useless in v5.0.4 [#29252](https://github.com/pingcap/tidb/issues/29252)
    - Fix the panic when the `case-when` function meets enum type input argument [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix the problem that result of the `microsecond` function is wrong in vectorized evaluation [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Fix the problem that the log lose the SQL text when auto analyze fails [#29188](https://github.com/pingcap/tidb/issues/29188)
    - Fix the problem that result of the `hour` function is wrong in vectorized evaluation [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the problem that unexpected error like `tidb_cast to Int32 is not supported` is raised when executing a MPP query [#23907](https://github.com/pingcap/tidb/issues/23907)
    - Fix the problem that MPP node availability detection does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix the problem that data-race may happen when alloc MPP task id [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix the problem that `index out of range [-1]` error is raised when a SQL contains `Union` and is running in MPP mode [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the problem that TiDB panicks when inserting invalid date values concurrently [#25393](https://github.com/pingcap/tidb/issues/25393)
    - Fix the problem that the error like `can not found column in Schema column` is raised unexpectedly for mpp queries [#28147](https://github.com/pingcap/tidb/pull/28147)
    - Fix the problem that TiDB may crash when TiFlash shut down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Fix the problem that the `index out of range` error is raised unexpectly when the planner doing join reorder [#24095](https://github.com/pingcap/tidb/issues/24095).
    - Fix the problem that the results of `if`,`case-when`,`elt` functions are wrong when the input arguments if of type enum [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix the problem the `concat(ifnull(time(3))` returns wrong result [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the problem that `greatest/least(unsigned)` returns wrong result [#30101](https://github.com/pingcap/tidb/issues/30101)
    - Fix the problem that SQL is cancelled when including json column joins char column [#29401](https://github.com/pingcap/tidb/issues/29401)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the problem that window function may return different results when using transaction or not [#29947](https://github.com/pingcap/tidb/issues/29947)
    - Fix the problem that `cast(integer as char) union string` returns wrong result[#29513](https://github.com/pingcap/tidb/issues/29513)
    - Fix the problem that `concat(decimal_col)` returns wrong result [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the problem that the error `Column 'col_name' in field list is ambiguous` is raised unexpectedly when a SQL contains natural join [#25041](https://github.com/pingcap/tidb/issues/25041)
    - Fix the problem that `greatest` returns different results when `tidb_enable_vectorized_expression` is on or not [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix the problem that planner may cache invalid plans for joins in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix the problem that the error `index out of range [1] with length 1` is raised when a SQL tries to evaluates an aggregation result on the result of join in some cases [#1978](https://github.com/pingcap/tics/issues/1978)

+ TiKV

    - Fix resolved timestamp lag increased after stoping a tikv [#11351](https://github.com/tikv/tikv/issues/11351)
    - Fix connection abort when too many small logs are batched into one messages [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11440](https://github.com/tikv/tikv/issues/11440)
    - Fix negative sign when decimal divide to zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Avoid possible OOM due to the accumulation of GC tasks [#11410](https://github.com/tikv/tikv/issues/11410)
    - Fix incorrect metrics  "gRPC average duration by-instance". [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix bug of reporting metrics about destroyed threads to Prometheus. [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix CDC panic due to missing downstream. [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix channel full could break the raft connection [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix panic caused by SST NotFound, which is ingested by  Lightning import. [#10438](https://github.com/tikv/tikv/issues/10438)
    - copr: fix Max/Min bug when comparing signed and unsigned int64 [#10158](https://github.com/tikv/tikv/issues/10158)
    - Fix follower meta corruption in rare cases with more than 4 replicas [#10225](https://github.com/tikv/tikv/issues/10225)
    - Fix backup threads leak [#10287](https://github.com/tikv/tikv/issues/10287)
    - copr cast invalid utf8 string to real bug fix [#23322](https://github.com/pingcap/tidb/issues/23322)

+ PD

    - Fix panic issue after TiKV node scales in with some corner cases [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that operator can get blocked due to down store [#3353](https://github.com/tikv/pd/issues/3353)
    - Fix the issue that PD may not elect leader as soon as leader step down [#3936](https://github.com/tikv/pd/issues/3936)
    - Fix the issue that `evict-leader-scheduler` cannot schedule the regions with unhealthy peers. [#4093](https://github.com/tikv/pd/issues/4093)
    - Fix the issue that there is the store limit of remove peer of the down store [#4090](https://github.com/tikv/pd/issues/4090)
    - Fix the issue that the hot cache cannot be cleared when the heartbeat interval is less than 60 [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix potential data inconsistency when widen pk column type if pk is handle
    - Fix Tiflash arm build when include `libnsl.so`. Try copy `libnsl.so` to `INSTALL_DIR`
    - Fix store size on `tiflash metrics` is not consistent.Decrease the size of checkpoint file when removing it
    - Fix exception: `GC` removed normal file which just created
    - Fix sync schema exception when user upgrade the TiFlash version
    - Fix tiflash randomly crash when a mpp query is killed
    - Fix throw not constants exception in `substringUTF8`
    - Fix decode DAG request failed.Add retry when decode DAG request failed
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type
    - Fix `main_capacity_quota_` check
    - Fix the inconsistent behavior of `CastStringAsDecimal` between tiflash and tidb/tikv
    - Fix exception: `expected Nullable(Int64), got Int64`. Sending schemas in exchangeSender to avoid schema mismatch
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)`
    - Fix the issue that comparison between Decimal may cause overflow and report Can't compare

+ Tools

    + TiCDC

        - Fix table is not replicated when adding partition about partition table without valid index. [#2834](https://github.com/pingcap/tiflow/issues/2834)
        - Fix cdc cli silently truncated user parameters when receiving unexpected parameters, causing the user input parameters to be lost. [#2303](https://github.com/pingcap/tiflow/issues/2303)
        - Fix cdc scheduling tables too early. [#2625](https://github.com/pingcap/tiflow/issues/2625)
        - Fix Kafka_producer deadlock when an error occurs in asyncClient. [#2978](https://github.com/pingcap/tiflow/issues/2978)
        - Fix MQ sink don't support non binary json string encoding. [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - Fix Kafka sink can not send message due to constraint by `max-message-size` option. [#2962](https://github.com/pingcap/tiflow/issues/2962)
        - Fix  fallback resolvedTs event  block the progress of resolve lock when meet region merging. [#3061](https://github.com/pingcap/tiflow/issues/3061)
        - Fix unexpected duplicate region request stream issue. [#2386](https://github.com/pingcap/tiflow/issues/2386)
        - Fix changefeed region loss when multiple TiKVs crash or forcing restart. [#3288](https://github.com/pingcap/tiflow/issues/3288)
        - Fix changefeed checkpoint lag metric negative value error. [#3010](https://github.com/pingcap/tiflow/issues/3010)
        - Fix MySQL sink deadlock warning too frequently. [#2706](https://github.com/pingcap/tiflow/issues/2706)
        - Fix Avro sink don't support json type column. [#3624](https://github.com/pingcap/tiflow/issues/3624)
        - Fix read error schema snapshot from TiKV when owner restart. [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - Fix schema GC not work correctly and OOM issue when processing too many DDL. [#3174](https://github.com/pingcap/tiflow/issues/3174)
        - Fix old value enabled is not forced on Canal and Maxwell protocols automatically. [#3676](https://github.com/pingcap/tiflow/issues/3676)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc).  [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix txn_batch_size metric inaccurate issue for Kafka sink. [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix Kafka partition count not check when auto-create-topic is disabled by the user. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Fix Kafka message too large for broker. [#3337](https://github.com/pingcap/tiflow/issues/3337)
        - Fix EtcdWorker row metric error. [#4000](https://github.com/pingcap/tiflow/pull/4000)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed. [#11017](https://github.com/tikv/tikv/issues/11017)
        - Fix the congestion in gPRC, which may cause slow initialization phase. [#3110](https://github.com/pingcap/tiflow/issues/3110)

    + (Backup & Restore) BR

        - Fix failed to retry grpc errors. [#27421](https://github.com/pingcap/tidb/issues/27421)
        - Fix failed after importing table with expression index using local backend. [#1404](https://github.com/pingcap/br/issues/1404)
        - Fix the average speed isn't accurate in backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - Fix the bug that dumpling gets very slow when dumping composite primary/unique key tables. [#29386](https://github.com/pingcap/tidb/issues/29386)