---
title: AS_DECIMAL
---

Strict casting `VARIANT` values to DECIMAL data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_DECIMAL( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

DECIMAL

## Examples

```sql
SELECT as_decimal(parse_json('12.34'));
+---------------------------------+
| as_decimal(parse_json('12.34')) |
+---------------------------------+
| 12.34                           |
+---------------------------------+

SELECT as_decimal(parse_json('123.456789'));
+--------------------------------------+
| as_decimal(parse_json('123.456789')) |
+--------------------------------------+
| 123.456789                           |
+--------------------------------------+

-- Returns NULL for non-decimal values
SELECT as_decimal(parse_json('"abc"'));
+---------------------------------+
| as_decimal(parse_json('"abc"')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```
