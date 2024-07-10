---
title: JSON Functions
summary: Learn about JSON functions.
---

# JSON Functions

You can use JSON functions to work with data in the [JSON data type](/data-type-json.md).

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
| [JSON_MERGE_PATCH()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_patch)  | Merges two or more JSON documents, without preserving values of duplicate keys |
| [JSON_MERGE_PRESERVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge_preserve)  | Merges two or more JSON documents by preserving all values |
| [JSON_MERGE()](/functions-and-operators/json-functions/json-functions-modify.md#json_merge)  | A deprecated alias for `JSON_MERGE_PRESERVE()` |
| [JSON_REMOVE()](/functions-and-operators/json-functions/json-functions-modify.md#json_remove)    | Removes data from a JSON document and returns the result |
| [JSON_REPLACE()](/functions-and-operators/json-functions/json-functions-modify.md#json_replace) | Replaces existing values in a JSON document and returns the result |
| [JSON_SET()](/functions-and-operators/json-functions/json-functions-modify.md#json_set)  | Inserts or updates data in a JSON document and returns the result |
| [JSON_UNQUOTE()](/functions-and-operators/json-functions/json-functions-modify.md#json_unquote) |  Unquotes a JSON value and returns the result as a string |

## Functions that return JSON value attributes

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_DEPTH()](/functions-and-operators/json-functions/json-functions-return.md#json_depth) | Returns the maximum depth of a JSON document |
| [JSON_LENGTH()](/functions-and-operators/json-functions/json-functions-return.md#json_length) | Returns the length of a JSON document, or, if a path argument is given, the length of the value within the path |
| [JSON_TYPE()](/functions-and-operators/json-functions/json-functions-return.md#json_type) | Returns a string indicating the type of a JSON value |
| [JSON_VALID()](/functions-and-operators/json-functions/json-functions-return.md#json_valid) | Checks if a json\_doc is valid JSON. |

## Utility functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_PRETTY()](/functions-and-operators/json-functions/json-functions-utility.md#json_pretty) | Pretty formatting of a JSON document |
| [JSON_STORAGE_FREE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_free) | Returns how much storage space was freed in the binary representation of the JSON value after it was updated in place. |
| [JSON_STORAGE_SIZE()](/functions-and-operators/json-functions/json-functions-utility.md#json_storage_size) | Returns an approximate size of bytes required to store the json value. As the size does not account for TiKV using compression, the output of this function is not strictly compatible with MySQL. |

## Aggregate functions

| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_ARRAYAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg) | Provides an aggregation of keys. |
| [JSON_OBJECTAGG()](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg) | Provides an aggregation of values for a given key. |

## Validation functions
    
| Function Name                     | Description |
| --------------------------------- | ----------- |
| [JSON_SCHEMA_VALID()](/functions-and-operators/json-functions/json-functions-validate.md#json_schema_valid) | Validates a JSON document against a schema to ensure data integrity and consistency. |

## JSONPath

Many of JSON functions use [JSONPath](https://www.rfc-editor.org/rfc/rfc9535.html) to select parts of a JSON document.

| Symbol         | Description                  |
| -------------- | ---------------------------- |
| `$`            | Document root                |
| `.`            | Member selection             |
| `[]`           | Array selection              |
| `*`            | Wildcard                     |
| `**`           | Path wildcard                |
| `[<n> to <n>]` | Array range selection        |

The subsequent content takes the following JSON document as an example to demonstrate how to use JSONPath:

```json
{
    "database": {
        "name": "TiDB",
        "features": [
            "distributed",
            "scalable",
            "relational",
            "cloud native"
        ],
        "license": "Apache-2.0 license",
        "versions": [
            {
                "version": "v8.1.0",
                "type": "lts",
                "release_date": "2024-05-24" 
            },
            {
                "version": "v8.0.0",        
                "type": "dmr",
                "release_date": "2024-03-29"
            }
        ]
    },
    "migration_tool": {
        "name": "TiDB Data Migration",
        "features": [
            "MySQL compatible",            
            "Shard merging"
        ],
        "license": "Apache-2.0 license"
    }
}
```

| JSONPath                              | Description                             | Example with [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) | 
|-------------------------------------- |-----------------------------------------|-------------------------------|
| `$`                                   | The root of the document                | Returns the full document                              |
| `$.database`                          | The `database` object                  |  Returns the full structure starting with `"database"`. It does not include `"migration_tool"` and the structure below that.                             |
| `$.database.name`                     | The name of the database.               | `"TiDB"`                      |
| `$.database.features`                 | All database features                   | `["distributed", "scalable", "relational", "cloud native"]`                              |
| `$.database.features[0]`              | The first database feature.             | `"distributed"`               |
| `$.database.features[2]`              | The third database feature.             | `"relational"`                |
| `$.database.versions[0].type`         | The type of the first database version. | `"lts"`                       |
| `$.database.versions[*].release_date` | The release date for all versions.      | `["2024-05-24","2024-03-29"]` |
| `$.*.features`                        | Two array's of features                 | `[["distributed", "scalable", "relational", "cloud native"], ["MySQL compatible", "Shard merging"]]`                              |
| `$**.version`                         | All versions, with path wildcard        | `["v8.1.0","v8.0.0"]`         |
| `$.database.features[0 to 2]`         | Range of database features from the first to the third.             | `["scalable","relational"]`   |

For more information, see [the IETF draft for JSONPath](https://www.ietf.org/archive/id/draft-goessner-dispatch-jsonpath-00.html).

## See also

* [JSON Data Type](/data-type-json.md)

## Unsupported functions

- `JSON_SCHEMA_VALIDATION_REPORT()`
- `JSON_TABLE()`
- `JSON_VALUE()`

For more information, see [#14486](https://github.com/pingcap/tidb/issues/14486).

## MySQL compatibility

- TiDB supports most of the [JSON functions](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html) available in MySQL 8.0.
