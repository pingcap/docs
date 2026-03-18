---
title: TO_INT8
summary: Converts a value to INT8 data type.
---

# TO_INT8

Converts a value to INT8 data type.

## Syntax

```sql
TO_INT8( <expr> )
```

## Examples

```sql
SELECT TO_INT8('123');

┌────────────────┐
│ to_int8('123') │
│      UInt8     │
├────────────────┤
│            123 │
└────────────────┘
```
