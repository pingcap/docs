---
title: 返回 JSON 值的 JSON 函数
summary: 了解返回 JSON 值的 JSON 函数。
---

# 返回 JSON 值的 JSON 函数

TiDB 支持 MySQL 8.0 中所有 [返回 JSON 值属性的 JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html)。

## `JSON_DEPTH()`

`JSON_DEPTH(json_doc)` 函数返回一个 JSON 文档的最大嵌套层级。

示例：

在以下示例中，`JSON_DEPTH()` 返回 `3`，因为有三级嵌套：

- 根节点（`$`）
- weather（`$.weather`）
- weather current（`$.weather.sunny`）

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

## `JSON_LENGTH()`

`JSON_LENGTH(json_doc [,path])` 函数返回 JSON 文档的长度。如果指定了 `path` 参数，则返回该路径下值的长度。

示例：

在以下示例中，返回值为 `1`，因为文档根节点下只有一个项 `weather`。

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

在以下示例中，返回值为 `2`，因为 `$.weather` 下有两个项：`current` 和 `tomorrow`。

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

## `JSON_TYPE()`

`JSON_TYPE(json_val)` 函数返回一个字符串，指示 [JSON 值的类型](/data-type-json.md#json-value-types)。

示例：

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

需要注意的是，看起来相同的值，其类型可能不同，如下例所示。

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

## `JSON_VALID()`

`JSON_VALID(str)` 函数用于检查参数是否为合法的 JSON。这在将某一列转换为 `JSON` 类型前进行检查时非常有用。

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

## 参见

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
