---
title: ARRAY_DISTINCT
summary: 从 JSON 数组中移除重复元素，并返回仅包含不同元素的数组。
---

# ARRAY_DISTINCT

从 JSON 数组中移除重复元素，并返回仅包含不同元素的数组。

## 别名 {#aliases}

- `JSON_ARRAY_DISTINCT`

## 语法 {#syntax}

```sql
ARRAY_DISTINCT(<json_array>)
```

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

```sql
SELECT ARRAY_DISTINCT('["apple", "banana", "apple", "orange", "banana"]'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_distinct('["apple", "banana", "apple", "orange", "banana"]'::VARIANT): ["apple","banana","orange"]
```