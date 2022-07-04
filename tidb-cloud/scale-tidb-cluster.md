---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
aliases: ['/tidbcloud/beta/scale-tidb-cluter']
---

# Scale Your TiDB Cluster

> **Note:**
>
> - Currently, you cannot scale a [Developer Tier cluster](/tidb-cloud/select-cluster-tier.md#developer-tier).
> - When a cluster is in the scaling status, you cannot perform any new scaling operations on it.

## Scale a cluster

To scale a cluster, take the following steps:

1. Navigate to **Active Clusters** page and click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, you can make the following changes:

    - TiDB: increase or decrease the node quantity.
    - TiKV: increase the node quantity and storage size.
    - TiFlash<sup>beta</sup>: increase the node quantity and storage size.

5. Click **Confirm**.

## Increase the node size

When a cluster is running, you cannot increase its node size. To make such change, take either of the following methods:

- Method 1: Increase the node size through backup and restore

    You need to [create a latest backup of the cluster](/tidb-cloud/backup-and-restore.md#manual-backup), [delete the cluster](/tidb-cloud/delete-tidb-cluster.md), and then increase the node size when you [restore the deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster). Before taking this method, make sure the following impacts are acceptable:

    - To avoid any data loss during or after the backup, you need to stop the connection to the cluster through your SQL client before creating the backup.
    - After you stop the connection to the cluster, your applications running on this cluster cannot provide service normally until the restoring process is completed.

- Method 2: Increase the node size through a support ticket

    Perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to create a support ticket. For each node to be scaled, provide the following information in the **Description** box of the ticket:

    - Cluster name: xxx
    - Cloud provider: GCP or AWS
    - Node type: TiDB, TiKV, or TiFlash
    - Current node size: xxx
    - Expected node size: xxx

## Scale in a cluster

To make the following scale-in or scale-down changes, you need to submit a support ticket. We will contact you and complete the scaling within the agreed time.

- Decrease the node size of TiDB, TiKV, or TiFlash<sup>beta</sup>
- Scale in TiKV or TiFlash<sup>beta</sup> nodes

> **Warning:**
>
> The preceding scale-down and scale-in changes can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To submit a support request, perform the steps in [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to contact our support team. For each node to be scaled, provide the following information in the **Description** box:

- Cluster name: xxx
- Cloud provider: GCP or AWS
- Node type: TiDB, TiKV, or TiFlash
- Current node size: xxx
- Expected node size: xxx
- Current node number: xxx
- Expected node number: xxx
- Current storage size: xxx
- Expected storage size: xxx