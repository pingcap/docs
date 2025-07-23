---
title: 使用 Prisma 连接 TiDB
summary: 学习如何使用 Prisma 连接 TiDB。本教程提供适用于 TiDB 的 Node.js 示例代码片段，演示如何通过 Prisma 进行操作。
---

# 使用 Prisma 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Prisma](https://github.com/prisma/prisma) 是一个流行的开源 ORM 框架，适用于 Node.js。

在本教程中，你可以学习如何使用 TiDB 和 Prisma 完成以下任务：

- 设置你的环境。
- 使用 Prisma 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以查阅 [示例代码片段](#sample-code-snippets) 以了解基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) >= 16.x。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 运行中的 TiDB 集群。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- (推荐) 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### 步骤 2：安装依赖

运行以下命令以安装示例应用所需的包（包括 `prisma`）：

```shell
npm install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

对于你的已有项目，运行以下命令以安装相关包：

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### 步骤 3：提供连接参数

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 确认连接对话框中的配置与你的环境匹配。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `Prisma`。
    - **Operating System** 与你运行应用的操作系统一致。

4. 如果还没有设置密码，可以点击 **Generate Password** 生成随机密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，配置环境变量 `DATABASE_URL`，将其中的占位符 `{}` 替换为连接对话框中的连接字符串：

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **注意**
    >
    > 对于 {{{ .starter }}}，使用公共端点时**必须**启用 TLS 连接，方法是在连接字符串中设置 `sslaccept=strict`。

7. 保存 `.env` 文件。
8. 在 `prisma/schema.prisma` 中，将 `mysql` 设为数据源提供者，将 `env("DATABASE_URL")` 设为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果还没有配置 IP 访问列表，可以点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，配置环境变量 `DATABASE_URL`，用连接对话框中的参数替换对应的占位符 `{}`：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **注意**
    >
    > 对于 {{{ .starter }}}，建议在使用公共端点时启用 TLS 连接，方法是在连接字符串中设置 `sslaccept=strict`。启用 TLS 后，**必须**通过 `sslcert=/path/to/ca.pem` 指定从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。
7. 在 `prisma/schema.prisma` 中，将 `mysql` 设为数据源提供者，将 `env("DATABASE_URL")` 设为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，配置环境变量 `DATABASE_URL`，用你的 TiDB 集群的连接参数替换 `{}` 占位符：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

   如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

4. 在 `prisma/schema.prisma` 中，将 `mysql` 设为数据源提供者，将 `env("DATABASE_URL")` 设为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### 步骤 4：初始化数据库 schema

运行以下命令，调用 [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) 来根据 `prisma/prisma.schema` 中定义的数据模型初始化数据库。

```shell
npx prisma migrate dev
```

**在 `prisma.schema` 中定义的数据模型：**

```prisma
// 定义一个 Player 模型，代表 `players` 表。
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// 定义一个 Profile 模型，代表 `profiles` 表。
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // 定义 `Player` 和 `Profile` 模型之间的一对一关系，带外键。
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

想了解如何在 Prisma 中定义数据模型，请查阅 [Data model](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model) 文档。

**预期执行输出：**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

此命令还会基于 `prisma/prisma.schema` 生成用于访问 TiDB 数据库的 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)。

### 步骤 5：运行代码

运行以下命令执行示例代码：

```shell
npm start
```

**示例代码中的主要逻辑：**

```typescript
// 步骤 1. 导入自动生成的 `@prisma/client` 包。
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // 步骤 2. 创建一个新的 `PrismaClient` 实例。
  const prisma = new PrismaClient();
  try {

    // 步骤 3. 使用 Prisma Client 执行一些 CRUD 操作...

  } finally {
    // 步骤 4. 断开 Prisma Client 连接。
    await prisma.$disconnect();
  }
}

void main();
```

**预期执行输出：**

如果连接成功，终端会输出 TiDB 集群的版本信息，例如：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-{{{ .tidb-version }}})
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式，请查阅 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart) 仓库。

### 插入数据

以下查询创建一个 `Player` 记录，并返回包含 TiDB 生成的 `id` 字段的 `Player` 对象：

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

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回 ID 为 `101` 的单个 `Player` 对象，如果没有找到记录，则返回 `null`：

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `101` 的 `Player` 添加 `50` 个金币和 `50` 个商品：

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

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `101` 的 `Player`：

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 有用的注意事项

### Foreign key constraints vs Prisma relation mode

为了检查 [referential integrity](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)，你可以使用外键约束或 Prisma relation mode：

- [Foreign key](https://docs.pingcap.com/tidb/stable/foreign-key) 是从 TiDB v6.6.0 开始支持的功能，v8.5.0 及以上版本已普遍支持。外键允许跨表引用相关数据，而外键约束确保相关数据的一致性。

    > **Warning:**
    >
    > **Foreign keys 适用于小到中等规模的数据场景。** 在大数据量场景下使用外键可能导致严重的性能问题，并对系统产生不可预料的影响。如果你打算使用外键，务必先进行充分验证，并谨慎使用。

- [Prisma relation mode](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode) 是在 Prisma Client 端模拟引用完整性，但需要注意的是，它会带来性能影响，因为需要额外的数据库查询来维护引用完整性。

## 后续步骤

- 了解更多关于 ORM 框架 Prisma 驱动的用法，请参考 [Prisma 文档](https://www.prisma.io/docs)。
- 学习 TiDB 应用开发的最佳实践，参考 [开发者指南]( /develop/dev-guide-overview.md) 中的章节，例如： [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Query data](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>