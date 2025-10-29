---
title: 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB
summary: 学习如何使用 Rails 框架连接 TiDB。本教程提供了可在 Rails 框架下通过 ActiveRecord ORM 操作 TiDB 的 Ruby 示例代码片段。
---

# 使用 Rails 框架和 ActiveRecord ORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[Rails](https://github.com/rails/rails) 是一个流行的 Ruby Web 应用框架，[ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord) 是 Rails 中的对象关系映射组件。

在本教程中，你可以学习如何使用 TiDB 和 Rails 完成以下任务：

- 搭建你的开发环境
- 使用 Rails 连接到你的 TiDB 集群
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基于 ActiveRecord ORM 的基本 CRUD 操作示例。

> **Note:**
>
> 本教程适用于 TiDB Cloud Starter、TiDB Cloud Essential、TiDB Cloud Dedicated 以及自建 TiDB 集群。

## 前置条件

完成本教程，你需要：

- 在本地安装 [Ruby](https://www.ruby-lang.org/en/)，版本 >= 3.0
- 在本地安装 [Bundler](https://bundler.io/)
- 在本地安装 [Git](https://git-scm.com/downloads)
- 已有一个正在运行的 TiDB 集群

**如果你还没有 TiDB 集群，可以按如下方式创建：**

<CustomContent platform="tidb">

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
```

### 第 2 步：安装依赖

运行以下命令安装示例应用所需的依赖包（包括 `mysql2` 和 `dotenv`）：

```shell
bundle install
```

<details>
<summary><b>为已有项目安装依赖</b></summary>

对于你的已有项目，运行以下命令安装依赖包：

```shell
bundle add mysql2 dotenv
```

</details>

### 第 3 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connect With** 下拉列表选择 `Rails`，**Connection Type** 保持默认的 `Public`。

4. 如果你还未设置密码，点击 **Generate Password** 生成随机密码。

5. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下格式设置 `DATABASE_URL` 环境变量，并将连接对话框中的连接字符串复制为变量值。

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database_name}?ssl_mode=verify_identity'
    ```

   > **Note**
   >
   > 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，使用公共连接地址时，**必须** 通过 `ssl_mode=verify_identity` 参数启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List**，或参考 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置后再首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参考 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下格式设置 `DATABASE_URL` 环境变量，将连接对话框中的连接字符串复制为变量值，并将 `sslca` 参数设置为刚才下载的 CA 证书文件路径：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}?ssl_mode=verify_identity&sslca=/path/to/ca.pem'
    ```

   > **Note**
   >
   > 推荐在使用公共连接地址连接 TiDB Cloud Dedicated 时启用 TLS 连接。
   >
   > 启用 TLS 连接时，请将 `ssl_mode` 参数值设置为 `verify_identity`，`sslca` 参数值设置为从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB 自建集群">

1. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下格式设置 `DATABASE_URL` 环境变量，并将 `{user}`、`{password}`、`{host}`、`{port}`、`{database}` 替换为你自己的 TiDB 连接信息：

    ```dotenv
    DATABASE_URL='mysql2://{user}:{password}@{host}:{port}/{database}'
    ```

   如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 4 步：运行代码并检查结果

1. 创建数据库和数据表：

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2. 初始化示例数据：

    ```shell
    bundle exec rails db:seed
    ```

3. 运行以下命令执行示例代码：

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

如果连接成功，控制台会输出 TiDB 集群的版本信息，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.3)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参考 [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart) 仓库。

### 通过连接参数连接 TiDB

以下 `config/database.yml` 文件中的代码，通过环境变量配置参数，建立与 TiDB 的连接：

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
> 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，使用公共连接地址时，**必须** 在 `DATABASE_URL` 中通过设置 `ssl_mode=verify_identity` 启用 TLS 连接，但**不需要**通过 `DATABASE_URL` 指定 SSL CA 证书，因为 mysql2 gem 会按特定顺序自动查找本地已存在的 CA 证书文件。

### 插入数据

以下语句创建一个包含两个字段的 Player，并返回新建的 `Player` 对象：

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下语句根据 ID 查询指定玩家的记录：

```ruby
player = Player.find_by(id: new_player.id)
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下语句更新一个 `Player` 对象：

```ruby
player.update(coins: 50, goods: 50)
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下语句删除一个 `Player` 对象：

```ruby
player.destroy
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 最佳实践

默认情况下，ActiveRecord ORM 通过 mysql2 gem 连接 TiDB 时，会按如下顺序查找本地已存在的 CA 证书文件，直到找到为止：

1. /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2. /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3. /etc/ssl/ca-bundle.pem # OpenSUSE
4. /etc/ssl/cert.pem # MacOS / Alpine (docker 容器)

虽然可以手动指定 CA 证书路径，但在多环境部署场景下，不同机器和环境的 CA 证书存放路径可能不同，这种方式会带来较大不便。因此，推荐将 `sslca` 设置为 `nil`，以便在不同环境下灵活部署和使用。

## 后续步骤

- 通过 [ActiveRecord 官方文档](https://guides.rubyonrails.org/active_record_basics.html) 学习更多 ActiveRecord ORM 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>