---
title: DROP INVERTED INDEX
summary: "{{{ .lake }}} の inverted index を削除します。"
---

# DROP INVERTED INDEX

{{{ .lake }}} の inverted index を削除します。

## 構文 {#syntax}

```sql
DROP INVERTED INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## 例 {#examples}

```sql
-- Drop the inverted index 'customer_feedback_idx' on the 'customer_feedback' table
DROP INVERTED INDEX customer_feedback_idx ON customer_feedback;
```