---
title: ATAN
---

Returns the arc tangent of `x`, that is, the value whose tangent is `x`.

## Syntax

```sql
ATAN( <x> )
```

## Examples

```sql
SELECT ATAN(-2);

┌─────────────────────┐
│     atan((- 2))     │
├─────────────────────┤
│ -1.1071487177940906 │
└─────────────────────┘
```