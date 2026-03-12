---
title: LOG10
---

Returns the base-10 logarithm of `x`. If `x` is less than or equal to 0.0E0, the function returns NULL.

## Syntax

```sql
LOG10( <x> )
```

## Examples

```sql
SELECT LOG10(100);

┌────────────┐
│ log10(100) │
├────────────┤
│          2 │
└────────────┘
```