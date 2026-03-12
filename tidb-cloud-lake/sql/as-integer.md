---
title: AS_INTEGER
---

Strict casting `VARIANT` values to BIGINT data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_INTEGER( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

BIGINT

## Examples

```sql
SELECT as_integer(parse_json('123'));
+-------------------------------+
| as_integer(parse_json('123')) |
+-------------------------------+
| 123                           |
+-------------------------------+

SELECT as_integer(parse_json('-456'));
+--------------------------------+
| as_integer(parse_json('-456')) |
+--------------------------------+
| -456                           |
+--------------------------------+

-- Returns NULL for non-integer values
SELECT as_integer(parse_json('12.34'));
+---------------------------------+
| as_integer(parse_json('12.34')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```
