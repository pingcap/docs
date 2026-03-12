---
title: BITMAP_COUNT
---

Counts the number of bits set to 1 in the bitmap.

## Syntax

```sql
BITMAP_COUNT( <bitmap> )
```

## Aliases

- [BITMAP_CARDINALITY](bitmap-cardinality.md)

## Examples

```sql
SELECT BITMAP_COUNT(BUILD_BITMAP([1,4,5])), BITMAP_CARDINALITY(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ bitmap_count(build_bitmap([1, 4, 5])) │ bitmap_cardinality(build_bitmap([1, 4, 5])) │
├───────────────────────────────────────┼─────────────────────────────────────────────┤
│                                     3 │                                           3 │
└─────────────────────────────────────────────────────────────────────────────────────┘
```