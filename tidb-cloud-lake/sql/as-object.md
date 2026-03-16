---
title: AS_OBJECT
---

Strict casting `VARIANT` values to OBJECT data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_OBJECT( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

Variant contains Object

## Examples

```sql
SELECT as_object(parse_json('{"k":"v","a":"b"}'));
+--------------------------------------------+
| as_object(parse_json('{"k":"v","a":"b"}')) |
+--------------------------------------------+
| {"k":"v","a":"b"}                          |
+--------------------------------------------+

SELECT as_object(parse_json('{"name":"John","age":30}'));
+-----------------------------------------------+
| as_object(parse_json('{"name":"John","age":30}')) |
+-----------------------------------------------+
| {"name":"John","age":30}                      |
+-----------------------------------------------+

-- Returns NULL for non-object values
SELECT as_object(parse_json('[1,2,3]'));
+----------------------------------+
| as_object(parse_json('[1,2,3]')) |
+----------------------------------+
| NULL                             |
+----------------------------------+
```
