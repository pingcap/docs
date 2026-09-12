---
title: REFRESH INVERTED INDEX
summary: "{{{ .lake }}} 会在写入新数据时自动刷新 `SYNC` 模式的倒排索引。`REFRESH INVERTED INDEX` 主要用于回填在声明索引之前已存在的行。"
---

# REFRESH INVERTED INDEX

{{{ .lake }}} 会在写入新数据时自动刷新 `SYNC` 模式的倒排索引。`REFRESH INVERTED INDEX` 主要用于回填在声明索引之前已存在的行。

## 语法 {#syntax}

```sql
REFRESH INVERTED INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| 参数 | 描述 |
|-----------|----------------------------------------------------------------------------------------------------------------------------------|
| `<limit>` | 指定索引刷新期间要处理的最大行数。如果未指定，则会处理表中的所有行。 |

## 示例 {#examples}

```sql
-- Existing table with data loaded before the index was declared
CREATE TABLE IF NOT EXISTS customer_feedback(id INT, body STRING);
INSERT INTO customer_feedback VALUES
  (1, 'Great coffee beans'),
  (2, 'Needs fresh roasting');

-- Create the inverted index afterward
CREATE INVERTED INDEX customer_feedback_idx ON customer_feedback(body);

-- Backfill historical rows so the index covers earlier inserts
REFRESH INVERTED INDEX customer_feedback_idx ON customer_feedback;

-- Future inserts refresh automatically in SYNC mode
```