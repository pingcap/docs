---
title: Auto Embedding
summary: Learn how to use auto embedding in your application.
---

# Auto Embedding

The Auto Embedding feature automatically generates vector embeddings for your text data.

> **Note:**
>
> For a complete example of auto embedding, see [Auto Embedding Example](/ai/examples/auto-embedding-with-pytidb.md).

## Basic usage

This document uses a TiDB Cloud hosted embedding model for demonstration. For a full list of supported providers, see [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models).

### Step 1. Define an embedding function

Define an embedding function to generate vector embeddings for your text data.

```python
from pytidb.embeddings import EmbeddingFunction

embed_func = EmbeddingFunction(
    model_name="tidbcloud_free/amazon/titan-embed-text-v2",
)
```

### Step 2. Create a table and a vector field

Use `embed_func.VectorField()` to create a vector field in the table schema.

To enable auto embedding, set `source_field` to the field you want to embed.

```python hl_lines="7"
from pytidb.schema import TableModel, Field
from pytidb.datatype import TEXT

class Chunk(TableModel):
    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = embed_func.VectorField(source_field="text")

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

You don't need to specify the `dimensions` parameter, because the embedding model automatically determines it.

However, you can set the `dimensions` parameter to override the default dimension.

### Step 3. Insert some sample data

Insert some sample data into the table.

```python
table.bulk_insert([
    Chunk(text="TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."),
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB."),
    Chunk(text="LlamaIndex is a Python library for building AI-powered applications."),
])
```

When inserting data, the `text_vec` field is automatically populated with embeddings generated from `text`.

### Step 4. Perform a vector search

You can pass query text directly to the `search()` method. The query text will be embedded automatically and then used for vector search.

```python
table.search("HTAP database").limit(3).to_list()
```
