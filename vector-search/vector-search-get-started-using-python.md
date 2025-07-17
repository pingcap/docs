---
title: 使用 Python 搭配 TiDB + AI 入门
summary: 学习如何使用 Python 和 TiDB Vector Search 快速开发一个执行语义搜索的 AI 应用。
---

# 使用 Python 搭配 TiDB + AI 入门

本教程演示如何开发一个提供 **semantic search** 功能的简单 AI 应用。与传统的关键词搜索不同，语义搜索能够智能理解你的查询背后的含义，并返回最相关的结果。例如，如果你有标题为 "dog"、"fish" 和 "tree" 的文档，当你搜索 "一只会游泳的动物" 时，应用会识别出 "fish" 是最相关的结果。

在整个教程中，你将使用 [TiDB Vector Search](/vector-search/vector-search-overview.md)、Python、[TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python) 和 AI 模型来开发此应用。

<CustomContent platform="tidb">

> **Warning:**
>
> 目前向量搜索功能处于实验阶段，不建议在生产环境中使用。此功能可能会在不提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 目前向量搜索功能处于测试版，可能会在不提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（建议使用 v8.5.0 及以上版本）。

## 前提条件

完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)
- 安装 [Git](https://git-scm.com/downloads)
- 拥有一个 TiDB 集群

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- 参考 [部署本地测试用 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产用 TiDB 集群](/production-deployment-using-tiup.md) 来创建本地集群。
- 参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试用 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产用 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建版本为 v8.4.0 或更高版本的本地集群。

</CustomContent>

## 入门步骤

以下步骤演示如何从零开始开发应用。若想直接运行示例，可以在 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) 仓库中查看示例代码。

### 步骤 1. 创建一个新的 Python 项目

在你偏好的目录下，创建一个新的 Python 项目和一个名为 `example.py` 的文件：

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### 步骤 2. 安装所需依赖

在你的项目目录下，运行以下命令安装所需的包：

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`：用于与 TiDB 向量搜索交互的 Python 客户端。
- [`sentence-transformers`](https://sbert.net)：提供预训练模型，用于从文本生成 [vector embeddings](/vector-search/vector-search-overview.md#vector-embedding)。

### 步骤 3. 配置连接字符串到 TiDB 集群

根据你选择的 TiDB 部署方式，配置集群连接字符串。

<SimpleTab>
<div label="{{{ .starter }}}">

对于 {{{ .starter }}} 集群，按照以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设为 `Public`。
    - **Branch** 设为 `main`。
    - **Connect With** 设为 `SQLAlchemy`。
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，切换到对应的 Linux 发行版。

4. 点击 **PyMySQL** 标签页，复制连接字符串。

    > **Tip:**
    >
    > 如果还未设置密码，可以点击 **Generate Password** 生成随机密码。

5. 在你的 Python 项目的根目录下，创建 `.env` 文件，并将连接字符串粘贴进去。

    下面是 macOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed">

对于 TiDB Self-Managed 集群，在你的 Python 项目根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量值：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

如果你在本地运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初次启动集群时，`<PASSWORD>` 为空，可以省略此字段。

以下是各参数的说明：

- `<USER>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机地址。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：你要连接的数据库名。

</div>

</SimpleTab>

### 步骤 4. 初始化嵌入模型

[embedding model](/vector-search/vector-search-overview.md#embedding-model) 将数据转换为 [vector embeddings](/vector-search/vector-search-overview.md#vector-embedding)。本示例使用预训练模型 [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) 进行文本嵌入。该轻量级模型由 `sentence-transformers` 库提供，将文本数据转换为 384 维的向量嵌入。

将以下代码复制到 `example.py` 文件中，用于初始化 `SentenceTransformer` 实例，并定义一个 `text_to_embedding()` 函数供后续使用。

```python
from sentence_transformers import SentenceTransformer

print("Downloading and loading the embedding model...")
embed_model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L12-cos-v5", trust_remote_code=True)
embed_model_dims = embed_model.get_sentence_embedding_dimension()

def text_to_embedding(text):
    """为给定文本生成向量嵌入。"""
    embedding = embed_model.encode(text)
    return embedding.tolist()
```

### 步骤 5. 连接到 TiDB 集群

使用 `TiDBVectorClient` 类连接到你的 TiDB 集群，并创建一个名为 `embedded_documents` 的表，包含一个向量列。

> **Note**
>
> 确保表中的向量列维度与嵌入模型生成的向量维度一致。例如，`msmarco-MiniLM-L12-cos-v5` 模型生成的向量维度为 384，因此 `embedded_documents` 表中的向量列维度也应为 384。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# 从 .env 文件加载连接字符串
load_dotenv()

vector_store = TiDBVectorClient(
   # `embedded_documents` 表将存储向量数据。
   table_name='embedded_documents',
   # 连接 TiDB 集群的连接字符串。
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # 嵌入模型生成的向量维度。
   vector_dimension=embed_model_dims,
   # 如果表已存在，则重新创建。
   drop_existing_table=True,
)
```

### 步骤 6. 嵌入文本数据并存储向量

在此步骤中，你将准备包含单词的示例文档，例如 "dog"、"fish" 和 "tree"。以下代码使用 `text_to_embedding()` 函数将这些文本转换为向量嵌入，然后插入到向量存储中。

```python
documents = [
    {
        "id": "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
        "text": "dog",
        "embedding": text_to_embedding("dog"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
        "text": "fish",
        "embedding": text_to_embedding("fish"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "e4991349-d00b-485c-a481-f61695f2b5ae",
        "text": "tree",
        "embedding": text_to_embedding("tree"),
        "metadata": {"category": "plant"},
    },
]

vector_store.insert(
    ids=[doc["id"] for doc in documents],
    texts=[doc["text"] for doc in documents],
    embeddings=[doc["embedding"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
)
```

### 步骤 7. 执行语义搜索

在此步骤中，你将搜索 "一只会游泳的动物"，该词组与现有文档中的词没有直接匹配。

以下代码再次使用 `text_to_embedding()` 函数，将查询文本转换为向量嵌入，然后用该嵌入进行查询，找到最接近的前三个匹配。

```python
def print_result(query, result):
   print(f"Search result (\"{query}\"):")
   for r in result:
      print(f"- text: \"{r.document}\", distance: {r.distance}")

query = "一只会游泳的动物"
query_embedding = text_to_embedding(query)
search_result = vector_store.query(query_embedding, k=3)
print_result(query, search_result)
```

运行 `example.py` 文件，输出如下：

```plain
Search result ("一只会游泳的动物"):
- text: "fish", distance: 0.4562914811223072
- text: "dog", distance: 0.6469335836410557
- text: "tree", distance: 0.798545178640937
```

搜索结果中的三个词条按照它们与查询向量的距离排序：距离越小，相关性越高。

因此，根据输出，最可能的匹配对象是鱼，或者是擅长游泳的狗。

## 相关链接

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)