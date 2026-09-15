---
title: ARRAY_OVERLAP
summary: 检查两个 JSON 数组是否存在重叠；如果有公共元素则返回 true，否则返回 false。
---

# ARRAY_OVERLAP

检查两个 JSON 数组是否存在重叠；如果有公共元素则返回 `true`，否则返回 `false`。

## 别名 {#aliases}

- `JSON_ARRAY_OVERLAP`

## 语法 {#syntax}

```sql
ARRAY_OVERLAP(<json_array1>, <json_array2>)
```

## 返回类型 {#return-type}

该函数返回一个布尔值：

- 如果两个 JSON 数组之间至少有一个公共元素，则返回 `true`；
- 如果没有公共元素，则返回 `false`。

## 示例 {#examples}

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