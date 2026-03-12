---
title: BITMAP_MIN
---

Gets the minimum value in the bitmap.

## Syntax

```sql
BITMAP_MIN( <bitmap> )
```

## Examples

```sql
SELECT BITMAP_MIN(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────┐
│ bitmap_min(build_bitmap([1, 4, 5])) │
├─────────────────────────────────────┤
│                                   1 │
└─────────────────────────────────────┘
```