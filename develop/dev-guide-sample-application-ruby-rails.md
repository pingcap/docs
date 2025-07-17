---
title: 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB
summary: 学习如何使用 Rails 框架连接 TiDB。本教程提供了适用于 TiDB 的 Ruby 示例代码片段，结合 Rails 框架和 ActiveRecord ORM。
---

# 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Rails](https://github.com/rails/rails) 是用 Ruby 编写的流行 Web 应用框架，[ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord) 是 Rails 中的对象关系映射。

在本教程中，你可以学习如何使用 TiDB 和 Rails 完成以下任务：

- 设置你的环境。
- 使用 Rails 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以查阅 [示例代码片段](#sample-code-snippets) 来了解使用 ActiveRecord ORM 进行基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- 在你的机器上安装 [Ruby](https://www.ruby-lang.org/en/) >= 3.0
- 在你的机器上安装 [Bundler](https://bundler.io/)
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 运行中的 TiDB 集群

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- (推荐) 参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第一步：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### 第二步：安装依赖

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

### 第三步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 在连接对话框中，从 **Connect With** 下拉列表中选择 `Rails`，并保持 **Connection Type** 的默认设置为 `Public`。

4. 如果还没有设置密码，点击 **Generate Password** 以生成随机密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，配置 `DATABASE_URL` 环境变量，内容如下，并将连接对话框中的连接字符串复制到变量值中。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity'
    ```

   > **Note**
   >
   > 对于 {{{ .starter }}}，使用公共端点时，**必须**在 `DATABASE_URL` 中启用 TLS 连接，并设置 `ssl_mode=verify_identity` 查询参数。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果还没有配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，配置 `DATABASE_URL` 环境变量，内容如下，将连接对话框中的连接字符串复制到变量值中，并将 `sslca` 查询参数设置为下载的 CA 证书文件路径：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem'
    ```

   > **Note**
   >
   > 建议在使用公共端点连接 TiDB Cloud Dedicated 时启用 TLS 连接。
   >
   > 要启用 TLS 连接，请将 `ssl_mode` 查询参数的值修改为 `verify_identity`，并将 `sslca` 的值设置为从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，配置 `DATABASE_URL` 环境变量，内容如下，并将 `{user}`、`{password}`、`{host}`、`{port}` 和 `{database}` 替换为你自己的 TiDB 连接信息：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}'
    ```

   如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第四步：运行代码并检查结果

1. 创建数据库和表：

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2. 填充示例数据：

    ```shell
    bundle exec rails db:seed
    ```

3. 运行以下命令执行示例代码：

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

如果连接成功，控制台将输出 TiDB 集群的版本信息，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-{{{ .tidb-version }}})
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式，请查阅 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart) 仓库。

### 使用连接选项连接 TiDB

以下代码在 `config/database.yml` 中，利用环境变量中的配置建立到 TiDB 的连接：

```yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  url: <%= ENV["DATABASE_URL"] %>

development:
  <<: *default

test:
  <<: *default
  database: quickstart_test

production:
  <<: *default
```

> **Note**
>
> 对于 {{{ .starter }}}，在使用公共端点连接时，**必须**通过在 `DATABASE_URL` 中设置 `ssl_mode=verify_identity` 来启用 TLS 连接，但你**不需要**通过 `DATABASE_URL` 指定 SSL CA 证书，因为 mysql2 gem 会按特定顺序搜索现有的 CA 证书，直到找到文件为止。

### 插入数据

以下查询创建一个包含两个字段的 Player，并返回创建的 `Player` 对象：

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回指定 ID 的玩家记录：

```ruby
player = Player.find_by(id: new_player.id)
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询更新一个 `Player` 对象：

```ruby
player.update(coins: 50, goods: 50)
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除一个 `Player` 对象：

```ruby
player.destroy
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，ActiveRecord 使用的 mysql2 gem（连接 TiDB）会按特定顺序搜索现有的 CA 证书，直到找到文件。

1. /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2. /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3. /etc/ssl/ca-bundle.pem # OpenSUSE
4. /etc/ssl/cert.pem # MacOS / Alpine (docker 容器)

虽然可以手动指定 CA 证书路径，但在多环境部署场景中，这种方式可能带来较大不便，因为不同的机器和环境可能存放 CA 证书的位置不同。因此，建议将 `sslca` 设置为 `nil`，以实现更好的灵活性和跨环境的部署便利。

## 后续步骤

- 了解更多 ActiveRecord ORM 的用法，请参考 [ActiveRecord 官方文档](https://guides.rubyonrails.org/active_record_basics.html)。
- 学习 TiDB 应用开发的最佳实践，参考 [开发者指南]( /develop/dev-guide-overview.md) 中的章节，例如： [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Query data](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>