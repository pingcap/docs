---
title: ARRAY
summary: 根据提供的表达式构建数组字面量。每个参数都会按顺序求值并存储。所有元素都必须能够转换为同一种公共类型。
---

# ARRAY

根据提供的表达式构建数组字面量。每个参数都会按顺序求值并存储。所有元素都必须能够转换为同一种公共类型。

## 语法 {#syntax}

```sql
ARRAY(<expr1>, <expr2>, ... )
```

## 返回类型 {#return-type}

`ARRAY`

## 示例 {#examples}

```sql
SELECT ARRAY(1, 2, 3) AS arr_int;

┌─────────┐
│ arr_int │
├─────────┤
│ [1,2,3] │
└─────────┘
```

```sql
SELECT ARRAY('alpha', UPPER('beta')) AS arr_text;

┌───────────┐
│ arr_text  │
├───────────┤
│ ["alpha","BETA"] │
└───────────┘
```

```sql
SELECT ARRAY(1, NULL, 3) AS arr_with_null;

┌────────────────┐
│ arr_with_null  │
├────────────────┤
│ [1,NULL,3]     │
└────────────────┘
```