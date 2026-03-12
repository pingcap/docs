---
title: BITMAP_SUBSET_LIMIT
---

Generates a sub-bitmap of the source bitmap, beginning with a range from the start value, with a size limit.

## Syntax

```sql
BITMAP_SUBSET_LIMIT( <bitmap>, <start>, <limit> )
```

## Examples

```sql
SELECT BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,4,5]), 2, 2)::String;

┌────────────────────────────────────────────────────────────┐
│ bitmap_subset_limit(build_bitmap([1, 4, 5]), 2, 2)::string │
├────────────────────────────────────────────────────────────┤
│ 4,5                                                        │
└────────────────────────────────────────────────────────────┘
```