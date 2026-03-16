---
title: AS_STRING
---

Strict casting `VARIANT` values to VARCHAR data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_STRING( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

VARCHAR

## Examples

```sql
SELECT as_string(parse_json('"abc"'));
+--------------------------------+
| as_string(parse_json('"abc"')) |
+--------------------------------+
| abc                            |
+--------------------------------+

SELECT as_string(parse_json('"hello world"'));
+----------------------------------------+
| as_string(parse_json('"hello world"')) |
+----------------------------------------+
| hello world                            |
+----------------------------------------+

-- Returns NULL for non-string values
SELECT as_string(parse_json('123'));
+------------------------------+
| as_string(parse_json('123')) |
+------------------------------+
| NULL                         |
+------------------------------+
```
