---
title: JSON Functions That Validate JSON Documents
summary: Learn about JSON functions that validate JSON documents.
---

# JSON Functions That Validate JSON Documents

This document describes JSON functions that validate JSON documents.

## [JSON_SCHEMA_VALID()](https://dev.mysql.com/doc/refman/8.0/en/json-validation-functions.html#function_json-schema-valid)

The `JSON_SCHEMA_VALID(schema, json_doc)` function validate a JSON document against a schema to ensure data integrity and consistency.

This can be used together with a [CHECK](/constraints.md#check) constraint to do automatic schema validation when a table is modified.

This function follows the [JSON Schema specification](https://json-schema.org/specification).

The supported validation keywords are as follows:

| Validation keyword | Applied type | Description |
|---|---|---|
| `type`                 | Any | Tests the type (such as `array` and `string`) |
| `enum`                 | Any | Tests if a value is in the specified array of values |
| `const`                | Any | Similar to `enum`, but for a single value |
| `allOf`                | Any | Matches all of the specified schemas |
| `anyOf`                | Any | Matches any of the specified schemas |
| `multipleOf`           | `number`/`integer` | Tests if the value is a multiple of the specified value |
| `maximum`              | `number`/`integer` | Tests if the value is below the maximum (inclusive) |
| `exclusiveMaximum`     | `number`/`integer` | Tests if the value is below the maximum (exclusive) |
| `minimum`              | `number`/`integer` | Tests if the value is above the minimum (inclusive) |
| `exclusiveMinimum`     | `number`/`integer` | Tests if the value is above the minimum (exclusive) |
| `maxlength`            | `string` | Tests if the length of the value is not exceeding the specified value |
| `minLength`            | `string` | Tests if the length of the value is at least the specified value |
| `format`               | `string` | Tests if a string matches a named format |
| `pattern`              | `string` | Tests if a string matches a pattern |
| `items`                | `array` | Schema to apply to the items of an array |
| `prefixItems`          | `array` | Schema to apply to positional items of an array |
| `maxItems`             | `array` | Tests if the number of items in the array is not exceeding the specified value |
| `minItems`             | `array` | Tests if the number of items in the array is at least the specified value |
| `uniqueItems`          | `array` | Tests if the items in the array are unique, `true`/`false`|
| `contains`             | `array` | Sets schema for items contained in the array |
| `maxContains`          | `array` | Used together with `contains` to test the maximum times an item can be present |
| `minContains`          | `array` | Used together with `contains` to test the minimum times an item can be present |
| `properties`           | `object` | Schema to apply to the properties of an object |
| `patternProperties`    | `object` | Schema to apply to certain properties based on pattern matching of the property name |
| `additionalProperties` | `object` | Whether additional properties are allowed or not, `true`/`false` |
| `minProperties`        | `object` | Tests the minimum number of properties that an object can have |
| `maxProperties`        | `object` | Tests the maximum number of properties that an object can have |
| `required`             | `object` | Tests if the specified property names exist in an object |

Examples:

For some of the examples, use this JSON document:

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

Use a [user defined variable](/user-defined-variables.md) to hold the JSON document.

```sql
SET @j := '{"fruits": ["orange", "apple", "pear"], "vegetables": ["carrot", "pepper", "kale"]}';
```

Start by testing the type:

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

As you can see in the preceding output, the type of `@j` is `object`. This matches with the output of [`JSON_TYPE()`](/functions-and-operators/json-functions/json-functions-return.md#json_type).

Now validate the presence of certain attributes.

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

In the preceding output, you can see that the validation of the presence of the `fruits` and `vegetables` attributes succeeds.

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

In the preceding output, you can see that the validation of the presence of the `fruits`, `vegetables` and `grains` attributes fails because `grains` is not present.

Now validate that `fruits` is an array.

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

The preceding output confirms that `fruits` is an array.

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

The preceding output shows that `fruits` is **not** a string.

Now verify the number of items in the array.

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

The preceding output shows that `fruits` is an array with at least 3 items.

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

The preceding output shows that `fruits` is **not** an array with at least 4 items. This is because it does not meet the minimum number of items.

For integers values, you can check if they are in a certain range.

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

For a string, you can validate whether it matches a certain pattern.

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

You can check whether a value matches a certain named format. The formats that can be validated include `ipv4`, `ipv6`, `time`, `date`, `duration`, `email`, `hostname`, `uuid`, and `uri`.

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

You can also use `enum` to check if a string is in an array.

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

With `anyOf`, you can combine certain requirements and validate whether any of the requirements is met.

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

## MySQL compatibility

- If the schema to be validated in `JSON_SCHEMA_VALID()` is invalid (such as `{"type": "sting"}`), MySQL might accept it, but TiDB returns an error. Note that there is a spelling mistake in `"sting"`, which should be `"string"`.
- MySQL uses an older draft version of the JSON Schema standard.

## See also

- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/reference)
- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)