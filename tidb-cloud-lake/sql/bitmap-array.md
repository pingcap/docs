---
title: BITMAP_TO_ARRAY
---

Converts a Bitmap into an Array.

## Syntax

```sql
BITMAP_TO_ARRAY( <bitmap> )
```

## Return Type

`Array (UInt64)`

## Examples

```sql
SELECT BITMAP_TO_ARRAY(TO_BITMAP('1, 3, 5'));

╭───────────────────────────────────────╮
│ bitmap_to_array(to_bitmap('1, 3, 5')) │
├───────────────────────────────────────┤
│ [1,3,5]                               │
╰───────────────────────────────────────╯
```
