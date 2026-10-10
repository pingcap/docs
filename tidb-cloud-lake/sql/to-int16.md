---
title: TO_INT16
summary: 値を INT16 データ型に変換します。
---

# TO_INT16

値を INT16 データ型に変換します。

## 構文 {#syntax}

```sql
TO_INT16( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_INT16('123');

┌─────────────────┐
│ to_int16('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```