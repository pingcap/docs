---
title: 解释使用子查询的语句
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 解释使用子查询的语句

TiDB 对 [多项优化](/subquery-optimization.md) 进行了若干优化，以提升子查询的性能。本文档描述了这些优化中一些常见子查询的内容，以及如何解读 `EXPLAIN` 的输出。

本文中的示例基于以下样例数据：

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
CREATE TABLE t3 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 t1_id INT NOT NULL,
 UNIQUE (t1_id)
);

INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
INSERT INTO t3 SELECT NULL, id FROM t1 WHERE id < 1000;

SELECT SLEEP(1);
ANALYZE TABLE t1, t2, t3;
```

## 内连接（非唯一子查询）

在以下示例中，`IN` 子查询搜索 `t2` 表中的一组 ID。为了语义正确性，TiDB 需要保证 `t1_id` 列是唯一的。使用 `EXPLAIN`，你可以看到用以去重并执行 `INNER JOIN` 操作的执行计划：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows  | task      | access object                | operator info                                                                                                             |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_15                   | 21.11    | root      |                              | inner join, inner:TableReader_12, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_44(Build)          | 21.11    | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_45             | 21.11    | root      |                              | index:StreamAgg_34                                                                                                        |
| │   └─StreamAgg_34             | 21.11    | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_26       | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─TableReader_12(Probe)        | 21.11    | root      |                              | data:TableRangeScan_11                                                                                                    |
|   └─TableRangeScan_11          | 21.11    | cop[tikv] | table:t1                     | range: decided by [test.t2.t1_id], keep order:false                                                                       |
+--------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

从上述查询结果可以看到，TiDB 使用索引连接操作 `IndexJoin_15` 来连接并转换子查询。在执行计划中，执行过程如下：

1. TiKV 端的索引扫描操作符 `└─IndexFullScan_26` 读取 `t2.t1_id` 列的值。
2. `└─StreamAgg_34` 操作的部分任务在 TiKV 中对 `t1_id` 的值进行去重。
3. `├─StreamAgg_44(Build)` 操作的部分任务在 TiDB 中对 `t1_id` 的值进行去重，去重由聚合函数 `firstrow(test.t2.t1_id)` 完成。
4. 结果与 `t1` 表的主键进行连接，连接条件为 `eq(test.t1.id, test.t2.t1_id)`。

## 内连接（唯一子查询）

在前例中，为确保 `t1_id` 的值唯一，进行了聚合操作后再与 `t1` 表连接。但在以下示例中，`t3.t1_id` 已由 `UNIQUE` 约束保证唯一：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object                | operator info                                                                                                             |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                | 999.00  | root      |                              | inner join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─IndexReader_41(Build)     | 999.00  | root      |                              | index:IndexFullScan_40                                                                                                    |
| │ └─IndexFullScan_40        | 999.00  | cop[tikv] | table:t3, index:t1_id(t1_id) | keep order:false                                                                                                          |
| └─TableReader_15(Probe)     | 999.00  | root      |                              | data:TableRangeScan_14                                                                                                    |
|   └─TableRangeScan_14       | 999.00  | cop[tikv] | table:t1                     | range: decided by [test.t3.t1_id], keep order:false                                                                       |
+-----------------------------+---------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

语义上，由于 `t3.t1_id` 已由 `UNIQUE` 约束保证唯一，可以直接作为 `INNER JOIN` 执行。

## 半连接（相关子查询）

在前两个示例中，TiDB 能在子查询中的数据经过 `StreamAgg` 变得唯一或本身已唯一后，执行 `INNER JOIN`。这两种连接都采用索引连接。

在此示例中，TiDB 选择了不同的执行计划：

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object                | operator info                                                                                          |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40 | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 90000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00 | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00 | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00 | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
```

从结果可以看出，TiDB 使用了 _semi join_ 算法。半连接不同于内连接：半连接只允许右侧键（`t2.t1_id`）的第一个值，这意味着重复值在连接操作中被去除。连接算法也是 Merge Join，类似于高效的拉链式合并，操作符以排序的顺序从左右两侧读取数据。

原始语句被视为 _相关子查询_，因为子查询中引用了子查询外存在的列（`t1.int_col`）。但 `EXPLAIN` 的输出显示在应用 [子查询去相关优化](/correlated-subquery-optimization.md) 后的执行计划。条件 `t1_id != t1.int_col` 被重写为 `t1.id != t1.int_col`。TiDB 可以在 `└─Selection_21` 中执行此操作，因为它在读取 `t1` 表的数据，因此此去相关和重写极大提升了执行效率。

## 反半连接（`NOT IN` 子查询）

在以下示例中，语义上返回 `t3` 表中的所有行 _除非_ `t3.t1_id` 在子查询中：

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                                                                 |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                | 799.20  | root      |               | anti semi join, inner:TableReader_12, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_28(Build)     | 999.00  | root      |               | data:TableFullScan_27                                                                                                         |
| │ └─TableFullScan_27        | 999.00  | cop[tikv] | table:t3      | keep order:false                                                                                                              |
| └─TableReader_12(Probe)     | 999.00  | root      |               | data:Selection_11                                                                                                             |
|   └─Selection_11            | 999.00  | cop[tikv] |               | lt(test.t1.int_col, 100)                                                                                                      |
|     └─TableRangeScan_10     | 999.00  | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:false                                                                           |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------+
```

此查询先读取 `t3` 表，然后基于 `PRIMARY KEY` 连接 `t1` 表。连接类型为 _anti semi join_；反 semi 表示此示例用于判断值不存在（`NOT IN`），半连接表示只需匹配第一个行即可拒绝连接。

## 空感知半连接（`IN` 和 `= ANY` 子查询）

`IN` 或 `= ANY` 集合操作符的值具有三值逻辑（`true`、`false` 和 `NULL`）。对于由这两个操作符转换而来的连接类型，TiDB 需要意识到连接键两端的 `NULL`，并以特殊方式处理。

包含 `IN` 和 `= ANY` 操作符的子查询会被转换为半连接和左外半连接。前述 [半连接](#semi-join-correlated-subquery) 示例中，由于两端的列 `test.t1.id` 和 `test.t2.t1_id` 都非空，半连接无需考虑空感知（`NULL` 不会被特殊处理）。TiDB 以笛卡尔积和过滤的方式处理空感知半连接，未进行特殊优化。示例如下：

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                             |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
| HashJoin_8                  | 1.00    | root      |               | CARTESIAN left outer semi join, other cond:eq(test.t.a, test.s.a), eq(test.t.b, test.s.b) |
| ├─TableReader_12(Build)     | 1.00    | root      |               | data:TableFullScan_11                                                                     |
| │ └─TableFullScan_11        | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                            |
| └─TableReader_10(Probe)     | 1.00    | root      |               | data:TableFullScan_9                                                                      |
|   └─TableFullScan_9         | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                            |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                       |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
| HashJoin_11                  | 1.00    | root      |               | inner join, equal:[eq(test.t.a, test.s.a) eq(test.t.b, test.s.b)]                                   |
| ├─TableReader_14(Build)      | 1.00    | root      |               | data:Selection_13                                                                                   |
| │ └─Selection_13             | 1.00    | cop[tikv] |               | not(isnull(test.t.a)), not(isnull(test.t.b))                                                        |
| │   └─TableFullScan_12       | 1.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                                      |
| └─HashAgg_17(Probe)          | 1.00    | root      |               | group by:test.s.a, test.s.b, funcs:firstrow(test.s.a)->test.s.a, funcs:firstrow(test.s.b)->test.s.b |
|   └─TableReader_24           | 1.00    | root      |               | data:Selection_23                                                                                   |
|     └─Selection_23           | 1.00    | cop[tikv] |               | not(isnull(test.s.a)), not(isnull(test.s.b))                                                        |
|       └─TableFullScan_22     | 1.00    | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------+
8 rows in set (0.01 sec)
```

在第一个语句 `EXPLAIN SELECT (a,b) IN (SELECT * FROM s) FROM t;` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 允许为空，`IN` 子查询转换的左外半连接是空感知的。具体来说，先计算笛卡尔积，然后将连接在 `IN` 或 `= ANY` 上的列作为普通的等值条件加入其他条件进行过滤。

在第二个语句 `EXPLAIN SELECT * FROM t WHERE (a,b) IN (SELECT * FROM s);` 中，由于 `t` 和 `s` 的列 `a` 和 `b` 允许为空，`IN` 子查询本应转换为空感知半连接。但 TiDB 通过将半连接优化为内连接和聚合，提升了性能。这是因为在非标量输出的 `IN` 子查询中，`NULL` 和 `false` 等价。推下过滤中的 `NULL` 行会导致 `WHERE` 子句的负面语义，从而可以提前忽略这些行。

> **注意：**
>
> `Exists` 操作符也会被转换为半连接，但它不是空感知的。

## 空感知反半连接（`NOT IN` 和 `!= ALL` 子查询）

`NOT IN` 或 `!= ALL` 集合操作符的值具有三值逻辑（`true`、`false` 和 `NULL`）。对于由这两个操作符转换而来的连接类型，TiDB 需要意识到连接键两端的 `NULL`，并以特殊方式处理。

包含 `NOT IN` 和 `! = ALL` 操作符的子查询会被转换为反半连接和反左外半连接。前述 [反半连接](#anti-semi-join-not-in-subquery) 示例中，由于两端的列 `test.t3.t1_id` 和 `test.t1.id` 都非空，反半连接无需考虑空感知（`NULL` 不会被特殊处理）。

TiDB v6.3.0 对空感知反半连接（NAAJ）进行了如下优化：

- 使用空感知等值连接（NA-EQ）构建哈希连接

    集合操作符引入了等值条件，这需要对条件两端的 `NULL` 值进行特殊处理。要求空感知的等值条件称为 NA-EQ。不同于早期版本，TiDB v6.3.0 不再像以前那样处理 NA-EQ，而是在连接后将其放入其他条件中，然后在匹配笛卡尔积后判断结果的合法性。

    自 TiDB v6.3.0 起，NA-EQ 作为一种弱化的等值条件，仍用于构建哈希连接。这减少了需要遍历的匹配数据量，加快了匹配速度。当构建表的 `DISTINCT()` 值的总百分比几乎为 100% 时，优化效果更为显著。

- 利用 `NULL` 的特殊属性加快匹配结果的返回

    由于反半连接是合取范式（CNF），连接两端的 `NULL` 会导致确定的结果。此属性可用来加快整个匹配过程的返回速度。

示例如下：

```sql
CREATE TABLE t(a INT, b INT);
CREATE TABLE s(a INT, b INT);
EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
```

```sql
tidb> EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                               |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
| HashJoin_8                  | 10000.00 | root      |               | Null-aware anti left outer semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                                       |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                              |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                                        |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                              |
+-----------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)

tidb> EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                                                    |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
| HashJoin_8                  | 8000.00  | root      |               | Null-aware anti semi join, equal:[eq(test.t.b, test.s.b) eq(test.t.a, test.s.a)] |
| ├─TableReader_12(Build)     | 10000.00 | root      |               | data:TableFullScan_11                                                            |
| │ └─TableFullScan_11        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                                                   |
| └─TableReader_10(Probe)     | 10000.00 | root      |               | data:TableFullScan_9                                                             |
|   └─TableFullScan_9         | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                                                   |
+-----------------------------+----------+-----------+---------------+----------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

在第一个语句 `EXPLAIN SELECT (a, b) NOT IN (SELECT * FROM s) FROM t;` 中，由于表 `t` 和 `s` 的列 `a` 和 `b` 允许为空，`NOT IN` 子查询转换的左外半连接是空感知的。不同之处在于 NAAJ 优化也将 NA-EQ 作为哈希连接条件，大大加快了连接计算。

在第二个语句 `EXPLAIN SELECT * FROM t WHERE (a, b) NOT IN (SELECT * FROM s);` 中，由于 `t` 和 `s` 的列 `a` 和 `b` 允许为空，`NOT IN` 子查询转换的反半连接也是空感知的。不同之处在于 NAAJ 优化也将 NA-EQ 作为哈希连接条件，从而极大提升了连接计算速度。

目前，TiDB 仅支持空感知反半连接和空感知反左外半连接。仅支持哈希连接类型，且其构建表必须为右表。

> **注意：**
>
> `Not Exists` 操作符也会被转换为反半连接，但它不是空感知的。

## 使用其他类型子查询的解释语句

+ [Explain Statements in the MPP Mode](/explain-mpp.md)
+ [Explain Statements That Use Indexes](/explain-indexes.md)
+ [Explain Statements That Use Joins](/explain-joins.md)
+ [Explain Statements That Use Aggregation](/explain-aggregation.md)
+ [Explain Statements Using Views](/explain-views.md)
+ [Explain Statements Using Partitions](/explain-partitions.md)
+ [Explain Statements Using Index Merge](/explain-index-merge.md)