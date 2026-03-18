---
title: TO_INT64
summary: Converts a value to INT64 data type.
---
Converts a value to INT64 data type.

## Syntax

```sql
TO_INT64( <expr> )
```

## Examples

```sql
SELECT TO_INT64('123');

┌─────────────────┐
│ to_int64('123') │
├─────────────────┤
│             123 │
└─────────────────┘
```