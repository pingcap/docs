---
title: Eliminate Max/Min
summary: 介绍消除 Max/Min 函数的规则。
---

# Eliminate Max/Min

当一个 SQL 语句包含 `max`/`min` 函数时，查询优化器会尝试通过应用 `max`/`min` 优化规则，将这些聚合函数转换为 TopN 操作符。这样，TiDB 就能通过索引更高效地执行查询。

此优化规则根据 `select` 语句中 `max`/`min` 函数的数量，分为以下两类：

- [仅含一个 `max`/`min` 函数的语句](#one-maxmin-function)
- [含多个 `max`/`min` 函数的语句](#multiple-maxmin-functions)

## 仅含一个 `max`/`min` 函数

当一个 SQL 语句满足以下条件时，应用此规则：

- 语句中仅包含一个聚合函数，为 `max` 或 `min`。
- 该聚合函数没有相关的 `group by` 子句。

例如：

```sql
select max(a) from t
```

优化规则会将该语句重写为：

```sql
select max(a) from (select a from t where a is not null order by a desc limit 1) t
```

当列 `a` 有索引，或者列 `a` 是某个复合索引的前缀时，借助索引，新 SQL 语句只需扫描一行数据即可找到最大值或最小值。这避免了全表扫描。

该示例语句的执行计划如下：

```sql
mysql> explain select max(a) from t;
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                           | estRows | task      | access object           | operator info                       |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
| StreamAgg_13                 | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
| └─Limit_17                   | 1.00    | root      |                         | offset:0, count:1                   |
|   └─IndexReader_27           | 1.00    | root      |                         | index:Limit_26                      |
|     └─Limit_26               | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|       └─IndexFullScan_25     | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------+---------+-----------+-------------------------+-------------------------------------+
```

## 含多个 `max`/`min` 函数

当一个 SQL 语句满足以下条件时，应用此规则：

- 语句中包含多个聚合函数，且全部为 `max` 或 `min`。
- 这些聚合函数都没有相关的 `group by` 子句。
- 每个 `max`/`min` 函数中的列都具有索引以保持顺序。

例如：

```sql
select max(a) - min(a) from t
```

优化规则首先会检查列 `a` 是否有索引以保持其顺序。如果有，SQL 语句会被重写为两个子查询的笛卡尔积：

```sql
select max_a - min_a
from
    (select max(a) as max_a from t) t1,
    (select min(a) as min_a from t) t2
```

通过重写，优化器可以对两个子查询分别应用仅含一个 `max`/`min` 函数的规则。语句会被重写为：

```sql
select max_a - min_a
from
    (select max(a) as max_a from (select a from t where a is not null order by a desc limit 1) t) t1,
    (select min(a) as min_a from (select a from t where a is not null order by a asc limit 1) t) t2
```

同样地，如果列 `a` 有索引以保持其顺序，优化后只需扫描两行数据，而不是全表扫描。然而，如果列 `a` 没有索引以保持其顺序，此规则会导致两次全表扫描，但如果不重写，执行只需一次全表扫描。因此，在这种情况下，不应用此规则。

最终的执行计划如下：

```sql
mysql> explain select max(a)-min(a) from t;
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| id                                 | estRows | task      | access object           | operator info                       |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
| Projection_17                      | 1.00    | root      |                         | minus(Column#4, Column#5)->Column#6 |
| └─HashJoin_18                      | 1.00    | root      |                         | CARTESIAN inner join                |
|   ├─StreamAgg_45(Build)            | 1.00    | root      |                         | funcs:min(test.t.a)->Column#5       |
|   │ └─Limit_49                     | 1.00    | root      |                         | offset:0, count:1                   |
|   │   └─IndexReader_59             | 1.00    | root      |                         | index:Limit_58                      |
|   │     └─Limit_58                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|   │       └─IndexFullScan_57       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, stats:pseudo       |
|   └─StreamAgg_24(Probe)            | 1.00    | root      |                         | funcs:max(test.t.a)->Column#4       |
|     └─Limit_28                     | 1.00    | root      |                         | offset:0, count:1                   |
|       └─IndexReader_38             | 1.00    | root      |                         | index:Limit_37                      |
|         └─Limit_37                 | 1.00    | cop[tikv] |                         | offset:0, count:1                   |
|           └─IndexFullScan_36       | 1.00    | cop[tikv] | table:t, index:idx_a(a) | keep order:true, desc, stats:pseudo |
+------------------------------------+---------+-----------+-------------------------+-------------------------------------+
```