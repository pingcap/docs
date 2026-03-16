---
title: TO_FLOAT64
---

Converts a value to FLOAT64 data type.

## Syntax

```sql
TO_FLOAT64( <expr> )
```

## Examples

```sql
SELECT TO_FLOAT64('1.2');

┌───────────────────┐
│ to_float64('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```