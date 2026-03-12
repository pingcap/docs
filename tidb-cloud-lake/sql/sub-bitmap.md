---
title: SUB_BITMAP
---

Generates a sub-bitmap of the source bitmap, beginning from the start index, with a specified size.

## Syntax

```sql
SUB_BITMAP( <bitmap>, <start>, <size> )
```

## Examples

```sql
SELECT SUB_BITMAP(BUILD_BITMAP([1, 2, 3, 4, 5]), 1, 3)::String;

┌─────────────────────────────────────────────────────────┐
│ sub_bitmap(build_bitmap([1, 2, 3, 4, 5]), 1, 3)::string │
├─────────────────────────────────────────────────────────┤
│ 2,3,4                                                   │
└─────────────────────────────────────────────────────────┘
```