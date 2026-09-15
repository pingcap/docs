---
title: 刷新 NGRAM 索引
summary: "{{{ .lake }}} 在数据摄取时会自动刷新 NGRAM 索引。当你需要回填在索引定义之前已存在的数据时，请使用 REFRESH NGRAM INDEX。"
---

# 刷新 NGRAM 索引

{{{ .lake }}} 在数据摄取时会自动刷新 NGRAM 索引。当你需要回填在索引定义之前已存在的数据时，请使用 `REFRESH NGRAM INDEX`。

## 语法 {#syntax}

```sql
REFRESH NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## 示例 {#examples}

```sql
-- Table already populated before the NGRAM index exists
CREATE TABLE IF NOT EXISTS amazon_reviews_ngram(review_id INT, review STRING);
INSERT INTO amazon_reviews_ngram VALUES
  (1, 'coffee beans from Colombia'),
  (2, 'best roasting kit');

-- Declare the NGRAM index afterward
CREATE NGRAM INDEX idx1 ON amazon_reviews_ngram(review) WITH (ngram_size = 3);

-- Refresh so the pre-existing rows are indexed
REFRESH NGRAM INDEX idx1 ON amazon_reviews_ngram;

-- Subsequent inserts refresh automatically in SYNC mode
```