---
title: BITMAP_TO_ARRAY
summary: 将 Bitmap 转换为 Array。
---

# BITMAP_TO_ARRAY

将 Bitmap 转换为 Array。

## 语法 {#syntax}

```sql
BITMAP_TO_ARRAY( <bitmap> )
```

## 返回类型 {#return-type}

`Array (UInt64)`

## 示例 {#examples}

```sql
SELECT BITMAP_TO_ARRAY(TO_BITMAP('1, 3, 5'));

╭───────────────────────────────────────╮
│ bitmap_to_array(to_bitmap('1, 3, 5')) │
├───────────────────────────────────────┤
│ [1,3,5]                               │
╰───────────────────────────────────────╯
```