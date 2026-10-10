---
title: TO_FLOAT64
summary: 値を FLOAT64 データ型に変換します。
---

# TO_FLOAT64

値を FLOAT64 データ型に変換します。

## 構文 {#syntax}

```sql
TO_FLOAT64( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_FLOAT64('1.2');

┌───────────────────┐
│ to_float64('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```