---
title: H3_HEX_AREA_M2
---

Returns the average hexagon area in square meters at the given resolution. Excludes pentagons. 

## Syntax

```sql
H3_HEX_AREA_M2(res)
```

## Examples

```sql
SELECT H3_HEX_AREA_M2(1);

┌───────────────────┐
│ h3_hex_area_m2(1) │
├───────────────────┤
│ 609788441794.1339 │
└───────────────────┘
```