---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release Date: December 10, 2021

TiDB version: 4.0.16

## Compatibility changes

+ TiKV

    - When casting invalid utf8 string to real, try to truncate the utf8 prefix instead of returning error. [#9870](https://github.com/tikv/tikv/pull/9870)
    - [cdc: reduce events batch to solve congest error (#11086) by ti-srebot · Pull Request #11089 · tikv/tikv](https://github.com/tikv/tikv/pull/11089)

+ Tools

    + TiDB Binlog

        - [drainer: fix kafka message limit problem (#1039) by ti-chi-bot · Pull Request #1078 · pingcap/tidb-binlog](https://github.com/pingcap/tidb-binlog/pull/1078)

## Improvements

+ TiKV

    - sst_importer: Reduce the space usage when using BR-Restore or Lightning-Local-backend by using zstd compression in SSTs. [#10642](https://github.com/tikv/tikv/pull/10642)

+ Tools

    + Backup & Restore (BR)

        - Increase the robustness for restoring. [#1445](https://github.com/pingcap/br/pull/1445)

    + TiCDC

        - Add rate limiter to limit EtcdWorker tick frequency. [#3267](https://github.com/pingcap/ticdc/pull/3267)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3131](https://github.com/pingcap/ticdc/pull/3131)
        - Change Kafka sink default `MaxMessageBytes` to 1MB. [#3106](https://github.com/pingcap/ticdc/pull/3106)
        - Ignore the global flag for changefeed update command. [#2875](https://github.com/pingcap/ticdc/pull/2875)
        - Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time. [#2851](https://github.com/pingcap/ticdc/pull/2851)
        - Prohibit operating TiCDC clusters across major and minor versions. [#2601](https://github.com/pingcap/ticdc/pull/2601)

## Bug fixes

+ TiDB

    - Fix a query panic caused by overflow in statistics module when calculating selectivity and converting a range to points for cost estimation [#30017](https://github.com/pingcap/tidb/pull/30017)
    - Fix wrong result for control function (`if`, `case when`, etc) with enum type. [#30011](https://github.com/pingcap/tidb/pull/30011)
    - Fix different results for function `greatest` when vectorized is off. [#29916](https://github.com/pingcap/tidb/pull/29916)
    - Fix index join panic on prefix index on some cases [#29217](https://github.com/pingcap/tidb/pull/29217)
    - Fix a bug that planner may cache invalid plans for joins in some cases [#28444](https://github.com/pingcap/tidb/pull/28444)
    - Fix a bug that TiDB can not insert null into a not null column when `sql_mode` is empty [#27832](https://github.com/pingcap/tidb/pull/27832)
    - Fix wrong result type for function `greatest`/`least` [#29911](https://github.com/pingcap/tidb/pull/29911)
    - Fix privilege checking for `grant` and `revoke` operation on global level privileges [#29899](https://github.com/pingcap/tidb/pull/29899)
    - Fix panic for `case when` function with enum type [#29508](https://github.com/pingcap/tidb/pull/29508)
    - Fix wrong result of `microsecond` function in vectorized expression [#29384](https://github.com/pingcap/tidb/pull/29384)
    - Fix wrong result of `hour` function in vectorized expression [#28870](https://github.com/pingcap/tidb/pull/28870)
    - Prevent conflicted optimistic transactions from locking each other. [#29775](https://github.com/pingcap/tidb/pull/29775)
    - Fix incomplete log information about auto analyze. [#29227](https://github.com/pingcap/tidb/pull/29227)
    - Fix an issue that `NO_ZERO_IN_DATE` does not work on the default values. [#26902](https://github.com/pingcap/tidb/pull/26902)
    - Fix copt-cache metrics, it will display the number of hits/miss/evict on Grafana now. [#26342](https://github.com/pingcap/tidb/pull/26342)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26237](https://github.com/pingcap/tidb/pull/26237)

+ TiKV

    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11509](https://github.com/tikv/tikv/pull/11509)
    - Make negative sign as false when decimal divide result is zero [#11332](https://github.com/tikv/tikv/pull/11332)
    - Fix incorrect by-instance gRPC average duration. [#11326](https://github.com/tikv/tikv/pull/11326)
    - Fix CDC panic due to missing downstream. [#11135](https://github.com/tikv/tikv/pull/11135)
    - Fix channel full could break the raft connection [#11069](https://github.com/tikv/tikv/pull/11069)
    - Fix Max/Min bug when comparing signed and unsigned int64 [#10616](https://github.com/tikv/tikv/pull/10616)
    -  Fix frequent CDC incremental scan retry due to `Congest` error. [#11089](https://github.com/tikv/tikv/pull/11089)

+ PD

    - Fix panic issue after TiKV node scales in [#4378](https://github.com/tikv/pd/pull/4378)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4219](https://github.com/tikv/pd/pull/4219)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4133](https://github.com/tikv/pd/pull/4133)

+ TiFlash

    - Fix the issue that comparison between Decimal may cause overflow and report `Can't compare`. [#3365](https://github.com/pingcap/tics/pull/3365)
    - Fix the issue that TiFlash fails to start up under platform without library `nsl` [#3209](https://github.com/pingcap/tics/pull/3209)

+ Tools

    + TiCDC

        - Fix changefeed checkpoint lag negative value error. [#3532](https://github.com/pingcap/ticdc/pull/3532)
        - Fix OOM in container environments. [#3440](https://github.com/pingcap/ticdc/pull/3440)
        - Fix TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3290](https://github.com/pingcap/ticdc/pull/3290)
        - Fix memory leak after processing DDLs. [#3274](https://github.com/pingcap/ticdc/pull/3274)
        - Fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3134](https://github.com/pingcap/ticdc/pull/3134)
        - Fix fallback resolvedTs event will block the progress of resolve lock when occur region merging. [#3099](https://github.com/pingcap/ticdc/pull/3099)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#3094](https://github.com/pingcap/ticdc/pull/3094)
        - Fix kafka sink can not send message due to constraint by `max-message-size` option. [#3046](https://github.com/pingcap/ticdc/pull/3046)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed. [#3023](https://github.com/pingcap/ticdc/pull/3023)
        - Fix possible deadlocking when Kafka producer reports an error. [#3015](https://github.com/pingcap/ticdc/pull/3015)
        - Fix dml is not replicated after adding partition in partition table without valid index. [#2863](https://github.com/pingcap/ticdc/pull/2863)
        - Fix memory leak which may happen in create new changefeed. [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - Set config.Metadata.Timeout correctly to prevent stuck data synchronization. [#3669](https://github.com/pingcap/ticdc/pull/3669)
