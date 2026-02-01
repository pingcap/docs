---
title: NVIDIA NIM Embeddings
summary: Learn how to use NVIDIA NIM embedding models in TiDB Cloud.
aliases: ['/tidbcloud/vector-search-auto-embedding-nvidia-nim/']
---

# NVIDIA NIM Embeddings

This document describes how to use NVIDIA NIM embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

Embedding models hosted on NVIDIA NIM are available for use with the `nvidia_nim/` prefix if you bring your own [NVIDIA NIM API key](https://build.nvidia.com/settings/api-keys) (BYOK).

For your convenience, the following section takes a popular model as an example to show how to use it with Auto Embedding. For a full list of available models, see [NVIDIA NIM Text-to-embedding Models](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding).

## bge-m3

- Name: `nvidia_nim/baai/bge-m3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 8,192
- Price: Charged by NVIDIA
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Docs: <https://docs.api.nvidia.com/nim/reference/baai-bge-m3>

Example:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = 'your-nvidia-nim-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "nvidia_nim/baai/bge-m3",
                `content`
              )) STORED
);

INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
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

## nv-embed-v1

This example demonstrates creating a vector table, inserting documents, and performing similarity search using `nvidia/nv-embed-v1` model.

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

If you're using NVIDIA NIM models that require authentication, you can configure your API key. You can get free access to NIM API endpoints through the [NVIDIA Developer Program](https://developer.nvidia.com/nim) or create your API key from the [NVIDIA Build Platform](https://build.nvidia.com/settings/api-keys):

<SimpleTab groupId="language">
<div label="Python" value="python">

Configure the API key for NVIDIA NIM models using the TiDB Client:

```python
tidb_client.configure_embedding_provider(
    provider="nvidia_nim",
    api_key="{your-nvidia-api-key}",
)
```

</div>
<div label="SQL" value="sql">

Set the API key for NVIDIA NIM models using SQL:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = "{your-nvidia-api-key}";
```

</div>
</SimpleTab>

### Step 3: Create a vector table

Create a table with a vector field that uses an NVIDIA NIM model to generate embeddings:

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
        model_name="nvidia/nv-embed-v1"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(4096) GENERATED ALWAYS AS (EMBED_TEXT(
        "nvidia/nv-embed-v1",
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
    Document(id=1, content="Machine learning algorithms can identify patterns in data."),
    Document(id=2, content="Deep learning uses neural networks with multiple layers."),
    Document(id=3, content="Natural language processing helps computers understand text."),
    Document(id=4, content="Computer vision enables machines to interpret images."),
    Document(id=5, content="Reinforcement learning learns through trial and error."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

Insert data using the `INSERT INTO` statement:

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Machine learning algorithms can identify patterns in data."),
    (2, "Deep learning uses neural networks with multiple layers."),
    (3, "Natural language processing helps computers understand text."),
    (4, "Computer vision enables machines to interpret images."),
    (5, "Reinforcement learning learns through trial and error.");
```

</div>
</SimpleTab>

### Step 5: Search for similar documents

<SimpleTab groupId="language">
<div label="Python" value="python">

Use the `table.search()` API to perform vector search:

```python
results = table.search("How do neural networks work?") \
    .limit(3) \
    .to_list()

for doc in results:
    print(f"ID: {doc.id}, Content: {doc.content}")
```

</div>
<div label="SQL" value="sql">

Use the `VEC_EMBED_COSINE_DISTANCE` function to perform vector search with cosine distance:

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How do neural networks work?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 3;
```

</div>
</SimpleTab>

## See also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
