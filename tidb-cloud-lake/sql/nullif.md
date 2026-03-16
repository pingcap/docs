---
title: NULLIF
---

Returns NULL if two expressions are equal. Otherwise return expr1. They must have the same data type.

## Syntax

```sql
NULLIF(<expr1>, <expr2>)
```

## Examples

```sql
SELECT NULLIF(0, NULL);

┌─────────────────┐
│ nullif(0, null) │
├─────────────────┤
│               0 │
└─────────────────┘
```