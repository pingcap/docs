---
title: JSON_PATH_MATCH
summary: 检查指定的 JSON 路径表达式是否与 JSON 数据中的特定条件匹配。请注意，`@@` 运算符是此函数的同义形式。更多信息，参见 JSON Operators。
---

# JSON_PATH_MATCH

检查指定的 JSON 路径表达式是否与 JSON 数据中的特定条件匹配。请注意，`@@` 运算符是此函数的同义形式。更多信息，参见 [JSON 运算符](/tidb-cloud-lake/sql/json-operators.md)。

## 语法 {#syntax}

```sql
JSON_PATH_MATCH(<json_data>, <json_path_expression>)
```

- `json_data`：指定要检查的 JSON 数据。它可以是 JSON 对象或数组。
- `json_path_expression`：指定要在 JSON 数据中检查的条件。该表达式描述了要匹配的具体路径或条件，例如验证 JSON 结构中特定字段的值是否满足某些条件。`$` 符号表示 JSON 数据的根。它用于开始路径表达式，并表示 JSON 结构中的顶层对象。

## 返回类型 {#return-type}

该函数返回：

- 如果指定的 JSON 路径表达式与 JSON 数据中的条件匹配，则返回 `true`。
- 如果指定的 JSON 路径表达式与 JSON 数据中的条件不匹配，则返回 `false`。
- 如果 `json_data` 或 `json_path_expression` 任一为 NULL 或无效，则返回 NULL。

## 示例 {#examples}

```sql
-- Check if the value at JSON path $.a is equal to 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1');

┌────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1') │
├────────────────────────────────────────────────────────────────┤
│ true                                                           │
└────────────────────────────────────────────────────────────────┘

-- Check if the first element in the array at JSON path $.b is greater than 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1');

┌──────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1') │
├──────────────────────────────────────────────────────────────────┤
│ false                                                            │
└──────────────────────────────────────────────────────────────────┘

-- Check if any element in the array at JSON path $.b
-- from the second one to the last are greater than or equal to 2
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2');

┌───────────────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2') │
├───────────────────────────────────────────────────────────────────────────┤
│ true                                                                      │
└───────────────────────────────────────────────────────────────────────────┘

-- NULL is returned if either the json_data or json_path_expression is NULL or invalid.
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), NULL);

┌──────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), null) │
├──────────────────────────────────────────────────────────┤
│ NULL                                                     │
└──────────────────────────────────────────────────────────┘

SELECT JSON_PATH_MATCH(NULL, '$.a == 1');

┌───────────────────────────────────┐
│ json_path_match(null, '$.a == 1') │
├───────────────────────────────────┤
│ NULL                              │
└───────────────────────────────────┘
```