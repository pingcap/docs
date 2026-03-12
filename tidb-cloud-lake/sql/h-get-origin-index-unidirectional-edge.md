---
title: H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE
---

Returns the origin hexagon index from the unidirectional edge H3Index.

## Syntax

```sql
H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(h3)
```

## Examples

```sql
SELECT H3_GET_ORIGIN_INDEX_FROM_UNIDIRECTIONAL_EDGE(1248204388774707199);

┌───────────────────────────────────────────────────────────────────┐
│ h3_get_origin_index_from_unidirectional_edge(1248204388774707199) │
├───────────────────────────────────────────────────────────────────┤
│                                                599686042433355775 │
└───────────────────────────────────────────────────────────────────┘
```