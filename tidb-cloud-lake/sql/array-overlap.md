---
title: ARRAY_OVERLAP
summary: 2 つの JSON 配列に重複があるかどうかを確認し、共通要素がある場合は true を返し、ない場合は false を返します。
---

# ARRAY_OVERLAP

2 つの JSON 配列に重複があるかどうかを確認し、共通要素がある場合は `true` を返し、ない場合は `false` を返します。

## エイリアス {#aliases}

- `JSON_ARRAY_OVERLAP`

## 構文 {#syntax}

```sql
ARRAY_OVERLAP(<json_array1>, <json_array2>)
```

## 戻り値の型 {#return-type}

この関数はブール値を返します。

- 2 つの JSON 配列の間に少なくとも 1 つの共通要素がある場合は `true`
- 共通要素がない場合は `false`

## 例 {#examples}

```sql
SELECT ARRAY_OVERLAP(
    '["apple", "banana", "cherry"]'::JSON,
    '["banana", "kiwi", "mango"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_overlap('["apple", "banana", "cherry"]'::VARIANT, '["banana", "kiwi", "mango"]'::VARIANT): true

SELECT ARRAY_OVERLAP(
    '["grape", "orange"]'::JSON,
    '["apple", "kiwi"]'::JSON
);

-[ RECORD 1 ]-----------------------------------
array_overlap('["grape", "orange"]'::VARIANT, '["apple", "kiwi"]'::VARIANT): false
```