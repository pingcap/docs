---
title: ARRAY_STDDEV_SAMP
title_includes: ARRAY_STDDEV
---

Computes the sample standard deviation of numeric array values. `NULL` items are ignored; non-numeric entries raise an error.

## Syntax

```sql
ARRAY_STDDEV_SAMP(<array>)
```

## Return Type

Floating-point.

## Examples

```sql
SELECT ARRAY_STDDEV_SAMP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_samp;

┌─────────────┐
│ stddev_samp │
├─────────────┤
│ 2.138089935299395 │
└─────────────┘
```

```sql
SELECT ARRAY_STDDEV_SAMP([1.5, 2.5, NULL, 3.5]) AS stddev_samp_null;

┌─────────────────┐
│ stddev_samp_null │
├─────────────────┤
│              1  │
└─────────────────┘
```
