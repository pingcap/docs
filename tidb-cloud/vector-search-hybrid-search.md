---
title: Hybrid Search
summary: 使用全文搜索和向量搜索结合，提高检索质量。
aliases: ['/tidb/stable/vector-search-hybrid-search']
---

# Hybrid Search

通过使用全文搜索，你可以基于精确关键词检索文档；通过使用向量搜索，你可以基于语义相似性检索文档。我们是否可以结合这两种搜索方法，以提升检索效果并应对更多场景？答案是可以的，这种方法被称为混合搜索（hybrid search），在人工智能应用中被广泛采用。

TiDB 中混合搜索的通用工作流程如下：

1. 使用 TiDB 进行 **全文搜索** 和 **向量搜索**。
2. 使用 **reranker** 来结合两者的搜索结果。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

本教程演示如何在 TiDB 中结合使用混合搜索，借助 [pytidb](https://github.com/pingcap/pytidb) Python SDK，该 SDK 内置支持嵌入（embedding）和 reranking（重排序）。使用 pytidb 完全是可选的 —— 你也可以直接使用 SQL 进行搜索，并根据需要使用自己的 reranking 模型。

## 前提条件

混合搜索依赖于 [全文搜索](/tidb-cloud/vector-search-full-text-search-python.md) 和向量搜索。全文搜索目前仍处于早期阶段，我们正在不断向更多客户推广。目前，全文搜索仅在以下产品选项和区域提供：

- TiDB Cloud Serverless：`Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

完成本教程前，请确保你在支持的区域拥有一个 TiDB Cloud Serverless 集群。如果还没有，可以参考 [创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建。

## 开始使用

### 第一步：安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

```shell
pip install "pytidb[models]"

# (可选) 如果你不想使用内置的 embedding 函数和 reranker：
# pip install pytidb

# (可选) 若要将查询结果转换为 pandas DataFrame：
# pip install pandas
```

### 第二步：连接到 TiDB

```python
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="HOST_HERE",
    port=4000,
    username="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DATABASE_HERE",
)
```

你可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 获取这些连接参数：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect** 按钮，会弹出连接对话框，列出连接参数。

   例如，连接参数显示如下：

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   对应的 Python 连接代码示例如下：

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   注意，上述示例仅为演示用途。你需要填写自己的参数值，并妥善保管。

### 第三步：创建表

以创建名为 `chunks` 的表为例，包含以下字段：

- `id`（int）：块的 ID
- `text`（text）：块的文本内容
- `text_vec`（vector）：文本的向量表示，由 pytidb 中的 embedding 模型自动生成
- `user_id`（int）：创建该块的用户 ID

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction("openai/text-embedding-3-small")

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(
        source_field="text"
    )  # 👈 定义向量字段
    user_id: int = Field()

table = db.create_table(schema=Chunk)
```

### 第四步：插入数据

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),   # 👈 text 字段会被嵌入成向量，存入 "text_vec" 字段
        Chunk(id=3, text="baz", user_id=3),   # 并自动存储
        Chunk(id=4, text="qux", user_id=4),   # 以此类推
    ]
)
```

### 第五步：执行混合搜索

在此示例中，使用 [jina-reranker](https://huggingface.co/jinaai/jina-reranker-m0) 模型对搜索结果进行 rerank。

```python
from pytidb.rerankers import Reranker

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0")

df = (
  table.search("<query>", search_type="hybrid")
    .rerank(jinaai, "text")  # 👈 使用 jinaai 模型对查询结果进行 rerank
    .limit(2)
    .to_pandas()
)
```

完整示例请参考 [pytidb hybrid search demo](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)。

## 相关链接

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [Python 实现全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)

## 反馈与帮助

全文搜索目前仍处于早期阶段，访问权限有限。如果你希望在尚未支持的区域尝试全文搜索，或有反馈或需要帮助，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>