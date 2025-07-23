---
title: 将 TiDB Vector Search 与 peewee 集成
summary: 学习如何将 TiDB Vector Search 与 peewee 集成，用于存储嵌入向量和执行语义搜索。
---

# 将 TiDB Vector Search 与 peewee 集成

本教程将引导你如何使用 [peewee](https://docs.peewee-orm.com/) 与 [TiDB Vector Search](/vector-search/vector-search-overview.md) 交互，存储嵌入向量，并执行向量搜索查询。

<CustomContent platform="tidb">

> **Warning:**
>
> 该向量搜索功能处于实验阶段。不建议在生产环境中使用。此功能可能在未提前通知的情况下进行更改。如果你发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该向量搜索功能处于测试版，可能会在未提前通知的情况下进行更改。如果你发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 该向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## 前提条件

完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)
- 安装 [Git](https://git-scm.com/downloads)
- 一个 TiDB 集群

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。
- 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建版本为 v8.4.0 或更高版本的本地集群。

</CustomContent>

## 运行示例应用

你可以通过以下步骤快速了解如何将 TiDB Vector Search 与 peewee 集成。

### 第 1 步：克隆仓库

将 [`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python) 仓库克隆到你的本地机器：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

或者，你也可以单独安装以下包：

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### 第 4 步：配置环境变量

根据你选择的 TiDB 部署方式，配置环境变量。

<SimpleTab>
<div label="{{{ .starter }}}">

对于 {{{ .starter }}} 集群，按照以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `General`。
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，切换到对应的 Linux 发行版。

4. 从连接对话框复制连接参数。

    > **Tip:**
    >
    > 如果还未设置密码，可以点击 **Generate Password** 生成随机密码。

5. 在你的 Python 项目的根目录下，创建 `.env` 文件，并将连接参数粘贴到对应的环境变量中。

    - `TIDB_HOST`: TiDB 集群的主机地址。
    - `TIDB_PORT`: TiDB 集群的端口。
    - `TIDB_USERNAME`: 连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`: 连接 TiDB 集群的密码。
    - `TIDB_DATABASE`: 要连接的数据库名。
    - `TIDB_CA_PATH`: 根证书文件的路径。

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

对于 TiDB Self-Managed 集群，在你的 Python 项目的根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量的值：

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

如果你在本地运行 TiDB，`TIDB_HOST` 默认为 `127.0.0.1`。初次启动集群时，`TIDB_PASSWORD` 默认为空，可以省略此字段。

以下是各参数的说明：

- `TIDB_HOST`: TiDB 集群的主机地址。
- `TIDB_PORT`: TiDB 集群的端口。
- `TIDB_USERNAME`: 连接 TiDB 集群的用户名。
- `TIDB_PASSWORD`: 连接 TiDB 集群的密码。
- `TIDB_DATABASE`: 你要连接的数据库名称。

</div>

</SimpleTab>

### 第 5 步：运行示例

```bash
python peewee-quickstart.py
```

示例输出：

```text
Get 3-nearest neighbor documents:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
  - distance: 0.7327387580875756
    document: tree
Get documents within a certain distance:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
```

## 示例代码片段

你可以参考以下示例代码片段，开发你的应用。

### 创建向量表

#### 连接到 TiDB 集群

```python
import os
import dotenv

from peewee import Model, MySQLDatabase, SQL, TextField
from tidb_vector.peewee import VectorField

dotenv.load_dotenv()

# 使用 `pymysql` 作为驱动
connect_kwargs = {
    'ssl_verify_cert': True,
    'ssl_verify_identity': True,
}

# 使用 `mysqlclient` 作为驱动
# connect_kwargs = {
#     'ssl_mode': 'VERIFY_IDENTITY',
#     'ssl': {
#         # 根证书默认路径
#         # https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/#root-certificate-default-path
#         'ca': os.environ.get('TIDB_CA_PATH', '/path/to/ca.pem'),
#     },
# }

db = MySQLDatabase(
    database=os.environ.get('TIDB_DATABASE', 'test'),
    user=os.environ.get('TIDB_USERNAME', 'root'),
    password=os.environ.get('TIDB_PASSWORD', ''),
    host=os.environ.get('TIDB_HOST', 'localhost'),
    port=int(os.environ.get('TIDB_PORT', '4000')),
    **connect_kwargs,
)
```

#### 定义向量列

创建一个名为 `peewee_demo_documents` 的表，包含存储 3 维向量的列。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### 存储带有嵌入向量的文档

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 搜索语义最接近的邻居文档

根据余弦距离函数，搜索与查询向量 `[1, 2, 3]` 语义最接近的前 3 个文档。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 搜索距离在一定范围内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 相关链接

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
