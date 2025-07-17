---
title: 使用 Sequelize 连接 TiDB
summary: 学习如何使用 Sequelize 连接 TiDB。本教程提供了适用于 TiDB 的 Node.js 示例代码片段，使用 Sequelize 实现。
---

# 使用 Sequelize 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Sequelize](https://sequelize.org/) 是 Node.js 中流行的 ORM 框架。

在本教程中，你可以学习如何使用 TiDB 和 Sequelize 完成以下任务：

- 设置你的环境。
- 使用 Sequelize 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以查阅 [示例代码片段](#sample-code-snippets) 以了解基本的 CRUD 操作。

> **Note**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- [Node.js **18**](https://nodejs.org/en/download/) 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接到 TiDB

本节演示如何运行示例代码并连接到 TiDB。

> **Note**
>
> 完整的代码片段和运行说明，请参考 [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart) GitHub 仓库。

### 第一步：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-nodejs-sequelize-quickstart.git
cd tidb-nodejs-sequelize-quickstart
```

### 第二步：安装依赖

运行以下命令以安装示例应用所需的包（包括 `sequelize`）：

```bash
npm install
```

### 第三步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>

<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

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
    > 如果之前已生成过密码，可以使用原有密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照以下方式设置环境变量，将对应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    ```

7. 保存 `.env` 文件。

</div>

<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照以下方式设置环境变量，将对应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```shell
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    TIDB_CA_PATH='{path/to/ca}'
    ```

6. 保存 `.env` 文件。

</div>

<div label="TiDB Self-Managed">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照以下方式设置环境变量，将对应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```shell
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第四步：运行示例应用

运行以下命令执行示例代码：

```shell
npm start
```

<details>
<summary>**预期输出（部分）：**</summary>

```shell
INFO (app/10117): Getting sequelize instance...
Executing (default): SELECT 1+1 AS result
Executing (default): DROP TABLE IF EXISTS `players`;
Executing (default): CREATE TABLE IF NOT EXISTS `players` (`id` INTEGER NOT NULL auto_increment  COMMENT 'The unique ID of the player.', `coins` INTEGER NOT NULL COMMENT 'The number of coins that the player had.', `goods` INTEGER NOT NULL COMMENT 'The number of goods that the player had.', `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB;
Executing (default): SHOW INDEX FROM `players`
Executing (default): INSERT INTO `players` (`id`,`coins`,`goods`,`createdAt`,`updatedAt`) VALUES (1,100,100,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(2,200,200,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(3,300,300,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(4,400,400,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(5,500,500,'2023-08-31 09:10:11','2023-08-31 09:10:11');
Executing (default): SELECT `id`, `coins`, `goods`, `createdAt`, `updatedAt` FROM `players` AS `players` WHERE `players`.`coins` > 300;
Executing (default): UPDATE `players` SET `coins`=?,`goods`=?,`updatedAt`=? WHERE `id` = ?
Executing (default): DELETE FROM `players` WHERE `id` = 6
```

</details>

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码和运行方式，请查看 [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart) 仓库。

### 连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```typescript
// src/lib/tidb.ts
import { Sequelize } from 'sequelize';

export function initSequelize() {
  return new Sequelize({
    dialect: 'mysql',
    host: process.env.TIDB_HOST || 'localhost',     // TiDB host，例如：{gateway-region}.aws.tidbcloud.com
    port: Number(process.env.TIDB_PORT) || 4000,    // TiDB 端口，默认：4000
    username: process.env.TIDB_USER || 'root',      // TiDB 用户，例如：{prefix}.root
    password: process.env.TIDB_PASSWORD || 'root',  // TiDB 密码
    database: process.env.TIDB_DB_NAME || 'test',   // TiDB 数据库名，默认：test
    dialectOptions: {
      ssl:
        process.env?.TIDB_ENABLE_SSL === 'true'     // （可选）启用 SSL
          ? {
              minVersion: 'TLSv1.2',
              rejectUnauthorized: true,
              ca: process.env.TIDB_CA_PATH          // （可选）自定义 CA 证书路径
                ? readFileSync(process.env.TIDB_CA_PATH)
                : undefined,
            }
          : null,
    },
}

export async function getSequelize() {
  if (!sequelize) {
    sequelize = initSequelize();
    try {
      await sequelize.authenticate();
      logger.info('连接已成功建立。');
    } catch (error) {
      logger.error('无法连接到数据库：');
      logger.error(error);
      throw error;
    }
  }
  return sequelize;
}
```

### 插入数据

以下示例创建一条 `Players` 记录，并返回一个 `Players` 对象：

```typescript
logger.info('创建新玩家...');
const newPlayer = await playersModel.create({
  id: 6,
  coins: 600,
  goods: 600,
});
logger.info('新玩家已创建。');
logger.info(newPlayer.toJSON());
```

更多信息，请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回所有 `coins` 大于 `300` 的 `Players` 记录：

```typescript
logger.info('读取所有 coins > 300 的玩家...');
const allPlayersWithCoinsGreaterThan300 = await playersModel.findAll({
  where: {
    coins: {
      [Op.gt]: 300,
    },
  },
});
logger.info('已读取所有 coins > 300 的玩家。');
logger.info(allPlayersWithCoinsGreaterThan300.map((p) => p.toJSON()));
```

更多信息，请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询将 `ID` 为 `6` 的 `Players` 的 `coins` 和 `goods` 设置为 `700`，该记录在 [插入数据](#insert-data) 部分创建：

```typescript
logger.info('更新新玩家...');
await newPlayer.update({ coins: 700, goods: 700 });
logger.info('已更新新玩家。');
logger.info(newPlayer.toJSON());
```

更多信息，请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除在 [插入数据](#insert-data) 部分创建的 `ID` 为 `6` 的 `Player` 记录：

```typescript
logger.info('删除新玩家...');
await newPlayer.destroy();
const deletedNewPlayer = await playersModel.findByPk(6);
logger.info('已删除新玩家。');
logger.info(deletedNewPlayer?.toJSON());
```

更多信息，请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 了解更多关于 ORM 框架 Sequelize 驱动的用法，请参考 [Sequelize 文档](https://sequelize.org/)。
- 通过 [开发者指南](https://github.com/pingcap/tidb-dev-guide) 中的章节学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Single table reading](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>