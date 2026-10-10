---
title: REFRESH NGRAM INDEX
summary: "{{{ .lake }}} は、データが取り込まれると自動的に NGRAM インデックスを更新します。インデックスが定義される前から存在していたデータをバックフィルする必要がある場合は、REFRESH NGRAM INDEX を使用します。"
---

# REFRESH NGRAM INDEX

{{{ .lake }}} は、データが取り込まれると自動的に NGRAM インデックスを更新します。インデックスが定義される前から存在していたデータをバックフィルする必要がある場合は、`REFRESH NGRAM INDEX` を使用します。

## 構文 {#syntax}

```sql
REFRESH NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## 例 {#examples}

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