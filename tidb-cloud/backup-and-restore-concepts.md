---
title: Backup & Restore
summary: Learn about backup & restore concepts for TiDB Cloud.
---

# Backup & Restore

TiDB Cloud Backup & Restore features are designed to safeguard your data and ensure business continuity by enabling you to back up and recover data.

<CustomContent plan="byoc">

For TiDB Cloud BYOC, you can manage backup and restore operations through the TiDB Cloud console, while the data plane runs in your own cloud account. This allows you to use managed backup and restore workflows while keeping the BYOC data plane within your cloud environment.

</CustomContent>

## Automatic backup

In TiDB Cloud, snapshot backups are taken automatically by default and stored according to your backup retention policy.

For more information, see the following:

- [Automatic backups for {{{ .starter }}} and {{{ .essential }}} instances](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [Automatic backups for {{{ .premium }}}  <CustomContent plan="byoc"> and {{{ .byoc}}} </CustomContent> instances](/tidb-cloud/premium/backup-and-restore-premium.md#automatic-backups)
- [Automatic backups for TiDB Cloud Dedicated clusters](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## Manual backup

Manual backup enables you to back up your data to a known state as needed, and then restore to that state at any time. You can use a manual backup before high-risk operations such as system upgrades, critical data deletion, or irreversible schema changes.

{{{ .premium }}} <CustomContent plan="byoc">, {{{ .byoc}}} </CustomContent> and TiDB Cloud Dedicated support manual backups.  A manual backup provides a controlled restore point and is retained until you explicitly delete it. Manual backups do not support PITR or partial backups, and each restore operation creates a new instance.


For more information, see the following:

- [Manual backups for {{{ .premium }}} <CustomContent plan="byoc"> and {{{ .byoc}}} </CustomContent> instances](/tidb-cloud/premium/backup-and-restore-premium.md#manual-backups)
- [Perform a manual backup for TiDB Cloud Dedicated clusters](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)

## Dual region backup

Dual region backup is a feature of TiDB Cloud Dedicated that enables you to replicate backups from your cluster region to another different region. After it is enabled, all backups are automatically replicated to the specified region. This provides cross-region data protection and disaster recovery capabilities. It is estimated that approximately 99% of the data can be replicated to the secondary region within an hour.

For more information, see [Turn on dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).

## Point-in-time Restore

Point-in-time Restore is a feature that enables you to restore data of any point in time to a new TiDB cluster or instance. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

If you want to perform Point-in-time Restore, note the following:

- For {{{ .starter }}} instances, Point-in-time Restore is not available.
- For {{{ .essential }}} instances, you can restore to any time within the last 30 days. For more information, see [Restore mode](/tidb-cloud/backup-and-restore-serverless.md#restore-mode).
- For TiDB Cloud Dedicated clusters, you need to [enable PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore) in advance.

## Restore

TiDB Cloud supports restoring data from backup snapshots or point-in-time recovery to a new cluster or instance. Restore operations help you recover from accidental data loss, data corruption, or application errors.

For {{{ .premium }}}  <CustomContent plan="byoc"> and {{{ .byoc}}} </CustomContent> instances, you can restore data to a new instance. You can restore from automatic backups, manual backups, or supported external cloud storage backups. PITR is supported only for automatic backups and is not supported for manual backups.

