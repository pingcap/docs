---
title: 通过阿里云私有终端节点连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过阿里云私有终端节点连接到你的 TiDB Cloud 集群。
---

# 通过阿里云私有终端节点连接 TiDB Cloud Starter 或 Essential

本教程将指导你如何通过阿里云的私有终端节点连接到你的 TiDB Cloud Starter 或 Essential 集群。通过私有终端节点连接，可以在不经过公网的情况下，实现你的服务与 TiDB Cloud 集群之间的安全、私密通信。

> **Tip:**
>
> 如果你想了解如何通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential 集群，请参阅 [Connect to TiDB Cloud via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

## 限制

- 目前，TiDB Cloud Starter 和 TiDB Cloud Essential 支持在终端节点服务托管于 AWS 或阿里云时使用私有终端节点连接。如果服务托管在其他云服务商，私有终端节点不可用。
- 不支持跨地域的私有终端节点连接。

## 使用阿里云设置私有终端节点

要通过私有终端节点连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请按照以下步骤操作：

1. [选择 TiDB 集群](#step-1-choose-a-tidb-cluster)
2. [在阿里云上创建私有终端节点](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3. [使用私有终端节点连接到你的 TiDB 集群](#step-3-connect-to-your-tidb-cluster-using-the-private-endpoint)

### Step 1. 选择 TiDB 集群

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 记录下 **Service Name**、**Availability Zone ID** 和 **Region ID**。

### Step 2. 在阿里云上创建私有终端节点

要使用阿里云管理控制台创建 VPC 接口终端节点，请执行以下步骤：

1. 登录 [阿里云管理控制台](https://account.alibabacloud.com/login/login.htm)。
2. 进入 **VPC** > **Endpoints**。
3. 在 **Interface Endpoints** 标签页下，点击 **Create Endpoint**。
4. 填写终端节点信息：
    - **Region**：选择与你的 TiDB Cloud 集群相同的地域。
    - **Endpoint Name**：为终端节点选择一个名称。
    - **Endpoint Type**：选择 **Interface Endpoint**。
    - **Endpoint Service**：选择 **Other Endpoint Services**。

5. 粘贴你从 TiDB Cloud 复制的 **Endpoint Service Name**。
6. 点击 **Verify**。如果服务有效，会出现绿色对勾。
7. 选择要用于该终端节点的 **VPC**、**Security Group** 和 **Zone**。
8. 点击 **OK** 创建终端节点。
9. 等待终端节点状态变为 **Active**，连接状态变为 **Connected**。

### Step 3: 使用私有终端节点连接到你的 TiDB 集群

创建接口终端节点后，返回 TiDB Cloud 控制台，按照以下步骤操作：

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 在 **Connect With** 下拉列表中，选择你偏好的连接方式。对应的连接字符串会显示在对话框底部。

    对于 host，请前往阿里云的 **Endpoint Details** 页面，复制 **Domain Name of Endpoint Service** 作为你的 host。

5. 使用该连接字符串连接到你的集群。