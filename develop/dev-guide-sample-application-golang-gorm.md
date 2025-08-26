---
title: 使用 GORM 连接 TiDB
summary: 学习如何使用 GORM 连接 TiDB。本教程提供了可与 TiDB 搭配使用的 Golang 示例代码片段。
---

# 使用 GORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[GORM](https://gorm.io/index.html) 是 Golang 领域流行的开源 ORM 框架。GORM 适配了 TiDB 的特性，如 `AUTO_RANDOM`，并且[默认支持 TiDB 作为数据库选项](https://gorm.io/docs/connecting_to_the_database.html#TiDB)。

在本教程中，你可以学习如何使用 TiDB 和 GORM 完成以下任务：

- 搭建你的开发环境。
- 使用 GORM 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以在 [示例代码片段](#sample-code-snippets) 中找到基本 CRUD 操作的示例代码。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- [Go](https://go.dev/) **1.20** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或[部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或[部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-golang-gorm-quickstart.git
cd tidb-golang-gorm-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致

    > **Tip:**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    > 
    > 如果你之前已经创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数。

    {{{ .starter }}} 需要安全连接，因此你需要将 `USE_SSL` 设置为 `true`。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 完成首次连接前的配置。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数。

6. 保存 `.env` 文件。

</div>
<div label="TiDB 自建集群">

1. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    请务必将 `{}` 占位符替换为实际的连接参数，并将 `USE_SSL` 设置为 `false`。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参考 [tidb-samples/tidb-golang-gorm-quickstart](https://github.com/tidb-samples/tidb-golang-gorm-quickstart) 仓库。

### 连接 TiDB

```golang
func createDB() *gorm.DB {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})

    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}
```

使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}` 和 `${tidb_db_name}` 替换为你 TiDB 集群的实际值。{{{ .starter }}} 需要安全连接，因此你需要将 `${use_ssl}` 设置为 `true`。

### 插入数据

```golang
db.Create(&Player{ID: "id", Coins: 1, Goods: 1})
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```golang
var queryPlayer Player
db.Find(&queryPlayer, "id = ?", "id")
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```golang
db.Save(&Player{ID: "id", Coins: 100, Goods: 1})
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```golang
db.Delete(&Player{ID: "id"})
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 通过 [GORM 官方文档](https://gorm.io/docs/index.html) 以及 [GORM 文档中的 TiDB 章节](https://gorm.io/docs/connecting_to_the_database.html#TiDB) 学习更多 GORM 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>