---
title: BITMAP_OR
summary: 对两个位图执行按位 OR 运算。
---

# BITMAP_OR

对两个位图执行按位 OR 运算。

## 语法 {#syntax}

```sql
BITMAP_OR( <bitmap1>, <bitmap2> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_OR(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([6,7]))::String;

┌──────────────────────────────────────────────────────────────────┐
│ bitmap_or(build_bitmap([1, 4, 5]), build_bitmap([6, 7]))::string │
├──────────────────────────────────────────────────────────────────┤
│ 1,4,5,6,7                                                        │
└──────────────────────────────────────────────────────────────────┘
```