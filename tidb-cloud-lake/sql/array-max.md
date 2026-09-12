---
title: ARRAY_MAX
summary: 返回数组中的最大数值。`NULL` 元素会被跳过；非数值会导致错误。
---

# ARRAY_MAX

返回数组中的最大数值。`NULL` 元素会被跳过；非数值会导致错误。

## 语法 {#syntax}

```sql
ARRAY_MAX(<array>)
```

## 返回类型 {#return-type}

与数组元素相同的数值类型。

## 示例 {#examples}

```sql
SELECT ARRAY_MAX([5, 2, 9, -1]) AS max_int;

┌─────────┐
│ max_int │
├─────────┤
│       9 │
└─────────┘
```

```sql
SELECT ARRAY_MAX([1.5, -2.25, 3.0]) AS max_decimal;

┌─────────────┐
│ max_decimal │
├─────────────┤
│      3.00   │
└─────────────┘
```

```sql
SELECT ARRAY_MAX([NULL, 10, 4]) AS max_with_null;

┌───────────────┐
│ max_with_null │
├───────────────┤
│           10  │
└───────────────┘
```