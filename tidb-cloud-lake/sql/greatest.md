---
title: GREATEST
summary: Returns the maximum value from a set of values. If any value in the set is NULL, the function returns NULL.
---

# GREATEST

Returns the maximum value from a set of values. If any value in the set is `NULL`, the function returns `NULL`.

See also: [GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md)

## Syntax

```sql
GREATEST(<value1>, <value2> ...)
```

## Examples

```sql
SELECT GREATEST(5, 9, 4), GREATEST(5, 9, null);
```

```sql
┌──────────────────────────────────────────┐
│ greatest(5, 9, 4) │ greatest(5, 9, NULL) │
├───────────────────┼──────────────────────┤
│                 9 │ NULL                 │
└──────────────────────────────────────────┘
```
