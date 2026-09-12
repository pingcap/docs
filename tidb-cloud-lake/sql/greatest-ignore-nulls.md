---
title: GREATEST_IGNORE_NULLS
summary: 返回一组值中的最大值，并忽略任何 NULL 值。
---

# GREATEST_IGNORE_NULLS

返回一组值中的最大值，并忽略任何 NULL 值。

另请参阅：[GREATEST](/tidb-cloud-lake/sql/greatest.md)

## 语法 {#syntax}

```sql
GREATEST_IGNORE_NULLS(<value1>, <value2> ...)
```

## 示例 {#examples}

```sql
SELECT GREATEST_IGNORE_NULLS(5, 9, 4), GREATEST_IGNORE_NULLS(5, 9, null);
```

```sql
┌────────────────────────────────────────────────────────────────────┐
│ greatest_ignore_nulls(5, 9, 4) │ greatest_ignore_nulls(5, 9, NULL) │
├────────────────────────────────┼───────────────────────────────────┤
│                              9 │                                 9 │
└────────────────────────────────────────────────────────────────────┘
```