---
title: JSON Functions
summary: Learn about JSON functions.
category: user guide
---

# JSON Functions

## Functions that create JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| JSON_ARRAY | desc |
| JSON_OBJECT | desc |

## Functions that search JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| JSON_CONTAINS | desc |
| JSON_CONTAINS_PATH | desc |
| JSON_EXTRACT | desc |
| -> | desc |
| ->> | desc |

## Functions that modify JSON values

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| JSON_INSERT | desc |
| JSON_MERGE | desc |
| JSON_REMOVE | desc |
| JSON_REPLACE | desc |
| JSON_SET | desc |
| JSON_UNQUOTE | desc |

## Functions that return JSON value attributes

| Function Name and Syntactic Sugar | Description |
| --------------------------------- | ----------- |
| JSON_LENGTH | desc |
| JSON_TYPE | desc |


## Unsupported JSON Functions

The following JSON functions are currently unsupported in TiDB.  You can track our progress in adding them in [TIDB #7546](https://github.com/pingcap/tidb/issues/7546):

* `JSON_QUOTE`
* `JSON_APPEND` and its alias `JSON_ARRAY_APPEND`
* `JSON_ARRAY_INSERT`
* `JSON_MERGE_PATCH`
* `JSON_MERGE_PRESERVE`, use the alias `JSON_MERGE` instead
* `JSON_VALID`
* `JSON_PRETTY`
* `JSON_SEARCH`
* `JSON_STORAGE_SIZE`
* `JSON_DEPTH`
* `JSON_KEYS`
* `JSON_ARRAYAGG`
* `JSON_OBJECTAGG`

| Function Name and Syntactic Sugar  | Description  |
| ---------- | ------------------ |
| [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract]| Return data from a JSON document, selected from the parts of the document matched by the `path` arguments |
| [JSON_UNQUOTE(json_val)][json_unquote] |  Unquote JSON value and return the result as a string |
| [JSON_TYPE(json_val)][json_type] | Return a string indicating the type of a JSON value |
| [JSON_SET(json_doc, path, val[, path, val] ...)][json_set]  | Insert or update data in a JSON document and return the result |
| [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert] | Insert data into a JSON document and return the result |
| [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace] | Replace existing values in a JSON document and return the result |
| [JSON_REMOVE(json_doc, path[, path] ...)][json_remove]    | Remove data from a JSON document and return the result |
| [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge]  | Merge two or more JSON documents and return the merged result |
| [JSON_OBJECT(key, val[, key, val] ...)][json_object]   | Evaluate a (possibly empty) list of key-value pairs and return a JSON object containing those pairs  |
| [JSON_ARRAY([val[, val] ...])][json_array]  | Evaluate a (possibly empty) list of values and return a JSON array containing those values |
| ->  | Return value from JSON column after evaluating path; the syntactic sugar of `JSON_EXTRACT(doc, path_literal)`   |
| ->>  | Return value from JSON column after evaluating path and unquoting the result; the syntactic sugar of `JSON_UNQUOTE(JSONJSON_EXTRACT(doc, path_literal))` |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
