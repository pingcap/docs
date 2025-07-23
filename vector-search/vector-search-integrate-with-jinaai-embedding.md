---
title: 将 TiDB Vector Search 与 Jina AI Embeddings API 集成
summary: 学习如何将 TiDB Vector Search 与 Jina AI Embeddings API 集成，用于存储嵌入向量和执行语义搜索。
---

# 将 TiDB Vector Search 与 Jina AI Embeddings API 集成

本教程将引导你如何使用 [Jina AI](https://jina.ai/) 生成文本数据的嵌入向量，然后将这些嵌入存储在 TiDB 向量存储中，并基于嵌入向量进行相似文本搜索。

<CustomContent platform="tidb">

> **Warning:**
>
> 该向量搜索功能处于实验阶段。不建议在生产环境中使用。此功能可能在未提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该向量搜索功能处于 beta 阶段，可能会在未提前通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 该向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## 前提条件

完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)
- 安装 [Git](https://git-scm.com/downloads)
- 拥有一个 TiDB 集群

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

你可以通过以下步骤快速了解如何将 TiDB Vector Search 与 JinaAI Embedding 集成。

### 第一步：克隆仓库

将 `tidb-vector-python` 仓库克隆到你的本地机器：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第二步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 第三步：安装依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

### 第四步：配置环境变量

从 [Jina AI Embeddings API](https://jina.ai/embeddings/) 页面获取你的 API 密钥，然后根据你选择的 TiDB 部署方式配置环境变量。

<SimpleTab>
<div label="{{{ .starter }}}">

对于 {{{ .starter }}} 集群，按照以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群的名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与您的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `SQLAlchemy`
    - **Operating System** 与你的环境匹配。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到对应的 Linux 发行版。

4. 切换到 **PyMySQL** 标签页，点击 **Copy** 图标复制连接字符串。

    > **Tip:**
    >
    > 如果还未设置密码，可以点击 **Create password** 生成一个随机密码。

5. 在终端中将 Jina AI API 密钥和 TiDB 连接字符串设置为环境变量，或创建 `.env` 文件，内容如下：

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```

    下面是 macOS 的示例连接字符串：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed">

对于 TiDB Self-Managed 集群，在你的终端中设置连接到 TiDB 集群的环境变量如下：

```shell
export JINA_API_KEY="****"
export TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：export TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

你需要根据你的 TiDB 集群参数替换上述命令中的内容。如果你在本地运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初次启动集群时，`<PASSWORD>` 为空，可以省略。

以下是各参数的说明：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机地址。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：你要连接的数据库名称。

</div>

</SimpleTab>

### 第五步：运行示例

```bash
python jina-ai-embeddings-demo.py
```

示例输出：

```text
- Inserting Data to TiDB...
  - Inserting: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - Inserting: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- List All Documents and Their Distances to the Query:
  - distance: 0.3585317326132522
    content: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- The Most Relevant Document and Its Distance to the Query:
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
```

## 示例代码片段

### 获取 Jina AI 的嵌入向量

定义一个 `generate_embeddings` 辅助函数，用于调用 Jina AI 嵌入 API：

```python
import os
import requests
import dotenv

dotenv.load_dotenv()

JINAAI_API_KEY = os.getenv('JINAAI_API_KEY')

def generate_embeddings(text: str):
    JINAAI_API_URL = 'https://api.jina.ai/v1/embeddings'
    JINAAI_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINAAI_API_KEY}'
    }
    JINAAI_REQUEST_DATA = {
        'input': [text],
        'model': 'jina-embeddings-v2-base-en'  # 嵌入向量维度为 768。
    }
    response = requests.post(JINAAI_API_URL, headers=JINAAI_HEADERS, json=JINAAI_REQUEST_DATA)
    return response.json()['data'][0]['embedding']
```

### 连接到 TiDB 集群

通过 SQLAlchemy 连接到 TiDB 集群：

```python
import os
import dotenv

from tidb_vector.sqlalchemy import VectorType
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

dotenv.load_dotenv()

TIDB_DATABASE_URL = os.getenv('TIDB_DATABASE_URL')
assert TIDB_DATABASE_URL is not None
engine = create_engine(url=TIDB_DATABASE_URL, pool_recycle=300)
```

### 定义向量表结构

创建一个名为 `jinaai_tidb_demo_documents` 的表，包含存储文本的 `content` 列和存储嵌入向量的 `content_vec` 列：

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS 由嵌入模型决定，
        # 对于 Jina AI 的 jina-embeddings-v2-base-en 模型为 768。
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
    )
```

> **Note:**
>
> - 向量列的维度必须与嵌入模型生成的嵌入向量维度一致。
> - 在此示例中，`jina-embeddings-v2-base-en` 模型生成的嵌入向量维度为 `768`。

### 使用 Jina AI 生成嵌入向量并存入 TiDB

利用 Jina AI Embeddings API 为每段文本生成嵌入向量，并存入 TiDB：

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # 通过 Jina AI API 生成文本的嵌入向量。
    embedding = generate_embeddings(text)
    data.append({
        'text': text,
        'embedding': embedding
    })

with Session(engine) as session:
    print('- Inserting Data to TiDB...')
    for item in data:
        print(f'  - Inserting: {item["text"]}')
        session.add(Document(
            content=item['text'],
            content_vec=item['embedding']
        ))
    session.commit()
```

### 在 TiDB 中使用 Jina AI 嵌入向量进行语义搜索

通过 Jina AI 嵌入 API 生成查询文本的嵌入向量，然后根据**查询文本的嵌入向量**与**向量表中的每个嵌入向量**的余弦距离，搜索最相关的文档：

```python
query = 'What is TiDB?'
# 通过 Jina AI API 生成查询的嵌入向量。
query_embedding = generate_embeddings(query)

with Session(engine) as session:
    print('- The Most Relevant Document and Its Distance to the Query:')
    doc, distance = session.query(
        Document,
        Document.content_vec.cosine_distance(query_embedding).label('distance')
    ).order_by(
        'distance'
    ).limit(1).first()
    print(f'  - distance: {distance}\n'
          f'    content: {doc.content}')
```

## 相关链接

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)