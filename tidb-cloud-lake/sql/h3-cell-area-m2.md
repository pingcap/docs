---
title: H3_CELL_AREA_M2
---

Returns the exact area of specific cell in square meters.

## Syntax

```sql
H3_CELL_AREA_M2(h3)
```

## Examples

```sql
SELECT H3_CELL_AREA_M2(599119489002373119);

┌─────────────────────────────────────┐
│ h3_cell_area_m2(599119489002373119) │
├─────────────────────────────────────┤
│                  127785582.60809991 │
└─────────────────────────────────────┘
```