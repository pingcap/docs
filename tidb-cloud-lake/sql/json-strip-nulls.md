---
title: JSON_STRIP_NULLS
summary: Removes all properties with null values from a JSON object.
---

# JSON_STRIP_NULLS

> **Note:**
>
> Introduced or updated in v1.2.762.

Removes all properties with null values from a JSON object.

## Syntax

```sql
JSON_STRIP_NULLS(<variant_expr>)
```

## Arguments

An expression of type VARIANT.

## Return Type

VARIANT.

## Examples

```sql
SELECT JSON_STRIP_NULLS(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────╮
│           value           │
├───────────────────────────┤
│ {"age":30,"name":"Alice"} │
╰───────────────────────────╯
```
