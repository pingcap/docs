---
title: 管理 TiDB Cloud 资源和项目
summary: 了解如何在 My TiDB 页面上管理你的 TiDB Cloud 资源和项目。
---

# 管理 TiDB Cloud 资源和项目

在 [TiDB Cloud console](https://tidbcloud.com/) 中，你可以在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面发现、访问并管理你所在组织中的所有 TiDB Cloud 资源和项目。

## 什么是 TiDB Cloud 资源和项目？ {#what-are-tidb-cloud-resources-and-projects}

### TiDB Cloud 资源 {#tidb-cloud-resources}

TiDB Cloud 资源是你可以管理的可部署单元。它可以是以下之一：

- TiDB X 实例，即一种面向服务的 TiDB Cloud 产品，基于 [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md) 构建，例如 {{{ .starter }}}, Essential, 或 Premium 实例
- 一个 {{{ .dedicated }}} 集群

### TiDB Cloud 项目 {#tidb-cloud-projects}

在 TiDB Cloud 中，你可以使用 [projects](/tidb-cloud/tidb-cloud-glossary.md#project) 来组织和管理你的 TiDB Cloud 资源。

- 对于 TiDB X 实例，项目是可选的，这意味着你既可以将这些实例归入某个项目，也可以将它们保留在组织级别。
- 对于 {{{ .dedicated }}} 集群，项目是必需的。

## 管理 TiDB Cloud 资源 {#manage-tidb-cloud-resources}

本节介绍如何使用 [**My TiDB**](https://tidbcloud.com/tidbs) 页面查看、创建和管理 TiDB Cloud 资源。

### 查看 TiDB Cloud 资源 {#view-tidb-cloud-resources}

默认情况下，[**My TiDB**](https://tidbcloud.com/tidbs) 页面显示资源视图，其中展示了你当前组织内所有你有权限访问的资源。

如果你的组织有很多实例或集群，你可以使用页面顶部的筛选器快速找到所需内容。

要查看某个 TiDB Cloud 资源的详细信息，请点击目标资源的名称进入其概览页面。

### 创建 TiDB Cloud 资源 {#create-tidb-cloud-resources}

要创建 TiDB Cloud 资源，请进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Create Resource**。

更多信息，请参见以下文档：

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/create-tidb-cluster-serverless.md)

- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)

- [Create a {{{ .dedicated }}} Cluster](/tidb-cloud/create-tidb-cluster.md)

### 管理 TiDB Cloud 资源 {#manage-tidb-cloud-resources}

在 **My TiDB** 页面上，你可以点击目标资源所在行中的 **...**，对 TiDB Cloud 资源执行快速操作，例如删除、重命名和导入数据。

要执行更多操作并管理特定 TiDB Cloud 资源的设置，请点击目标资源的名称进入其概览页面。

## 管理 TiDB Cloud 项目 {#manage-tidb-cloud-projects}

本节介绍如何使用 [**My TiDB**](https://tidbcloud.com/tidbs) 页面查看、创建和管理 TiDB Cloud 项目。

### 查看项目 {#view-projects}

要按项目分组查看你的 TiDB Cloud 资源，请在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面点击 **Project view** 标签页。

> **Tip:**
>
> 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

在项目视图中，你可以看到你在该组织中所属的项目：

- 不属于任何项目的 TiDB X 实例会显示在名为 `Out of project` 的表中。
- 属于特定项目的 TiDB X 实例会显示在对应的 TiDB X 项目表中。
- TiDB Cloud Dedicated 集群会显示在对应的 Dedicated 项目表中。这些表的文件夹图标中带有 **D**，用于标识 **Dedicated** 项目类型。

### 创建项目 {#create-a-project}

> **Note:**
>
> - 免费试用用户不能创建新项目。
> - 对于 TiDB X 实例，创建项目是可选的。对于 TiDB Cloud Dedicated 集群，你必须使用默认项目或创建新项目来管理它们。

如果你具有 `Organization Owner` 角色，则可以在你的组织中创建项目。

要创建新项目，请执行以下步骤：

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Create Project**。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 在显示的对话框中，输入项目名称。

3. 根据你要为哪种类型的 TiDB Cloud 资源创建项目，执行以下操作之一：

    - 如果该项目是为 TiDB X 实例创建的，点击 **Confirm**。

        > **Note:**
        >
        > 对于 {{{ .premium }}} 实例，加密是按实例而不是按项目配置的。创建实例后，你可以启用 [Dual-Layer Data Encryption](/tidb-cloud/premium/dual-layer-data-encryption-premium.md)，在默认的存储层加密之上增加数据库层加密。

    - 如果该项目是为 {{{ .dedicated }}} 集群创建的，选择 **Create for Dedicated Cluster** 选项，为该项目配置 [Customer-Managed Encryption Keys (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md) 和 [maintenance window](/tidb-cloud/configure-maintenance-window.md)，然后点击 **Confirm**。

### 管理项目 {#manage-a-project}

如果你具有 `Organization Owner` 或 `Project Owner` 角色，则可以管理你的项目。

要管理项目，请执行以下步骤：

1. 在 TiDB Cloud console 中，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

2. 在项目视图中，找到目标项目，然后按如下方式进行管理：

    - 对于 TiDB X 和 TiDB Dedicated 项目，你都可以点击目标项目所在行中的 **...**，对项目执行快速操作，例如重命名项目或邀请成员加入项目。更多信息，请参见 [Manage project access](/tidb-cloud/manage-user-access.md)。
    - 对于 TiDB Dedicated 项目，你还可以点击目标项目所在行中的 <MDSvgIcon name="icon-project-settings" /> 图标，按项目管理 {{{ .dedicated }}} 集群的设置，例如网络、维护、告警订阅和加密访问。

### 在项目之间移动 TiDB X 实例 {#move-a-tidb-x-instance-between-projects}

如果你具有 `Organization Owner` 或 `Project Owner` 角色，则可以将 TiDB X 实例移动到某个项目中，或移出所有项目。

> **Note:**
>
> 只有 TiDB X 实例支持在 TiDB X 项目之间移动以及移出所有 TiDB X 项目。TiDB Cloud Dedicated 集群不支持在项目之间移动。

要移动 TiDB X 实例，请执行以下步骤：

1. 在 [TiDB Cloud console](https://tidbcloud.com)，进入你所在组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击 **Project view** 标签页。

2. 在项目视图中，展开包含待移动 TiDB X 实例的项目文件夹，点击目标 TiDB X 实例的 **...**，然后点击 **Move**。

    > **Tip:**
    >
    > 如果 TiDB X 实例不在任何项目中，它会显示在 **Out of project** 文件夹中。

3. 在显示的对话框中，执行以下操作之一：

    - 要将 TiDB X 实例移动到某个项目，选择 **To a project**，然后从下拉列表中选择目标项目。
    - 要将 TiDB X 实例移出所有项目，选择 **Outside any project**。

4. 点击 **Move**。