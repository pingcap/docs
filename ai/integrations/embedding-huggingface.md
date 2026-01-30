---
title: "Integrate TiDB Vector Search with Hugging Face Embeddings"
description: "Learn how to integrate TiDB Vector Search with Hugging Face models to store embeddings and perform semantic search."
keywords: "TiDB, Hugging Face, Vector search, text embeddings, transformers"
---

# Integrate TiDB Vector Search with Hugging Face Embeddings

This tutorial demonstrates how to use [Hugging Face](https://huggingface.co/) models to generate text embeddings, store them in TiDB vector storage, and perform semantic search.

!!! info

    Currently, [Server-Side Auto Embedding](../guides/auto-embedding.md) is only available on [TiDB Cloud Starter](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme) clusters in the following AWS regions:

    - `Frankfurt (eu-central-1)`
    - `Oregon (us-west-2)`
    - `N. Virginia (us-east-1)`

## Hugging Face Embeddings

Hugging Face provides access to a vast collection of pre-trained embedding models through the Hugging Face Hub. You can integrate these models with TiDB using the AI SDK, which enables automatic embedding generation from various transformer-based models.

### Supported Models

Hugging Face supports a wide range of embedding models. Here are some popular examples:

| Model Name | Dimensions | Max Input Tokens | Description |
|------------|------------|------------------|-------------|
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | 256 | Fast, lightweight model for general-purpose embeddings |
| `sentence-transformers/all-mpnet-base-v2` | 768 | 384 | High-quality embeddings with good performance |
| `sentence-transformers/all-MiniLM-L12-v2` | 384 | 256 | Balanced model between speed and quality |
| `BAAI/bge-small-en-v1.5` | 384 | 512 | Multilingual model optimized for semantic search |
| `BAAI/bge-base-en-v1.5` | 768 | 512 | Higher quality multilingual embeddings |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 384 | 256 | Multilingual model for semantic similarity across languages |
| `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` | 768 | 384 | High-quality multilingual model based on MPNet architecture |
| `bert-base-uncased` | 768 | 512 | Google's BERT base model with 12 layers and 12 attention heads |
| `distilbert-base-uncased` | 768 | 512 | Lightweight BERT model with ~60% fewer parameters, 60% faster inference |

For a complete list of supported models and detailed specifications, see the [Hugging Face Model Hub](https://huggingface.co/models?pipeline_tag=sentence-similarity).

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using Hugging Face embedding models.

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

If you're using a private model or need higher rate limits, you can configure your Hugging Face API token. You can create your token from the [Hugging Face Token Settings](https://huggingface.co/settings/tokens) page:

=== "Python"

    Configure the API token for Hugging Face models using the TiDB Client:

    ```python
    tidb_client.configure_embedding_provider(
        provider="huggingface",
        api_key="{your-huggingface-token}",
    )
    ```

=== "SQL"

    Set the API token for Hugging Face models using SQL:

    ```sql
    SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = "{your-huggingface-token}";
    ```

### Step 3: Create a vector table

Create a table with a vector field that uses a Hugging Face model to generate embeddings:

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
            model_name="huggingface/sentence-transformers/all-MiniLM-L6-v2"
        ).VectorField(source_field="content")

    table = tidb_client.create_table(schema=Document, if_exists="overwrite")
    ```

=== "SQL"

    ```sql
    CREATE TABLE sample_documents (
        `id`        INT PRIMARY KEY,
        `content`   TEXT,
        `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
            "huggingface/sentence-transformers/all-MiniLM-L6-v2",
            `content`
        )) STORED
    );
    ```

!!! tip

    The vector dimensions depend on the model you choose. For example, `huggingface/sentence-transformers/all-MiniLM-L6-v2` produces 384-dimensional vectors, while `huggingface/sentence-transformers/all-mpnet-base-v2` produces 768-dimensional vectors.

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
