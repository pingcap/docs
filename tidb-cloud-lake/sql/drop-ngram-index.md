---
title: DROP NGRAM INDEX
summary: 从表中删除现有的 NGRAM 索引。
---

# DROP NGRAM INDEX

从表中删除现有的 NGRAM 索引。

## 语法 {#syntax}

```sql
DROP NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## 示例 {#examples}

以下示例从 `amazon_reviews_ngram` 表中删除 `idx1` 索引：

```sql
DROP NGRAM INDEX idx1 ON amazon_reviews_ngram;
```