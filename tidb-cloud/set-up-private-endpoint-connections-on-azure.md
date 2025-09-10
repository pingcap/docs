---
title: 通过 Azure Private Link 连接 TiDB Cloud 专属集群
summary: 了解如何通过 Azure Private Link 连接 TiDB Cloud 专属集群。
---

# 通过 Azure Private Link 连接 TiDB Cloud 专属集群

本文档介绍如何通过 [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) 连接你的 TiDB Cloud 专属集群。

<CustomContent language="en,zh">

> **提示：**
>
> - 如需了解如何通过 AWS 私有终端节点连接 TiDB Cloud 专属集群，请参见 [通过 AWS PrivateLink 连接 TiDB Cloud 专属集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 如需了解如何通过 Google Cloud 私有终端节点连接 TiDB Cloud 专属集群，请参见 [通过 Google Cloud Private Service Connect 连接 TiDB Cloud 专属集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> - 如需了解如何通过私有终端节点连接 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请参见以下文档：
>     - [通过 AWS PrivateLink 连接 TiDB Cloud Starter](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
>     - [通过阿里云私有终端节点连接 TiDB Cloud Starter 或 Essential](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

> **Tip:**
>
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with AWS, see [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md).
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with Google Cloud, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> - To learn how to connect to a TiDB Cloud Starter or TiDB Cloud Essential cluster via private endpoint, see [Connect to TiDB Cloud Starter via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

</CustomContent>

TiDB Cloud 支持通过 [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) 在 Azure 虚拟网络中以高度安全和单向的方式访问托管在 TiDB Cloud 的服务，就像服务部署在你自己的虚拟网络中一样。你可以在自己的虚拟网络中创建一个私有终端节点，然后通过该终端节点并获得权限后连接 TiDB Cloud 服务。

借助 Azure Private Link，终端节点连接安全且私密，不会将你的数据暴露在公网上。此外，终端节点连接支持 CIDR 重叠，便于网络管理。

Azure Private Link 的架构如下所示：[^1]

![Azure Private Link architecture](/media/tidb-cloud/azure-private-endpoint-arch.png)

如需了解私有终端节点和终端节点服务的详细定义，请参见以下 Azure 文档：

- [什么是 Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
- [什么是私有终端节点](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [创建私有终端节点](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## 限制

- 只有 `Organization Owner` 和 `Project Owner` 角色可以创建私有终端节点。
- 私有终端节点和要连接的 TiDB 集群必须位于同一区域。

## 使用 Azure Private Link 设置私有终端节点

要通过私有终端节点连接你的 TiDB Cloud 专属集群，请完成以下步骤：

1. [选择 TiDB 集群](#step-1-select-a-tidb-cluster)
2. [创建 Azure 私有终端节点](#step-2-create-an-azure-private-endpoint)
3. [接受终端节点](#step-3-accept-the-endpoint)
4. [连接到你的 TiDB 集群](#step-4-connect-to-your-tidb-cluster)

如果你有多个集群，需要对每个希望通过 Azure Private Link 连接的集群重复这些步骤。

### Step 1. 选择 TiDB 集群

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中选择 **Private Endpoint**，然后点击 **Create Private Endpoint Connection**，打开 **Create Azure Private Endpoint Connection** 对话框。

> **注意：**
>
> 如果你已经创建了私有终端节点连接，活动终端节点会显示在连接对话框中。若需创建更多私有终端节点连接，请通过点击左侧导航栏的 **Settings** > **Networking** 进入 **Networking** 页面。

### Step 2. 创建 Azure 私有终端节点

1. 在 **Create Azure Private Endpoint Connection** 对话框中，复制私有链路服务的 TiDB Cloud 资源 ID，并保持对话框打开以便后续使用。

    > **注意：**
    >
    > 对于每个 TiDB Cloud 专属集群，相关的终端节点服务会在集群创建后 3 到 4 分钟内自动创建。

2. 登录 [Azure portal](https://portal.azure.com/)，然后使用复制的 TiDB Cloud 资源 ID 为你的集群创建私有终端节点，具体步骤如下：

    1. 在 Azure portal 中，搜索 **Private endpoints**，然后在结果中选择 **Private endpoints**。
    2. 在 **Private endpoint** 页面，点击 **+ Create**。
    3. 在 **Basics** 标签页，填写项目和实例信息，然后点击 **Next: Resource**。
    4. 在 **Resource** 标签页，将 **connection method** 选择为 **Connect to an Azure resource by resource ID or alias**，并将 TiDB Cloud 资源 ID 粘贴到 **Resource ID or alias** 字段。
    5. 继续点击 **Next**，完成剩余配置标签页的必填项。然后点击 **Create** 创建并部署私有终端节点。Azure 可能需要几秒钟完成部署。更多信息请参见 Azure 文档 [创建私有终端节点](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint)。

3. 私有终端节点创建并部署完成后，点击 **Go to resource**，然后执行以下操作：

     - 点击左侧导航栏的 **Settings** > **Properties**，复制其 **Resource ID** 以备后用。

         ![Azure private endpoint resource ID](/media/tidb-cloud/azure-private-endpoint-resource-id.png)

     - 点击左侧导航栏的 **Settings** > **DNS configuration**，复制其 **IP address** 以备后用。

         ![Azure private endpoint DNS IP](/media/tidb-cloud/azure-private-endpoint-dns-ip.png)

### Step 3. 接受终端节点

1. 返回 TiDB Cloud 控制台中的 **Create Azure Private Endpoint Connection** 对话框，将复制的 **Resource ID** 和 **IP address** 粘贴到对应字段。
2. 点击 **Verify Endpoint** 验证私有终端节点访问权限。如果遇到错误，请根据错误提示进行排查，然后重试。
3. 验证成功后，点击 **Accept Endpoint**，批准来自你的私有终端节点的连接。

### Step 4. 连接到你的 TiDB 集群

在你接受终端节点连接后，会自动返回到连接对话框。

1. 等待私有终端节点连接状态变为 **Active**（大约 5 分钟）。你可以通过点击左侧导航栏的 **Settings** > **Networking** 进入 **Networking** 页面查看状态。
2. 在 **Connect With** 下拉列表中选择你偏好的连接方式。对应的连接字符串会显示在对话框底部。
3. 使用该连接字符串连接到你的集群。

### 私有终端节点状态参考

如需查看私有终端节点或私有终端节点服务的状态，请通过点击左侧导航栏的 **Settings** > **Networking** 进入 **Networking** 页面。

私有终端节点可能的状态说明如下：

- **Discovered**：TiDB Cloud 可以在接受请求前自动检测与你的终端节点服务关联的私有终端节点，避免重复创建。
- **Pending**：等待处理。
- **Active**：你的私有终端节点已准备就绪。此状态下无法编辑该私有终端节点。
- **Deleting**：私有终端节点正在被删除。
- **Failed**：私有终端节点创建失败。你可以点击该行的 **Edit** 重试创建。

私有终端节点服务可能的状态说明如下：

- **Creating**：终端节点服务正在创建，通常需要 3 到 5 分钟。
- **Active**：终端节点服务已创建，无论私有终端节点是否已创建。

## 故障排查

### TiDB Cloud 创建终端节点服务失败怎么办？

在你打开 **Create Azure Private Endpoint** 页面并选择 TiDB 集群后，终端节点服务会自动创建。如果显示为失败或长时间处于 **Creating** 状态，请提交 [工单](/tidb-cloud/tidb-cloud-support.md) 获取帮助。

### 如果在设置过程中取消了操作，接受私有终端节点前需要做什么？

Azure 私有终端节点连接功能可以自动检测你的私有终端节点。这意味着，在 Azure portal [创建 Azure 私有终端节点](#step-2-create-an-azure-private-endpoint) 后，如果你在 TiDB Cloud 控制台的 **Create Azure Private Endpoint Connection** 对话框中点击了 **Cancel**，你仍然可以在 **Networking** 页面查看已创建的终端节点。如果取消是误操作，你可以继续配置终端节点完成设置。如果取消是有意为之，你可以直接在 TiDB Cloud 控制台删除该终端节点。

[^1]: Azure Private Link 架构图来自 Azure 文档 [什么是 Azure Private Link 服务](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview)（[GitHub 源文件](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/private-link/private-link-service-overview.md)），遵循 Creative Commons Attribution 4.0 International 许可协议。