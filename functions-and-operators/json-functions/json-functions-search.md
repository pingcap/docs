---
title: JSON Functions that search JSON values
summary: Learn about JSON functions that search JSON values.
---

## [JSON_CONTAINS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains)

The `JSON_CONTAINS(json_doc, search [,path])` function indicates by returning 1 or 0 whether a given candidate JSON document is contained within a target JSON document.

Examples:

Here `a` is contained in the document.

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

Here `e` isn't contained in the document.

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

Here `{"foo": "bar"}` is contained in the document.

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

Here `"bar"` isn't contained in the root of the document.

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

Here `"bar"` isn't contained in the `$.foo` attribute of the document.

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

The `JSON_CONTAINS_PATH(json_doc, all_or_one, path [,path, ...])` function returns 0 or 1 to indicate whether a JSON document contains data at a given path or paths.

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

Here the document doesn't contain `$.bar`.

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

The `JSON_EXTRACT(json_doc, path)` function extracts data from a JSON document, selected from the parts of the document matched by the `path` arguments.

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

Returns the value from a JSON column after the evaluating path; an alias for [`JSON_EXTRACT()`](#json_extract).

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

Returns the value from a JSON column after the evaluating path and unquoting the result; an alias for `JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`.

## [JSON_KEYS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys)

Returns the keys from the top-level value of a JSON object as a JSON array, or, if a path argument is given, the top-level keys from the selected path.

## [JSON_SEARCH()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search)

Search a JSON document for one or all matches of a string.

## [MEMBER OF()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of)

If the passed value is an element of the JSON array, returns 1. Otherwise, returns 0.

## [JSON_OVERLAPS()](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps)

Indicates whether two JSON documents have overlapping part. If yes, returns 1. If not, returns 0.

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)