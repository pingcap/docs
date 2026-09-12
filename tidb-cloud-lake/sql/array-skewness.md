---
title: ARRAY_SKEWNESS
summary: 返回数组中数值的偏度。`NULL` 项会被忽略；非数值项会引发错误。
---

# ARRAY_SKEWNESS

返回数组中数值的偏度。`NULL` 项会被忽略；非数值项会引发错误。

## 语法 {#syntax}

```sql
ARRAY_SKEWNESS(<array>)
```

## 返回类型 {#return-type}

浮点型。

## 示例 {#examples}

```sql
SELECT ARRAY_SKEWNESS([1, 2, 3, 4]) AS skew;

┌──────┐
│ skew │
├──────┤
│    0 │
└──────┘
```

```sql
SELECT ARRAY_SKEWNESS([1.5, 2.5, 3.5, 4.5]) AS skew_decimal;

┌────────────┐
│ skew_decimal│
├────────────┤
│          0 │
└────────────┘
```

```sql
SELECT ARRAY_SKEWNESS([NULL, 2, 3, 10]) AS skew_null;

┌────────────────────┐
│ skew_null          │
├────────────────────┤
│ 1.6300591617118865 │
└────────────────────┘
```