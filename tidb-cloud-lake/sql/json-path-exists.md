---
title: JSON_PATH_EXISTS
summary: 检查 JSON 数据中指定路径是否存在。
---

# JSON_PATH_EXISTS

检查 JSON 数据中指定路径是否存在。

## 语法 {#syntax}

```sql
JSON_PATH_EXISTS(<json_data>, <json_path_expression>)
```

- json_data：指定要在其中搜索的 JSON 数据。它可以是 JSON 对象或数组。

- json_path_expression：指定要在 JSON 数据中检查的路径，该路径从 JSON 数据根开始，以 `$` 表示。你还可以在表达式中包含条件，使用 `@` 引用当前正在求值的节点或元素，以过滤结果。

## 返回类型 {#return-type}

该函数返回：

- 如果指定的 JSON 路径（以及条件，如果有）在 JSON 数据中存在，则返回 `true`。
- 如果指定的 JSON 路径（以及条件，如果有）在 JSON 数据中不存在，则返回 `false`。
- 如果 json_data 或 json_path_expression 之一为 NULL 或无效，则返回 NULL。

## 示例 {#examples}

```sql
SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), '$.a ? (@ == 1)');

----
true

SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), '$.a ? (@ > 1)');

----
false

SELECT JSON_PATH_EXISTS(NULL, '$.a');

----
NULL

SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), NULL);

----
NULL
```