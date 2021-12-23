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

        - Output the cdc server cmd error from stdout to stderr. [#3875](https://github.com/pingcap/tiflow/pull/3875)

## Improvements

+ TiDB

    - Prevent conflicted optimistic transactions from locking each other [#29776](https://github.com/pingcap/tidb/pull/29776)
    - Avoid confusing error log like `invalid cop task execution summaries length` when running MPP query [#28262](https://github.com/pingcap/tidb/pull/28262)
    - The debug log on coprocessor doesn't print out the statement when encountering a lock, which makes it difficult to know what statement was affected by the lock. This fix tries to add the statement.[#27927](https://github.com/pingcap/tidb/pull/27927)

+ TiKV

    - Move verify_checksum to import-thread from apply-thread. [#11257](https://github.com/tikv/tikv/pull/11257)
    - Add metrics for raft log garbage-collect to locate performance problem. [#11381](https://github.com/tikv/tikv/pull/11381)
    - Hide untouched storage commands' metrics in grafana dashboard [#11001](https://github.com/tikv/tikv/pull/11001)

+ PD

    - Speed scheduler exit after transfer PD leader [#4201](https://github.com/tikv/pd/pull/4201)
    - Make scatter range scheduler work better by allowing empty region schedule and fix config [#4116](https://github.com/tikv/pd/pull/4116)

+ Tools

    + TiCDC
        - Optimize the rate limit control when TiKV reloads. [#3132](https://github.com/pingcap/tiflow/pull/3132)
        - Reduce lock competition in sink module. [#2760](https://github.com/pingcap/tiflow/pull/2760)
        - Extend creating service gc safepoint ttl to 1 hour to support creating changefeeds that needs long initialization time. [#2852](https://github.com/pingcap/tiflow/pull/2852)
        - Changefeed supports fast fail when occur ErrGCTTLExceeded error. [#3135](https://github.com/pingcap/tiflow/pull/3135)
        - Add rate limiter to limit EtcdWorker tick frequency. [#3268](https://github.com/pingcap/tiflow/pull/3268)
        - Support batch messages to reduce EtcdWorker tick. [#3391](https://github.com/pingcap/tiflow/pull/3391)
        - Support unified sorter cgroup aware. [#3441](https://github.com/pingcap/tiflow/pull/3441)
        - Add Kafka sink default configuration config.Metadata.Timeout. [#3670](https://github.com/pingcap/tiflow/pull/3670)
        - Change Kafka sink default `MaxMessageBytes` to 1MB. [#3107](https://github.com/pingcap/tiflow/pull/3107)
        - Add more monitor metric and alert, including "no owner alert" [#3834](https://github.com/pingcap/tiflow/pull/3834), "mounter row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "table sink total row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "buffer sink total row" [#2830](https://github.com/pingcap/tiflow/pull/2830), "go gc" [#2998](https://github.com/pingcap/tiflow/pull/2998), "go_max_procs" [#2998](https://github.com/pingcap/tiflow/pull/2998), "cached region" [#2733](https://github.com/pingcap/tiflow/pull/2733).

    + (Backup & Restore) BR

        - Retry pd request and TiKV IO timeout error [#1436](https://github.com/pingcap/br/pull/1436)

## Bug fixes

+ TiDB

    - Fix the problem that error is raised when a grant/revoke SQL contains global level identifier [#30161](https://github.com/pingcap/tidb/pull/30161)
    - Fix the problem that adding index panics by chance [#30125](https://github.com/pingcap/tidb/pull/30125)
    - Fix the problem that the `enforce-mpp` config item is useless in v5.0.4 [#29637](https://github.com/pingcap/tidb/pull/29637)
    - Fix the panic when the `case-when` function meets enum type input argument [#29509](https://github.com/pingcap/tidb/pull/29509)
    - Fix the problem that result of the `microsecond` function is wrong in vectorized evaluation [#29385](https://github.com/pingcap/tidb/pull/29385)
    - Fix the problem that the log lose the SQL text when auto analyze fails [#29228](https://github.com/pingcap/tidb/pull/29228)
    - Fix the problem that result of the `hour` function is wrong in vectorized evaluation [#28871](https://github.com/pingcap/tidb/pull/28871)
    - Fix the problem that unexpected error like `tidb_cast to Int32 is not supported` is raised when executing a MPP query [#28651](https://github.com/pingcap/tidb/pull/28651)
    - Fix the problem that MPP node availability detection does not work in some corner cases [#28287](https://github.com/pingcap/tidb/pull/28287)
    - Fix the problem that data-race may happen when alloc MPP task id [#28284](https://github.com/pingcap/tidb/pull/28284)
    - Fix the problem that `index out of range [-1]` error is raised when a SQL contains `Union` and is running in MPP mode [#28278](https://github.com/pingcap/tidb/pull/28278)
    - Fix the problem that TiDB panicks when inserting invalid date values concurrently [#28198](https://github.com/pingcap/tidb/pull/28198)
    - Fix the problem that the error like `can not found column in Schema column` is raised unexpectedly for mpp queries [#28147](https://github.com/pingcap/tidb/pull/28147)
    - Fix the problem that TiDB may crash when TiFlash shut down [#28138](https://github.com/pingcap/tidb/pull/28138)
    - Fix the problem that the `index out of range` error is raised unexpectly when the planner doing join reorder [#30881](https://github.com/pingcap/tidb/pull/30881).
    - Fix the problem that the results of `if`,`case-when`,`elt` functions are wrong when the input arguments if of type enum [#30857](https://github.com/pingcap/tidb/pull/30857)
    - Fix the problem the `concat(ifnull(time(3))` returns wrong result [#30830](https://github.com/pingcap/tidb/pull/30830)
    - Fix the problem that `greatest/least(unsigned)` returns wrong result [#30791](https://github.com/pingcap/tidb/pull/30791)
    - Fix the problem that SQL is cancelled when including json column joins char column [#30778](https://github.com/pingcap/tidb/pull/30778)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization [#30533](https://github.com/pingcap/tidb/pull/30533)
    - Fix the problem that window function may return different results when using transaction or not [#30389](https://github.com/pingcap/tidb/pull/30389)
    - Fix the problem that `cast(integer as char) union string` returns wrong result[#30055](https://github.com/pingcap/tidb/pull/30055)
    - Fix the problem that `concat(decimal_col)` returns wrong result [#30014](https://github.com/pingcap/tidb/pull/30014)
    - Fix the problem that the error `Column 'col_name' in field list is ambiguous` is raised unexpectedly when a SQL contains natural join [#30049](https://github.com/pingcap/tidb/pull/30049)
    - Fix the problem that `greatest` returns different results when `tidb_enable_vectorized_expression` is on or not [#29917](https://github.com/pingcap/tidb/pull/29917)
    - Fix the problem that planner may cache invalid plans for joins in some cases [#28445](https://github.com/pingcap/tidb/pull/28445)
    - Fix the problem that the error `index out of range [1] with length 1` is raised when a SQL tries to evaluates an aggregation result on the result of join in some cases [#28295](https://github.com/pingcap/tidb/pull/28295)

+ TiKV

    - Fix resolved timestamp lag increased after stoping a tikv [#11538](https://github.com/tikv/tikv/pull/11538)
    - Fix connection abort when too many small logs are batched into one messages [#11532](https://github.com/tikv/tikv/pull/11532)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11510](https://github.com/tikv/tikv/pull/11510)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11453](https://github.com/tikv/tikv/pull/11453)
    - Fix negative sign when decimal divide to zero [#11333](https://github.com/tikv/tikv/pull/11333)
    - Avoid possible OOM due to the accumulation of GC tasks [#11419](https://github.com/tikv/tikv/pull/11419)
    - Fix incorrect metrics  "gRPC average duration by-instance". [#11327](https://github.com/tikv/tikv/pull/11327)
    - Fix bug of reporting metrics about destroyed threads to Prometheus. [#11201](https://github.com/tikv/tikv/pull/11201)
    - Fix CDC panic due to missing downstream. [#11136](https://github.com/tikv/tikv/pull/11136)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11090](https://github.com/tikv/tikv/pull/11090)
    - Fix channel full could break the raft connection [#11070](https://github.com/tikv/tikv/pull/11070)
    - Fix panic caused by SST NotFound, which is ingested by  Lightning import. [#10740](https://github.com/tikv/tikv/pull/10740)
    - copr: fix Max/Min bug when comparing signed and unsigned int64 [#10617](https://github.com/tikv/tikv/pull/10617)
    - Fix follower meta corruption in rare cases with more than 4 replicas [#10500](https://github.com/tikv/tikv/pull/10500)
    - Fix backup threads leak [#10361](https://github.com/tikv/tikv/pull/10361)
    - copr cast invalid utf8 string to real bug fix [#9871](https://github.com/tikv/tikv/pull/9871)

+ PD

    - Fix panic issue after TiKV node scales in with some corner cases [#4379](https://github.com/tikv/pd/pull/4379)
    - Fix the issue that operator can get blocked due to down store [#4367](https://github.com/tikv/pd/pull/4367)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4218](https://github.com/tikv/pd/pull/4218)
    - Fix the issue that `evict-leader-scheduler` cannot schedule the regions with unhealthy peers. [#4130](https://github.com/tikv/pd/pull/4130)
    - Fix the issue that there is the store limit of remove peer of the down store [#4097](https://github.com/tikv/pd/pull/4097)
    - Fix the issue that the hot cache cannot be cleared when the heartbeat interval is less than 60 [#4432](https://github.com/tikv/pd/pull/4432)

+ TiFlash

    - Fix potential data inconsistency when widen pk column type if pk is handle [#3572](https://github.com/pingcap/tics/pull/3572)
    - Fix Tiflash arm build when include `libnsl.so`. Try copy `libnsl.so` to `INSTALL_DIR` [#3205](https://github.com/pingcap/tics/pull/3205)
    - Fix store size on `tiflash metrics` is not consistent.Decrease the size of checkpoint file when removing it  [#3187](https://github.com/pingcap/tics/pull/3187)
    - Fix exception: `GC` removed normal file which just created [#3226](https://github.com/pingcap/tics/pull/3226)
    - Fix sync schema exception when user upgrade the TiFlash version. [#2701](https://github.com/pingcap/tics/pull/2701)
    - Fix tiflash randomly crash when a mpp query is killed. [#3448](https://github.com/pingcap/tics/pull/3448)
    - Fix throw not constants exception in `substringUTF8` [#3266](https://github.com/pingcap/tics/pull/3266)
    - Fix decode DAG request failed.Add retry when decode DAG request failed. [#3678](https://github.com/pingcap/tics/pull/3678)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3477](https://github.com/pingcap/tics/pull/3477)
    - Fix `main_capacity_quota_` check  [#3425](https://github.com/pingcap/tics/pull/3425)
    - Fix the inconsistent behavior of `CastStringAsDecimal` between tiflash and tidb/tikv. [#3674](https://github.com/pingcap/tics/pull/3674)
    - Fix exception: `expected Nullable(Int64), got Int64`. Sending schemas in exchangeSender to avoid schema mismatch. [#3369](https://github.com/pingcap/tics/pull/3369)
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)` [#3376](https://github.com/pingcap/tics/pull/3376)
    - Fix the issue that comparison between Decimal may cause overflow and report Can't compare. [#3097](https://github.com/pingcap/tics/pull/3097)

+ Tools

    + TiCDC

        - Fix table is not replicated when adding partition about partition table without valid index. [#2864](https://github.com/pingcap/tiflow/pull/2864)
        - Fix cdc cli silently truncated user parameters when receiving unexpected parameters, causing the user input parameters to be lost. [#2888](https://github.com/pingcap/tiflow/pull/2888)
        - Fix cdc scheduling tables too early. [#2633](https://github.com/pingcap/tiflow/pull/2633)
        - Fix Kafka_producer deadlock when an error occurs in asyncClient. [#3016](https://github.com/pingcap/tiflow/pull/3016)
        - Fix MQ sink don't support non binary json string encoding. [#2782](https://github.com/pingcap/tiflow/pull/2782)
        - Fix Kafka sink can not send message due to constraint by `max-message-size` option. [#3047](https://github.com/pingcap/tiflow/pull/3047)
        - Fix  fallback resolvedTs event  block the progress of resolve lock when meet region merging. [#3100](https://github.com/pingcap/tiflow/pull/3100)
        - Fix unexpected duplicate region request stream issue. [#3091](https://github.com/pingcap/tiflow/pull/3091)
        - Fix changefeed region loss when multiple TiKVs crash or forcing restart. [#3291](https://github.com/pingcap/tiflow/pull/3291)
        - Fix changefeed checkpoint lag metric negative value error. [#3533](https://github.com/pingcap/tiflow/pull/3533)
        - Fix MySQL sink deadlock warning too frequently. [#3797](https://github.com/pingcap/tiflow/pull/3797)
        - Fix Avro sink don't support json type column. [#3651](https://github.com/pingcap/tiflow/pull/3651)
        - Fix read error schema snapshot from TiKV when owner restart. [#2610](https://github.com/pingcap/tiflow/pull/2610)
        - Fix schema GC not work correctly and OOM issue when processing too many DDL. [#3275](https://github.com/pingcap/tiflow/pull/3275)
        - Fix old value enabled is not forced on Canal and Maxwell protocols automatically. [#3780](https://github.com/pingcap/tiflow/pull/3780)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc).  [#3908](https://github.com/pingcap/tiflow/pull/3908)
        - Fix txn_batch_size metric inaccurate issue for Kafka sink. [#3820](https://github.com/pingcap/tiflow/pull/3820)
        - Fix Kafka partition count not check when auto-create-topic is disabled by the user. [#3566](https://github.com/pingcap/tiflow/pull/3566)
        - Fix Kafka message too large for broker. [#3566](https://github.com/pingcap/tiflow/pull/3566)
        - Fix EtcdWorker row metric error. [#4000](https://github.com/pingcap/tiflow/pull/4000)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed. [#3024](https://github.com/pingcap/tiflow/pull/3024)
        - Fix the congestion in gPRC, which may cause slow initialization phase. [#3132](https://github.com/pingcap/tiflow/pull/3132)

    + (Backup & Restore) BR

        - Fix failed to retry grpc errors. [#1438](https://github.com/pingcap/br/pull/1438)
        - Fix failed after importing table with expression index using local backend. [#1419](https://github.com/pingcap/br/pull/1419)
        - Fix the average speed isn't accurate in backup and restore [#1411](https://github.com/pingcap/br/pull/1411)

    + Dumpling

        - Fix the bug that dumpling gets very slow when dumping composite primary/unique key tables. [#399](https://github.com/pingcap/dumpling/pull/399)