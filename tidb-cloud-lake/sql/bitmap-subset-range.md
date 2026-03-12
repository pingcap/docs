---
title: BITMAP_SUBSET_IN_RANGE
---

Generates a sub-bitmap of the source bitmap within a specified range.

## Syntax

```sql
BITMAP_SUBSET_IN_RANGE( <bitmap>, <start>, <end> )
```

## Examples

```sql
SELECT BITMAP_SUBSET_IN_RANGE(BUILD_BITMAP([5,7,9]), 6, 9)::String;

┌───────────────────────────────────────────────────────────────┐
│ bitmap_subset_in_range(build_bitmap([5, 7, 9]), 6, 9)::string │
├───────────────────────────────────────────────────────────────┤
│ 7                                                             │
└───────────────────────────────────────────────────────────────┘
```