---
title: TO_BITMAP
---

Converts a value to BITMAP data type.

## Syntax

```sql
TO_BITMAP( <expr> )
```

## Examples

```sql
SELECT TO_BITMAP('1101');

┌───────────────────┐
│ to_bitmap('1101') │
├───────────────────┤
│ <bitmap binary>   │
└───────────────────┘
```