---
title: Back Up and Restore TiDB Cloud Serverless Data
summary: Learn how to back up and restore your TiDB Cloud Serverless cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back Up and Restore TiDB Cloud Serverless Data

This document describes how to back up and restore your TiDB Cloud Serverless cluster data on TiDB Cloud.

> **Tip:**
>
> To learn how to back up and restore TiDB Cloud Dedicated cluster data, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

## Automatic Backups

Automatic backups will back up your cluster data automatically, and you can restore your data from the backup snapshot to reduce your loss in extreme disaster situations.

### Learn about the backup setting

Automatic backups is controlled by the backup setting, which is different for free clusters and scalable clusters:

| backup setting   | free cluster | scalable cluster |
|------------------|--------------|------------------|
| Backup Cycle     | Daily        | Daily            |
| Backup Retention | 1 day        | 14 days          |
| Backup Time      | Fixed time   | Configurable     |

- **Backup Cycle** is the frequency at which backups are taken.

    - Free clusters: the backup cycle is daily.
    - Scalable clusters: the backup cycle is daily.

- **Backup Retention** is the duration for which backups are retained. The expired backups will not be available for restoration.
   
    - Free clusters: the backup retention is 1 day.
    - Scalable clusters: the backup retention is 14 days.

- **Backup Time** is the time when the backup start to be scheduled. Note that the final backup time may fall behind the configured backup time.
   
    - Free clusters: the backup time is a randomly fixed time.
    - Scalable clusters: the backup time can be configured to every half an hour. Default to a randomly fixed time.

### Configure the backup setting

To set the backup time, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Cloud Serverless cluster.

2. Click **Backup Settings**. This will open the **Backup Settings** window, where you can configure the automatic backup settings according to your requirements.

3. In **Backup Time**, schedule a start time for the daily cluster backup.

4. Click **Confirm**.

## Restore

TiDB Cloud Serverless cluster provides restore functionality to help you recover your data in case of accidental data loss or corruption.

### Restore mode

TiDB Cloud Serverless supports snapshot restore and point-in-time restore for your cluster.

- **Snapshot Restore**: Restore your cluster from a specific backup snapshot.

- **Point-in-Time Restore(beta)**: Restore your cluster to a specific time.

    - Free clusters: not supported.
    - Scalable clusters: restore to any time within the last 14 days, but you are not allowed to restore to a time before the cluster creation time or after the current time minus one minute.

### Restore destination

TiDB Cloud Serverless supports restore in-place and restore to a new cluster.

**In-place Restore**

Restore to the current cluster, which will overwrite the existing data. Pay attention to the following points:

- The existing connections will be terminated after the restore is triggered.
- The cluster will be unavailable and any new connection will be blocked during the restore process.
- When a restore is performed, tables in the `mysql` schema are also impacted. Hence, any changes made to user credentials and permissions or system variables will be rolled back to the state when the backup was taken.

**Restore to a New Cluster**

Create and restore to the created new cluster. Pay attention to the following points:

- The user credentials and permissions in the source cluster will not be restored to the new cluster.

### Perform the restore

To restore your TiDB Cloud Serverless cluster, follow these steps:

1. Navigate to the **Backup** page of a cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, you can choose to restore from a specific backup or any point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore to.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. In **Destination**, you can choose to restore in-place or restore to a new cluster.

    <SimpleTab>
    <div label="Restore to a New Cluster">

    To restore a new cluster, take the following steps:

    1. Click **Restore to a New Cluster**.
    2. Enter a name for the new cluster.
    3. Choose the cluster plan for the new cluster.
    4. Set spending limits when your choice is a scalable cluster.
    5. Set the advanced settings as you need when your choice is a scalable cluster.

    </div>
    <div label="Restore to a New Cluster">

    To restore in-place, just click **In-place Restore**.

   </div>
   </SimpleTab>

5. Click **Restore** to begin the restoration process.

After initiating the restore process, the cluster status changes to **Restoring**. The cluster will be unavailable until the restore is complete and cluster status changes to **Available**.

## Limitations

- If any TiFlash replica is enabled, the replica will be unavailable for a while after the restore because data needs to be rebuilt in TiFlash.
- Manual backups are not supported for TiDB Cloud Serverless clusters.
