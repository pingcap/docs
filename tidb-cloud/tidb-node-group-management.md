---
title: 管理 TiDB 节点组
summary: 了解如何管理 TiDB 节点组及其端点，以实现业务负载隔离。
---

# 管理 TiDB 节点组

本文档介绍如何通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 管理 TiDB 节点组及其端点，以实现业务负载隔离。

> **Note**:
>
> TiDB 节点组功能 **不适用于** TiDB Cloud Serverless 集群。

## 术语

- TiDB 节点组：TiDB 节点组用于管理 TiDB 节点的分组，并维护端点与 TiDB 节点之间的映射关系。

    - 每个 TiDB 节点组都有一个唯一的端点。
    - 当你删除一个 TiDB 节点组时，相关的网络设置（如私有链路和 IP 访问列表）也会被删除。

- 默认组：当集群创建时，会自动创建一个默认的 TiDB 节点组。因此，每个集群都有一个默认组。默认组无法被删除。

## 前提条件

- 你已经在 AWS 或 Google Cloud 上部署了 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。
- 你拥有组织的 **Organization Owner** 或 **Project Owner** 角色。更多信息，参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

> **Note**:
>
> TiDB 节点组无法在集群创建时直接创建。你需要在集群创建完成并处于 **Available** 状态后，再添加节点组。

## 创建 TiDB 节点组

要创建 TiDB 节点组，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Nodes**。
3. 点击右上角的 **Modify**。此时会显示 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，点击 **+** 以添加新的 TiDB 节点组。你也可以直接使用默认组。

    - TiDB
        - **vCPU + RAM**：选择你需要的 [TiDB 规格](/tidb-cloud/size-your-cluster.md#size-tidb)。仅支持 8 vCPU 16 GiB 内存及以上规格的 TiDB 节点。
        - **Node Groups**：点击 **+** 创建新的 TiDB 节点组。你也可以直接使用默认组，并在 **DefaultGroup** 字段中填写 TiDB 节点数量。
    
    - TiKV
        - **vCPU + RAM**：选择你需要的 [TiKV 规格](/tidb-cloud/size-your-cluster.md#size-tikv)。
        - **Storage x Nodes**：选择存储容量和 TiKV 节点数量。
    
    - TiFlash（可选）
        - **vCPU + RAM**：选择你需要的 [TiFlash 规格](/tidb-cloud/size-your-cluster.md#size-tiflash)。
        - **Storage x Nodes**：选择存储容量和 TiFlash 节点数量。

    ![Create TiDB Node Group](/media/tidb-cloud/tidb-node-group-create.png)

5. 新的 TiDB 节点会随着新的 TiDB 节点组一起添加，这会影响集群的计费。请在右侧面板确认集群规模后，点击 **Confirm**。

默认情况下，你最多可以为一个 TiDB Cloud Dedicated 集群创建 5 个 TiDB 节点组。如果需要更多节点组，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

如果你创建了 TiDB 节点组，但仍然使用默认组的端点连接集群，则该 TiDB 节点组中的节点不会承担任何负载，造成资源浪费。你需要为新建的 TiDB 节点组创建新的连接。参见 [连接到 TiDB 节点组](#connect-to-a-tidb-node-group)。

## 连接到 TiDB 节点组

### 通过公网连接

新建的 TiDB 节点组默认关闭公网连接。你需要先启用它。

启用公网连接，请执行以下操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在右上角点击 **Connect**，弹出连接对话框。
3. 在 **TiDB Node Group** 列表中选择你的 TiDB 节点组，在 **Connection Type** 列表中选择 **Public**。

    如果你尚未配置 IP 访问列表，请点击 **Configure IP Access List**，或按照 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行首次连接前的配置。

4. 在左侧导航栏点击 **Settings** > **Networking**。
5. 在 **Networking** 页面右上角的 **TiDB Node Group** 列表中选择你的 TiDB 节点组。
6. 在 **Public Endpoint** 区域点击 **Enable**，然后在 **IP Access List** 区域点击 **Add IP Address**。
7. 在 **Networking** 页面右上角点击 **Connect** 获取连接串。

![Connect to the new TiDB node group via Public Endpoint](/media/tidb-cloud/tidb-node-group-connect-public-endpoint.png)

更多信息，参见 [通过公网连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

### 通过私有端点连接

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在右上角点击 **Connect**，弹出连接对话框。
3. 在 **TiDB Node Group** 列表中选择你的 TiDB 节点组，在 **Connection Type** 列表中选择 **Private Endpoint**。
4. 在左侧导航栏点击 **Settings** > **Networking**。
5. 在 **Networking** 页面右上角的 **TiDB Node Group** 列表中选择你的 TiDB 节点组。
6. 点击 **Create Private Endpoint Connection**，为该节点组创建新的私有端点连接。

     - 如果集群部署在 AWS，请参考 [通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
     - 如果集群部署在 Google Cloud，请参考 [通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

    > **Note**:
    >
    > 如果你使用 Private Link 连接不同的节点组，需要为每个节点组分别创建私有端点连接。

7. 创建私有端点连接后，点击页面右上角的 **Connect** 获取连接串。

### 通过 VPC Peering 连接

由于所有 TiDB 节点组与集群共享同一个 VPC，你只需为该集群创建一个 VPC Peering 连接，即可为所有节点组开启访问。

1. 按照 [通过 VPC Peering 连接到 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md) 的说明为该集群创建 VPC Peering。
2. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
3. 在左侧导航栏点击 **Settings** > **Networking**。
4. 在 **Networking** 页面右上角点击 **Connect** 获取连接串。

## 查看 TiDB 节点组

要查看 TiDB 节点组的详细信息，请执行以下步骤：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Nodes**，即可查看 TiDB 节点组列表。

    若需切换为表格视图，请点击 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 -4 24 24" stroke-width="1.5"><path d="M3 9.5H21M3 14.5H21M7.8 4.5H16.2C17.8802 4.5 18.7202 4.5 19.362 4.82698C19.9265 5.1146 20.3854 5.57354 20.673 6.13803C21 6.77976 21 6.61984 21 8.3V15.7C21 17.3802 21 17.2202 20.673 17.862C20.3854 18.4265 19.9265 18.8854 19.362 19.173C18.7202 19.5 17.8802 19.5 16.2 19.5H7.8C6.11984 19.5 5.27976 19.5 4.63803 19.173C4.07354 18.8854 3.6146 18.4265 3.32698 17.862C3 17.2202 3 17.3802 3 15.7V8.3C3 6.61984 3 6.77976 3.32698 6.13803C3.6146 5.57354 4.07354 5.1146 4.63803 4.82698C5.27976 4.5 6.11984 4.5 7.8 4.5Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg>。

## 修改 TiDB 节点组

你可以修改组名以及组内节点的配置。

### 修改组名

要修改组名，请执行以下步骤：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Nodes**。
3. 点击 <svg width="16" height="16" viewBox="0 -2 24 24" stroke-width="1.5" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"/></svg>，并为 TiDB 节点组输入新名称。

### 更新节点配置

要更新组内 TiDB、TiKV 或 TiFlash 节点的配置，请执行以下步骤：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Nodes**。
3. 在 **Node Map** 页面，点击右上角的 **Modify**，进入 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，你可以：

    - 修改 TiDB 节点数量。
    - 添加新的节点组。
    - 更新 TiKV 和 TiFlash 节点的规格及 **Storage x Nodes** 配置。

![Change TiDB node group node count](/media/tidb-cloud/tidb-node-group-change-node-count.png)

## 删除 TiDB 节点组

> **Note**:
>
> 当你删除 TiDB 节点组时，其节点和网络配置也会被一并移除，包括私有端点连接和公网访问的 IP 列表。

要删除 TiDB 节点组，请执行以下步骤：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 在左侧导航栏点击 **Nodes**。
3. 在 **Node Map** 页面，点击右上角的 **Modify**，进入 **Modify Cluster** 页面。
4. 在 **Modify Cluster** 页面，点击 <svg width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 6V5.2C16 4.0799 16 3.51984 15.782 3.09202C15.5903 2.71569 15.2843 2.40973 14.908 2.21799C14.4802 2 13.9201 2 12.8 2H11.2C10.0799 2 9.51984 2 9.09202 2.21799C8.71569 2.40973 8.40973 2.71569 8.21799 3.09202C8 3.51984 8 4.0799 8 5.2V6M10 11.5V16.5M14 11.5V16.5M3 6H21M19 6V17.2C19 18.8802 19 19.7202 18.673 20.362C18.3854 20.9265 17.9265 21.3854 17.362 21.673C16.7202 22 15.8802 22 14.2 22H9.8C8.11984 22 7.27976 22 6.63803 21.673C6.07354 21.3854 5.6146 20.9265 5.32698 20.362C5 19.7202 5 18.8802 5 17.2V6" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"/></svg> 删除 TiDB 节点组。

![Delete the TiDB node group](/media/tidb-cloud/tidb-node-group-delete.png)