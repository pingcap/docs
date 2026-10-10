---
title: GREATEST
summary: 値の集合から最大値を返します。集合内のいずれかの値が NULL の場合、この関数は NULL を返します。
---

# GREATEST

値の集合から最大値を返します。集合内のいずれかの値が `NULL` の場合、この関数は `NULL` を返します。

関連情報: [GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md)

## 構文 {#syntax}

```sql
GREATEST(<value1>, <value2> ...)
```

## 例 {#examples}

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