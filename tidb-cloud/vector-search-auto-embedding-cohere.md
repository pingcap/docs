---
title: Cohere Embeddings
summary: Learn how to use Cohere embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-cohere"]
---

# Cohere Embeddings

## Available Models

TiDB Cloud provides the following [Cohere](https://cohere.com/) embedding models natively. No API key required.

**Cohere Embed v3 model**

- Name: `tidbcloud_free/cohere/embed-english-v3`
- Dimensions: 1024
- Distance Metric: Cosine / L2
- Languages: English
- Max input text tokens: 512 (1 token is about 4 characters)
- Max input text characters: 2,048
- Price: Free
- Hosted by TiDB Cloud: ✅ `tidbcloud_free/cohere/embed-english-v3`
- Bring Your Own Key: ✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 model**

- Name: `tidbcloud_free/cohere/embed-multilingual-v3`
- Dimensions: 1024
- Distance Metric: Cosine / L2
- Languages: 100+ languages
- Max input text tokens: 512 (1 token is about 4 characters)
- Max input text characters: 2,048
- Price: Free
- Hosted by TiDB Cloud: ✅ `tidbcloud_free/cohere/embed-multilingual-v3`
- Bring Your Own Key: ✅ `cohere/embed-multilingual-v3.0`

Alternatively, all Cohere models are available for use under the `cohere/` prefix when you bring your own Cohere API key. To name a few:

**Cohere Embed v4 model**

- Name: `cohere/embed-v4.0`
- Dimensions: 256, 512, 1024, 1536 (default)
- Distance Metric: Cosine / L2
- Max input text tokens: 128k
- Price: Charged by Cohere
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of Cohere models, please refer to [Cohere's Documentation](https://docs.cohere.com/docs/cohere-embed).

## Availability

This feature is currently available in these regions and offerings:

- Starter: AWS Frankfurt (eu-central-1)
- Starter: AWS Oregon (us-west-2)
- Starter: AWS N. Virginia (us-east-1)

## SQL Usage Example (TiDB Cloud Hosted)

Create table:

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/cohere/embed-multilingual-v3",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

> **Note**:
>
> For the Cohere model, you must specify `input_type` in the `EMBED_TEXT()` function. For example, `'{"input_type": "search_document", "input_type@search": "search_query"}'` means that `input_type` is set to `search_document` for data insertion and `search_query` for vector searches.
>
> The `@search` suffix is used to mark that field to take effect only when it is used for vector search queries.

Insert and query data:

```sql
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

Result:

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## Options (TiDB Cloud Hosted)

Both the Embed v3 and Multilingual Embed v3 models support the following options, which you can specify via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

- `input_type` – **Required**. Prepends special tokens to differentiate each type from one another. You should not mix different types together, except when mixing types for search and retrieval. In this case, embed your corpus with the `search_document` type and embed queries with the `search_query` type.

  - `search_document` – In search use-cases, use `search_document` when you encode documents for embeddings that you store in a vector database.
  - `search_query` – Use `search_query` when querying your vector DB to find relevant documents.
  - `classification` – Use `classification` when using embeddings as an input to a text classifier.
  - `clustering` – Use `clustering` to cluster the embeddings.

- `truncate` - (optional) Specifies how the API handles inputs longer than the maximum token length. Use one of the following:

  - `NONE` – (Default) Returns an error when the input exceeds the maximum input token length.
  - `START` – Discards the start of the input.
  - `END` – Discards the end of the input.

  If you specify `START` or `END`, the model discards the input until the remaining input is exactly the maximum input token length for the model.

## SQL Usage Example (BYOK)

To use BYOK Cohere models, a Cohere API key is required:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = 'your-cohere-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
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

> **Note**: Replace `'your-cohere-api-key-here'` with your actual Cohere API key. You can obtain an API key from the [Cohere Dashboard](https://dashboard.cohere.com/).

## Options (BYOK)

All [Cohere embedding options](https://docs.cohere.com/v2/reference/embed) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify different `input_type` for Search vs Insert**

The `@search` suffix can be used to mark any field to take effect only when it is used for vector search queries.

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

**Example: Use alternative dimensions**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"output_dimension": 512}'
              )) STORED
);
```

For all available options, please refer to [Cohere's Documentation](https://docs.cohere.com/v2/reference/embed).

## Python Usage Example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
