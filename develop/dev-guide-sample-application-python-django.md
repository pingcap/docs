---
title: 使用 Django 连接 TiDB
summary: 学习如何使用 Django 连接 TiDB。本教程提供了可与 TiDB 搭配使用的 Python 示例代码片段。
---

# 使用 Django 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[Django](https://www.djangoproject.com) 是一个流行的 Python Web 框架，内置了强大的对象关系映射（ORM）库。

在本教程中，你可以学习如何使用 TiDB 和 Django 完成以下任务：

- 搭建你的开发环境。
- 使用 Django 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你还可以找到基本 CRUD 操作的示例代码片段。

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
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用所需的依赖包（包括 Django、django-tidb 和 mysqlclient）：

```shell
pip install -r requirements.txt
```

如果你在安装 mysqlclient 时遇到问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。

#### 什么是 `django-tidb`？

`django-tidb` 是 Django 的 TiDB 方言，用于解决 TiDB 与 Django 之间的兼容性问题。

安装 `django-tidb` 时，请选择与你的 Django 版本相匹配的版本。例如，如果你使用的是 `django==4.2.*`，则安装 `django-tidb==4.2.*`。小版本号无需完全一致，建议使用最新的小版本。

更多信息请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 步骤 3：配置连接信息

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

    {{{ .starter }}} 需要安全连接。由于 mysqlclient 的 `ssl_mode` 默认是 `PREFERRED`，你无需手动指定 `CA_PATH`，只需留空即可。但如果你有特殊需求需要手动指定 `CA_PATH`，可参考 [TLS 连接到 {{{ .starter }}}](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) 获取不同操作系统的证书路径。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，请点击 **Configure IP Access List**，或按照 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，以便首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

### 步骤 4：初始化数据库

在项目根目录下运行以下命令，初始化数据库：

```shell
python manage.py migrate
```

### 步骤 5：运行示例应用

1. 以开发模式运行应用：

    ```shell
    python manage.py runserver
    ```

    应用默认运行在端口 `8000`。如需使用其他端口，可在命令后追加端口号。例如：

    ```shell
    python manage.py runserver 8080
    ```

2. 访问应用，在浏览器中打开 `http://localhost:8000/`。在示例应用中，你可以：

    - 创建新玩家
    - 批量创建玩家
    - 查看所有玩家
    - 更新玩家信息
    - 删除玩家
    - 在两个玩家之间交易物品

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

完整示例代码及运行方法请参见 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart) 仓库。

### 连接 TiDB

在 `sample_project/settings.py` 文件中，添加如下配置：

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
# insert a single object
player = Player.objects.create(name="player1", coins=100, goods=1)

# bulk insert multiple objects
Player.objects.bulk_create([
    Player(name="player1", coins=100, goods=1),
    Player(name="player2", coins=200, goods=2),
    Player(name="player3", coins=300, goods=3),
])
```

更多信息请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
# get a single object
player = Player.objects.get(name="player1")

# get multiple objects
filtered_players = Player.objects.filter(name="player1")

# get all objects
all_players = Player.objects.all()
```

更多信息请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
# update a single object
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# update multiple objects
Player.objects.filter(coins=100).update(coins=200)
```

更多信息请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
# delete a single object
player = Player.objects.get(name="player1")
player.delete()

# delete multiple objects
Player.objects.filter(coins=100).delete()
```

更多信息请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 后续步骤

- 通过 [Django 官方文档](https://www.djangoproject.com/) 学习更多 Django 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
