---
title: TiDB 8.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 8.5.4.
---

# TiDB 8.5.4 Release Notes

Release date: xx xx, 2025

TiDB version: 8.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Compatibility changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
- (dup): release-7.5.7.md > Compatibility changes - TiKV deprecates the following configuration items and replaces them with the new [`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file/#gcauto-compaction) configuration group, which controls automatic compaction behavior [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - Deprecated configuration items: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-interval), [`region-compact-check-step`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-step), [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones), [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent), [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710), and [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710).
    - New configuration items: [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#check-interval-new-in-v757), [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757), [`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757), [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757), and [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bottommost-level-force-new-in-v757).

## Improvements

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md(beta.1) > # SQL * Support creating global indexes on non-unique columns of partitioned tables [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > Improvements> TiDB - Support applying the `semi_join_rewrite` hint to Semi Joins in `IN` subqueries [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.7.md > Improvements> TiKV - Optimize the tail latency of async snapshot and write operations in environments with a large number of SST files [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD

    - degrade some unecessary error log [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - upgrade the golang and dependent version[#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - support to distribute table feature, make scatter easier #[8986](https://github.com/tikv/pd/issues/8986)  @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.7.md > Bug fixes> TiDB - Fix the issue that row count estimates across months or years can be significantly overestimated [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ PD

    - Fix PD Client initial strategy not work well [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - Fix the wrong APIS of the `/config` 和 `/members`  [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024) 
    - Fix the handler way of the tso error #[9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - Fix the bucket split still work even if the bucket doesn't report #[9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - Fix the wrong token allocation of the resource manager #[9455](https://github.com/tikv/pd/issues/9455)  @[JmPotato](https://github.com/JmPotato)
    - Fix the placement rule revert after pd leader changed #[9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - Fix the ttl configuration not work #[9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - Fix the issue where Zstd compression did not take effect in log backup, resulting in uncompressed output. [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        - Fixed a bug that may cause flush operation slow in azure blob storage. [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `log truncate` panic when failed to delete file. [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        - Fixed a bug that may cause `stats_meta` be zero when checksumming disabled. [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        - Reduced chance of BR restore failure from S3-compatible storage when the S3 server limits bandwidth through traffic shaping. [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        - Fix the issue that the log backup observer loses observation of a region. [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        - Fixed a a bug that may cause `restore point` fail when there are some special sized table schemas.   [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})