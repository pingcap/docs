---
title: OpenAI Embeddings
summary: Learn how to use OpenAI embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-openai"]
---

# OpenAI Embeddings

All OpenAI models are available for use under the `openai/` prefix when you bring your own OpenAI API key. To name a few:

**text-embedding-3-small**

- Name: `openai/text-embedding-3-small`
- Dimensions: 512 - 1536 (default: 1536)
- Distance Metric: Cosine / L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**text-embedding-3-large**

- Name: `openai/text-embedding-3-large`
- Dimensions: 256 - 3072 (default: 3072)
- Distance Metric: Cosine / L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, please refer to [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings).

## SQL Usage Example

To use OpenAI models, an [OpenAI API key](https://platform.openai.com/api-keys) is required:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-small",
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

> **Note**: Replace `'your-openai-api-key-here'` with your actual OpenAI API key.

## Options

All [OpenAI embedding options](https://platform.openai.com/docs/api-reference/embeddings/create) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Use alternative dimensions for text-embedding-3-large**

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

For all available options, please refer to [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create).

## Python Usage Example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
