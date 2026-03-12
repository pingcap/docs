---
title: BITMAP_XOR
---

Performs a bitwise XOR (exclusive OR) operation on the two bitmaps.

## Syntax

```sql
BITMAP_XOR( <bitmap1>, <bitmap2> )
```

## Examples

```sql
SELECT BITMAP_XOR(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([5,6,7]))::String;

┌──────────────────────────────────────────────────────────────────────┐
│ bitmap_xor(build_bitmap([1, 4, 5]), build_bitmap([5, 6, 7]))::string │
├──────────────────────────────────────────────────────────────────────┤
│ 1,4,6,7                                                              │
└──────────────────────────────────────────────────────────────────────┘
```