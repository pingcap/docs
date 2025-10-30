---
title: 集成 TiDB 向量检索与 Jina AI Embeddings API
summary: 学习如何将 TiDB 向量检索与 Jina AI Embeddings API 集成，实现向量存储与语义检索。
---

# 集成 TiDB 向量检索与 Jina AI Embeddings API

本教程将指导你如何使用 [Jina AI](https://jina.ai/) 为文本数据生成向量，并将这些向量存储到 TiDB 向量存储中，基于向量实现相似文本的检索。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量检索功能目前为实验性特性。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量检索功能目前为 Beta 版本，可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量检索功能适用于 TiDB Self-Managed、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 前置条件

完成本教程，你需要：

- 已安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 已安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。
- 参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建 v8.4.0 或更高版本的本地集群。

</CustomContent>

## 运行示例应用

你可以按照以下步骤，快速了解如何将 TiDB 向量检索与 JinaAI Embedding 集成。

### 步骤 1. 克隆代码仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为你的项目创建一个虚拟环境：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装依赖

为示例项目安装所需依赖：

```bash
pip install -r requirements.txt
```

### 步骤 4. 配置环境变量

从 [Jina AI Embeddings API](https://jina.ai/embeddings/) 页面获取 Jina AI API key，然后根据你选择的 TiDB 部署方式配置环境变量。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 集群，按如下步骤获取集群连接串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `SQLAlchemy`
    - **Operating System** 与你的环境一致

    > **Tip:**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 切换到 **PyMySQL** 标签页，点击 **Copy** 图标复制连接串。

    > **Tip:**
    >
    > 如果你还未设置密码，请点击 **Create password** 生成随机密码。

5. 在终端中将 Jina AI API key 和 TiDB 连接串设置为环境变量，或创建一个 `.env` 文件，内容如下：

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```

    以下是 macOS 下的连接串示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB Self-Managed">

对于 TiDB Self-Managed 集群，在终端中设置连接 TiDB 集群的环境变量：

```shell
export JINA_API_KEY="****"
export TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：export TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

你需要根据自己的 TiDB 集群替换上述命令中的参数。如果你在本地运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初始 `<PASSWORD>` 为空，如果是首次启动集群，可以省略该字段。

各参数说明如下：

- `<USERNAME>`：连接 TiDB 集群的用户名
- `<PASSWORD>`：连接 TiDB 集群的密码
- `<HOST>`：TiDB 集群的主机地址
- `<PORT>`：TiDB 集群的端口
- `<DATABASE>`：你要连接的数据库名称

</div>

</SimpleTab>

### 步骤 5. 运行示例

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

### 从 Jina AI 获取向量

定义 `generate_embeddings` 辅助函数，调用 Jina AI embeddings API：

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
        'model': 'jina-embeddings-v2-base-en'  # with dimension 768.
    }
    response = requests.post(JINAAI_API_URL, headers=JINAAI_HEADERS, json=JINAAI_REQUEST_DATA)
    return response.json()['data'][0]['embedding']
```

### 连接 TiDB 集群

通过 SQLAlchemy 连接 TiDB 集群：

```python
import os
import dotenv

from tidb_vector.sqlalchemy import VectorType
from sqlalchemy.orm import Session, declarative_base

dotenv.load_dotenv()

TIDB_DATABASE_URL = os.getenv('TIDB_DATABASE_URL')
assert TIDB_DATABASE_URL is not None
engine = create_engine(url=TIDB_DATABASE_URL, pool_recycle=300)
```

### 定义向量表结构

创建名为 `jinaai_tidb_demo_documents` 的表，包含用于存储文本的 `content` 字段和用于存储向量的 `content_vec` 字段：

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS is determined by the embedding model,
        # for Jina AI's jina-embeddings-v2-base-en model it's 768.
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
```

> **Note:**
>
> - 向量字段的维度必须与嵌入模型生成的向量维度一致。
> - 本示例中，`jina-embeddings-v2-base-en` 模型生成的向量维度为 `768`。

### 使用 Jina AI 生成向量并存储到 TiDB

使用 Jina AI Embeddings API 为每条文本生成向量，并将其存储到 TiDB：

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # Generate embeddings for the texts via Jina AI API.
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

### 在 TiDB 中基于 Jina AI 向量进行语义检索

通过 Jina AI embeddings API 为查询文本生成向量，然后基于 **查询文本的向量** 与 **向量表中每条数据的向量** 的余弦距离，检索最相关的文档：

```python
query = 'What is TiDB?'
# Generate the embedding for the query via Jina AI API.
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

## 相关阅读

- [向量数据类型](/vector-search/vector-search-data-types.md)
- [向量检索索引](/vector-search/vector-search-index.md)
