---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
aliases: ['/tidbcloud/beta/scale-tidb-cluter']
---

# Scale Your TiDB Cluster

> **Note:**
>
> - Currently, you cannot scale your [Developer Tier clusters](/cloud/select-cluster-tier.md#developer-tier).
> - When a cluster is in the scaling status, you cannot perform any new scaling operations on it.

On TiDB Cloud, you can easily scale out or scale in your TiDB cluster.

1. Navigate to the TiDB Clusters page and click the name of a cluster that you want to scale. The overview page of the cluster is displayed.
2. In the cluster information pane on the left, click **Setting**.
3. Click **Scale** in the drop-down menu. The **Scale** window is displayed.
4. In the **Scale** window, set the node quantity of your TiDB, TiKV, and TiFlash<sup>beta</sup> respectively by clicking the plus or the minus sign.
5. Click **Confirm**.

> **Warning:**
>
> Scaling in your TiKV nodes and TiFlash<sup>beta</sup> nodes can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To scale in TiKV nodes or TiFlash<sup>beta</sup> nodes, you need to submit a scale-in support ticket. We will contact you and complete the scale-in within the agreed time.

To submit a scale-in request, perform the steps in [TiDB Cloud Support](/cloud/tidb-cloud-support.md) to contact our support team. Note to provide the following information in the **Description** box:

- Current TiKV node number: xxx
- Expected TiKV node number: xxx
- Cloud Provider: GCP or AWS
- Cluster Name: xxx
