---
title: 创建 {{{ .premium }}} 实例
summary: 了解如何创建 {{{ .premium }}} 实例。
---

# 创建 {{{ .premium }}} 实例

本文档介绍如何在 [TiDB Cloud console](https://tidbcloud.com/) 中创建 {{{ .premium }}} 实例。

> **注意：**
>
> 如需了解如何创建 TiDB Cloud Dedicated 集群，请参见 [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)。

## 开始之前 {#before-you-begin}

如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/signup)注册账号。

<CustomContent language="en,zh">

- 你可以使用电子邮箱和密码注册，以便通过 TiDB Cloud 管理密码；也可以使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。为此，请在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。为此，请在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。为此，请在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账号。
- 对于 Alibaba Cloud Marketplace 用户，你也可以通过 Alibaba Cloud Marketplace 注册。为此，请在 [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账号。

</CustomContent>

<CustomContent language="ja">

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

</CustomContent>

## 步骤 {#steps}

如果你拥有 `Organization Owner` 角色，可以按如下方式创建 {{{ .premium }}} 实例：

1. 在 [TiDB Cloud console](https://tidbcloud.com/tidbs) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击右上角的 **Create Resource**。
2. 在 **Create Resource** 页面，选择 **Premium** 作为你的套餐。
3. 输入 {{{ .premium }}} 实例的名称，然后选择要托管实例的云服务提供商和区域。
4. （可选）如需将此 {{{ .premium }}} 实例归入某个项目以便管理，请点击 **Group Your Instance in a Project**，然后为该实例选择目标项目。如果你的组织中还没有项目，可以点击 **Create a Project** 创建一个。
5. 在 **Capacity** 区域，为实例设置 Request Capacity Units (RCUs) 的最大数量。RCU 表示为你的工作负载预配的计算资源。TiDB Cloud 会根据需求在此范围内自动扩缩容你的实例。

    > **注意：**
    > 
    > - 最大 RCU 值必须以 100 为增量进行设置。
    > - 系统会按最小 RCU 数量向你计费，该值称为 **Minimum Billing RCU**。此值取以下两者中的较大者：你所配置最大 RCU 的 25% 和 5,000 RCUs。最小计费 RCU 可确保为峰值性能预留专用资源。即使你的实际使用量更低，也会按此最小值收费。

6. 对于 {{{ .premium }}} 实例，仅启用区域级高可用，且不可配置。更多信息，请参见 [High Availability](/tidb-cloud/serverless-high-availability.md)。

7. 点击 **Create**。

    实例创建过程随即开始。如果这是你在所选区域中的第一个实例，预配通常需要约 30 分钟。如果所选区域中已存在实例，则过程会更快，通常约 1 分钟内完成。

## 下一步 {#what-s-next}

实例创建完成后，请按照 [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/premium/connect-to-premium-via-public-connection.md) 中的说明为你的实例创建密码。

> **注意：**
>
> 如果你未设置密码，则无法连接到该实例。