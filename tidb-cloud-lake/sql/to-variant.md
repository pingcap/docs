---
title: TO_VARIANT
summary: 値を VARIANT データ型に変換します。
---

# TO_VARIANT

値を VARIANT データ型に変換します。

## 構文 {#syntax}

```sql
TO_VARIANT( <expr> )
```

## 例 {#examples}

```sql
SELECT TO_VARIANT(TO_BITMAP('100,200,300'));

┌──────────────────────────────────────┐
│ to_variant(to_bitmap('100,200,300')) │
├──────────────────────────────────────┤
│ [100,200,300]                        │
└──────────────────────────────────────┘
```