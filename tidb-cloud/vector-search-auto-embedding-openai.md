---
title: OpenAI Embeddings
summary: 了解如何在 TiDB Cloud 中使用 OpenAI 嵌入模型。
---

# OpenAI Embeddings

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 使用 OpenAI 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 OpenAI API 密钥（BYOK），则所有 OpenAI 模型均可通过 `openai/` 前缀使用。例如：

**text-embedding-3-small**

- 名称：`openai/text-embedding-3-small`
- 维度：512-1536（默认：1536）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- TiDB Cloud 托管：❌
- 支持自带密钥：✅

**text-embedding-3-large**

- 名称：`openai/text-embedding-3-large`
- 维度：256-3072（默认：3072）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- TiDB Cloud 托管：❌
- 支持自带密钥：✅

完整的可用模型列表，请参见 [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings)。

## SQL 使用示例

要使用 OpenAI 模型，你必须按如下方式指定 [OpenAI API key](https://platform.openai.com/api-keys)：

> **Note:**
>
> 请将 `'your-openai-api-key-here'` 替换为你实际的 OpenAI API 密钥。

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

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 选项

所有 [OpenAI embedding options](https://platform.openai.com/docs/api-reference/embeddings/create) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为 text-embedding-3-large 使用自定义维度**

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

所有可用选项请参见 [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
