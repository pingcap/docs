---
title: TO_FLOAT32
summary: 値を FLOAT32 データ型に変換します。
---

# TO_FLOAT32

値を FLOAT32 データ型に変換します。

## 構文 {#syntax}

```sql
TO_FLOAT32( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_FLOAT32('1.2');

┌───────────────────┐
│ to_float32('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```