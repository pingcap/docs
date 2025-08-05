---
title: Jina AI Embeddings
summary: Learn how to use Jina AI embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-jina-ai"]
---

# Jina AI Embeddings

All Jina AI models are available for use under the `jina_ai/` prefix when you bring your own Jina AI API key. To name a few:

**jina-embeddings-v4**

- Name: `jina_ai/jina-embeddings-v4`
- Dimensions: 2048
- Distance Metric: Cosine / L2
- Max input text tokens: 32K
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**jina-embeddings-v3**

- Name: `jina_ai/jina-embeddings-v3`
- Dimensions: 1024
- Distance Metric: Cosine / L2
- Max input text tokens: 8K
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, please refer to [Jina AI Documentation](https://jina.ai/embeddings/).

## SQL Usage Example

To use Jina AI models, a [Jina AI API key](https://jina.ai/) is required:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = 'your-jina-ai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
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

Result:

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

> **Note**: Replace `'your-jina-ai-api-key-here'` with your actual Jina AI API key.

## Options

All [Jina AI options](https://jina.ai/embeddings/) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify "downstream task" for better performance**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
                `content`,
                '{"task": "retrieval.passage", "task@search": "retrieval.query"}'
              )) STORED
);
```

**Example: Use alternative dimensions**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v3",
                `content`,
                '{"dimensions":768}'
              )) STORED
);
```

For all available options, please refer to [Jina AI Documentation](https://jina.ai/embeddings/).

## Python Usage Example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
