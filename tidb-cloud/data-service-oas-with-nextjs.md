---
title: 在 Next.js 中使用 Data App 的 OpenAPI 规范
summary: 学习如何使用 Data App 的 OpenAPI 规范生成客户端代码并开发 Next.js 应用。
---

# 在 Next.js 中使用 Data App 的 OpenAPI 规范

本文介绍如何使用 [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) 的 OpenAPI 规范生成客户端代码，并开发 Next.js 应用。

## 开始之前

在将 OpenAPI 规范与 Next.js 配合使用之前，请确保你已具备以下条件：

- 一个 TiDB 集群。更多信息，参见 [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md) 或 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。
- [Node.js](https://nodejs.org/en/download)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [yarn](https://yarnpkg.com/getting-started/install)

本文以 TiDB Cloud Serverless 集群为例。

## 步骤 1. 准备数据

首先，在你的 TiDB 集群中创建表 `test.repository`，并插入一些示例数据。以下示例插入了由 PingCAP 开发的一些开源项目，作为演示数据。

你可以在 [TiDB Cloud 控制台](https://tidbcloud.com)的 [SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)中执行这些 SQL 语句。

```sql
-- 选择数据库
USE test;

-- 创建表
CREATE TABLE repository (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(64) NOT NULL,
        url varchar(256) NOT NULL
);

-- 向表中插入一些示例数据
INSERT INTO repository (name, url)
VALUES ('tidb', 'https://github.com/pingcap/tidb'),
        ('tikv', 'https://github.com/tikv/tikv'),
        ('pd', 'https://github.com/tikv/pd'),
        ('tiflash', 'https://github.com/pingcap/tiflash');
```

## 步骤 2. 创建 Data App

数据插入完成后，前往 [TiDB Cloud 控制台](https://tidbcloud.com)的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。创建一个关联到你的 TiDB 集群的 Data App，为该 Data App 创建一个 API key，然后在 Data App 中创建一个 `GET /repositories` 的 endpoint。该 endpoint 对应的 SQL 语句如下，用于查询 `test.repository` 表中的所有行：

```sql
SELECT * FROM test.repository;
```

更多信息，参见 [快速开始使用 Data Service](/tidb-cloud/data-service-get-started.md)。

## 步骤 3. 生成客户端代码

以下以 Next.js 为例，演示如何使用 Data App 的 OpenAPI 规范生成客户端代码。

1. 创建名为 `hello-repos` 的 Next.js 项目。

    要使用官方模板创建 Next.js 项目，请执行以下命令，并在提示时保持所有默认选项：

    ```shell
    yarn create next-app hello-repos
    ```

    使用以下命令切换到新创建的项目目录：

    ```shell
    cd hello-repos
    ```

2. 安装依赖。

    本文使用 [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) 根据 OpenAPI 规范自动生成 API 客户端库。

    通过以下命令将 OpenAPI Generator 作为开发依赖安装：

    ```shell
    yarn add @openapitools/openapi-generator-cli --dev
    ```

3. 下载 OpenAPI 规范并保存为 `oas/doc.json`。

    1. 在 TiDB Cloud [**Data Service**](https://tidbcloud.com/project/data-service) 页面，点击左侧面板中的 Data App 名称，进入 App 设置页面。
    2. 在 **API Specification** 区域，点击 **Download**，选择 JSON 格式，如有提示点击 **Authorize**。
    3. 将下载的文件保存为 `hello-repos` 项目目录下的 `oas/doc.json`。

    更多信息，参见 [下载 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#download-the-openapi-specification)。

    `oas/doc.json` 文件的结构如下：

    ```json
    {
      "openapi": "3.0.3",
      "components": {
        "schemas": {
          "getRepositoriesResponse": {
            "properties": {
              "data": {
                "properties": {
                  "columns": { ... },
                  "result": { ... },
                  "rows": {
                    "items": {
                      "properties": {
                        "id": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "url": {
                          "type": "string"
                        }
    ...
      "paths": {
        "/repositories": {
          "get": {
            "operationId": "getRepositories",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/getRepositoriesResponse"
                    }
                  }
                },
                "description": "OK"
              },
    ...
    ```

4. 生成客户端代码：

    ```shell
    yarn run openapi-generator-cli generate -i oas/doc.json --generator-name typescript-fetch -o gen/api
    ```

    该命令以 `oas/doc.json` 规范为输入，生成客户端代码并输出到 `gen/api` 目录。

## 步骤 4. 开发你的 Next.js 应用

你可以使用生成的客户端代码开发 Next.js 应用。

1. 在 `hello-repos` 项目目录下，创建 `.env.local` 文件，并添加以下变量，然后将变量值设置为你的 Data App 的 public key 和 private key。

    ```
    TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY=YOUR_PUBLIC_KEY
    TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY=YOUR_PRIVATE_KEY
    ```

    有关如何为 Data App 创建 API key，参见 [创建 API key](/tidb-cloud/data-service-api-key.md#create-an-api-key)。

2. 在 `hello-repos` 项目目录下，将 `app/page.tsx` 的内容替换为以下代码，该代码会从 `GET /repositories` endpoint 获取数据并进行渲染：

    ```js
    import {DefaultApi, Configuration} from "../gen/api"

    export default async function Home() {
      const config = new Configuration({
        username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
        password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
      });
      const apiClient = new DefaultApi(config);
      const resp = await apiClient.getRepositories();
      return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <ul className="font-mono text-2xl">
            {resp.data.rows.map((repo) => (
              <a href={repo.url}>
                <li key={repo.id}>{repo.name}</li>
              </a>
            ))}
          </ul>
        </main>
      )
    }
    ```

    > **注意：**
    >
    > 如果你的 Data App 关联的集群分布在不同区域，你会在下载的 OpenAPI 规范文件的 `servers` 部分看到多个项。此时，你还需要在 `config` 对象中配置 endpoint 路径，如下所示：
    >
    >  ```js
    >  const config = new Configuration({
    >      username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
    >      password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
    >      basePath: "https://${YOUR_REGION}.data.dev.tidbcloud.com/api/v1beta/app/${YOUR_DATA_APP_ID}/endpoint"
    >    });
    >  ```
    >
    > 请确保将 `basePath` 替换为你的 Data App 实际的 endpoint 路径。要获取 `${YOUR_REGION}` 和 `{YOUR_DATA_APP_ID}`，请在 endpoint 的 **Properties** 面板中查看 **Endpoint URL**。

## 步骤 5. 预览你的 Next.js 应用

> **注意：**
>
> 在预览前，请确保所有必需的依赖已安装并正确配置。

要在本地开发服务器中预览你的应用，请运行以下命令：

```shell
yarn dev
```

然后你可以在浏览器中打开 [http://localhost:3000](http://localhost:3000)，即可在页面上看到 `test.repository` 数据库中的数据。