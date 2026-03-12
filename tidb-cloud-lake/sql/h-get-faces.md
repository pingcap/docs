---
title: H3_GET_FACES
---

Finds all icosahedron faces intersected by the given [H3](https://eng.uber.com/h3/) index. Faces are represented as integers from 0-19.

## Syntax

```sql
H3_GET_FACES(h3)
```

## Examples

```sql
SELECT H3_GET_FACES(599119489002373119);

┌──────────────────────────────────┐
│ h3_get_faces(599119489002373119) │
├──────────────────────────────────┤
│ [0,1,2,3,4]                      │
└──────────────────────────────────┘
```