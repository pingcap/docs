---
title: TO_VARIANT
---

Converts a value to VARIANT data type.

## Syntax

```sql
TO_VARIANT( <expr> )
```

## Examples

```sql
SELECT TO_VARIANT(TO_BITMAP('100,200,300'));

┌──────────────────────────────────────┐
│ to_variant(to_bitmap('100,200,300')) │
├──────────────────────────────────────┤
│ [100,200,300]                        │
└──────────────────────────────────────┘
```