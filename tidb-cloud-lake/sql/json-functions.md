---
title: JSON Functions
---

This section provides reference information for JSON functions in Databend. JSON functions enable parsing, validation, querying, and manipulation of JSON data structures.

## JSON Parsing & Validation

| Function | Description | Example |
|----------|-------------|---------|
| [PARSE_JSON](json/parse-json) | Parses a JSON string into a variant value | `PARSE_JSON('{"name":"John","age":30}')` → `{"name":"John","age":30}` |
| [CHECK_JSON](json/check-json) | Validates if a string is valid JSON | `CHECK_JSON('{"valid": true}')` → `true` |

## JSON Type Information

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_TYPEOF](json/json-typeof) | Returns the type of a JSON value | `JSON_TYPEOF('{"key": "value"}')` → `'OBJECT'` |

## JSON Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_TO_STRING](json/json-to-string) | Converts a JSON value to a string | `JSON_TO_STRING({"name":"John"})` → `'{"name":"John"}'` |

## JSON Path Operations

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_PATH_EXISTS](json/json-path-exists) | Checks if a JSON path exists | `JSON_PATH_EXISTS('{"a":1}', '$.a')` → `true` |
| [JSON_PATH_MATCH](json/json-path-match) | Matches JSON values against a path pattern | `JSON_PATH_MATCH('{"items":[1,2,3]}', '$.items[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY](json/json-path-query) | Queries JSON data using JSONPath | `JSON_PATH_QUERY('{"a":1,"b":2}', '$.a')` → `1` |
| [JSON_PATH_QUERY_ARRAY](json/json-path-query-array) | Queries JSON data and returns results as an array | `JSON_PATH_QUERY_ARRAY('[1,2,3]', '$[*]')` → `[1,2,3]` |
| [JSON_PATH_QUERY_FIRST](json/json-path-query-first) | Returns the first result from a JSON path query | `JSON_PATH_QUERY_FIRST('[1,2,3]', '$[*]')` → `1` |

## JSON Data Extraction

| Function | Description | Example |
|----------|-------------|---------|
| [GET](json/get) | Extracts value from JSON by index or field name | `GET('{"name":"John"}', 'name')` → `"John"` |
| [GET_IGNORE_CASE](json/get-ignore-case) | Extracts value with case-insensitive field matching | `GET_IGNORE_CASE('{"Name":"John"}', 'name')` → `"John"` |
| [GET_BY_KEYPATH](json/get-by-keypath) | Extracts nested value using brace key paths | `GET_BY_KEYPATH('{"user":{"name":"Ada"}}', '{user,name}')` → `"Ada"` |
| [GET_PATH](json/get-path) | Extracts value using path notation | `GET_PATH('{"user":{"name":"John"}}', 'user.name')` → `"John"` |
| [JSON_EXTRACT_PATH_TEXT](json/json-extract-path-text) | Extracts text value from JSON using path | `JSON_EXTRACT_PATH_TEXT('{"name":"John"}', 'name')` → `'John'` |
| [JSON_EACH](json/json-each) | Expands JSON object into key-value pairs | `JSON_EACH('{"a":1,"b":2}')` → `[("a",1),("b",2)]` |
| [JSON_ARRAY_ELEMENTS](json/json-array-elements) | Expands JSON array into individual elements | `JSON_ARRAY_ELEMENTS('[1,2,3]')` → `1, 2, 3` |

## JSON Formatting & Processing

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_PRETTY](json/json-pretty) | Formats JSON with proper indentation | `JSON_PRETTY('{"a":1}')` → Formatted JSON string |
| [STRIP_NULL_VALUE](json/strip-null-value) | Removes null values from JSON | `STRIP_NULL_VALUE('{"a":1,"b":null}')` → `{"a":1}` |
| [JQ](json/jq) | Processes JSON using jq-style queries | `JQ('{"name":"John"}', '.name')` → `"John"` |

## JSON Containment & Existence

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_CONTAINS_IN_LEFT](json/json-contains) | Tests whether the left JSON contains the right JSON | `JSON_CONTAINS_IN_LEFT('{"a":1,"b":2}', '{"b":2}')` → `true` |
| [JSON_EXISTS_KEY](json/json-exists-keys) | Checks whether specific keys exist | `JSON_EXISTS_KEY('{"a":1}', 'a')` → `true` |
| [JSON_EXISTS_ANY_KEYS](json/json-exists-keys) | Returns `true` if any key in the list exists | `JSON_EXISTS_ANY_KEYS('{"a":1}', ['x','a'])` → `true` |
| [JSON_EXISTS_ALL_KEYS](json/json-exists-keys) | Returns `true` only if all keys exist | `JSON_EXISTS_ALL_KEYS('{"a":1,"b":2}', ['a','b'])` → `true` |
