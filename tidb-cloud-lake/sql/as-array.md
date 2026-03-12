---
title: AS_ARRAY
---

Strict casting `VARIANT` values to ARRAY data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_ARRAY( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

Variant contains Array

## Examples

```sql
SELECT as_array(parse_json('[1,2,3]'));
+---------------------------------+
| as_array(parse_json('[1,2,3]')) |
+---------------------------------+
| [1,2,3]                         |
+---------------------------------+

SELECT as_array(parse_json('["a","b","c"]'));
+---------------------------------------+
| as_array(parse_json('["a","b","c"]')) |
+---------------------------------------+
| ["a","b","c"]                         |
+---------------------------------------+

-- Returns NULL for non-array values
SELECT as_array(parse_json('{"key":"value"}'));
+-----------------------------------------+
| as_array(parse_json('{"key":"value"}')) |
+-----------------------------------------+
| NULL                                    |
+-----------------------------------------+
```
