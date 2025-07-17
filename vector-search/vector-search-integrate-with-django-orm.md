---
title: 将 TiDB 向量搜索集成到 Django ORM
summary: 学习如何将 TiDB 向量搜索与 Django ORM 集成，用于存储嵌入向量和执行语义搜索。
---

# 将 TiDB 向量搜索集成到 Django ORM

本教程将引导你如何使用 [Django](https://www.djangoproject.com/) ORM 与 [TiDB 向量搜索](/vector-search/vector-search-overview.md) 交互，存储嵌入向量，并执行向量搜索查询。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量搜索功能处于实验阶段。不建议在生产环境中使用此功能。此功能可能在未提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量搜索功能处于 beta 阶段。可能会在未提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## 前提条件

完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)
- 安装 [Git](https://git-scm.com/downloads)
- 一个 TiDB 集群

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下步骤创建：**

- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。
- 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下步骤创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建版本为 v8.4.0 或更高版本的本地集群。

</CustomContent>

## 运行示例应用

你可以通过以下步骤快速了解如何将 TiDB 向量搜索与 Django ORM 集成。

### 步骤 1. 克隆仓库

将 `tidb-vector-python` 仓库克隆到你的本地机器：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

或者，你也可以单独安装以下包：

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

如果在安装 mysqlclient 时遇到问题，请参考 mysqlclient 官方文档。

#### 什么是 `django-tidb`

`django-tidb` 是 Django 的 TiDB 方言，增强了 Django ORM 对 TiDB 的支持（例如，向量搜索），并解决了 TiDB 与 Django 之间的兼容性问题。

要安装 `django-tidb`，请选择与你的 Django 版本匹配的版本。例如，如果你使用 `django==4.2.*`，则安装 `django-tidb==4.2.*`。次版本号不必完全一致，建议使用最新的次版本。

更多信息请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 步骤 4. 配置环境变量

根据你选择的 TiDB 部署方式，配置环境变量。

<SimpleTab>
<div label="{{{ .starter }}}">

对于 {{{ .starter }}} 集群，按照以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与操作环境匹配。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致。

    > **Tip:**
    >
    > 如果你的程序在 Windows 子系统 Linux（WSL）中运行，请切换到对应的 Linux 发行版。

4. 从连接对话框复制连接参数。

    > **Tip:**
    >
    > 如果还未设置密码，可以点击 **Generate Password** 生成随机密码。

5. 在你的 Python 项目的根目录下，创建一个 `.env` 文件，并将连接参数粘贴到对应的环境变量中。

    - `TIDB_HOST`: TiDB 集群的主机地址
    - `TIDB_PORT`: TiDB 集群的端口
    - `TIDB_USERNAME`: 连接 TiDB 集群的用户名
    - `TIDB_PASSWORD`: 连接 TiDB 集群的密码
    - `TIDB_DATABASE`: 要连接的数据库名
    - `TIDB_CA_PATH`: 根证书文件的路径

    下面是 macOS 的示例：

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>
<div label="TiDB Self-Managed">

对于 TiDB Self-Managed 集群，在你的 Python 项目的根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量值：

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

如果你在本地运行 TiDB，`TIDB_HOST` 默认为 `127.0.0.1`。初次启动集群时，`TIDB_PASSWORD` 默认为空，可以省略此字段。

以下是各参数的说明：

- `TIDB_HOST`: TiDB 集群的主机地址
- `TIDB_PORT`: TiDB 集群的端口
- `TIDB_USERNAME`: 连接 TiDB 集群的用户名
- `TIDB_PASSWORD`: 连接 TiDB 集群的密码
- `TIDB_DATABASE`: 你要连接的数据库名称

</div>

</SimpleTab>

### 步骤 5. 运行示例

迁移数据库架构：

```bash
python manage.py migrate
```

启动 Django 开发服务器：

```bash
python manage.py runserver
```

打开浏览器，访问 `http://127.0.0.1:8000`，体验示例应用。以下是可用的 API 路径：

| API 路径                                | 描述                              |
| --------------------------------------- | -------------------------------- |
| `POST: /insert_documents`               | 插入带有嵌入向量的文档。            |
| `GET: /get_nearest_neighbors_documents` | 获取最接近的 3 个邻居文档。        |
| `GET: /get_documents_within_distance`   | 获取在一定距离内的文档。            |

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

### 连接到 TiDB 集群

在 `sample_project/settings.py` 文件中添加以下配置：

```python
dotenv.load_dotenv()

DATABASES = {
    "default": {
        # https://github.com/pingcap/django-tidb
        "ENGINE": "django_tidb",
        "HOST": os.environ.get("TIDB_HOST", "127.0.0.1"),
        "PORT": int(os.environ.get("TIDB_PORT", 4000)),
        "USER": os.environ.get("TIDB_USERNAME", "root"),
        "PASSWORD": os.environ.get("TIDB_PASSWORD", ""),
        "NAME": os.environ.get("TIDB_DATABASE", "test"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH", "")
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

你可以在项目根目录下创建 `.env` 文件，设置环境变量 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD`、`TIDB_DATABASE` 和 `TIDB_CA_PATH`，填入你的 TiDB 集群的实际值。

### 创建向量表

#### 定义向量列

`tidb-django` 提供 `VectorField` 用于存储向量嵌入。

创建一个包含名为 `embedding` 的列的表，用于存储 3 维向量。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### 存储带有嵌入的文档

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 搜索最邻近的文档

TiDB 向量支持以下距离函数：

- `L1Distance`
- `L2Distance`
- `CosineDistance`
- `NegativeInnerProduct`

根据余弦距离函数，搜索与查询向量 `[1, 2, 3]` 语义最接近的前 3 个文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 搜索距离在一定范围内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 另请参阅

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
