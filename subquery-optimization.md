---
title: 子查询相关优化
summary: 了解与子查询相关的优化。
---

# 子查询相关优化

本文主要介绍与子查询相关的优化。

子查询通常出现在以下几种情况：

- `NOT IN (SELECT ... FROM ...)`
- `NOT EXISTS (SELECT ... FROM ...)`
- `IN (SELECT ... FROM ..)`
- `EXISTS (SELECT ... FROM ...)`
- `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

有时子查询中会包含非子查询的列，例如 `select * from t where t.a in (select * from t2 where t.b=t2.b)`。子查询中的 `t.b` 列并不属于子查询本身，而是从子查询外部引入的。这类子查询通常被称为“相关子查询”，而外部引入的列称为“相关列”。关于相关子查询的优化，请参见 [相关子查询的去相关化](/correlated-subquery-optimization.md)。本文主要关注不涉及相关列的子查询。

默认情况下，子查询会使用 [半连接（相关子查询）](/explain-subqueries.md#semi-join-correlated-subquery) 中提到的 `semi join` 作为执行方式。对于某些特殊的子查询，TiDB 会进行一些逻辑重写以获得更好的性能。

## `... < ALL (SELECT ... FROM ...)` 或 `... > ANY (SELECT ... FROM ...)`

在这种情况下，`ALL` 和 `ANY` 可以分别用 `MAX` 和 `MIN` 替换。当表为空时，`MAX(EXPR)` 和 `MIN(EXPR)` 的结果为 NULL。当 `EXPR` 的结果包含 `NULL` 时，表现也是一样的。`EXPR` 的结果是否包含 `NULL` 可能会影响表达式的最终结果，因此完整的重写形式如下：

- `t.id < all (select s.id from s)` 会被重写为 `t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`
- `t.id > any (select s.id from s)` 会被重写为 `t.id > max(s.id) or if(sum(s.id is null) != 0, null, false)`

## `... != ANY (SELECT ... FROM ...)`

在这种情况下，如果子查询中的所有值都是不同的，只需与这些值进行比较即可。如果子查询中不同值的数量大于 1，则必然存在不等。因此，这类子查询可以重写为：

- `select * from t where t.id != any (select s.id from s)` 会被重写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`

## `... = ALL (SELECT ... FROM ...)`

在这种情况下，如果子查询中不同值的数量大于 1，则该表达式的结果必然为 false。因此，这类子查询在 TiDB 中会被重写为：

- `select * from t where t.id = all (select s.id from s)` 会被重写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`

## `... IN (SELECT ... FROM ...)`

在这种情况下，`IN` 的子查询会被重写为 `SELECT ... FROM ... GROUP ...`，然后再重写为常规的 `JOIN` 形式。

例如，`select * from t1 where t1.a in (select t2.a from t2)` 会被重写为 `select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2. The form of a`。这里的 `DISTINCT` 属性如果 `t2.a` 拥有 `UNIQUE` 属性，则可以自动消除。

```sql
explain select * from t1 where t1.a in (select t2.a from t2);
```

```sql
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
| IndexJoin_12                 | 9990.00 | root      |                        | inner join, inner:TableReader_11, outer key:test.t2.a, inner key:test.t1.a |
| ├─HashAgg_21(Build)          | 7992.00 | root      |                        | group by:test.t2.a, funcs:firstrow(test.t2.a)->test.t2.a                   |
| │ └─IndexReader_28           | 9990.00 | root      |                        | index:IndexFullScan_27                                                     |
| │   └─IndexFullScan_27       | 9990.00 | cop[tikv] | table:t2, index:idx(a) | keep order:false, stats:pseudo                                             |
| └─TableReader_11(Probe)      | 7992.00 | root      |                        | data:TableRangeScan_10                                                     |
|   └─TableRangeScan_10        | 7992.00 | cop[tikv] | table:t1               | range: decided by [test.t2.a], keep order:false, stats:pseudo              |
+------------------------------+---------+-----------+------------------------+----------------------------------------------------------------------------+
```

当 `IN` 子查询相对较小而外部查询较大时，这种重写可以获得更好的性能，因为如果不进行重写，无法使用 t2 作为驱动表的 `index join`。但缺点是当重写过程中无法自动消除聚合且 `t2` 表较大时，这种重写会影响查询性能。目前，可以通过变量 [tidb\_opt\_insubq\_to\_join\_and\_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg) 控制该优化。当该优化不适用时，你可以手动关闭它。

## `EXISTS` 子查询与 `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

目前，对于这类场景下的子查询，如果子查询不是相关子查询，TiDB 会在优化阶段提前对其进行计算，并直接用结果集替换。如下图所示，`EXISTS` 子查询在优化阶段被提前计算为 `TRUE`，因此在最终的执行结果中不会显示。

```sql
create table t1(a int);
create table t2(a int);
insert into t2 values(1);
explain select * from t1 where exists (select * from t2);
```

```sql
+------------------------+----------+-----------+---------------+--------------------------------+
| id                     | estRows  | task      | access object | operator info                  |
+------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_12         | 10000.00 | root      |               | data:TableFullScan_11          |
| └─TableFullScan_11     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+------------------------+----------+-----------+---------------+--------------------------------+
```

在上述优化中，优化器会自动优化语句的执行。此外，你还可以添加 [`SEMI_JOIN_REWRITE`](/optimizer-hints.md#semi_join_rewrite) hint 进一步重写语句。

如果不使用该 hint 对查询进行重写，当执行计划选择 hash join 时，semi-join 查询只能使用子查询构建哈希表。在这种情况下，如果子查询的结果比外部查询大，执行速度可能会比预期慢。

同样地，当执行计划选择 index join 时，semi-join 查询只能使用外部查询作为驱动表。在这种情况下，如果子查询的结果比外部查询小，执行速度也可能会比预期慢。

当使用 `SEMI_JOIN_REWRITE()` 对查询进行重写时，优化器可以扩展选择范围，从而选择更优的执行计划。