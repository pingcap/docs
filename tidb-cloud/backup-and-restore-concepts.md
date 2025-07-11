---
title: Backup & Restore
summary: Learn about backup & restore concepts for TiDB Cloud.
---

# Backup & Restore

TiDB Cloud Backup & Restore features are designed to safeguard your data and ensure business continuity by enabling you to back up and recover cluster data.

## Automatic backup

For both TiDB Cloud Serverless and TiDB Cloud Dedicated clusters, snapshot backups are taken automatically by default and stored according to your backup retention policy.

For more information, see the following:

- [Automatic backups for TiDB Cloud Serverless clusters](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [Automatic backups for TiDB Cloud Dedicated clusters](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## Manual backup

Manual backup is a feature of TiDB Cloud Dedicated that enables you to back up your data to a known state as needed, and then restore to that state at any time.

For more information, see [Perform a manual backup](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup).

## Dual region backup

Dual region backup is a feature of TiDB Cloud Dedicated that enables you to replicate backups from your cluster region to another different region. After it is enabled, all backups are automatically replicated to the specified region. This provides cross-region data protection and disaster recovery capabilities. It is estimated that approximately 99% of the data can be replicated to the secondary region within an hour.

For more information, see [Turn on dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).

## Point-in-time Restore

Point-in-time Restore is a feature that enables you to restore data of any point in time to a new cluster. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

If you want to perform Point-in-time Restore, note the following:

- For TiDB Cloud Serverless clusters, Point-in-time Restore is available only for scalable clusters and not available for free clusters. For more information, see [Restore mode](/tidb-cloud/backup-and-restore-serverless.md#restore-mode).
- For TiDB Cloud Dedicated clusters, you need to [enable PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore) in advance.
