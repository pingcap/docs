---
title: JSON Functions That Modify JSON Values
summary: Learn about JSON functions that modify JSON values.
---

# JSON Functions That Modify JSON Values

This document describes JSON functions that modify JSON values.

## [JSON_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)

An alias to [`JSON_ARRAY_APPEND()`](#json_array_append).

## [JSON_ARRAY_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)

The `JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)` function appends values to the end of the indicated arrays within a JSON document at the specified `path` and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

The following example adds an item to an array, which is the root of the JSON document.

```sql
SELECT JSON_ARRAY_APPEND('["Car", "Boat", "Train"]', '$', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Car", "Boat", "Train", "Airplane"] |
+--------------------------------------+
1 row in set (0.00 sec)
```

The following example adds an item to an array at the specified path.

```sql
SELECT JSON_ARRAY_APPEND('{"transport_options": ["Car", "Boat", "Train"]}', '$.transport_options', "Airplane") AS "Transport options";
```

```
+-------------------------------------------------------------+
| Transport options                                           |
+-------------------------------------------------------------+
| {"transport_options": ["Car", "Boat", "Train", "Airplane"]} |
+-------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_ARRAY_INSERT()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-insert)

The `JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)` function inserts a `value` into the specified position of the `json_array` in the `path` and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

The following example inserts a value at the position of index 0 in the array.

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[0]', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Airplane", "Car", "Boat", "Train"] |
+--------------------------------------+
1 row in set (0.01 sec)
```

The following example inserts a value at the position of index 1 in the array.

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[1]', "Airplane") AS "Transport options";
```

```
+--------------------------------------+
| Transport options                    |
+--------------------------------------+
| ["Car", "Airplane", "Boat", "Train"] |
+--------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_INSERT()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert)

The `JSON_INSERT(json_doc, path, value [,path, value] ...)` function inserts one or more values into a JSON document and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

```sql
SELECT JSON_INSERT(
    '{"language": ["Go", "Rust", "C++"]}',
    '$.architecture', 'riscv',
    '$.os', JSON_ARRAY("linux","freebsd")
) AS "Demo";
```

```
+------------------------------------------------------------------------------------------+
| Demo                                                                                     |
+------------------------------------------------------------------------------------------+
| {"architecture": "riscv", "language": ["Go", "Rust", "C++"], "os": ["linux", "freebsd"]} |
+------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Note that this function does not overwrite values of existing attributes. For example, the following statement appears to overwrite the `"a"` attribute, but it does not actually do so.

```sql
SELECT JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63);
```

```
+---------------------------------------------------------+
| JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63) |
+---------------------------------------------------------+
| {"a": 61, "b": 62, "c": 63}                             |
+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE_PATCH()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)

The `JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` function merges two or more JSON documents into a single JSON document, without preserving values of duplicate keys. For `json_doc` arguments with duplicated keys, only the values from the later specified `json_doc` argument are preserved in the merged result.

Examples:

In the following example, you can see that the value of `a` gets overwritten by argument 2 and that `c` is added as a new attribute in the merged result.

```sql
SELECT JSON_MERGE_PATCH(
    '{"a": 1, "b": 2}',
    '{"a": 100}',
    '{"c": 300}'
);
```

```
+-----------------------------------------------------------------+
| JSON_MERGE_PATCH('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
+-----------------------------------------------------------------+
| {"a": 100, "b": 2, "c": 300}                                    |
+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE_PRESERVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-preserve)

The `JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` function merges two or more JSON documents while preserving all values associated with each key and returns the merged result.

Examples:

In the following example, you can see that the value of argument 2 is appended to `a` and that `c` is added as a new attribute.

```sql
SELECT JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}');
```

```
+--------------------------------------------------------------------+
| JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
+--------------------------------------------------------------------+
| {"a": [1, 100], "b": 2, "c": 300}                                  |
+--------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_MERGE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge)

> **Warning:**
>
> This function is deprecated.

A deprecated alias for [`JSON_MERGE_PRESERVE()`](#json_merge_preserve).

## [JSON_REMOVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)

The `JSON_REMOVE(json_doc, path [,path] ...)` function removes data of the specified `path` from a JSON document and returns the result.

Examples:

This example removes the `b` attribute from the JSON document.

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b');
```

```
+--------------------------------------------------+
| JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b') |
+--------------------------------------------------+
| {"a": 61, "c": 63}                               |
+--------------------------------------------------+
1 row in set (0.00 sec)
```

This example removes the `b` and `c` attributes from the JSON document.

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c');
```

```
+--------------------------------------------------------+
| JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c') |
+--------------------------------------------------------+
| {"a": 61}                                              |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_REPLACE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-replace)

The `JSON_REPLACE(json_doc, path, value [, path, value] ...)` function replaces values in specified paths of a JSON document and returns the result. If a specified path does not exist, the value corresponding to the path is not added to the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

In the following example, you change the value at `$.b` from `62` to `42`.

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42);
```

```
+---------------------------------------------+
| JSON_REPLACE('{"a": 41, "b": 62}','$.b',42) |
+---------------------------------------------+
| {"a": 41, "b": 42}                          |
+---------------------------------------------+
1 row in set (0.00 sec)
```

In the following example, you can change the value at `$.b` from `62` to `42`.  In addition, this statement tries to replace the value at `$.c` with `43`, but it does not work because the `$.c` path does not exist in `{"a": 41, "b": 62}`.

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43);
```

```
+------------------------------------------------------+
| JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43) |
+------------------------------------------------------+
| {"a": 41, "b": 42}                                   |
+------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_SET()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)

The `JSON_SET(json_doc, path, value [,path, value] ...)` function inserts or updates data in a JSON document and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

In the following example, you can update the `$.version` from `1.1` to `1.2`.

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2);
```

```
+-----------------------------------------------------------------+
| JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2) |
+-----------------------------------------------------------------+
| {"name": "example", "version": 1.2}                             |
+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

In the following example, you can update the `$.version` from `1.1` to `1.2`. And you can update `$.branch`, which does not exist before, to `main`.

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main");
```

```
+------------------------------------------------------------------------------------+
| JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main") |
+------------------------------------------------------------------------------------+
| {"branch": "main", "name": "example", "version": 1.2}                              |
+------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_UNQUOTE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote)

The `JSON_UNQUOTE(json)` function unquotes a JSON value and returns the result as a string. This is the opposite of the [`JSON_QUOTE()`](/functions-and-operators/json-functions/json-functions-create.md#json_quote) function.

Examples:

In the example, `"foo"` is unquoted to `foo`.

```sql
SELECT JSON_UNQUOTE('"foo"');
```

```
+-----------------------+
| JSON_UNQUOTE('"foo"') |
+-----------------------+
| foo                   |
+-----------------------+
1 row in set (0.00 sec)
```

This function is often used together with [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract). For the following examples, you can extract a JSON value with quotes in the first example and then use the two functions together to unquote the value in the second example. Note that instead of `JSON_UNQUOTE(JSON_EXTRACT(...))`, you can use the [`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1) operator.

```sql
SELECT JSON_EXTRACT('{"database": "TiDB"}', '$.database');
```

```
+----------------------------------------------------+
| JSON_EXTRACT('{"database": "TiDB"}', '$.database') |
+----------------------------------------------------+
| "TiDB"                                             |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database'));
```

```
+------------------------------------------------------------------+
| JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database')) |
+------------------------------------------------------------------+
| TiDB                                                             |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)