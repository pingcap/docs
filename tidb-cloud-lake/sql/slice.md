---
title: SLICE
---

Extracts a slice from the array by index (1-based).

## Syntax

```sql
SLICE( <array>, <start>[, <end>] )
```

## Aliases

- [ARRAY_SLICE](array-slice.md)

## Examples

```sql
SELECT ARRAY_SLICE([1, 21, 32, 4], 2, 3), SLICE([1, 21, 32, 4], 2, 3);

┌─────────────────────────────────────────────────────────────────┐
│ array_slice([1, 21, 32, 4], 2, 3) │ slice([1, 21, 32, 4], 2, 3) │
├───────────────────────────────────┼─────────────────────────────┤
│ [21,32]                           │ [21,32]                     │
└─────────────────────────────────────────────────────────────────┘
```