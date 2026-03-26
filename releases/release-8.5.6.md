---
title: TiDB 8.5.6 Release Notes
summary: Understand the compatibility changes, improvements, and bug fixes in the TiDB 8.5.6 release.
---

# TiDB 8.5.6 Release Notes

Release Date: 2026-xx-xx

TiDB Version: 8.5.6

Try it out: [Quick Start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production Deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup) | [Download Offline Package](https://pingkai.cn/download#tidb-community)

## Feature Details

### Stability

- The ability to set resource limits for background tasks in Resource Control is now Generally Available (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1933-->

    TiDB Resource Control can identify and lower the priority of background tasks. In some scenarios, even with idle resources, users may want to keep the consumption of background tasks at a very low level. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks under Resource Control can use, controlling the usage of all background tasks on each node below this percentage. This feature allows you to finely control the resource consumption of background tasks, further enhancing cluster stability.

    In v8.5.6, this feature is Generally Available (GA).

    For more information, please refer to the [User Documentation](/tidb-resource-control-background-tasks.md).

### Data Migration

- (dup): release-9.0.0.md > # Data migration * Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## Compatibility Changes

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Improvements

+ TiDB

    - Enhanced slow query log control by supporting [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules-new-in-v900) for targeted slow query log output based on combinations of multiple metrics, [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec-new-in-v900) for limiting the number of slow query log entries per second, and the [`WRITE_SLOW_LOG`](/identify-slow-queries.md#related-hint) hint for forcing specified SQL statements to be recorded in the slow query log [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)
    - Enhanced [Top SQL](/dashboard/top-sql.md) for resource analysis by supporting Top `5`, `20`, or `100` queries, hotspot analysis sorted by CPU, network traffic, or logical I/O, and aggregated analysis by `Query`, `Table`, `DB`, or `Region` on TiKV instances [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)
    - 新增 DXF 的 max_node_count 配置项支持 [#66376](https://github.com/pingcap/tidb/pull/66376)@[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - Add MVCC-read-aware load-based compaction to prioritize regions with heavy MVCC read overhead. [#19133](https://github.com/tikv/tikv/issues/19133) @[mittalrishabh](https://github.com/mittalrishabh)
    - Optimize stale-range cleanup during scaling by deleting stale keys directly instead of ingesting SST files, reducing latency impact. [#18042](https://github.com/tikv/tikv/issues/18042) @[LykxSassinator](https://github.com/LykxSassinator)
    - Make default gRPC raft connection and concurrency settings scale with CPU quota to improve resource utilization. [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add Top SQL support for collecting network traffic and logical I/O information to help diagnose SQL performance issues. [#18815](https://github.com/tikv/tikv/issues/18815) @[yibin87](https://github.com/yibin87)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.7.md > Improvements> PD - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

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

    - Fix the issue that upgrading from release-8.5-20250606-v8.5.2 to upstream release-8.5 can skip PITR metadata upgrades and cause PITR operations to fail. [#66994](https://github.com/pingcap/tidb/issues/66994) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that after EXCHANGE PARTITION, non-unique or nullable unique global indexes on non-clustered partitioned tables can become inconsistent and return incomplete results. [#65289](https://github.com/pingcap/tidb/issues/65289) @[mjonss](https://github.com/mjonss)
    - Support column-level privileges in GRANT and REVOKE. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve the performance of privilege updates such as GRANT and REVOKE in deployments with large numbers of privilege entries. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that KILL QUERY incorrectly kills idle connections. [#65447](https://github.com/pingcap/tidb/issues/65447) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that column-level privilege checks can be incorrect for JOIN ... USING, NATURAL JOIN, and INSERT ... ON DUPLICATE KEY UPDATE. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve privilege-check performance for deployments with many column-level privilege entries. [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Add cluster_id to mysql.tidb so external tools can determine whether two TiDB instances belong to the same cluster. [#59476](https://github.com/pingcap/tidb/issues/59476) @[YangKeao](https://github.com/YangKeao)
    - Improve the slow query log by printing non-printable prepared-statement arguments as hexadecimal literals. [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden)
    - 修复 tidb_service_scope 设置时未统一转换为小写的问题 [#66835](https://github.com/pingcap/tidb/pull/66835)@[D3Hunter](https://github.com/D3Hunter)
    - 修复 TiDB 重启后无法展示亲和力表的问题 [#66284](https://github.com/pingcap/tidb/issues/66284) @[lcwangchao](https://github.com/lcwangchao)
    - 修复可能出现的内存泄漏 [#65522](https://github.com/pingcap/tidb/issues/65522) @[bufferflies](https://github.com/bufferflies)

+ TiKV

    - Fix the issue that global indexes on non-unique columns of partitioned tables might become inconsistent and return incorrect results in some cases. [#19262](https://github.com/tikv/tikv/issues/19262) @[mjonss](https://github.com/mjonss)
    - Fix the issue that stalled coprocessor snapshot retrieval could occupy unified read pool workers until request deadlines expired, delaying other read requests. [#18491](https://github.com/tikv/tikv/issues/18491) @[AndreMouche](https://github.com/AndreMouche)
    - Fix the issue that follower replica reads could remain blocked on disk-full TiKV nodes by rejecting read-index requests on disk-full followers. [#19201](https://github.com/tikv/tikv/issues/19201) @[glorv](https://github.com/glorv)
    - Fix the issue that resolved-ts task backlogs could cause OOM when the resolved-ts worker is busy. [#18359](https://github.com/tikv/tikv/issues/18359) @[overvenus](https://github.com/overvenus)
    - Fix long-tail follower-read latency during leader transfer by retrying read-index requests sooner and adding a dedicated retry interval setting. [#18417](https://github.com/tikv/tikv/issues/18417) @[gengliqi](https://github.com/gengliqi)
    - Fix ingest latency spikes in large clusters by increasing the default `rocksdb.max-manifest-file-size` from 128 MiB to 256 MiB. [#18996](https://github.com/tikv/tikv/issues/18996) @[glorv](https://github.com/glorv)
    - (dup): release-5.1.4.md > Bug fixes> TiKV - Fix the rare data inconsistency issue when retrying a prewrite request in pessimistic transactions [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiCDC

        - Fixed an issue where changefeed might repeatedly create invalid dispatchers when the server restarts. [#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fixed an issue where table renaming operations could not be performed normally when the upstream TiDB version was <= v8.1.x. [#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        - Fixed a bug during data scanning to avoid potential abnormal crashes of TiKV when CDC is enabled. [#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        - Supported Azure Managed Identity authentication for azblob sinks and fixed a potential stuck issue during cloud storage uploads. [#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

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
