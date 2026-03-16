---
title: LOG2
---

Returns the base-2 logarithm of `x`. If `x` is less than or equal to 0.0E0, the function returns NULL.

## Syntax

```sql
LOG2( <x> )
```

## Examples

```sql
SELECT LOG2(65536);

┌─────────────┐
│ log2(65536) │
├─────────────┤
│          16 │
└─────────────┘
```