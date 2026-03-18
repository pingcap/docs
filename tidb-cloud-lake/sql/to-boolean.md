---
title: TO_BOOLEAN
summary: Converts a value to BOOLEAN data type.
---
Converts a value to BOOLEAN data type.

## Syntax

```sql
TO_BOOLEAN( <expr> )
```

## Examples

```sql
SELECT TO_BOOLEAN('true');

┌────────────────────┐
│ to_boolean('true') │
├────────────────────┤
│ true               │
└────────────────────┘
```