---
title: "LOG(x)"
---

Returns the natural logarithm of `x`. If x is less than or equal to 0.0E0, the function returns NULL.

## Syntax

```sql
LOG( <x> )
```

## Examples

```sql
SELECT LOG(2);

┌────────────────────┐
│       log(2)       │
├────────────────────┤
│ 0.6931471805599453 │
└────────────────────┘
```