---
title: 管理 TiProxy
summary: 了解如何启用、禁用、查看和修改 TiProxy。
---

# 管理 TiProxy

本文档介绍如何启用、禁用、查看和修改 TiProxy。

> **注意：**
>
> TiProxy 目前处于 beta 阶段，仅适用于部署在 AWS 上的 TiDB Cloud Dedicated 集群。

## 启用 TiProxy

你可以在任何 TiDB 节点组中为新集群或现有集群启用 TiProxy。

### 决定 TiProxy 节点的规格和数量

TiProxy 节点的规格和数量取决于集群的 QPS 和网络带宽。网络带宽是客户端请求和 TiDB 响应带宽的总和。

下表展示了每种 TiProxy 规格的最大 QPS 和网络带宽。

| 规格  | 最大 QPS | 最大网络带宽         |
| :---- | :------- | :------------------- |
| Small | 30K      | 93 MiB/s             |
| Large | 120K     | 312 MiB/s            |

可用的 TiProxy 规格为 `Small` 和 `Large`。可用的 TiProxy 节点数量为 2、3、6、9、12、15、18、21 和 24。默认的两个 Small 规格 TiProxy 节点可提供 60K QPS 和 186 MiB/s 网络带宽。建议预留 20% 的 QPS 容量以防止高延时。

例如，如果你的集群最大 QPS 为 100K，最大网络带宽为 100 MiB/s，则 TiProxy 节点的规格和数量主要取决于 QPS。在这种情况下，你可以选择 6 个 Small 规格的 TiProxy 节点。

### 为新集群启用 TiProxy

在创建新集群时启用 TiProxy，点击 TiProxy 开关并选择 TiProxy 的规格和数量。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 为现有集群启用 TiProxy

> **注意：**
>
> 启用 TiProxy 会导致对应 TiDB 节点组中的 TiDB 节点滚动重启，重启期间会断开现有连接。此外，创建新连接可能会假死最长 30 秒。请确保在维护窗口内启用 TiProxy。

为现有集群启用 TiProxy，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **...**，在下拉菜单中点击 **Modify**。此时会显示 **Modify Cluster** 页面。
3. 在 **Modify Cluster** 页面，点击 TiProxy 开关并选择 TiProxy 的规格和数量。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 限制与配额

- 每个 TiDB 节点组中至少需要有两个 TiDB 节点。
- TiDB 节点规格至少为 4 vCPU。
- 组织中 TiProxy 节点的默认最大数量为 `10`。更多信息参见 [Limitations and Quotas](/tidb-cloud/limitations-and-quotas.md)。
- TiDB 集群的版本必须为 v6.5.0 或更高。

## 禁用 TiProxy

> **注意：**
>
> 禁用 TiProxy 会导致连接断开。此外，创建新连接可能会假死最长 10 秒。请确保在维护窗口内禁用 TiProxy。

要禁用 TiProxy，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **...**，在下拉菜单中点击 **Modify**。此时会显示 **Modify Cluster** 页面。
3. 在 **Modify Cluster** 页面，点击 TiProxy 开关以禁用 TiProxy。

![Disable TiProxy](/media/tidb-cloud/tiproxy-disable-tiproxy.png)

## 查看 TiProxy

### 查看 TiProxy 拓扑结构

要查看 TiProxy 拓扑结构，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Monitoring > Nodes**。此时会显示 **Node Map** 页面。
3. 在 **Node Map** 页面，TiProxy 拓扑结构显示在 **TiDB** 面板中。

![TiProxy Topology](/media/tidb-cloud/tiproxy-topology.png)

### 查看 TiProxy 统计/指标（信息）

要查看 TiProxy 统计/指标（信息），请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Monitoring > Metrics**。此时会显示 **Metrics** 页面。
3. 在 **Metrics** 页面，点击 **Server** 并下拉至 TiProxy 相关统计/指标（信息）。如需查看特定 TiDB 节点组的 TiProxy 统计/指标（信息），点击 **TiDB Node Group View**，选择你的 TiDB 节点组，然后下拉至 TiProxy 相关统计/指标（信息）。

这些统计/指标（信息）包括：

- **TiProxy CPU Usage**：每个 TiProxy 节点的 CPU 使用率统计。上限为 100%。如果最大 CPU 使用率超过 80%，建议扩容 TiProxy。
- **TiProxy Connections**：每个 TiProxy 节点上的连接数。
- **TiProxy Throughput**：每个 TiProxy 节点每秒传输的字节数。如果最大吞吐达到最大网络带宽，建议扩容 TiProxy。关于最大网络带宽的更多信息，参见 [决定 TiProxy 节点的规格和数量](#决定-tiproxy-节点的规格和数量)。
- **TiProxy Sessions Migration Reasons**：每分钟发生的会话迁移次数及其原因。例如，当 TiDB 缩容且 TiProxy 将会话迁移到其他 TiDB 节点时，原因为 `status`。更多迁移原因，参见 [TiProxy Monitoring Metrics](https://docs.pingcap.com/tidb/stable/tiproxy-grafana#balance)。

### 查看 TiProxy 账单

要查看 TiProxy 账单，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏点击 **Billing**。在 **Billing** 页面，默认显示 **Bills** 标签页。
3. 在 **Summary by Service** 部分，TiProxy 节点费用显示在 **TiDB Dedicated** 下，而 TiProxy 数据传输费用包含在 **Data Transfer > Same Region** 中。

![TiProxy Billing](/media/tidb-cloud/tiproxy-billing.png)

## 修改 TiProxy

> **注意**
>
> - 不支持直接修改 TiProxy 规格。建议你修改 TiProxy 节点数量。如果必须修改 TiProxy 规格，需要在所有 TiDB 节点组中禁用 TiProxy，然后重新启用以选择不同规格。
> - 缩容 TiProxy 会导致连接断开。请确保在维护窗口内进行缩容操作。

要对 TiProxy 进行扩容或缩容，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **...**，在下拉菜单中点击 **Modify**。此时会显示 **Modify Cluster** 页面。
3. 在 **Modify Cluster** 页面，修改 TiProxy 节点的数量。

![Modify TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

## 在多个 TiDB 节点组中管理 TiProxy

当你拥有多个 TiDB 节点组时，每个 TiDB 节点组都有其专属的 TiProxy 组。TiProxy 会将流量路由到同一 TiDB 节点组中的 TiDB 节点，以实现计算资源隔离。你可以在每个 TiDB 节点组中启用、禁用或修改 TiProxy。但所有 TiDB 节点组中的 TiProxy 规格必须保持一致。