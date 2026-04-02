---
title: 通过阿里云私有 endpoint 连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过阿里云私有 endpoint 连接你的 TiDB Cloud 集群。
---

# 通过阿里云私有 endpoint 连接 TiDB Cloud Starter 或 Essential

本教程将指导你通过阿里云上的私有 endpoint 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。通过私有 endpoint 连接，可以在你的服务与 TiDB Cloud 集群之间实现安全且私有的通信，无需经过公网。

> **提示：**
>
> 如需了解如何通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请参见 [Connect to TiDB Cloud via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

## 限制

- 目前，TiDB Cloud Starter 和 TiDB Cloud Essential 支持在 endpoint service 托管于 AWS 或阿里云时的私有 endpoint 连接。如果 service 托管在其他云服务商，私有 endpoint 不适用。
- 不支持跨 Region 的私有 endpoint 连接。

## 在阿里云上设置私有 endpoint

要通过私有 endpoint 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请按照以下步骤操作：

1. [选择 TiDB 集群](#step-1-choose-a-tidb-cluster)
2. [在阿里云上创建私有 endpoint](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3. [在 TiDB Cloud 中授权你的私有 endpoint](#step-3-authorize-your-private-endpoint-in-tidb-cloud)
4. [使用私有 endpoint 连接到你的 TiDB 集群](#step-4-connect-to-your-tidb-cluster-using-the-private-endpoint)

### Step 1. 选择 TiDB 集群

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 记录下 **Service Name**、**Availability Zone ID** 和 **Region ID**。

### Step 2. 在阿里云上创建私有 endpoint

要使用阿里云管理控制台创建 VPC interface endpoint，请执行以下步骤：

1. 登录 [阿里云管理控制台](https://account.alibabacloud.com/login/login.htm)。
2. 导航到 **VPC** > **Endpoints**。
3. 在 **Interface Endpoints** 标签页下，点击 **Create Endpoint**。
4. 填写 endpoint 信息：
    - **Region**：选择与你的 TiDB Cloud 集群相同的 Region。
    - **Endpoint Name**：为 endpoint 选择一个名称。
    - **Endpoint Type**：选择 **Interface Endpoint**。
    - **Endpoint Service**：选择 **Other Endpoint Services**。

5. 在 **Endpoint Service Name** 字段中，粘贴你从 TiDB Cloud 复制的 service name。
6. 点击 **Verify**。如果 service 有效，会出现绿色勾选。
7. 选择要用于 endpoint 的 **VPC**、**Security Group** 和 **Zone**。
8. 点击 **OK** 创建 endpoint。
9. 等待 endpoint 状态变为 **Active**，连接状态变为 **Connected**。

### Step 3. 在 TiDB Cloud 中授权你的私有 endpoint

在阿里云上创建 interface endpoint 后，你需要将其添加到集群的 allowlist 中。

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Settings** > **Networking**。
3. 向下滚动到 **Private Endpoint** 部分，找到 **Authorized Networks** 表格。
4. 点击 **Add Rule** 添加防火墙规则。

    - **Endpoint Service Name**：粘贴你在 [Step 1](#step-1-choose-a-tidb-cluster) 获取的 service name。
    - **Firewall Rule Name**：输入用于标识此连接的名称。
    - **Your Endpoint ID**：粘贴你在阿里云管理控制台获取的 23 位 endpoint ID（以 `ep-` 开头）。

    > **提示：**
    > 
    > 如果你希望允许来自云 Region 的所有 Private Endpoint 连接（用于测试或开放访问），可在 **Your Endpoint ID** 字段中输入一个星号（`*`）。

5. 点击 **Submit**。

### Step 4. 使用私有 endpoint 连接到你的 TiDB 集群

创建 interface endpoint 后，返回 TiDB Cloud 控制台，按照以下步骤操作：

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 在 **Connect With** 下拉列表中，选择你偏好的连接方法。对话框底部会显示相应的连接字符串。

    对于 host，请前往阿里云的 **Endpoint Details** 页面，复制 **Domain Name of Endpoint Service** 作为你的 host。

5. 使用该连接字符串连接到你的集群。