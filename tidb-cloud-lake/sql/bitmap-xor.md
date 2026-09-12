---
title: BITMAP_XOR
summary: 对两个位图执行按位 XOR（异或）运算。
---

# BITMAP_XOR

对两个位图执行按位 XOR（异或）运算。

## 语法 {#syntax}

```sql
BITMAP_XOR( <bitmap1>, <bitmap2> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_XOR(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([5,6,7]))::String;

┌──────────────────────────────────────────────────────────────────────┐
│ bitmap_xor(build_bitmap([1, 4, 5]), build_bitmap([5, 6, 7]))::string │
├──────────────────────────────────────────────────────────────────────┤
│ 1,4,6,7                                                              │
└──────────────────────────────────────────────────────────────────────┘
```