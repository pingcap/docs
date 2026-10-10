---
title: GREATEST_IGNORE_NULLS
summary: NULL 値を無視して、値の集合から最大値を返します。
---

# GREATEST_IGNORE_NULLS

NULL 値を無視して、値の集合から最大値を返します。

関連情報: [GREATEST](/tidb-cloud-lake/sql/greatest.md)

## 構文 {#syntax}

```sql
GREATEST_IGNORE_NULLS(<value1>, <value2> ...)
```

## 例 {#examples}

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