---
title: 使用 mysqlclient 连接 TiDB
summary: 学习如何使用 mysqlclient 连接 TiDB。本教程提供了适用于 TiDB 的 Python 代码示例片段。
---

# 使用 mysqlclient 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[mysqlclient](https://github.com/PyMySQL/mysqlclient) 是一个流行的 Python 开源驱动。

在本教程中，你可以学习如何使用 TiDB 和 mysqlclient 完成以下任务：

- 搭建你的环境。
- 使用 mysqlclient 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以找到基本 CRUD 操作的代码示例片段。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 和 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- [Python **3.10** 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 第 1 步：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart.git
cd tidb-python-mysqlclient-quickstart;
```

### 第 2 步：安装依赖

运行以下命令安装示例应用所需的依赖包（包括 `mysqlclient`）：

```shell
pip install -r requirements.txt
```

如果遇到安装问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。

### 第 3 步：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

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
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    请务必将 `{}` 占位符替换为连接对话框中获得的连接参数。

    {{{ .starter }}} 需要安全连接。由于 mysqlclient 的 `ssl_mode` 默认是 `PREFERRED`，你无需手动指定 `CA_PATH`，保持为空即可。但如果你有特殊需求需要手动指定 `CA_PATH`，可参考 [TLS 连接到 {{{ .starter }}}](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) 获取不同操作系统的证书路径。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参考 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置后再首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参考 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获得的连接参数，并将 `CA_PATH` 配置为上一步下载的证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB 自建集群">

1. 运行以下命令，复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 将对应的连接字符串复制粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    请务必将 `{}` 占位符替换为连接参数，并删除 `CA_PATH` 这一行。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 4 步：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    python mysqlclient_example.py
    ```

2. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart/blob/main/Expected-Output.txt) 是否与输出结果一致。

## 代码示例片段

你可以参考以下代码示例片段，完成你自己的应用开发。

完整示例代码及运行方法请参考 [tidb-samples/tidb-python-mysqlclient-quickstart](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart) 仓库。

### 连接 TiDB

```python
def get_mysqlclient_connection(autocommit:bool=True) -> MySQLdb.Connection:
    db_conf = {
        "host": ${tidb_host},
        "port": ${tidb_port},
        "user": ${tidb_user},
        "password": ${tidb_password},
        "database": ${tidb_db_name},
        "autocommit": autocommit
    }

    if ${ca_path}:
        db_conf["ssl_mode"] = "VERIFY_IDENTITY"
        db_conf["ssl"] = {"ca": ${ca_path}}

    return MySQLdb.connect(**db_conf)
```

使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为你 TiDB 集群的实际值。

### 插入数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute(
            "UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s",
            (-amount, price, player_id),
        )
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 使用驱动还是 ORM 框架？

Python 驱动提供了对数据库的底层访问，但这要求开发者：

- 手动建立和释放数据库连接。
- 手动管理数据库事务。
- 手动将数据行（在 `mysqlclient` 中表现为元组）映射为数据对象。

除非你需要编写复杂的 SQL 语句，否则推荐使用 [ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping) 框架进行开发，如 [SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md)、[Peewee](/develop/dev-guide-sample-application-python-peewee.md) 和 Django ORM。它可以帮助你：

- 减少管理连接和事务的 [样板代码](https://en.wikipedia.org/wiki/Boilerplate_code)。
- 通过数据对象操作数据，而不是大量 SQL 语句。

## 后续步骤

- 通过 [mysqlclient 的文档](https://mysqlclient.readthedocs.io/) 学习更多 `mysqlclient` 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
