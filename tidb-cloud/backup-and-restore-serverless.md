---
title: Back Up and Restore TiDB Cloud Data
summary: Learn how to back up and restore your TiDB Cloud cluster.
---

# Back Up and Restore TiDB Cloud Data

This document describes how to back up and restore your TiDB Cloud cluster data on TiDB Cloud.

## View the Backup page

1. On the [**Clusters**](https://console.tidb.io/project/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Data** > **Backup**.

## Automatic backups

TiDB Cloud automatically backs up your cluster data, allowing you to restore data from a backup snapshot to minimize data loss in the event of a disaster.

### Learn about the backup setting

Automatic backup settings vary between Starter clusters and Essential clusters, as shown in the following table:

| Backup setting   | Starter clusters | Essential clusters |
|------------------|--------------|------------------|
| Backup Cycle     | Daily        | Daily            |
| Backup Retention | 1 day        | 14 days          |
| Backup Time      | Fixed time   | Configurable     |

- **Backup Cycle** is the frequency at which backups are taken.

- **Backup Retention** is the duration for which backups are retained. Expired backups cannot be restored.

- **Backup Time** is the time when the backup starts to be scheduled. Note that the final backup time might fall behind the configured backup time.

    - Starter clusters: the backup time is a randomly fixed time.
    - Essential clusters: you can configure the backup time to every half an hour. The default value is a randomly fixed time.

### Configure the backup setting

To set the backup time for an Essential cluster, perform the following steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Backup Setting**. This will open the **Backup Setting** window, where you can configure the automatic backup settings according to your requirements.

3. In **Backup Time**, schedule a start time for the daily cluster backup.

4. Click **Confirm**.

## Restore

TiDB Cloud clusters offer restore functionality to help recover data in case of accidental loss or corruption.

### Restore mode

TiDB Cloud supports snapshot restore and point-in-time restore for your cluster.

- **Snapshot Restore**: restores your cluster from a specific backup snapshot.

- **Point-in-Time Restore (beta)**: restores your cluster to a specific time.

    - Starter clusters: not supported.
    - Essential clusters: restores to any time within the last 14 days, but not before the cluster creation time or after the current time minus one minute.

### Restore destination

TiDB Cloud supports restoring in-place and restoring to a new cluster.

**In-place restore**

Restore to the current cluster will overwrite existing data. Note the following:

- Existing connections will be terminated once the restore is started.
- The cluster will be unavailable, and new connections will be blocked during the restore process.
- Restore will affect tables in the `mysql` schema. Any changes to user credentials, permissions, or system variables will be reverted to their state at the backup time.

**Restore to a new cluster**

Create and restore to the new cluster. Note the following:

- User credentials and permissions from the source cluster will not be restored to the new cluster.

### Restore timeout

The restore process typically completes within a few minutes. If the restore takes longer than three hours, it is automatically canceled. The outcome of a canceled restore depends on the destination:

- **In-place restore**: the cluster status changes from **Restoring** to **Available**, and the cluster becomes accessible.
- **Restore to a new cluster**: the new cluster is deleted and the source cluster remains unchanged.

If the data is corrupted after a canceled restore and cannot be recovered, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance.

### Perform the restore

To restore your TiDB Cloud cluster, follow these steps:

1. Navigate to the [**Backup**](#view-the-backup-page) page of your cluster.

2. Click **Restore**. The setting window displays.

3. In **Restore Mode**, you can choose to restore from a specific backup or any point in time.

    <SimpleTab>
    <div label="Snapshot Restore">

    To restore from a selected backup snapshot, take the following steps:

    1. Click **Snapshot Restore**.
    2. Select the backup snapshot you want to restore from.

    </div>
    <div label="Point-in-Time Restore">

    To restore to a specific point in time for an Essential cluster, take the following steps:

    1. Click **Point-in-Time Restore**.
    2. Select the date and time you want to restore to.

    </div>
    </SimpleTab>

4. In **Destination**, you can choose to restore to a new cluster or restore in-place.

    <SimpleTab>
    <div label="Restore to a new cluster">

    To restore to a new cluster, take the following steps:

    1. Click **Restore to a New Cluster**.
    2. Enter a name for the new cluster.
    3. Choose the cluster plan for the new cluster.

        - If you choose a Starter cluster, set a monthly spending limit.
        - If you choose an Essential cluster, set the minimum RCU and maximum RCU, and then configure advanced settings as needed.

    </div>
    <div label="Restore in-place">

    To restore in-place, click **In-place Restore**.

    </div>
    </SimpleTab>

5. Click **Restore** to begin the restore process.

Once the restore process begins, the cluster status changes to **Restoring**. The cluster will remain unavailable until the restore is complete and the status changes to **Available**.

## Limitations

- If a TiFlash replica is enabled, it will be unavailable for a period after the restore, because the data needs to be rebuilt in TiFlash.
- Clusters with more than 1 TiB of data do not support restoring to new clusters by default. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance with larger datasets.
