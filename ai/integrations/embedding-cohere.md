---
title: "Integrate TiDB Vector Search with Cohere Embeddings API"
description: "Learn how to integrate TiDB Vector Search with Cohere Embeddings API to store embeddings and perform semantic search."
keywords: "TiDB, Cohere, Vector search, text embeddings, multilingual embeddings"
---

# Integrate TiDB Vector Search with Cohere Embeddings API

This tutorial demonstrates how to use [Cohere](https://cohere.com/embed) to generate text embeddings, store them in TiDB vector storage, and perform semantic search.

!!! info

    Currently, [Server-Side Auto Embedding](../guides/auto-embedding.md) is only available on [TiDB Cloud Starter](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme) clusters in the following AWS regions:

    - `Frankfurt (eu-central-1)`
    - `Oregon (us-west-2)`
    - `N. Virginia (us-east-1)`

## Cohere Embeddings

Cohere offers multilingual embedding models for search, RAG, and classification. The latest `embed-v4.0` model supports text, images, and mixed content. You can use the Cohere Embeddings API with TiDB through the AI SDK or native SQL functions for automatic embedding generation.

### Supported Models

| Model Name                       | Dimensions | Max Input Tokens | Description |
|----------------------------------|------------|------------------|-------------|
| `cohere/embed-v4.0`             | 256, 512, 1024, 1536 (default) | 128k | Latest multimodal model supporting text, images, and mixed content (PDFs) |
| `cohere/embed-english-v3.0`     | 1024       | 512              | High-performance English embedding model optimized for search and classification |
| `cohere/embed-multilingual-v3.0`| 1024       | 512              | Multilingual model supporting 100+ languages |
| `cohere/embed-english-light-v3.0` | 384     | 512              | Lightweight English model for faster processing with similar performance |
| `cohere/embed-multilingual-light-v3.0` | 384 | 512          | Lightweight multilingual model for faster processing with similar performance |

For a complete list of supported models and detailed specifications, see the [Cohere Embeddings Documentation](https://docs.cohere.com/docs/cohere-embed).

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using Cohere embedding models.

### Step 1: Connect to the database

=== "Python"

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

=== "SQL"

    ```bash
    mysql -h {gateway-region}.prod.aws.tidbcloud.com \
        -P 4000 \
        -u {prefix}.root \
        -p{password} \
        -D {database}
    ```

### Step 2: Configure the API key

Create your API key from the [Cohere Dashboard](https://dashboard.cohere.com/api-keys) and bring your own key (BYOK) to use the embedding service.

=== "Python"

    Configure the API key for the Cohere embedding provider using the TiDB Client:

    ```python
    tidb_client.configure_embedding_provider(
        provider="cohere",
        api_key="{your-cohere-api-key}",
    )
    ```

=== "SQL"

    Set the API key for the Cohere embedding provider using SQL:

    ```sql
    SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = "{your-cohere-api-key}";
    ```

### Step 3: Create a vector table

Create a table with a vector field that uses the `cohere/embed-v4.0` model to generate 1536-dimensional vectors (default dimension):

=== "Python"

    ```python
    from pytidb.schema import TableModel, Field
    from pytidb.embeddings import EmbeddingFunction
    from pytidb.datatype import TEXT

    class Document(TableModel):
        __tablename__ = "sample_documents"
        id: int = Field(primary_key=True)
        content: str = Field(sa_type=TEXT)
        embedding: list[float] = EmbeddingFunction(
            model_name="cohere/embed-v4.0"
        ).VectorField(source_field="content")

    table = tidb_client.create_table(schema=Document, if_exists="overwrite")
    ```

=== "SQL"

    ```sql
    CREATE TABLE sample_documents (
        `id`        INT PRIMARY KEY,
        `content`   TEXT,
        `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
            "cohere/embed-v4.0",
            `content`
        )) STORED
    );
    ```

### Step 4: Insert data into the table

=== "Python"

    Use the `table.insert()` or `table.bulk_insert()` API to add data:

    ```python
    documents = [
        Document(id=1, content="Python: High-level programming language for data science and web development."),
        Document(id=2, content="Python snake: Non-venomous constrictor found in tropical regions."),
        Document(id=3, content="Python framework: Django and Flask are popular web frameworks."),
        Document(id=4, content="Python libraries: NumPy and Pandas for data analysis."),
        Document(id=5, content="Python ecosystem: Rich collection of packages and tools."),
    ]
    table.bulk_insert(documents)
    ```

=== "SQL"

    Insert data using the `INSERT INTO` statement:

    ```sql
    INSERT INTO sample_documents (id, content)
    VALUES
        (1, "Python: High-level programming language for data science and web development."),
        (2, "Python snake: Non-venomous constrictor found in tropical regions."),
        (3, "Python framework: Django and Flask are popular web frameworks."),
        (4, "Python libraries: NumPy and Pandas for data analysis."),
        (5, "Python ecosystem: Rich collection of packages and tools.");
    ```

### Step 5: Search for similar documents

=== "Python"

    Use the `table.search()` API to perform vector search:

    ```python
    results = table.search("How to learn Python programming?") \
        .limit(2) \
        .to_list()
    print(results)
    ```

=== "SQL"

    Use the `VEC_EMBED_COSINE_DISTANCE` function to perform vector search based on cosine distance metric:

    ```sql
    SELECT
        `id`,
        `content`,
        VEC_EMBED_COSINE_DISTANCE(embedding, "How to learn Python programming?") AS _distance
    FROM sample_documents
    ORDER BY _distance ASC
    LIMIT 2;
    ```
