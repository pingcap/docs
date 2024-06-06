---
title: JSON Functions that modify JSON values
summary: Learn about JSON functions that modify JSON values.
---

## [JSON_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)

An alias to [`JSON_ARRAY_APPEND()`](#json_array_append).

## [JSON_ARRAY_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)

The `JSON_ARRAY_APPEND(json_array, path, val)` function appends values to the end of the indicated arrays within a JSON document at the specified `path` and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

The example below adds an item to an array, which is the root of the JSON document.

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

The example below adds an item to an array at the specified path.

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

The `JSON_ARRAY_INSERT(json_array, path, str)` function inserts a value into the specified locations of a JSON array and returns the result.

This function takes arguments in pairs, where each pair is a `path` and a `value`.

Examples:

In this example we add a value at position 0 of the array.

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

In this example we add a value at position 1 of the array.

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

## [JSON_MERGE_PATCH()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-merge-patch)

The `JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` function merges two or more JSON documents by patching existing attributes and returns the merged result.

Examples:

In this example you can see that the value of `a` gets overwritten by argument 2 and that `c` gets added as new attribute.

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

The `JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` function merges two or more JSON documents by appending to existing attributes and returns the merged result.

Examples:

In this example you can see that the value of argument 2 gets appended to `a` and that `c` gets added as new attribute.

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

The `JSON_REMOVE(json_doc, path [,path] ...)` function removes `path` from a JSON document and returns the result.

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

Replaces existing values in a JSON document and returns the result.

## [JSON_SET()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-set)

Inserts or updates data in a JSON document and returns the result.

## [JSON_UNQUOTE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-unquote)

Unquotes a JSON value and returns the result as a string.

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)