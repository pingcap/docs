---
title: DROP INVERTED INDEX
summary: 删除 {{{ .lake }}} 中的倒排索引。
---

# DROP INVERTED INDEX

删除 {{{ .lake }}} 中的倒排索引。

## 语法 {#syntax}

```sql
DROP INVERTED INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## 示例 {#examples}

```sql
-- Drop the inverted index 'customer_feedback_idx' on the 'customer_feedback' table
DROP INVERTED INDEX customer_feedback_idx ON customer_feedback;
```