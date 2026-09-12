---
title: LEAST
summary: 返回一组值中的最小值。如果该组中的任意值为 NULL，则该函数返回 NULL。
---

# LEAST

返回一组值中的最小值。如果该组中的任意值为 `NULL`，则该函数返回 `NULL`。

另请参阅：[LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md)

## 语法 {#syntax}

```sql
LEAST(<value1>, <value2> ...)
```

## 示例 {#examples}

```sql
SELECT LEAST(5, 9, 4), LEAST(5, 9, null);
```

```
┌────────────────────────────────────┐
│ least(5, 9, 4) │ least(5, 9, NULL) │
├────────────────┼───────────────────┤
│              4 │ NULL              │
└────────────────────────────────────┘
```