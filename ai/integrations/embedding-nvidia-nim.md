---
title: "Integrate TiDB Vector Search with NVIDIA NIM Embeddings"
description: "Learn how to integrate TiDB Vector Search with NVIDIA NIM models to store embeddings and perform semantic search."
keywords: "TiDB, NVIDIA NIM, Vector search, text embeddings, AI models"
---

# Integrate TiDB Vector Search with NVIDIA NIM Embeddings

This tutorial demonstrates how to use [NVIDIA NIM](https://developer.nvidia.com/nim) models to generate text embeddings, store them in TiDB vector storage, and perform semantic search.

!!! info

    Currently, [Server-Side Auto Embedding](../guides/auto-embedding.md) is only available on [TiDB Cloud Starter](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme) clusters in the following AWS regions:

    - `Frankfurt (eu-central-1)`
    - `Oregon (us-west-2)`
    - `N. Virginia (us-east-1)`

## NVIDIA NIM Embeddings

NVIDIA NIM™ (NVIDIA Inference Microservices) provides containers to self-host GPU-accelerated inferencing microservices for pretrained and customized AI models across clouds, data centers, and RTX™ AI PCs and workstations. NIM microservices expose industry-standard APIs for simple integration into AI applications, development frameworks, and workflows.

You can integrate NVIDIA NIM embedding models with TiDB using the AI SDK, which enables automatic embedding generation from various transformer-based models.

### Supported Models

NVIDIA NIM supports a range of embedding models optimized for different use cases. Here are some popular examples:

| Model Name | Dimensions | Max Input Tokens | Description |
|------------|------------|------------------|-------------|
| `nvidia/nv-embed-v1` | 4096 | 32k | High-quality general-purpose embeddings based on Mistral-7B-v0.1 with Latent-Attention pooling |
| `nvidia/llama-3_2-nemoretriever-300m-embed-v1` | 2048 | 8192 | Multilingual embeddings using Llama 3.2 architecture, supporting 20+ languages and long-context reasoning |

For a complete list of supported models and detailed specifications, see the [NVIDIA Build Platform](https://build.nvidia.com/search?q=Embedding).

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using NVIDIA NIM embedding models.

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

If you're using NVIDIA NIM models that require authentication, you can configure your API key. You can get free access to NIM API endpoints through the [NVIDIA Developer Program](https://developer.nvidia.com/nim) or create your API key from the [NVIDIA Build Platform](https://build.nvidia.com/settings/api-keys):

=== "Python"

    Configure the API key for NVIDIA NIM models using the TiDB Client:

    ```python
    tidb_client.configure_embedding_provider(
        provider="nvidia_nim",
        api_key="{your-nvidia-api-key}",
    )
    ```

=== "SQL"

    Set the API key for NVIDIA NIM models using SQL:

    ```sql
    SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = "{your-nvidia-api-key}";
    ```

### Step 3: Create a vector table

Create a table with a vector field that uses an NVIDIA NIM model to generate embeddings:

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
            model_name="nvidia/nv-embed-v1"
        ).VectorField(source_field="content")

    table = tidb_client.create_table(schema=Document, if_exists="overwrite")
    ```

=== "SQL"

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

### Step 4: Insert data into the table

=== "Python"

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

=== "SQL"

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

### Step 5: Search for similar documents

=== "Python"

    Use the `table.search()` API to perform vector search:

    ```python
    results = table.search("How do neural networks work?") \
        .limit(3) \
        .to_list()
    
    for doc in results:
        print(f"ID: {doc.id}, Content: {doc.content}")
    ```

=== "SQL"

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
