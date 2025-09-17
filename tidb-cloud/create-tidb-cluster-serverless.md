---
title: 创建 TiDB Cloud Starter 或 Essential 集群
summary: 了解如何创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
---

# 创建 TiDB Cloud Starter 或 Essential 集群

本文档介绍如何在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

> **Tip:**
>
> 如果你想了解如何创建 TiDB Cloud Dedicated 集群，请参见 [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)。

## 开始之前

如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/signup)注册账号。

<CustomContent language="en,zh">

- 你可以使用邮箱和密码注册，这样可以通过 TiDB Cloud 管理你的密码，或者使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。方法是，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照页面提示设置你的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。方法是，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照页面提示设置你的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。方法是，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照页面提示设置你的 TiDB Cloud 账号。
- 对于阿里云云市场用户，你也可以通过阿里云云市场注册。方法是，在 [阿里云云市场](https://marketplace.alibabacloud.com/) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照页面提示设置你的 TiDB Cloud 账号。

</CustomContent>

<CustomContent language="ja">

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

</CustomContent>

## 操作步骤

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以按照以下步骤创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

2. 点击 **Create Cluster**。

3. 选择集群方案和云服务商。

    <CustomContent language="en,zh">

    - 对于 AWS，你可以从 **Starter** 集群开始。
    - 对于阿里云，你可以从 **Starter** 集群开始，随着需求增长可以升级到 **Essential** 集群。

    </CustomContent>

    <CustomContent language="ja">

    For AWS, you can start with a **Starter** cluster.

    </CustomContent>

    更多信息请参见 [cluster plans](/tidb-cloud/select-cluster-tier.md)。

4. 选择你希望部署集群的区域。

5. 如有需要，修改默认的集群名称。

6. 修改集群的容量配置。

    - **Starter** 方案：

        - 你可以设置集群的消费上限。如果消费上限设置为 0，集群将保持免费。如果消费上限大于 0，则需要在创建集群前添加信用卡。

        - 默认情况下，每个组织最多可以创建五个[免费 Starter 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。如需创建更多 Starter 集群，必须添加信用卡并指定消费上限。

    - **Essential** 方案：

        - 你必须为集群指定最小和最大 Request Capacity Units（RCUs）。

        - RCU 代表为你的工作负载分配的计算资源。TiDB Cloud 会根据需求在该范围内自动扩缩容。

7. 点击 **Create**。

    集群创建流程将启动，你的 TiDB Cloud 集群将在大约 30 秒内创建完成。

## 后续操作

集群创建完成后，请按照 [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) 的说明为你的集群创建密码。

> **Note:**
>
> 如果你未设置密码，将无法连接到集群。