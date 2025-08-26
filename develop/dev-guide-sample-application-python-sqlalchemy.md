---
title: 使用 SQLAlchemy 连接 TiDB
summary: 学习如何使用 SQLAlchemy 连接 TiDB。本教程提供了可与 TiDB 搭配使用的 Python 示例代码片段。
---

# 使用 SQLAlchemy 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[SQLAlchemy](https://www.sqlalchemy.org/) 是一个流行的 Python SQL 工具包和对象关系映射（ORM）库。

在本教程中，你可以学习如何使用 TiDB 和 SQLAlchemy 完成以下任务：

- 搭建你的开发环境。
- 使用 SQLAlchemy 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以参考基本 CRUD 操作的示例代码片段。

> **Note:**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前置条件

完成本教程，你需要：

- [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 运行示例应用并连接 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令，克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart.git
cd tidb-python-sqlalchemy-quickstart
```

### 步骤 2：安装依赖

运行以下命令，为示例应用安装所需的依赖包（包括 SQLAlchemy 和 PyMySQL）：

```shell
pip install -r requirements.txt
```

#### 为什么使用 PyMySQL？

SQLAlchemy 是一个支持多种数据库的 ORM 库。它为数据库提供了高级抽象，帮助开发者以更面向对象的方式编写 SQL 语句。但 SQLAlchemy 并不自带数据库驱动。要连接数据库，你需要安装相应的数据库驱动。本示例应用使用 PyMySQL 作为数据库驱动，它是一个纯 Python 的 MySQL 客户端库，兼容 TiDB，并可在所有平台上安装。

你也可以使用其他数据库驱动，如 [mysqlclient](https://github.com/PyMySQL/mysqlclient) 和 [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)。但它们不是纯 Python 库，需要相应的 C/C++ 编译器和 MySQL 客户端进行编译。更多信息请参考 [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/en/20/core/engines.html#mysql)。

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

> **Note:**
>
> 目前，{{{ .starter }}} 集群有一个限制：如果 5 分钟内没有活跃连接，集群会自动关闭，所有连接会被断开。因此，当你在 {{{ .starter }}} 集群上使用 SQLAlchemy 时，连接池可能会遇到 `OperationalError`，如 `Lost connection to MySQL server during query` 或 `MySQL Connection not available`。为避免此类错误，你可以将 `pool_recycle` 参数设置为 `300`。更多信息请参见 SQLAlchemy 文档中的 [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects)。

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页面。

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
    > 如果你之前已创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

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
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或参照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行首次连接前的配置。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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
    CA_PATH='{your-downloaded-ca-path}'
    ```

    请务必将 `{}` 占位符替换为连接对话框中获取的连接参数，并将 `CA_PATH` 配置为上一步下载的证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

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

### 步骤 4：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    python sqlalchemy_example.py
    ```

2. 检查 [Expected-Output.txt](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart/blob/main/Expected-Output.txt) 文件，确认输出是否一致。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参见 [tidb-samples/tidb-python-sqlalchemy-quickstart](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart) 仓库。

### 连接 TiDB

```python
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

def get_db_engine():
    connect_args = {}
    if ${ca_path}:
        connect_args = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=${tidb_user},
            password=${tidb_password},
            host=${tidb_host},
            port=${tidb_port},
            database=${tidb_db_name},
        ),
        connect_args=connect_args,
    )

engine = get_db_engine()
Session = sessionmaker(bind=engine)
```

使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为你 TiDB 集群的实际值。

### 定义数据表

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Player(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    coins = Column(Integer)
    goods = Column(Integer)

    __tablename__ = "players"
```

更多信息请参考 [SQLAlchemy 文档：Mapping classes with declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)。

### 插入数据

```python
with Session() as session:
    player = Player(name="test", coins=100, goods=100)
    session.add(player)
    session.commit()
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    print(player)
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    player.coins = 200
    session.commit()
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    session.delete(player)
    session.commit()
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 通过 [SQLAlchemy 官方文档](https://www.sqlalchemy.org/) 学习更多 SQLAlchemy 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
