---
title: LN
---

Returns the natural logarithm of `x`; that is, the base-e logarithm of `x`. If x is less than or equal to 0.0E0, the function returns NULL.

## Syntax

```sql
LN( <x> )
```

## Examples

```sql
SELECT LN(2);

┌────────────────────┐
│        ln(2)       │
├────────────────────┤
│ 0.6931471805599453 │
└────────────────────┘
```