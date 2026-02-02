---
title: OpenAI Embeddings
summary: Learn how to use OpenAI embedding models in TiDB Cloud.
aliases: ['/tidbcloud/vector-search-auto-embedding-openai/']
---

# OpenAI Embeddings

This document describes how to use OpenAI embedding models with [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

All OpenAI models are available for use with the `openai/` prefix if you bring your own OpenAI API key (BYOK). For example:

**text-embedding-3-small**

- Name: `openai/text-embedding-3-small`
- Dimensions: 512-1536 (default: 1536)
- Distance metric: Cosine, L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**text-embedding-3-large**

- Name: `openai/text-embedding-3-large`
- Dimensions: 256-3072 (default: 3072)
- Distance metric: Cosine, L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings).

## Usage example

This example demonstrates creating a vector table, inserting documents, and performing similarity search using OpenAI embedding models.

You can integrate the OpenAI Embeddings API with TiDB using the AI SDK or native SQL functions for automatic embedding generation.

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

Create your own API key from the [OpenAI API Platform](https://platform.openai.com/api-keys) and bring your own key (BYOK) to use the embedding service.

<SimpleTab groupId="language">
<div label="Python" value="python">

Configure the API key for the OpenAI embedding provider using the TiDB Client:

```python
tidb_client.configure_embedding_provider(
    provider="openai",
    api_key="{your-openai-api-key}",
)
```

</div>
<div label="SQL" value="sql">

Set the API key for the OpenAI embedding provider using SQL:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = "{your-openai-api-key}";
```

</div>
</SimpleTab>

### Step 3: Create a vector table

Create a table with a vector field that uses the `openai/text-embedding-3-small` model to generate 1536-dimensional vectors:

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
        model_name="openai/text-embedding-3-small"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
        "openai/text-embedding-3-small",
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

Use the `VEC_EMBED_COSINE_DISTANCE` function to perform vector search with cosine distance:

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

Result:

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

</div>
</SimpleTab>

## Use Azure OpenAI

To use OpenAI embedding models on Azure, set the global variable `TIDB_EXP_EMBED_OPENAI_API_BASE` to the URL of your Azure resource. For example:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = 'https://<your-resource-name>.openai.azure.com/openai/v1';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

Note that even if your resource URL appears as `https://<your-resource-name>.cognitiveservices.azure.com/`, you must use `https://<your-resource-name>.openai.azure.com/openai/v1` as the API base to ensure OpenAI-compatible request and response formats.

To switch from Azure OpenAI to OpenAI directly, set `TIDB_EXP_EMBED_OPENAI_API_BASE` to an empty string:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **Note:**
>
> - For security reasons, you can only set the API base to an Azure OpenAI URL or the OpenAI URL. Arbitrary base URLs are not allowed.
> - To use another OpenAI-compatible embedding service, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Options

All [OpenAI embedding options](https://platform.openai.com/docs/api-reference/embeddings/create) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Use an alternative dimension for text-embedding-3-large**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
                `content`,
                '{"dimensions": 1024}'
              )) STORED
);
```

For all available options, see [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create).

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/concepts/vector-search-overview.md)
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)