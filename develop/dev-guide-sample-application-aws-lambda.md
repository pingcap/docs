---
title: 使用 mysql2 在 AWS Lambda 函数中连接 TiDB
summary: 本文介绍如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 构建一个 CRUD 应用，并提供一个简单的示例代码片段。
---

# 使用 mysql2 在 AWS Lambda 函数中连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[AWS Lambda 函数](https://aws.amazon.com/lambda/) 是一项计算服务，[mysql2](https://github.com/sidorares/node-mysql2) 是一个流行的开源 Node.js 驱动程序。

在本教程中，你可以学习如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 来完成以下任务：

- 设置你的环境。
- 使用 mysql2 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你可以查阅 [示例代码片段](#sample-code-snippets) 来了解基本的 CRUD 操作。
- 部署你的 AWS Lambda 函数。

> **Note**
>
> 本教程适用于 {{{ .starter }}} 和 TiDB 自托管版本。

## 前提条件

完成本教程，你需要：

- [Node.js **18**](https://nodejs.org/en/download/) 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。
- 一个具有管理员权限的 [AWS 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)。
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

如果你没有 AWS 账号或用户，可以按照 [Getting Started with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) 指南中的步骤创建。

## 运行示例应用以连接到 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

> **Note**
>
> 有关完整的代码片段和运行说明，请参考 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub 仓库。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### 第 2 步：安装依赖

运行以下命令以安装示例应用所需的包（包括 `mysql2`）：

```bash
npm install
```

### 第 3 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>

<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境匹配。

    > **Note**
    >
    > 在 Node.js 应用中，你无需提供 SSL CA 证书，因为 Node.js 在建立 TLS（SSL）连接时默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 点击 **Generate Password** 以生成随机密码。

    > **Tip**
    >
    > 如果之前已生成过密码，可以使用原密码，或点击 **Reset Password** 生成新密码。

5. 复制并粘贴相应的连接字符串到 `env.json` 中。示例如下：

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
        "TIDB_PORT": "4000",
        "TIDB_USER": "{prefix}.root",
        "TIDB_PASSWORD": "{password}"
      }
    }
    ```

    将 `{}` 中的占位符替换为连接对话框中获得的值。

</div>

<div label="TiDB Self-Managed">

复制并粘贴相应的连接字符串到 `env.json` 中。示例如下：

```json
{
  "Parameters": {
    "TIDB_HOST": "{tidb_server_host}",
    "TIDB_PORT": "4000",
    "TIDB_USER": "root",
    "TIDB_PASSWORD": "{password}"
  }
}
```

将 `{}` 中的占位符替换为在 **Connect** 窗口中获得的值。

</div>

</SimpleTab>

### 第 4 步：运行代码并检查结果

1. （前提）安装 [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建包：

    ```bash
    npm run build
    ```

3. 调用示例 Lambda 函数：

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4. 在终端中查看输出。如果输出类似如下内容，说明连接成功：

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

确认连接成功后，你可以按照 [下一节](#deploy-the-aws-lambda-function) 进行 AWS Lambda 函数的部署。

## 部署 AWS Lambda 函数

你可以使用 [SAM CLI](#sam-cli-deployment-recommended) 或 [AWS Lambda 控制台](#web-console-deployment) 来部署 AWS Lambda 函数。

### SAM CLI 部署（推荐）

1. （前提）安装 [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建包：

    ```bash
    npm run build
    ```

3. 更新 [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml) 中的环境变量：

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4. 设置 AWS 环境变量（参考 [Short-term credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)）：

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5. 部署 AWS Lambda 函数：

    ```bash
    sam deploy --guided

    # 示例：

    # 配置 SAM 部署
    # ======================

    #        正在查找配置文件 [samconfig.toml] ：未找到

    #        设置 'sam deploy' 的默认参数
    #        =========================================
    #        Stack Name [sam-app]: tidb-aws-lambda-quickstart
    #        AWS Region [us-east-1]:
    #        # 显示即将部署的资源变更，需要输入 'Y' 来确认
    #        Confirm changes before deploy [y/N]:
    #        # SAM 需要权限创建角色以连接模板中的资源
    #        Allow SAM CLI IAM role creation [Y/n]:
    #        # 在操作失败时保留之前配置的资源状态
    #        Disable rollback [y/N]:
    #        tidbHelloWorldFunction 可能没有定义授权，是否继续？ [y/N]: y
    #        (后续提示同样输入 y)
    ```

### Web 控制台部署

1. 构建包：

    ```bash
    npm run build

    # 打包为 AWS Lambda
    # =====================
    # dist/index.zip
    ```

2. 访问 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home#/functions)。

3. 按照 [创建 Lambda 函数](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html) 的步骤，创建一个 Node.js Lambda 函数。

4. 按照 [Lambda 部署包](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip) 的步骤，上传 `dist/index.zip` 文件。

5. [复制并配置相应的连接字符串](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) 到 Lambda 函数中。

    1. 在 Lambda 控制台的 [Functions](https://console.aws.amazon.com/lambda/home#/functions) 页面，选择 **Configuration** 标签，然后选择 **Environment variables**。
    2. 选择 **Edit**。
    3. 添加数据库访问凭据，操作如下：
        - 选择 **Add environment variable**，在 **Key** 中输入 `TIDB_HOST`，在 **Value** 中输入主机名。
        - 选择 **Add environment variable**，在 **Key** 中输入 `TIDB_PORT`，在 **Value** 中输入端口（默认 4000）。
        - 选择 **Add environment variable**，在 **Key** 中输入 `TIDB_USER`，在 **Value** 中输入用户名。
        - 选择 **Add environment variable**，在 **Key** 中输入 `TIDB_PASSWORD`，在 **Value** 中输入你创建数据库时设置的密码。
        - 点击 **Save**。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

有关完整示例代码及运行方式，请查阅 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) 仓库。

### 连接到 TiDB

以下代码使用环境变量中定义的参数建立与 TiDB 的连接：

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host，例如：{gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB 端口，默认：4000
    user: process.env.TIDB_USER, // TiDB 用户，例如：{prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB 密码
    database: process.env.TIDB_DATABASE || 'test', // TiDB 数据库名，默认：test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // 在无服务器函数环境中，将 connectionLimit 设置为 1，有助于优化资源使用、降低成本、确保连接稳定性，并实现无缝扩展。
    maxIdle: 1, // 最大空闲连接数，默认值与 `connectionLimit` 相同
    enableKeepAlive: true,
  });
}

export function getPool(): mysql.Pool {
  if (!pool) {
    pool = connect();
  }
  return pool;
}
```

### 插入数据

以下查询创建一个 `Player` 记录，并返回一个 `ResultSetHeader` 对象：

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询根据 ID `1` 返回一个 `Player` 记录：

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 添加 `50` 个金币和 `50` 件商品：

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 有用的注意事项

- 使用 [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) 管理数据库连接，可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入，建议使用 [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在涉及不多复杂 SQL 语句的场景中，使用 ORM 框架如 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/)、或 [Prisma](https://www.prisma.io/) 可以大大提高开发效率。
- 构建应用的 RESTful API 时，建议 [使用 AWS Lambda 搭配 API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)。
- 关于使用 {{{ .starter }}} 和 AWS Lambda 构建高性能应用的最佳实践，参考 [这篇博客](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)。

## 后续步骤

- 想了解更多在 AWS Lambda 函数中使用 TiDB 的细节，可以查看我们的 [TiDB-Lambda-integration/aws-lambda-bookstore Demo](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)。你也可以使用 AWS API Gateway 构建应用的 RESTful API。
- 了解更多关于 `mysql2` 的用法，请参考 [mysql2 的文档](https://sidorares.github.io/node-mysql2/docs/documentation)。
- 了解更多关于 AWS Lambda 的用法，请参考 [AWS 开发者指南中的 `Lambda`](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)。
- 了解使用 [Developer guide](/develop/dev-guide-overview.md) 中的章节（如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Single table reading](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md)、[SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md)）的 TiDB 应用开发最佳实践。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>