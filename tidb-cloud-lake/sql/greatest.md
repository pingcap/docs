---
title: GREATEST
summary: 返回一组值中的最大值。如果集合中的任意值为 NULL，则该函数返回 NULL。
---

# GREATEST

返回一组值中的最大值。如果集合中的任意值为 `NULL`，则该函数返回 `NULL`。

另请参阅：[GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md)

## 语法 {#syntax}

```sql
GREATEST(<value1>, <value2> ...)
```

## 示例 {#examples}

```sql
SELECT GREATEST(5, 9, 4), GREATEST(5, 9, null);
```

```sql
┌──────────────────────────────────────────┐
│ greatest(5, 9, 4) │ greatest(5, 9, NULL) │
├───────────────────┼──────────────────────┤
│                 9 │ NULL                 │
└──────────────────────────────────────────┘
```