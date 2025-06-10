---
title: Back Up and Restore TiDB Cloud Dedicated Data
summary: Learn how to back up and restore your TiDB Cloud Dedicated cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Cloud Dedicated Data

This document describes how to back up and restore your TiDB Cloud Dedicated cluster data on TiDB Cloud. TiDB Cloud Dedicated supports automatic backup and manual backup. You can also restore backup data to a new cluster or restore a deleted cluster from the recycle bin.

> **Tip**
>
> To learn how to back up and restore TiDB Cloud Serverless cluster data, see [Back Up and Restore TiDB Cloud Serverless Data](/tidb-cloud/backup-and-restore-serverless.md).

## Limitations

- For clusters of v6.2.0 or later versions, TiDB Cloud Dedicated supports restoring user accounts and SQL bindings from backups by default.
- TiDB Cloud Dedicated does not support restoring system variables stored in the `mysql` schema. 
- It is recommended that you import data first, then perform a **manual** snapshot backup, and finally enable Point-in-time Restore. Because the data imported through the TiDB Cloud console **does not** generate change logs, it cannot be automatically detected and backed up. For more information, see [Import CSV Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md). 
- If you turn on and off Point-in-time Restore multiple times, you can only choose a time point within the recoverable range after the most recent Point-in-time Restore is enabled. The earlier recoverable range is not accessible.
- DO NOT modify the switches of **Point-in-time Restore** and **Dual Region Backup** at the same time.

## Backup

### View the Backup page

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Data** > **Backup**.

### Turn on auto backup

TiDB Cloud Dedicated supports both [snapshot backup](https://docs.pingcap.com/tidb/stable/br-snapshot-guide) and [log backup](https://docs.pingcap.com/tidb/stable/br-pitr-guide). Snapshot backup enables you to restore data to the backup point. By default, snapshot backups are taken automatically and stored according to your backup retention policy. You can disable auto backup at any time.

#### Turn on Point-in-time Restore

> **Note**
>
> The Point-in-time Restore feature is supported for TiDB Cloud Dedicated clusters that are v6.4.0 or later.

This feature supports restoring data of any point in time to a new cluster. You can use it to:

- Reduce RPO in disaster recovery.
- Resolve cases of data write errors by restoring point-in-time that is before the error event.
- Audit the historical data of the business.

It is strongly recommended to turn on this feature. The cost is the same as snapshot backup. For more information, refer to [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost).

To turn on this feature for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**.

3. Toggle the **Auto Backup** switch to **On**.

4. Toggle the **Point-in-time Restore** switch to **On**.

    > **Warning**
    >
    > Point-in-Time Restore only takes effect after the next backup task is completed. To make it take effect earlier, you can [manually perform a backup](#perform-a-manual-backup) after enabling it.

5. Click **Save** to save changes.

#### Configure backup schedule

TiDB Cloud Dedicated supports daily and weekly backup schedules. By default, the backup schedule is set to daily. You can choose a specific time of the day or week to start snapshot backup.

To configure the backup schedule for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**.

3. Toggle the **Auto Backup** switch to **On**.

4. Configure the backup schedule as follows:

    - In **Backup Cycle**, click either the **Daily Backup** or **Weekly Backup** tab. For **Weekly Backup**, you need to specify the days of the week for the backup.

        > **Warning**
        >
        > - When weekly backup is enabled, the Point-in-time Restore feature is enabled by default and cannot be disabled.
        > - If you change the backup cycle from weekly to daily, the Point-in-time Restore feature remains its original setting. You can manually disable it if needed.

    - In **Backup Time**, schedule a start time for the daily or weekly cluster backup.

        If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

        > **Note**
        >
        > - Backup jobs are automatically delayed when data import jobs are in progress. **DO NOT** run manual backups during data import or cluster scaling.

    - In **Backup Retention**, configure the minimum backup data retention period. The default period is 7 days. To minimize the impact on business, it is recommended to schedule automatic backup during periods of low workloads.

        > **Note**
        >
        > - All auto-backups, except the latest one, will be deleted if their lifetime exceeds the retention period. The latest auto-backup will not be deleted unless you delete it manually. This ensures that you can restore cluster data if accidental deletion occurs.
        > - After you delete a cluster, auto-backups with a lifetime within the retention period will be moved to the recycle bin.

### Turn on dual region backup

> **Note:**
>
> - Currently, the dual region backup feature is only available for clusters hosted on AWS and Google Cloud.
> - TiDB Cloud Dedicated clusters hosted on Google Cloud work seamlessly with Google Cloud Storage. Similar to Google Cloud Storage, **TiDB Cloud Dedicated supports dual-region pairing only within the same multi-region code as Google dual-region storage**. For example, in Asia, currently you must pair Tokyo and Osaka together for dual-region storage. For more information, refer to [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr).

TiDB Cloud Dedicated supports dual region backup by replicating backups from your cluster region to another different region. After you enable this feature, all backups are automatically replicated to the specified region. This provides cross-region data protection and disaster recovery capabilities. It is estimated that approximately 99% of the data can be replicated to the secondary region within an hour.

Dual region backup costs include both backup storage usage and cross-region data transfer fees. For more information, refer to [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details#backup-storage-cost).

To turn on dual region backup for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**.

3. Toggle the **Dual Region Backup** switch to **On**.

4. From the **Secondary Region** drop-down list, select a region to store the backup files.

5. Click **Save** to save changes.

### Turn off auto backup

> **Note**
>
> Turning off auto backup will also turn off point-in-time restore by default.

To turn off auto backup for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**.

3. Toggle the **Auto Backup** switch to **Off**.

4. Click **Save** to save changes.

### Turn off dual region backup

> **Tip**
>
> Disabling dual region backup does not immediately delete the backups in the secondary region. These backups will be cleaned up later according to the backup retention schedule. To remove them immediately, you can manually [delete the backups](#delete-backups).

To turn off dual region backup for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**.

3. Toggle the **Dual Region Backup** switch to **Off**.

4. Click **Save** to save changes.

### Perform a manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

> **Note**
>
> - Manual backups are retained indefinitely until you choose to delete them manually or your account is closed.
> - After a TiDB Cloud Dedicated cluster is deleted, its existing manual backups will be moved to the recycle bin and kept there until manually deleted or your account is closed.

To apply a manual backup to your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. In the upper-right corner, click **...** > **Manual Backup**. 

3. In the displayed dialog, enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

### Delete backups

#### Delete backup files

To delete an existing backup file for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Locate the corresponding backup file you want to delete, and click **...** > **Delete** in the **Action** column.

#### Delete a running backup job

To delete a running backup job for your TiDB Cloud Dedicated cluster, it is similar as [**Delete backup files**](#delete-backup-files).

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Locate the running backup job that is in the **Pending** or **Running** state, and click **...** > **Delete** in the **Action** column.

## Restore

### Restore data to a new cluster

> **Note**
>
> When you restore a TiDB cluster from backups, the restore process retains the original time zone setting without overwriting it.

To restore your TiDB Cloud Dedicated cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, choose **Restore From Region**, indicating the region of backup stores.

    > **Note**
    >
    > - The default value of the **Restore From Region** is the same as the backup cluster.

4. In **Restore Mode**, choose to restore data of any point in time or a selected backup to a new cluster.

    <SimpleTab>
    <div label="Select Time Point">

    To restore data of any point in time within the backup retention to a new cluster, make sure that **Point-in-time Restore** in **Backup Setting** is on and then take the following steps:

    - Click **Select Time Point**.
    - Select **Date** and **Time** you want to restore to.

    </div>

    <div label="Select Backup Name">

    To restore a selected backup to the new cluster, take the following steps:

    - Click **Select Backup Name**.
    - Select a backup you want to restore to.

    </div>
    </SimpleTab>

5. In **Restore to Region**, select the same region as the **Primary Region** configured in the **Backup Setting**.

6. In the **Restore** window, you can also make the following changes if necessary:

    - Set the cluster name.
    - Update the port number of the cluster.
    - Increase node number, vCPU and RAM, and storage for the cluster.

7. Click **Restore**.

   The cluster restore process starts and the **Password Settings** dialog box is displayed.

8. In the **Password Settings** dialog box, set the root password to connect to your cluster, and then click **Save**.

### Restore a deleted cluster

> **Note:**
>
> You cannot restore a deleted cluster to any point in time. You can only select an automatic or manual backup to restore.

To restore a deleted cluster from recycle bin, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Recycle Bin**.
3. On the **Recycle Bin** page, locate the cluster you want to restore, and then click **Backups** in the **Action** column.
4. Locate your desired backup time, and then click **Restore** in the **Action** column.
5. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node number, vCPU and RAM, and storage for the cluster.

6. Click **Confirm**.

   The cluster restore process starts and the **Password Settings** dialog box is displayed.

7. In the **Password Settings** dialog box, set the root password to connect to your cluster, and then click **Save**.
