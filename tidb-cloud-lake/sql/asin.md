---
title: ASIN
---

Returns the arc sine of `x`, that is, the value whose sine is `x`. Returns NULL if `x` is not in the range -1 to 1.

## Syntax

```sql
ASIN( <x> )
```

## Examples

```sql
SELECT ASIN(0.2);

┌────────────────────┐
│      asin(0.2)     │
├────────────────────┤
│ 0.2013579207903308 │
└────────────────────┘
```