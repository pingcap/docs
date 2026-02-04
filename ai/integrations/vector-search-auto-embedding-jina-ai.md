---
title: Jina AI Embeddings
summary: Learn how to use Jina AI embedding models in TiDB Cloud.
aliases: ['/tidbcloud/vector-search-auto-embedding-jina-ai/']
---

# Jina AI Embeddings

This document describes how to use [Jina AI embedding models](https://jina.ai/embeddings/) with [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches with text queries.

> **Note:**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

Jina AI provides high-performance, multimodal, and multilingual long-context embeddings for search, RAG, and agent applications.

All Jina AI models are available for use with the `jina_ai/` prefix if you bring your own Jina AI API key (BYOK). For example:

**jina-embeddings-v4**

- Name: `jina_ai/jina-embeddings-v4`
- Dimensions: 2048
- Distance metric: Cosine, L2
- Maximum input text tokens: 32,768
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**jina-embeddings-v3**

- Name: `jina_ai/jina-embeddings-v3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 8,192
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [Jina AI Documentation](https://jina.ai/embeddings/).

## Usage example

This example shows how to create a vector table, insert documents, and run similarity search using Jina AI embedding models.

### Step 1: Connect to the database

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb import TiDBClient

tidb_client = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="{database}",
    ensure_db=True,
)
```

</div>
<div label="SQL" value="sql">

```bash
mysql -h {gateway-region}.prod.aws.tidbcloud.com \
    -P 4000 \
    -u {prefix}.root \
    -p{password} \
    -D {database}
```
</div>
</SimpleTab>

### Step 2: Configure the API key

Create your API key from the [Jina AI Platform](https://jina.ai/embeddings/) and bring your own key (BYOK) to use the embedding service.

<SimpleTab groupId="language">
<div label="Python" value="python">

Configure the API key for the Jina AI embedding provider using the TiDB Client:

```python
tidb_client.configure_embedding_provider(
    provider="jina_ai",
    api_key="{your-jina-api-key}",
)
```

</div>
<div label="SQL" value="sql">

Set the API key for the Jina AI embedding provider using SQL:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = "{your-jina-api-key}";
```

</div>
</SimpleTab>

### Step 3: Create a vector table

Create a table with a vector field that uses the `jina_ai/jina-embeddings-v4` model to generate 2048-dimensional vectors:

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="jina_ai/jina-embeddings-v4"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
        "jina_ai/jina-embeddings-v4",
        `content`
    )) STORED
);
```

</div>
</SimpleTab>

### Step 4: Insert data into the table

<SimpleTab groupId="language">
<div label="Python" value="python">

Use the `table.insert()` or `table.bulk_insert()` API to add data:

```python
documents = [
    Document(id=1, content="Java: Object-oriented language for cross-platform development."),
    Document(id=2, content="Java coffee: Bold Indonesian beans with low acidity."),
    Document(id=3, content="Java island: Densely populated, home to Jakarta."),
    Document(id=4, content="Java's syntax is used in Android apps."),
    Document(id=5, content="Dark roast Java beans enhance espresso blends."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

Insert data using the `INSERT INTO` statement:

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");
```

</div>
</SimpleTab>

### Step 5: Search for similar documents

<SimpleTab groupId="language">
<div label="Python" value="python">

Use the `table.search()` API to perform vector search:

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

</div>
<div label="SQL" value="sql">

Use the `VEC_EMBED_COSINE_DISTANCE` function to perform vector search based on cosine distance metric:

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

Result:

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

</div>
</SimpleTab>

## Options

All [Jina AI options](https://jina.ai/embeddings/) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify "downstream task" for better performance**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
                `content`,
                '{"task": "retrieval.passage", "task@search": "retrieval.query"}'
              )) STORED
);
```

**Example: Use an alternative dimension**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v3",
                `content`,
                '{"dimensions":768}'
              )) STORED
);
```

For all available options, see [Jina AI Documentation](https://jina.ai/embeddings/).

## See also

- [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/concepts/vector-search-overview.md)
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)
