---
title: TO_BITMAP
summary: 値を BITMAP データ型に変換します。
---

# TO_BITMAP

値を BITMAP データ型に変換します。

## 構文 {#syntax}

```sql
TO_BITMAP( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_BITMAP('1101');

┌───────────────────┐
│ to_bitmap('1101') │
├───────────────────┤
│ <bitmap binary>   │
└───────────────────┘
```