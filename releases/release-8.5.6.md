---
title: TiDB 8.5.6 Release Notes
summary: Understand the compatibility changes, improvements, and bug fixes in the TiDB 8.5.6 release.
---

# TiDB 8.5.6 Release Notes

Release Date: 2026-xx-xx

TiDB Version: 8.5.6

Try it out: [Quick Start](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [Production Deployment](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [Download Offline Package](https://pingkai.cn/download#tidb-community)

## Feature Details

### Stability

- The ability to set resource limits for background tasks in Resource Control is now Generally Available (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDB Resource Control can identify and lower the priority of background tasks. In some scenarios, even with idle resources, users may want to keep the consumption of background tasks at a very low level. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks under Resource Control can use, controlling the usage of all background tasks on each node below this percentage. This feature allows you to finely control the resource consumption of background tasks, further enhancing cluster stability.

    In v8.5.6, this feature is Generally Available (GA).

    For more information, please refer to the [User Documentation](/tidb-resource-control-background-tasks.md).

### Data Migration

- (dup): release-9.0.0.md > # 数据迁移 * 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## Compatibility Changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.4.md > 改进提升> TiKV - 优化 gRPC 线程池线程数量默认值的计算方式，将原固定值调整为根据总的 CPU 配置动态计算，避免因 gRPC 线程数量过小导致的性能瓶颈 [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.5.5.md > 改进提升> TiKV - 在 TiKV 内存占用高时，对 BR 的日志恢复请求进行限流，防止 TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.5.md > 改进提升> PD - 优化了高基数指标，降低 PD 的内存占用和监控系统压力 [#9357](https://github.com/tikv/pd/issues/9357) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.5.7.md > 改进提升> PD - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
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

## Bug Fixes

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-5.1.4.md > Bug 修复> TiKV - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-8.5.4.md > 错误修复> PD - 修复 Resource Manager 错误分配 token 导致查询卡住的问题 [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - (dup): release-8.5.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复集群中存在大量 Region 时，开启日志备份导致内存占用过高的问题 [#18719](https://github.com/tikv/tikv/issues/18719) @[YuJuncen](https://github.com/YuJuncen)

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