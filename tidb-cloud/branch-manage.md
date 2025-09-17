---
title: 管理 TiDB Cloud 分支
summary: 了解如何管理 TiDB Cloud 分支。
---

# 管理 TiDB Cloud 分支

本文档介绍如何使用 [TiDB Cloud 控制台](https://tidbcloud.com) 管理你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的分支。若需使用 TiDB Cloud CLI 进行管理，请参见 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)。

## 所需权限

- 若要[创建分支](#create-a-branch)或[连接到分支](#connect-to-a-branch)，你必须是组织的 `Organization Owner` 角色或目标项目的 `Project Owner` 角色。
- 若要[查看项目中集群的分支](#create-a-branch)，你必须属于该项目。

关于权限的更多信息，请参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

## 创建分支

> **Note:**
>
> 你只能为 2023 年 7 月 5 日之后创建的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群创建分支。更多限制请参见 [限制与配额](/tidb-cloud/branch-overview.md#limitations-and-quotas)。

创建分支，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Branches**。
3. 在 **Branches** 页面右上角，点击 **Create Branch**。此时会弹出对话框。

    或者，你也可以从已有的父分支创建分支，找到目标父分支所在行，然后点击 **...** > **Create Branch**（在 **Action** 列）。

4. 在 **Create Branch** 对话框中，配置以下选项：

    - **Name**：输入分支名称。
    - **Parent branch**：选择原始集群或已有分支。`main` 代表当前集群。
    - **Include data up to**：选择以下之一：
        - **Current point in time**：从当前状态创建分支。
        - **Specific date and time**：从指定时间点创建分支。

5. 点击 **Create**。

根据你集群中的数据量，分支创建将在几分钟内完成。

## 查看分支

要查看集群的分支，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Branches**。

    集群的分支列表会显示在右侧面板。

## 连接到分支

要连接到分支，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Branches**。
3. 在目标分支所在行的 **Action** 列，点击 **...**。
4. 在下拉列表中点击 **Connect**。此时会弹出连接信息对话框。
5. 点击 **Generate Password** 或 **Reset Password**，以创建或重置 root 密码。
6. 使用连接信息连接到该分支。

另外，你也可以在集群概览页面获取连接字符串：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在右上角点击 **Connect**。
3. 在 `Branch` 下拉列表中选择你要连接的分支。
4. 点击 **Generate Password** 或 **Reset Password**，以创建或重置 root 密码。
5. 使用连接信息连接到该分支。

## 删除分支

要删除分支，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Branches**。
3. 在目标分支所在行的 **Action** 列，点击 **...**。
4. 在下拉列表中点击 **Delete**。
5. 确认删除操作。

## 重置分支

重置分支会将其与父分支的最新数据进行同步。

> **Note:**
> 
> 此操作不可逆。在重置分支前，请确保你已备份所有重要数据。

要重置分支，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Branches**。
3. 在目标分支所在行的 **Action** 列，点击 **...**。
4. 在下拉列表中点击 **Reset**。
5. 确认重置操作。

## 后续操作

- [将 TiDB Cloud 分支集成到你的 GitHub CI/CD 流水线](/tidb-cloud/branch-github-integration.md)