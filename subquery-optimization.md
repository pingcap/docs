---
title: Subquery Related Optimizations
summary: 了解与子查询相关的优化措施。
---

# Subquery Related Optimizations

本文主要介绍与子查询相关的优化措施。

子查询通常出现在以下几种情况：

- `NOT IN (SELECT ... FROM ...)`
- `NOT EXISTS (SELECT ... FROM ...)`
- `IN (SELECT ... FROM ..)`
- `EXISTS (SELECT ... FROM ...)`
- `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

有时子查询中包含非子查询列，例如 `select * from t where t.a in (select * from t2 where t.b=t2.b)`。子查询中的 `t.b` 列不属于子查询，而是从子查询外部引入的。这类子查询通常称为“相关子查询”，而外部引入的列称为“相关列”。关于相关子查询的优化，参考 [Decorrelation of correlated subquery](/correlated-subquery-optimization.md)。本文重点介绍不涉及相关列的子查询。

默认情况下，子查询采用 [Understanding TiDB Execution Plan](/explain-overview.md) 中提到的 `semi join` 作为执行方式。对于某些特殊的子查询，TiDB 会进行一些逻辑重写以获得更好的性能。

## `... < ALL (SELECT ... FROM ...)` 或 `... > ANY (SELECT ... FROM ...)`

在这种情况下，`ALL` 和 `ANY` 可以被 `MAX` 和 `MIN` 替代。当表为空时，`MAX(EXPR)` 和 `MIN(EXPR)` 的结果为 NULL。当 `EXPR` 的结果中包含 `NULL` 时，效果相同。`EXPR` 的结果是否包含 `NULL` 可能会影响最终的表达式结果，因此完整的重写形式如下：

- `t.id < all (select s.id from s)` 重写为 `t.id < min(s.id) and if(sum(s.id is null) != 0, null, true)`
- `t.id > any (select s.id from s)` 重写为 `t.id > max(s.id) or if(sum(s.id is null) != 0, null, false)`

## `... != ANY (SELECT ... FROM ...)`

在这种情况下，如果子查询中的所有值都是不同的，那么只需将查询与它们进行比较即可。如果子查询中的不同值数量超过一个，则必然存在不等的情况。因此，这类子查询可以重写为：

- `select * from t where t.id != any (select s.id from s)` 重写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s) where (t.id != s.id or cnt_distinct > 1)`

## `... = ALL (SELECT ... FROM ...)`

在这种情况下，当子查询中的不同值数量超过一个时，表达式的结果必定为 false。因此，在 TiDB 中，这类子查询被重写为：

- `select * from t where t.id = all (select s.id from s)` 重写为 `select t.* from t, (select s.id, count(distinct s.id) as cnt_distinct from s ) where (t.id = s.id and cnt_distinct <= 1)`

## `... IN (SELECT ... FROM ...)`

在这种情况下，`IN` 的子查询会被重写为 `SELECT ... FROM ... GROUP ...`，然后再重写为普通的 `JOIN` 形式。

例如，`select * from t1 where t1.a in (select t2.a from t2)` 会被重写为 `select t1.* from t1, (select distinct(a) a from t2) t2 where t1.a = t2.a`。这里的 `DISTINCT` 属性可以在 `t2.a` 具有 `UNIQUE` 属性时自动消除。

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

当 `IN` 子查询相对较小时，外部查询较大时，这种重写能带来更好的性能，因为未重写时，使用 `index join` 以 t2 为驱动表是不可行的。然而，缺点是当重写过程中无法自动消除聚合，且 t2 表较大时，这种重写会影响查询性能。目前，变量 [tidb\_opt\_insubq\_to\_join\_and\_agg](/system-variables.md#tidb_opt_insubq_to_join_and_agg) 用于控制此优化。当此优化不适用时，你可以手动禁用。

## `EXISTS` 子查询和 `... >/>=/</<=/=/!= (SELECT ... FROM ...)`

目前，对于这类场景中的子查询，如果子查询不是相关子查询，TiDB 会在优化阶段提前对其进行评估，并直接用结果集替代。如下面的示例，`EXISTS` 子查询在优化阶段被提前评估为 `TRUE`，因此不会出现在最终的执行结果中。

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

在上述优化中，优化器会自动优化语句的执行。此外，你还可以添加 [`SEMI_JOIN_REWRITE`](/optimizer-hints.md#semi_join_rewrite) 提示，以进一步重写语句。

如果不使用此提示进行重写，当执行计划选择哈希连接时，半连接查询只能用子查询构建哈希表。在这种情况下，当子查询的结果比外部查询大时，执行速度可能会比预期慢。

类似地，当执行计划选择索引连接时，半连接查询只能用外部查询作为驱动表。在这种情况下，当子查询的结果比外部查询小，执行速度可能会比预期慢。

当使用 `SEMI_JOIN_REWRITE()` 重写查询时，优化器可以扩展选择范围，从而选择更优的执行计划。