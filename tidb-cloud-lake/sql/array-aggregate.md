---
title: ARRAY_AGGREGATE
---

Aggregates elements in the array with an aggregate function.

## Syntax

```sql
ARRAY_AGGREGATE( <array>, '<agg_func>' )
```

- Supported aggregate functions include `avg`, `count`, `max`, `min`, `sum`, `any`, `stddev_samp`, `stddev_pop`, `stddev`, `std`, `median`, `approx_count_distinct`, `kurtosis`, and `skewness`.

- The syntax can be rewritten as `ARRAY_<agg_func>( <array> )`. For example, `ARRAY_AVG( <array> )`.

## Examples

```sql
SELECT ARRAY_AGGREGATE([1, 2, 3, 4], 'SUM'), ARRAY_SUM([1, 2, 3, 4]);

┌────────────────────────────────────────────────────────────────┐
│ array_aggregate([1, 2, 3, 4], 'sum') │ array_sum([1, 2, 3, 4]) │
├──────────────────────────────────────┼─────────────────────────┤
│                                   10 │                      10 │
└────────────────────────────────────────────────────────────────┘
```
