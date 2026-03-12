---
title: BITMAP_INTERSECT
---

Counts the number of bits set to 1 in the bitmap by performing a logical INTERSECT operation.

## Syntax

```sql
BITMAP_INTERSECT( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_INTERSECT(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────────┐
│ bitmap_intersect(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────────┤
│ 1,3,5                                          │
└────────────────────────────────────────────────┘
```