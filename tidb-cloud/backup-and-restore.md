---
title: Back up and Restore TiDB Cluster Data
summary: Learn how to back up and restore your TiDB Cloud cluster.
aliases: ['/tidbcloud/restore-deleted-tidb-cluster']
---

# Back up and Restore TiDB Cluster Data

This document describes how to back up and restore your TiDB cluster data on TiDB Cloud.

> **Note:**
>
> For [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier), the backup and restore feature is unavailable. You can use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.

## Backup

TiDB Cloud supports automatic backup and manual backup.

Automatic backups are scheduled for your TiDB clusters according to the backup setting, which can reduce your loss in extreme disaster situations. You can also pick a backup snapshot and restore it into a new TiDB cluster at any time.

### Automatic backup

By the automatic backup, you can back up the cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Backup Settings**. The setting window displays.

3. In the setting window,

    - check whether the PITR(**Point-in-time Recovery**) feature is on. To use the PITR feature, firstly make sure your TiDB cluster version is at least v6.3.0 and the TiKV node configuration is at least 8c/16g, then file a ticket to request to enable the PITR feature.

    - In **Backup Time**, schedule a start time for the daily cluster backup. It is recommended to schedule automatic backup at the low workload period. If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time, which is 2:00 AM in the time zone of the region where the cluster is located.

    - In **Backup Retention**, configure the minimum backup data retention period.

    - In **Backup Storage Region**, select the regions where you want to store your backup data. TiDB Cloud stores your backup data in your local region by default. In addition, you can add another remote region, and TiDB Cloud will copy all new backup data to the remote region, which facilitates data safety and faster recovery. After adding a remote region as a backup data store, you can't turn it off.

4. Click **Confirm**.

> **Note that:**
> You can not disable automatic backup.

### Backup storage region support

TiDB Cloud does not yet support adding an arbitrary remote region as backup data storage, the regions already supported are as follows:

| Cloud provider | Region                      | Remote regions support   |
|----------------|-----------------------------|--------------------------|
| GCP            | Tokyo (asia-northeast1)     | Osaka (asia-northeast2)  |

> **Note that:**
> TiDB Cloud will charge you for multiple copies of backup storage based on Backup Storage Region setting, and backup storage price varies by region.
> If you select multiple backup storage regions then you will also incur backup data replication charges.
> See [Data Backup Cost](https://en.pingcap.com/tidb-cloud-pricing-details/#data-backup-cost) for more information.

### Manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual** on the upper right.

3. Enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

### Delete backup files

To delete an existing backup file, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that you want to delete.

### Delete a running backup job

To delete a running backup job, it is similar as [**Delete backup files**](#delete-backup-files).

1. Navigate to the **Backup** tab of a cluster.

2. Click **Delete** for the backup file that is in the **Pending** or **Running** state.

### Best practices for backup

- It is recommended that you perform backup operations at cluster idle time to minimize the impact on business.
- Do not run the manual backup while importing data, or during cluster scaling.
- After you delete a cluster, the existing manual backup files will be retained until you manually delete them, or your account is closed. Automatic backup files will be retained for 7 days from the date of cluster deletion. You need to delete the backup files accordingly.

## Restore

TiDB Cloud provides two types of data restoration:

- Restore backup data to a new cluster
- Restore a deleted cluster from the recycle bin

### Restore data to a new cluster

To restore your TiDB cluster data from a backup to a new cluster, take the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Restore**. The setting window displays.

3. Select **Restore Mode**, you can

    - In **Select Backup Name**, select an existing backup in the backup list.
    - If PITR is enabled, you can click **Select Time Point**, select the point in time you want to recover.

4. In **Restore to Region**, you can select the same region as the **Backup Storage Region** configured in the **Backup Settings**.

5. In the **Restore** window, you can also make the following changes if necessary:

    - Set the cluster name.
    - Update the port number of the cluster.
    - Increase the node size, node quantity, and node storage for the cluster.

6. Click **Restore**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

7. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

### Restore a deleted cluster

To restore a deleted cluster from recycle bin, take the following steps:

1. In the TiDB Cloud console, go to the target project and click the **Recycle Bin** tab.
2. Locate the cluster you want to restore, and then click **Backups** in the **Action** column.
3. Locate your desired backup time, and then click **Restore**.
4. In the **Restore** window, make the following changes if necessary:

    - Update the port number of the cluster.
    - Increase the node size, node quantity, and node storage for the cluster.

5. Click **Confirm**.

   The cluster restore process starts and the **Security Settings** dialog box is displayed.

6. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

> **Note that:** Do PITRin the Recycle Bin is not supported.
