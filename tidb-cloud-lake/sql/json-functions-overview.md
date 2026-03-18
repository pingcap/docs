---
title: JSON Functions
summary: This section provides reference information for JSON functions in Databend. JSON functions enable parsing, validation, querying, and manipulation of JSON data structures.
---
This section provides reference information for JSON functions in Databend. JSON functions enable parsing, validation, querying, and manipulation of JSON data structures.

## JSON Parsing & Validation

| Function | Description | Example |
|----------|-------------|---------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | Parses a JSON string into a variant value | `PARSE_JSON('{"name":"John","age":30}')` → `{"name":"John","age":30}` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | Validates if a string is valid JSON | `CHECK_JSON('{"valid": true}')` → `true` |

## JSON Type Information

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | Returns the type of a JSON value | `JSON_TYPEOF('{"key": "value"}')` → `'OBJECT'` |

## JSON Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | Converts a JSON value to a string | `JSON_TO_STRING({"name":"John"})` → `'{"name":"John"}'` |

## JSON Path Operations

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | Checks if a JSON path exists | `JSON_PATH_EXISTS('{"a":1}', '$.a')` → `true` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | Matches JSON values against a path pattern | `JSON_PATH_MATCH('{"items":[1,2,3]}', '$.items[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | Queries JSON data using JSONPath | `JSON_PATH_QUERY('{"a":1,"b":2}', '$.a')` → `1` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | Queries JSON data and returns results as an array | `JSON_PATH_QUERY_ARRAY('[1,2,3]', '$[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | Returns the first result from a JSON path query | `JSON_PATH_QUERY_FIRST('[1,2,3]', '$[*]')` → `1` |

## JSON Data Extraction

| Function | Description | Example |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | Extracts value from JSON by index or field name | `GET('{"name":"John"}', 'name')` → `"John"` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | Extracts value with case-insensitive field matching | `GET_IGNORE_CASE('{"Name":"John"}', 'name')` → `"John"` |
| [GET_BY_KEYPATH](/tidb-cloud-lake/sql/get-by-keypath.md) | Extracts nested value using brace key paths | `GET_BY_KEYPATH('{"user":{"name":"Ada"}}', '{user,name}')` → `"Ada"` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | Extracts value using path notation | `GET_PATH('{"user":{"name":"John"}}', 'user.name')` → `"John"` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | Extracts text value from JSON using path | `JSON_EXTRACT_PATH_TEXT('{"name":"John"}', 'name')` → `'John'` |
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | Expands JSON object into key-value pairs | `JSON_EACH('{"a":1,"b":2}')` → `[("a",1),("b",2)]` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | Expands JSON array into individual elements | `JSON_ARRAY_ELEMENTS('[1,2,3]')` → `1, 2, 3` |

## JSON Formatting & Processing

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | Formats JSON with proper indentation | `JSON_PRETTY('{"a":1}')` → Formatted JSON string |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | Removes null values from JSON | `STRIP_NULL_VALUE('{"a":1,"b":null}')` → `{"a":1}` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | Processes JSON using jq-style queries | `JQ('{"name":"John"}', '.name')` → `"John"` |

## JSON Containment & Existence

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_CONTAINS_IN_LEFT](/tidb-cloud-lake/sql/contains.md) | Tests whether the left JSON contains the right JSON | `JSON_CONTAINS_IN_LEFT('{"a":1,"b":2}', '{"b":2}')` → `true` |
| [JSON_EXISTS_KEY](/tidb-cloud-lake/sql/json-exists-key.md) | Checks whether specific keys exist | `JSON_EXISTS_KEY('{"a":1}', 'a')` → `true` |
| [JSON_EXISTS_ANY_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | Returns `true` if any key in the list exists | `JSON_EXISTS_ANY_KEYS('{"a":1}', ['x','a'])` → `true` |
| [JSON_EXISTS_ALL_KEYS](/tidb-cloud-lake/sql/json-exists-key.md) | Returns `true` only if all keys exist | `JSON_EXISTS_ALL_KEYS('{"a":1,"b":2}', ['a','b'])` → `true` |
