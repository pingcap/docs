---
title: Auto Embedding Overview
summary: Learn how to use Auto Embedding to perform semantic search using pure text instead of vectors.
aliases: ["/tidb/stable/vector-search-auto-embedding-overview"]
---

# Auto Embedding Overview

Auto Embedding is a powerful feature that allows you to use vector search with pure text instead of bringing your own vectors.
With Auto Embedding, you can insert text data directly and perform semantic searches using text queries, while TiDB automatically handles the vector conversion behind the scenes.

To use Auto Embedding, here's the basic workflow:

1. **Define a table** with a text column and a generated vector column using `EMBED_TEXT()`
2. **Insert text data** - vectors are automatically generated and stored concurrently
3. **Query using text** - use `VEC_EMBED_COSINE_DISTANCE()` or `VEC_EMBED_L2_DISTANCE()` to find semantically similar content

## Quick Start Example

> **Tip:**
>
> For Python usage, see [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

Here's a simple example showing how to use Auto Embedding with cosine distance. No API keys are required:

```sql
-- Create a table with auto-embedding
-- The dimension of the vector column must match the dimension of the embedding model,
-- otherwise an error will be returned when inserting data.
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED
);

-- Insert text data (vectors generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content using text query
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

Results:

```
+----+--------------------------------------------------------------+
| id | content                                                      |
+----+--------------------------------------------------------------+
|  2 | Solar panels convert sunlight into renewable energy.         |
|  1 | Electric vehicles reduce air pollution in cities.            |
|  4 | Deep learning algorithms improve medical diagnosis accuracy. |
+----+--------------------------------------------------------------+
```

For other models, see [Available Text Embedding Models](#available-text-embedding-models) below.

## Auto Embedding + Vector Index

Auto embedding is compatible with [Vector Index](/vector-search/vector-search-index.md) for better query performance. Define a vector index over the generated vector column, and it will be used automatically:

```sql
-- Create a table with auto-embedding and vector index over the generated vector
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    VECTOR INDEX ((VEC_COSINE_DISTANCE(content_vector)))
);

-- Insert text data (vectors generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content using text query over vector index using the same VEC_EMBED_COSINE_DISTANCE() function
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

> **Note:**
>
> You must use `VEC_COSINE_DISTANCE` or `VEC_L2_DISTANCE` when defining the vector index, while using `VEC_EMBED_COSINE_DISTANCE` or `VEC_EMBED_L2_DISTANCE` when performing vector search queries.

## Available Text Embedding Models

TiDB Cloud supports various embedding models. Choose the one that best fits your needs:

| Embedding Model | Documentation                                                                       | Hosted by TiDB Cloud [<sup>1</sup>](#hosted-models) | BYOK [<sup>2</sup>](#byok-models) |
| --------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------- |
| Amazon Titan    | [Amazon Titan Embeddings](/tidb-cloud/vector-search-auto-embedding-amazon-titan.md) | ✅                                                  |                                   |
| Cohere          | [Cohere Embeddings](/tidb-cloud/vector-search-auto-embedding-cohere.md)             | ✅                                                  | ✅                                |
| Jina AI         | [Jina AI Embeddings](/tidb-cloud/vector-search-auto-embedding-jina-ai.md)           |                                                     | ✅                                |
| OpenAI          | [OpenAI Embeddings](/tidb-cloud/vector-search-auto-embedding-openai.md)             |                                                     | ✅                                |
| Gemini          | [Gemini Embeddings](/tidb-cloud/vector-search-auto-embedding-gemini.md)             |                                                     | ✅                                |

You can also use open-source embedding models via following inference services supported by TiDB Cloud:

| Embedding Model       | Documentation                                                                     | Hosted by TiDB Cloud [<sup>1</sup>](#hosted-models) | BYOK [<sup>2</sup>](#byok-models) | Example Supported Models      |
| --------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------- | ----------------------------- |
| HuggingFace Inference | [HuggingFace Embeddings](/tidb-cloud/vector-search-auto-embedding-huggingface.md) |                                                     | ✅                                | bge-m3, multilingual-e5-large |
| NVIDIA NIM            | [NVIDIA NIM Embeddings](/tidb-cloud/vector-search-auto-embedding-nvidia-nim.md)   |                                                     | ✅                                | bge-m3, nv-embed-v1           |

<a name="hosted-models"></a> <sup>1</sup> Hosted models are hosted by TiDB Cloud and don't require any API keys. They are currently free to use.

<a name="byok-models"></a> <sup>2</sup> BYOK (Bring Your Own Key) models require you to provide your own API keys of the corresponding embedding provider. TiDB Cloud does not charge for the usage of BYOK models. You are responsible for managing and monitoring the costs associated with using these models.

## How Auto Embedding Works

Auto Embedding uses the [`EMBED_TEXT()`](#embed_text) function to automatically convert text into vector embeddings using your chosen embedding model.
The generated vectors are stored in `VECTOR` columns and can be used for semantic similarity searches using text queries with [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) or [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance).

Under the hood, [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) and [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) will be translated into [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance) and [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance) with the text query automatically converted into a vector embedding.

## Key Functions

### EMBED_TEXT()

Converts text to vector embeddings:

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

Use this function in `GENERATED ALWAYS AS` clauses to automatically create embeddings when inserting text data.

### VEC_EMBED_COSINE_DISTANCE()

Calculates cosine similarity between a stored vector and a text query:

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

Use this function in `ORDER BY` clauses to rank results by cosine distance. It uses the same calculation as [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance), but automatically generates the embedding for the query text.

### VEC_EMBED_L2_DISTANCE()

Calculates L2 (Euclidean) distance between a stored vector and a text query:

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

Use this function in `ORDER BY` clauses to rank results by L2 distance. It uses the same calculation as [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance), but automatically generates the embedding for the query text.

## Use Auto Embedding in Python

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
