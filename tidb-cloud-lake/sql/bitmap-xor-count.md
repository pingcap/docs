---
title: BITMAP_XOR_COUNT
---

Counts the number of bits set to 1 in the bitmap by performing a logical XOR (exclusive OR) operation.

## Syntax

```sql
BITMAP_XOR_COUNT( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_XOR_COUNT(TO_BITMAP('1, 3, 5'));

┌────────────────────────────────────────┐
│ bitmap_xor_count(to_bitmap('1, 3, 5')) │
├────────────────────────────────────────┤
│                                      3 │
└────────────────────────────────────────┘
```