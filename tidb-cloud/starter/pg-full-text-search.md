---
title: Full-Text Search
summary: Learn how to use PostgreSQL-compatible full-text search on PostgreSQL-compatible TiDB Cloud Starter.
---

# Full-Text Search

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL-compatible full-text search with `tsvector`, `tsquery`, language-specific tokenizers, ranking functions, and GIN indexes.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in Limited Public Preview.

Full-text search is built in and does not require installing a separate extension. Chinese tokenization is also available through `zhparser`-compatible configurations.

## Supported text search configurations

The following text search configurations are supported:

| Configuration | Aliases | Description |
| --- | --- | --- |
| `jieba` | `chinese`, `zhparser` | Chinese word segmentation. |
| `chinese_ngram` | `zhparser_ngram` | Chinese word segmentation with a bigram overlay for multi-character words. |
| `simple` | - | Whitespace tokenization for English and Latin text, without stemming or stopword removal. |
| `english` | - | Whitespace tokenization with a minimal stopword list. Does not perform stemming. |
| `english_stem` | - | English Snowball stemming with PostgreSQL-compatible English stopwords. |

The default text search configuration is `simple`.

You can check the current default configuration using:

```sql
SHOW default_text_search_config;
```

> **Note:**
>
> Unlike PostgreSQL, the `english` configuration does not perform stemming. Use `english_stem` when you need stemmed English search.

## Create a GIN index for full-text search

GIN indexes can accelerate full-text search queries.

Create a GIN index on a `tsvector` column:

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

You can also create a GIN expression index:

```sql
CREATE INDEX idx_documents_content_fts
ON documents
USING GIN (to_tsvector('simple', content));
```

When the expression used by the `@@` operator matches the indexed expression, the optimizer can use the GIN index automatically.

## Search English text

Use `simple` for exact token matching:

```sql
CREATE INDEX idx_documents_simple
ON documents
USING GIN (to_tsvector('simple', content));

SELECT *
FROM documents
WHERE to_tsvector('simple', content)
      @@ to_tsquery('simple', 'database');
```

Use `english_stem` when you need stemming and stopword removal:

```sql
CREATE INDEX idx_documents_english
ON documents
USING GIN (to_tsvector('english_stem', content));

SELECT *
FROM documents
WHERE to_tsvector('english_stem', content)
      @@ plainto_tsquery('english_stem', 'running');
```

Use the same text search configuration in the index expression and the search query.

## Search Chinese text

Use the `jieba` configuration for Chinese tokenization.

For example:

```sql
CREATE INDEX idx_documents_chinese
ON documents
USING GIN (to_tsvector('jieba', content));

SELECT *
FROM documents
WHERE to_tsvector('jieba', content)
      @@ plainto_tsquery('jieba', '数据库');
```

The aliases `chinese` and `zhparser` use the same Chinese tokenization capability.

## Query functions

PostgreSQL-compatible {{{ .starter }}} supports common PostgreSQL text-search query functions:

| Function | Description | Example |
| --- | --- | --- |
| `plainto_tsquery` | Converts plain text to a text-search query. | `plainto_tsquery('simple', 'database search')` |
| `to_tsquery` | Creates a query using PostgreSQL text-search operators. | `to_tsquery('simple', 'database & search')` |
| `phraseto_tsquery` | Creates a phrase query. | `phraseto_tsquery('simple', 'hello world')` |
| `websearch_to_tsquery` | Creates a query using web-search-style syntax. | `websearch_to_tsquery('simple', '"exact phrase" -exclude')` |

## Boolean search

Use `to_tsquery()` for Boolean search expressions:

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

## Rank search results

Use `ts_rank()` to rank matching documents.

For example:

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

## Search with weights

Use `setweight()` to assign different weights to different fields.

For example:

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    body TEXT,
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

## Limitations

The following limitations apply during the Limited Public Preview:

- Only the text search configurations listed in [Supported text search configurations](#supported-text-search-configurations) are supported.
- The `english` configuration does not perform PostgreSQL-style stemming. Use `english_stem` for stemmed English search.
- Prefix matching using the `:*` flag is not supported. The prefix flag is ignored, so do not rely on expressions such as `to_tsquery('simple', 'data:*')` for prefix search.
- `ts_headline()` does not highlight Chinese Han-script search terms. If you need highlighting for Chinese search results, implement highlighting in the application layer.
- A scalar text-search function such as `plainto_tsquery()` cannot be used as a table expression in the `FROM` clause. Use a CTE or inline the function in the query instead.
- The maximum `tsvector` value size is 1 MiB.
