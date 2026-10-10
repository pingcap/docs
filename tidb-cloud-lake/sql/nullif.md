---
title: NULLIF
summary: 2 つの式が等しい場合は NULL を返します。それ以外の場合は expr1 を返します。これらは同じデータ型である必要があります。
---

# NULLIF

2 つの式が等しい場合は NULL を返します。それ以外の場合は expr1 を返します。これらは同じデータ型である必要があります。

## 構文 {#syntax}

```sql
NULLIF(<expr1>, <expr2>)
```

## 例 {#examples}

```sql
SELECT NULLIF(0, NULL);

┌─────────────────┐
│ nullif(0, null) │
├─────────────────┤
│               0 │
└─────────────────┘
```