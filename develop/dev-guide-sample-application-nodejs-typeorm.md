---
title: 使用 TypeORM 连接 TiDB
summary: 学习如何使用 TypeORM 连接 TiDB。本教程提供了可在 Node.js 环境下通过 TypeORM 操作 TiDB 的示例代码片段。
---

# 使用 TypeORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[TypeORM](https://github.com/TypeORM/TypeORM) 是 Node.js 领域流行的开源 ORM 框架。

在本教程中，你将学习如何结合 TiDB 和 TypeORM 完成以下任务：

- 搭建开发环境
- 使用 TypeORM 连接到你的 TiDB 集群
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本的 CRUD 操作示例。

> **Note**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- 在本地安装 [Node.js](https://nodejs.org/en) >= 16.x
- 在本地安装 [Git](https://git-scm.com/downloads)
- 已有一个正在运行的 TiDB 集群

**如果你还没有 TiDB 集群，可以按如下方式创建：**

<CustomContent platform="tidb">

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用并连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用所需的依赖包（包括 `typeorm` 和 `mysql2`）：

```shell
npm install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

如果你是在已有项目中集成，运行以下命令安装相关依赖：

- `typeorm`：Node.js 的 ORM 框架
- `mysql2`：Node.js 的 MySQL 驱动。你也可以使用 `mysql` 驱动
- `dotenv`：从 `.env` 文件加载环境变量
- `typescript`：将 TypeScript 代码编译为 JavaScript
- `ts-node`：无需编译直接运行 TypeScript 代码
- `@types/node`：为 Node.js 提供 TypeScript 类型定义

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
```

</details>

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接信息对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 选择为 `Public`
    - **Branch** 选择为 `main`
    - **Connect With** 选择为 `General`
    - **Operating System** 选择你运行应用的操作系统

4. 如果你还未设置密码，点击 **Generate Password** 生成随机密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下格式设置环境变量，并将 `{}` 占位符替换为连接对话框中的参数：

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
    > 对于 {{{ .starter }}} 和 {{{ .essential }}}, 使用公网连接时你**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接信息对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List** 或参考 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置后再首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [连接 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下格式设置环境变量，并将 `{}` 占位符替换为连接对话框中的参数：

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
    > 对于 TiDB Cloud Dedicated，**推荐**在使用公网连接时通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。当你设置 `TIDB_ENABLE_SSL=true` 时，**必须**通过 `TIDB_CA_PATH=/path/to/ca.pem` 指定从连接对话框下载的 CA 证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB 自建集群">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下格式设置环境变量，并将 `{}` 占位符替换为你的 TiDB 集群连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：初始化数据库结构

运行以下命令，调用 TypeORM CLI，根据 `src/migrations` 文件夹下的 migration 文件中的 SQL 语句初始化数据库：

```shell
npm run migration:run
```

<details>
<summary><b>预期执行输出</b></summary>

以下 SQL 语句会创建 `players` 表和 `profiles` 表，并通过外键将两张表关联起来。

```sql
query: SELECT VERSION() AS `version`
query: SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'migrations'
query: CREATE TABLE `migrations` (`id` int NOT NULL AUTO_INCREMENT, `timestamp` bigint NOT NULL, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB
query: SELECT * FROM `test`.`migrations` `migrations` ORDER BY `id` DESC
0 migrations are already loaded in the database.
1 migrations were found in the source code.
1 migrations are new migrations must be executed.
query: START TRANSACTION
query: CREATE TABLE `profiles` (`player_id` int NOT NULL, `biography` text NOT NULL, PRIMARY KEY (`player_id`)) ENGINE=InnoDB
query: CREATE TABLE `players` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `coins` decimal NOT NULL, `goods` int NOT NULL, `created_at` datetime NOT NULL, `profilePlayerId` int NULL, UNIQUE INDEX `uk_players_on_name` (`name`), UNIQUE INDEX `REL_b9666644b90ccc5065993425ef` (`profilePlayerId`), PRIMARY KEY (`id`)) ENGINE=InnoDB
query: ALTER TABLE `players` ADD CONSTRAINT `fk_profiles_on_player_id` FOREIGN KEY (`profilePlayerId`) REFERENCES `profiles`(`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
query: INSERT INTO `test`.`migrations`(`timestamp`, `name`) VALUES (?, ?) -- PARAMETERS: [1693814724825,"Init1693814724825"]
Migration Init1693814724825 has been  executed successfully.
query: COMMIT
```

</details>

Migration 文件是根据 `src/entities` 文件夹下定义的实体自动生成的。关于如何在 TypeORM 中定义实体，参考 [TypeORM: Entities](https://typeorm.io/entities)。

### 步骤 5：运行代码并查看结果

运行以下命令执行示例代码：

```shell
npm start
```

**预期执行输出：**

如果连接成功，终端会输出 TiDB 集群的版本信息，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v{{{ .tidb-version }}})
🆕 Created a new player with ID 2.
ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式请参考 [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart) 仓库。

### 使用连接参数连接

以下代码通过环境变量定义的参数建立与 TiDB 的连接：

```typescript
// src/dataSource.ts

// Load environment variables from .env file to process.env.
require('dotenv').config();

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.TIDB_HOST || '127.0.0.1',
  port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000,
  username: process.env.TIDB_USER || 'root',
  password: process.env.TIDB_PASSWORD || '',
  database: process.env.TIDB_DATABASE || 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
    minVersion: 'TLSv1.2',
    ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
  } : null,
  synchronize: process.env.NODE_ENV === 'development',
  logging: false,
  entities: [Player, Profile],
  migrations: [__dirname + "/migrations/**/*{.ts,.js}"],
});
```

> **Note**
>
> 对于 {{{ .starter }}} 和 {{{ .essential }}}, 使用公网连接时你必须启用 TLS 连接。在本示例代码中，请在 `.env` 文件中将环境变量 `TIDB_ENABLE_SSL` 设置为 `true`。
>
> 但你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书已被 {{{ .starter }}} 和 {{{ .essential }}} 信任。

### 插入数据

以下查询会创建一条 `Player` 记录，并返回包含 TiDB 生成的 `id` 字段的 `Player` 对象：

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

更多信息参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询会返回 ID 为 101 的 `Player` 对象，如果未找到则返回 `null`：

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

更多信息参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询会为 ID 为 `101` 的 `Player` 增加 `50` 个 goods：

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

更多信息参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询会删除 ID 为 `101` 的 `Player`：

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

更多信息参考 [删除数据](/develop/dev-guide-delete-data.md)。

### 执行原生 SQL 查询

以下查询会执行一条原生 SQL 语句（`SELECT VERSION() AS tidb_version;`），并返回 TiDB 集群的版本号：

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

更多信息参考 [TypeORM: DataSource API](https://typeorm.io/data-source-api)。

## 实用说明

### 外键约束

使用 [外键约束](https://docs.pingcap.com/tidb/stable/foreign-key) 可以通过在数据库端增加校验，保证数据的 [引用完整性](https://en.wikipedia.org/wiki/Referential_integrity)。但在大数据量场景下，可能会带来严重的性能问题。

你可以通过 `createForeignKeyConstraints` 选项（默认值为 `true`）控制在实体间建立关系时是否创建外键约束。

```typescript
@Entity()
export class ActionLog {
    @PrimaryColumn()
    id: number

    @ManyToOne((type) => Person, {
        createForeignKeyConstraints: false,
    })
    person: Person
}
```

更多信息参考 [TypeORM FAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation) 以及 [外键约束](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints)。

## 后续步骤

- 通过 [TypeORM 官方文档](https://typeorm.io/) 学习更多 TypeORM 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
