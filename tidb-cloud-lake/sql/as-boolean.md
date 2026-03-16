---
title: AS_BOOLEAN
---

Strict casting `VARIANT` values to BOOLEAN data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_BOOLEAN( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

BOOLEAN

## Examples

```sql
SELECT as_boolean(parse_json('true'));
+--------------------------------+
| as_boolean(parse_json('true')) |
+--------------------------------+
| 1                              |
+--------------------------------+

SELECT as_boolean(parse_json('false'));
+---------------------------------+
| as_boolean(parse_json('false')) |
+---------------------------------+
| 0                               |
+---------------------------------+

-- Returns NULL for non-boolean values
SELECT as_boolean(parse_json('123'));
+-------------------------------+
| as_boolean(parse_json('123')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```
