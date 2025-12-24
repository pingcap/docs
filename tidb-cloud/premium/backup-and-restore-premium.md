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

TiDB Cloud Premium offers enhanced automatic backup capabilities, combining high-frequency snapshots with log backups to ensure maximum data reliability for production environments.

### Automatic Backup Policy Details
TiDB Cloud Premium instances provide a comprehensive data protection strategy through a multi-layered backup architecture:

- **Point-in-Time Recovery (PITR)**
    - Retention: 7 days.
    - Restore Detail: Allows restoration to any specific moment within the 7-day retention period.

- **Hourly Backup Snapshot**
    - Retention: 7 days.
    - Restore Detail: Regular restoration is available for each hourly snapshot generated within the 7-day window.

- **Daily Backup Snapshot**
    - Retention: 33 days.
    - Restore Detail: Restoration is available for daily snapshots (defaulted at 0:00 UTC) for the 33-day retention period.

### Backup Execution Rules
- **Backup Cycle**: Premium instances support both daily and hourly automatic backups.

- **Backup Time**:
    - Daily Backup: Runs at a fixed time of 0:00 UTC. Backup time management/customization is currently not supported.
    - Hourly Backup: Always runs on the hour.

- **Retention Mechanism**: Backups that exceed their retention period (7 days or 33 days) will automatically expire and cannot be restored.

> **Note**:
>
> **Storage Fees**: Storage costs for automatic backups are calculated based on your backup data volume and retention duration.
>
> **Extending Retention**: If you need to extend the backup retention period, contact the TiDB support team.
>
> **Manual Backup**: Manual backup is currently not supported.


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

### Restore backups from a different plan type

Currently, you can only restore backups from a {{{ .dedicated }}} cluster hosted on AWS to a new {{{ .premium }}} instance.

To restore a backup generated by a {{{ .dedicated }}} cluster, follow these steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the upper-right corner, click **...**, and then click **Restore from Another Plan**.

2. On the **Select Backup** page, select the project that contains the target {{{ .dedicated }}} cluster. Select the cluster, select the backup snapshot that you want to restore, and then click **Next**.

    > **Note:**
    >
    > - Ensure that the cluster that contains the backup snapshot is in either the **Active** or **Deleted** status within the selected project.
    > - The snapshot must be located in a region that {{{ .premium }}} supports. If the region is not supported, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to open a new region for {{{ .premium }}}, or select another backup snapshot.

3. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.

### Restore backups from cloud storage

{{{ .premium }}} supports restoring backups from cloud storage (such as Amazon S3 and Alibaba Cloud Object Storage Service (OSS)) to a new instance. This feature is compatible with backups generated from {{{ .dedicated }}} clusters or TiDB Self-Managed clusters.

>**Note:**
>
> - Currently, only backups located in **Amazon S3** and **Alibaba Cloud OSS** are supported.
> - You can restore backups only to a new instance hosted by the same cloud provider as your storage bucket.
> - If the instance and the storage bucket are located in different regions, additional cross-region data transfer fees might apply.

#### Steps

Before you begin, ensure that you have an access key and secret key with sufficient permissions to access the backup files.

To restore backups from cloud storage, follow these steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com), and then navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page. In the upper-right corner, click **...**, and then click **Restore from Cloud Storage**.

2. On the **Select Backup Storage Location** page, provide the following information:

    - **Cloud Provider**: select the cloud provider where your backup files are stored.
    - **Region**: if your cloud provider is Alibaba Cloud OSS, select a region.
    - **Backup Files URI**: enter the URI of the top-level folder that contains your backup files.
    - **Access Key ID**: enter your access key ID.
    - **Access Key Secret**: enter your access key secret.

3. Click **Verify Backup and Next**.

4. If the verification is successful, the **Restore to a New Instance** page appears. Review the backup information displayed at the top of the page, and then follow the steps in [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md) to restore the backup to a new instance.

    If the backup information is incorrect, click **Previous** to return to the previous page, and then enter the correct information.

5. Click **Restore** to restore the backup.

## Limitations

Currently, manual backups are not supported for {{{ .premium }}} instances.
