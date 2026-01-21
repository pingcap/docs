---
title: 通过 Private Link 连接访问 Amazon RDS
summary: 了解如何使用 AWS Endpoint Service Private Link 连接访问 Amazon RDS 实例。
---

# 通过 Private Link 连接访问 Amazon RDS

本文档介绍如何将 TiDB Cloud Essential 集群通过 [AWS Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md)连接到 [Amazon RDS](https://aws.amazon.com/rds/) 实例。

## 前提条件

- 你已有一个现有的 Amazon RDS 实例，或拥有创建实例所需的权限。

- 你的账户具备以下管理网络组件的权限：

    - 管理安全组
    - 管理负载均衡器
    - 管理 endpoint service

- 你的 TiDB Cloud Essential 托管在 AWS 上，并且处于活跃状态。请获取并保存以下信息以备后用：

    - AWS 账户 ID
    - 可用区（AZ）

要查看 AWS 账户 ID 和可用区，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到 TiDB 集群的集群总览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹出的对话框中，你可以找到 AWS 账户 ID 和可用区。

## 第 1 步. 设置 Amazon RDS 实例

确定要使用的 Amazon RDS 实例，或[创建一个新的实例](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html)。

Amazon RDS 实例必须满足以下要求：

- Region 匹配：实例必须与 TiDB Cloud Essential 集群位于同一 AWS Region。
- 你的 Amazon RDS 实例的 [子网组](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets)必须包含与 TiDB Cloud Essential 集群重叠的可用区。
- 为你的 Amazon RDS 实例设置合适的安全组，并确保其在 VPC 内可访问。例如，你可以创建如下规则的安全组：

    - 允许 MySQL/Aurora 的入站规则： 
        - 类型: `MySQL/Aurora`
        - 来源: `Anywhere-IPv4`
    
    - 允许 MySQL/Aurora 的出站规则： 
        - 类型: `MySQL/Aurora`
        - 目标: `Anywhere-IPv4`

> **注意**
>
> 如需连接跨 Region 的 RDS 实例，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 第 2 步. 将 Amazon RDS 实例暴露为 endpoint service

你需要在 AWS 控制台中设置负载均衡器和 AWS Endpoint Service。

### 第 2.1 步. 设置负载均衡器

要在与 RDS 相同的 Region 内设置负载均衡器，请执行以下步骤：

1. 前往 [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup) 创建 target group，并填写以下信息：

    - **Target type**: 选择 `IP addresses`。
    - **Protocol and Port**: 协议设置为 `TCP`，端口设置为你的数据库端口，例如 MySQL 的 `3306`。
    - **IP address type**: 选择 `IPv4`。
    - **VPC**: 选择你的 RDS 所在的 VPC。
    - **Register targets**: 注册你的 Amazon RDS 实例的 IP 地址。你可以通过 ping RDS endpoint 获取 IP 地址。
 
    更多信息请参见 [为 Network Load Balancer 创建 target group](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html)。

2. 前往 [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers) 创建网络负载均衡器，并填写以下信息：

    - **Schema**: 选择 `Internal`
    - **Load balancer IP address type**: 选择 `IPv4`
    - **VPC**: 选择你的 RDS 所在的 VPC
    - **Availability Zones**: 选择与你的 TiDB Cloud Essential 集群重叠的可用区
    - **Security groups**: 创建一个包含以下规则的新安全组：
        - 允许 MySQL/Aurora 的入站规则： 
            - 类型: `MySQL/Aurora`
            - 来源: `Anywhere-IPv4`

        - 允许 MySQL/Aurora 的出站规则：        
            - 类型: `MySQL/Aurora`
            - 目标: `Anywhere-IPv4`

    - **Listeners and routing**:  
        - **Protocol and Port**: 协议设置为 `TCP`，端口设置为你的数据库端口，例如 MySQL 的 `3306`
        - **Target group**: 选择你在上一步创建的 target group

  更多信息请参见 [创建 Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)。

### 第 2.2 步. 设置 AWS Endpoint Service

要在与 RDS 相同的 Region 内设置 endpoint service，请执行以下步骤：

1. 前往 [Endpoint services](https://console.aws.amazon.com/vpcconsole/home#EndpointServices) 创建 endpoint service，并填写以下信息：

    - **Load balancer type**: 选择 `Network`
    - **Available load balancers**: 输入你在上一步创建的负载均衡器
    - **Supported Regions**: 如果没有跨 Region 需求则留空
    - **Require acceptance for endpoint**: 建议选择 `Acceptance required`
    - **Supported IP address types**: 选择 `IPv4`

2. 进入 endpoint service 的详情页，复制 endpoint service 名称，格式为 `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`。你需要将其提供给 TiDB Cloud。

3. 在 endpoint service 的详情页，点击 **Allow principals** 标签页，然后将你在[前提条件](#prerequisites)中获取的 AWS 账户 ID 添加到 allowlist，例如 `arn:aws:iam::<account_id>:root`。

## 第 3 步. 在 TiDB Cloud 中创建 AWS Endpoint Service Private Link 连接

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 创建 Private Link 连接。

更多信息请参见 [创建 AWS Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)。