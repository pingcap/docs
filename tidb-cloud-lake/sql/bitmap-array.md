---
title: BITMAP_TO_ARRAY
summary: Bitmap を Array に変換します。
---

# BITMAP_TO_ARRAY

Bitmap を Array に変換します。

## 構文 {#syntax}

```sql
BITMAP_TO_ARRAY( <bitmap> )
```

## 戻り値の型 {#return-type}

`Array (UInt64)`

## 例 {#examples}

```sql
SELECT BITMAP_TO_ARRAY(TO_BITMAP('1, 3, 5'));

╭───────────────────────────────────────╮
│ bitmap_to_array(to_bitmap('1, 3, 5')) │
├───────────────────────────────────────┤
│ [1,3,5]                               │
╰───────────────────────────────────────╯
```