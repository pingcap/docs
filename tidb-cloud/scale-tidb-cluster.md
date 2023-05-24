---
title: Scale Your TiDB Cluster
summary: Learn how to scale your TiDB Cloud cluster.
---

# Scale Your TiDB Cluster

> **Note:**
>
> - You cannot scale a [TiDB Serverless cluster](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).
> - When a cluster is in the **MODIFYING** status, you cannot perform any new scaling operations on it.

You can scale a TiDB cluster in the following dimensions:

- Node number of TiDB, TiKV, and TiFlash
- Node storage of TiKV and TiFlash
- Node size (including vCPUs and memory) of TiDB, TiKV, and TiFlash

For information about how to determine the size of your TiDB cluster, see [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md).

> **Note:**
>
> If the node size of TiDB or TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions. To bypass these restrictions, you can [increase your node size](#change-node-size) first.
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiDB can only be used with 2 vCPU TiKV, and 2 vCPU TiKV can only be used with 2 vCPU TiDB.
> - 4 vCPU TiDB can only be used with 4 vCPU TiKV, and 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

## Change node number

You can increase or decrease the number of TiDB, TiKV, or TiFlash nodes.

> **Warning:**
>
> Decreasing TiKV or TiFlash node number can be risky, which might lead to insufficient storage space, excessive CPU usage, or excessive memory usage on remaining nodes.

To change the number of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the number of TiDB, TiKV, or TiFlash nodes.
5. Click **Confirm**.

You can also change the number of TiDB, TiKV, or TiFlash nodes using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Change node storage

You can increase the node storage of TiKV or TiFlash.

> **Warning:**
>
> - For a running cluster, AWS and Google Cloud do not allow in-place storage capacity downgrade.
> - AWS has a cooldown period of node storage changes. If your TiDB cluster is hosted on AWS, after changing the node storage or node size of TiKV or TiFlash, you must wait at least six hours before you can change it again.

To change the node storage of TiKV or TiFlash, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the node storage of TiKV or TiFlash.
5. Click **Confirm**.

You can also change the storage of a TiKV or TiFlash node using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Change node size

You can increase or decrease the size (including vCPUs and memory) of TiDB, TiKV, or TiFlash nodes.

> **Note:**
>
> - Changing node size is only available to the following clusters:
>     - Hosted on AWS and created after 2022/12/31.
>     - Hosted on GCP and created after 2023/04/26.
> - AWS has a cooldown period of node size changes. If your TiDB cluster is hosted on AWS, after changing the node storage or node size of TiKV or TiFlash, you must wait at least six hours before you can change it again.

To change the size of TiDB, TiKV, or TiFlash nodes, take the following steps:

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of the cluster that you want to scale, click **...**.

    > **Tip:**
    >
    > Alternatively, you can also click the name of the cluster that you want to scale on the **Clusters** page and click **...** in the upper-right corner.

3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, change the size of TiDB, TiKV, or TiFlash nodes.
5. Click **Confirm**.

You can also change the size of a TiDB, TiKV, or TiFlash node using TiDB Cloud API through the [Modify a TiDB Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) endpoint. Currently, TiDB Cloud API is still in beta. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).
