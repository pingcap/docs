---
title: JSON 函数
summary: 本节提供 {{{ .lake }}} 中 JSON 函数的参考信息。JSON 函数支持对 JSON 数据结构进行解析、验证、查询和操作。
---

# JSON 函数

本节提供 {{{ .lake }}} 中 JSON 函数的参考信息。JSON 函数支持对 JSON 数据结构进行解析、验证、查询和操作。

## JSON 解析与验证 {#json-parsing-validation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | 将 JSON 字符串解析为 variant 值 | `PARSE_JSON('{"name":"John","age":30}')` → `{"name":"John","age":30}` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | 验证一个字符串是否为有效的 JSON | `CHECK_JSON('{"valid": true}')` → `true` |

## JSON 类型信息 {#json-type-information}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | 返回 JSON 值的类型 | `JSON_TYPEOF('{"key": "value"}')` → `'OBJECT'` |

## JSON 转换 {#json-conversion}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | 将 JSON 值转换为字符串 | `JSON_TO_STRING({"name":"John"})` → `'{"name":"John"}'` |

## JSON 路径操作 {#json-path-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | 检查 JSON 路径是否存在 | `JSON_PATH_EXISTS('{"a":1}', '$.a')` → `true` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | 将 JSON 值与路径模式进行匹配 | `JSON_PATH_MATCH('{"items":[1,2,3]}', '$.items[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | 使用 JSONPath 查询 JSON 数据 | `JSON_PATH_QUERY('{"a":1,"b":2}', '$.a')` → `1` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | 查询 JSON 数据并以数组形式返回结果 | `JSON_PATH_QUERY_ARRAY('[1,2,3]', '$[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | 返回 JSON 路径查询的第一个结果 | `JSON_PATH_QUERY_FIRST('[1,2,3]', '$[*]')` → `1` |

## JSON 数据提取 {#json-data-extraction}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | 按索引或字段名从 JSON 中提取值 | `GET('{"name":"John"}', 'name')` → `"John"` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | 以不区分大小写的字段匹配方式提取值 | `GET_IGNORE_CASE('{"Name":"John"}', 'name')` → `"John"` |
| [GET_BY_KEYPATH](/tidb-cloud-lake/sql/get-by-keypath.md) | 使用大括号键路径提取嵌套值 | `GET_BY_KEYPATH('{"user":{"name":"Ada"}}', '{user,name}')` → `"Ada"` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | 使用路径表示法提取值 | `GET_PATH('{"user":{"name":"John"}}', 'user.name')` → `"John"` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | 使用路径从 JSON 中提取文本值 | `JSON_EXTRACT_PATH_TEXT('{"name":"John"}', 'name')` → `'John'` |
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | 将 JSON 对象展开为键值对 | `JSON_EACH('{"a":1,"b":2}')` → `[("a",1),("b",2)]` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | 将 JSON 数组展开为单独的元素 | `JSON_ARRAY_ELEMENTS('[1,2,3]')` → `1, 2, 3` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | 使用 jq 风格的查询处理 JSON | `JQ('{"name":"John"}', '.name')` → `"John"` |

## JSON 格式化与处理 {#json-formatting-processing}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | 使用适当的缩进格式化 JSON | `JSON_PRETTY('{"a":1}')` → 格式化后的 JSON 字符串 |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | 从 JSON 中移除空值 | `STRIP_NULL_VALUE('{"a":1,"b":null}')` → `{"a":1}` |
| [JSON_STRIP_NULLS](/tidb-cloud-lake/sql/json-strip-nulls.md) | 从 JSON 对象中移除空值 | `JSON_STRIP_NULLS(PARSE_JSON('{"a":1,"b":null}'))` → `{"a":1}` |

## JSON 包含与存在性 {#json-containment-existence}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_CONTAINS_IN_LEFT](/tidb-cloud-lake/sql/contains.md) | 测试左侧 JSON 是否包含右侧 JSON | `JSON_CONTAINS_IN_LEFT('{"a":1,"b":2}', '{"b":2}')` → `true` |
| [JSON_EXISTS_KEY](/tidb-cloud-lake/sql/json-exists-key.md) | 检查是否存在指定的键 | `JSON_EXISTS_KEY('{"a":1}', 'a')` → `true` |
| [JSON_EXISTS_ANY_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | 如果列表中的任意键存在，则返回 `true` | `JSON_EXISTS_ANY_KEYS('{"a":1}', ['x','a'])` → `true` |
| [JSON_EXISTS_ALL_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | 仅当所有键都存在时返回 `true` | `JSON_EXISTS_ALL_KEYS('{"a":1,"b":2}', ['a','b'])` → `true` |