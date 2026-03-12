---
title: H3_EXACT_EDGE_LENGTH_M
---

Computes the length of this directed edge, in meters.

## Syntax

```sql
H3_EXACT_EDGE_LENGTH_M(h3)
```

## Examples

```sql
SELECT H3_EXACT_EDGE_LENGTH_M(1319695429381652479);

┌─────────────────────────────────────────────┐
│ h3_exact_edge_length_m(1319695429381652479) │
├─────────────────────────────────────────────┤
│                           8267.326832647143 │
└─────────────────────────────────────────────┘
```