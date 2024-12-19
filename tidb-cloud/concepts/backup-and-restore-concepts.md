---
title: Backup & Restore
summary: Learn about backup & restore concepts for TiDB Cloud.
---

# Backup & Restore

TiDB Cloud Backup & Restore features are designed to safeguard your data and ensure business continuity by enabling you to back up and recover cluster data.

## Snapshot backup

Snapshot backup is an implementation to back up the entire cluster. It is based on [multi-version concurrency control (MVCC)](/tidb-storage.md#mvcc) and backs up all data in the specified snapshot to a target storage. The size of the backup data is approximately the size of the compressed single replica in the cluster.

## Automatic backup

For both TiDB Cloud Serverless and TiDB Cloud Dedicated clusters, snapshot backups are taken automatically by default and stored according to your backup retention policy.

## Log backup

Snapshot backup contains the full cluster data at a certain point, while TiDB log backup can back up data written by applications to a specified storage in a timely manner.

If you want to choose the restore point as required, that is, to perform point-in-time recovery (PITR), note the following:

- For TiDB Cloud Serverless clusters, PITR is available only for scalable clusters and not available for free clusters.
- For TiDB Cloud Dedicated clusters, you need to [enable PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore) in advance.

## Manual backup

Dual region backup is a feature of TiDB Cloud Dedicated that enables you to back up your data to a known state as needed, and then restore to that state at any time.

For more information, see [Perform a manual backup](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup).

## Dual region backup

Dual region backup is a feature of TiDB Cloud Dedicated that enables you to replicate backups from your cluster region to another different region. After it is enabled, all backups are automatically replicated to the specified region. This provides cross-region data protection and disaster recovery capabilities. It is estimated that approximately 99% of the data can be replicated to the secondary region within an hour.

For more information, see [Turn on dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).

## Point-in-time Restore

Point-in-time Restore is a feature that enables you to restore data of any point in time to a new cluster. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

For more information, see [Turn on Point-in-time Restore](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore).