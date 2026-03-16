---
title: JSON_CONTAINS_IN_LEFT
title_includes: JSON_CONTAINS_IN_RIGHT
---

Tests containment relationships between two `VARIANT` values:

- `JSON_CONTAINS_IN_LEFT(left, right)` returns `TRUE` when *left* contains *right* (i.e., *left* is a superset).
- `JSON_CONTAINS_IN_RIGHT(left, right)` returns `TRUE` when *right* contains *left*.

Containment works for both JSON objects and arrays.

## Syntax

```sql
JSON_CONTAINS_IN_LEFT(<variant_left>, <variant_right>)
JSON_CONTAINS_IN_RIGHT(<variant_left>, <variant_right>)
```

## Return Type

`BOOLEAN`

## Examples

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('{"a":1,"b":{"c":2}}'),
                             PARSE_JSON('{"b":{"c":2}}')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ true         │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('[1,2,3]'),
                             PARSE_JSON('[2,3]')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ true         │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('[1,2]'),
                             PARSE_JSON('[2,4]')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ false        │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_RIGHT(PARSE_JSON('{"a":1}'),
                              PARSE_JSON('{"a":1,"b":2}')) AS right_contains;

┌───────────────┐
│ right_contains│
├───────────────┤
│ true          │
└───────────────┘
```
