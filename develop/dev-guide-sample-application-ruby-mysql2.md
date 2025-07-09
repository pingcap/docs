---
title: 使用 mysql2 连接 TiDB
summary: 学习如何使用 Ruby mysql2 连接 TiDB。本教程提供适用于 TiDB 的 Ruby 示例代码片段，使用 mysql2 gem。
---

# 使用 mysql2 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[mysql2](https://github.com/brianmario/mysql2) 是 Ruby 中最受欢迎的 MySQL 驱动之一。

在本教程中，你可以学习如何使用 TiDB 和 mysql2 完成以下任务：

- 设置你的环境。
- 使用 mysql2 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以查阅 [示例代码片段](#sample-code-snippets) 来了解基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB 自托管版本。

## 前提条件

完成本教程，你需要：

- 在你的机器上安装 [Ruby](https://www.ruby-lang.org/en/) >= 3.0
- 在你的机器上安装 [Bundler](https://bundler.io/)
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 运行中的 TiDB 集群

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

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
```

### 步骤 2：安装依赖

运行以下命令以安装示例应用所需的包（包括 `mysql2` 和 `dotenv`）：

```shell
bundle install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

对于你的已有项目，运行以下命令以安装包：

```shell
bundle add mysql2 dotenv
```

</details>

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式，配置连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

   - **Connection Type** 设置为 `Public`。
   - **Branch** 设置为 `main`。
   - **Connect With** 设置为 `General`。
   - **Operating System** 与你运行应用的操作系统一致。

4. 如果还未设置密码，点击 **Generate Password** 生成随机密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照以下方式设置环境变量，并用连接对话框中的参数替换对应的占位符 `{}`：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    ```

   > **Note**
   >
   > 对于 {{{ .starter }}}，使用公共端点时**必须**启用 TLS 连接，通过 `DATABASE_ENABLE_SSL` 设置为 `true`，并在连接对话框中下载的 SSL CA 证书路径填写到 `DATABASE_SSL_CA`。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果还未配置 IP 访问列表，点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照以下方式设置环境变量，并用连接对话框中的参数替换对应的 `{}` 占位符：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    DATABASE_SSL_CA={downloaded_ssl_ca_path}
    ```

   > **Note**
   >
   > 建议在使用公共端点连接 TiDB Cloud Dedicated 集群时启用 TLS 连接。
   >
   > 要启用 TLS 连接，将 `DATABASE_ENABLE_SSL` 设置为 `true`，并用 `DATABASE_SSL_CA` 指定从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB 自托管">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照以下方式设置环境变量，并用连接信息中的参数替换 `{}` 占位符：

    ```dotenv
    DATABASE_HOST={host}
    DATABASE_PORT=4000
    DATABASE_USER={user}
    DATABASE_PASSWORD={password}
    DATABASE_NAME=test
    ```

   如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并查看结果

运行以下命令执行示例代码：

```shell
ruby app.rb
```

如果连接成功，控制台会输出 TiDB 集群的版本信息，例如：

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

完整示例代码及运行方式，请查阅 [tidb-samples/tidb-ruby-mysql2-quickstart](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart) 仓库。

### 使用连接选项连接 TiDB

以下代码使用环境变量中定义的参数建立连接：

```ruby
require 'dotenv/load'
require 'mysql2'
Dotenv.load # 从 .env 文件加载环境变量

options = {
  host: ENV['DATABASE_HOST'] || '127.0.0.1',
  port: ENV['DATABASE_PORT'] || 4000,
  username: ENV['DATABASE_USER'] || 'root',
  password: ENV['DATABASE_PASSWORD'] || '',
  database: ENV['DATABASE_NAME'] || 'test'
}
options.merge(ssl_mode: :verify_identity) unless ENV['DATABASE_ENABLE_SSL'] == 'false'
options.merge(sslca: ENV['DATABASE_SSL_CA']) if ENV['DATABASE_SSL_CA']
client = Mysql2::Client.new(options)
```

> **Note**
>
> 对于 {{{ .starter }}}，使用公共端点时**必须**启用 TLS 连接，通过 `DATABASE_ENABLE_SSL` 设置为 `true`，但你**不需要**通过 `DATABASE_SSL_CA` 指定 SSL CA 证书文件路径，因为 mysql2 gem 会按特定顺序搜索现有的 CA 证书，直到找到文件。

### 插入数据

以下查询创建一个包含两个字段的单个玩家，并返回 `last_insert_id`：

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回指定 ID 的玩家记录：

```ruby
def get_player_by_id(client, id)
  result = client.query(
    "SELECT id, coins, goods FROM players WHERE id = #{id};"
  )
  result.first
end
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询更新指定 ID 的玩家记录：

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除指定 ID 的玩家记录：

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，mysql2 gem 会按特定顺序搜索现有的 CA 证书，直到找到文件。

1. `/etc/ssl/certs/ca-certificates.crt` 适用于 Debian、Ubuntu、Gentoo、Arch 或 Slackware
2. `/etc/pki/tls/certs/ca-bundle.crt` 适用于 RedHat、Fedora、CentOS、Mageia、Vercel 或 Netlify
3. `/etc/ssl/ca-bundle.pem` 适用于 OpenSUSE
4. `/etc/ssl/cert.pem` 适用于 macOS 或 Alpine（docker 容器）

虽然可以手动指定 CA 证书路径，但在多环境部署场景中这样做可能会带来较大不便，因为不同的机器和环境可能会将 CA 证书存放在不同位置。因此，建议将 `sslca` 设置为 `nil`，以增强灵活性并简化跨环境部署。

## 后续步骤

- 通过 [mysql2 的文档](https://github.com/brianmario/mysql2#readme) 了解更多关于 mysql2 驱动的用法。
- 参考 [开发者指南](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如： [Insert data](/develop/dev-guide-insert-data.md)、 [Update data](/develop/dev-guide-update-data.md)、 [Delete data](/develop/dev-guide-delete-data.md)、 [Query data](/develop/dev-guide-get-data-from-single-table.md)、 [Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>