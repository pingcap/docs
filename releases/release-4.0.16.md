---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release Date: December 10, 2021

TiDB version: 4.0.16

## Compatibility changes

+ TiKV

    - When casting invalid utf8 string to real, try to truncate the utf8 prefix instead of returning error [#11466](https://github.com/tikv/tikv/issues/11466)
    - cdc: reduce events batch to solve congest error [#11082](https://github.com/tikv/tikv/issues/11082)

+ Tools

    + TiDB Binlog

        - drainer: fix kafka message limit problem [#1078](https://github.com/pingcap/tidb-binlog/pull/1078)

+ Tools
       + TiCDC
              - Change Kafka Sink default `max-message-bytes` to 1MB [#2962](https://github.com/pingcap/ticdc/issues/2962)
              - Change Kafka Sink default `partition-num` to 3. [#3337](https://github.com/pingcap/ticdc/issues/3337)
## Improvements

+ TiKV

    - sst_importer: Reduce the space usage when using BR-Restore or Lightning-Local-backend by using zstd compression in SSTs  [#11469](https://github.com/tikv/tikv/issues/11469)

+ Tools

    + Backup & Restore (BR)

        - Increase the robustness for restoring [#1445](https://github.com/pingcap/br/pull/1445)

    + TiCDC

        - Add rate limiter to limit EtcdWorker tick frequency [#3267](https://github.com/pingcap/ticdc/pull/3267)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase [#3110](https://github.com/pingcap/ticdc/issues/3110)
        - Ignore the global flag for changefeed update command [#2803](https://github.com/pingcap/ticdc/issues/2803)
        - Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - Prohibit operating TiCDC clusters across major and minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)

## Bug fixes

+ TiDB

    - Fix a query panic caused by overflow in statistics module when calculating selectivity and converting a range to points for cost estimation [#23625](https://github.com/pingcap/tidb/issues/23625)
    - Fix wrong result for control function (`if`, `case when`, etc) with enum type [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix different results for function `greatest` when vectorized is off [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix index join panic on prefix index on some cases [#24547](https://github.com/pingcap/tidb/issues/24547)
    - Fix a bug that planner may cache invalid plans for joins in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix a bug that TiDB can not insert null into a not null column when `sql_mode` is empty [#11648](https://github.com/pingcap/tidb/issues/11648)
    - Fix wrong result type for function `greatest`/`least` [#29019](https://github.com/pingcap/tidb/issues/29019)
    - Fix privilege checking for `grant` and `revoke` operation on global level privileges [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix panic for `case when` function with enum type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong result of `microsecond` function in vectorized expression [#29244](https://github.com/pingcap/tidb/issues/29244)
    - Fix wrong result of `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Prevent conflicted optimistic transactions from locking each other [#11148](https://github.com/tikv/tikv/issues/11148)
    - Fix incomplete log information about auto analyze [#29188](https://github.com/pingcap/tidb/issues/29188)
    - Fix an issue that `NO_ZERO_IN_DATE` does not work on the default values [#26766](https://github.com/pingcap/tidb/issues/26766)
    - Fix copt-cache metrics, it will display the number of hits/miss/evict on Grafana now [#26338](https://github.com/pingcap/tidb/issues/26338)
    - Fix the issue that concurrently truncating the same partition hangs DDL [#26229](https://github.com/pingcap/tidb/issues/26229)
    - expression: fix wrong flen when cast decimal to string. [#29417](https://github.com/pingcap/tidb/issues/29417)
    - planner: change redundantSchema to fullSchema to correctly handle natural and "using" joins. [#29481](https://github.com/pingcap/tidb/issues/29481)
    - planner: fix topn wrongly pushed to index scan side when it's a prefix index [#29711](https://github.com/pingcap/tidb/issues/29711)
    - insert: fix the auto id retry won't cast the datum to origin type. [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - Make negative sign as false when decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix incorrect by-instance gRPC average duration [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix CDC panic due to missing downstream [#11123](https://github.com/tikv/tikv/issues/11123)
    - Fix channel full could break the raft connection [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix Max/Min bug when comparing signed and unsigned int64 [#10158](https://github.com/tikv/tikv/issues/10158)
    - Fix frequent CDC incremental scan retry due to `Congest` error [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - Fix panic issue after TiKV node scales in [#4344](https://github.com/tikv/pd/issues/4344)
    - Fix the issue that PD may not elect leader as soon as leader step down [#3936](https://github.com/tikv/pd/issues/3936)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

    - Fix the issue that comparison between Decimal may cause overflow and report `Can't compare`
    - Fix the issue that TiFlash fails to start up under platform without library `nsl`

+ Tools

    + TiCDC

        - Fix changefeed checkpoint lag negative value error [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix OOM in container environments [#3440](https://github.com/pingcap/ticdc/pull/3440)
        - Fix TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - Fix memory leak after processing DDLs [#3274](https://github.com/pingcap/ticdc/pull/3274)
        - Fix changefeed does not fast fail when occur ErrGCTTLExceeded error [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - Fix fallback resolvedTs event will block the progress of resolve lock when occur region merging [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - Fix kafka sink can not send message due to constraint by `max-message-size` option [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed [#11017](https://github.com/tikv/tikv/issues/11017)
        - Fix possible deadlocking when Kafka producer reports an error [#3015](https://github.com/pingcap/ticdc/pull/3015)
        - Fix dml is not replicated after adding partition in partition table without valid index [#2863](https://github.com/pingcap/ticdc/pull/2863)
        - Fix memory leak which may happen in create new changefeed [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - Set config.Metadata.Timeout correctly to prevent stuck data synchronization [#3539](https://github.com/pingcap/ticdc/pull/3539)
        - processor,sink(cdc): let sink report resolved ts and do not skip buffer sink flush [#3561](https://github.com/pingcap/ticdc/pull/3561)
