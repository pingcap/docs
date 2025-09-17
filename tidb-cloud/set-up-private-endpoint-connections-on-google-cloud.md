---
title: 通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群
summary: 了解如何通过 Google Cloud Private Service Connect 连接你的 TiDB Cloud 集群。
---

# 通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群

本文档介绍如何通过 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 连接你的 TiDB Cloud Dedicated 集群。Google Cloud Private Service Connect 是 Google Cloud 提供的私有端点服务。

<CustomContent language="en,zh">

> **提示：**
>
> - 如需了解如何通过 AWS 私有端点连接 TiDB Cloud Dedicated 集群，请参见 [通过 AWS PrivateLink 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 如需了解如何通过 Azure 私有端点连接 TiDB Cloud Dedicated 集群，请参见 [通过 Azure Private Link 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 如需了解如何通过私有端点连接 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请参见以下文档：
>     - [通过 AWS PrivateLink 连接 TiDB Cloud Starter](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
>     - [通过阿里云私有端点连接 TiDB Cloud Starter 或 Essential](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

> **Tip:**
>
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with AWS, see [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md).
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with Azure, see [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md).
> - To learn how to connect to a TiDB Cloud Starter or TiDB Cloud Essential cluster via private endpoint, see [Connect to TiDB Cloud Starter via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

</CustomContent>

TiDB Cloud 支持通过 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 实现对托管在 Google Cloud VPC 中的 TiDB Cloud 服务的高安全性、单向访问。你可以创建一个端点，并使用该端点连接到 TiDB Cloud 服务。

借助 Google Cloud Private Service Connect，端点连接安全且私密，不会将你的数据暴露在公网上。此外，端点连接支持 CIDR 重叠，便于网络管理。

Google Cloud Private Service Connect 的架构如下所示：[^1]

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

如需了解私有端点和端点服务的详细定义，请参见以下 Google Cloud 文档：

- [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- [通过端点访问已发布的服务](https://cloud.google.com/vpc/docs/configure-private-service-connect-services)

## 限制

- 此功能适用于 2023 年 4 月 13 日之后创建的 TiDB Cloud Dedicated 集群。对于更早创建的集群，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 获取帮助。
- 只有 `Organization Owner` 和 `Project Owner` 角色可以创建 Google Cloud Private Service Connect 端点。
- 每个 TiDB 集群最多可处理来自 10 个端点的连接。
- 每个 Google Cloud 项目最多可有 10 个端点连接到一个 TiDB 集群。
- 自 2025 年 8 月 12 日起，你在 Google Cloud 上为 TiDB Cloud Dedicated 集群每个区域可创建的 Google Private Service Connect (PSC) 连接数上限取决于 NAT 子网 CIDR 块的大小：
    - `/20`：每个区域最多 7 个 PSC 连接
    - `/19`：每个区域最多 23 个 PSC 连接
    - `/18`：每个区域最多 55 个 PSC 连接
    - `/17`：每个区域最多 119 个 PSC 连接
    - `/16`：每个区域最多 247 个 PSC 连接
- 私有端点和要连接的 TiDB 集群必须位于同一区域。
- 出站防火墙规则必须允许流量访问端点的内部 IP 地址。[隐式允许出站防火墙规则](https://cloud.google.com/firewall/docs/firewalls#default_firewall_rules) 允许出站到任意目标 IP 地址。
- 如果你在 VPC 网络中创建了出站拒绝防火墙规则，或创建了修改隐式允许出站行为的分层防火墙策略，可能会影响对端点的访问。在这种情况下，你需要创建特定的出站允许防火墙规则或策略，以允许流量访问端点的内部目标 IP 地址。

在大多数场景下，建议你优先使用私有端点连接而非 VPC 对等连接。但在以下场景下，应使用 VPC 对等连接而不是私有端点连接：

- 你正在使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 集群在不同区域间将数据从源 TiDB 集群同步到目标 TiDB 集群，以实现高可用。目前，私有端点不支持跨区域连接。
- 你正在使用 TiCDC 集群将数据同步到下游集群（如 Amazon Aurora、MySQL 和 Kafka），但无法自行维护下游的端点服务。

## 通过 Google Cloud Private Service Connect 设置私有端点

要通过私有端点连接到你的 TiDB Cloud Dedicated 集群，请完成[前置条件](#prerequisites)并按照以下步骤操作：

1. [选择 TiDB 集群](#step-1-select-a-tidb-cluster)
2. [创建 Google Cloud 私有端点](#step-2-create-a-google-cloud-private-endpoint)
3. [接受端点访问](#step-3-accept-endpoint-access)
4. [连接到你的 TiDB 集群](#step-4-connect-to-your-tidb-cluster)

如果你有多个集群，需要对每个希望通过 Google Cloud Private Service Connect 连接的集群重复上述步骤。

### 前置条件

在开始创建端点前：

- 在你的 Google Cloud 项目中[启用](https://console.cloud.google.com/apis/library/compute.googleapis.com)以下 API：
    - [Compute Engine API](https://cloud.google.com/compute/docs/reference/rest/v1)
    - [Service Directory API](https://cloud.google.com/service-directory/docs/reference/rest)
    - [Cloud DNS API](https://cloud.google.com/dns/docs/reference/v1)

- 准备好具备创建端点所需权限的 [IAM 角色](https://cloud.google.com/iam/docs/understanding-roles)。

    - 任务：
        - 创建端点
        - 自动或手动为端点配置 [DNS 记录](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#dns-endpoint)
    - 所需 IAM 角色：
        - [Compute Network Admin](https://cloud.google.com/iam/docs/understanding-roles#compute.networkAdmin) (roles/compute.networkAdmin)
        - [Service Directory Editor](https://cloud.google.com/iam/docs/understanding-roles#servicedirectory.editor) (roles/servicedirectory.editor)

### Step 1. 选择 TiDB 集群

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB 集群的名称，进入其概览页面。你可以选择以下任一状态的集群：

    - **Available**
    - **Restoring**
    - **Modifying**
    - **Importing**

2. 点击右上角的 **Connect**。会弹出连接对话框。

3. 在 **Connection Type** 下拉列表中选择 **Private Endpoint**，然后点击 **Create Private Endpoint Connection**。

    > **注意：**
    >
    > 如果你已经创建了私有端点连接，活动端点会显示在连接对话框中。若需创建更多私有端点连接，请通过左侧导航栏点击 **Settings** > **Networking** 进入 **Networking** 页面。

### Step 2. 创建 Google Cloud 私有端点

1. 提供以下信息以生成创建私有端点的命令：
    - **Google Cloud Project ID**：与你的 Google Cloud 账户关联的项目 ID。你可以在 [Google Cloud **Dashboard** 页面](https://console.cloud.google.com/home/dashboard)找到该 ID。
    - **Google Cloud VPC Name**：指定项目中的 VPC 名称。你可以在 [Google Cloud **VPC networks** 页面](https://console.cloud.google.com/networking/networks/list)找到。
    - **Google Cloud Subnet Name**：指定 VPC 下的子网名称。你可以在 **VPC network details** 页面找到。
    - **Private Service Connect Endpoint Name**：为将要创建的私有端点输入一个唯一名称。
2. 输入信息后，点击 **Generate Command**。
3. 复制生成的命令。
4. 打开 [Google Cloud Shell](https://console.cloud.google.com/home/dashboard)，执行该命令以创建私有端点。

### Step 3. 接受端点访问

在 Google Cloud Shell 成功执行命令后，返回 TiDB Cloud 控制台，点击 **Accept Endpoint Access**。

如果你看到错误 `not received connection request from endpoint`，请确保你已正确复制命令并在 Google Cloud Shell 中成功执行。

### Step 4. 连接到你的 TiDB 集群

在你接受私有端点连接后，会自动返回到连接对话框。

1. 等待私有端点连接状态从 **System Checking** 变为 **Active**（大约 5 分钟）。
2. 在 **Connect With** 下拉列表中选择你偏好的连接方式。对应的连接字符串会显示在对话框底部。
3. 使用该连接字符串连接到你的集群。

### 私有端点状态参考

当你使用私有端点连接时，私有端点或私有端点服务的状态会显示在 [**Private Endpoint** 页面](#prerequisites)。

私有端点可能的状态说明如下：

- **Pending**：等待处理。
- **Active**：你的私有端点已可用。此状态下无法编辑该私有端点。
- **Deleting**：私有端点正在删除中。
- **Failed**：私有端点创建失败。你可以点击该行的 **Edit** 重试创建。

私有端点服务可能的状态说明如下：

- **Creating**：端点服务正在创建中，通常需要 3 到 5 分钟。
- **Active**：端点服务已创建，无论私有端点是否已创建。

## 故障排查

### TiDB Cloud 创建端点服务失败，怎么办？

在你打开 **Create Google Cloud Private Endpoint Connection** 页面并选择 TiDB 集群后，端点服务会自动创建。如果显示为失败或长时间处于 **Creating** 状态，请提交 [支持工单](/tidb-cloud/tidb-cloud-support.md) 获取帮助。

### 在 Google Cloud 创建端点失败，怎么办？

要排查该问题，你需要查看在 Google Cloud Shell 执行私有端点创建命令后返回的错误信息。如果是权限相关错误，必须先授予所需权限后再重试。

### 我取消了某些操作，接受端点访问前该如何处理？

已取消操作的未保存草稿不会被保留或显示。下次在 TiDB Cloud 控制台创建新私有端点时，需要重新执行每一步。

如果你已经在 Google Cloud Shell 执行了创建私有端点的命令，需要在 Google Cloud 控制台手动[删除对应端点](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint)。

### 为什么在 TiDB Cloud 控制台直接复制服务附件生成的端点无法看到？

在 TiDB Cloud 控制台，你只能查看通过 **Create Google Cloud Private Endpoint Connection** 页面生成命令创建的端点。

而直接复制服务附件（即未通过 TiDB Cloud 控制台生成的命令创建的端点）所生成的端点不会在 TiDB Cloud 控制台显示。

[^1]: Google Cloud Private Service Connect 架构图来自 Google Cloud 文档 [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)，遵循 Creative Commons Attribution 4.0 International 许可协议。