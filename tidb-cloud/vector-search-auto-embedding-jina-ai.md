---
title: Jina AI Embeddings
summary: 了解如何在 TiDB Cloud 中使用 Jina AI 嵌入模型。
---

# Jina AI Embeddings

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 使用 Jina AI 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> 目前，[Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 仅在以下 AWS 区域的 TiDB Cloud Starter 集群中可用：
>
> - `Frankfurt (eu-central-1)`
> - `Oregon (us-west-2)`
> - `N. Virginia (us-east-1)`

## 可用模型

如果你自带 Jina AI API key（BYOK），所有 Jina AI 模型均可通过 `jina_ai/` 前缀使用。例如：

**jina-embeddings-v4**

- 名称：`jina_ai/jina-embeddings-v4`
- 维度：2048
- 距离度量：Cosine，L2
- 最大输入文本 tokens：32,768
- 价格：由 Jina AI 收费
- 由 TiDB Cloud 托管：❌
- 自带密钥：✅

**jina-embeddings-v3**

- 名称：`jina_ai/jina-embeddings-v3`
- 维度：1024
- 距离度量：Cosine，L2
- 最大输入文本 tokens：8,192
- 价格：由 Jina AI 收费
- 由 TiDB Cloud 托管：❌
- 自带密钥：✅

完整可用模型列表请参见 [Jina AI Documentation](https://jina.ai/embeddings/)。

## SQL 使用示例

要使用 Jina AI 模型，你必须按如下方式指定 [Jina AI API key](https://jina.ai/)：

> **Note:**
>
> 请将 `'your-jina-ai-api-key-here'` 替换为你实际的 Jina AI API key。

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

所有 [Jina AI options](https://jina.ai/embeddings/) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行支持。

**示例：为更好的性能指定 "downstream task"**

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

**示例：使用其他维度**

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

所有可用选项请参见 [Jina AI Documentation](https://jina.ai/embeddings/)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/integrations/embedding-jinaai/)。

## 参见

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
