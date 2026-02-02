---
title: HuggingFace Embeddings
summary: Learn how to use HuggingFace embedding models in TiDB Cloud.
aliases: ['/tidbcloud/vector-search-auto-embedding-huggingface/']
---

# HuggingFace Embeddings

This document describes how to use HuggingFace embedding models with [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

HuggingFace models are available for use with the `huggingface/` prefix if you bring your own [HuggingFace Inference API](https://huggingface.co/docs/inference-providers/index) key (BYOK).

For your convenience, the following sections take several popular models as examples to show how to use them with Auto Embedding. For a full list of available models, see [HuggingFace Models](https://huggingface.co/models?library=sentence-transformers&inference_provider=hf-inference&sort=trending). Note that not all models are provided by HuggingFace Inference API or always working.

## multilingual-e5-large

- Name: `huggingface/intfloat/multilingual-e5-large`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/intfloat/multilingual-e5-large>

Example:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/intfloat/multilingual-e5-large",
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

## bge-m3

- Name: `huggingface/BAAI/bge-m3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/BAAI/bge-m3>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/BAAI/bge-m3",
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

## all-MiniLM-L6-v2

- Name: `huggingface/sentence-transformers/all-MiniLM-L6-v2`
- Dimensions: 384
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>

Example:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-MiniLM-L6-v2",
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

## all-mpnet-base-v2

- Name: `huggingface/sentence-transformers/all-mpnet-base-v2`
- Dimensions: 768
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/sentence-transformers/all-mpnet-base-v2>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-mpnet-base-v2",
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

## Qwen3-Embedding-0.6B

> **Note:**
>
> HuggingFace Inference API might be not stable for this model.

- Name: `huggingface/Qwen/Qwen3-Embedding-0.6B`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 512
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/Qwen/Qwen3-Embedding-0.6B",
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

## Python usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using Hugging Face embedding models.

### Step 1: Connect to the database

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

### Step 2: Configure the API key

If you're using a private model or need higher rate limits, you can configure your Hugging Face API token. You can create your token from the [Hugging Face Token Settings](https://huggingface.co/settings/tokens) page:

Configure the API token for Hugging Face models using the TiDB Client:

```python
tidb_client.configure_embedding_provider(
    provider="huggingface",
    api_key="{your-huggingface-token}",
)
```

### Step 3: Create a vector table

Create a table with a vector field that uses a Hugging Face model to generate embeddings:

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="huggingface/sentence-transformers/all-MiniLM-L6-v2"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

> **Tip:**
>
> The vector dimensions depend on the model you choose. For example, `huggingface/sentence-transformers/all-MiniLM-L6-v2` produces 384-dimensional vectors, while `huggingface/sentence-transformers/all-mpnet-base-v2` produces 768-dimensional vectors.

### Step 4: Insert data into the table

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

### Step 5: Search for similar documents

Use the `table.search()` API to perform vector search:

```python
results = table.search("How do neural networks work?") \
    .limit(3) \
    .to_list()

for doc in results:
    print(f"ID: {doc.id}, Content: {doc.content}")
```

## See also

- [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/concepts/vector-search-overview.md)
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)
