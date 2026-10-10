---
title: ARRAY_INTERSECTION
summary: 2 つの JSON 配列の共通要素を返します。
---

# ARRAY_INTERSECTION

2 つの JSON 配列の共通要素を返します。

## エイリアス {#aliases}

- `JSON_ARRAY_INTERSECTION`

## 構文 {#syntax}

```sql
ARRAY_INTERSECTION(<json_array1>, <json_array2>)
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

```sql
-- 2 つの JSON 配列の積集合を検索する
SELECT ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON);

-[ RECORD 1 ]-----------------------------------
array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT): ["Electronics","Books"]

-- 反復的なアプローチを使用して、最初のクエリの結果と 3 つ目の JSON 配列との積集合を検索する
SELECT ARRAY_INTERSECTION(
    ARRAY_INTERSECTION('["Electronics", "Books", "Toys"]'::JSON, '["Books", "Fashion", "Electronics"]'::JSON),
    '["Electronics", "Books", "Clothing"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_intersection(array_intersection('["Electronics", "Books", "Toys"]'::VARIANT, '["Books", "Fashion", "Electronics"]'::VARIANT), '["Electronics", "Books", "Clothing"]'::VARIANT): ["Electronics","Books"]
```