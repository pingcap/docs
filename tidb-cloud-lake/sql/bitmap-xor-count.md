---
title: BITMAP_XOR_COUNT
summary: 通过执行逻辑 XOR（异或）运算，统计 bitmap 中值为 1 的位数。
---

# BITMAP_XOR_COUNT

通过执行逻辑 XOR（异或）运算，统计 bitmap 中值为 1 的位数。

## 语法 {#syntax}

```sql
BITMAP_XOR_COUNT( <bitmap> )
```

## 示例 {#examples}

```sql
SELECT BITMAP_XOR_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_xor_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```