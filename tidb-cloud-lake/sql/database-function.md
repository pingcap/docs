---
title: DATABASE
---

Returns the name of the currently selected database. If no database is selected, then this function returns `default`.

## Syntax

```sql
DATABASE()
```

## Examples

```sql
SELECT DATABASE();

┌────────────┐
│ database() │
├────────────┤
│ default    │
└────────────┘
```