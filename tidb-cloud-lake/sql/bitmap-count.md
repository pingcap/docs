---
title: BITMAP_AND_COUNT
---

Counts the number of bits set to 1 in the bitmap by performing a logical AND operation.

## Syntax

```sql
BITMAP_AND_COUNT( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_AND_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_and_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```