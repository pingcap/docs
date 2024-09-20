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

    In v8.4.0, this feature becomes generally available (GA).

    For more information, see [documentation](/partitioned-table.md#global-indexes).

* Optimize query performance for cached tables in some scenarios [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao) **tw@hfxsd** <!--1965-->

    Optimize query performance on cached tables by up to 5. 4 times when using `IndexLookup` to execute `SELECT ... LIMIT 1` with `IndexLookup`. Improve the performance of `IndexLookupReader` in full table scan and primary key query scenarios.

### Reliability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Availability

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

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

* Feature summary [#issue-number](issue-link) @[pr-auorthor-id](author-link)

    Feature descriptions (including what the feature is, why it is valuable for users, and how to use this feature generally)

    For more information, see [documentation](doc-link).

### Security

* TiDB BR Supports AWS IMDSv2 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu) **tw@hfxsd** <!--1945-->

    TiDB BR now supports AWS's Instance Metadata Service Version 2 (IMDSv2) when deployed on AWS EC2. This enables users to configure the newer session-oriented method on their EC2 instances, and for BR to be able to successfully use the IAM Role associated with the instance to access AWS S3 with the appropriate privileges.

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
