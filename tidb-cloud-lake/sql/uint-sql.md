---
title: TO_UINT32
---

Converts a value to UINT32 data type.

## Syntax

```sql
TO_UINT32( <expr> )
```

## Examples

```sql
SELECT TO_UINT32('123');

┌──────────────────┐
│ to_uint32('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```