---
title: BITMAP_AND
summary: 对两个位图执行按位与运算。
---

# BITMAP_AND

对两个位图执行按位与运算。

## 语法 {#syntax}

```sql
BITMAP_AND( <bitmap1>, <bitmap2> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_AND(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([4,5]))::String;

┌───────────────────────────────────────────────────────────────────┐
│ bitmap_and(build_bitmap([1, 4, 5]), build_bitmap([4, 5]))::string │
├───────────────────────────────────────────────────────────────────┤
│ 4,5                                                               │
└───────────────────────────────────────────────────────────────────┘
```