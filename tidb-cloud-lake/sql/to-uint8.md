---
title: TO_UINT8
summary: 値を UINT8 データ型に変換します。
---

# TO_UINT8

値を UINT8 データ型に変換します。

## 構文 {#syntax}

```sql
TO_UINT8( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_UINT8('123');

┌─────────────────┐
│ to_uint8('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```