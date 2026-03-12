---
title: AS_BINARY
---

Strict casting `VARIANT` values to BINARY data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_BINARY( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

BINARY

## Examples

```sql
SELECT as_binary(to_binary('abcd')::variant);
+---------------------------------------+
| as_binary(to_binary('abcd')::variant) |
+---------------------------------------+
| 61626364                              |
+---------------------------------------+

SELECT as_binary(to_binary('hello')::variant);
+-----------------------------------------+
| as_binary(to_binary('hello')::variant) |
+-----------------------------------------+
| 68656C6C6F                              |
+-----------------------------------------+

-- Returns NULL for non-binary values
SELECT as_binary(parse_json('"text"'));
+---------------------------------+
| as_binary(parse_json('"text"')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```
