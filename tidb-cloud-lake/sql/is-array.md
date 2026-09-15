---
title: IS_ARRAY
summary: 检查输入值是否为 JSON 数组。请注意，JSON 数组与 ARRAY 数据类型并不相同。JSON 数组是 JSON 中常用的一种数据结构，表示由方括号 [] 括起来的有序值集合。它是一种灵活的格式，可用于组织和交换多种数据类型，包括字符串、数字、布尔值、对象和空值。
---

# IS_ARRAY

检查输入值是否为 JSON 数组。请注意，JSON 数组与 [ARRAY](/tidb-cloud-lake/sql/array.md) 数据类型并不相同。JSON 数组是 JSON 中常用的一种数据结构，表示由方括号 `[ ]` 括起来的有序值集合。它是一种灵活的格式，可用于组织和交换多种数据类型，包括字符串、数字、布尔值、对象和空值。

```json title='JSON Array Example:'
[
  "Apple",
  42,
  true,
  {"name": "John", "age": 30, "isStudent": false},
  [1, 2, 3],
  null
]
```

## 语法 {#syntax}

```sql
IS_ARRAY( <expr> )
```

## 返回类型 {#return-type}

如果输入值是 JSON 数组，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_ARRAY(PARSE_JSON('true')),
  IS_ARRAY(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_array(parse_json('true')) │ is_array(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ false                        │ true                            │
└────────────────────────────────────────────────────────────────┘
```