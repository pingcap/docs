---
title: ARRAY_MIN
summary: 返回数组中的最小数值。`NULL` 元素会被跳过；非数值会导致错误。
---

# ARRAY_MIN

返回数组中的最小数值。`NULL` 元素会被跳过；非数值会导致错误。

## 语法 {#syntax}

```sql
ARRAY_MIN(<array>)
```

## 返回类型 {#return-type}

与数组元素相同的数值类型。

## 示例 {#examples}

```sql
SELECT ARRAY_MIN([5, 2, 9, -1]) AS min_int;

┌─────────┐
│ min_int │
├─────────┤
│      -1 │
└─────────┘
```

```sql
SELECT ARRAY_MIN([1.5, -2.25, 3.0]) AS min_decimal;

┌──────────────┐
│ min_decimal  │
├──────────────┤
│       -2.25  │
└──────────────┘
```

```sql
SELECT ARRAY_MIN([NULL, 10, 4]) AS min_with_null;

┌──────────────┐
│ min_with_null│
├──────────────┤
│            4 │
└──────────────┘
```