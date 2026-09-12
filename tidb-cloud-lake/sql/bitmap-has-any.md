---
title: BITMAP_HAS_ANY
summary: 检查第一个 bitmap 是否包含与第二个 bitmap 中任意位匹配的位。
---

# BITMAP_HAS_ANY

检查第一个 bitmap 是否包含与第二个 bitmap 中任意位匹配的位。

## 语法 {#syntax}

```sql
BITMAP_HAS_ANY( <bitmap1>, <bitmap2> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_HAS_ANY(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([1,2]));

┌───────────────────────────────────────────────────────────────┐
│ bitmap_has_any(build_bitmap([1, 4, 5]), build_bitmap([1, 2])) │
├───────────────────────────────────────────────────────────────┤
│ true                                                          │
└───────────────────────────────────────────────────────────────┘
```