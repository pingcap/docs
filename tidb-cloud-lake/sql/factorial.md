---
title: FACTORIAL
summary: 返回 `x` 的阶乘。如果 `x` 小于或等于 0，函数返回 0。
---

# FACTORIAL

返回 `x` 的阶乘。如果 `x` 小于或等于 0，函数返回 0。

## 语法 {#syntax}

```sql
FACTORIAL( <x> )
```

## 示例 {#examples}

```sql
SELECT FACTORIAL(5);

┌──────────────┐
│ factorial(5) │
├──────────────┤
│          120 │
└──────────────┘
```