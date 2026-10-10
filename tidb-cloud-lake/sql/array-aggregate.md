---
title: ARRAY_AGGREGATE
summary: 集約関数を使用して配列内の要素を集約します。
---

# ARRAY_AGGREGATE

集約関数を使用して配列内の要素を集約します。

## 構文 {#syntax}

```sql
ARRAY_AGGREGATE( <array>, '<agg_func>' )
```

- サポートされている集約関数には、`avg`、`count`、`max`、`min`、`sum`、`any`、`stddev_samp`、`stddev_pop`、`stddev`、`std`、`median`、`approx_count_distinct`、`kurtosis`、`skewness` があります。

- この構文は `ARRAY_<agg_func>( <array> )` と書き換えることもできます。たとえば、`ARRAY_AVG( <array> )` です。

## 例 {#examples}

```sql
SELECT ARRAY_AGGREGATE([1, 2, 3, 4], 'SUM'), ARRAY_SUM([1, 2, 3, 4]);

┌────────────────────────────────────────────────────────────────┐
│ array_aggregate([1, 2, 3, 4], 'sum') │ array_sum([1, 2, 3, 4]) │
├──────────────────────────────────────┼─────────────────────────┤
│                                   10 │                      10 │
└────────────────────────────────────────────────────────────────┘
```