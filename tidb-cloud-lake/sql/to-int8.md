---
title: TO_INT8
summary: 値を INT8 データ型に変換します。
---

# TO_INT8

値を INT8 データ型に変換します。

## 構文 {#syntax}

```sql
TO_INT8( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_INT8('123');

┌────────────────┐
│ to_int8('123') │
│      UInt8     │
├────────────────┤
│            123 │
└────────────────┘
```