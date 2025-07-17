---
title: JSON Functions That Modify JSON Values
summary: 了解修改 JSON 值的 JSON 函数。
---

# JSON Functions That Modify JSON Values

本文档描述了修改 JSON 值的 JSON 函数。

## [JSON_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-append)

是 [`JSON_ARRAY_APPEND()`](#json_array_append) 的别名。

## [JSON_ARRAY_APPEND()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-array-append)

`JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)` 函数在指定 `path` 位置的 JSON 文档中的数组末尾追加值，并返回结果。

此函数的参数成对出现，每对为一个 `path` 和一个 `value`。

示例：

以下示例在 JSON 文档的根数组中添加一个项目。

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

以下示例在指定路径的数组中添加一个项目。

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

`JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)` 函数在 `json_array` 中的指定位置插入 `value`，并返回结果。

此函数的参数成对出现，每对为一个 `path` 和一个 `value`。

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

## [JSON_INSERT()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-insert)

`JSON_INSERT(json_doc, path, value [,path, value] ...)` 函数在 JSON 文档中插入一个或多个值，并返回结果。

此函数的参数成对出现，每对为一个 `path` 和一个 `value`。

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

注意，此函数不会覆盖已存在属性的值。例如，以下语句似乎会覆盖 `"a"` 属性，但实际上并不会。

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

`JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)` 函数将两个或多个 JSON 文档合并成一个 JSON 文档，不保留重复键的值。对于带有重复键的 `json_doc` 参数，合并结果中只保留后面指定的 `json_doc` 的值。

示例：

以下示例中，`a` 的值被第二个参数覆盖，`c` 被添加为新属性。

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

`JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)` 函数合并两个或多个 JSON 文档，同时保留每个键的所有值，并返回合并后的结果。

示例：

以下示例中，第二个参数的值被追加到 `a`，`c` 被添加为新属性。

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
> 这个函数已被弃用。

是 [`JSON_MERGE_PRESERVE()`](#json_merge_preserve) 的弃用别名。

## [JSON_REMOVE()](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html#function_json-remove)

`JSON_REMOVE(json_doc, path [,path] ...)` 函数删除 JSON 文档中指定 `path` 的数据，并返回结果。

示例：

此示例删除 JSON 文档中的 `b` 属性。

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

此示例删除 JSON 文档中的 `b` 和 `c` 属性。

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

`JSON_REPLACE(json_doc, path, value [, path, value] ...)` 函数替换 JSON 文档中指定路径的值，并返回结果。如果指定路径不存在，则不会添加对应的值。

此函数的参数成对出现，每对为一个 `path` 和一个 `value`。

示例：

以下示例将 `$.b` 的值由 `62` 改为 `42`。

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

以下示例尝试将 `$.b` 的值由 `62` 改为 `42`，同时还试图将 `$.c` 的值替换为 `43`，但由于 `{"a": 41, "b": 62}` 中不存在 `$.c` 路径，后者不会生效。

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

`JSON_SET(json_doc, path, value [,path, value] ...)` 函数在 JSON 文档中插入或更新数据，并返回结果。

此函数的参数成对出现，每对为一个 `path` 和一个 `value`。

示例：

以下示例将 `$.version` 从 `1.1` 更新为 `1.2`。

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

以下示例在更新 `$.version` 的同时，还可以新增 `$.branch`，即之前不存在的路径，设置为 `main`。

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

`JSON_UNQUOTE(json)` 函数对 JSON 值取消引号，返回字符串。这与 [`JSON_QUOTE()`](#json_quote) 函数相反。

示例：

在示例中，`"foo"` 被取消引号变为 `foo`。

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

此函数常与 [`JSON_EXTRACT()`](#json_extract) 一起使用。以下示例中，第一行提取带引号的 JSON 值，第二行结合两个函数取消引号。注意，除了 `JSON_UNQUOTE(JSON_EXTRACT(...))`，你也可以使用 [`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1) 操作符。

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