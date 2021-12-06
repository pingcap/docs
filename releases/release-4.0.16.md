---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release Date: December 03, 2021

TiDB version: 4.0.16

## Improvements

+ Tools

  + TiCDC

    + Show changefeed checkepoint catch-up ETA in metrics. [#3313](https://github.com/pingcap/ticdc/pull/3313)
    + Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3131](https://github.com/pingcap/ticdc/pull/3131)
    + change Kafka sink default `MaxMessageBytes` to 1MB. [#3106](https://github.com/pingcap/ticdc/pull/3106)
    + Nond [#3042](https://github.com/pingcap/ticdc/pull/3042)
    + Add metrics to observe incremental scan remaining time [#3032](https://github.com/pingcap/ticdc/pull/3032)
    + Release new owner and processor implementation to release-5.0.
    + Highly available model and core modules refactoring. [1927](https://github.com/pingcap/ticdc/pull/1927) [#3014](https://github.com/pingcap/ticdc/pull/3014)
    + `None`. [#2945](https://github.com/pingcap/ticdc/pull/2945)
    + Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time. [#2851](https://github.com/pingcap/ticdc/pull/2851)
    + Prohibit operating TiCDC clusters across major and minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)

## Bug Fixes

+ TiFlash

  + Fix the issue that comparison between Decimal may cause overflow and report `Can't compare`. [#3365](https://github.com/pingcap/tics/pull/3365)
  + Fix the issue that TiFlash fails to start up under platform without library `nsl` [#3209](https://github.com/pingcap/tics/pull/3209)

+ Tools

  + TiCDC

    + Fix a bug that TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3290](https://github.com/pingcap/ticdc/pull/3290)
    + Fix memory leak after processing DDLs. [#3274](https://github.com/pingcap/ticdc/pull/3274)
    + Fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3134](https://github.com/pingcap/ticdc/pull/3134)
    + Fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3099](https://github.com/pingcap/ticdc/pull/3099)
    + Fix kafka sink can not send message due to constraint by `max-message-size` option. [#3046](https://github.com/pingcap/ticdc/pull/3046)
    + Fix possible deadlocking when Kafka producer reports an error. [#3015](https://github.com/pingcap/ticdc/pull/3015)
    + Fix dml is not replicated after adding partition in partition table without valid index [#2863](https://github.com/pingcap/ticdc/pull/2863)
    + Fix memory leak which may happen in create new changefeed. [#2623](https://github.com/pingcap/ticdc/pull/2623)