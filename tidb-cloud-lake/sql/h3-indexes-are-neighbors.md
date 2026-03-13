---
title: H3_INDEXES_ARE_NEIGHBORS
---

Returns whether or not the provided [H3](https://eng.uber.com/h3/) indexes are neighbors.

## Syntax

```sql
H3_INDEXES_ARE_NEIGHBORS(h3, a_h3)
```

## Examples

```sql
SELECT H3_INDEXES_ARE_NEIGHBORS(644325524701193974, 644325524701193897);

┌──────────────────────────────────────────────────────────────────┐
│ h3_indexes_are_neighbors(644325524701193974, 644325524701193897) │
├──────────────────────────────────────────────────────────────────┤
│ true                                                             │
└──────────────────────────────────────────────────────────────────┘
```