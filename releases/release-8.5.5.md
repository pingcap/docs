---
title: TiDB 8.5.5 Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB 8.5.5.
---

# TiDB 8.5.5 Release Notes

Release date: xx xx, 2026

TiDB version: 8.5.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Features

### Scalability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Performance

* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001--> <!--TBD-->

    Starting from v8.5.5, the log backup compaction feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

    - **Improved recovery performance** - SST files can be more quickly imported into the cluster.
    - **Reduced storage space consumption** - redundant data is removed during compaction.
    - **Reduced impact on applications** - RPOs can be amintained with less frequent full snapshot-based backups.

  For more information, see [documentation](/br/br-compact-log-backup.md).

* Accelerated recovery of system tables from backups [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth) **tw@lilin90** <!--2109-->

    When restoring system tables from a backup, BR now introduces a new `--fast-load-sys-tables` parameter to use physical restoration instead of logical restoration. This option completely overwrites/replaces the existing tables, instead of restoring into them, for faster restoration for large scale deployments.

    For more information, see [Documentation](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema).

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Reliability

* Improved store scheduling in presence of network jitter [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang) **tw@qiancai** <!--2260-->

    Provides a network status feedback mechanism to PD to avoid re-scheduling the leaders back to a problematic node (experiencing network jitter) after the leaders had been transferred off the node by TiKV raft mechanism. If the network continues to jitter, PD will actively evict leader from jittering node.

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Availability

* Introduce Client Circuit Breaker Pettern for PD [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--2051-->

    To protect the PD leader from overloading due to retry storms or similar feedback loops, a circuit breaker pattern is introduced to limit incoming traffic (when a threshold of errors is reached) to enable the system to stabilize. The `tidb_cb_pd_metadata_error_rate_threshold_ratio` system variable is used to control the application of the circuit breaker.

    For more information, see [Documentation](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855).

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### SQL

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### DB operations

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    Starting from v8.5.5, log backups can continue to run when performing a snapshot restore (when prerequisite conditions are met). This enables ongoing log backups to proceed without having to stop them during the restore procedure. The newly restored data will also be recorded in the ongoing log backup.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore).

* Table level restores from Log Backups [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    Starting from v8.5.5, individual table level point in time recoveries can now be performed from log backups using filters. Being able to restore individual tables, instead of the full cluster, to a specific point in time enables much more flexible, and less impactful, recovery options.

    For more information, see [documentation](/br/br-pitr-manual.md#restore-data-using-filters).

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Observability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Security

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Data migration

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

## Compatibility changes

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

## Improvements

## Bug fixes