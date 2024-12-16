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

## Automatic backups

Automatic backups will back up your cluster data regularly, allowing you to restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Automatic backups is controlled by the backup setting, which is different for free clusters and scalable clusters, as shown in the following table:

| Backup setting   | Free clusters | Scalable clusters |
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

- **Backup Time** is the time when the backup starts to be scheduled. Note that the final backup time might fall behind the configured backup time.
   
    - Free clusters: the backup time is a randomly fixed time.
    - Scalable clusters: you can configure the backup time to every half an hour. The default value is a randomly fixed time.

### Configure the backup setting

To set the backup time, perform the following steps:

1. Navigate to the **Backup** page of a TiDB Cloud Serverless cluster.

2. Click **Backup Settings**. This will open the **Backup Settings** window, where you can configure the automatic backup settings according to your requirements.

3. In **Backup Time**, schedule a start time for the daily cluster backup.

4. Click **Confirm**.

## Restore

TiDB Cloud Serverless clusters offer restore functionality to help recover data in case of accidental loss or corruption.

### Restore mode

TiDB Cloud Serverless supports snapshot restore and point-in-time restore for your cluster.

- **Snapshot Restore**: Restore your cluster from a specific backup snapshot.

- **Point-in-Time Restore(beta)**: Restore your cluster to a specific time.

    - Free clusters: not supported.
    - Scalable clusters: restore to any time within the last 14 days, but not before the cluster creation time or after the current time minus one minute.

### Restore destination

TiDB Cloud Serverless supports restore in-place and restore to a new cluster.

**In-place restore**

Restore to the current cluster will overwrite existing data. Note the following:

- Existing connections will be terminated once the restore is started.
- The cluster will be unavailable, and new connections will be blocked during the restore process.
- Restore will affect tables in the `mysql` schema. Any changes to user credentials, permissions, or system variables will be reverted to their state at the time of the backup.

**Restore to a new cluster**

Create and restore to the new cluster. Note the following:

- User credentials and permissions from the source cluster will not be restored to the new cluster.

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
    <div label="Restore to a new cluster">

    To restore a new cluster, take the following steps:

    1. Click **Restore to a New Cluster**.
    2. Enter a name for the new cluster.
    3. Choose the cluster plan for the new cluster.
    4. Set spending limits when you choose a scalable cluster.
    5. Set the advanced settings as needed when you choose a scalable cluster.

    </div>
    <div label="Restore in-place">

    To restore in-place, click **In-place Restore**.

   </div>
   </SimpleTab>

5. Click **Restore** to begin the restoration process.

After initiating the restore process, the cluster status changes to **Restoring**. The cluster will be unavailable until the restore is complete and cluster status changes to **Available**.

## Limitations

- If a TiFlash replica is enabled, it will be unavailable for a period after the restore, because data needs to be rebuilt in TiFlash.
- Manual backups are not supported for TiDB Cloud Serverless clusters.
