---
title: 通过 Private Link 连接在 AWS 上连接到 Confluent Cloud
summary: 了解如何使用 AWS Endpoint Service private link 连接，在 AWS 上连接到 Confluent Cloud Dedicated 集群。
---

# 通过 Private Link 连接在 AWS 上连接到 Confluent Cloud

本文档介绍如何通过 [AWS Endpoint Service private link 连接](/tidb-cloud/serverless-private-link-connection.md)，将 TiDB Cloud Essential 集群连接到 [Confluent Cloud Dedicated 集群](https://docs.confluent.io/cloud/current/clusters/cluster-types.html)（部署在 AWS 上）。

> **注意**
>
> 在 AWS 上的所有 Confluent Cloud 集群类型中，只有 Confluent Cloud Dedicated 集群支持 private link 连接。

## 前提条件

- 你拥有一个 [Confluent Cloud](https://confluent.cloud/) 账户。

- 你的 TiDB Cloud Essential 托管在 AWS 上，并且处于活跃状态。请提前获取并保存以下信息：

    - AWS 账户 ID
    - 可用区（AZ）

要查看 AWS 账户 ID 和可用区，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 TiDB 集群的集群概览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹出的对话框中，你可以找到 AWS 账户 ID 和可用区信息。

## 第 1 步：设置 Confluent Cloud 网络

确定你要使用的 Confluent Cloud 网络，或[在 AWS 上创建新的 Confluent Cloud 网络](https://docs.confluent.io/cloud/current/networking/ccloud-network/aws.html#create-ccloud-network-aws)。

Confluent Cloud 网络必须满足以下要求：

- 类型：网络必须为 **PrivateLink** 网络。
- Region 匹配：网络必须与 TiDB Cloud Essential 集群位于同一 AWS Region。
- 可用区（AZ）可用性：网络的可用区必须与 TiDB Cloud Essential 集群的可用区有重叠。

要获取 Confluent Cloud 网络的唯一名称，请执行以下步骤：

1. 在 [Confluent Cloud 控制台](https://confluent.cloud/)中，进入 [**Environments**](https://confluent.cloud/environments) 页面，然后点击你的 Confluent Cloud 网络所在的 environment。
2. 点击 **Network management** 并选择 **For dedicated clusters**，找到你创建的网络。
3. 进入 **Network overview** 页面，获取 Confluent Cloud 网络的 DNS 子域名。
4. 从 DNS 子域名中提取 Confluent Cloud 网络的唯一名称。例如，如果 DNS 子域名为 `use1-az1.domnprzqrog.us-east-1.aws.confluent.cloud`，则唯一名称为 `domnprzqrog.us-east-1`。
5. 保存该唯一名称以备后用。

## 第 2 步：为网络添加 PrivateLink Access

为你在 [第 1 步](#第-1-步设置-confluent-cloud-网络)中确定或设置的网络添加 PrivateLink Access。详细信息请参见 [在 Confluent Cloud 中添加 PrivateLink Access](https://docs.confluent.io/cloud/current/networking/private-links/aws-privatelink.html#add-a-privatelink-access-in-ccloud)。

在此过程中，你需要：

- 提供在 [前提条件](#前提条件) 中获取的 TiDB Cloud AWS 账户 ID。
- 保存 Confluent Cloud 提供的 `VPC Service Endpoint`，以备后用，通常格式为 `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`。

## 第 3 步：在该网络下创建 Confluent Cloud Dedicated 集群

在你于 [第 1 步](#第-1-步设置-confluent-cloud-网络)中设置的现有网络下，创建 Confluent Cloud Dedicated 集群。详细信息请参见 [在 Confluent Cloud 中创建 dedicated 集群](https://docs.confluent.io/cloud/current/clusters/create-cluster.html#create-ak-clusters)。

## 第 4 步：在 TiDB Cloud 中创建 private link 连接

要在 TiDB Cloud 中创建 private link 连接，请执行以下操作：

1. 使用 Confluent Cloud 提供的 `VPC Service Endpoint`，在 TiDB Cloud 中创建 private link 连接。

    详细信息请参见 [创建 AWS Endpoint Service private link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)。

    > **注意：**
    >
    > 对于 AWS 上的 Confluent Cloud Dedicated 集群，你无需在 AWS 控制台的 endpoint service 详情页手动接受来自 TiDB Cloud 的 endpoint 连接请求。Confluent Cloud 会自动处理该请求。

2. 将 Confluent Cloud 的服务域名附加到 private link 连接，以便 TiDB Cloud 中的数据流服务可以访问 Confluent 集群。

    详细信息请参见 [将域名附加到 private link 连接](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)。