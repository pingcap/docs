---
title: 将向量搜索集成到 LangChain
summary: 学习如何将 TiDB 向量搜索与 LangChain 集成。
---

# 将向量搜索集成到 LangChain

本教程演示如何将 [vector search](/vector-search/vector-search-overview.md) 功能的 TiDB 与 [LangChain](https://python.langchain.com/) 集成。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量搜索功能处于实验阶段。不建议在生产环境中使用。此功能可能在未通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量搜索功能处于 beta 阶段，可能会在未通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

> **Tip**
>
> 你可以在 Jupyter Notebook 上查看完整的 [示例代码](https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb)，也可以直接在 [Colab](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) 在线环境中运行示例代码。

## 前提条件

完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)
- 安装 [Jupyter Notebook](https://jupyter.org/install)
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

## 开始使用

本节提供逐步指导，介绍如何将 TiDB 向量搜索与 LangChain 集成，实现语义搜索。

### 步骤 1. 创建新的 Jupyter Notebook 文件

在你偏好的目录下，创建一个名为 `integrate_with_langchain.ipynb` 的 Jupyter Notebook 文件：

```shell
touch integrate_with_langchain.ipynb
```

### 步骤 2. 安装所需依赖

在你的项目目录下，运行以下命令安装所需的包：

```shell
!pip install langchain langchain-community
!pip install langchain-openai
!pip install pymysql
!pip install tidb-vector
```

在 Jupyter Notebook 中打开 `integrate_with_langchain.ipynb` 文件，然后添加以下代码导入所需包：

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
```

### 步骤 3. 设置环境

根据你选择的 TiDB 部署方式，配置环境变量。

<SimpleTab>
<div label="{{{ .starter }}}">

对于 {{{ .starter }}} 集群，按照以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与操作环境匹配。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `SQLAlchemy`。
    - **Operating System** 与你的环境一致。

4. 点击 **PyMySQL** 标签，复制连接字符串。

    > **Tip:**
    >
    > 如果还未设置密码，可以点击 **Generate Password** 生成随机密码。

5. 配置环境变量。

    本文使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供方。在此步骤中，你需要提供上一步获得的连接字符串和你的 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

    运行以下代码配置环境变量。系统会提示你输入连接字符串和 OpenAI API 密钥：

    ```python
    # 使用 getpass 在终端中安全提示输入环境变量。
    import getpass
    import os

    # 从 TiDB Cloud 控制台复制你的连接字符串。
    # 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    tidb_connection_string = getpass.getpass("TiDB Connection String:")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    ```

</div>
<div label="TiDB Self-Managed">

本文件使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供方。在此步骤中，你需要提供上一步获得的连接字符串和你的 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

运行以下代码配置环境变量。系统会提示你输入连接字符串和 OpenAI API 密钥：

```python
# 使用 getpass 在终端中安全提示输入环境变量。
import getpass
import os

# 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

以 macOS 为例，集群连接字符串如下：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

你需要根据你的 TiDB 集群修改连接参数的值。如果在本地运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初始的 `<PASSWORD>` 为空，如果首次启动集群，可以省略此字段。

以下是各参数的说明：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机地址。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：要连接的数据库名。

</div>

</SimpleTab>

### 步骤 4. 加载示例文档

#### 步骤 4.1 下载示例文档

在你的项目目录下，创建 `data/how_to/` 目录，并从 [langchain-ai/langchain](https://github.com/langchain-ai/langchain) GitHub 仓库下载示例文档 [`state_of_the_union.txt`](https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt)：

```shell
!mkdir -p 'data/how_to/'
!wget 'https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/how_to/state_of_the_union.txt' -O 'data/how_to/state_of_the_union.txt'
```

#### 步骤 4.2 加载并拆分文档

从 `data/how_to/state_of_the_union.txt` 加载示例文档，使用 `CharacterTextSplitter` 将其拆分成大约每段 1000 字符的块：

```python
loader = TextLoader("data/how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

### 步骤 5. 嵌入并存储文档向量

TiDB 向量存储支持余弦距离（`cosine`）和欧几里得距离（`l2`）两种相似度度量策略。默认使用余弦距离。

以下代码在 TiDB 中创建一个名为 `embedded_documents` 的表，优化为支持向量搜索：

```python
embeddings = OpenAIEmbeddings()
vector_store = TiDBVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    table_name="embedded_documents",
    connection_string=tidb_connection_string,
    distance_strategy="cosine",  # 默认，另一个选项是 "l2"
)
```

成功执行后，可以直接在 TiDB 数据库中查看并访问 `embedded_documents` 表。

### 步骤 6. 执行向量搜索

本步骤演示如何从 `state_of_the_union.txt` 文档中查询“总统关于 Ketanji Brown Jackson 说了什么”。

```python
query = "What did the president say about Ketanji Brown Jackson"
```

#### 选项 1：使用 `similarity_search_with_score()`

`similarity_search_with_score()` 方法计算文档与查询之间的向量空间距离。此距离作为相似度得分，由 `distance_strategy` 决定。该方法返回前 `k` 个得分最低的文档。得分越低，表示文档与查询越相似。

```python
docs_with_score = vector_store.similarity_search_with_score(query, k=3)
for doc, score in docs_with_score:
   print("-" * 80)
   print("Score: ", score)
   print(doc.page_content)
   print("-" * 80)
```

<details>
   <summary><b>预期输出</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.18472413652518527
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.21757513022785557
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.

We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
```

</details>

#### 选项 2：使用 `similarity_search_with_relevance_scores()`

`similarity_search_with_relevance_scores()` 方法返回相关性得分最高的前 `k` 个文档。得分越高，表示文档与查询的相似度越高。

```python
docs_with_relevance_score = vector_store.similarity_search_with_relevance_scores(query, k=2)
for doc, score in docs_with_relevance_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

<details>
   <summary><b>预期输出</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.8152758634748147
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.7824248697721444
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.

We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
```

</details>

### 作为检索器使用

在 Langchain 中，[retriever](https://python.langchain.com/v0.2/docs/concepts/#retrievers) 是一种在响应非结构化查询时检索文档的接口，提供比向量存储更丰富的功能。以下代码演示如何将 TiDB 向量存储作为检索器使用。

```python
retriever = vector_store.as_retriever(
   search_type="similarity_score_threshold",
   search_kwargs={"k": 3, "score_threshold": 0.8},
)
docs_retrieved = retriever.invoke(query)
for doc in docs_retrieved:
   print("-" * 80)
   print(doc.page_content)
   print("-" * 80)
```

预期输出如下：

```
--------------------------------------------------------------------------------
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
--------------------------------------------------------------------------------
```

### 删除向量存储

要删除已有的 TiDB 向量存储，可以使用 `drop_vectorstore()` 方法：

```python
vector_store.drop_vectorstore()
```

## 使用元数据过滤器进行搜索

为了细化搜索，可以使用元数据过滤器，检索符合条件的最近邻结果。

### 支持的元数据类型

TiDB 向量存储中的每个文档都可以配有元数据，结构为键值对的 JSON 对象。键始终为字符串，值可以是以下类型之一：

- 字符串
- 数值：整数或浮点数
- 布尔值：`true` 或 `false`

例如，以下是有效的元数据负载：

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

### 元数据过滤语法

支持的过滤器包括：

- `$or`：匹配任意一个条件的向量
- `$and`：匹配所有条件的向量
- `$eq`：等于指定值
- `$ne`：不等于指定值
- `$gt`：大于指定值
- `$gte`：大于等于指定值
- `$lt`：小于指定值
- `$lte`：小于等于指定值
- `$in`：在指定数组中
- `$nin`：不在指定数组中

如果某个文档的元数据如下：

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

则以下元数据过滤器可以匹配此文档：

```json
{ "page": 12 }
```

```json
{ "page": { "$eq": 12 } }
```

```json
{
  "page": {
    "$in": [11, 12, 13]
  }
}
```

```json
{ "page": { "$nin": [13] } }
```

```json
{ "page": { "$lt": 11 } }
```

```json
{
  "$or": [{ "page": 11 }, { "page": 12 }],
  "$and": [{ "page": 12 }, { "page": 13 }]
}
```

在元数据过滤器中，TiDB 将每个键值对作为单独的过滤条件，并用 `AND` 逻辑操作符组合。

### 示例

以下示例向 `TiDBVectorStore` 添加两个文档，并为每个文档添加 `title` 字段作为元数据：

```python
vector_store.add_texts(
    texts=[
        "TiDB Vector 提供先进的高速向量处理能力，提升 AI 工作流中的数据处理和分析效率。",
        "TiDB Vector，基础用量低至每月 10 美元起",
    ],
    metadatas=[
        {"title": "TiDB Vector 功能"},
        {"title": "TiDB Vector 价格"},
    ],
)
```

预期输出如下：

```plain
[UUID('c782cb02-8eec-45be-a31f-fdb78914f0a7'),
 UUID('08dcd2ba-9f16-4f29-a9b7-18141f8edae3')]
```

执行带有元数据过滤的相似度搜索：

```python
docs_with_score = vector_store.similarity_search_with_score(
    "Introduction to TiDB Vector", filter={"title": "TiDB Vector 功能"}, k=4
)
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

预期输出如下：

```plain
--------------------------------------------------------------------------------
Score:  0.12761409169211535
TiDB Vector 提供先进的高速向量处理能力，提升 AI 工作流中的数据处理和分析效率。
--------------------------------------------------------------------------------
```

## 高级用例示例：旅游代理

本节演示如何将向量搜索与 Langchain 集成，用于旅游代理的场景。目标是为客户创建个性化的旅游报告，帮助他们找到具有特定设施的机场，例如干净的休息室和素食选择。

流程包括两个主要步骤：

1. 在机场评论中进行语义搜索，识别符合需求的机场代码。
2. 执行 SQL 查询，将这些代码与航线信息合并，突出显示符合用户偏好的航空公司和目的地。

### 准备数据

首先，创建存储机场航线数据的表：

```python
# 创建存储航班计划数据的表。
vector_store.tidb_vector_client.execute(
    """CREATE TABLE airplan_routes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        airport_code VARCHAR(10),
        airline_code VARCHAR(10),
        destination_code VARCHAR(10),
        route_details TEXT,
        duration TIME,
        frequency INT,
        airplane_type VARCHAR(50),
        price DECIMAL(10, 2),
        layover TEXT
    );"""
)

# 插入一些示例数据到 airplan_routes 和向量表。
vector_store.tidb_vector_client.execute(
    """INSERT INTO airplan_routes (
        airport_code,
        airline_code,
        destination_code,
        route_details,
        duration,
        frequency,
        airplane_type,
        price,
        layover
    ) VALUES
    ('JFK', 'DL', 'LAX', '非直达 JFK 至 LAX。', '06:00:00', 5, 'Boeing 777', 299.99, '无'),
    ('LAX', 'AA', 'ORD', '直达 LAX 至 ORD。', '04:00:00', 3, 'Airbus A320', 149.99, '无'),
    ('EFGH', 'UA', 'SEA', '每日 SFO 至 SEA 航班。', '02:30:00', 7, 'Boeing 737', 129.99, '无');
    """
)
vector_store.add_texts(
    texts=[
        "干净的休息室和优质的素食餐饮选择。强烈推荐。",
        "休息区座椅舒适，食物多样，包括素食。",
        "小型机场，设施基本。",
    ],
    metadatas=[
        {"airport_code": "JFK"},
        {"airport_code": "LAX"},
        {"airport_code": "EFGH"},
    ],
)
```

预期输出如下：

```plain
[UUID('6dab390f-acd9-4c7d-b252-616606fbc89b'),
 UUID('9e811801-0e6b-4893-8886-60f4fb67ce69'),
 UUID('f426747c-0f7b-4c62-97ed-3eeb7c8dd76e')]
```

### 进行语义搜索

以下代码搜索具有干净设施和素食选项的机场：

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.85},
)
semantic_query = "你能推荐一个有干净休息室和良好素食餐饮的美国机场吗？"
reviews = retriever.invoke(semantic_query)
for r in reviews:
    print("-" * 80)
    print(r.page_content)
    print(r.metadata)
    print("-" * 80)
```

预期输出如下：

```plain
--------------------------------------------------------------------------------
干净的休息室和优质的素食餐饮选择。强烈推荐。
{'airport_code': 'JFK'}
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
休息区座椅舒适，食物多样，包括素食。
{'airport_code': 'LAX'}
--------------------------------------------------------------------------------
```

### 获取详细机场信息

提取搜索结果中的机场代码，并查询数据库获取详细的航线信息：

```python
# 提取元数据中的机场代码
airport_codes = [review.metadata["airport_code"] for review in reviews]

# 执行查询获取机场详细信息
search_query = "SELECT * FROM airplan_routes WHERE airport_code IN :codes"
params = {"codes": tuple(airport_codes)}

airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

预期输出如下：

```plain
[(1, 'JFK', 'DL', 'LAX', '非直达 JFK 至 LAX。', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), '无'),
 (2, 'LAX', 'AA', 'ORD', '直达 LAX 至 ORD。', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), '无')]
```

### 简化流程

或者，可以用一条 SQL 查询简化整个流程：

```python
search_query = f"""
    SELECT
        VEC_Cosine_Distance(se.embedding, :query_vector) as distance,
        ar.*,
        se.document as airport_review
    FROM
        airplan_routes ar
    JOIN
        {TABLE_NAME} se ON ar.airport_code = JSON_UNQUOTE(JSON_EXTRACT(se.meta, '$.airport_code'))
    ORDER BY distance ASC
    LIMIT 5;
"""
query_vector = embeddings.embed_query(semantic_query)
params = {"query_vector": str(query_vector)}
airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

预期输出如下：

```plain
[(0.1219207353407008, 1, 'JFK', 'DL', 'LAX', '非直达 JFK 至 LAX。', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), '无', '干净的休息室和优质的素食餐饮选择。强烈推荐。'),
 (0.14613754359804654, 2, 'LAX', 'AA', 'ORD', '直达 LAX 至 ORD。', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), '无', '休息区座椅舒适，食物多样，包括素食。'),
 (0.19840519342700513, 3, 'EFGH', 'UA', 'SEA', '每日 SFO 至 SEA 航班。', datetime.timedelta(seconds=9000), 7, 'Boeing 737', Decimal('129.99'), '无', '小型机场，设施基本。')]
```

### 清理数据

最后，删除创建的表：

```python
vector_store.tidb_vector_client.execute("DROP TABLE airplan_routes")
```

预期输出如下：

```json
{"success": True, "result": 0, "error": null}
```

## 相关链接

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
