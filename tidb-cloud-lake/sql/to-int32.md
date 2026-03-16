---
title: TO_INT32
---

Converts a value to INT32 data type.

## Syntax

```sql
TO_INT32( <expr> )
```

## Examples

```sql
SELECT TO_INT32('123');

┌─────────────────┐
│ to_int32('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```