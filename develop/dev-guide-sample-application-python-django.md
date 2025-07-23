---
title: 使用 Django 连接 TiDB
summary: 学习如何使用 Django 连接 TiDB。本教程提供适用于 TiDB 的 Python 示例代码片段，演示如何通过 Django 进行操作。
---

# 使用 Django 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Django](https://www.djangoproject.com) 是一个流行的 Python Web 框架，内置强大的对象关系映射（ORM）库。

在本教程中，你可以学习如何使用 TiDB 和 Django 完成以下任务：

- 设置你的环境。
- 使用 Django 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。可选地，你还可以找到用于基本 CRUD 操作的示例代码片段。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed 集群。

## 前提条件

完成本教程，你需要：

- [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 也可以参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 运行示例应用以连接到 TiDB

本节演示如何运行示例应用代码并连接到 TiDB。

### 步骤 1：克隆示例应用仓库

在终端窗口中运行以下命令以克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 步骤 2：安装依赖

运行以下命令以安装示例应用所需的包（包括 Django、django-tidb 和 mysqlclient）：

```shell
pip install -r requirements.txt
```

如果在安装 mysqlclient 时遇到问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。

#### 什么是 `django-tidb`？

`django-tidb` 是为 Django 提供的 TiDB 方言，用于解决 TiDB 和 Django 之间的兼容性问题。

要安装 `django-tidb`，请选择与你的 Django 版本匹配的版本。例如，如果你使用 `django==4.2.*`，则安装 `django-tidb==4.2.*`。次版本号不需要完全一致，建议使用最新的次版本。

更多信息请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    > 
    > 如果之前已创建密码，可以使用原密码，也可以点击 **Reset Password** 生成新密码。

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
    CA_PATH='{ssl_ca}'  # 例如 /etc/ssl/certs/ca-certificates.crt（Debian / Ubuntu / Arch）
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数。

    {{{ .starter }}} 需要安全连接。由于 mysqlclient 的 `ssl_mode` 默认为 `PREFERRED`，你无需手动指定 `CA_PATH`，只需留空即可。但如果你有特殊原因需要手动指定 `CA_PATH`，可以参考 [TLS connections to {{{ .starter }}}](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)，获取不同操作系统的证书路径。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，可以点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再首次连接。

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
    CA_PATH='{your-downloaded-ca-path}'
    ```

    一定要将 `{}` 占位符替换为从连接对话框获取的连接参数，并将 `CA_PATH` 配置为之前步骤中下载的证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 复制粘贴对应的连接字符串到 `.env` 文件中。示例内容如下：

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    一定要将 `{}` 占位符替换为连接参数，并删除 `CA_PATH` 行。如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：初始化数据库

在项目根目录下，运行以下命令初始化数据库：

```shell
python manage.py migrate
```

### 步骤 5：运行示例应用

1. 以开发模式运行应用：

    ```shell
    python manage.py runserver
    ```

    默认情况下，应用在端口 `8000` 上运行。若要使用其他端口，可以在命令后添加端口号，例如：

    ```shell
    python manage.py runserver 8080
    ```

2. 打开浏览器，访问 `http://localhost:8000/`。在示例应用中，你可以：

    - 创建新玩家。
    - 批量创建玩家。
    - 查看所有玩家。
    - 更新玩家信息。
    - 删除玩家。
    - 进行玩家之间的物品交易。

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方式，请查看 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart) 仓库。

### 连接到 TiDB

在 `sample_project/settings.py` 文件中，添加以下配置：

```python
DATABASES = {
    "default": {
        "ENGINE": "django_tidb",
        "HOST": ${tidb_host},
        "PORT": ${tidb_port},
        "USER": ${tidb_user},
        "PASSWORD": ${tidb_password},
        "NAME": ${tidb_db_name},
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = ${ca_path}
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为你的 TiDB 集群的实际值。

### 定义数据模型

```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

更多信息请参考 [Django models](https://docs.djangoproject.com/en/dev/topics/db/models/)。

### 插入数据

```python
# 插入单个对象
player = Player.objects.create(name="player1", coins=100, goods=1)

# 批量插入多个对象
Player.objects.bulk_create([
    Player(name="player1", coins=100, goods=1),
    Player(name="player2", coins=200, goods=2),
    Player(name="player3", coins=300, goods=3),
])
```

更多信息请参考 [Insert data](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
# 获取单个对象
player = Player.objects.get(name="player1")

# 获取多个对象
filtered_players = Player.objects.filter(name="player1")

# 获取所有对象
all_players = Player.objects.all()
```

更多信息请参考 [Query data](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
# 更新单个对象
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# 更新多个对象
Player.objects.filter(coins=100).update(coins=200)
```

更多信息请参考 [Update data](/develop/dev-guide-update-data.md)。

### 删除数据

```python
# 删除单个对象
player = Player.objects.get(name="player1")
player.delete()

# 删除多个对象
Player.objects.filter(coins=100).delete()
```

更多信息请参考 [Delete data](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 通过 [Django 官方文档](https://www.djangoproject.com/) 学习更多 Django 的用法。
- 通过 [开发者指南](https://github.com/pingcap/tidb-dev-guide) 中的章节，学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Single table reading](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>