---
title: H3_EXACT_EDGE_LENGTH_KM
---

Computes the length of this directed edge, in kilometers.

## Syntax

```sql
H3_EXACT_EDGE_LENGTH_KM(h3)
```

## Examples

```sql
SELECT H3_EXACT_EDGE_LENGTH_KM(1319695429381652479);

┌──────────────────────────────────────────────┐
│ h3_exact_edge_length_km(1319695429381652479) │
├──────────────────────────────────────────────┤
│                            8.267326832647143 │
└──────────────────────────────────────────────┘
```