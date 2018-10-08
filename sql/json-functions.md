---
title: JSON Functions
summary: Learn about JSON functions.
category: user guide
---

# JSON Functions

TiDB supports most of the JSON functions that shipped with the GA release of MySQL 5.7.  Additional JSON functions were added to MySQL 5.7 after its release, and not all are available in TiDB (see [unsupported functions](#unsupported-functions)).

## Functions that create JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAY([val[, val] ...])][json_array]  | Evaluate a (possibly empty) list of values and return a JSON array containing those values |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]   | Evaluate a (possibly empty) list of key-value pairs and return a JSON object containing those pairs  |
| [JSON_QUOTE][json_quote] | desc |

## Functions that search JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_CONTAINS][json_contains] | desc |
| [JSON_CONTAINS_PATH][json_contains_path] | desc |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]| Return data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [->][json_short_extract]  | Return value from JSON column after evaluating path; the syntactic sugar of `JSON_EXTRACT(doc, path_literal)`   |
| [->>][json_short_extract_unquote]  | Return value from JSON column after evaluating path and unquoting the result; the syntactic sugar of `JSON_UNQUOTE(JSONJSON_EXTRACT(doc, path_literal))` |
| [JSON_KEYS][json_keys] | desc |

## Functions that modify JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | Insert data into a JSON document and return the result |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | Merge two or more JSON documents and return the merged result |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | Remove data from a JSON document and return the result |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | Replace existing values in a JSON document and return the result |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | Insert or update data in a JSON document and return the result |
| [JSON_UNQUOTE(json_val)][json_unquote] |  Unquote JSON value and return the result as a string |

## Functions that return JSON value attributes

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| [JSON_LENGTH][json_length] | desc |
| [JSON_TYPE(json_val)][json_type] | Return a string indicating the type of a JSON value |
| [JSON_VALID][json_valid] | desc |

## Unsupported functions

The following JSON functions are unsupported in TiDB.  You can track our progress in adding them in [TIDB #7546](https://github.com/pingcap/tidb/issues/7546):

* `JSON_APPEND` and its alias `JSON_ARRAY_APPEND`
* `JSON_ARRAY_INSERT`
* `JSON_MERGE_PATCH`
* `JSON_MERGE_PRESERVE`, use the alias `JSON_MERGE` instead
* `JSON_PRETTY`
* `JSON_SEARCH`
* `JSON_STORAGE_SIZE`
* `JSON_DEPTH`
* `JSON_ARRAYAGG`
* `JSON_OBJECTAGG`

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
