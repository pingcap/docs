---
title: ACOS
---

Returns the arc cosine of `x`, that is, the value whose cosine is `x`. Returns NULL if `x` is not in the range -1 to 1.

## Syntax

```sql
ACOS( <x> )
```

## Examples

```sql
SELECT ACOS(1);

┌─────────┐
│ acos(1) │
├─────────┤
│       0 │
└─────────┘
```