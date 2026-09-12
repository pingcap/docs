---
title: SQRT
summary: 返回非负数 `x` 的平方根。对于负数输入，返回 Nan。
---

# SQRT

返回非负数 `x` 的平方根。对于负数输入，返回 Nan。

## 语法 {#syntax}

```sql
SQRT( <x> )
```

## 示例 {#examples}

```sql
SELECT SQRT(4);

┌─────────┐
│ sqrt(4) │
├─────────┤
│       2 │
└─────────┘
```