---
title: AS_DATE
---

Strict casting `VARIANT` values to DATE data type.
If the input data type is not `VARIANT`, the output is `NULL`.
If the type of value in the `VARIANT` does not match the output value, the output is `NULL`.

## Syntax

```sql
AS_DATE( <variant> )
```

## Arguments

| Arguments   | Description       |
|-------------|-------------------|
| `<variant>` | The VARIANT value |

## Return Type

DATE

## Examples

```sql
SELECT as_date(to_date('2025-10-11')::variant);
+-----------------------------------------+
| as_date(to_date('2025-10-11')::variant) |
+-----------------------------------------+
| 2025-10-11                              |
+-----------------------------------------+

SELECT as_date(parse_json('"2024-12-25"')::variant);
+-----------------------------------------------+
| as_date(parse_json('"2024-12-25"')::variant) |
+-----------------------------------------------+
| 2024-12-25                                    |
+-----------------------------------------------+

-- Returns NULL for non-date values
SELECT as_date(parse_json('123'));
+----------------------------+
| as_date(parse_json('123')) |
+----------------------------+
| NULL                       |
+----------------------------+
```
