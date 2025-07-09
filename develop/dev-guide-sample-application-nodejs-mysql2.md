---
title: 使用 node-mysql2 连接 TiDB
summary: 学习如何使用 node-mysql2 连接 TiDB。本教程提供适用于 TiDB 的 Node.js 示例代码片段，使用 node-mysql2。
---

# 使用 node-mysql2 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[node-mysql2](https://github.com/sidorares/node-mysql2) 是一个快速的与 [mysqljs/mysql](https://github.com/mysqljs/mysql) 兼容的 MySQL 驱动程序，适用于 Node.js。

在本教程中，你可以学习如何使用 TiDB 和 node-mysql2 完成以下任务：

- 设置你的环境。
- 使用 node-mysql2 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以查阅 [示例代码片段](#sample-code-snippets) 来实现基本的 CRUD 操作。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) >= 16.x。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 运行中的 TiDB 集群。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接到 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart.git
cd tidb-nodejs-mysql2-quickstart
```

### 步骤 2：安装依赖

运行以下命令以安装示例应用所需的包（包括 `mysql2` 和 `dotenv`）：

```shell
npm install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

对于你的已有项目，运行以下命令以安装相关包：

```shell
npm install mysql2 dotenv --save
```

</details>

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式，配置连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 确认连接对话框中的配置与你的操作环境匹配。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `General`。
    - **Operating System** 与你运行应用的操作系统一致。

4. 如果还未设置密码，点击 **Generate Password** 生成随机密码。

5. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照以下方式设置环境变量，将连接对话框中的对应占位符 `{}` 替换为连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

    > **Note**
    >
    > 对于 {{{ .starter }}}，使用公共端点连接时，**必须**启用 TLS 连接，通过 `TIDB_ENABLE_SSL` 设置为 `true`。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果还未配置 IP 访问列表，点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照以下方式设置环境变量，将连接对话框中的对应占位符 `{}` 替换为连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH={downloaded_ssl_ca_path}
    ```

    > **Note**
    >
    > 建议在使用公共端点连接 TiDB Cloud Dedicated 时启用 TLS 连接。
    >
    > 要启用 TLS 连接，将 `TIDB_ENABLE_SSL` 设置为 `true`，并使用 `TIDB_CA_PATH` 指定从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照以下方式设置环境变量，将连接对话框中的对应占位符 `{}` 替换为连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

   如果你在本地运行 TiDB，默认的主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并查看结果

运行以下命令执行示例代码：

```shell
npm start
```

如果连接成功，控制台会输出 TiDB 集群的版本信息，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码和运行方式，请查看 [tidb-samples/tidb-nodejs-mysql2-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart) 仓库。

### 使用连接选项连接

以下代码使用环境变量中定义的参数建立到 TiDB 的连接：

```javascript
// Step 1. 导入 'mysql' 和 'dotenv' 包。
import { createConnection } from "mysql2/promise";
import dotenv from "dotenv";
import * as fs from "fs";

// Step 2. 从 .env 文件加载环境变量到 process.env。
dotenv.config();

async function main() {
   // Step 3. 创建到 TiDB 集群的连接。
   const options = {
      host: process.env.TIDB_HOST || '127.0.0.1',
      port: process.env.TIDB_PORT || 4000,
      user: process.env.TIDB_USER || 'root',
      password: process.env.TIDB_PASSWORD || '',
      database: process.env.TIDB_DATABASE || 'test',
      ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
         minVersion: 'TLSv1.2',
         ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
      } : null,
   }
   const conn = await createConnection(options);

   // Step 4. 执行一些 SQL 操作...

   // Step 5. 关闭连接。
   await conn.end();
}

void main();
```

> **Note**
>
> 对于 {{{ .starter }}}，在使用公共端点连接时，**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。不过，你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书文件路径，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，这是被 {{{ .starter }}} 信任的。

### 插入数据

以下查询创建一个 `Player` 记录，并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询根据 ID `1` 返回一个 `Player` 记录：

```javascript
const [rows] = await conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID `1` 的 `Player` 添加 `50` 个金币和 `50` 件商品：

```javascript
const [rsh] = await conn.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```javascript
const [rsh] = await conn.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 有用的注意事项

- 使用 [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) 管理数据库连接，可以减少频繁建立和销毁连接带来的性能开销。
- 为避免 SQL 注入，建议使用 [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在涉及较多复杂 SQL 语句的场景中，使用 ORM 框架如 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/)、或 [Prisma](https://www.prisma.io/) 可以大大提高开发效率。
- 建议在处理数据库中的大数字（如 `BIGINT` 和 `DECIMAL` 列）时启用 `supportBigNumbers: true` 选项。
- 建议启用 `enableKeepAlive: true` 选项，以避免因网络问题导致的 socket 错误 `read ECONNRESET`。（相关问题： [sidorares/node-mysql2#683](https://github.com/sidorares/node-mysql2/issues/683)）

## 后续步骤

- 通过 [node-mysql2 的文档](https://github.com/sidorares/node-mysql2#readme) 了解更多驱动的用法。
- 参考 [开发者指南](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如： [Insert data](/develop/dev-guide-insert-data.md)、 [Update data](/develop/dev-guide-update-data.md)、 [Delete data](/develop/dev-guide-delete-data.md)、 [Query data](/develop/dev-guide-get-data-from-single-table.md)、 [Transactions](/develop/dev-guide-transaction-overview.md)、 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>