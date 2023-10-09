---
title: Back Up and Restore TiDB Dedicated Data
summary: Learn how to back up and restore your TiDB Dedicated cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Dedicated Data

This document describes how to back up and restore your TiDB Dedicated cluster data on TiDB Cloud. TiDB Dedicated supports both automatic backup and manual backup. Meanwhile, TiDB Dedicated supports two types of data restoration: restore backup data to a new cluster and restore a deleted cluster from the recycle bin.

> **Tip**
>
> To learn how to back up and restore TiDB Serverless cluster data, see [Back Up and Restore TiDB Serverless Data](/tidb-cloud/backup-and-restore-serverless.md).

## Limitations

- TiDB Cloud does not support restoring tables in the `mysql` schema, including user permissions and system variables.

- If you turn on and off Point-in-time Restore (Point-in-time Restore) multiple times, you can only choose a time point within the recoverable range after the most recent Point-in-time Restore is enabled. The earlier recoverable range is not accessible.

## Turn on auto backup

TiDB Dedicated supports both [snapshot backups](https://docs.pingcap.com/tidb/stable/br-snapshot-guide) and [log backups](https://docs.pingcap.com/tidb/stable/br-pitr-guide). Snapshot backup enables users to restore to the the backup point. By default, snapshot backups are taken automatically and stored according to your backup retention policy.

You can disable auto backup at any time.

### Turn on point-in-time restore / log backup

> **Note**
>
> Point-in-time Restore / Log Backup is supported from **TiDB v6.4.0**.

This option enables users to restore to any point in time whithin the backup retention window to a new cluster. It could be used to reduce RPO in disaster recovery, undo mistaken DML, and audit historical business data. It's strongly recommended to turn on this feature. It's charged as same as snpashot backup. For more information, refer to: [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#backup-storage-cost).

To turn on this feature:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Turn the **Auto Backup** switch to **ON**.

4. Turn the **Point-in-time Restore** switch to **ON**.

  > **Warning**
  >
  > - When weekly backup is enabled, point-in-time restore will be enabled by default and cannot be modified.
  > - If the backup schedule is changed from weekly to daily, point-in-time restore remains its original settings. You can manually disable it if needed.
  > - Once point-in-time restore configuration is enabled, **it will only become effective after the completion of the next backup task**. If you want point-in-time restore take effect immediately, you need to manually initiate a backup after configuring it.
  > - 

5. Click **Confirm** to preview the configuration changes.

6. Click **Confirm** again to save changes.

### Configure backup schedule

  > **Warning**
  >
  > - When weekly backup is enabled, point-in-time restore will be enabled by default and cannot be modified.
  > - If the backup schedule is changed from weekly to daily, point-in-time restore remains its original settings. You can manually disable it if needed.

TiDB Dedicated supports two backup schedules: Daily and Weekly. By default, the backup schedule is set to Daily.You can choose a specific time of the day or week to start snapshot backup.

To configure backup schedule:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Under **Backup Schedule**, choose either the **Daily** or **Weekly** option. If you choose **Weekly**, specify the days of the week for the backup.

4. In **Backup Time**, set a start time for the daily or weekly cluster backup. By default, it's a daily backup starting from 2:00 AM in the time zone of the cluster's region.

     > **Note**
     >
     > - Scheduling automatic backup jobs during periods of low workload is recommended to minimize the impact on business operations.
     > - Backup jobs will be automatically delayed when importing data jobs are in progress. Do not run the manual backup during data import jobs or cluster scaling.


5. In **Backup Retention**, configure the minimum backup data retention period. The default is 7 days.

    > **Note**
    >
    > - After you delete the cluster, the automatic backup files will be kept for a specific duration, as set in Backup Settings. Remember to delete these backup files as needed.
    > - After you delete a cluster, the existing manual backup files will be retained until you manually delete them, or your account is closed.

6. Click **Confirm** to preview the configuration change.

7. Click **Confirm** again to save changes.

## Turn on dual region backup

TiDB Dedicated supports dual region backup by copying backups to the new region as selected. After enabling it, all backups will be automatically copied to the specified region, providing an cross region data protection and disaster recovery capabilities. Approximately 99% of the data could be copied to the additional region within 1 hour.

Dual region backup costs include both backup storage usage and cross region data transfer fees. For more information, refer to: [Data Backup Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#backup-storage-cost).

To turn on dual region backup:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Turn the **Dual Region Backup** switch to **ON**.

4. Choose the additional region from the drop box where stores backup data.

5. Click **Confirm** to preview the configuration changes.

6. Click **Confirm** again to save changes.

## Perform a manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB Dedicated cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual Backup**. The setting window displays.

3. Enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

## Delete backups

### Delete backup files

To delete an existing backup file, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that you want to delete.

### Delete a running backup job

To delete a running backup job, it is similar as [**Delete backup files**](#delete-backup-files).

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that is in the **Pending** or **Running** state.

## Restore data to a new cluster

To restore your TiDB Dedicated cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, choose **Restore From Region**, indicating the region of backup stores.

     > **Note**
     >
     > - The default value of the **Restore From Region** is the same as the backup cluster.

4. In **Restore Mode**, choose to restore data of any point in time or a selected backup to a new cluster.

    <SimpleTab>
    <div label="Select Time Point">

    To restore data of any point in time within the backup retention to a new cluster, make sure that **Point-in-time restore** in **Backup Settings** is on and then take the following steps:

    1. Click **Select Time Point**.
    2. Select **Date** and **Time** you want to restore to.

    </div>

    <div label="Select Backup Name">

    To restore a selected backup to the new cluster, take the following steps:

    - Click **Select Backup Name**.
    - Select a backup you want to restore to.

    </div>
    </SimpleTab>

5. In **Restore to Region**, select the same region as the **Backup Storage Region** configured in the **Backup Settings**.

6. In the **Restore** window, you can also make the following changes if necessary:

    - Set the cluster name.
    - Update the port number of the cluster.
    - Increase node number, vCPU and RAM, and storage for the cluster.

7. Click **Restore**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

8. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

## Restore a deleted cluster

To restore a deleted cluster from recycle bin, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Recycle Bin** in the left navigation pane, locate the cluster you want to restore, and then click **Backups** in the **Action** column.
4. Locate your desired backup time, and then click **Restore** in the **Action** column.
5. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node number, vCPU and RAM, and storage for the cluster.

6. Click **Confirm**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

7. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

> **Note:**
>
> You cannot restore a deleted cluster to any point in time. You can only select an automatic or manual backup to restore.


## Turn off auto backup

  > **Note**
  >
  > - Turning off auto backup will also turn off point-in-time restore by default.

To turn off auto backup:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Turn the **Auto Backup** switch to **OFF**.

4. Click **Confirm** to preview the configuration changes.

5. Click **Confirm** again to save changes.

## Turn off dual region backup

  > **Tip**
  >
  > - Disabling dual region backup does not immediately delete the backups in the additional region. They will be cleaned up later according to the backup retention schedule. However, if you want to remove them immediately, you can choose to manually delete the backups.

To turn off dual region backup:

1. Navigate to the **Backup** page of a TiDB Dedicated cluster.

2. Click **Backup Settings**.

3. Turn the **Dual Region Backup** switch to **OFF**.

4. Click **Confirm** to preview the configuration changes.

5. Click **Confirm** again to save changes.