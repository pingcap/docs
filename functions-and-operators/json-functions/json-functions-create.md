---
title: JSON Functions That Create JSON Values
summary: 了解用于创建 JSON 值的 JSON 函数。
---

# 用于创建 JSON 值的 JSON 函数

TiDB 支持 MySQL 8.0 中所有 [用于创建 JSON 值的 JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html)。

## `JSON_ARRAY()`

`JSON_ARRAY([val[, val] ...])` 函数会对一个（可能为空的）值列表进行求值，并返回一个包含这些值的 JSON 数组。

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

`JSON_OBJECT([key, val[, key, val] ...])` 函数会对一个（可能为空的）键值对列表进行求值，并返回一个包含这些键值对的 JSON 对象。

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

`JSON_QUOTE(str)` 函数会将一个字符串作为带引号的 JSON 值返回。

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

## 参见

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)