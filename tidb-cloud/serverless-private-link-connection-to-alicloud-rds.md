---
title: 通过 Private Link 连接到阿里云 ApsaraDB RDS for MySQL
summary: 了解如何通过阿里云 Endpoint Service Private Link 连接，将 TiDB Cloud Essential 集群连接到阿里云 ApsaraDB RDS for MySQL 实例。
---

# 通过 Private Link 连接到阿里云 ApsaraDB RDS for MySQL

本文介绍如何使用 [阿里云 Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md) 将 TiDB Cloud Essential 集群连接到 [阿里云 ApsaraDB RDS for MySQL](https://www.alibabacloud.com/en/product/apsaradb-for-rds-mysql) 实例。

## 前提条件

- 你已有现有的 ApsaraDB RDS for MySQL 实例，或拥有创建实例所需的权限。

- 确认你的账户拥有以下权限以管理网络组件：

    - 管理负载均衡器
    - 管理 endpoint services

- 你的 TiDB Cloud Essential 集群部署在阿里云上，并且处于活跃状态。请获取并保存以下信息以备后续使用：

    - 阿里云账户 ID
    - 可用区（AZ）

要查看阿里云账户 ID 和可用区，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 TiDB 集群的集群总览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹出的对话框中，你可以找到阿里云账户 ID 和可用区信息。

## 步骤 1. 创建 ApsaraDB RDS for MySQL 实例

确定你要使用的阿里云 ApsaraDB RDS for MySQL，或[新建一个 RDS 实例](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases)。

你的 ApsaraDB RDS for MySQL 实例需满足以下要求：

- Region 匹配：实例必须与 TiDB Cloud Essential 集群处于同一阿里云 Region。
- 可用区（AZ）可用性：可用区需与 TiDB Cloud Essential 集群的可用区有重叠。
- 网络可达性：实例需配置合适的 IP 允许列表，并可在 VPC 内访问。

> **注意**
>
> 不支持 ApsaraDB RDS for MySQL 的跨 Region 连接。

## 步骤 2. 将 ApsaraDB RDS for MySQL 实例暴露为 endpoint service

你需要在阿里云控制台中设置负载均衡器和 endpoint service。

### 步骤 2.1. 设置负载均衡器

在与你的 ApsaraDB RDS for MySQL 实例相同的 Region 内设置负载均衡器，操作如下：

1. 前往 [Server Groups](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups) 创建服务器组，填写以下信息：

    - **Server Group Type**：选择 `IP`
    - **VPC**：输入你的 ApsaraDB RDS for MySQL 所在的 VPC
    - **Backend Server Protocol**：选择 `TCP`

2. 点击已创建的服务器组添加后端服务器，然后添加你的 ApsaraDB RDS for MySQL 实例的 IP 地址。

    你可以通过 ping RDS endpoint 获取 IP 地址。
 
3. 前往 [NLB](https://slb.console.alibabacloud.com/nlb) 创建网络型负载均衡器，填写以下信息：

    - **Network Type**：选择 `Internal-facing`
    - **VPC**：选择你的 ApsaraDB RDS for MySQL 所在的 VPC
    - **Zone**：需与 TiDB Cloud Essential 集群的可用区有重叠
    - **IP Version**：选择 `IPv4`

4. 找到你创建的负载均衡器，点击 **Create Listener**，填写以下信息：
    
    - **Listener Protocol**：选择 `TCP`
    - **Listener Port**：输入数据库端口，例如 MySQL 的 `3306`
    - **Server Group**：选择上一步创建的服务器组
  
### 步骤 2.2. 设置 endpoint service

在与你的 ApsaraDB RDS for MySQL 实例相同的 Region 内设置 endpoint service，操作如下：

1. 前往 [Endpoint Service](https://vpc.console.alibabacloud.com/endpointservice) 创建 endpoint service，填写以下信息：

    - **Service Resource Type**：选择 `NLB`
    - **Select Service Resource**：选择 NLB 所在的所有可用区，并选择你在上一步创建的 NLB
    - **Automatically Accept Endpoint Connections**：建议选择 `No`

2. 进入 endpoint service 的详情页，复制 **Endpoint Service Name**，例如 `com.aliyuncs.privatelink.<region>.xxxxx`。后续在 TiDB Cloud 中需要用到该名称。

3. 在 endpoint service 的详情页，点击 **Service Whitelist** 标签页，点击 **Add to Whitelist**，然后输入你在[前提条件](#prerequisites)中获取的阿里云账户 ID。

## 步骤 3. 在 TiDB Cloud 中创建 Private Link 连接

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 创建 Private Link 连接。

更多信息请参见 [创建阿里云 Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-alibaba-cloud-endpoint-service-private-link-connection)。