---
title: 全文搜索
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 上使用全文搜索。
---

# 全文搜索

兼容 PostgreSQL 的 {{{ .starter }}} 支持兼容 PostgreSQL 的全文搜索，包括 `tsvector`、`tsquery`、特定语言的分词器、排序函数和 GIN 索引。

> **Note:**
>
> 兼容 PostgreSQL 的 {{{ .starter }}} 当前处于公测阶段。

全文搜索为内置功能，无需安装单独的扩展。还可通过兼容 `zhparser` 的配置使用中文分词。

## 支持的文本搜索配置 {#supported-text-search-configurations}

支持以下文本搜索配置：

| 配置 | 别名 | 描述 |
| --- | --- | --- |
| `jieba` | `chinese`, `zhparser` | 中文分词。 |
| `chinese_ngram` | `zhparser_ngram` | 中文分词，并对多字符词叠加 bigram 切分。 |
| `simple` | - | 对英文和拉丁文本按空白字符分词，不进行词干提取或停用词移除。 |
| `english` | - | 按空白字符分词，并使用最小停用词列表。不进行词干提取。 |
| `english_stem` | - | 使用 English Snowball 词干提取，并采用兼容 PostgreSQL 的英文停用词。 |

默认的文本搜索配置为 `simple`。

你可以使用以下语句检查当前默认配置：

```sql
SHOW default_text_search_config;
```

> **Note:**
>
> 与 PostgreSQL 不同，`english` 配置不执行词干提取。如需对英文搜索执行词干提取，请使用 `english_stem`。

## 为全文搜索创建 GIN 索引 {#create-a-gin-index-for-full-text-search}

GIN 索引可以加速全文搜索查询。

在 `tsvector` 列上创建 GIN 索引：

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    tsv TSVECTOR
);

CREATE INDEX idx_documents_tsv
ON documents
USING GIN (tsv);
```

你也可以创建 GIN 表达式索引：

```sql
CREATE INDEX idx_documents_content_fts
ON documents
USING GIN (to_tsvector('simple', content));
```

当 `@@` 运算符使用的表达式与已建立索引的表达式匹配时，优化器可以自动使用 GIN 索引。

## 搜索英文文本 {#search-english-text}

使用 `simple` 进行精确 Token 匹配：

以下查询可以使用上一节中创建的 GIN 表达式索引，因为它使用了相同的 `to_tsvector('simple', content)` 表达式。

```sql
SELECT *
FROM documents
WHERE to_tsvector('simple', content)
      @@ to_tsquery('simple', 'database');
```

当你需要词干提取和停用词移除时，请使用 `english_stem`：

```sql
CREATE INDEX idx_documents_english
ON documents
USING GIN (to_tsvector('english_stem', content));

SELECT *
FROM documents
WHERE to_tsvector('english_stem', content)
      @@ plainto_tsquery('english_stem', 'running');
```

请在索引表达式和搜索查询中使用相同的文本搜索配置。

## 搜索中文文本 {#search-chinese-text}

使用 `jieba` 配置进行中文分词。

例如：

```sql
CREATE INDEX idx_documents_chinese
ON documents
USING GIN (to_tsvector('jieba', content));

SELECT *
FROM documents
WHERE to_tsvector('jieba', content)
      @@ plainto_tsquery('jieba', '数据库');
```

别名 `chinese` 和 `zhparser` 使用相同的中文分词能力。

## 查询函数 {#query-functions}

兼容 PostgreSQL 的 {{{ .starter }}} 支持常见的 PostgreSQL 文本搜索查询函数：

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `plainto_tsquery` | 将纯文本转换为文本搜索查询。 | `plainto_tsquery('simple', 'database search')` |
| `to_tsquery` | 使用 PostgreSQL 文本搜索运算符创建查询。 | `to_tsquery('simple', 'database & search')` |
| `phraseto_tsquery` | 创建短语查询。 | `phraseto_tsquery('simple', 'hello world')` |
| `websearch_to_tsquery` | 使用 Web 搜索风格的语法创建查询。 | `websearch_to_tsquery('simple', '"exact phrase" -exclude')` |

## 布尔搜索 {#boolean-search}

使用 `to_tsquery()` 编写布尔搜索表达式：

```sql
-- AND
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'database & performance');

-- OR
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'postgres | mysql');

-- NOT
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'database & !oracle');
```

## 对搜索结果排序 {#rank-search-results}

使用 `ts_rank()` 对匹配文档进行排序。

例如：

```sql
SELECT
    content,
    ts_rank(
        to_tsvector('jieba', content),
        plainto_tsquery('jieba', '数据库')
    ) AS rank
FROM documents
WHERE to_tsvector('jieba', content)
      @@ plainto_tsquery('jieba', '数据库')
ORDER BY rank DESC
LIMIT 10;
```

## 使用权重进行搜索 {#search-with-weights}

使用 `setweight()` 为不同字段分配不同权重。

例如：

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tsv TSVECTOR
);

UPDATE articles
SET tsv =
    setweight(to_tsvector('jieba', title), 'A') ||
    setweight(to_tsvector('jieba', body), 'B');

WITH q AS (
    SELECT plainto_tsquery('jieba', '数据库') AS query
)
SELECT
    a.title,
    ts_rank(a.tsv, q.query) AS rank
FROM articles AS a, q
WHERE a.tsv @@ q.query
ORDER BY rank DESC;
```

## 限制 {#limitations}

以下限制在公测期间适用：

- 仅支持[支持的文本搜索配置](#supported-text-search-configurations)中列出的文本搜索配置。
- `english` 配置不会执行 PostgreSQL 风格的词干提取。对于带词干提取的英文搜索，请使用 `english_stem`。
- 不支持使用 `:*` 参数进行前缀匹配。此前缀参数会被忽略，因此不要依赖 `to_tsquery('simple', 'data:*')` 这类表达式来执行前缀搜索。
- `ts_headline()` 不会高亮中文汉字搜索词。如果你需要对中文搜索结果进行高亮，请在应用 layer 实现高亮。
- 标量文本搜索函数（例如 `plainto_tsquery()`）不能在 `FROM` 子句中用作表表达式。请改用 CTE，或将该函数直接内联到查询中。
- `tsvector` 值的最大大小为 1 MiB。