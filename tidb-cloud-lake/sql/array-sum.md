---
title: ARRAY_SUM
summary: 对数组中的数值元素求和。`NULL` 项会被跳过，非数值会引发错误。
---

# ARRAY_SUM

对数组中的数值元素求和。`NULL` 项会被跳过，非数值会引发错误。

## 语法 {#syntax}

```sql
ARRAY_SUM(<array>)
```

## 返回类型 {#return-type}

数值型（与数组中最宽的数值类型一致）。

## 示例 {#examples}

```sql
SELECT ARRAY_SUM([1, 2, 3, 4]) AS total;

┌───────┐
│ total │
├───────┤
│    10 │
└───────┘
```

```sql
SELECT ARRAY_SUM([1.5, 2.25, 3.0]) AS total;

┌────────┐
│ total  │
├────────┤
│   6.75 │
└────────┘
```

```sql
SELECT ARRAY_SUM([10, NULL, -3]) AS total;

┌───────┐
│ total │
├───────┤
│     7 │
└───────┘
```

## 相关内容 {#related}

- [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md)