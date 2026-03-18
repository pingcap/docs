---
title: SQRT
summary: Returns the square root of a nonnegative number x. Returns Nan for negative input.
---
Returns the square root of a nonnegative number `x`. Returns Nan for negative input.

## Syntax

```sql
SQRT( <x> )
```

## Examples

```sql
SELECT SQRT(4);

┌─────────┐
│ sqrt(4) │
├─────────┤
│       2 │
└─────────┘
```