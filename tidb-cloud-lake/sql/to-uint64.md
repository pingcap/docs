---
title: TO_UINT64
summary: 値を UINT64 データ型に変換します。
---

# TO_UINT64

値を UINT64 データ型に変換します。

## 構文 {#syntax}

```sql
TO_UINT64( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_UINT64('123');

┌──────────────────┐
│ to_uint64('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```