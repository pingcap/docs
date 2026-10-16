---
title: 创建 TiDB Cloud Starter 或 Essential 实例
summary: 了解如何创建 TiDB Cloud Starter 或 TiDB Cloud Essential 实例。
---

# 创建 TiDB Cloud Starter 或 Essential 实例

本文档介绍如何在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中创建 TiDB Cloud Starter 或 TiDB Cloud Essential 实例。

> **Tip:**
>
> 如果你想了解如何创建 TiDB Cloud Dedicated 集群，请参见 [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)。

## 开始之前

如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/signup)注册账号。

<CustomContent language="en,zh">

- 你可以使用邮箱和密码注册，这样可以通过 TiDB Cloud 管理你的密码，或者使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。方法是，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。方法是，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。方法是，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于阿里云云市场用户，你也可以通过阿里云云市场注册。方法是，在 [阿里云云市场](https://marketplace.alibabacloud.com/) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。

</CustomContent>

<CustomContent language="ja">

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

</CustomContent>

> **注意：**
>
> PostgreSQL 兼容的 TiDB Cloud Starter 当前处于公测阶段。创建 Starter 实例时，你可以选择 PostgreSQL 兼容模式。

## 操作步骤

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以按照以下步骤创建 TiDB Cloud Starter 或 TiDB Cloud Essential 实例：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

2. 点击 **Create Resource**。

3. 选择一个方案。

    你可以选择 **Starter** 或 **Essential**。

    对于 MySQL 兼容的工作负载，你可以从 Starter 实例开始，随着需求增长，后续可以升级到 Essential 实例。更多信息请参见 [选择方案](/tidb-cloud/select-cluster-tier.md)。

4. 如果你选择 **Starter**，请在 **Compatibility Mode** 部分选择以下选项之一：

    - **MySQL Compatible**：TiDB Cloud Starter 的默认兼容模式。
    - **PostgreSQL Compatible**：提供 PostgreSQL 兼容性，当前处于公测阶段。此兼容模式仅适用于 TiDB Cloud Starter。

5. 输入实例名称，然后选择你希望托管实例的云服务商和区域。

6. （可选）如需将此实例归入某个项目以便管理，请点击 **Group Your Instance in a Project**，然后为该实例选择目标项目。如果你的组织中还没有项目，可以点击 **Create a Project** 创建一个项目。

7. 根据所选方案和兼容模式配置或查看容量和用量配额。有关每种 Starter 兼容模式的免费用量配额，请参见 [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter)。

    - **MySQL-compatible Starter**：

        - 你可以修改 TiDB Cloud Starter 实例的消费上限。如果消费上限设置为 0，实例将保持免费。如果消费上限大于 0，则需要在创建实例前添加信用卡。
        - 默认情况下，每个组织最多可以创建五个免费的 MySQL-compatible Starter 实例。如需创建更多实例，必须添加信用卡并指定消费上限。

    - **PostgreSQL-compatible Starter**：

        在公测期间，每个组织最多可以创建 10 个免费的 PostgreSQL-compatible Starter 实例。

        当实例达到其免费配额时，超出的资源消耗可能会受到用量限制或服务暂停。如果你预计会超出免费用量配额，请联系 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 讨论你的需求。

    - **Essential**：

        - 对于运行在 CLOUD.202603.x 或更高版本上的 {{{ .essential }}} 实例，默认选中 **Elastic Mode**。在 Elastic Mode 下，你无需设置最大 RCU 数。相反，你的实例会使用固定的 **Baseline RCU** 2,000 RCU，这是向你计费的最小 Request Capacity Units（RCUs）数量，也是自动扩缩容的初始容量。

        - 如需限制容量，请选择 **Limited Mode**，然后指定实例可扩展到的最大 RCU 数。以下版本上的 {{{ .essential }}} 实例不支持 Elastic Mode；对于这些实例，你需要同时指定最小和最大 RCU 数。

        - RCU 代表为你的工作负载分配的计算资源。TiDB Cloud 会根据需求自动扩缩 {{{ .essential }}} 实例。如果你的工作负载持续需要超过 100,000 RCU，建议升级到 {{{ .premium }}} 以避免潜在瓶颈。

8. 点击 **Create**。

实例创建流程将启动，你的实例将在大约 30 秒内创建完成。

## 后续操作

- {{{ .starter }}} 或 Essential 实例创建完成后，请按照 [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) 的指引为你的实例创建密码。

    > **Note:**
    >
    > 如果你未设置密码，将无法连接到 {{{ .starter }}} 或 Essential 实例。

- 如需使用 TiDB Cloud CLI 管理你的实例，请参见 [TiDB Cloud CLI Reference (PREVIEW)](/tidb-cloud/cli-reference.md)。
