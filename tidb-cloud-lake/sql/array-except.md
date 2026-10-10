---
title: ARRAY_EXCEPT
summary: 2 番目の JSON 配列に存在しない、1 番目の JSON 配列の要素を含む新しい JSON 配列を返します。
---

# ARRAY_EXCEPT

2 番目の JSON 配列に存在しない、1 番目の JSON 配列の要素を含む新しい JSON 配列を返します。

## エイリアス {#aliases}

- `JSON_ARRAY_EXCEPT`

## 構文 {#syntax}

```sql
ARRAY_EXCEPT(<source_array>, <array_of_elements_to_exclude>)
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

```sql
SELECT ARRAY_EXCEPT(
    '["apple", "banana", "orange"]'::VARIANT,
    '["banana", "grapes"]'::VARIANT
);

-[ RECORD 1 ]-----------------------------------
array_except('["apple", "banana", "orange"]'::VARIANT, '["banana", "grapes"]'::VARIANT): ["apple","orange"]

-- 1 番目の配列のすべての要素が 2 番目の配列に存在するため、空の配列を返します。
SELECT ARRAY_EXCEPT('["apple", "banana", "orange"]'::VARIANT, '["apple", "banana", "orange"]'::VARIANT)

-[ RECORD 1 ]-----------------------------------
array_except('["apple", "banana", "orange"]'::VARIANT, '["apple", "banana", "orange"]'::VARIANT): []
```