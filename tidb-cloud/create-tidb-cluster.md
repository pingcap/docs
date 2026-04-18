---
title: 创建 TiDB Cloud Dedicated 集群
summary: 了解如何创建你的 TiDB Cloud Dedicated 集群。
---

# 创建 TiDB Cloud Dedicated 集群

本教程将指导你注册并创建 TiDB Cloud Dedicated 集群。

> **提示：**
>
> 如需了解如何创建 TiDB Cloud Starter 或 TiDB Cloud Essential 实例，请参阅 [创建 TiDB Cloud Starter 或 Essential 实例](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 开始之前

如果你还没有 TiDB Cloud 账户，请点击[这里](https://tidbcloud.com/signup)注册账户。

- 你可以使用邮箱和密码注册，这样你可以通过 TiDB Cloud 管理你的密码，或者使用 Google、GitHub 或 Microsoft 账户注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。方法是，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账户。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。方法是，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账户。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。方法是，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账户。

## 第 1 步：创建 TiDB Cloud Dedicated 集群 {#step-1-create-a-tidb-cloud-dedicated-cluster}

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以按如下步骤创建 TiDB Cloud Dedicated 集群：

1. 导航到 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 点击 **Create Resource**。

3. 在 **Create Resource** 页面，选择 **Dedicated**，然后按如下方式配置信息：

    1. 为你的 TiDB Cloud Dedicated 集群选择一个项目。如果你的组织中还没有项目，可以点击 **Create a Project** 创建一个项目。
    2. 输入 TiDB Cloud Dedicated 集群的名称。
    3. 选择要托管集群的云服务提供商和区域。

        > **注意：**
        >
        > - 目前，TiDB Cloud Dedicated 对 Azure 的支持处于公开预览阶段。
        > - 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace) 注册 TiDB Cloud，则云服务提供商为 AWS，且无法在 TiDB Cloud 中更改。
        > - 如果你通过 [Azure Marketplace](https://azuremarketplace.microsoft.com) 注册 TiDB Cloud，则云服务提供商为 Azure Cloud，且无法在 TiDB Cloud 中更改。
        > - 如果你通过 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud，则云服务提供商为 Google Cloud，且无法在 TiDB Cloud 中更改。

    4. 分别为 TiDB、TiKV 和 TiFlash（可选）配置[集群规模](/tidb-cloud/size-your-cluster.md)。
    5. 如有需要，更新默认端口号。
    6. 如果尚未为该区域配置 CIDR，则需要设置 CIDR。如果你没有看到 **Project CIDR** 字段，则表示该区域已配置 CIDR。

        > **注意：**
        >
        > - TiDB Cloud 会在该区域创建第一个集群时，使用此 CIDR 创建一个 VPC。此后，同一项目在该区域中的所有集群都将使用此 VPC。
        > - 设置 CIDR 时，请避免与应用所在 VPC 的 CIDR 冲突。VPC 创建后，CIDR 无法修改。

4. 在右侧确认集群和账单信息。

5. 如果你尚未添加支付方式，请点击右下角的 **Add Credit Card**。

    > **注意：**
    >
    > 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud，你可以直接通过 AWS 账户、Azure 账户或 Google Cloud 账户支付，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

6. 点击 **Create**。

    TiDB Cloud 集群大约会在 20 到 30 分钟内创建完成。创建完成后，你将收到来自 TiDB Cloud 控制台的通知。

    > **注意：**
    >
    > 集群创建时间因区域而异，可能会超过 30 分钟。如果创建过程明显超出预期，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 第 2 步：设置 root 密码 {#step-2-set-the-root-password}

TiDB Cloud Dedicated 集群创建完成后，按以下步骤设置 root 密码：

1. 在集群概览页面右上角，点击 **...**，然后选择 **Password Settings**。

2. 设置用于连接集群的 root 密码，然后点击 **Save**。

    你可以点击 **Auto-generate Password** 生成随机密码。生成的密码不会再次显示，因此请将密码保存在安全的位置。

## 后续操作

在 TiDB Cloud 上创建 TiDB Cloud Dedicated 集群后，你可以通过 [连接到你的 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md) 中提供的方法进行连接。
