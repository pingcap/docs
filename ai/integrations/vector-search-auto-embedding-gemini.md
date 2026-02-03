---
title: Gemini Embeddings
summary: Learn how to use Google Gemini embedding models in TiDB Cloud.
aliases: ['/tidbcloud/vector-search-auto-embedding-gemini/']
---

# Gemini Embeddings

This document describes how to use Gemini embedding models with [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic search with text queries.

> **Note:**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

All Gemini models are available for use with the `gemini/` prefix if you bring your own Gemini API key (BYOK). For example:

**gemini-embedding-001**

- Name: `gemini/gemini-embedding-001`
- Dimensions: 128–3072 (default: 3072)
- Distance metric: Cosine, L2
- Maximum input text tokens: 2,048
- Price: Charged by Google
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## Usage example

This example shows how to create a vector table, insert documents, and run similarity search using Google Gemini embedding models.

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

Create your API key from the [Google AI Studio](https://makersuite.google.com/app/apikey) and bring your own key (BYOK) to use the embedding service.

<SimpleTab groupId="language">
<div label="Python" value="python">

Configure the API key for the Google Gemini embedding provider using the TiDB Client:

```python
tidb_client.configure_embedding_provider(
    provider="google_gemini",
    api_key="{your-google-api-key}",
)
```

</div>
<div label="SQL" value="sql">

Set the API key for the Google Gemini embedding provider using SQL:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = "{your-google-api-key}";
```

</div>
</SimpleTab>

### Step 3: Create a vector table

Create a table with a vector field that uses the `gemini-embedding-001` model to generate 3072-dimensional vectors (default):

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
        model_name="gemini-embedding-001"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
        "gemini-embedding-001",
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
    Document(id=1, content="Java: Object-oriented language for cross-platform development."),
    Document(id=2, content="Java coffee: Bold Indonesian beans with low acidity."),
    Document(id=3, content="Java island: Densely populated, home to Jakarta."),
    Document(id=4, content="Java's syntax is used in Android apps."),
    Document(id=5, content="Dark roast Java beans enhance espresso blends."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

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

</div>
</SimpleTab>

### Step 5: Search for similar documents

<SimpleTab groupId="language">
<div label="Python" value="python">

Use the `table.search()` API to perform vector search:

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

</div>
<div label="SQL" value="sql">

Use the `VEC_EMBED_COSINE_DISTANCE` function to perform vector search based on cosine distance:

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## Custom embedding dimensions

The `gemini-embedding-001` model supports flexible dimensions through Matryoshka Representation Learning (MRL). You can specify the desired dimensions in your embedding function:

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
# For 1536 dimensions
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=1536
).VectorField(source_field="content")

# For 768 dimensions
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=768
).VectorField(source_field="content")
```

</div>
<div label="SQL" value="sql">

```sql
-- For 1536 dimensions
`embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 1536}}'
)) STORED

-- For 768 dimensions
`embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 768}}'
)) STORED
```

</div>
</SimpleTab>

Choose dimensions based on your performance requirements and storage constraints. Higher dimensions can improve accuracy but require more storage and compute resources.

## Options

All [Gemini options](https://ai.google.dev/gemini-api/docs/embeddings) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify the task type to improve quality**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"task_type": "SEMANTIC_SIMILARITY"}'
              )) STORED
);
```

**Example: Use an alternative dimension**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"output_dimensionality": 768}'
              )) STORED
);
```

For all available options, see [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## See also

- [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/concepts/vector-search-overview.md)
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)
