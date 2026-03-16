---
title: H3_EDGE_LENGTH_KM
---

Returns the average hexagon edge length in kilometers at the given resolution. Excludes pentagons.

## Syntax

```sql
H3_EDGE_LENGTH_KM(res)
```

## Examples

```sql
SELECT H3_EDGE_LENGTH_KM(1);

┌──────────────────────┐
│ h3_edge_length_km(1) │
├──────────────────────┤
│    483.0568390711111 │
└──────────────────────┘
```