---
title: ROUND
---

Rounds the argument x to d decimal places. The rounding algorithm depends on the data type of x. d defaults to 0 if not specified. d can be negative to cause d digits left of the decimal point of the value x to become zero. The maximum absolute value for d is 30; any digits in excess of 30 (or -30) are truncated.

When using this function's result in calculations, be aware of potential precision issues due to its return data type being DOUBLE, which may affect final accuracy:

```sql
SELECT ROUND(4/7, 4) - ROUND(3/7, 4); -- Result: 0.14280000000000004
SELECT ROUND(4/7, 4)::DECIMAL(8,4) - ROUND(3/7, 4)::DECIMAL(8,4); -- Result: 0.1428
```

## Syntax

```sql
ROUND( <x, d> )
```

## Examples

```sql
SELECT ROUND(0.123, 2);

┌─────────────────┐
│ round(0.123, 2) │
├─────────────────┤
│ 0.12            │
└─────────────────┘
```