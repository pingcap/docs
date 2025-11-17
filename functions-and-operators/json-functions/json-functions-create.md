---
title: JSON Functions That Create JSON Values
summary: Learn about JSON functions that create JSON values.
---

# JSON Functions That Create JSON Values

TiDB supports all the [JSON functions that create JSON values](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html) available in MySQL 8.0.

## `JSON_ARRAY()`

The `JSON_ARRAY([val[, val] ...])` function evaluates a (possibly empty) list of values and returns a JSON array containing those values.

```sql
SELECT JSON_ARRAY(1,2,3,4,5), JSON_ARRAY("foo", "bar");
```

```
+-----------------------+--------------------------+
| JSON_ARRAY(1,2,3,4,5) | JSON_ARRAY("foo", "bar") |
+-----------------------+--------------------------+
| [1, 2, 3, 4, 5]       | ["foo", "bar"]           |
+-----------------------+--------------------------+
1 row in set (0.00 sec)
```

## `JSON_OBJECT()`

The `JSON_OBJECT([key, val[, key, val] ...])` function evaluates a (possibly empty) list of key-value pairs and returns a JSON object containing those pairs.

```sql
SELECT JSON_OBJECT("database", "TiDB", "distributed", TRUE);
```

```
+------------------------------------------------------+
| JSON_OBJECT("database", "TiDB", "distributed", TRUE) |
+------------------------------------------------------+
| {"database": "TiDB", "distributed": true}            |
+------------------------------------------------------+
1 row in set (0.00 sec)
```

## `JSON_QUOTE()`

The `JSON_QUOTE(str)` function returns a string as a JSON value with quotes.

```sql
SELECT JSON_QUOTE('The name is "O\'Neil"');
```

```
+-------------------------------------+
| JSON_QUOTE('The name is "O\'Neil"') |
+-------------------------------------+
| "The name is \"O'Neil\""            |
+-------------------------------------+
1 row in set (0.00 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)