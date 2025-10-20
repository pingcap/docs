---
title: Back Up and Restore Data on Premium
summary: Learn how to back up and restore your Premium instance.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore Data on Premium

This document describes how to back up and restore your data on TiDB Cloud Premium instances. TiDB Cloud Premium supports automatic backup and allows you to restore backup data to a new instance when needed.

Backup files can originate from the following sources:

- Active TiDB Cloud Premium instances
- TiDB Cloud Dedicated clusters
- The recycle bin for backups from deleted Dedicated clusters or Premium instances

> **Tip:**
>
> To learn how to back up and restore data on TiDB Cloud Dedicated clusters, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

> To learn how to back up and restore data on {{{ .starter }}} or {{{ .essential }}} clusters, see [Back Up and Restore Data on {{{ .starter }}} or Essential](/tidb-cloud/backup-and-restore-serverless.md).

## View the Backup page

1. On the [**Instances**](https://tidbcloud.com/project/clusters) page, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your instance data, allowing you to restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Compared with {{{ .starter }}} clusters and {{{ .essential }}} clusters, TiDB Premium offers enhanced backup capabilities, including longer retention and hourly backup support.


| Backup setting   | {{{ .starter }}} (free) | {{{ .starter }}} (with spending limit > 0) | {{{ .essential }}} | {{{ .premium }}} |
|------------------|--------------------------|---------------------------------------------|--------------------|------------------|
| Backup Cycle     | Daily                    | Daily                                       | Daily              | Daily + Hourly   |
| Backup Retention | 1 day                    | 30 days                                     | 30 days            | Up to 33 days    |
| Backup Time      | Fixed time               | Configurable                               | Configurable       | Configurable     |


- **Backup Cycle** determines how frequently backups are created.  

  - Premium instances support both **daily** and **hourly** backups.  
  - **Default** is **hourly backups**.  
 
- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

  - Premium instances can retain backups for up to **33 days**.

- **Backup Time** is the scheduled start time for backups.  

  - For Premium instances, **daily backups** can be configured to start at a preferred time (in 30-minute intervals), while **hourly backups** always run on the hour.

 ### Configure the backup settings

To configure backups for a Premium instance, follow these steps:

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

To delete an existing backup file for your TiDB Cloud Premium , perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Locate the corresponding backup file you want to delete, and click **...** > **Delete** in the **Action** column.

## Restore

TiDB Cloud provides restore functionality to help recover data in case of accidental loss or corruption. You can restore from backups of active instances or from deleted  in the Recycle Bin.


### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your instance.

- **Snapshot Restore**: restores your instance from a specific backup snapshot.

- **Point-in-Time Restore**: restores your instance to a specific point in time.

    - **Premium instances**: can be restored to any time within the past 33 days, but not before the instance creation time or later than one minute before the current time.

### Restore destination

TiDB Cloud supports restoring data to a new instancee.

### Restore to a new instance

> **Note:**
>
> User credentials and permissions from the source instance will **not** be restored to the new instance, You must recreate any users and permissions manually in the new instance.

To restore your data to a new instance, take the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your instance.

2. Click **Restore**.

3. On the **Select a Backup** page, choose the **Restore Mode** you want to use. You can restore from a specific backup snapshot or restore to a specific point in time.

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


4. Click **Next** to proceed to the **Restore to a New TiDB** page.

5. Configure your new TiDB instance for restoration. The steps are the same as [creating a new TiDB instance]()

   - Note: The cloud provider and region for the new instance will match those of the backup.

6. Click **Restore** to start the restore process.


Once the restore process begins, the instance status changes to **Restoring**. The instance will remain unavailable until the restore is complete and the status changes to **Available**.



### Restore from Recycle Bin

To restore a deleted instance from recycle bin, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com),  and then navigate to the [TiDB instance](https://staging.tidbcloud.com/tidbs?orgId=1369847559692509630&uiMode=new-offerings-preview) page. In the top-right corner, click **Recycle Bin**.

2. On the **Recycle Bin** page, locate the TiDB instance you want to restore：
    
    - Click the **>** button to expand instance details.

    - Find the desired backup, click **…** in the **Action** column, and then select **Restore**.

3. On the **Restore** page, follow the same steps as [Restore to a new instance](#restore-to-a-new-instance) to restore the backup to a new instance.





## Limitations

- Manual backups are not supported for Premium instances.


