---
title: BUILD_BITMAP
---

Converts an array of positive integers to a BITMAP value.

## Syntax

```sql
BUILD_BITMAP( <expr> )
```

## Examples

```sql
SELECT BUILD_BITMAP([1,4,5])::String;

┌─────────────────────────────────┐
│ build_bitmap([1, 4, 5])::string │
├─────────────────────────────────┤
│ 1,4,5                           │
└─────────────────────────────────┘
```