---
title: H3_TO_PARENT
---

Returns the parent index containing the `h3` at resolution `parent_res`. Returning 0 means an error occurred.

## Syntax

```sql
H3_TO_PARENT(h3, parent_res)
```

## Examples

```sql
SELECT H3_TO_PARENT(635318325446452991, 12);

┌──────────────────────────────────────┐
│ h3_to_parent(635318325446452991, 12) │
├──────────────────────────────────────┤
│                   630814725819082751 │
└──────────────────────────────────────┘
```