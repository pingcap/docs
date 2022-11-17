---
title: TiDB Backup and Restore Overview
summary: Learn about the definition and features of TiDB backup and restore.
aliases: ['/docs/dev/br/backup-and-restore-tool/','/docs/dev/reference/tools/br/br/','/docs/dev/how-to/maintain/backup-and-restore/br/','/tidb/dev/backup-and-restore-tool/','/tidb/dev/point-in-time-recovery/']
---

# TiDB Backup and Restore Overview

Based on the Raft protocol and a reasonable topology, TiDB achieves high availability of clusters. When a few nodes in the cluster fail, the cluster can still provide services. On this basis, to further ensure the security of user data, TiDB provides the backup and restore feature. As the last resort to recover data from natural disasters and misuse, this feature provides the capability to restore service data from any misoperations.

TiDB backup and restore satisfies the following business requirements:

- Back up cluster data to a disaster recovery (DR) system with an RPO of no more than 10 minutes, reducing data loss in disaster scenarios.
- Handle the cases of incorrect writes from applications by rolling back data to a time point before the error event.
- Perform history data auditing to meet the requirements of laws and regulations.
- Clone the production environment, which is convenient for troubleshooting, performance tuning and verification, and simulation testing.

## Use backup and restore

The way to use the backup and restore feature varies with the deployment method of TiDB. This document introduces how to use the br command-line tool to back up and restore TiDB cluster data in on-premise deployment.

For information about how to use this feature in other deployment scenarios, see the following documents:

- [Back Up and Restore TiDB Deployed on TiDB Cloud](https://docs.pingcap.com/tidbcloud/backup-and-restore): It is recommended that you create TiDB clusters on [TiDB Cloud](https://www.pingcap.com/tidb-cloud/?from=en). TiDB Cloud offers an easy way to deploy and manage databases to let you focus on your applications.
- [Back Up and Restore Data Using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview): If you deploy a TiDB cluster using TiDB Operator on Kubernetes, it is recommended to back up and restore data using Kubernetes CustomResourceDefinition (CRD).

## Backup and restore features

TiDB backup and restore provides the following features:

- Back up cluster data: You can back up full data (**full backup**) of the cluster at a certain time point, or back up the data changes in TiDB (**log backup**, in which log means kv changes in TiKV).

- Restore backup data:

    - You can **restore a full backup** or **specific databases or tables** in a full backup to the state when data is backed up.
    - Based on backup data (full backup and log backup), you can specify any time point to restore the target cluster to the state when it is backed up. This type of restore is called point-in-time recovery, or PITR for short.

### Back up cluster data

Full backup backs up all data of a cluster at a specific time point. TiDB supports the following ways of full backup:

- Back up cluster snapshots: A snapshot of a TiDB cluster contains transactionally consistent data at a specific time. You can back up snapshot data of a TiDB cluster using br command-line tool. For details, see [Snapshot backup](TBP).

Ful backup occupies much storage space and contains only cluster data at a specific time point. If you need to flexibly choose the time point of recovery (PITR), you can use the following two ways of backup at the same time:

- Start [log backup](/br/br-pitr-guide.md#start-log-backup). After log backup is started, the task keeps running on all TiKV nodes and backs up TiDB incremental data in small batches to the specified storage periodically.
- Perform [snapshot backup](/br/br-snapshot-guide.md#back-up-snapshots) regularly. Back up the full cluster data to the backup storage, for example, perform cluster snapshot backup at 0:00 every day.

#### Backup performance and impact on TiDB clusters

- The impact of backup on a TiDB cluster is kept below 20%, and this value can be reduced to 10% or less with the proper configuration of the TiDB cluster. The backup speed of a TiKV node is scalable and ranges from 50 MB/s to 100 MB/s. For more information, see [Backup performance and impact](/br/br-usage-backup.md#performance-and-impact-of-snapshot-backup).
- When there are only log backup tasks, the impact on the cluster is about 5%. Log backup flushes all the changes generated after the last refresh every 5-10 minutes to the backup storage, which can **achieve a Recovery Point Objective (RPO) of no more than ten minutes**.

### Restore backup data

Corresponding to the backup features, you can perform two types of restore: full restore and PITR.

- Restore a full backup

    - Restore cluster snapshot backup: You can restore snapshot backup data to an empty data or a cluster that does not have data conflicts (with duplicate schemas or tables). For details, see [Restore snapshot backup](/br/br-snapshot-guide.md#restore-snapshot-backup). In addition, you can restore specific databases or tables from the backup data and filter out unwanted data. For details, see [Restore specific databases or tables from backup data](/br/br-snapshot-guide.md#restore-specific-databases-or-tables-from-backup-data).

- Restore data to any point in time (PITR)

    - By running the `br restore point` command, you can restore the latest snapshot backup data and log back data to a specified time. br command-line tool automatically determines the restore scope, accesses backup data, and restores data to the target cluster.

#### Restore performance and impact on TiDB clusters

- Data restore is performed at a scalable speed. Generally, the speed is 100 MB/s per TiKV node. BR only supports restoring data to a new cluster and uses the resources of the target cluster as much as possible. For more details, see [Restoration performance and impact](/br/br-snapshot-guide.md#restoration-performance-and-impact).
- On each TiKV node, PITR can restore log data at 30 GiB/h. For more details, see [PITR performance and impact](/br/br-pitr-guide.md#performance-and-impact).

## Backup storage

BR supports backing up data to Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, NFS, and other S3-compatible file storage services. For details, see the following content:

- [Specify backup storage in URL](/br/backup-and-restore-storages.md#url-format)
- [Configure access privileges to backup storages](/br/backup-and-restore-storages.md#authentication)

## Before you use

This section describes the prerequisites for using the TiDB backup and restore tool, including the usage tips and compatibility issues.

### Some tips

Snapshot backup

- It is recommended that you perform the backup operation during off-peak hours to minimize the impact on applications.
- It is recommended that you execute multiple backup or restoration operations one by one. Running backup operations in parallel reduces performance and also affects online applications. Worse still, lack of collaboration between multiple tasks might result in task failures and affect cluster performance.

Snapshot restore

- br command-line tool uses resources of the target cluster as much as possible. Therefore, it is recommended that you restore data to a new cluster or an offline cluster. Avoid restoring data to a production cluster. Otherwise, services might be affected. PITR only supports restoring data to empty clusters.

PITR

- You can only perform cluster-level PITR. Database-level and table-level PITR are not supported.
- You cannot restore data in the user tables or the privilege tables.

Backup storage and network configuration

- It is recommended that you store backup data to a storage system that is compatible with Amazon S3, GCS, or Azure Blob Storage.
- br command-line tool, TiKV, and the backup storage system should provide network bandwidth, and the storage system should have sufficient write/read performance (IOPS). Otherwise, they might become a performance bottleneck during backup and restore.

### Compatibility

Before you use BR, pay attention to its usage restrictions, compatibility, and other considerations.

#### Compatibility with other features

Backup and restore might go wrong when some features are enabled or disabled. If these features are not consistently enabled or disabled during backup and restore, compatibility issues might occur.

| Feature | Issue | Solution |
|  ----  | ----  | ----- |
|GBK charset|| br command-line tool of versions earlier than v5.4.0 does not support restoring `charset=GBK` tables. No version of br command-line tool supports recovering `charset=GBK` tables to TiDB clusters earlier than v5.4.0. |
| Clustered index | [#565](https://github.com/pingcap/br/issues/565) | Make sure that the value of the `tidb_enable_clustered_index` global variable during restoration is consistent with that during backup. Otherwise, data inconsistency might occur, such as `default not found` and inconsistent data index. |
| New collation  | [#352](https://github.com/pingcap/br/issues/352)       | Make sure that the value of the `new_collations_enabled_on_first_bootstrap` variable during restoration is consistent with that during backup. Otherwise, inconsistent data index might occur and checksum might fail to pass. For more information, see [FAQ - Why does BR report `new_collations_enabled_on_first_bootstrap` mismatch?](/faq/backup-and-restore-faq.md#why-does-br-report-new_collations_enabled_on_first_bootstrap-mismatch). |
| Global temporary tables | | Make sure that you are using v5.3.0 or a later version of br command-line tool to back up and restore data. Otherwise, an error occurs in the definition of the backed global temporary tables. |
| TiDB Lightning Physical Import| | If the upstream database uses TiDB Lightning's physical import mode to import data, the data cannot be backed up in log backup. It is recommended to perform a full backup after the data import.  For more information, see [When the upstream database imports data using TiDB Lightning in the physical import mode, the log backup feature becomes unavailable. Why?](TBP).|

#### Version check

Before performing backup and restore, br command-line tool compares and checks the TiDB cluster version with its own. If there is a major-version mismatch, br command-line tool prompts a reminder to exit. To forcibly skip the version check, you can set `--check-requirements=false`. Note that skipping the version check might introduce incompatibility.

| Backup version (vertical) \ Restoration version (horizontal) | Restore to TiDB v6.0 | Restore to TiDB v6.1 | Restore to TiDB v6.2 | Restore to TiDB v6.3 |
|  ----  |  ----  | ---- | ---- | ---- |
| TiDB v6.0 snapshot backup | Compatible | Compatible | Compatible | Compatible |
| TiDB v6.1 snapshot backup | Compatible (A known issue [#36379](https://github.com/pingcap/tidb/issues/36379): if backup data contains an empty schema, br might report an error.) | Compatible | Compatible | Compatible |
| TiDB v6.2 snapshot backup | Compatible (A known issue [#36379](https://github.com/pingcap/tidb/issues/36379): if backup data contains an empty schema, BR might report an error.) | Compatible | Compatible | Compatible |
| TiDB v6.3 snapshot backup | Compatible (A known issue [#36379](https://github.com/pingcap/tidb/issues/36379): if backup data contains an empty schema, BR might report an error.) | Compatible | Compatible | Compatible |
| TiDB v6.3 log backup| \ | \ | Incompatible | Compatible |

## See also

- [TiDB Snapshot Backup and Restore Guide](/br/br-snapshot-guide.md)
- [TiDB Log Backup and PITR Guide](/br/br-pitr-guide.md)
- [Backup Storages](/br/backup-and-restore-storages.md)
