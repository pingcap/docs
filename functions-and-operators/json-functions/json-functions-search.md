---
title: JSON Functions That Search JSON Values
summary: Learn about JSON functions that search JSON values.
---

# JSON Functions That Search JSON Values

This document describes JSON functions that search JSON values.

## [JSON_CONTAINS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)

By returning `1` or `0`, the `JSON_CONTAINS(json_doc, candidate [,path])` function indicates whether a given `candidate` JSON document is contained within a target JSON document.

Examples:

Here `a` is contained in the target document.

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"a"');
```

```
+--------------------------------------+
| JSON_CONTAINS('["a","b","c"]','"a"') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```

Here `e` is not contained in the target document.

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"e"');
```

```
+--------------------------------------+
| JSON_CONTAINS('["a","b","c"]','"e"') |
+--------------------------------------+
|                                    0 |
+--------------------------------------+
1 row in set (0.00 sec)
```

Here `{"foo": "bar"}` is contained in the target document.

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}');
```

```
+------------------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

Here `"bar"` is not contained in the root of the target document.

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"');
```

```
+---------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"') |
+---------------------------------------------------+
|                                                 0 |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

Here `"bar"` is contained in the `$.foo` attribute of the target document.

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo');
```

```
+------------------------------------------------------------+
| JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_CONTAINS_PATH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path)

The `JSON_CONTAINS_PATH(json_doc, all_or_one, path [,path, ...])` function returns `0` or `1` to indicate whether a JSON document contains data at a given path or paths.

Examples:

Here the document contains `$.foo`.

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo');
```

```
+--------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo') |
+--------------------------------------------------------------+
|                                                            1 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

Here the document does not contain `$.bar`.

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar');
```

```
+--------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar') |
+--------------------------------------------------------------+
|                                                            0 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

Here the document contains both `$.foo` and `$.aaa`.

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa');
```

```
+-----------------------------------------------------------------------+
| JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa') |
+-----------------------------------------------------------------------+
|                                                                     1 |
+-----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_EXTRACT()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract)

The `JSON_EXTRACT(json_doc, path[, path] ...)` function extracts data from a JSON document, selected from the parts of the document matched by the `path` arguments.

```sql
SELECT JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo');
```

```
+---------------------------------------------------+
| JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo') |
+---------------------------------------------------+
| "bar"                                             |
+---------------------------------------------------+
1 row in set (0.00 sec)
```

## [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path)

The `column->path` function returns the data in `column` that matches the `path` argument. It is an alias for [`JSON_EXTRACT()`](#json_extract).

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

```
+------------+--------------------------+
| j->'$.foo' | JSON_EXTRACT(j, '$.foo') |
+------------+--------------------------+
| "bar"      | "bar"                    |
+------------+--------------------------+
1 row in set (0.00 sec)
```

## [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path)

The `column->>path` function unquotes data in `column` that matches the `path` argument. It is an alias for `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`.

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
    j->>'$.foo',
    JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo'))
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

```
+------------+--------------------------+-------------+----------------------------------------+
| j->'$.foo' | JSON_EXTRACT(j, '$.foo') | j->>'$.foo' | JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo')) |
+------------+--------------------------+-------------+----------------------------------------+
| "bar"      | "bar"                    | bar         | bar                                    |
+------------+--------------------------+-------------+----------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_KEYS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)

The `JSON_KEYS(json_doc [,path])` function returns the top-level keys of a JSON object as a JSON array. If a `path` argument is given, it returns the top-level keys from the selected path.

Examples:

The following example returns the two top-level keys in the JSON document.

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}');
```

```
+---------------------------------------------------------------------------+
| JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}') |
+---------------------------------------------------------------------------+
| ["name", "type"]                                                          |
+---------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

The following example returns the top-level keys that are in the `$.name` path of the JSON document.

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name');
```

```
+-------------------------------------------------------------------------------------+
| JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name') |
+-------------------------------------------------------------------------------------+
| ["first", "last"]                                                                   |
+-------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_SEARCH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search)

The `JSON_SEARCH(json_doc, one_or_all, str)` function searches a JSON document for one or all matches of a string.

Examples:

In the following example, you can search for the first result for `cc`, which is at the position of index 2 in the `a` array.

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc');
```

```
+------------------------------------------------------------------------+
| JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc') |
+------------------------------------------------------------------------+
| "$.a[2]"                                                               |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Now you do the same, but set `one_or_all` to `all` to get not just the first result, but all results.

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc');
```

```
+------------------------------------------------------------------------+
| JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc') |
+------------------------------------------------------------------------+
| ["$.a[2]", "$.b[0]"]                                                   |
+------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

## [MEMBER OF()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)

The `str MEMBER OF (json_array)` function tests if the passed value `str` is an element of the `json_array`, it returns `1`. Otherwise, it returns `0`. It returns `NULL` if any of the arguments is `NULL`.

```
SELECT '🍍' MEMBER OF ('["🍍","🥥","🥭"]') AS 'Contains pineapple';
```

```
+--------------------+
| Contains pineapple |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.00 sec)

```

## [JSON_OVERLAPS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)

The `JSON_OVERLAPS(json_doc, json_doc)` function indicates whether two JSON documents have overlapping part. If yes, it returns `1`. If not, it returns `0`. It returns `NULL` if any of the arguments is `NULL`.

Examples:

The following example shows that there is no overlap because the array value does not have the same number of elements.

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        0 |
+----------+
1 row in set (0.00 sec)
```

The following example shows that both JSON documents overlap as they are identical.

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

The following example shows that there is an overlap, while the second document has an extra attribute.

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"], "arch": ["arm64"]}'
) AS 'Overlaps';
```

```
+----------+
| Overlaps |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)