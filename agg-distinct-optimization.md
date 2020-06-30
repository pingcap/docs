---
title: Distinct Optimization
category: performance
---

# Distinct Optimization

This document introduces the `distinct` optimization in the TiDB query optimizer. Including `SELECT DISTINCT` and `DISTINCT` in the aggregate functions.

## `DISTINCT` modifier in `SELECT` statements

The `DISTINCT` modifier specifies removal of duplicate rows from the result set. `SELECT DISTINCT` is transformed to `GROUP BY`, for example：

```sql
mysql> explain SELECT DISTINCT a from t;
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| id                       | estRows | task      | access object | operator info                                         |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
| HashAgg_6                | 2.40    | root      |               | group by:test.t.a, funcs:firstrow(test.t.a)->test.t.a |
| └─TableReader_11         | 3.00    | root      |               | data:TableFullScan_10                                 |
|   └─TableFullScan_10     | 3.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                        |
+--------------------------+---------+-----------+---------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

## `DISTINCT` option in aggregate function

Usually, aggregate function with `DISTINCT` option is executed in the TiDB layer in a single threded execution model.

The system variable [`tidb_opt_distinct_agg_push_down`](/tidb-specific-system-variables.md#tidb_opt_distinct_agg_push_down) or the [`distinct-agg-push-down`](/tidb-configuration-file.md#distinct-agg-push-down) config item in TiDB controls whether to rewrite the distinct aggregate queries and push them to the TiKV/TiFlash Coprocessor.

Take the following queries as an example of this optimization. `tidb_opt_distinct_agg_push_down` is disabled by default, which means the aggregate functions is executed in the TiDB layer. After enableing this optimization by setting its value to `1`, `count(distinct a)` is pushed to TiKV/TiFlash Coprocessor: there is a `HashAgg_5` in the TiKV Coprocessor to dedpulicate column `a` in the TiKV Coprocessor. It may helps to reduce the compution overhead of `HashAgg_8` in the TiDB layer.

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```
