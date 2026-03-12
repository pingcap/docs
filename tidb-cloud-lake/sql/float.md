---
title: TO_FLOAT32
---

Converts a value to FLOAT32 data type.

## Syntax

```sql
TO_FLOAT32( <expr> )
```

## Examples

```sql
SELECT TO_FLOAT32('1.2');

┌───────────────────┐
│ to_float32('1.2') │
├───────────────────┤
│               1.2 │
└───────────────────┘
```