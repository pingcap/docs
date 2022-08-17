---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# Pause or Resume a TiDB Cluster

TiDB Cloud allows you to easily pause and resume a cluster that is not in operation at all times.

Comparing with backup and restore, pausing and resuming a cluster takes less time and keeps your cluster state information (including cluster version, cluster configuration, and TiDB user accounts).

> **Note:**
>
> Currently, you cannot pause a [Developer Tier cluster](/tidb-cloud/select-cluster-tier.md#developer-tier). Once a Developer Tier cluster remains idle for 24 hours, the cluster hibernates automatically and you can resume it by [connecting to your cluster](/tidb-cloud/connect-to-tidb-cluster.md) or clicking **Resume** for the cluster in the TiDB Cloud console.

## Limitation

- You cannot pause your cluster if the cluster has any [Changefeeds](/tidb-cloud/changefeed-overview.md). You need to delete existing Changefeeds (delete [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) or Delete [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)) before pausing the cluster.
- You cannot pause your cluster if the cluster is backing up data, you can either wait for the current backup jobs to be completed or [delete the running backup job](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job).

## Pause a TiDB cluster

> **Note:**
>
> You can only pause a cluster that is in the **Normal** state. If a cluster is in other states such as **Importing** or **Scaling**, you must wait for the current operation to be completed before pausing the cluster.

When a cluster is paused:

- TiDB Cloud stops collecting the monitoring information of the cluster, and you cannot read data from or write data to the cluster.
- TiDB Cloud only charges the cluster for storage cost and does not charge for any other costs.
- TiDB Cloud stops [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To pause a cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page for your project.
2. For the cluster you want to pause, click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to pause on the **Active Clusters** page and click **...** in the upper-right corner.

3. Click **Pause** in the drop-down menu.
4. Click **Pause** to confirm your choice.

Depending on your cluster size, it can take up to xxx minutes for the cluster to go to the **Paused** state.

## Resume a TiDB cluster

After a paused cluster is resumed:

- TiDB Cloud resumes collecting the monitoring information of the cluster, and you can read data from or write data to the cluster.
- TiDB Cloud resumes charging both compute and storage costs.
- TiDB Cloud resumes [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To resume a paused cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page for your project.
2. For the cluster you want to resume, click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to resume on the **Active Clusters** page and click **...** in the upper-right corner.

3. Click **Resume** in the drop-down menu.
4. Click **Resume** to confirm your choice.

Depending on your cluster size, it can take several minutes to resume the cluster. After the cluster is resumed, the cluster state changes to **Normal**.