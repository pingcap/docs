---
title: LEAST_IGNORE_NULLS
summary: NULL 値を無視して、一連の値の中から最大値を返します。
---

# LEAST_IGNORE_NULLS

NULL 値を無視して、一連の値の中から最大値を返します。

関連情報: [LEAST](/tidb-cloud-lake/sql/least.md)

## 構文 {#syntax}

```sql
LEAST_IGNORE_NULLS(<value1>, <value2> ...)
```

## 例 {#examples}

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