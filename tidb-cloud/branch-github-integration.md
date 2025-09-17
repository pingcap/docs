---
title: 集成 TiDB Cloud Branching（Beta）与 GitHub
summary: 了解如何将 TiDB Cloud Branching 功能与 GitHub 集成。
---

# 集成 TiDB Cloud Branching（Beta）与 GitHub

> **Note:**
>
> 此集成基于 [TiDB Cloud Branching](/tidb-cloud/branch-overview.md)。在阅读本文档前，请确保你已熟悉 TiDB Cloud Branching。

如果你在应用开发中使用 GitHub，可以将 TiDB Cloud Branching 集成到你的 GitHub CI/CD 流水线中，从而让你能够在不影响生产数据库的情况下，使用分支自动测试你的 pull request。

在集成过程中，你会被提示安装 [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub 应用。该应用可以根据你 GitHub 仓库中的 pull request，自动管理 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的分支。例如，当你创建一个 pull request 时，应用会为你的集群创建一个对应的分支，你可以在该分支中独立开发新功能或修复 bug，而不会影响生产数据库。

本文档涵盖以下内容：

1. 如何将 TiDB Cloud Branching 与 GitHub 集成
2. TiDB Cloud Branching 应用的工作原理
3. 如何构建基于分支的 CI 工作流，使用分支而非生产集群测试每个 pull request

## 开始前的准备

在集成前，请确保你具备以下条件：

- 一个 GitHub 账号
- 一个用于你的应用的 GitHub 仓库
- 一个 [TiDB Cloud Starter 或 TiDB Cloud Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

## 将 TiDB Cloud Branching 集成到你的 GitHub 仓库 {#integrate-branching-with-your-github-repository}

要将 TiDB Cloud Branching 集成到你的 GitHub 仓库，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。

2. 在左侧导航栏点击 **Branches**。

3. 在 **Branches** 页面右上角，点击 **Connect to GitHub**。

    - 如果你尚未登录 GitHub，会被要求先登录 GitHub。
    - 如果是你首次使用该集成，会被要求授权 **TiDB Cloud Branching** 应用。

   <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4. 在 **Connect to GitHub** 对话框中，在 **GitHub Account** 下拉列表中选择一个 GitHub 账号。

    如果你的账号不在列表中，点击 **Install Other Account**，然后按照屏幕提示安装该账号。

5. 在 **GitHub Repository** 下拉列表中选择你的目标仓库。如果列表较长，可以通过输入名称进行搜索。

6. 点击 **Connect**，将你的集群与 GitHub 仓库进行连接。

   <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloud Branching 应用行为

当你将 TiDB Cloud Starter 或 TiDB Cloud Essential 集群与 GitHub 仓库连接后，对于该仓库中的每个 pull request，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub 应用都可以自动管理集群的对应分支。以下是 pull request 变更的默认行为列表：

| Pull request 变更                  | TiDB Cloud Branching 应用行为                                                                                                                                                                                                                                                                                                                                        |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 创建 pull request                  | 当你在仓库中创建 pull request 时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用会为你的集群创建一个分支。当 `branch.mode` 设置为 `reset` 时，分支名称为 `${github_branch_name}_${pr_id}` 格式。当 `branch.mode` 设置为 `reserve` 时，分支名称为 `${github_branch_name}_${pr_id}_${commit_sha}` 格式。注意，分支数量有 [限制](/tidb-cloud/branch-overview.md#limitations-and-quotas)。 |
| 向 pull request 推送新提交         | 当 `branch.mode` 设置为 `reset` 时，每次你向仓库中的 pull request 推送新提交，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用会重置该分支。当 `branch.mode` 设置为 `reserve` 时，应用会为最新提交创建一个新分支。                                                                                                                            |
| 关闭或合并 pull request            | 当你关闭或合并 pull request 时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用会删除该 pull request 对应的分支。                                                                                                                                                                                                                         |
| 重新打开 pull request              | 当你重新打开 pull request 时，[TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用会为该 pull request 的最新提交创建一个分支。                                                                                                                                                                                                                 |

## 配置 TiDB Cloud Branching 应用

要配置 [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) 应用的行为，你可以在仓库根目录下添加一个 `tidbcloud.yml` 文件，并根据以下说明将所需配置添加到该文件中。

### branch.blockList

**类型：** 字符串数组。**默认值：** `[]`。

指定禁止 TiDB Cloud Branching 应用的 GitHub 分支，即使这些分支在 `allowList` 中。

```yaml
github:
    branch:
        blockList:
            - ".*_doc"
            - ".*_blackList"
```

### branch.allowList

**类型：** 字符串数组。**默认值：** `[.*]`。

指定允许 TiDB Cloud Branching 应用的 GitHub 分支。

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### branch.mode

**类型：** 字符串。**默认值：** `reset`。

指定 TiDB Cloud Branching 应用如何处理分支更新：

- 如果设置为 `reset`，TiDB Cloud Branching 应用会用最新数据更新已有分支。
- 如果设置为 `reserve`，TiDB Cloud Branching 应用会为你的最新提交创建一个新分支。

```yaml
github:
    branch:
        mode: reset
```

### branch.autoDestroy

**类型：** 布尔值。**默认值：** `true`。

如果设置为 `false`，当 pull request 被关闭或合并时，TiDB Cloud Branching 应用不会删除 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的分支。

```yaml
github:
    branch:
        autoDestroy: true
```

## 创建基于分支的 CI 工作流

使用分支的最佳实践之一是创建基于分支的 CI 工作流。通过该工作流，你可以在 pull request 合并前，使用集群的分支而不是生产集群来测试你的代码。你可以在 [这里](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example) 查看在线演示。

创建该工作流的主要步骤如下：

1. [将 TiDB Cloud Branching 集成到你的 GitHub 仓库](#integrate-branching-with-your-github-repository)。

2. 获取分支连接信息。

    你可以使用 [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch) action 等待分支就绪，并获取分支的连接信息。

    以 TiDB Cloud Starter 集群的分支为例：

   ```yaml
   steps:
     - name: Wait for TiDB Cloud Starter branch to be ready
       uses: tidbcloud/wait-for-tidbcloud-branch@v0
       id: wait-for-branch
       with:
         token: ${{ secrets.GITHUB_TOKEN }}
         public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
         private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

     - name: Test with TiDB Cloud Starter branch
        run: |
           echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
           echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
           echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
   ```
   
   - `token`：GitHub 会自动创建一个 [GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) secret，可以直接使用。
   - `public-key` 和 `private-key`：TiDB Cloud [API key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

3. 修改你的测试代码。

   修改你的测试代码以从 GitHub Actions 接收连接信息。例如，你可以通过环境变量接收连接信息，具体可参考 [在线演示](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)。

## 后续操作

你可以通过以下示例，学习如何使用分支 GitHub 集成：

- [branching-gorm-example](https://github.com/tidbcloud/branching-gorm-example)
- [branching-django-example](https://github.com/tidbcloud/branching-django-example)
- [branching-rails-example](https://github.com/tidbcloud/branching-rails-example)

你也可以在不使用分支 GitHub 集成的情况下，构建自己的分支 CI/CD 工作流。例如，你可以使用 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli) 和 GitHub Actions 自定义你的 CI/CD 工作流。