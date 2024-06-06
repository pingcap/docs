---
title: JSON Functions
summary: Learn about JSON functions.
aliases: ['/docs/dev/functions-and-operators/json-functions/','/docs/dev/reference/sql/functions-and-operators/json-functions/']
---

# JSON Functions

JSON functions can be used to work with data in the [JSON data type](/data-type-json.md).

## Functions that create JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAY()](/functions-and-operators/json-functions/json-functions-create.md#json_array) | Evaluates a (possibly empty) list of values and returns a JSON array containing those values |
| [JSON_OBJECT()](/functions-and-operators/json-functions/json-functions-create.md#json_object) | Evaluates a (possibly empty) list of key-value pairs and returns a JSON object containing those pairs  |
| [JSON_QUOTE()](/functions-and-operators/json-functions/json-functions-create.md#json_quote) | Returns a string as a JSON value with quotes |

## Functions that search JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_CONTAINS()](/functions-and-operators/json-functions/json-functions-search.md#json_contains) | Indicates by returning 1 or 0 whether a given candidate JSON document is contained within a target JSON document |
| [JSON_CONTAINS_PATH()](/functions-and-operators/json-functions/json-functions-search.md#json_contains_path) | Returns 0 or 1 to indicate whether a JSON document contains data at a given path or paths |
| [JSON_EXTRACT()](/functions-and-operators/json-functions/json-functions-search.md#json_extract) | Returns data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [->](/functions-and-operators/json-functions/json-functions-search.md#-)  | Returns the value from a JSON column after the evaluating path; an alias for `JSON_EXTRACT(doc, path_literal)`   |
| [->>](/functions-and-operators/json-functions/json-functions-search.md#--1)  | Returns the value from a JSON column after the evaluating path and unquoting the result; an alias for `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))` |
| [JSON_KEYS()](/functions-and-operators/json-functions/json-functions-search.md#json_keys) | Returns the keys from the top-level value of a JSON object as a JSON array, or, if a path argument is given, the top-level keys from the selected path |
| [JSON_SEARCH()](/functions-and-operators/json-functions/json-functions-search.md#json_search) | Search a JSON document for one or all matches of a string |
| [MEMBER OF()](/functions-and-operators/json-functions/json-functions-search.md#member-of) | If the passed value is an element of the JSON array, returns 1. Otherwise, returns 0. |
| [JSON_OVERLAPS()](/functions-and-operators/json-functions/json-functions-search.md#json_overlaps) | Indicates whether two JSON documents have overlapping part. If yes, returns 1. If not, returns 0. |

## Functions that modify JSON values

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_append) | An alias to `JSON_ARRAY_APPEND()` |
| [JSON_ARRAY_APPEND()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_append) | Appends values to the end of the indicated arrays within a JSON document and returns the result |
| [JSON_ARRAY_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_array_insert) | Insert values into the specified locations of a JSON document and returns the result |
| [JSON_INSERT()](/functions-and-operators/json-functions/json-functions-modify.md#json_insert) | Inserts data into a JSON document and returns the result |
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch)  | Merge JSON documents |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve)  | Merges two or more JSON documents and returns the merged result |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge)  | A deprecated alias for `JSON_MERGE_PRESERVE()` |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove)    | Removes data from a JSON document and returns the result |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace) | Replaces existing values in a JSON document and returns the result |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set)  | Inserts or updates data in a JSON document and returns the result |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote) |  Unquotes a JSON value and returns the result as a string |

## Functions that return JSON value attributes

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_DEPTH(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth) | Returns the maximum depth of a JSON document |
| [JSON_LENGTH(json_doc[, path])](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length) | Returns the length of a JSON document, or, if a path argument is given, the length of the value within the path |
| [JSON_TYPE(json_val)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type) | Returns a string indicating the type of a JSON value |
| [JSON_VALID(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid) | Checks if a json\_doc is valid JSON. Useful for checking a column before converting it to the json type. |

## Utility functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_PRETTY(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty) | Pretty formatting of a JSON document |
| [JSON_STORAGE_FREE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free) | Returns how much storage space was freed in the binary representation of the JSON value after it was updated in place. As TiDB has different storage architecture from MySQL, this function always returns 0 for a valid JSON value, and it is implemented for compatibility with MySQL 8.0. |
| [JSON_STORAGE_SIZE(json_doc)](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size) | Returns an approximate size of bytes required to store the json value. As the size does not account for TiKV using compression, the output of this function is not strictly compatible with MySQL. |

## Aggregate functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG(key)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg) | Provides an aggregation of keys. |
| [JSON_OBJECTAGG(key, value)](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg) | Provides an aggregation of values for a given key. |

## See also

* [JSON Function Reference](https://dev.mysql.com/doc/refman/8.0/en/json-function-reference.html)
* [JSON Data Type](/data-type-json.md)

## Unsupported functions

- `JSON_SCHEMA_VALID()`
- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

For more information, see [#14486](https://github.com/pingcap/tidb/issues/14486).

## MySQL Compatibility

- TiDB supports most of the [JSON functions](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html) available in MySQL 8.0.