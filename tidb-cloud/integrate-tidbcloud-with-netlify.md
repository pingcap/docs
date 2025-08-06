---
title: 集成 TiDB Cloud 与 Netlify
summary: 了解如何将你的 TiDB Cloud 集群连接到 Netlify 项目。
---

# 集成 TiDB Cloud 与 Netlify

[Netlify](https://netlify.com/) 是一个一体化平台，用于自动化现代 Web 项目。它用单一的工作流替代了你的托管基础设施、持续集成和部署流水线，并在项目发展过程中集成了如无服务器函数、用户认证和表单处理等动态功能。

本文档介绍了如何在 Netlify 上部署一个以 TiDB Cloud 作为数据库后端的全栈应用。你还可以学习如何将 Netlify edge function 与我们的 TiDB Cloud serverless driver 一起使用。

## 前置条件

在部署之前，请确保满足以下前置条件。

### 一个 Netlify 账号和 CLI

你需要拥有一个 Netlify 账号和 CLI。如果还没有，请参考以下链接创建：

* [注册 Netlify 账号](https://app.netlify.com/signup)
* [获取 Netlify CLI](https://docs.netlify.com/cli/get-started/)

### 一个 TiDB Cloud 账号和 TiDB 集群

你需要在 TiDB Cloud 中拥有一个账号和一个集群。如果还没有，请参考以下内容创建：

- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)
- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)

一个 TiDB Cloud 集群可以连接到多个 Netlify 站点。

### TiDB Cloud 中流量过滤器允许所有 IP 地址

对于 TiDB Cloud Dedicated 集群，请确保集群的流量过滤器允许所有 IP 地址（设置为 `0.0.0.0/0`）进行连接。这是因为 Netlify 部署使用动态 IP 地址。

TiDB Cloud Serverless 集群默认允许所有 IP 地址连接，因此无需配置任何流量过滤器。

## 步骤 1. 获取示例项目和连接字符串

为了帮助你快速上手，TiDB Cloud 提供了一个基于 TypeScript、Next.js、React 和 Prisma Client 的全栈示例应用。它是一个简单的博客站点，你可以在其中发布和删除自己的博客。所有内容都通过 Prisma 存储在 TiDB Cloud 中。

### Fork 示例项目并克隆到你的空间

1. 将 [Fullstack Example with Next.js and Prisma](https://github.com/tidbcloud/nextjs-prisma-example) 仓库 fork 到你自己的 GitHub 仓库。

2. 将 fork 后的仓库克隆到你的本地空间：

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### 获取 TiDB Cloud 连接字符串

对于 TiDB Cloud Serverless 集群，你可以通过 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 或 [TiDB Cloud 控制台](https://tidbcloud.com/) 获取连接字符串。

对于 TiDB Cloud Dedicated 集群，你只能通过 TiDB Cloud 控制台获取连接字符串。

<SimpleTab>
<div label="TiDB Cloud CLI">

> **提示：**
>
> 如果你还没有安装 Cloud CLI，请参考 [TiDB Cloud CLI 快速入门](/tidb-cloud/get-started-with-cli.md) 进行快速安装，然后再执行以下步骤。

1. 以交互模式获取集群的连接字符串：

    ```shell
    ticloud cluster connect-info
    ```

2. 按提示选择你的集群、客户端和操作系统。注意，本教程使用的客户端为 `Prisma`。

    ```
    Choose the cluster
    > [x] Cluster0(13796194496)
    Choose the client
    > [x] Prisma
    Choose the operating system
    > [x] macOS/Alpine (Detected)
    ```

    输出如下，你可以在 `url` 字段中找到 Prisma 的连接字符串。

    ```shell
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **注意：**
    >
    > 在后续使用连接字符串时，请注意以下事项：
    >
    > - 将连接字符串中的参数替换为实际值。
    > - 本文档中的示例应用需要一个新数据库，因此你需要将 `<Database>` 替换为一个唯一的新名称。

</div>
<div label="TiDB Cloud console">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页，然后点击右上角的 **Connect**。在弹出的对话框中，你可以从连接字符串中获取以下连接参数：

    - `${host}`
    - `${port}`
    - `${user}`
    - `${password}`

2. 将连接参数填入以下连接字符串：

    ```shell
    mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
    ```

    > **注意：**
    >
    > 在后续使用连接字符串时，请注意以下事项：
    >
    > - 将连接字符串中的参数替换为实际值。
    > - 本文档中的示例应用需要一个新数据库，因此你需要将 `<Database>` 替换为一个唯一的新名称。

</div>
</SimpleTab>

## 步骤 2. 将示例应用部署到 Netlify

1. 在 Netlify CLI 中，认证你的 Netlify 账号并获取访问令牌。

    ```shell
    netlify login
    ```

2. 启动自动化设置。此步骤会连接你的仓库以实现持续部署，因此 Netlify CLI 需要访问权限以在仓库中创建 deploy key 和 webhook。

    ```shell
    netlify init
    ```

    当出现提示时，选择 **Create & configure a new site**，并授权 GitHub 访问。其他选项均使用默认值。

    ```shell
    Adding local .netlify folder to .gitignore file...
    ? What would you like to do? +  Create & configure a new site
    ? Team: your_username’s team
    ? Site name (leave blank for a random name; you can change it later):

    Site Created

    Admin URL: https://app.netlify.com/sites/mellow-crepe-e2ca2b
    URL:       https://mellow-crepe-e2ca2b.netlify.app
    Site ID:   b23d1359-1059-49ed-9d08-ed5dba8e83a2

    Linked to mellow-crepe-e2ca2b


    ? Netlify CLI needs access to your GitHub account to configure Webhooks and Deploy Keys. What would you like to do? Authorize with GitHub through app.netlify.com
    Configuring Next.js runtime...

    ? Your build command (hugo build/yarn run build/etc): npm run netlify-build
    ? Directory to deploy (blank for current dir): .next

    Adding deploy key to repository...
    (node:36812) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
    (Use `node --trace-warnings ...` to show where the warning was created)
    Deploy key added!

    Creating Netlify GitHub Notification Hooks...
    Netlify Notification Hooks configured!

    Success! Netlify CI/CD Configured!

    This site is now configured to automatically deploy from github branches & pull requests

    Next steps:

    git push       Push to your git repository to trigger new site builds
    netlify open   Open the Netlify admin URL of your site
    ```

3. 设置环境变量。为了让你的本地空间和 Netlify 空间都能连接到 TiDB Cloud 集群，你需要将 `DATABASE_URL` 设置为在 [步骤 1](#step-1-get-the-example-project-and-the-connection-string) 获取到的连接字符串。

    ```shell
    # 为你的本地空间设置环境变量
    export DATABASE_URL='mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'

    # 为 Netlify 空间设置环境变量
    netlify env:set DATABASE_URL 'mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    ```

    检查你的环境变量。

    ```shell
    # 检查本地空间的环境变量
    env | grep DATABASE_URL

    # 检查 Netlify 空间的环境变量
    netlify env:list
    ```

4. 在本地构建应用并将 schema 迁移到你的 TiDB Cloud 集群。

    > **提示：**
    >
    > 如果你想跳过本地部署，直接将应用部署到 Netlify，请直接跳到第 6 步。

    ```shell
    npm install .
    npm run netlify-build
    ```

5. 在本地运行应用。你可以启动本地开发服务器预览你的站点。

    ```shell
    netlify dev
    ```

    然后在浏览器中访问 `http://localhost:3000/`，体验其界面。

6. 将应用部署到 Netlify。当你对本地预览满意后，可以使用以下命令将站点部署到 Netlify。`--trigger` 表示不上传本地文件进行部署。如果你有本地更改，请确保已提交到你的 GitHub 仓库。

    ```shell
    netlify deploy --prod --trigger
    ```

    前往你的 Netlify 控制台查看部署状态。部署完成后，应用的站点将拥有 Netlify 提供的公网 IP 地址，所有人都可以访问。

## 使用 edge function

上文提到的示例应用运行在 Netlify 的无服务器函数上。本节将介绍如何将 [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md) 与 edge function 一起使用。edge function 是 Netlify 提供的一项功能，允许你在 Netlify CDN 的边缘运行无服务器函数。

要使用 edge function，请按以下步骤操作：

1. 在项目根目录下创建名为 `netlify/edge-functions` 的目录。

2. 在该目录下创建名为 `hello.ts` 的文件，并添加以下代码：

    ```typescript
    import { connect } from 'https://esm.sh/@tidbcloud/serverless'
    
    export default async () => {
      const conn = connect({url: Netlify.env.get('DATABASE_URL')})
      const result = await conn.execute('show databases')
      return new Response(JSON.stringify(result));
    }
   
    export const config = { path: "/api/hello" };
    ```

3. 设置 `DATABASE_URL` 环境变量。你可以从 [TiDB Cloud 控制台](https://tidbcloud.com/) 获取连接信息。

    ```shell
    netlify env:set DATABASE_URL 'mysql://<username>:<password>@<host>/<database>'
    ```

4. 将 edge function 部署到 Netlify。

    ```shell
    netlify deploy --prod --trigger
    ```

然后你可以前往 Netlify 控制台查看部署状态。部署完成后，你可以通过 `https://<netlify-host>/api/hello` URL 访问 edge function。