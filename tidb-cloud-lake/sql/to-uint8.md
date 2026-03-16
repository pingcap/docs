---
title: TO_UINT8
---

Converts a value to UINT8 data type.

## Syntax

```sql
TO_UINT8( <expr> )
```

## Examples

```sql
SELECT TO_UINT8('123');

┌─────────────────┐
│ to_uint8('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```