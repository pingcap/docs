---
title: CONTAINS
---

Checks if the array contains a specific element.

## Syntax

```sql
CONTAINS( <array>, <element> )
```

## Aliases

- [ARRAY_CONTAINS](array-contains.md)

## Examples

```sql
SELECT ARRAY_CONTAINS([1, 2], 1), CONTAINS([1, 2], 1);

┌─────────────────────────────────────────────────┐
│ array_contains([1, 2], 1) │ contains([1, 2], 1) │
├───────────────────────────┼─────────────────────┤
│ true                      │ true                │
└─────────────────────────────────────────────────┘
```