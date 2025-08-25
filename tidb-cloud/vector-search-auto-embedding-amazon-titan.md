---
title: Amazon Titan Embeddings
summary: Learn how to use Amazon Titan embedding models in TiDB Cloud.
aliases: ["/tidb/stable/vector-search-auto-embedding-amazon-titan"]
---

# Amazon Titan Embeddings

This document describes how to use Amazon Titan embedding models with [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> Currently, [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters in the following AWS regions:
>
> - `Frankfurt (eu-central-1)`
> - `Oregon (us-west-2)`
> - `N. Virginia (us-east-1)`

## Available models

TiDB Cloud provides the following [Amazon Titan embedding model](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html) natively. No API key is required.

**Amazon Titan Text Embedding V2 model**

- Name: `tidbcloud_free/amazon/titan-embed-text-v2`
- Dimensions: 1024 (default), 512, 256
- Distance metric: Cosine / L2
- Languages: English (100+ languages in preview)
- Typical use cases: RAG, document search, reranking, and classification
- Maximum input text tokens: 8,192
- Maximum input text characters: 50,000
- Price: Free
- Hosted by TiDB Cloud: ✅
- Bring Your Own Key: ❌

For more information about this model, see [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html).

## SQL usage example

The following example shows how to use the Amazon Titan embedding model with Auto Embedding.

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

You can specify the following options via the `additional_json_options` parameter of the `EMBED_TEXT()` function:

- `normalize` (optional): whether to normalize the output embedding. Defaults to `true`.
- `dimensions` (optional): the number of dimensions of the output embedding. Supported values: `1024` (default), `512`, and `256`.

**Example: Use an alternative dimension**

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

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
