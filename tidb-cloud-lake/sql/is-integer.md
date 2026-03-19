---
title: IS_INTEGER
summary: Checks if the input JSON value is an integer.
---

# IS_INTEGER

> **Note:**
>
> Introduced or updated in v1.2.368.

Checks if the input JSON value is an integer.

## Syntax

```sql
IS_INTEGER( <expr> )
```

## Return Type

Returns `true` if the input JSON value is an integer, and `false` otherwise.

## Examples

```sql
SELECT
  IS_INTEGER(PARSE_JSON('123')),
  IS_INTEGER(PARSE_JSON('[1,2,3]'));

┌───────────────────────────────────────────────────────────────────┐
│ is_integer(parse_json('123')) │ is_integer(parse_json('[1,2,3]')) │
├───────────────────────────────┼───────────────────────────────────┤
│ true                          │ false                             │
└───────────────────────────────────────────────────────────────────┘
```
