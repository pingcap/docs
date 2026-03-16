---
title: BITMAP_UNION
---

Counts the number of bits set to 1 in the bitmap by performing a logical UNION operation.

## Syntax

```sql
BITMAP_UNION( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_UNION(TO_BITMAP('1, 3, 5'))::String;

┌────────────────────────────────────────────┐
│ bitmap_union(to_bitmap('1, 3, 5'))::string │
├────────────────────────────────────────────┤
│ 1,3,5                                      │
└────────────────────────────────────────────┘
```