---
title: 使用 Go-MySQL-Driver 连接 TiDB
summary: 学习如何使用 Go-MySQL-Driver 连接 TiDB。本教程提供了适用于 TiDB 的 Golang 示例代码片段，演示如何通过 Go-MySQL-Driver 进行操作。
---

# 使用 Go-MySQL-Driver 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) 是 [database/sql](https://pkg.go.dev/database/sql) 接口的 MySQL 实现。

在本教程中，你可以学习如何使用 TiDB 和 Go-MySQL-Driver 完成以下任务：

- 搭建你的开发环境。
- 使用 Go-MySQL-Driver 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以参考 [示例代码片段](#sample-code-snippets) 完成基本的 CRUD 操作。

> **Note:**
>
> 本教程适用于 Starter、Essential、TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- [Go](https://go.dev/) **1.20** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart.git
cd tidb-golang-sql-driver-quickstart
```

### 第 2 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="Starter 或 Essential">

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

    Starter 需要安全连接，因此你需要将 `USE_SSL` 设置为 `true`。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参考 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行首次连接前的配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参考 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

    请务必将 `{}` 占位符替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 3 步：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式请参考 [tidb-samples/tidb-golang-sql-driver-quickstart](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart) 仓库。

### 连接 TiDB

```golang
func openDB(driverName string, runnable func(db *sql.DB)) {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})
    db, err := sql.Open(driverName, dsn)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}
```

使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}` 和 `${tidb_db_name}` 替换为你 TiDB 集群的实际值。Starter 和 Essential 需要安全连接，因此你需要将 `${use_ssl}` 设置为 `true`。

### 插入数据

```golang
openDB("mysql", func(db *sql.DB) {
    insertSQL = "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"
    _, err := db.Exec(insertSQL, "id", 1, 1)

    if err != nil {
        panic(err)
    }
})
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```golang
openDB("mysql", func(db *sql.DB) {
    selectSQL = "SELECT id, coins, goods FROM player WHERE id = ?"
    rows, err := db.Query(selectSQL, "id")
    if err != nil {
        panic(err)
    }

    // This line is extremely important!
    defer rows.Close()

    id, coins, goods := "", 0, 0
    if rows.Next() {
        err = rows.Scan(&id, &coins, &goods)
        if err == nil {
            fmt.Printf("player id: %s, coins: %d, goods: %d\n", id, coins, goods)
        }
    }
})
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```golang
openDB("mysql", func(db *sql.DB) {
    updateSQL = "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
    _, err := db.Exec(updateSQL, 1, -1, "id")

    if err != nil {
        panic(err)
    }
})
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```golang
openDB("mysql", func(db *sql.DB) {
    deleteSQL = "DELETE FROM player WHERE id=?"
    _, err := db.Exec(deleteSQL, "id")

    if err != nil {
        panic(err)
    }
})
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 使用驱动还是 ORM 框架？

Golang 驱动提供了对数据库的底层访问，但这要求开发者：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行映射为数据对象。

除非你需要编写复杂的 SQL 语句，否则推荐使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架进行开发，例如 [GORM](/develop/dev-guide-sample-application-golang-gorm.md)。它可以帮助你：

- 减少管理连接和事务的 [样板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 通过数据对象操作数据，而不是大量 SQL 语句。

## 后续步骤

- 通过 [Go-MySQL-Driver 的文档](https://github.com/go-sql-driver/mysql/blob/master/README.md) 学习更多 Go-MySQL-Driver 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>