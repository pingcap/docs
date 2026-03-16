---
title: XXHASH32
---

Calculates an xxHash32 32-bit hash value for a string. The value is returned as a UInt32 or NULL if the argument was NULL.

## Syntax

```sql
XXHASH32(expr)
```

## Examples

```sql
SELECT XXHASH32('1234567890');

┌────────────────────────┐
│ xxhash32('1234567890') │
├────────────────────────┤
│             3896585587 │
└────────────────────────┘
```