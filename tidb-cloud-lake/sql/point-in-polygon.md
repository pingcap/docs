---
title: POINT_IN_POLYGON
---

Calculates whether a given point falls within the polygon formed by joining multiple points. A polygon is a closed shape connected by coordinate pairs in the order they appear. Changing the order of coordinate pairs can result in a different shape.

## Syntax

```sql
POINT_IN_POLYGON((x,y), [(a,b), (c,d), (e,f) ... ])
```

## Examples

```sql
SELECT POINT_IN_POLYGON((3., 3.), [(6, 0), (8, 4), (5, 8), (0, 2)]);

┌────────────────────────────────────────────────────────────┐
│ point_in_polygon((3, 3), [(6, 0), (8, 4), (5, 8), (0, 2)]) │
├────────────────────────────────────────────────────────────┤
│                                                          1 │
└────────────────────────────────────────────────────────────┘
```