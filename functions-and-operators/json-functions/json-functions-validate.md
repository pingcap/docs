---
title: 用于验证 JSON 文档的 JSON 函数
summary: 了解用于验证 JSON 文档的 JSON 函数。
---

# 用于验证 JSON 文档的 JSON 函数

本文档介绍了用于验证 JSON 文档的 JSON 函数。

> **Note:**
>
> 目前，该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## [JSON_SCHEMA_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-validation-functions.html#function_json-schema-valid)

`JSON_SCHEMA_VALID(schema, json_doc)` 函数用于根据 schema 验证 JSON 文档，以确保数据的完整性和一致性。

该函数可以与 [CHECK](/constraints.md#check) 约束结合使用，在表被修改时自动进行 schema 验证。

此函数遵循 [JSON Schema 规范](https://json-schema.org/specification)。

支持的校验关键字如下：

| 校验关键字              | 适用类型         | 描述 |
|---|---|---|
| `type`                 | 任意 | 检查类型（如 `array` 和 `string`） |
| `enum`                 | 任意 | 检查值是否在指定的值数组中 |
| `const`                | 任意 | 类似于 `enum`，但只针对单个值 |
| `allOf`                | 任意 | 匹配所有指定的 schema |
| `anyOf`                | 任意 | 匹配任意一个指定的 schema |
| `multipleOf`           | `number`/`integer` | 检查值是否为指定值的倍数 |
| `maximum`              | `number`/`integer` | 检查值是否小于等于最大值（包含） |
| `exclusiveMaximum`     | `number`/`integer` | 检查值是否小于最大值（不包含） |
| `minimum`              | `number`/`integer` | 检查值是否大于等于最小值（包含） |
| `exclusiveMinimum`     | `number`/`integer` | 检查值是否大于最小值（不包含） |
| `maxlength`            | `string` | 检查值的长度是否不超过指定值 |
| `minLength`            | `string` | 检查值的长度是否至少为指定值 |
| `format`               | `string` | 检查字符串是否匹配命名格式 |
| `pattern`              | `string` | 检查字符串是否匹配正则表达式 |
| `items`                | `array` | 应用于数组元素的 schema |
| `prefixItems`          | `array` | 应用于数组位置元素的 schema |
| `maxItems`             | `array` | 检查数组元素数量是否不超过指定值 |
| `minItems`             | `array` | 检查数组元素数量是否至少为指定值 |
| `uniqueItems`          | `array` | 检查数组元素是否唯一，`true`/`false`|
| `contains`             | `array` | 为数组中包含的元素设置 schema |
| `maxContains`          | `array` | 与 `contains` 一起使用，检查某元素最多出现的次数 |
| `minContains`          | `array` | 与 `contains` 一起使用，检查某元素最少出现的次数 |
| `properties`           | `object` | 应用于对象属性的 schema |
| `patternProperties`    | `object` | 基于属性名模式匹配应用 schema |
| `additionalProperties` | `object` | 是否允许额外属性，`true`/`false` |
| `minProperties`        | `object` | 检查对象最少拥有的属性数量 |
| `maxProperties`        | `object` | 检查对象最多拥有的属性数量 |
| `required`             | `object` | 检查对象中是否存在指定属性名 |

示例：

对于部分示例，使用如下 JSON 文档：

```json
{
    "fruits": [
        "orange",
        "apple",
        "pear"
    ],
    "vegetables": [
        "carrot",
        "pepper",
        "kale"]
}
```

使用 [用户自定义变量](/user-defined-variables.md) 保存该 JSON 文档。

```sql
SET @j := '{"fruits": ["orange", "apple", "pear"], "vegetables": ["carrot", "pepper", "kale"]}';
```

首先测试类型：

```sql
SELECT JSON_SCHEMA_VALID('{"type": "object"}',@j);
```

```
+--------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "object"}',@j) |
+--------------------------------------------+
|                                          1 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "array"}',@j);
```

```
+-------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "array"}',@j) |
+-------------------------------------------+
|                                         0 |
+-------------------------------------------+
1 row in set (0.00 sec)
```

```sql
mysql> SELECT JSON_TYPE(@j);
```

```
+---------------+
| JSON_TYPE(@j) |
+---------------+
| OBJECT        |
+---------------+
1 row in set (0.00 sec)
```

如上输出所示，`@j` 的类型为 `object`。这与 [`JSON_TYPE()`](/functions-and-operators/json-functions/json-functions-return.md#json_type) 的输出一致。

现在验证某些属性是否存在。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j);
```

```
+---------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j) |
+---------------------------------------------------------------+
|                                                             1 |
+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

如上输出所示，`fruits` 和 `vegetables` 属性的存在性校验通过。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

如上输出所示，`fruits`、`vegetables` 和 `grains` 属性的存在性校验失败，因为 `grains` 不存在。

现在验证 `fruits` 是否为数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array"}}}',@j);
```

```
+-----------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array"}}}',@j) |
+-----------------------------------------------------------------------+
|                                                                     1 |
+-----------------------------------------------------------------------+
1 row in set (0.01 sec)
```

上述输出确认了 `fruits` 是一个数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

上述输出表明 `fruits` **不是** 字符串。

现在验证数组中的元素数量。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    1 |
+--------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

上述输出表明 `fruits` 是一个包含至少 3 个元素的数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    0 |
+--------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

上述输出表明 `fruits` **不是** 一个包含至少 4 个元素的数组。因为它不满足最小元素数量的要求。

对于整数值，可以检查其是否在某个范围内。

```sql
SELECT JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42');
+------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42') |
+------------------------------------------------------------------------------+
|                                                                            1 |
+------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '123');
```

```
+-------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '123') |
+-------------------------------------------------------------------------------+
|                                                                             0 |
+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

对于字符串，可以验证其是否匹配某个模式。

```sql
SELECT JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"TiDB"');
```

```
+---------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"TiDB"') |
+---------------------------------------------------------------------+
|                                                                   1 |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"PingCAP"');
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "string", "pattern": "^Ti"}', '"PingCAP"') |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

你可以检查某个值是否匹配指定的命名格式。可校验的格式包括 `ipv4`、`ipv6`、`time`、`date`、`duration`、`email`、`hostname`、`uuid` 和 `uri`。

```sql
SELECT JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"');
```

```
+--------------------------------------------------------+
| JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"') |
+--------------------------------------------------------+
|                                                      1 |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"format": "ipv4"}', '"327.0.0.1"');
```

```
+--------------------------------------------------------+
| JSON_SCHEMA_VALID('{"format": "ipv4"}', '"327.0.0.1"') |
+--------------------------------------------------------+
|                                                      0 |
+--------------------------------------------------------+
1 row in set (0.00 sec)
```

你还可以使用 `enum` 检查字符串是否在数组中。

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"');
```

```
+------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"MySQL"');
```

```
+-------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"MySQL"') |
+-------------------------------------------------------------+
|                                                           1 |
+-------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"SQLite"');
```

```
+--------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"SQLite"') |
+--------------------------------------------------------------+
|                                                            0 |
+--------------------------------------------------------------+
1 row in set (0.00 sec)
```

通过 `anyOf`，你可以组合多个要求，并验证是否满足其中任意一个。

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"');
```

```
+------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"') |
+------------------------------------------------------------------------------------+
|                                                                                  1 |
+------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '["TiDB", "MySQL"]');
```

```
+-----------------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '["TiDB", "MySQL"]') |
+-----------------------------------------------------------------------------------------------+
|                                                                                             0 |
+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '5');
```

```
+-------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '5') |
+-------------------------------------------------------------------------------+
|                                                                             1 |
+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

- 如果 `JSON_SCHEMA_VALID()` 中用于校验的 schema 无效（如 `{"type": "sting"}`），MySQL 可能会接受，但 TiDB 会返回错误。注意 `"sting"` 拼写错误，正确应为 `"string"`。
- MySQL 使用的是较早的 JSON Schema 标准草案版本。

## 另请参阅

- [JSON Schema 参考](https://json-schema.org/understanding-json-schema/reference)
- [JSON 函数总览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)
