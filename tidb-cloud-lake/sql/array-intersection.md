---
title: ARRAY_INTERSECTION
summary: 返回两个 JSON 数组之间的公共元素。
---

# ARRAY_INTERSECTION

返回两个 JSON 数组之间的公共元素。

## 别名 {#aliases}

- `JSON_ARRAY_INTERSECTION`

## 语法 {#syntax}

```sql
ARRAY_INTERSECTION(<json_array1>, <json_array2>)
```

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

```sql
-- 查找两个 JSON 数组的交集
SELECT ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON);

-[ RECORD 1 ]-----------------------------------
array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT): ["Electronics","Books"]

-- 使用迭代方法，将第一次查询的结果与第三个 JSON 数组求交集
SELECT ARRAY_INTERSECTION(
    ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON),
    '["Electronics", "Books", "Clothing"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_intersection(array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT), '["Electronics", "Books", "Clothing"]'::VARIANT): ["Electronics","Books"]
```