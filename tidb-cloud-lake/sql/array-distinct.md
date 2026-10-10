---
title: ARRAY_DISTINCT
summary: JSON 配列から重複する要素を削除し、重複のない要素のみを含む配列を返します。
---

# ARRAY_DISTINCT

JSON 配列から重複する要素を削除し、重複のない要素のみを含む配列を返します。

## エイリアス {#aliases}

- `JSON_ARRAY_DISTINCT`

## 構文 {#syntax}

```sql
ARRAY_DISTINCT(<json_array>)
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

```sql
SELECT ARRAY_DISTINCT('["apple", "banana", "apple", "orange", "banana"]'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_distinct('["apple", "banana", "apple", "orange", "banana"]'::VARIANT): ["apple","banana","orange"]
```