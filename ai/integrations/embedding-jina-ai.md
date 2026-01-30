---
title: "Integrate TiDB Vector Search with Jina AI Embeddings API"
description: "Learn how to integrate TiDB Vector Search with Jina AI Embeddings API to store embeddings and perform semantic search."
keywords: "TiDB, Jina AI, Vector search, text embeddings, multimodal embeddings"
---

# Integrate TiDB Vector Search with Jina AI Embeddings API

This tutorial demonstrates how to use [Jina AI](https://jina.ai/embeddings/) to generate embeddings for text and image data, store them in TiDB vector storage, and perform semantic search.

!!! info

    Currently, [Server-Side Auto Embedding](../guides/auto-embedding.md) is only available on [TiDB Cloud Starter](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme) clusters in the following AWS regions:

    - `Frankfurt (eu-central-1)`
    - `Oregon (us-west-2)`
    - `N. Virginia (us-east-1)`

## Jina AI Embeddings

Jina AI provides high-performance, multimodal, and multilingual long-context embeddings for search, RAG, and agent applications.

### Supported Models

| Model Name                       | Dimensions | Max Input Tokens | Description |
|----------------------------------|------------|------------------|-------------|
| `jina_ai/jina-embeddings-v4`     | 2048 | 32,768 | Multimodal, multilingual, text and image embeddings |
| `jina_ai/jina-clip-v2`           | 1024       | 8192             | Multilingual multimodal embeddings for texts and images |
| `jina_ai/jina-embeddings-v3`     | 1024       | 8192             | Multilingual, text and code embeddings |

For a complete list of supported models and detailed specifications, see the [Jina AI Embeddings Documentation](https://jina.ai/embeddings/).

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using Jina AI embedding models.

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

Create your API key from the [Jina AI Platform](https://jina.ai/embeddings/) and bring your own key (BYOK) to use the embedding service.

=== "Python"

    Configure the API key for the Jina AI embedding provider using the TiDB Client:

    ```python
    tidb_client.configure_embedding_provider(
        provider="jina_ai",
        api_key="{your-jina-api-key}",
    )
    ```

=== "SQL"

    Set the API key for the Jina AI embedding provider using SQL:

    ```sql
    SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = "{your-jina-api-key}";
    ```

### Step 3: Create a vector table

Create a table with a vector field that uses the `jina_ai/jina-embeddings-v4` model to generate 2048-dimensional vectors:

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
            model_name="jina_ai/jina-embeddings-v4"
        ).VectorField(source_field="content")

    table = tidb_client.create_table(schema=Document, if_exists="overwrite")
    ```

=== "SQL"

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

### Step 4: Insert data into the table

=== "Python"

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

=== "SQL"

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

### Step 5: Search for similar documents

=== "Python"

    Use the `table.search()` API to perform vector search:

    ```python
    results = table.search("How to start learning Java programming?") \
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
        VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
    FROM sample_documents
    ORDER BY _distance ASC
    LIMIT 2;
    ```
