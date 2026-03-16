---
title: IS_NULL
---

Checks whether a value is NULL.

## Syntax

```sql
IS_NULL(<expr>)
```

## Examples

```sql
SELECT IS_NULL(1);

┌────────────┐
│ is_null(1) │
├────────────┤
│ false      │
└────────────┘
```