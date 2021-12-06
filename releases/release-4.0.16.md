---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release Date: December 10, 2021

TiDB version: 4.0.16

## Compatibility change(s)

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

## Feature enhancement(s)

+ TiDB

    - Fix wrong result type for greatest/least [#29911](https://github.com/pingcap/tidb/pull/29911)
    - This is a fix for grant global level case in v4.0 and v5.0 [#29899](https://github.com/pingcap/tidb/pull/29899)
    - Prevent conflicted optimistic transactions from locking each other. [#29775](https://github.com/pingcap/tidb/pull/29775)
    - Fix panic for caseWhen function with enum type [#29508](https://github.com/pingcap/tidb/pull/29508)
    - Fix wrong result of microsecond function in vectorized [#29384](https://github.com/pingcap/tidb/pull/29384)
    - Fix incomplete log information about auto analyze. [#29227](https://github.com/pingcap/tidb/pull/29227)
    - Fix wrong result of hour function in vectorized expression [#28870](https://github.com/pingcap/tidb/pull/28870)
    - None. [#27926](https://github.com/pingcap/tidb/pull/27926)
    - Fix an issue that NO_ZERO_IN_DATE does not work on the default values. [#26902](https://github.com/pingcap/tidb/pull/26902)
    - Fix copt-cache metrics, it will display the number of  hits/miss/evict on Grafana. [#26342](https://github.com/pingcap/tidb/pull/26342)
    - Fix the issue that concurrently truncating the same partition hangs DDL. [#26237](https://github.com/pingcap/tidb/pull/26237)

+ TiKV

    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11509](https://github.com/tikv/tikv/pull/11509)
    - Fix negative sign when decimal divide to zero [#11332](https://github.com/tikv/tikv/pull/11332)
    - Fix incorrect by-instance gRPC average duration. [#11326](https://github.com/tikv/tikv/pull/11326)
    - Fix CDC panic due to missing downstream. [#11135](https://github.com/tikv/tikv/pull/11135)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11089](https://github.com/tikv/tikv/pull/11089)
    - fix channel full could break the raft connection [#11069](https://github.com/tikv/tikv/pull/11069)
    - Database restored from BR or Lightning Local-backend is now smaller, should be matching the original cluster size when backed up. [#10642](https://github.com/tikv/tikv/pull/10642)
    - [#10616](https://github.com/tikv/tikv/pull/10616)
    - [#9870](https://github.com/tikv/tikv/pull/9870)

+ PD

    - Should break the suspect region range loop when checker is busy [#4339](https://github.com/tikv/pd/pull/4339)
    - [#4292](https://github.com/tikv/pd/pull/4292)
    - Speed scheduler exit [#4200](https://github.com/tikv/pd/pull/4200)

+ TiFlash

+ Tools

    + BR

        - Increase the robustness for restoring. [#1445](https://github.com/pingcap/br/pull/1445)

    + TiCDC

        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3565](https://github.com/pingcap/ticdc/pull/3565)
        - Fix changefeed checkpoint lag negative value error [#3532](https://github.com/pingcap/ticdc/pull/3532)
        - Fix OOM in container environments. [#3440](https://github.com/pingcap/ticdc/pull/3440)
        - Show changefeed checkepoint catch-up ETA in metrics. [#3313](https://github.com/pingcap/ticdc/pull/3313)
        - Fix a bug that TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3290](https://github.com/pingcap/ticdc/pull/3290)
        - Fix memory leak after processing DDLs. [#3274](https://github.com/pingcap/ticdc/pull/3274)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3267](https://github.com/pingcap/ticdc/pull/3267)
        - `None`. [#3210](https://github.com/pingcap/ticdc/pull/3210)
        - Please add a release note. If you don't think this PR needs a release note then fill it with `None`. [#3176](https://github.com/pingcap/ticdc/pull/3176)
        - bugfix: fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3134](https://github.com/pingcap/ticdc/pull/3134)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3131](https://github.com/pingcap/ticdc/pull/3131)
        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3106](https://github.com/pingcap/ticdc/pull/3106)
        - fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3099](https://github.com/pingcap/ticdc/pull/3099)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#3094](https://github.com/pingcap/ticdc/pull/3094)
        - fix kafka sink can not send message due to constraint by `max-message-size` option. [#3046](https://github.com/pingcap/ticdc/pull/3046)
        - Nond [#3042](https://github.com/pingcap/ticdc/pull/3042)
        - Add metrics to observe incremental scan remaining time [#3032](https://github.com/pingcap/ticdc/pull/3032)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed. [#3023](https://github.com/pingcap/ticdc/pull/3023)
        - Fix possible deadlocking when Kafka producer reports an error. [#3015](https://github.com/pingcap/ticdc/pull/3015)
        - Release new owner and processor implementation to release-5.0.
        - Highly available model and core modules refactoring.(ref: https://github.com/pingcap/ticdc/pull/1927) [#3014](https://github.com/pingcap/ticdc/pull/3014)
        - `None`. [#2945](https://github.com/pingcap/ticdc/pull/2945)
        - ignore the global flag for changefeed update command. [#2875](https://github.com/pingcap/ticdc/pull/2875)
        - Fix dml is not replicated after adding partition in partition table without valid index [#2863](https://github.com/pingcap/ticdc/pull/2863)
        - Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time. [#2851](https://github.com/pingcap/ticdc/pull/2851)
        - Fix memory leak which may happen in create new changefeed. [#2623](https://github.com/pingcap/ticdc/pull/2623)
        - Prohibit operating TiCDC clusters across major and minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)

## Improvements

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

## Bug Fixes

+ TiDB

    - Check step overflow when converting a range to points for estimation [#30017](https://github.com/pingcap/tidb/pull/30017)
    - Fix wrong result for control function with enum type. [#30011](https://github.com/pingcap/tidb/pull/30011)
    - expression: fix different results for greatest when vectorized is off. [#29916](https://github.com/pingcap/tidb/pull/29916)
    - Fix index join panic on prefix index on some cases [#29217](https://github.com/pingcap/tidb/pull/29217)
    - Planner: fix the issue that planner may cache invalid plans for joins in some cases [#28444](https://github.com/pingcap/tidb/pull/28444)
    - Fix a bug that can not insert null into a not null column in the empty SQL mode [#27832](https://github.com/pingcap/tidb/pull/27832)

+ TiKV

+ PD

    - Fix panic issue after TiKV node scales in [#4378](https://github.com/tikv/pd/pull/4378)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4219](https://github.com/tikv/pd/pull/4219)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4133](https://github.com/tikv/pd/pull/4133)

+ TiFlash

    - Fix the issue that comparison between Decimal may cause overflow and report `Can't compare`. [#3365](https://github.com/pingcap/tics/pull/3365)
    - Fix the issue that TiFlash fails to start up under platform without library `nsl` [#3209](https://github.com/pingcap/tics/pull/3209)

+ Tools