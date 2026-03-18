---
title: LEAST
summary: Returns the minimum value from a set of values. If any value in the set is NULL, the function returns NULL.
---

> **Note:**
>
> Introduced or updated in v1.2.738.

Returns the minimum value from a set of values. If any value in the set is `NULL`, the function returns `NULL`.

See also: [LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md)

## Syntax

```sql
LEAST(<value1>, <value2> ...)
```

## Examples

```sql
SELECT LEAST(5, 9, 4), LEAST(5, 9, null);
```

```
┌────────────────────────────────────┐
│ least(5, 9, 4) │ least(5, 9, NULL) │
├────────────────┼───────────────────┤
│              4 │ NULL              │
└────────────────────────────────────┘
```