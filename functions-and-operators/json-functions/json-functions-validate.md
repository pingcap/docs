---
title: JSON Functions That Validate JSON Documents
summary: 了解用于验证 JSON 文档的 JSON 函数。
---

# JSON Functions That Validate JSON Documents

本文档描述了用于验证 JSON 文档的 JSON 函数。

> **Note:**
>
> 目前，该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## [JSON_SCHEMA_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-validation-functions.html#function_json-schema-valid)

`JSON_SCHEMA_VALID(schema, json_doc)` 函数用来根据 schema 验证 JSON 文档，以确保数据的完整性和一致性。

可以结合 [CHECK](/constraints.md#check) 约束使用，在修改表时实现自动的 schema 验证。

该函数遵循 [JSON Schema 规范](https://json-schema.org/specification)。

支持的验证关键字如下表：

| 验证关键字 | 适用类型 | 描述 |
|---|---|---|
| `type`                 | 任何 | 测试类型（如 `array` 和 `string`） |
| `enum`                 | 任何 | 测试值是否在指定的值数组中 |
| `const`                | 任何 | 类似 `enum`，但用于单一值 |
| `allOf`                | 任何 | 匹配所有指定的 schema |
| `anyOf`                | 任何 | 匹配任意一个指定的 schema |
| `multipleOf`           | `number`/`integer` | 测试值是否为指定值的倍数 |
| `maximum`              | `number`/`integer` | 测试值是否小于等于最大值 |
| `exclusiveMaximum`     | `number`/`integer` | 测试值是否小于最大值（不包括最大值） |
| `minimum`              | `number`/`integer` | 测试值是否大于等于最小值 |
| `exclusiveMinimum`     | `number`/`integer` | 测试值是否大于最小值（不包括最小值） |
| `maxlength`            | `string` | 测试值的长度是否不超过指定值 |
| `minLength`            | `string` | 测试值的长度是否至少为指定值 |
| `format`               | `string` | 测试字符串是否符合命名的格式 |
| `pattern`              | `string` | 测试字符串是否匹配某个模式 |
| `items`                | `array` | 应用到数组元素的 schema |
| `prefixItems`          | `array` | 应用到数组位置元素的 schema |
| `maxItems`             | `array` | 测试数组元素个数是否不超过指定值 |
| `minItems`             | `array` | 测试数组元素个数是否不少于指定值 |
| `uniqueItems`          | `array` | 测试数组中的元素是否唯一，`true`/`false` |
| `contains`             | `array` | 设置数组中包含元素的 schema |
| `maxContains`          | `array` | 与 `contains` 搭配，测试元素最多出现的次数 |
| `minContains`          | `array` | 与 `contains` 搭配，测试元素最少出现的次数 |
| `properties`           | `object` | 应用到对象属性的 schema |
| `patternProperties`    | `object` | 根据属性名的匹配模式应用 schema |
| `additionalProperties` | `object` | 是否允许额外的属性，`true`/`false` |
| `minProperties`        | `object` | 测试对象的最小属性数 |
| `maxProperties`        | `object` | 测试对象的最大属性数 |
| `required`             | `object` | 测试对象是否包含指定的属性名 |

示例：

对于一些示例，使用以下 JSON 文档：

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

使用 [用户定义变量](/user-defined-variables.md) 来保存该 JSON 文档。

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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
```

从上面的输出可以看出，`@j` 的类型是 `object`。这与 [`JSON_TYPE()`](/functions-and-operators/json-functions/json-functions-return.md#json_type) 的输出一致。

现在验证某些属性的存在。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j);
```

```
+---------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables"]}',@j) |
+---------------------------------------------------------------+
|                                                             1 |
+---------------------------------------------------------------+
1 行，耗时 0.00 秒
```

在上述输出中，可以看到验证 `fruits` 和 `vegetables` 属性存在成功。

```sql
SELECT JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"required": ["fruits","vegetables","grains"]}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 行，耗时 0.00 秒
```

在上述输出中，可以看到验证 `fruits`、`vegetables` 和 `grains` 属性存在失败，因为 `grains` 不存在。

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
1 行，耗时 0.01 秒
```

上述输出确认 `fruits` 是数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j);
```

```
+------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "string"}}}',@j) |
+------------------------------------------------------------------------+
|                                                                      0 |
+------------------------------------------------------------------------+
1 行，耗时 0.00 秒
```

上述输出显示 `fruits` 不是字符串。

现在验证数组中的元素个数。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 3}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    1 |
+--------------------------------------------------------------------------------------+
1 行，耗时 0.00 秒
```

上述输出显示 `fruits` 是一个至少包含 3 个元素的数组。

```sql
SELECT JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j);
```

```
+--------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"properties": {"fruits": {"type": "array", "minItems": 4}}}',@j) |
+--------------------------------------------------------------------------------------+
|                                                                                    0 |
+--------------------------------------------------------------------------------------+
1 行，耗时 0.00 秒
```

上述输出显示 `fruits` 不是一个至少包含 4 个元素的数组，因为它不满足最小元素数。

对于整数值，可以验证它们是否在某个范围内。

```sql
SELECT JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42');
+------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"type": "integer", "minimum": 40, "maximum": 45}', '42') |
+------------------------------------------------------------------------------+
|                                                                            1 |
+------------------------------------------------------------------------------+
1 行，耗时 0.01 秒
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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
```

你还可以验证值是否符合某个命名的格式。支持的格式包括 `ipv4`、`ipv6`、`time`、`date`、`duration`、`email`、`hostname`、`uuid` 和 `uri`。

```sql
SELECT JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"');
```

```
+--------------------------------------------------------+
| JSON_SCHEMA_VALID('{"format": "ipv4"}', '"127.0.0.1"') |
+--------------------------------------------------------+
|                                                      1 |
+--------------------------------------------------------+
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
```

你还可以使用 `enum` 来检查字符串是否在数组中。

```sql
SELECT JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"');
```

```
+------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"enum": ["TiDB", "MySQL"]}', '"TiDB"') |
+------------------------------------------------------------+
|                                                          1 |
+------------------------------------------------------------+
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
```

使用 `anyOf`，可以组合某些要求，验证是否满足其中任意一项。

```sql
SELECT JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"');
```

```
+------------------------------------------------------------------------------------+
| JSON_SCHEMA_VALID('{"anyOf": [{"type": "string"},{"type": "integer"}]}', '"TiDB"') |
+------------------------------------------------------------------------------------+
|                                                                                  1 |
+------------------------------------------------------------------------------------+
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
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
1 行，耗时 0.00 秒
```

## MySQL 兼容性

- 如果 `JSON_SCHEMA_VALID()` 中验证的 schema 无效（例如 `{"type": "sting"}`），MySQL 可能会接受，但 TiDB 会返回错误。注意，`"sting"` 拼写错误，应为 `"string"`。
- MySQL 使用的是较旧版本的 JSON Schema 标准草案。

## 相关链接

- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/reference)
- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)