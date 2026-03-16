---
title: BITMAP_NOT_COUNT
---

Counts the number of bits set to 0 in the bitmap by performing a logical NOT operation.

## Syntax

```sql
BITMAP_NOT_COUNT( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_NOT_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_not_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```