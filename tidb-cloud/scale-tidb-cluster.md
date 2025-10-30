---
title: 扩容你的 TiDB 集群
summary: 了解如何扩容你的 TiDB Cloud 集群。
---

# 扩容你的 TiDB 集群

> **Note:**
>
> - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 会根据你的应用负载变化自动扩缩容。但你无法手动扩缩容 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
> - 当集群处于 **MODIFYING** 状态时，你无法对其执行任何新的扩缩容操作。

你可以从以下维度扩容 TiDB 集群：

- TiDB、TiKV 和 TiFlash 的节点数量
- TiDB、TiKV 和 TiFlash 的 vCPU 及内存（RAM）
- TiKV 和 TiFlash 的存储空间

关于如何确定你的 TiDB 集群规格，参见 [确定你的 TiDB 集群规格](/tidb-cloud/size-your-cluster.md)。

> **Note:**
>
> 如果 TiDB 或 TiKV 的 vCPU 和内存规格设置为 **4 vCPU, 16 GiB**，请注意以下限制。要绕过这些限制，你可以先[调整 vCPU 和内存](#change-vcpu-and-ram)。
>
> - TiDB 的节点数量只能设置为 1 或 2，TiKV 的节点数量固定为 3。
> - 4 vCPU 的 TiDB 只能与 4 vCPU 的 TiKV 搭配使用，4 vCPU 的 TiKV 也只能与 4 vCPU 的 TiDB 搭配使用。
> - TiFlash 不可用。

## 更改节点数量

你可以增加或减少 TiDB、TiKV 或 TiFlash 的节点数量。

> **Warning:**
>
> 减少 TiKV 或 TiFlash 节点数量存在风险，可能导致剩余节点的存储空间不足、CPU 使用率过高或内存使用率过高。

要更改 TiDB、TiKV 或 TiFlash 的节点数量，请按照以下步骤操作：

1. 在 TiDB Cloud 控制台，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要扩容的集群所在行，点击 **...**。

    > **Tip:**
    >
    > 你也可以在 **Clusters** 页面点击你想要扩容的集群名称，然后在右上角点击 **...**。

3. 在下拉菜单中点击 **Modify**，进入 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，修改 TiDB、TiKV 或 TiFlash 的节点数量。
5. 在右侧面板确认集群规格，然后点击 **Confirm**。

你也可以通过 TiDB Cloud API，使用 [Modify a TiDB Cloud Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 接口更改 TiDB、TiKV 或 TiFlash 的节点数量。目前，TiDB Cloud API 仍处于 beta 阶段。更多信息，参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 更改 vCPU 和内存

你可以增加或减少 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。

> **Note:**
>
> - 仅以下集群支持更改 vCPU 和内存：
>     - 部署在 AWS 上且创建时间为 2022/12/31 之后。
>     - 部署在 Google Cloud 上且创建时间为 2023/04/26 之后。
>     - 部署在 Azure 上。
> - AWS 对 vCPU 和内存的更改有冷却时间。如果你的 TiDB 集群部署在 AWS 上，在更改 TiKV 或 TiFlash 的 vCPU 和内存后，必须等待至少 6 小时才能再次更改。
> - 在减少 vCPU 之前，请确保 TiKV 或 TiFlash 当前节点的存储空间不超过目标 vCPU 的最大节点存储。详情参见 [TiKV 节点存储](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size) 和 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。如果任一组件当前存储超过其限制，则无法减少 vCPU。

要更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存，请按照以下步骤操作：

1. 在 TiDB Cloud 控制台，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要扩容的集群所在行，点击 **...**。

    > **Tip:**
    >
    > 你也可以在 **Clusters** 页面点击你想要扩容的集群名称，然后在右上角点击 **...**。

3. 在下拉菜单中点击 **Modify**，进入 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，修改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。
5. 在右侧面板确认集群规格，然后点击 **Confirm**。

你也可以通过 TiDB Cloud API，使用 [Modify a TiDB Cloud Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 接口更改 TiDB、TiKV 或 TiFlash 节点的 vCPU 和内存。目前，TiDB Cloud API 仍处于 beta 阶段。更多信息，参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

## 更改存储空间

你可以增加 TiKV 或 TiFlash 的存储空间。

> **Warning:**
>
> - 对于运行中的集群，AWS、Azure 和 Google Cloud 不支持原地降低存储容量。
> - AWS 和 Azure 对存储空间的更改有冷却时间。如果你的 TiDB 集群部署在 AWS 或 Azure 上，在更改 TiKV 或 TiFlash 的存储空间或 vCPU 和内存后，必须等待至少 6 小时才能再次更改。

要更改 TiKV 或 TiFlash 的存储空间，请按照以下步骤操作：

1. 在 TiDB Cloud 控制台，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要扩容的集群所在行，点击 **...**。

    > **Tip:**
    >
    > 你也可以在 **Clusters** 页面点击你想要扩容的集群名称，然后在右上角点击 **...**。

3. 在下拉菜单中点击 **Modify**，进入 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，修改每个 TiKV 或 TiFlash 节点的存储空间。
5. 在右侧面板确认集群规格，然后点击 **Confirm**。

你也可以通过 TiDB Cloud API，使用 [Modify a TiDB Cloud Dedicated cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 接口更改 TiKV 或 TiFlash 节点的存储空间。目前，TiDB Cloud API 仍处于 beta 阶段。更多信息，参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。