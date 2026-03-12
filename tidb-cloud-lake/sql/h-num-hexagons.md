---
title: H3_NUM_HEXAGONS
---

Returns the number of unique [H3](https://eng.uber.com/h3/) indexes at the given resolution. 

## Syntax

```sql
H3_NUM_HEXAGONS(res)
```

## Examples

```sql
SELECT H3_NUM_HEXAGONS(10);

┌─────────────────────┐
│ h3_num_hexagons(10) │
├─────────────────────┤
│         33897029882 │
└─────────────────────┘
```