---
title: NVIDIA NIM Embeddings
summary: Learn how to use NVIDIA NIM embedding models in TiDB Cloud.
---

# NVIDIA NIM Embeddings

This document describes how to use NVIDIA NIM embedding models with [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> Currently, [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters in the following AWS regions:
>
> - `Frankfurt (eu-central-1)`
> - `Oregon (us-west-2)`
> - `N. Virginia (us-east-1)`

## Available models

Embedding models hosted on NVIDIA NIM are available for use with the `nvidia_nim/` prefix if you bring your own [NVIDIA NIM API key](https://build.nvidia.com/settings/api-keys) (BYOK).

For your convenience, the following section takes a popular model as an example to show how to use it with Auto Embedding. For a full list of available models, see [NVIDIA NIM Text-to-embedding Models](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding).

## bge-m3

- Name: `nvidia_nim/baai/bge-m3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 8,192
- Price: Charged by NVIDIA
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Docs: https://docs.api.nvidia.com/nim/reference/baai-bge-m3

Example:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = 'your-nvidia-nim-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "nvidia_nim/baai/bge-m3",
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

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
