---
title: TO_UINT64
---

Converts a value to UINT64 data type.

## Syntax

```sql
TO_UINT64( <expr> )
```

## Examples

```sql
SELECT TO_UINT64('123');

┌──────────────────┐
│ to_uint64('123') │
├──────────────────┤
│              123 │
└──────────────────┘
```