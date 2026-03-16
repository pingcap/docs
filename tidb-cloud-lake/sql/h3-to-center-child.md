---
title: H3_TO_CENTER_CHILD
---

Returns the center child index at the specified resolution.

## Syntax

```sql
H3_TO_CENTER_CHILD(h3, res)
```

## Examples

```sql
SELECT H3_TO_CENTER_CHILD(599119489002373119, 15);

┌────────────────────────────────────────────┐
│ h3_to_center_child(599119489002373119, 15) │
├────────────────────────────────────────────┤
│                         644155484202336256 │
└────────────────────────────────────────────┘
```