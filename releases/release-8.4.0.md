---
title: TiDB 8.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.4.0.
---

# TiDB 8.4.0 Release Notes

Release date: xx xx, 2024

TiDB version: 8.4.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.4/quick-start-with-tidb)

8.4.0 introduces the following key features and improvements:

## Feature details

### Scalability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Performance

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* The performance of batch user creation and password changes has been improved by hundreds of times [#55604](https://github.com/pingcap/tidb/pull/55604) @[wjhuang2016](https://github.com/wjhuang2016) **tw@hfxsd** <!--1941-->

    In SaaS scenarios, you might need to batch-create a large number of users, rotate passwords periodically, and complete these tasks within a specific time window. Starting from v8.4.0, the performance of batch user creation and password rotation has been significantly improved. Additionally, you can further enhance performance by increasing concurrency through a higher number of session connections, which greatly reduces execution time for these operations.

* Partitioned tables support global indexes (GA) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple)

    In previous versions of partitioned tables, some limitations exist because global indexes are not supported. For example, the unique key must use every column in the table's partitioning expression. If the query condition does not use the partitioning key, the query will scan all partitions, resulting in poor performance. Starting from v7.6.0, the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) is introduced to enable the global index feature. But this feature was under development at that time and it is not recommended to enable it.

    Starting with v8.3.0, the global index feature is released as an experimental feature. You can explicitly create a global index for a partitioned table with the keyword `Global` to remove the restriction that the unique key must use every column in the table's partitioning expression, to meet flexible business needs. Global indexes also enhance the performance of queries that do not include partition keys.

    In v8.4.0, this feature becomes generally available (GA). You can directly use the keyword `GLOBAL` to create a global index, instead of setting the system variable [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760) to enable the global index feature.

    For more information, see [documentation](/partitioned-table.md#global-indexes).

* Optimize query performance for cached tables in some scenarios [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao) **tw@hfxsd** <!--1965-->

    Optimize the query performance of cached tables by up to 5.4 times when using `IndexLookup` to execute `SELECT ... LIMIT 1` with `IndexLookup`. Improve the performance of `IndexLookupReader` in full table scan and primary key query scenarios.

### Reliability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

* Support runaway queries to switch resource groups [#54434](https://github.com/pingcap/tidb/issues/54434) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1832-->

    In TiDB v8.4.0, you can redirect runaway queries to a specific resource group. If the `COOLDOWN` mechanism fails to lower resource consumption, you can create a [resource group](/tidb-resource-control.md#create-a-resource-group) and set the `SWITCH_GROUP` parameter to move identified runaway queries to this group. Meanwhile, subsequent queries within the same session will continue to execute in the original resource group. By switching resource groups, you can more precisely manage resource usage and better control the impact of runaway queries.

    For more information, see [documentation](/tidb-resource-control.md#query_limit-parameters).

* The system variable `tidb_scatter_region` supports the cluster-level Region scattering strategy [#55184](https://github.com/pingcap/tidb/issues/55184) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1927-->
	
    In previous versions, the system variable `tidb_scatter_region` can only be enabled or disabled. When enabled, it applies a table-level scattering strategy during batch table creation. However, when creating hundreds of thousands of tables in a batch, this approach results in a concentration of regions on a few TiKV nodes, causing out-of-memory (OOM) issues on those nodes.

    To address this, starting from v8.4.0, `tidb_scatter_region` is changed to a string type. It now supports a cluster-level scattering strategy, helping scatter regions more evenly and preventing OOM problems on TiKV nodes.
	
    For more information, see [documentation](/system-variables.md#tidb_scatter_region).

* Support setting resource caps for background tasks of resource control [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1909-->
	
    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of these tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set a maximum percentage of resources that a background task can consume. Each node will ensure that the resource usage of all background tasks stays within this limit. This feature enables precise control over resource consumption for background tasks, enhancing cluster stability.

    For more information, see [documentation](/tidb-resource-control.md#manage-background-tasks).

### Availability

* TiProxy supports traffic replay (experimental) [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1942-->

    Starting from TiProxy v1.3.0, you can use TiProxy to capture access traffic in a TiDB production cluster and replay it in a test cluster at a specified rate. This feature enables you to reproduce actual workloads from the production cluster in a test environment, verifying SQL statement execution results and performance.

    Traffic replay is suitable for the following scenarios:

    - Validate TiDB version upgrades
    - Assess change impact
    - Validate performance before TiDB scaling
    - Test performance limits

    You can use `tiproxyctrl` to connect to the TiProxy instance and perform traffic capture and replay.

    For more information, see [documentation](/tiproxy/tiproxy-traffic-replay.md).

### SQL

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### DB operations

* PITR adds client-side log backup data encryption support (experimental) [55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900) **tw@qiancai** <!--1920-->

    Previously only the data from a snapshot based backup could be encrypted (on the client side) with a data key provided by the user. With this feature, log backups may now also be encrypted, ensuring that the confidentiality of information within the backup data is secured.

    For more information, see [documentation](doc-link).

* BR reduces requires storage permissions for restores [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1943-->

    Previously, when BR was restoring data, checkpoint information about the progress of the restore was recorded in the location hosting the backup data. These restore checkpoints enabled restoration to be quickly resumed if it was interrupted. With this feature, the restore checkpoints are now stored in the target TiDB cluster. This means that BR only requires read access to the backup dataset location for restores.

    For more information, see [documentation](doc-link).
  
* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Observability

* Display the CPU time of TiDB and TiKV in the system table [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1877-->

      The [Top SQL page](/dashboard/top-sql.md) of [TiDB Dashboard](/dashboard/dashboard-intro.md) displays SQL statements with high CPU consumption. Starting from v8.4.0, TiDB includes CPU time consumption data in the system table, alongside other session or SQL metrics, allowing you to easily monitor high CPU usage from multiple perspectives. This information is especially useful in identifying the root cause of issues such as CPU spikes or hotspots in cluster read/write operations.

    - [STATEMENTS_SUMMARY](/statement-summary-tables.md) adds `AVG_TIDB_CPU_TIME` and `AVG_TIKV_CPU_TIME` to show the average CPU time consumed by individual SQL statements historically.
    - [INFORMATION_SCHEMA.PROCESSLIST](/information-schema/information-schema-processlist.md) adds `TIDB_CPU` and `TIKV_CPU` to display the cumulative CPU consumption of currently executing SQL statements in a session.
    - The [slow Log](/analyze-slow-queries.md) adds the `Tidb_cpu_time` and `Tikv_cpu_time` fields to show the CPU time of captured SQL statements.

  By default, TiKV CPU time is displayed. Collecting TiDB CPU time introduces an additional overhead (about 8%), so TiDB CPU time is only displayed as the actual value when the [Top SQL feature](https://github.com/dashboard/top-sql.md) is enabled; otherwise, it will always display as `0`.

    For more information, see [documentation](/information-schema/information-schema-processlist.md) and [documentation](information-schema/information-schema-slow-query.md).

### Security

* BR supports AWS IMDSv2 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu) **tw@hfxsd** <!--1945-->

    BR now supports AWS Instance Metadata Service Version 2 (IMDSv2) when deployed on AWS EC2. This allows you to configure the newer session-oriented method on EC2 instances, enabling BR to successfully use the instance's associated IAM role to access AWS S3 with the appropriate privileges.

    For more information, see [documentation](/backup-and-restore-storages#authentication).

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Data migration

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.3.0 to the current version (v8.4.0). If you are upgrading from v8.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* Behavior change

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### System tables

## Offline package changes

## Deprecated features

* The following features are deprecated starting from v8.4.0:

    * Deprecated feature

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.       
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.

* The following features are planned for removal in future versions:

    * Starting from v8.0.0, TiDB Lightning deprecates the [old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800) strategy for the physical import mode, and enables you to control the conflict detection strategy for both logical and physical import modes via the [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter. The [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) parameter for the old version of conflict detection will be removed in a future release.

## Improvements

+ TiDB

- Optimize MEMDB implementation to reduce write latency in transactions and TiDB CPU usage [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->

+ TiKV
- Increase the default value of Region from 96 MiB to 256 MiB to avoid the extra overhead caused by too many Regions [#17309](https://github.com/tikv/tikv/issues/17309) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1925-->
- Introduce a new `spill-dir` configuration in Raft Engine to support multi-disk storage for Raft logs. When the disk containing the home directory (`dir`) runs out of space, Raft Engine automatically writes new logs to `spill-dir`, ensuring continuous operation. [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1970-->
+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## Bug fixes

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## Contributors

We would like to thank the following contributors from the TiDB community:
