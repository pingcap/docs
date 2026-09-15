---
title: BITMAP_MIN
summary: 获取 bitmap 中的最小值。
---

# BITMAP_MIN

获取 bitmap 中的最小值。

## 语法 {#syntax}

```sql
BITMAP_MIN( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_MIN(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────┐
│ bitmap_min(build_bitmap([1, 4, 5])) │
├─────────────────────────────────────┤
│                                   1 │
└─────────────────────────────────────┘
```