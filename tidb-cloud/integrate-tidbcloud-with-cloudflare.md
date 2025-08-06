---
title: 集成 TiDB Cloud 与 Cloudflare
summary: 了解如何将 Cloudflare Workers 与 TiDB Cloud 部署集成。
---

# 集成 TiDB Cloud 与 Cloudflare Workers

[Cloudflare Workers](https://workers.cloudflare.com/) 是一个平台，允许你在特定事件发生时运行代码，例如 HTTP 请求或数据库变更。Cloudflare Workers 易于使用，可用于构建各种应用，包括自定义 API、无服务器函数和微服务。它对于需要低延迟性能或需要快速扩展的应用尤其有用。

你可能会发现从 Cloudflare Workers 连接到 TiDB Cloud 有一定难度，因为 Cloudflare Workers 运行在 V8 引擎上，无法直接建立 TCP 连接。你可以使用 [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md) 通过 HTTP 连接帮助你连接到 Cloudflare Workers。

本文档将逐步演示如何使用 TiDB Cloud serverless driver 连接到 Cloudflare Workers。

> **注意：**
>
> TiDB Cloud serverless driver 只能用于 TiDB Cloud Serverless。

## 开始之前

在尝试本文步骤之前，你需要准备以下内容：

- 一个 TiDB Cloud 账号，以及在 TiDB Cloud 上创建的 TiDB Cloud Serverless 集群。详情请参见 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)。
- 一个 [Cloudflare Workers 账号](https://dash.cloudflare.com/login)。
- 已安装 [npm](https://docs.npmjs.com/about-npm)。

## 步骤 1：设置 Wrangler

[Wrangler](https://developers.cloudflare.com/workers/wrangler/) 是官方的 Cloudflare Worker CLI。你可以用它来生成、构建、预览和发布你的 Workers。

1. 安装 Wrangler：

   ```
   npm install wrangler
   ```

2. 认证 Wrangler，运行 wrangler login：

    ```
    wrangler login
    ```

3. 使用 Wrangler 创建一个 worker 项目：

    ```
    wrangler init tidb-cloud-cloudflare
    ```

4. 在终端中，你会被询问一系列与项目相关的问题。所有问题均选择默认值即可。

## 步骤 2：安装 serverless driver

1. 进入你的项目目录：

    ```
    cd tidb-cloud-cloudflare
    ```

2. 使用 npm 安装 serverless driver：

    ```
    npm install @tidbcloud/serverless
    ```

   这会在 `package.json` 中添加 serverless driver 依赖。

## 步骤 3：开发 Cloudflare Worker 函数

你需要根据需求修改 `src/index.ts`。

例如，如果你想展示所有数据库，可以使用如下代码：

```ts
import { connect } from '@tidbcloud/serverless'


export interface Env {
   DATABASE_URL: string;
}

export default {
   async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
      const conn = connect({url:env.DATABASE_URL})
      const resp = await conn.execute("show databases")
      return new Response(JSON.stringify(resp));
   },
};
```

## 步骤 4：在环境中设置 DATABASE_URL

`DATABASE_URL` 遵循 `mysql://username:password@host/database` 格式。你可以使用 wrangler cli 设置环境变量：

```
wrangler secret put <DATABASE_URL>
```

你也可以通过 Cloudflare Workers 控制台编辑 `DATABASE_URL` secret。

## 步骤 5：发布到 Cloudflare Workers

现在你已经可以部署到 Cloudflare Workers 了。

在你的项目目录下，运行以下命令：

```
npx wrangler publish
```

## 步骤 6：测试你的 Cloudflare Workers

1. 前往 [Cloudflare 控制台](https://dash.cloudflare.com) 查找你的 worker。你可以在概览页面找到 worker 的 URL。

2. 访问该 URL，你将获得结果。

## 示例

参见 [Cloudflare Workers 示例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)。