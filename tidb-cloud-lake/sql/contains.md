---
title: CONTAINS
summary: Checks if the array contains a specific element.
---

# CONTAINS

Checks if the array contains a specific element.

## Syntax

```sql
CONTAINS( <array>, <element> )
```

## Aliases

- [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md)

## Examples

```sql
SELECT ARRAY_CONTAINS([1, 2], 1), CONTAINS([1, 2], 1);

┌─────────────────────────────────────────────────┐
│ array_contains([1, 2], 1) │ contains([1, 2], 1) │
├───────────────────────────┼─────────────────────┤
│ true                      │ true                │
└─────────────────────────────────────────────────┘
```
