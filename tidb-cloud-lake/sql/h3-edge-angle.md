---
title: H3_EDGE_ANGLE
---

Returns the average length of the H3 hexagon edge in grades.

## Syntax

```sql
H3_EDGE_ANGLE(res)
```

## Examples

```sql
SELECT H3_EDGE_ANGLE(10);

┌───────────────────────┐
│   h3_edge_angle(10)   │
├───────────────────────┤
│ 0.0006822586214153981 │
└───────────────────────┘
```