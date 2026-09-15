---
title: LEAST_IGNORE_NULLS
summary: 返回一组值中的最大值，并忽略任何 NULL 值。
---

# LEAST_IGNORE_NULLS

返回一组值中的最大值，并忽略任何 NULL 值。

另请参阅：[LEAST](/tidb-cloud-lake/sql/least.md)

## 语法 {#syntax}

```sql
LEAST_IGNORE_NULLS(<value1>, <value2> ...)
```

## 示例 {#examples}

```sql
SELECT LEAST_IGNORE_NULLS(5, 9, 4), LEAST_IGNORE_NULLS(5, 9, null);
```

```sql
┌──────────────────────────────────────────────────────────────┐
│ least_ignore_nulls(5, 9, 4) │ least_ignore_nulls(5, 9, NULL) │
├─────────────────────────────┼────────────────────────────────┤
│                           4 │                              5 │
└──────────────────────────────────────────────────────────────┘
```