---
title: H3_CELL_AREA_RADS2
---

Returns the exact area of specific cell in square radians.

## Syntax

```sql
H3_CELL_AREA_RADS2(h3)
```

## Examples

```sql
SELECT H3_CELL_AREA_RADS2(599119489002373119);

┌────────────────────────────────────────┐
│ h3_cell_area_rads2(599119489002373119) │
├────────────────────────────────────────┤
│                0.000003148224310427697 │
└────────────────────────────────────────┘
```