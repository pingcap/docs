---
title: BITMAP_HAS_ALL
summary: 检查第一个位图是否包含第二个位图中的所有位。
---

# BITMAP_HAS_ALL

检查第一个位图是否包含第二个位图中的所有位。

## 语法 {#syntax}

```sql
BITMAP_HAS_ALL( <bitmap1>, <bitmap2> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_HAS_ALL(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([1,2]));

┌───────────────────────────────────────────────────────────────┐
│ bitmap_has_all(build_bitmap([1, 4, 5]), build_bitmap([1, 2])) │
├───────────────────────────────────────────────────────────────┤
│ false                                                         │
└───────────────────────────────────────────────────────────────┘
```