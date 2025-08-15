---
title: Amazon Titan Embeddings
summary: Learn how to use Amazon Titan embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-amazon-titan"]
---

# Amazon Titan Embeddings

## Available Models

TiDB Cloud provides the following [Amazon Titan embedding model](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) natively. No API key required.

**Amazon Titan Text Embedding V2 model**

- Name: `tidbcloud_free/amazon/titan-embed-text-v2`
- Dimensions: 1024 (default), 512, 256
- Distance Metric: Cosine / L2
- Languages – English (100+ languages in preview)
- Supported use cases – RAG, document search, reranking, classification, etc.
- Max input text tokens: 8,192
- Max input text characters: 50,000
- Price: Free
- Hosted by TiDB Cloud: ✅
- Bring Your Own Key: ❌

For more details, see [its official documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html).

## SQL Usage Example

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
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

## Options

You can specify additional options via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

- `normalize` – (optional) Flag indicating whether or not to normalize the output embedding. Defaults to true.
- `dimensions` – (optional) The number of dimensions the output embedding should have. The following values are accepted: 1024 (default), 512, 256.

**Example: Use alternative dimensions via `dimensions`**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
                `content`,
                '{"dimensions": 512}'
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

## Python Usage Example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See Also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
