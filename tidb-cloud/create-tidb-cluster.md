---
title: 创建 TiDB Cloud Dedicated 集群
summary: 了解如何创建你的 TiDB Cloud Dedicated 集群。
---

# 创建 TiDB Cloud Dedicated 集群

本教程将指导你注册并创建一个 TiDB Cloud Dedicated 集群。

> **Tip:**
>
> 如果你想了解如何创建 TiDB Cloud Serverless 集群，请参见 [Create a TiDB Cloud Serverless Cluster](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 开始之前

如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/signup)注册账号。

- 你可以使用邮箱和密码注册，这样你可以通过 TiDB Cloud 管理你的密码，或者使用 Google、GitHub 或 Microsoft 账号注册。
- 对于 AWS Marketplace 用户，你也可以通过 AWS Marketplace 注册。方法是，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Azure Marketplace 用户，你也可以通过 Azure Marketplace 注册。方法是，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。
- 对于 Google Cloud Marketplace 用户，你也可以通过 Google Cloud Marketplace 注册。方法是，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的指引设置你的 TiDB Cloud 账号。

## （可选）步骤 1. 使用默认项目或创建新项目

登录 [TiDB Cloud 控制台](https://tidbcloud.com/) 后，你会有一个默认的 [project](/tidb-cloud/tidb-cloud-glossary.md#project)。当你的组织中只有一个项目时，集群会被创建在该项目下。关于项目的更多信息，请参见 [Organizations and projects](/tidb-cloud/manage-user-access.md#organizations-and-projects)。

如果你是组织所有者，可以根据需要重命名默认项目或为集群创建新项目，操作如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左上角的下拉框。你的默认组织和项目会显示出来。

2. 点击你的组织名称，然后在左侧导航栏点击 **Projects**。

3. 在 **Projects** 页面，执行以下操作之一：

    - 若要重命名默认项目，在 **Actions** 列点击 **...** > **Rename**。
    - 若要创建新项目，点击 **Create New Project**，输入项目名称，然后点击 **Confirm**。

4. 若要进入项目的集群列表页面，在 **Projects** 页面点击项目名称。

## 步骤 2. 创建 TiDB Cloud Dedicated 集群

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以按照以下步骤创建 TiDB Cloud Dedicated 集群：

1. 进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击 **Create Cluster**。

3. 在 **Create Cluster** 页面，选择 **Dedicated**，然后按如下方式配置集群信息：

    1. 选择云服务商和区域。

        > **Note:**
        >
        > - 目前，TiDB Cloud Dedicated 集群在 Azure 上的支持处于公开预览阶段。
        > - 如果你是通过 [AWS Marketplace](https://aws.amazon.com/marketplace) 注册的 TiDB Cloud，云服务商为 AWS，且无法在 TiDB Cloud 中更改。
        > - 如果你是通过 [Azure Marketplace](https://azuremarketplace.microsoft.com) 注册的 TiDB Cloud，云服务商为 Azure Cloud，且无法在 TiDB Cloud 中更改。
        > - 如果你是通过 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册的 TiDB Cloud，云服务商为 Google Cloud，且无法在 TiDB Cloud 中更改。

    2. 分别为 TiDB、TiKV 和 TiFlash（可选）配置 [cluster size](/tidb-cloud/size-your-cluster.md)。
    3. 如有需要，修改默认集群名称和端口号。
    4. 如果该区域尚未配置 CIDR，则需要设置 CIDR。如果你没有看到 **Project CIDR** 字段，说明该区域已配置了 CIDR。

        > **Note:**
        >
        > - 当该区域的第一个集群创建时，TiDB Cloud 会使用该 CIDR 创建一个 VPC。该区域同一项目下的后续集群都会使用该 VPC。
        > - 设置 CIDR 时，请避免与你应用所在 VPC 的 CIDR 冲突。VPC 创建后，CIDR 无法修改。

4. 在右侧确认集群和计费信息。

5. 如果你还没有添加支付方式，请点击右下角的 **Add Credit Card**。

    > **Note:**
    >
    > 如果你是通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册的 TiDB Cloud，可以直接通过 AWS 账号、Azure 账号或 Google Cloud 账号支付，但无法在 TiDB Cloud 控制台添加支付方式或下载发票。

6. 点击 **Create**。

    你的 TiDB Cloud 集群将在大约 20 到 30 分钟内创建完成。

## 步骤 3. 设置 root 密码

集群创建完成后，按照以下步骤设置 root 密码：

1. 在集群概览页面右上角，点击 **...** 并选择 **Password Settings**。

2. 设置连接集群所需的 root 密码，然后点击 **Save**。

    你可以点击 **Auto-generate Password** 自动生成一个随机密码。生成的密码不会再次显示，请妥善保存你的密码。

## 后续操作

在 TiDB Cloud 上创建集群后，你可以通过 [Connect to Your TiDB Cloud Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md) 中提供的方法连接到你的集群。