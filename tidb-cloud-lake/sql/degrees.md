---
title: DEGREES
---

Returns the argument `x`, converted from radians to degrees, where `x` is given in radians.

## Syntax

```sql
DEGREES( <x> )
```

## Examples

```sql
SELECT DEGREES(PI());

┌───────────────┐
│ degrees(pi()) │
├───────────────┤
│           180 │
└───────────────┘
```