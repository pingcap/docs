---
title: Back Up and Restore TiDB Cloud Dedicated Data
summary: Learn how to back up and restore your TiDB Cloud Dedicated cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Cloud Dedicated Data

This document describes how to back up and restore your TiDB Cloud Dedicated cluster data on TiDB Cloud. TiDB Cloud Dedicated supports automatic backup and manual backup. You can also restore backup data to a new cluster or restore a deleted cluster from the recycle bin.

> **Tip**
>
> To learn how to back up and restore data on {{{ .starter }}} or {{{ .essential }}} clusters, see [Back Up and Restore Data on {{{ .starter }}} or Essential](/tidb-cloud/backup-and-restore-serverless.md).

## Limitations

- For clusters of v6.2.0 or later versions, TiDB Cloud Dedicated supports restoring user accounts and SQL bindings from backups by default.
- TiDB Cloud Dedicated does not support restoring system variables stored in the `mysql` schema. 
- It is recommended that you import data first, then perform a **manual** snapshot backup, and finally enable Point-in-time Restore. Because the data imported through the TiDB Cloud console **does not** generate change logs, it cannot be automatically detected and backed up. For more information, see [Import CSV Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md). 
- If you turn on and off Point-in-time Restore multiple times, you can only choose a time point within the recoverable range after the most recent Point-in-time Restore is enabled. The earlier recoverable range is not accessible.
- DO NOT modify the switches of **Point-in-time Restore** and **Dual Region Backup** at the same time.

## Backup

### View the Backup page

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, click the name of your target cluster to go to its overview page.

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
        > - When weekly backup is enabled, the Point-in-time Restore feature is enabled by default and you can disable it manually.
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

### Export backups

To export a specific backup to cloud storage, such as Amazon S3 or Google Cloud Storage, follow the steps for your target storage provider.

> **Note:**
>
> Currently, this feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, fill in "Apply for the export backups feature" in the **Description** field, and then click **Submit**.

<SimpleTab>

<div label="Amazon S3">

To export a backup to Amazon S3, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Locate the backup you want to export, and then click **...** > **Export** in the **Action** column.

3. In the **Export Backup to Amazon S3** dialog, enter the **Folder URI** field, and then select a bucket region for the backup bucket.

4. Click **Generate Command** to view the command for configuring permissions.

    - **With AWS CLI**:

        Execute the generated command on AWS to grant TiDB Cloud access to your Amazon S3 bucket.

    - **With AWS Console**:

        1. Navigate to the [Amazon S3 console](https://console.aws.amazon.com/s3/).
        2. Open the target bucket details page, and then click the **Permissions** tab.
        3. Scroll to **Bucket policy**, and then click **Edit**.
        4. Copy the policy content from the generated command, and then paste it into the policy editor.
        5. Click **Save changes**.

5. Click **Export** to start the export process.

</div>

<div label="Google Cloud Storage">

To export a backup to Google Cloud Storage, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Locate the backup you want to export, and then click **...** > **Export** in the **Action** column.

3. In the **Export Backup to Google Cloud Storage** dialog, note down the **Google Cloud Service Account ID**, which is required for a later step.

4. In the [Google Cloud console](https://console.cloud.google.com/), create a custom IAM role with the following permissions. If you use an existing role, verify that it has these permissions.
    
    - `storage.buckets.get`
    - `storage.objects.list`
    - `storage.objects.create`
    - `storage.objects.delete`

5. Go to **Cloud Storage** > **Buckets**, select the target bucket, and then click **Permissions** > **Grant Access**.

6. In **New principals**, enter the **Service Account ID** from step 3, assign the role from step 4, and then click **Save**.

7. Open the **Configuration** tab, copy the **gsutil URI**, and paste it into the **Export Path** field in the **Export Backup to Google Cloud Storage** dialog. To export to a subdirectory, append a path suffix to the URI.

8. Click **Export** to start the export process.

</div>

</SimpleTab>

### Delete backups

#### Delete backup files

To delete an existing backup file for your TiDB Cloud Dedicated cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Locate the corresponding backup file you want to delete, and click **...** > **Delete** in the **Action** column.

#### Delete a running backup job

To delete a running backup job for your TiDB Cloud Dedicated cluster, follow a process similar to [**Delete backup files**](#delete-backup-files).

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
3. On the **Recycle Bin** page, locate the cluster you want to restore, click **...** in the **Action** column, and then click **Backups**.
4. On the **Backups** page, locate your desired backup time, click **...** in the **Action** column, and then click **Restore**.
5. On the **Restore** page, specify a name for the new cluster, and then make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node number, vCPU and RAM, and storage for the cluster.

6. In the **Summary** section, check the restore information, and then click **Restore**.

   The cluster restore process starts and the **Password Settings** dialog box is displayed.

7. In the **Password Settings** dialog box, set the root password to connect to your cluster, and then click **Save**.

## Export backups

TiDB Cloud Dedicated clusters can export a backup to your own Cloud Object Storage location.

### Export backups to Google Cloud Storage

To export your cluster backups to Google Cloud Storage, take the following steps:

1. Navigate to the **Backup** tab of a cluster deployed on Google Cloud.

2. From the list of backups, identify the backup that you want to export.

3. Click **Export** from the action menu of the identified backup. The export backup window displays.

4. In **Google Cloud Storage Settings**, enter the Folder URI of a Google Cloud Storage location that you want to export the backup into.

    > **Note**
    > - To allow TiDB Cloud to export the backup data to your GCS bucket, you need to configure the GCS access for the bucket. Once the configuration is done for one TiDB cluster in a project, all TiDB clusters in that project and region can access the GCS bucket.

5. If this is the first time exporting a backup to this bucket then configure access by:

   1. Copy the **Google Cloud Service Account ID**
   
   2. Sign in to the [Google Cloud console](https://console.cloud.google.com/).

   3. Go to the [Bucket](https://console.cloud.google.com/storage/browser) page, and click the name of the GCS bucket you want TiDB Cloud to access.

   4. On the **Bucket details** page, click the **PERMISSIONS** tab, and then click **GRANT ACCESS**.

       ![Grant Access to the bucket ](/media/tidb-cloud/gcp-bucket-permissions.png)

   5. Fill in the following information to grant access to your bucket, and then click **SAVE**.

       - In the **New Principals** field, paste the Google Cloud Service Account ID of the target TiDB cluster.
       - In the **Select a role** drop-down list, select the `Storage Legacy Bucket Writer` role.

       > **Note:**
       >
       > To remove the access to TiDB Cloud, you can simply remove the access that you have granted.

   6. On the **Bucket details** page, click the **OBJECTS** tab.

       If you want to copy a folder's gsutil URI, open the folder, and then click the copy button following the folder name to copy the folder name. After that, you need to add `gs://` to the beginning and `/` to the end of the name to get a correct URI of the folder.

       For example, if the folder name is `tidb-cloud-export-data`, you need to use `gs://tidb-cloud-export-data/` as the URI.

       ![Get bucket URI](/media/tidb-cloud/gcp-bucket-uri02.png)
    
    7. In the TiDB Cloud Console click **Export** to begin exporting the backup.

        The backup export process starts and the list of **Exported Backups** is displayed showing the progress.

        To return to the list at any time, click the **Exported Backups** option on the Cluster's **Backup** page.