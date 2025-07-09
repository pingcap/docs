---
title: 使用 mysql2 在 Next.js 中连接 TiDB
summary: 本文介绍如何在 Next.js 中结合 TiDB 和 mysql2 构建一个 CRUD 应用，并提供一个简单的示例代码片段。
---

# 使用 mysql2 在 Next.js 中连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[mysql2](https://github.com/sidorares/node-mysql2) 是一个在 Node.js 中广泛使用的开源驱动程序。

在本教程中，你可以学习如何在 Next.js 中使用 TiDB 和 mysql2 来完成以下任务：

- 设置你的环境。
- 使用 mysql2 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你可以查阅 [示例代码片段](#sample-code-snippets) 来实现基本的 CRUD 操作。

> **Note**
>
> 本教程适用于 {{{ .starter }}} 和 TiDB 自托管版本。

## 前提条件

完成本教程，你需要：

- [Node.js **18**](https://nodejs.org/en/download/) 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例代码并连接到 TiDB。

> **Note**
>
> 完整的代码片段和运行说明，请参考 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub 仓库。

### 第一步：克隆示例应用仓库

在终端中运行以下命令以克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### 第二步：安装依赖

运行以下命令以安装示例应用所需的包（包括 `mysql2`）：

```bash
npm install
```

### 第三步：配置连接信息

根据你选择的 TiDB 部署方式，配置连接到你的 TiDB 集群。

<SimpleTab>

<div label="{{{ .starter }}}">

1. 进入 [**Clusters** 页面](https://tidbcloud.com/project/clusters)，点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的环境匹配。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致。

    > **Note**
    >
    > 在 Node.js 应用中，你无需提供 SSL CA 证书，因为 Node.js 在建立 TLS（SSL）连接时默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip**
    >
    > 如果之前已创建密码，可以使用原有密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例内容如下：

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    将 `{}` 中的占位符替换为连接对话框中获得的实际值。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例内容如下：

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    将 `{}` 中的占位符替换为在 **Connect** 窗口中获得的实际值。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第四步：运行代码并查看结果

1. 启动应用：

   ```bash
   npm run dev
   ```

2. 打开浏览器，访问 `http://localhost:3000`。（检查终端中的实际端口号，默认是 `3000`。）

3. 点击 **RUN SQL** 执行示例代码。

4. 查看终端输出。如果输出类似如下内容，说明连接成功：

   ```json
   {
     "results": [
       {
         "Hello World": "Hello World"
       }
     ]
   }
   ```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码和运行方式，请查阅 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) 仓库。

### 连接到 TiDB

以下代码通过环境变量中定义的配置建立与 TiDB 的连接：

```javascript
// src/lib/tidb.js
import mysql from 'mysql2';

let pool = null;

export function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB 主机，例如：{gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB 端口，默认：4000
    user: process.env.TIDB_USER, // TiDB 用户，例如：{prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB 用户的密码
    database: process.env.TIDB_DATABASE || 'test', // TiDB 数据库名，默认：test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // 在无服务器函数环境中，将 connectionLimit 设置为“1”可以优化资源使用，降低成本，确保连接稳定，并实现无缝扩展。
    maxIdle: 1, // 最大空闲连接数，默认值与 `connectionLimit` 相同
    enableKeepAlive: true,
  });
}

export function getPool() {
  if (!pool) {
    pool = createPool();
  }
  return pool;
}
```

### 插入数据

以下查询创建一个 `Player` 记录，并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询根据 ID `1` 返回一个 `Player` 记录：

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 添加 `50` 个金币和 `50` 件商品：

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 有用的注意事项

- 使用 [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) 管理数据库连接，可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入，建议使用 [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在涉及不多复杂 SQL 语句的场景中，使用 ORM 框架如 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/) 可以大大提高开发效率。

## 后续步骤

- 想了解如何结合 ORM 和 Next.js 构建复杂应用，请查看 [我们的 Bookshop Demo](https://github.com/pingcap/tidb-prisma-vercel-demo)。
- 了解更多 node-mysql2 驱动的用法，请参考 [node-mysql2 的文档](https://sidorares.github.io/node-mysql2/docs/documentation)。
- 学习 TiDB 应用开发的最佳实践，参考 [开发者指南]( /develop/dev-guide-overview.md) 中的章节，如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Single table reading](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>