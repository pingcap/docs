---
title: BITMAP_HAS_ANY
---

Checks if the first bitmap has any bit matching the bits in the second bitmap.

## Syntax

```sql
BITMAP_HAS_ANY( <bitmap1>, <bitmap2> )
```

## Examples

```sql
SELECT BITMAP_HAS_ANY(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([1,2]));

┌───────────────────────────────────────────────────────────────┐
│ bitmap_has_any(build_bitmap([1, 4, 5]), build_bitmap([1, 2])) │
├───────────────────────────────────────────────────────────────┤
│ true                                                          │
└───────────────────────────────────────────────────────────────┘
```