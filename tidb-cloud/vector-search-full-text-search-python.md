---
title: 使用Python进行全文搜索
summary: 全文搜索让你能够根据精确关键词检索文档。在检索增强生成（RAG）场景中，你可以结合全文搜索和向量搜索以提升检索质量。
aliases: ['/tidb/stable/vector-search-full-text-search-python']
---

# 使用Python进行全文搜索

与[Vector Search](/tidb-cloud/vector-search-overview.md)，专注于语义相似性的搜索不同，全文搜索允许你根据精确关键词检索文档。在检索增强生成（RAG）场景中，你可以将全文搜索与向量搜索结合使用，以提升检索效果。

TiDB中的全文搜索功能提供了以下能力：

- **直接查询文本数据**：你可以直接搜索任何字符串列，无需进行嵌入处理。

- **支持多语言**：无需指定语言即可实现高质量搜索。TiDB支持存储多语言文档在同一张表中，并会自动为每个文档选择最佳的文本分析器。

- **按相关性排序**：搜索结果可以使用广泛采用的[BM25 ranking](https://en.wikipedia.org/wiki/Okapi_BM25)算法按相关性排序。

- **与SQL完全兼容**：所有SQL功能，如预过滤、后过滤、分组和连接，都可以与全文搜索结合使用。

> **Tip:**
>
> 关于SQL的使用方法，请参见 [Full-Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md)。
>
> 若要在你的AI应用中同时使用全文搜索和向量搜索，参见 [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)。

## 前提条件

全文搜索仍处于早期阶段，我们正在不断向更多客户推广。目前，全文搜索仅在以下产品选项和区域提供：

- TiDB Cloud Serverless：`Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

要完成本教程，确保你在支持的区域拥有一个TiDB Cloud Serverless集群。如果还没有，可以按照 [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) 创建。

## 开始使用

### 第1步：安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

[pytidb](https://github.com/pingcap/pytidb) 是TiDB的官方Python SDK，旨在帮助开发者高效构建AI应用。它内置支持向量搜索和全文搜索。

安装SDK，请运行以下命令：

```shell
pip install pytidb

# (可选) 若要使用内置的嵌入函数和重排序器：
# pip install "pytidb[models]"

# (可选) 若要将查询结果转换为pandas DataFrame：
# pip install pandas
```

### 第2步：连接到TiDB

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

你可以在 [TiDB Cloud控制台](https://tidbcloud.com) 获取这些连接参数：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示一个连接对话框，列出连接参数。

   例如，如果显示的连接参数如下：

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   则对应的Python连接代码如下：

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   注意，上述示例仅用于演示。你需要填写自己的参数，并妥善保管。

### 第3步：创建表和全文索引

以创建名为 `chunks` 的表为例，包含以下列：

- `id`（int）：块的ID
- `text`（text）：块的文本内容
- `user_id`（int）：创建该块的用户ID

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 在text列上创建全文索引
```

### 第4步：插入数据

```python
table.bulk_insert(
    [
        Chunk(id=2, text="the quick brown", user_id=2),
        Chunk(id=3, text="fox jumps", user_id=3),
        Chunk(id=4, text="over the lazy dog", user_id=4),
    ]
)
```

### 第5步：执行全文搜索

插入数据后，可以进行如下全文搜索：

```python
df = (
  table.search("brown fox", search_type="fulltext")
    .limit(2)
    .to_pandas() # 可选
)

#    id             text  user_id
# 0   3        fox jumps        3
# 1   2  the quick brown        2
```

完整示例请参见 [pytidb full-text search demo](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search)。

## 相关链接

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)

## 反馈与帮助

全文搜索仍处于早期阶段，访问权限有限。如果你想在尚未支持的区域试用全文搜索，或有反馈或需要帮助，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>