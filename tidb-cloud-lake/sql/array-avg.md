---
title: ARRAY_AVG
summary: 返回数组中数值项的平均值。`NULL` 元素会被忽略；非数值会引发错误。
---

# ARRAY_AVG

返回数组中数值项的平均值。`NULL` 元素会被忽略；非数值会引发错误。

## 语法 {#syntax}

```sql
ARRAY_AVG(<array>)
```

## 返回类型 {#return-type}

数值型（使用能够表示结果的最小数值类型）。

## 示例 {#examples}

```sql
SELECT ARRAY_AVG([1, 2, 3, 4]) AS avg_int;

┌─────────┐
│ avg_int │
├─────────┤
│     2.5 │
└─────────┘
```

```sql
SELECT ARRAY_AVG([1.5, 2.5, 3.5]) AS avg_decimal;

┌──────────────┐
│ avg_decimal  │
├──────────────┤
│       2.5000 │
└──────────────┘
```

```sql
SELECT ARRAY_AVG([10, NULL, 4]) AS avg_with_null;

┌──────────────┐
│ avg_with_null│
├──────────────┤
│          7.0 │
└──────────────┘
```