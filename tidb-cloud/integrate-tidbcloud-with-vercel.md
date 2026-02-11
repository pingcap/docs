---
title: 集成 TiDB Cloud 与 Vercel
summary: 了解如何将 TiDB Cloud 集群连接到 Vercel 项目。
---

<!-- markdownlint-disable MD029 -->

# 集成 TiDB Cloud 与 Vercel

[Vercel](https://vercel.com/) 是一个面向前端开发者的平台，提供创新者在灵感迸发时所需的速度与可靠性。

将 TiDB Cloud 与 Vercel 结合使用，可以让你基于 MySQL 兼容的关系型模型更快地构建新的前端应用，并借助具备高可用性、可扩展性以及最高级别数据隐私和安全的平台，放心地扩展你的应用。

本指南介绍了如何通过以下方法之一，将你的 TiDB Cloud 集群连接到 Vercel 项目：

* [通过 TiDB Cloud Vercel 集成进行连接](#connect-via-the-tidb-cloud-vercel-integration)
* [通过手动配置环境变量进行连接](#connect-via-manually-setting-environment-variables)

对于上述两种方法，TiDB Cloud 提供了以下可编程连接数据库的选项：

- 集群：通过直连或 [serverless driver](/develop/serverless-driver.md) 将 TiDB Cloud 集群连接到 Vercel 项目。
- [Data App](/tidb-cloud/data-service-manage-data-app.md)：通过一组 HTTP 端点访问 TiDB Cloud 集群的数据。

## 前置条件

在连接前，请确保满足以下前置条件。

### 一个 Vercel 账户和一个 Vercel 项目

你需要在 Vercel 中拥有一个账户和一个项目。如果还没有，请参考以下 Vercel 文档进行创建：

* [创建个人账户](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account) 或 [创建团队](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team)。
* 在 Vercel 中[创建项目](https://vercel.com/docs/concepts/projects/overview#creating-a-project)，如果你还没有可部署的应用，可以试用 [TiDB Cloud Starter 模板](https://vercel.com/templates/next.js/tidb-cloud-starter)。

一个 Vercel 项目只能连接一个 TiDB Cloud 集群。如需更换集成，需先断开当前集群，再连接新集群。

### 一个 TiDB Cloud 账户和一个 TiDB 集群

你需要在 TiDB Cloud 中拥有一个账户和一个集群。如果还没有，请参考以下内容进行创建：

- [创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注意：**
    >
    > TiDB Cloud Vercel 集成支持创建 TiDB Cloud Starter 和 TiDB Cloud Essential 集群。你也可以在集成过程中创建。

- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)

    > **注意：**
    >
    > 对于 TiDB Cloud Dedicated 集群，请确保集群的流量过滤器允许所有 IP 地址（设置为 `0.0.0.0/0`）进行连接，因为 Vercel 部署使用[动态 IP 地址](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)。

要[通过 TiDB Cloud Vercel 集成与 Vercel 集成](#connect-via-the-tidb-cloud-vercel-integration)，你需要是 TiDB Cloud 组织的 `Organization Owner` 角色，或目标项目的 `Project Owner` 角色。更多信息参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

一个 TiDB Cloud 集群可以连接多个 Vercel 项目。

### 一个 Data App 及其端点

如果你希望通过 [Data App](/tidb-cloud/data-service-manage-data-app.md) 连接 TiDB Cloud 集群，需要提前在 TiDB Cloud 中拥有目标 Data App 及其端点。如果还没有，请参考以下步骤进行创建：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. [为项目创建 Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app)。
3. [将 Data App 关联](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) 到目标 TiDB Cloud 集群。
4. [管理端点](/tidb-cloud/data-service-manage-endpoint.md)，以便自定义端点执行 SQL 语句。

一个 Vercel 项目只能连接一个 TiDB Cloud Data App。如需更换 Vercel 项目的 Data App，需先断开当前 App，再连接新 App。

## 通过 TiDB Cloud Vercel 集成进行连接

要通过 TiDB Cloud Vercel 集成进行连接，请前往 [TiDB Cloud 集成](https://vercel.com/integrations/tidb-cloud)页面（来自 [Vercel 的 Integrations Marketplace](https://vercel.com/integrations)）。使用此方法，你可以选择要连接的集群，TiDB Cloud 会自动为你的 Vercel 项目生成所有必要的环境变量。

> **注意：**
>
> 此方法仅适用于 TiDB Cloud Starter 和 TiDB Cloud Essential 集群。如果你想连接 TiDB Cloud Dedicated 集群，请使用[手动方法](#connect-via-manually-setting-environment-variables)。

### 集成流程

详细步骤如下：

<SimpleTab>
<div label="Cluster">

1. 在 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)页面右上角点击 **Add Integration**。会弹出 **Add TiDB Cloud** 对话框。
2. 在下拉列表中选择集成的作用域，然后点击 **Continue**。
3. 选择要添加集成的 Vercel 项目，点击 **Continue**。
4. 确认集成所需权限，点击 **Add Integration**。随后会跳转到 TiDB Cloud 控制台的集成页面。
5. 在集成页面，按如下操作：

    1. 选择目标 Vercel 项目，点击 **Next**。
    2. 选择目标 TiDB Cloud 组织和项目。
    3. 选择 **Cluster** 作为连接类型。
    4. 选择目标 TiDB Cloud 集群。如果 **Cluster** 下拉列表为空，或你想选择新的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，可点击列表中的 **+ Create Cluster** 创建。
    5. 选择要连接的数据库。如果 **Database** 下拉列表为空，或你想选择新的数据库，可点击列表中的 **+ Create Database** 创建。
    6. 选择 Vercel 项目所用的框架。如果目标框架未列出，选择 **General**。不同框架会决定不同的环境变量。
    7. 选择是否启用 **Branching**，以为预览环境创建新分支。
    8. 点击 **Add Integration and Return to Vercel**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6. 返回 Vercel 控制台，进入你的 Vercel 项目，点击 **Settings** > **Environment Variables**，检查目标 TiDB 集群的环境变量是否已自动添加。

    如果已添加以下变量，则集成完成。

    **General**

    ```shell
    TIDB_HOST
    TIDB_PORT
    TIDB_USER
    TIDB_PASSWORD
    TIDB_DATABASE
    ```

    **Prisma**

    ```
    DATABASE_URL
    ```

    **TiDB Cloud Serverless Driver**

    ```
    DATABASE_URL
    ```

</div>

<div label="Data App">

1. 在 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)页面右上角点击 **Add Integration**。会弹出 **Add TiDB Cloud** 对话框。
2. 在下拉列表中选择集成的作用域，然后点击 **Continue**。
3. 选择要添加集成的 Vercel 项目，点击 **Continue**。
4. 确认集成所需权限，点击 **Add Integration**。随后会跳转到 TiDB Cloud 控制台的集成页面。
5. 在集成页面，按如下操作：

    1. 选择目标 Vercel 项目，点击 **Next**。
    2. 选择目标 TiDB Cloud 组织和项目。
    3. 选择 **Data App** 作为连接类型。
    4. 选择目标 TiDB Data App。
    6. 点击 **Add Integration and Return to Vercel**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6. 返回 Vercel 控制台，进入你的 Vercel 项目，点击 **Settings** > **Environment Variables**，检查目标 Data App 的环境变量是否已自动添加。

    如果已添加以下变量，则集成完成。

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

### 配置连接

如果你已安装 [TiDB Cloud Vercel 集成](https://vercel.com/integrations/tidb-cloud)，可以在集成内添加或移除连接。

1. 在 Vercel 控制台点击 **Integrations**。
2. 在 TiDB Cloud 条目中点击 **Manage**。
3. 点击 **Configure**。
4. 点击 **Add Link** 或 **Remove** 以添加或移除连接。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    当你移除连接时，通过集成流程设置的环境变量也会从 Vercel 项目中移除。但此操作不会影响 TiDB Cloud 集群中的数据。

### 使用 TiDB Cloud 分支功能连接 {#connect-with-branching}

Vercel 的 [Preview Deployments](https://vercel.com/docs/deployments/preview-deployments) 功能允许你在不将更改合并到 Git 项目的生产分支的情况下，预览应用在真实部署中的更改。结合 [TiDB Cloud Branching](/tidb-cloud/branch-overview.md)，你可以为 Vercel 项目的每个分支创建一个新的实例，从而在不影响生产数据的情况下预览应用更改。

> **注意：**
>
> 目前，TiDB Cloud Branching 仅支持[关联 GitHub 仓库的 Vercel 项目](https://vercel.com/docs/deployments/git/vercel-for-github)。

要启用 TiDB Cloud Branching，需要在 [TiDB Cloud Vercel 集成流程](#integration-workflow)中确保：

1. 选择 **Cluster** 作为连接类型。
2. 启用 **Branching**，为预览环境创建新分支。

在你将更改 push 到 Git 仓库后，Vercel 会触发预览部署。TiDB Cloud 集成会自动为该 Git 分支创建 TiDB Cloud 集群分支并设置环境变量。详细步骤如下：

1. 在 Git 仓库中创建新分支。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2. 添加一些更改并 push 到远程仓库。
3. Vercel 会为新分支触发预览部署。

    ![Vercel Preview_Deployment](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1. 部署过程中，TiDB Cloud 集成会自动为你的集群创建与 Git 分支同名的分支。如果分支已存在，则跳过此步骤。

        ![TiDB_Cloud_Branch_Check](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2. 分支就绪后，TiDB Cloud 集成会在 Vercel 项目的预览部署中设置环境变量。

        ![Preview_Envs](/media/tidb-cloud/vercel/preview-envs.png)

    3. TiDB Cloud 集成还会注册一个阻塞检查，等待分支就绪。你可以手动重新运行检查。
4. 检查通过后，你可以访问预览部署查看更改。

> **注意：**
>
> 由于 Vercel 部署流程的限制，无法保证环境变量一定会在部署中设置。如遇此情况，请重新部署。

> **注意：**
>
> 在 TiDB Cloud 的每个组织中，默认最多可为 TiDB Cloud Starter 集群创建 5 个分支。为避免超出限制，你可以删除不再需要的集群分支。更多信息参见 [管理 TiDB Cloud 分支](/tidb-cloud/branch-manage.md)。

## 通过手动设置环境变量进行连接

<SimpleTab>
<div label="Cluster">

1. 获取 TiDB 集群的连接信息。

    你可以在集群的连接对话框中获取连接信息。打开方式：进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入概览页，然后点击右上角的 **Connect**。

2. 进入 Vercel 控制台 > Vercel 项目 > **Settings** > **Environment Variables**，根据 TiDB 集群的连接信息[声明每个环境变量的值](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

这里以 Prisma 应用和 TiDB Cloud Starter 集群为例，以下是 TiDB Cloud Starter 集群在 Prisma schema 文件中的 datasource 设置：

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

在 Vercel 中，你可以这样声明环境变量：

- **Key** = `DATABASE_URL`
- **Value** = `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

你可以在 TiDB Cloud 控制台获取 `<User>`、`<Password>`、`<Endpoint>`、`<Port>` 和 `<Database>` 的信息。

</div>
<div label="Data App">

1. 按照 [管理 Data APP](/tidb-cloud/data-service-manage-data-app.md) 和 [管理 Endpoint](/tidb-cloud/data-service-manage-endpoint.md) 的步骤创建 Data App 及其端点（如尚未创建）。

2. 进入 Vercel 控制台 > Vercel 项目 > **Settings** > **Environment Variables**，根据 Data App 的连接信息[声明每个环境变量的值](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    在 Vercel 中，你可以这样声明环境变量：

    - **Key** = `DATA_APP_BASE_URL`
    - **Value** = `<DATA_APP_BASE_URL>`
    - **Key** = `DATA_APP_PUBLIC_KEY`
    - **Value** = `<DATA_APP_PUBLIC_KEY>`
    - **Key** = `DATA_APP_PRIVATE_KEY`
    - **Value** = `<DATA_APP_PRIVATE_KEY>`

    你可以在 TiDB Cloud 控制台的 [Data Service](https://tidbcloud.com/project/data-service) 页面获取 `<DATA_APP_BASE_URL>`、`<DATA_APP_PUBLIC_KEY>`、`<DATA_APP_PRIVATE_KEY>` 的信息。

</div>
</SimpleTab>