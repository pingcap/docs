---
title: TO_INT64
summary: 値を INT64 データ型に変換します。
---

# TO_INT64

値を INT64 データ型に変換します。

## 構文 {#syntax}

```sql
TO_INT64( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_INT64('123');

┌─────────────────┐
│ to_int64('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```