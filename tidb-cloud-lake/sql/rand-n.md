---
title: RAND(n)
---

Returns a random floating-point value v in the range `0 <= v < 1.0`. To obtain a random integer R in the range `i <= R < j`, use the expression `FLOOR(i + RAND() * (j − i))`. Argument `n` is used as the seed value. For equal argument values, RAND(n) returns the same value each time , and thus produces a repeatable sequence of column values.

## Syntax

```sql
RAND( <n>)
```

## Examples

```sql
SELECT RAND(1);

┌────────────────────┐
│       rand(1)      │
├────────────────────┤
│ 0.7133693869548766 │
└────────────────────┘
```
