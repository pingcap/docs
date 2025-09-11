---
title: Cohere Embeddings
summary: 了解如何在 TiDB Cloud 中使用 Cohere 嵌入模型。
---

# Cohere Embeddings

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 使用 Cohere 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> 目前，[Auto Embedding](/tidb-cloud/vector-search-auto-embedding-overview.md) 仅在以下 AWS 区域的 TiDB Cloud Starter 集群中可用：
>
> - `Frankfurt (eu-central-1)`
> - `Oregon (us-west-2)`
> - `N. Virginia (us-east-1)`

## 可用模型

TiDB Cloud 原生提供以下 [Cohere](https://cohere.com/) 嵌入模型。无需 API key。

**Cohere Embed v3 model**

- 名称：`tidbcloud_free/cohere/embed-english-v3`
- 维度：1024
- 距离度量：Cosine, L2
- 语言：英语
- 最大输入文本 token 数：512（每个 token 约 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-english-v3`
- 自带密钥（BYOK）：✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 model**

- 名称：`tidbcloud_free/cohere/embed-multilingual-v3`
- 维度：1024
- 距离度量：Cosine, L2
- 语言：100+ 种语言
- 最大输入文本 token 数：512（每个 token 约 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-multilingual-v3`
- 自带密钥（BYOK）：✅ `cohere/embed-multilingual-v3.0`

另外，如果你自带 Cohere API key（BYOK），可以使用所有带有 `cohere/` 前缀的 Cohere 模型。例如：

**Cohere Embed v4 model**

- 名称：`cohere/embed-v4.0`
- 维度：256、512、1024、1536（默认）
- 距离度量：Cosine, L2
- 最大输入文本 token 数：128,000
- 价格：由 Cohere 收费
- 由 TiDB Cloud 托管：❌
- 自带密钥（BYOK）：✅

完整的 Cohere 模型列表请参见 [Cohere Documentation](https://docs.cohere.com/docs/cohere-embed)。

## SQL 使用示例（TiDB Cloud 托管）

以下示例展示了如何结合 Auto Embedding 使用 TiDB Cloud 托管的 Cohere 嵌入模型。

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

> **Note:**
>
> - 对于 Cohere 嵌入模型，在定义表时必须在 `EMBED_TEXT()` 函数中指定 `input_type`。例如，`'{"input_type": "search_document", "input_type@search": "search_query"}'` 表示插入数据时 `input_type` 设置为 `search_document`，在向量搜索时会自动应用 `search_query`。
>
> - `@search` 后缀表示该字段仅在向量搜索查询时生效，因此在查询时无需再次指定 `input_type`。

插入和查询数据：

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

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 选项（TiDB Cloud 托管）

**Embed v3** 和 **Multilingual Embed v3** 模型均支持以下选项，你可以通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行指定。

- `input_type`（必填）：在嵌入前添加特殊 token 以指示嵌入用途。对于同一任务，生成嵌入时必须始终使用相同的 input type，否则嵌入会被映射到不同的语义空间，导致不兼容。唯一的例外是语义搜索，文档使用 `search_document`，查询使用 `search_query`。
    - `search_document`：从文档生成嵌入，用于存储到向量数据库。
    - `search_query`：从查询生成嵌入，用于在向量数据库中检索已存储的嵌入。
    - `classification`：生成嵌入，作为文本分类器的输入。
    - `clustering`：生成嵌入，用于聚类任务。

- `truncate`（可选）：控制 API 如何处理超过最大 token 长度的输入。可选值如下：

    - `NONE`（默认）：当输入超过最大 token 长度时返回错误。
    - `START`：从开头截断文本，直到输入符合要求。
    - `END`：从结尾截断文本，直到输入符合要求。

## SQL 使用示例（BYOK）

如需使用自带密钥（BYOK）的 Cohere 模型，必须按如下方式指定 Cohere API key：

> **Note**
>
> 请将 `'your-cohere-api-key-here'` 替换为你的实际 Cohere API key。你可以在 [Cohere Dashboard](https://dashboard.cohere.com/) 获取 API key。

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

## 选项（BYOK）

所有 [Cohere embedding options](https://docs.cohere.com/v2/reference/embed) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为搜索和插入操作分别指定不同的 `input_type`**

使用 `@search` 后缀表示该字段仅在向量搜索查询时生效。

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

**示例：使用不同的维度**

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

所有可用选项请参见 [Cohere Documentation](https://docs.cohere.com/v2/reference/embed)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding Overview](/tidb-cloud/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)
