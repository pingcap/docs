---
title: 创建 TiDB Cloud Serverless 集群
summary: 了解如何创建你的 TiDB Cloud Serverless 集群。
---

# 创建 TiDB Cloud Serverless 集群

本文档介绍如何在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中创建 TiDB Cloud Serverless 集群。

> **Tip:**
>
> 如果你想了解如何创建 TiDB Cloud Dedicated 集群，请参见 [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)。

## 开始之前

如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/signup)注册账号。

- 你可以使用邮箱和密码注册，这样你可以通过 TiDB Cloud 管理你的密码，或者使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。具体操作为，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。具体操作为，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。具体操作为，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。

## 操作步骤

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以按照以下步骤创建 TiDB Cloud Serverless 集群：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

2. 点击 **Create Cluster**。

3. 在 **Create Cluster** 页面，**Serverless** 会被默认选中。

4. TiDB Cloud Serverless 的云服务商为 AWS。你可以选择希望托管集群的 AWS 区域。

5. 如有需要，可以修改默认的集群名称。

6. 选择集群方案。TiDB Cloud Serverless 提供两种 [集群方案](/tidb-cloud/select-cluster-tier.md#cluster-plans)：**Free Cluster** 和 **Scalable Cluster**。你可以从免费集群开始，随着需求增长再升级为可扩展集群。创建可扩展集群时，你需要指定 **Monthly Spending Limit** 并添加信用卡。

    > **Note:**
    >
    > 每个 TiDB Cloud 组织默认最多可以创建 5 个 [免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。如需创建更多 TiDB Cloud Serverless 集群，你需要添加信用卡并创建 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)以供使用。

7. 点击 **Create**。

    集群创建流程将启动，你的 TiDB Cloud 集群将在大约 30 秒内创建完成。

## 后续操作

集群创建完成后，请按照 [Connect to TiDB Cloud Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) 的指引为你的集群创建密码。

> **Note:**
>
> 如果你未设置密码，将无法连接到集群。