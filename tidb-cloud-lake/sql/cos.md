---
title: COS
summary: Returns the cosine of x, where x is given in radians.
---
Returns the cosine of `x`, where `x` is given in radians.

## Syntax

```sql
COS( <x> )
```

## Examples

```sql
SELECT COS(PI());

┌───────────┐
│ cos(pi()) │
├───────────┤
│        -1 │
└───────────┘
```