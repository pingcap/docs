---
title: TiDB 7.5.8 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 7.5.8.
---

# TiDB 7.5.8 Release Notes

Release date: TBD

TiDB version: 7.5.8

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## Improvements

+ PD

    - Add the `store` label to the `pd_cluster_status` metric so that PD reports per-store status metrics, making it easier to identify affected TiKV stores and aggregate cluster-wide values when needed [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/10060 -->

## Bug fixes

+ TiDB

    - Fix the issue that TiDB might crash with a `SIGSEGV` during `UNION` query execution when `UnionExec` shuts down concurrently with worker goroutines [#66391](https://github.com/pingcap/tidb/issues/66391) @[bb7133](https://github.com/bb7133) <!-- component: execution --> <!-- pr: https://github.com/pingcap/tidb/pull/67003 -->
    - Fix the issue that TiDB consumes excessive CPU during query planning in some scenarios because of expensive full-range checks [#63235](https://github.com/pingcap/tidb/issues/63235) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/64058 --> <!-- pr: https://github.com/pingcap/tidb/pull/63813 -->
    - Fix the potential panic issue that occurs during asynchronous statistics loading for newly added indexes when `tidb_opt_objective` is set to `determinate` [#64274](https://github.com/pingcap/tidb/issues/64274) @[0xPoe](https://github.com/0xPoe) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/64292 -->

+ TiKV

    - Fix the issue that TiKV might panic with `txn record found but not expected` due to a race between SST ingestion and concurrent writes during Region snapshot application [#19891](https://github.com/tikv/tikv/issues/19891) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19914 -->
    - Fix the issue that BR leaves stale GC service safepoints after a log backup task is stopped, which might prevent expected garbage collection cleanup [#19832](https://github.com/tikv/tikv/issues/19832) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19913 -->
    - Fix the issue that stale connections between TiKV and TiCDC might not be fully cleaned up after TiCDC restarts or network failures, exhausting the TiKV CDC memory quota and causing changefeeds to stall [#18169](https://github.com/tikv/tikv/issues/18169) [#19610](https://github.com/tikv/tikv/issues/19610) @[asddongmen](https://github.com/asddongmen) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/tikv/tikv/pull/18864 --> <!-- pr: https://github.com/tikv/tikv/pull/19689 -->
    - Fix the issue that TiKV throughput might continue to drop during a TiKV I/O hang because PD-related work is blocked by I/O operations [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/18969 -->
    - Fix the issue that external SST ingestion no longer allows foreground writes, which increases write latency during ingestion [#19954](https://github.com/tikv/tikv/issues/19954) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19978 -->
    - Fix the issue that TiKV might crash with a null pointer dereference during TiDB Lightning data import [#18671](https://github.com/tikv/tikv/issues/18671) @[Dog-Du](https://github.com/Dog-Du) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19908 -->

+ PD

    - Fix the issue that PD might experience a goroutine surge and become unstable when TiDB Lightning concurrently calls `SetRegionLabelRule` during import [#9854](https://github.com/tikv/pd/issues/9854) @[lhy1024](https://github.com/lhy1024) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/9897 -->

+ TiFlash

    - Fix the issue that TiFlash might return inconsistent results from TiKV after a column is modified from `NOT NULL` to `NULL` [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang) <!-- component: storage --> <!-- pr: https://github.com/pingcap/tiflash/pull/10690 -->

+ Tools

    + TiCDC

        - Fix the issue that TiCDC Kafka changefeeds might leak Kafka client instances when sending DDL events or checkpoints fails and TiCDC retries the operation, causing memory usage to keep increasing [#12666](https://github.com/pingcap/tiflow/issues/12666) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/tiflow/pull/12678 -->
        - Fix the issue that TiCDC Kafka sink retries might leak Sarama client connections and background goroutines when Kafka admin or producer initialization fails, or when closing wrapped clients [#12572](https://github.com/pingcap/tiflow/issues/12572) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/tiflow/pull/12592 -->
