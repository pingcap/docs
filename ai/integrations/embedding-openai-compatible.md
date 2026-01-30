---
title: OpenAI-Compatible Embeddings
summary: Learn how to integrate TiDB Vector Search with OpenAI-Compatible Embedding API to store embeddings and perform semantic search.
---

# OpenAI-Compatible Embeddings

This tutorial demonstrates how to use OpenAI-compatible embedding services to generate text embeddings, store them in TiDB vector storage, and perform semantic search.

> **Note:**
>
> Currently, [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## OpenAI-like embedding services

Because the OpenAI Embedding API is widely used, many AI service providers offer APIs that are compatible with the OpenAI Embedding API, such as:

- [Ollama](https://ollama.com/)
- [vLLM](https://vllm.ai/)

TiDB AI SDK provides an `EmbeddingFunction` class that can be used to integrate with OpenAI-compatible embedding services.

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using OpenAI-compatible embedding models.

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

### Step 2: Define the embedding function

To integrate with OpenAI-compatible embedding services, initialize the `EmbeddingFunction` class and set the `model_name` parameter with the `openai/` prefix.

```python
from pytidb.embeddings import EmbeddingFunction

openai_like_embed = EmbeddingFunction(
    model_name="openai/{model_name}",
    api_base="{your-api-base}",
    api_key="{your-api-key}",
)
```

The parameters are:

- `model_name`: Specifies the model to use. Use the format `openai/{model_name}`.
- `api_base`: The base URL of your OpenAI compatible embedding API service.
- `api_key`: The API key can be used to authenticate with the embedding API service.


**Example: Using Ollama and `nomic-embed-text` model**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="http://localhost:11434/v1"
)
```

**Example: Using vLLM and `nomic-embed-text` model**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/intfloat/e5-mistral-7b-instruct",
    api_base="http://localhost:8000/v1"
)
```

### Step 3: Create a vector table

Create a table with a vector field that uses Ollama platform and `nomic-embed-text` model.

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="{your-api-base}",
)

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = openai_like_embed.VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

### Step 4: Insert data into the table

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

With [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) enabled, TiDB automatically generates vector field values when you insert data.

### Step 5: Search for similar documents

Use the `table.search()` API to perform vector search:

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

With [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) enabled, TiDB automatically generates vector embeddings for query text during vector search.
