---
title: DROP NGRAM INDEX
summary: テーブルから既存の NGRAM インデックスを削除します。
---

# DROP NGRAM INDEX

テーブルから既存の NGRAM インデックスを削除します。

## 構文 {#syntax}

```sql
DROP NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## 例 {#examples}

次の例では、`amazon_reviews_ngram` テーブルから `idx1` インデックスを削除します。

```sql
DROP NGRAM INDEX idx1 ON amazon_reviews_ngram;
```