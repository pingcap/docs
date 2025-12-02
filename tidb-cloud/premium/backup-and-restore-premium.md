---
title: Back Up and Restore {{{ .premium }}} Data
summary: Learn how to back up and restore your {{{ .premium }}} instances.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore {{{ .premium }}} Data

This document describes how to back up and restore your data on {{{ .premium }}} instances. {{{ .premium }}} supports automatic backup and lets you restore backup data to a new instance as needed.

Backup files can originate from the following sources:

- Active {{{ .premium }}} instances
- The Recycle Bin for backups from deleted Premium instances

> **Tip:**
>
> - To learn how to back up and restore data on {{{ .dedicated }}} clusters, see [Back Up and Restore {{{ .dedicated }}} Data](/tidb-cloud/backup-and-restore.md).
> - To learn how to back up and restore data on {{{ .starter }}} or {{{ .essential }}} clusters, see [Back Up and Restore {{{ .starter }}} or Essential Data](/tidb-cloud/backup-and-restore-serverless.md).

## View the Backup page

1. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your instance data, letting you restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Compared with {{{ .starter }}} clusters and {{{ .essential }}} clusters, {{{ .premium }}} offers enhanced backup capabilities, including longer retention and hourly backup support.

| Backup setting   | {{{ .starter }}} (free) | {{{ .starter }}} (with spending limit > 0) | {{{ .essential }}} | {{{ .premium }}} |
|------------------|--------------------------|---------------------------------------------|--------------------|------------------|
| Backup Cycle     | Daily                    | Daily                                       | Daily              | Daily + Hourly   |
| Backup Retention | 1 day                    | 30 days                                     | 30 days            | Up to 33 days    |
| Backup Time      | Fixed time               | Configurable                               | Configurable       | Configurable     |

- **Backup Cycle** determines how frequently backups are created.

    - Premium instances support both **daily** and **hourly** backups.
    - The **default** is **hourly backups**.

- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

    - Premium instances can retain backups for up to **33 days**.

- **Backup Time** is the scheduled start time for backups.

    - For Premium instances, **daily backups** can be configured to start at a preferred time (in 30-minute intervals), while **hourly backups** always run on the hour.

### Configure the backup settings

To configure backups for a {{{ .premium }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your TiDB instance.

2. Click **Backup Setting**. This will open the **Backup Setting** window, where you can configure automatic backup options.

3. In **Backup Cycle**, choose between the **Hourly Backup** and **Daily Backup** tabs:

    - **Hourly Backup** (default):
        - Runs **on the hour**.
        - You can configure **Backup Retention** (1–33 days).
    - **Daily Backup**:
        - Runs at a configurable time in **30-minute intervals**.
        - You can configure both **Backup Retention** (1–33 days) and **Backup Time**.

4. Click **Save** to save your settings.

### Delete backup files

To delete an existing backup file for your {{{ .premium }}} instance, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Locate the corresponding backup file you want to delete, and click **...** > **Delete** in the **Action** column.

## Restore

TiDB Cloud provides restore functionality to help recover data in case of accidental loss or corruption. You can restore from backups of active instances or from deleted instances in the Recycle Bin.

### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your instance.

- **Snapshot Restore**: restores your instance from a specific backup snapshot.

- **Point-in-Time Restore**: restores your instance to a specific point in time.

    - Premium instances: can be restored to any time within the last 33 days, but not earlier than the instance creation time or later than one minute before the current time.

### Restore destination

TiDB Cloud supports restoring data to a new instance.

### Restore to a new instance

To restore your data to a new instance, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Click **Restore**.

3. On the **Select Backup** page, choose the **Restore Mode** you want to use. You can restore from a specific backup snapshot or restore to a specific point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore from.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time for a Premium instance, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. Click **Next** to proceed to the **Restore to a New Instance** page.

5. Configure your new TiDB instance for restoration. The steps are the same as [creating a new TiDB instance](/tidb-cloud/premium/create-tidb-instance-premium.md).

    > **Note:**
    >
    > The new instance uses the same cloud provider and region as the backup by default.

6. Click **Restore** to start the restore process.

    When the restore process starts, the instance status first changes to **Creating**. After the creation is complete, it changes to **Restoring**. The instance remains unavailable until the restore finishes and the status changes to **Available**.

### Restore from Recycle Bin

To restore a deleted instance from the Recycle Bin, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the top-right corner, click **Recycle Bin**.

2. On the **Recycle Bin** page, locate the TiDB instance you want to restore:

    - Click the **>** button to expand instance details.
    - Find the desired backup, click **...** in the **Action** column, and then select **Restore**.

3. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

### Restore classic backups from a different plan type

Currently, you can only restore classic backups from a TiDB Cloud Dedicated cluster hosted on AWS to a new Premium instance.

To restore a classic backup generated by a TiDB Cloud Dedicated cluster, follow these steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the top-right corner, click **...**, and then click **Restore from Another Plan**.

2. On the **Select Backup** page, select the project that contains the TiDB Cloud Dedicated cluster. Select the cluster, and then select the backup snapshot that you want to restore. Click **Next**.

    > **Note:**
    >
    > - Ensure that the cluster that contains the backup snapshot is either in the **Active** or **Deleted** status within the selected project.
> - The snapshot must be located in a region that Premium supports. If the region is not supported, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to open a new region for Premium, or select another backup snapshot.

3. On the **Restore page**, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

## Limitations

Currently, manual backups are not supported for Premium instances.

