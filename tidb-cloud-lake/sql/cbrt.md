---
title: CBRT
summary: 返回非负数 `x` 的立方根。
---

# CBRT

返回非负数 `x` 的立方根。

## 语法 {#syntax}

```sql
CBRT( <x> )
```

## 示例 {#examples}

```sql
SELECT CBRT(27);

┌──────────┐
│ cbrt(27) │
├──────────┤
│        3 │
└──────────┘
```