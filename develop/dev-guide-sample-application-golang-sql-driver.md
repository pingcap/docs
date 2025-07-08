---
title: 使用 Go-MySQL-Driver 连接 TiDB
summary: 学习如何使用 Go-MySQL-Driver 连接 TiDB。本教程提供了适用于 TiDB 的 Golang 示例代码片段，使用 Go-MySQL-Driver。
---

# 使用 Go-MySQL-Driver 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) 是一个实现了 [database/sql](https://pkg.go.dev/database/sql) 接口的 MySQL 驱动。

在本教程中，你可以学习如何使用 TiDB 和 Go-MySQL-Driver 完成以下任务：

- 设置你的环境。
- 使用 Go-MySQL-Driver 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你可以查阅 [示例代码片段](#sample-code-snippets) 以了解基本的 CRUD 操作。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB 自托管版本。

## 前提条件

完成本教程，你需要：

- [Go](https://go.dev/) **1.20** 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart.git
cd tidb-golang-sql-driver-quickstart
```

### 步骤 2：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    > 
    > 如果之前已创建密码，可以使用原密码，或点击 **Reset Password** 生成新密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 复制粘贴对应的连接字符串到 `.env` 文件中。示例内容如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数。

    {{{ .starter }}} 需要安全连接，因此需要将 `USE_SSL` 设置为 `true`。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果尚未配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后进行首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 复制粘贴对应的连接字符串到 `.env` 文件中。示例内容如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 复制粘贴对应的连接字符串到 `.env` 文件中。示例内容如下：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    一定要将 `{}` 占位符替换为连接参数，并将 `USE_SSL` 设置为 `false`。如果在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 3：运行代码并查看结果

1. 执行以下命令运行示例代码：

    ```shell
    make
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart/blob/main/Expected-Output.txt)，确认输出是否匹配。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法，请查阅 [tidb-samples/tidb-golang-sql-driver-quickstart](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart) 仓库。

### 连接到 TiDB

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

使用此函数时，需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}` 和 `${tidb_db_name}` 替换为你的 TiDB 集群的实际值。 {{{ .starter }}} 需要安全连接，因此需要将 `${use_ssl}` 设置为 `true`。

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

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

```golang
openDB("mysql", func(db *sql.DB) {
    selectSQL = "SELECT id, coins, goods FROM player WHERE id = ?"
    rows, err := db.Query(selectSQL, "id")
    if err != nil {
        panic(err)
    }

    // 这行非常重要！
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

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

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

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

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

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 常用注意事项

### 使用驱动或 ORM 框架？

Golang 驱动提供了对数据库的底层访问，但需要开发者：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行映射到数据对象。

除非你需要编写复杂的 SQL 语句，否则建议使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架进行开发，例如 [GORM](/develop/dev-guide-sample-application-golang-gorm.md)。它可以帮助你：

- 减少管理连接和事务的 [样板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 使用数据对象操作数据，而不是大量 SQL 语句。

## 后续步骤

- 通过 [Go-MySQL-Driver 的文档](https://github.com/go-sql-driver/mysql/blob/master/README.md) 学习更多用法。
- 参考 [开发者指南](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>