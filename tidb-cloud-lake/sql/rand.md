---
title: RAND()
---

Returns a random floating-point value v in the range `0 <= v < 1.0`. To obtain a random integer R in the range `i <= R < j`, use the expression `FLOOR(i + RAND() * (j − i))`.

## Syntax

```sql
RAND()
```

## Examples

```sql
SELECT RAND();

┌────────────────────┐
│       rand()       │
├────────────────────┤
│ 0.5191511074382174 │
└────────────────────┘
```
