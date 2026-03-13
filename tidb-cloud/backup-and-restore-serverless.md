---
title: Back Up and Restore {{{ .starter }}} or Essential Data
summary: Learn how to back up and restore your {{{ .starter }}} or {{{ .essential }}} instances.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore {{{ .starter }}} or Essential Data

This document describes how to back up and restore your data on {{{ .starter }}} or {{{ .essential }}} instances.

> **Tip:**
>
> To learn how to back up and restore data on TiDB Cloud Dedicated clusters, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

## View the Backup page

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and resources.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your data, allowing you to restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Automatic backup settings vary between {{{ .starter }}} instances and {{{ .essential }}} instances, as shown in the following table:

| Backup setting   | {{{ .starter }}} (free) | {{{ .starter }}} (with spending limit > 0) | {{{ .essential }}} |
|------------------|----------------------------|----------------------------|----------------------------|
| Backup Cycle     | Daily                      | Daily                      | Daily                      |
| Backup Retention | 1 day                      | Up to 30 days              | Up to 30 days              |
| Backup Time      | Fixed time                 | Configurable               | Configurable               |

- **Backup Cycle** is the frequency at which backups are taken.

- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

    - For a free {{{ .starter }}} instance, the backup retention is 1 day.
    - For a {{{ .starter }}} (with spending limit > 0) or {{{ .essential }}} instance, you can configure the backup retention to any value between 1 and 30 days. The default retention is 14 days.

- **Backup Time** is the time when the backup starts to be scheduled. Note that the final backup time might fall behind the configured backup time.

    - For a free {{{ .starter }}} instance, the backup time is a randomly fixed time.
    - For a {{{ .starter }}} (with spending limit > 0) or {{{ .essential }}} instance, you can configure the backup time to every half an hour. The default value is a randomly fixed time.

### Configure the backup setting

To set the backup time for a {{{ .essential }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .starter }}} or Essential instance.

2. Click **Backup Setting**. This will open the **Backup Setting** window, where you can configure the automatic backup settings according to your requirements.

3. In **Backup Time**, schedule a start time for the daily backup.

4. Click **Confirm**.

## Restore

TiDB Cloud offer restore functionality to help recover data in case of accidental loss or corruption.

### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your {{{ .starter }}} or Essential instance.

- **Snapshot Restore**: restores your {{{ .starter }}} or Essential instance from a specific backup snapshot.

- **Point-in-Time Restore (beta)**: restores your {{{ .essential }}} instance to a specific time.

    - {{{ .starter }}} instances: not supported.
    - {{{ .essential }}} instances: restores to any time within the backup retention, but not earlier than the {{{ .essential }}} instance creation time or later than one minute before the current time.

### Restore destination

TiDB Cloud supports restoring data to a new {{{ .starter }}} or Essential instance.

### Restore timeout

The restore process typically completes within a few minutes. If the restore takes longer than three hours, it is automatically canceled and the new {{{ .starter }}} or Essential instance is deleted, while the source instance remains unchanged.

If the data is corrupted after a canceled restore and cannot be recovered, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance.

### Perform the restore

> **Note:**
>
> User credentials and permissions from the source {{{ .starter }}} or Essential instance will not be restored to the new {{{ .starter }}} or Essential instance.

To restore your data to a new {{{ .starter }}} or Essential instance, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your {{{ .starter }}} or Essential instance.

2. Click **Restore**.

3. In **Restore Mode**, you can choose to restore from a specific backup or any point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore from.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time for a {{{ .essential }}} instance, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. Enter a name for the new instance.
5. Choose a plan for the new instance and update the capacity as needed.

    - If you choose a {{{ .starter }}} instance and need more resources than the [free quota](/tidb-cloud/select-cluster-tier.md#usage-quota), set a monthly spending limit.
    - If you choose a {{{ .essential }}} instance, set the minimum RCU and maximum RCU, and then configure advanced settings as needed.

6. Click **Restore** to begin the restore process.

Once the restore process begins, the {{{ .starter }}} or Essential instance status changes to **Restoring**. The {{{ .starter }}} or Essential instance will remain unavailable until the restore is complete and the status changes to **Available**.

## Limitations

- If a TiFlash replica is enabled, it will be unavailable for a period after the restore, because the data needs to be rebuilt in TiFlash.
- Manual backups are not supported for {{{ .starter }}} and {{{ .essential }}} instances.
- A {{{ .starter }}} or {{{ .essential }}} instance with more than 1 TiB of data does not support restoring to a new instance by default. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance with larger datasets.
