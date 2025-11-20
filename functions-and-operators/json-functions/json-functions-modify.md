---
title: JSON Functions That Modify JSON Values
summary: 了解用于修改 JSON 值的 JSON 函数。
---

# 用于修改 JSON 值的 JSON 函数

TiDB 支持 MySQL 8.0 中所有 [用于修改 JSON 值的 JSON 函数](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html)。

## `JSON_APPEND()`

[`JSON_ARRAY_APPEND()`](#json_array_append) 的别名。

## `JSON_ARRAY_APPEND()`

`JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)` 函数会将值追加到 JSON 文档中指定 `path` 路径下的数组末尾，并返回结果。

该函数的参数以成对的方式传递，每对参数为一个 `path` 和一个 `value`。

示例：

以下示例向作为 JSON 文档根节点的数组中添加一个元素。

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

以下示例向指定路径下的数组中添加一个元素。

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

## `JSON_ARRAY_INSERT()`

`JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)` 函数会在 `json_array` 的指定 `path` 位置插入一个 `value`，并返回结果。

该函数的参数以成对的方式传递，每对参数为一个 `path` 和一个 `value`。

示例：

以下示例在数组的索引 0 位置插入一个值。

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

以下示例在数组的索引 1 位置插入一个值。

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

## `JSON_INSERT()`

`JSON_INSERT(json_doc, path, value [,path, value] ...)` 函数会向 JSON 文档中插入一个或多个值，并返回结果。

该函数的参数以成对的方式传递，每对参数为一个 `path` 和一个 `value`。

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

注意，该函数不会覆盖已存在属性的值。例如，以下语句看似会覆盖 `"a"` 属性，但实际上并不会。

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

## `JSON_MERGE_PATCH()`

`JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` 函数会将两个或多个 JSON 文档合并为一个 JSON 文档，对于重复的键不会保留其所有值。对于有重复键的 `json_doc` 参数，只有最后一个指定的 `json_doc` 参数中的值会在合并结果中保留。

示例：

在以下示例中，你可以看到 `a` 的值被第二个参数覆盖，`c` 作为新属性被添加到合并结果中。

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

## `JSON_MERGE_PRESERVE()`

`JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` 函数会合并两个或多个 JSON 文档，并保留每个键对应的所有值，返回合并结果。

示例：

在以下示例中，你可以看到第二个参数的值被追加到 `a`，`c` 作为新属性被添加。

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

## `JSON_MERGE()`

> **Warning:**
>
> 此函数已废弃。

[`JSON_MERGE_PRESERVE()`](#json_merge_preserve) 的已废弃别名。

## `JSON_REMOVE()`

`JSON_REMOVE(json_doc, path [,path] ...)` 函数会从 JSON 文档中移除指定 `path` 路径的数据，并返回结果。

示例：

此示例从 JSON 文档中移除了 `b` 属性。

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

此示例从 JSON 文档中移除了 `b` 和 `c` 属性。

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

## `JSON_REPLACE()`

`JSON_REPLACE(json_doc, path, value [, path, value] ...)` 函数会替换 JSON 文档中指定路径的值，并返回结果。如果指定的路径不存在，则不会将该路径对应的值添加到结果中。

该函数的参数以成对的方式传递，每对参数为一个 `path` 和一个 `value`。

示例：

在以下示例中，你将 `$.b` 的值从 `62` 修改为 `42`。

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

在以下示例中，你将 `$.b` 的值从 `62` 修改为 `42`。同时，该语句尝试将 `$.c` 的值替换为 `43`，但由于 `{"a": 41, "b": 62}` 中不存在 `$.c` 路径，因此不会生效。

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

## `JSON_SET()`

`JSON_SET(json_doc, path, value [,path, value] ...)` 函数会在 JSON 文档中插入或更新数据，并返回结果。

该函数的参数以成对的方式传递，每对参数为一个 `path` 和一个 `value`。

示例：

在以下示例中，你可以将 `$.version` 从 `1.1` 更新为 `1.2`。

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

在以下示例中，你可以将 `$.version` 从 `1.1` 更新为 `1.2`，并将之前不存在的 `$.branch` 更新为 `main`。

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

## `JSON_UNQUOTE()`

`JSON_UNQUOTE(json)` 函数会对 JSON 值进行去引号处理，并以字符串形式返回结果。该函数与 [`JSON_QUOTE()`](/functions-and-operators/json-functions/json-functions-create.md#json_quote) 功能相反。

示例：

在该示例中，`"foo"` 被去引号为 `foo`。

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

该函数通常与 [`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract) 一起使用。如下例所示，你可以在第一个示例中提取带引号的 JSON 值，然后在第二个示例中结合两个函数对值进行去引号。注意，你也可以使用 [`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1) 运算符来代替 `JSON_UNQUOTE(JSON_EXTRACT(...))`。

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

## 参见

- [JSON 函数总览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
