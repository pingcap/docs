---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# Pause or Resume a TiDB Cluster

TiDB Cloud allows you to easily pause and resume a cluster that is not in operation at all times.

Comparing with backup and restore, pausing and resuming a cluster takes less time and keeps your cluster state information (including cluster version, cluster configurations, and TiDB user accounts).

> **Note:**
>
> You cannot pause a [Developer Tier cluster](/tidb-cloud/select-cluster-tier.md#developer-tier). See [Automatic hibernation and resuming] for Developer Tier.

## Prerequisites

<!--- - You cannot pause your cluster if it has any [Changefeeds](/tidb-cloud/changefeed-overview.md). You need to delete the existing Changefeeds ([Delete Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#delete-a-sink) or [Delete Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink)) before pausing the cluster. --->
- You can pause your cluster only when it is in the **Normal** state. If a cluster is in other states such as **Scaling**, you must wait for the current operation to be completed before pausing the cluster.
- You can not pause your cluster if the cluster is being imported, you can either wait for the import task finished or cancel the import task on TiDB Cloud UI.
- You cannot pause your cluster when it is backing up data, you can either wait for the current backup jobs to be completed or [delete the running backup job](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job).

## Pause a TiDB cluster

When a cluster is paused, note the following:

- TiDB Cloud stops collecting monitoring information of the cluster, you cannot read data from or write data to the cluster, and you cannot import or back up data.
- Only the following costs will be charged: 
    - Node Storage Cost
    - Data Backup Cost
    - Data Transfer – Load Balancing

- TiDB Cloud stops [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To pause a cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page of your project.
2. For the cluster that you want to pause, click **...** in the upper-right corner of the cluster area.

    > **Tip:**
    >
    > Alternatively, you can click the name of the cluster that you want to pause on the **Active Clusters** page, and then click **...** in the upper-right corner.

3. Click **Pause** in the drop-down menu.

    The **Pause your cluster** dialog is displayed.

4. In the dialog, click **Pause** to confirm your choice.

## Resume a TiDB cluster

After a paused cluster is resumed, note the following:

- TiDB Cloud resumes collecting the monitoring information of the cluster, and you can read data from or write data to the cluster.
- TiDB Cloud resumes charging both compute and storage costs.
- TiDB Cloud resumes [automatic backup](/tidb-cloud/backup-and-restore.md#automatic-backup) of the cluster.

To resume a paused cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page of your project.
2. For the cluster that you want to resume, click **Resume**.

    The **Resume your cluster** dialog is displayed.

3. In the dialog, click **Resume** to confirm your choice.

Depending on your cluster size, it can take several minutes to resume the cluster. After the cluster is resumed, the cluster state changes from **Resuming** to **Normal**.