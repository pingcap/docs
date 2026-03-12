---
title: AS_FLOAT
---

Strict casting `VARIANT` values to DOUBLE data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_FLOAT( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

DOUBLE

## Examples

```sql
SELECT as_float(parse_json('12.34'));
+-------------------------------+
| as_float(parse_json('12.34')) |
+-------------------------------+
| 12.34                         |
+-------------------------------+

SELECT as_float(parse_json('123'));
+-----------------------------+
| as_float(parse_json('123')) |
+-----------------------------+
| 123.0                       |
+-----------------------------+

-- Returns NULL for non-numeric values
SELECT as_float(parse_json('"abc"'));
+-------------------------------+
| as_float(parse_json('"abc"')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```
