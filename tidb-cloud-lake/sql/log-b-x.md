---
title: "LOG(b, x)"
---

Returns the base-b logarithm of `x`. If `x` is less than or equal to 0.0E0, the function returns NULL.

## Syntax

```sql
LOG( <b, x> )
```

## Examples

```sql
SELECT LOG(2, 65536);

┌───────────────┐
│ log(2, 65536) │
├───────────────┤
│            16 │
└───────────────┘
```