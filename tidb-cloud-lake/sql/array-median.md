---
title: ARRAY_MEDIAN
summary: 返回数组中数值的中位数。`NULL` 元素会被忽略。
---

# ARRAY_MEDIAN

返回数组中数值的中位数。`NULL` 元素会被忽略。

## 语法 {#syntax}

```sql
ARRAY_MEDIAN(<array>)
```

## 返回类型 {#return-type}

数值类型。对于偶数长度的输入，结果是中间两个值的平均值。

## 示例 {#examples}

```sql
SELECT ARRAY_MEDIAN([1, 3, 2, 4]) AS med_even;

┌────────┐
│ med_even │
├────────┤
│    2.5 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([1, 3, 5]) AS med_odd;

┌────────┐
│ med_odd│
├────────┤
│    3.0 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([NULL, 10, 20, 30]) AS med_null;

┌────────┐
│ med_null│
├────────┤
│   20.0 │
└────────┘
```