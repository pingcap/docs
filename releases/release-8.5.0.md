---
title: TiDB 8.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 8.5.0.
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

Release date: xx xx, 2024

TiDB version: 8.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

TiDB 8.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 8.1.0, 8.5.0 includes new features, improvements, and bug fixes released in [8.2.0-DMR](/releases/release-8.2.0.md), [8.3.0-DMR](/releases/release-8.3.0.md), and [8.4.0-DMR](/releases/release-8.4.0.md). When you upgrade from 8.1.x to 8.5.0, you can download the [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-en-release-notes.pdf) to view all release notes between the two LTS versions. The following table lists some highlights from 8.1.0 to 8.5.0:

<!--Highlights table: ToDo-->

## Feature details

### Scalability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Performance

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Reliability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Availability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### SQL

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### DB operations

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Observability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Security

* BR supports client-side encryption of log backup data (GA) [#56433](https://github.com/pingcap/tidb/issues/56433) @[Tristan1900](https://github.com/Tristan1900) tw@qiancai <!--1998-->

    TiDB v8.4.0 introduced an experimental feature to encrypt, on the client side, log backup data. Starting from v8.5.0, this feature is now Generally Avaialble. Before uploading log backup data to your backup storage, you can encrypt the backup data to ensure its security via one of the following methods:

    - Encrypt using a custom fixed key
    - Encrypt using a master key stored on a local disk
    - Encrypt using a master key managed by a Key Management Service (KMS)

  For more information, see [documentation](/br/br-pitr-manual.md#encrypt-the-log-backup-data).

### Data migration

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v8.1.0 to the current version (v8.2.0). If you are upgrading from v8.0.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|  |  |  |
|  |  |  |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### System tables

### Other changes

## Offline package changes

## Removed features

## Deprecated features

* The following features are planned for deprecation in future versions:

    * TiDB introduces the system variable [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800), which controls whether priority queues are enabled to optimize the ordering of tasks that automatically collect statistics. In future releases, the priority queue will be the only way to order tasks for automatically collecting statistics, so this system variable will be deprecated.
    * TiDB introduces the system variable [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) in v7.5.0. You can use it to set TiDB to use asynchronous merging of partition statistics to avoid OOM issues. In future releases, partition statistics will be merged asynchronously, so this system variable will be deprecated.
    * It is planned to redesign [the automatic evolution of execution plan bindings](/sql-plan-management.md#baseline-evolution) in subsequent releases, and the related variables and behavior will change.
    * In v8.0.0, TiDB introduces the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable to control whether TiDB supports disk spill for the concurrent HashAgg algorithm. In future versions, the [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800) system variable will be deprecated.
    * The TiDB Lightning parameter [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) is planned for deprecation in a future release and will be subsequently removed. This parameter will be replaced by [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task), which means that the maximum number of conflicting records is consistent with the maximum number of conflicting records that can be tolerated in a single import task.
    * Starting from v6.3.0, partitioned tables use [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode) by default. Compared with static pruning mode, dynamic pruning mode supports features such as IndexJoin and plan cache with better performance. Therefore, static pruning mode will be deprecated.

## Improvements

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Bug fixes

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [Contributor-GitHub-ID](id-link)
