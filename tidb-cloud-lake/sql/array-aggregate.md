---
title: ARRAY_AGGREGATE
summary: 使用聚合函数对数组中的元素进行聚合。
---

# ARRAY_AGGREGATE

使用聚合函数对数组中的元素进行聚合。

## 语法 {#syntax}

```sql
ARRAY_AGGREGATE( <array>, '<agg_func>' )
```

- 支持的聚合函数包括 `avg`、`count`、`max`、`min`、`sum`、`any`、`stddev_samp`、`stddev_pop`、`stddev`、`std`、`median`、`approx_count_distinct`、`kurtosis` 和 `skewness`。

- 该语法可以改写为 `ARRAY_<agg_func>( <array> )`。例如，`ARRAY_AVG( <array> )`。

## 示例 {#examples}

```sql
SELECT ARRAY_AGGREGATE([1, 2, 3, 4], 'SUM'), ARRAY_SUM([1, 2, 3, 4]);

┌────────────────────────────────────────────────────────────────┐
│ array_aggregate([1, 2, 3, 4], 'sum') │ array_sum([1, 2, 3, 4]) │
├──────────────────────────────────────┼─────────────────────────┤
│                                   10 │                      10 │
└────────────────────────────────────────────────────────────────┘
```