---
title: 使用 {{{ .starter }}} 连接 WordPress
summary: 学习如何使用 {{{ .starter }}} 运行 WordPress。本教程将为你提供分步指导，仅需几分钟即可运行 WordPress + {{{ .starter }}}。
---

# 使用 {{{ .starter }}} 连接 WordPress

TiDB 是兼容 MySQL 的数据库，{{{ .starter }}} 是完全托管的 TiDB 服务，[WordPress](https://github.com/WordPress) 是一个免费的开源内容管理系统（CMS），允许用户创建和管理网站。WordPress 由 PHP 编写，并使用 MySQL 数据库。

在本教程中，你可以学习如何使用 {{{ .starter }}} 免费运行 WordPress。

> **Note:**
>
> 除了 {{{ .starter }}}，本教程同样适用于 {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。但强烈推荐使用 {{{ .starter }}} 运行 WordPress，以获得更高的性价比。

## 前置条件

完成本教程，你需要：

- 一个 {{{ .starter }}} 集群。如果你还没有，请按照[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)来创建属于你自己的 TiDB Cloud 集群。

## 使用 {{{ .starter }}} 运行 WordPress

本节将演示如何使用 {{{ .starter }}} 运行 WordPress。

### 第 1 步：克隆 WordPress 示例仓库

在你的终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### 第 2 步：安装依赖

1. 示例仓库需要 [Docker](https://www.docker.com/) 和 [Docker Compose](https://docs.docker.com/compose/) 来启动 WordPress。如果你已经安装，可以跳过此步骤。强烈建议在 Linux 环境（如 Ubuntu）下运行 WordPress。运行以下命令安装 Docker 和 Docker Compose：

    ```shell
    sudo sh install.sh
    ```

2. 示例仓库包含 [TiDB Compatibility Plugin](https://github.com/pingcap/wordpress-tidb-plugin) 作为子模块。运行以下命令以更新子模块：

    ```shell
    git submodule update --init --recursive
    ```

### 第 3 步：配置连接信息

将 WordPress 数据库连接配置为 {{{ .starter }}}。

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Connect With** 设置为 `WordPress`。
    - **Operating System** 设置为 `Debian/Ubuntu/Arch`。
    - **Database** 设置为你想要使用的数据库，例如 `test`。

4. 点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以继续使用原有密码，或者点击 **Reset Password** 生成新密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    请务必将 `{}` 占位符替换为你在连接对话框中获得的连接参数。默认情况下，你的 {{{ .starter }}} 自带一个 `test` 数据库。如果你已经在 {{{ .starter }}} 集群中创建了其他数据库，可以将 `test` 替换为你的数据库名。

7. 保存 `.env` 文件。

### 第 4 步：使用 {{{ .starter }}} 启动 WordPress

1. 执行以下命令，将 WordPress 作为 Docker 容器运行：

    ```shell
    docker compose up -d
    ```

2. 通过访问 [localhost](http://localhost/)（如果你在本地机器上启动容器）或 `http://<your_instance_ip>`（如果 WordPress 运行在远程机器上）来设置你的 WordPress 站点。

### 第 5 步：确认数据库连接

1. 在 TiDB Cloud 控制台关闭集群的连接对话框，并打开 **SQL Editor** 页面。
2. 在左侧 **Schemas** 标签下，点击你连接到 WordPress 的数据库。
3. 确认你现在可以在该数据库的表列表中看到 WordPress 的表（如 `wp_posts` 和 `wp_comments`）。

## 需要帮助？

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。