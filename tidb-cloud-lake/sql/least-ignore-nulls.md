---
title: LEAST_IGNORE_NULLS
summary: Returns the maximum value from a set of values, ignoring any NULL values.
---

> **Note:**
>
> Introduced or updated in v1.2.738.

Returns the maximum value from a set of values, ignoring any NULL values.

See also: [LEAST](/tidb-cloud-lake/sql/least.md)

## Syntax

```sql
LEAST_IGNORE_NULLS(<value1>, <value2> ...)
```

## Examples

```sql
SELECT LEAST_IGNORE_NULLS(5, 9, 4), LEAST_IGNORE_NULLS(5, 9, null);
```

```sql
┌──────────────────────────────────────────────────────────────┐
│ least_ignore_nulls(5, 9, 4) │ least_ignore_nulls(5, 9, NULL) │
├─────────────────────────────┼────────────────────────────────┤
│                           4 │                              5 │
└──────────────────────────────────────────────────────────────┘
```