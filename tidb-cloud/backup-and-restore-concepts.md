---
title: Backup & Restore
summary: Learn about backup & restore concepts for TiDB Cloud.
---

# Backup & Restore

TiDB Cloud Backup & Restore features are designed to safeguard your data and ensure business continuity by enabling you to back up and recover cluster data.

## Automatic backup

For TiDB Cloud Starter clusters, snapshot backups are taken automatically by default and stored according to your backup retention policy.

For more information, see [Automatic backups for TiDB Cloud Starter clusters](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups).

## Point-in-time Restore

Point-in-time Restore is a feature that enables you to restore data of any point in time to a new cluster. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

Note that Point-in-time Restore is available only for TiDB Cloud Starter scalable clusters and not available for free clusters. For more information, see [Restore mode](/tidb-cloud/backup-and-restore-serverless.md#restore-mode).
