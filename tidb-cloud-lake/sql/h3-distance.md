---
title: H3_DISTANCE
summary: Returns the grid distance between the given two H3 indexes.
---

# H3_DISTANCE

Returns the grid distance between the given two [H3](https://h3geo.org/) indexes.

## Syntax

```sql
H3_DISTANCE(h3, a_h3)
```

## Examples

```sql
SELECT H3_DISTANCE(599119489002373119, 599119491149856767);

┌─────────────────────────────────────────────────────┐
│ h3_distance(599119489002373119, 599119491149856767) │
├─────────────────────────────────────────────────────┤
│                                                   1 │
└─────────────────────────────────────────────────────┘
```
