---
title: STRIP_NULL_VALUE
summary: Converts a JSON null value to a SQL NULL value. All other variant values are passed unchanged.
---

# STRIP_NULL_VALUE

> **Note:**
>
> Introduced or updated in v1.2.762.

Converts a JSON null value to a SQL NULL value. All other variant values are passed unchanged.

## Syntax

```sql
STRIP_NULL_VALUE(<variant_expr>)
```

## Arguments

An expression of type VARIANT.

## Return Type

- If the expression is a JSON null value, the function returns a SQL NULL.
- If the expression is not a JSON null value, the function returns the input value.

## Examples

```sql
SELECT STRIP_NULL_VALUE(PARSE_JSON('null')) AS value;

╭───────╮
│ value │
├───────┤
│ NULL  │
╰───────╯

SELECT STRIP_NULL_VALUE(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────────────────╮
│                 value                 │
├───────────────────────────────────────┤
│ {"age":30,"city":null,"name":"Alice"} │
╰───────────────────────────────────────╯
```
