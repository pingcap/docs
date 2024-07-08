---
title: JSON Functions That Return JSON Values
summary: Learn about JSON functions that return JSON values.
---

# JSON Functions That Return JSON Values

This document describes JSON functions that return JSON values.

## [JSON_DEPTH()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth)

The `JSON_DEPTH(json_doc)` function returns the maximum depth of a JSON document.

Examples:

In the following example, `JSON_DEPTH()` returns `3` because there are three levels:

- root (`$`)
- weather (`$.weather`)
- weather current (`$.weather.sunny`)

```sql
SELECT JSON_DEPTH('{"weather": {"current": "sunny"}}');
```

```
+-------------------------------------------------+
| JSON_DEPTH('{"weather": {"current": "sunny"}}') |
+-------------------------------------------------+
|                                               3 |
+-------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_LENGTH()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length)

The `JSON_LENGTH(json_doc [,path])` function returns the length of a JSON document. If a `path` argument is given, it returns the length of the value within the path.

Examples:

In the following example, the returned value is `1` because the only item at the root of the document is `weather`.

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$');
```

```
+----------------------------------------------------------------------------+
| JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$') |
+----------------------------------------------------------------------------+
|                                                                          1 |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

In the following example, the returned value is `2` because there are two items at `$.weather`: `current` and `tomorrow`.

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather');
```

```
+------------------------------------------------------------------------------------+
| JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather') |
+------------------------------------------------------------------------------------+
|                                                                                  2 |
+------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

## [JSON_TYPE()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type)

The `JSON_TYPE(json_val)` function returns a string indicating [the type of a JSON value](/data-type-json.md#json-value-types).

Example:

```sql
WITH demo AS (
    SELECT 'null' AS 'v' 
    UNION SELECT '"foobar"' 
    UNION SELECT 'true' 
    UNION SELECT '5' 
    UNION SELECT '1.14' 
    UNION SELECT '[]' 
    UNION SELECT '{}' 
    UNION SELECT POW(2,63)
)
SELECT v, JSON_TYPE(v) FROM demo ORDER BY 2;
```

```
+----------------------+--------------+
| v                    | JSON_TYPE(v) |
+----------------------+--------------+
| []                   | ARRAY        |
| true                 | BOOLEAN      |
| 1.14                 | DOUBLE       |
| 9.223372036854776e18 | DOUBLE       |
| 5                    | INTEGER      |
| null                 | NULL         |
| {}                   | OBJECT       |
| "foobar"             | STRING       |
+----------------------+--------------+
8 rows in set (0.00 sec)
```

Note that values that look the same might not have the same type, as demonstrated in the following example.

```sql
SELECT '"2025-06-14"',CAST(CAST('2025-06-14' AS date) AS json);
```

```
+--------------+------------------------------------------+
| "2025-06-14" | CAST(CAST('2025-06-14' AS date) AS json) |
+--------------+------------------------------------------+
| "2025-06-14" | "2025-06-14"                             |
+--------------+------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_TYPE('"2025-06-14"'),JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json));
```

```
+---------------------------+-----------------------------------------------------+
| JSON_TYPE('"2025-06-14"') | JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json)) |
+---------------------------+-----------------------------------------------------+
| STRING                    | DATE                                                |
+---------------------------+-----------------------------------------------------+
1 row in set (0.00 sec)
```

## [JSON_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid)

The `JSON_VALID(str)` function checks if the argument is valid JSON. This can be useful for checking a column before converting it to the `JSON` type.

```sql
SELECT JSON_VALID('{"foo"="bar"}');
```

```
+-----------------------------+
| JSON_VALID('{"foo"="bar"}') |
+-----------------------------+
|                           0 |
+-----------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT JSON_VALID('{"foo": "bar"}');
```

```
+------------------------------+
| JSON_VALID('{"foo": "bar"}') |
+------------------------------+
|                            1 |
+------------------------------+
1 row in set (0.01 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)
