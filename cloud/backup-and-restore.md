---
title: Back up and Restore TiDB Cluster Data
summary: Learn how to back up and restore your TiDB Cloud cluster.
---

# Back up and Restore TiDB Cluster Data

This document describes how to back up and restore your TiDB cluster data on TiDB Cloud.

## Backup

TiDB Cloud provides two types of data backup: automatic backup and manual backup.

For [Developer Tier clusters](/cloud/select-cluster-tier.md#developer-tier), each cluster allows one automatic backup and two manual backups:

- For automatic backup, if there is an existing backup, it will be replaced by the newer backup.
- For manual backup, if you already have two backups, you need to delete at least one backup before you are able to make another backup.

### Automatic backup

Automatic backups back up the cluster data every day at the backup time you have set. To set the backup time, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Auto Setting**. The setting window displays.

3. In the setting window, select **Backup Time** and maximum backup files in **Limit (backup files)**.

4. Click **Confirm**.

If you do not specify a preferred backup time, TiDB Cloud assigns a default backup time based on each region. The following table lists the default backup time for each region:

| Cloud provider | Region name              | Region          | Default backup time |
|----------------|--------------------------|-----------------|---------------------|
| AWS            | US East (N. Virginia)    | us-east-1       | 07:00 UTC           |
| AWS            | US West (Oregon)         | us-west-2       | 10:00 UTC           |
| AWS            | Asia Pacific (Tokyo)     | ap-northeast-1  | 17:00 UTC           |
| AWS            | Asia Pacific (Seoul)     | ap-northeast-2  | 17:00 UTC           |
| AWS            | Asia Pacific (Singapore) | ap-southeast-1  | 18:00 UTC           |
| AWS            | Europe (Frankfurt)       | eu-central-1    | 03:00 UTC           |
| GCP            | Iowa                     | us-central1     | 08:00 UTC           |
| GCP            | Oregon                   | us-west1        | 10:00 UTC           |
| GCP            | Tokyo                    | asia-northeast1 | 17:00 UTC           |
| GCP            | Singapore                | asia-southeast1 | 18:00 UTC           |

### Manual backup

Manual backups are user-initiated backups that enable you to back up your data to a known state as needed, and then restore to that state at any time.

To apply a manual backup to your TiDB cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Click **Manual** on the upper right.

3. Enter a **Name**.

4. Click **Confirm**. Then your cluster data is backed up.

## Restore

To restore your TiDB cluster data from a backup to a new cluster, perform the following steps:

1. Navigate to the **Backup** tab of a cluster.

2. Select an existing backup in the list, and click **Restore**.

3. In the **Restore** window, enter the cluster **Name** and **Password**.

4. Click **Confirm**.
