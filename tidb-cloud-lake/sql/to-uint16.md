---
title: TO_UINT16
summary: 値を UINT16 データ型に変換します。
---

# TO_UINT16

値を UINT16 データ型に変換します。

## 構文 {#syntax}

```sql
TO_UINT16( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_UINT16('123');

┌──────────────────┐
│ to_uint16('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```