---
title: "Integrate TiDB Vector Search with TiDB Cloud Hosted Embedding Models"
description: "Learn how to integrate TiDB Vector Search with TiDB Cloud Hosted Embedding Models to store embeddings and perform semantic search."
keywords: "TiDB, TiDB Cloud, Vector search, text embeddings"
---

# Integrate TiDB Vector Search with TiDB Cloud Hosted Embedding Models

This tutorial demonstrates how to use TiDB Cloud hosted embedding models to generate embeddings for text data, store them in TiDB vector storage, and perform semantic search.

!!! info

    Currently, [Server-Side Auto Embedding](../guides/auto-embedding.md) is only available on [TiDB Cloud Starter](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme) clusters in the following AWS regions:

    - `Frankfurt (eu-central-1)`
    - `Oregon (us-west-2)`
    - `N. Virginia (us-east-1)`

## TiDB Cloud Hosted Embeddings

TiDB Cloud provides hosted embedding models for generating text embeddings without requiring external API keys.

### Supported Models

TiDB Cloud currently supports the following hosted embedding models:

| Model Name                                    | Dimensions | Max Input Tokens | Features |
|-----------------------------------------------|------------|------------------|----------|
| `tidbcloud_free/amazon/titan-embed-text-v2`  | 1536       | 8192             | Text, Multilingual |
| `tidbcloud_free/cohere/embed-english-v3`     | 1024       | 512              | Text, English-optimized |
| `tidbcloud_free/cohere/embed-multilingual-v3`| 1024       | 512              | Text, Multilingual |

!!! info

    `tidbcloud_free` prefix models are provided by TiDB Cloud for free.

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using TiDB Cloud hosted embedding models.

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

### Step 2: Create a vector table

Create a table with a vector field that uses the `tidbcloud_free/amazon/titan-embed-text-v2` model to generate 1536-dimensional vectors:

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
            model_name="tidbcloud_free/amazon/titan-embed-text-v2"
        ).VectorField(source_field="content")

    table = tidb_client.create_table(schema=Document, if_exists="overwrite")
    ```

=== "SQL"

    ```sql
    CREATE TABLE sample_documents (
        `id`        INT PRIMARY KEY,
        `content`   TEXT,
        `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
            "tidbcloud_free/amazon/titan-embed-text-v2",
            `content`
        )) STORED
    );
    ```

!!! info

    `tidbcloud_free` prefix models is not required to configure the API key.

### Step 3: Insert data into the table

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

### Step 4: Search for similar documents

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