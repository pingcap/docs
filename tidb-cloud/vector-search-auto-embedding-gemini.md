---
title: Gemini Embeddings
summary: Learn how to use Google Gemini embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-gemini"]
---

# Gemini Embeddings

All Gemini models are available for use under the `gemini/` prefix when you bring your own Gemini API key.

**gemini-embedding-001**

- Name: `gemini/gemini-embedding-001`
- Dimensions: 128–3072 (default: 3072)
- Distance Metric: Cosine / L2
- Max input text tokens: 2048
- Price: Charged by Google
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, please refer to [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## Availability

This feature is currently available in these regions and offerings:

- Starter: AWS Frankfurt (eu-central-1)
- Starter: AWS Oregon (us-west-2)
- Starter: AWS N. Virginia (us-east-1)

## SQL Usage Example

To use Gemini models, a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) is required:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = 'your-gemini-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
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

> **Note**: Replace `'your-gemini-api-key-here'` with your actual Gemini API key.

## Options

All [Gemini options](https://ai.google.dev/gemini-api/docs/embeddings) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify task type to improve quality**

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

**Example: Use alternative dimensions**

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

For all available options, please refer to [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## Python Usage Example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
