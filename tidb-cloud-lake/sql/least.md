---
title: LEAST
summary: 値の集合から最小値を返します。集合内のいずれかの値が NULL の場合、この関数は NULL を返します。
---

# LEAST

値の集合から最小値を返します。集合内のいずれかの値が `NULL` の場合、この関数は `NULL` を返します。

関連情報: [LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md)

## 構文 {#syntax}

```sql
LEAST(<value1>, <value2> ...)
```

## 例 {#examples}

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