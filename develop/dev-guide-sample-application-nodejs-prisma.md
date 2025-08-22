---
title: 使用 Prisma 连接 TiDB
summary: 学习如何使用 Prisma 连接 TiDB。本教程提供了适用于 Node.js 的示例代码片段，演示如何通过 Prisma 操作 TiDB。
---

# 使用 Prisma 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[Prisma](https://github.com/prisma/prisma) 是一个流行的开源 Node.js ORM 框架。

在本教程中，你可以学习如何使用 TiDB 和 Prisma 完成以下任务：

- 搭建你的开发环境。
- 使用 Prisma 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本 CRUD 操作的代码示例。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) >= 16.x。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 一个正在运行的 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

<CustomContent platform="tidb">

- （推荐）参照 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）参照 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### 步骤 2：安装依赖

运行以下命令，为示例应用安装所需的依赖包（包括 `prisma`）：

```shell
npm install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

如果是你的已有项目，运行以下命令安装依赖包：

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### 步骤 3：配置连接参数

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `Prisma`。
    - **Operating System** 选择你运行应用的操作系统。

4. 如果你还未设置密码，点击 **Generate Password** 生成随机密码。

5. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下方式设置环境变量 `DATABASE_URL`，并将对应的占位符 `{}` 替换为连接对话框中的连接字符串：

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **Note**
    >
    > 对于 {{{ .starter }}}，使用公网地址时，**必须** 通过设置 `sslaccept=strict` 启用 TLS 连接。

7. 保存 `.env` 文件。
8. 在 `prisma/schema.prisma` 文件中，将 `mysql` 设置为连接 provider，将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List**，或参照 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行首次连接前的配置。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下方式设置环境变量 `DATABASE_URL`，并将对应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **Note**
    >
    > 对于 {{{ .starter }}}，**推荐** 在使用公网地址时通过设置 `sslaccept=strict` 启用 TLS 连接。当你设置 `sslaccept=strict` 启用 TLS 连接时，**必须** 通过 `sslcert=/path/to/ca.pem` 指定从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。
7. 在 `prisma/schema.prisma` 文件中，将 `mysql` 设置为连接 provider，将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下方式设置环境变量 `DATABASE_URL`，并将对应的占位符 `{}` 替换为你的 TiDB 集群连接参数：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

   如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

4. 在 `prisma/schema.prisma` 文件中，将 `mysql` 设置为连接 provider，将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### 步骤 4：初始化数据库 schema

运行以下命令，调用 [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) 根据 `prisma/prisma.schema` 中定义的数据模型初始化数据库：

```shell
npx prisma migrate dev
```

**`prisma.schema` 中定义的数据模型：**

```prisma
// Define a Player model, which represents the `players` table.
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// Define a Profile model, which represents the `profiles` table.
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // Define a 1:1 relation between the `Player` and `Profile` models with foreign key.
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

如需了解如何在 Prisma 中定义数据模型，请查阅 [Data model](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model) 文档。

**预期执行输出：**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

该命令还会基于 `prisma/prisma.schema` 为 TiDB 数据库访问生成 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)。

### 步骤 5：运行代码

运行以下命令执行示例代码：

```shell
npm start
```

**示例代码的主要逻辑：**

```typescript
// Step 1. Import the auto-generated `@prisma/client` package.
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // Step 2. Create a new `PrismaClient` instance.
  const prisma = new PrismaClient();
  try {

    // Step 3. Perform some CRUD operations with Prisma Client ...

  } finally {
    // Step 4. Disconnect Prisma Client.
    await prisma.$disconnect();
  }
}

void main();
```

**预期执行输出：**

如果连接成功，终端会输出 TiDB 集群的版本信息，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v{{{ .tidb-version }}})
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参见 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart) 仓库。

### 插入数据

以下查询会创建一条 `Player` 记录，并返回包含 TiDB 生成的 `id` 字段的 `Player` 对象：

```javascript
const player: Player = await prisma.player.create({
   data: {
      name: 'Alice',
      coins: 100,
      goods: 200,
      createdAt: new Date(),
   }
});
```

更多信息请参见 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询会返回 ID 为 `101` 的 `Player` 对象，如果未找到则返回 `null`：

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

更多信息请参见 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询会为 ID 为 `101` 的 `Player` 增加 `50` 个 coins 和 `50` 个 goods：

```javascript
await prisma.player.update({
   where: {
      id: 101,
   },
   data: {
      coins: {
         increment: 50,
      },
      goods: {
         increment: 50,
      },
   }
});
```

更多信息请参见 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询会删除 ID 为 `101` 的 `Player`：

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

更多信息请参见 [删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 外键约束 vs Prisma relation mode

要检查 [参照完整性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)，你可以使用外键约束或 Prisma relation mode：

- [外键](https://docs.pingcap.com/tidb/stable/foreign-key) 是 TiDB v6.6.0 开始支持的特性，并在 v8.5.0 起正式可用。外键允许跨表引用相关数据，外键约束可确保相关数据的一致性。

    > **Warning:**
    >
    > **外键适用于中小数据量场景。** 在大数据量场景下使用外键可能导致严重的性能问题，并可能对系统产生不可预期的影响。如果你计划使用外键，请务必充分验证并谨慎使用。

- [Prisma relation mode](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode) 是在 Prisma Client 端模拟参照完整性。但需要注意的是，这会带来性能影响，因为它需要额外的数据库查询来维护参照完整性。

## 后续步骤

- 通过 [Prisma 官方文档](https://www.prisma.io/docs) 学习更多 ORM 框架 Prisma driver 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
