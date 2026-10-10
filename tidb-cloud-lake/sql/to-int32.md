---
title: TO_INT32
summary: 値を INT32 データ型に変換します。
---

# TO_INT32

値を INT32 データ型に変換します。

## 構文 {#syntax}

```sql
TO_INT32( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_INT32('123');

┌─────────────────┐
│ to_int32('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```