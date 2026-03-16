---
title: ARRAY_STDDEV_POP
title_includes: ARRAY_STD
---

Computes the population standard deviation of numeric array values. `NULL` entries are ignored; non-numeric entries raise an error.

## Syntax

```sql
ARRAY_STDDEV_POP(<array>)
```

## Return Type

Floating-point.

## Examples

```sql
SELECT ARRAY_STDDEV_POP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_pop;

┌────────────┐
│ stddev_pop │
├────────────┤
│          2 │
└────────────┘
```

```sql
SELECT ARRAY_STDDEV_POP([1.5, 2.5, NULL, 3.5]) AS stddev_pop_null;

┌─────────────────┐
│ stddev_pop_null │
├─────────────────┤
│ 0.816496580927726 │
└─────────────────┘
```
