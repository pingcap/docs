---
title: GET
summary: Returns an element from an array by index (1-based).
---
Returns an element from an array by index (1-based).

## Syntax

```sql
GET( <array>, <index> )
```

## Aliases

- [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md)

## Examples

```sql
SELECT GET([1, 2], 2), ARRAY_GET([1, 2], 2);

┌───────────────────────────────────────┐
│ get([1, 2], 2) │ array_get([1, 2], 2) │
├────────────────┼──────────────────────┤
│              2 │                    2 │
└───────────────────────────────────────┘
```