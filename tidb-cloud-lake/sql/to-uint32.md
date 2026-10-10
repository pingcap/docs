---
title: TO_UINT32
summary: 値を UINT32 データ型に変換します。
---

# TO_UINT32

値を UINT32 データ型に変換します。

## 構文 {#syntax}

```sql
TO_UINT32( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_UINT32('123');

┌──────────────────┐
│ to_uint32('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```