---
title: 优化器 Hint
summary: 使用优化器 Hint 影响查询执行计划
---

# 优化器 Hint {#optimizer-hints}

TiDB 支持优化器 Hint，其语法基于 MySQL 5.7 引入的类似注释的语法。例如，常见的语法之一是 `/*+ HINT_NAME([t1_name [, t2_name] ...]) */`。当 TiDB 优化器选择了次优的查询计划时，建议使用优化器 Hint。

如果你遇到 Hint 不生效的情况，请参见[排查 Hint 不生效的常见问题](#troubleshoot-common-issues-that-hints-do-not-take-effect)。

## 语法 {#syntax}

优化器 Hint 不区分大小写，并且需要写在 SQL 语句中 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE` 关键字后面的 `/*+ ... */` 注释中。

可以通过逗号分隔指定多个 Hint。例如，以下查询使用了三种不同的 Hint：

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

优化器 Hint 对查询执行计划的影响可以通过 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 的输出结果观察到。

错误或不完整的 Hint 不会导致语句报错。这是因为 Hint 仅作为对查询执行的*建议*语义。同样地，如果 Hint 不适用，TiDB 最多只会返回一个警告。

> **注意：**
>
> 如果注释没有紧跟在指定关键字后面，则会被当作普通的 MySQL 注释处理。此时注释不会生效，也不会报出警告。

目前，TiDB 支持两类 Hint，作用范围不同。第一类 Hint 在查询块范围内生效，例如 [`/*+ HASH_AGG() */`](#hash_agg)；第二类 Hint 在整个查询中生效，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

一个语句中的每个查询或子查询对应一个不同的查询块，每个查询块都有自己的名称。例如：

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上述查询语句有三个查询块：最外层的 `SELECT` 对应第一个查询块，名称为 `sel_1`；两个 `SELECT` 子查询分别对应第二和第三个查询块，名称分别为 `sel_2` 和 `sel_3`。数字的顺序根据 `SELECT` 从左到右出现的顺序决定。如果将第一个 `SELECT` 替换为 `DELETE` 或 `UPDATE`，则对应的查询块名称为 `del_1` 或 `upd_1`。

## 查询块范围内生效的 Hint {#hints-that-take-effect-in-query-blocks}

此类 Hint 可以跟在**任意** `SELECT`、`UPDATE` 或 `DELETE` 关键字后面。为了控制 Hint 的生效范围，可以在 Hint 中使用查询块的名称。你可以通过准确标识查询中的每个表（以防表名或别名重复）来明确 Hint 的参数。如果 Hint 中未指定查询块，则默认在当前块中生效。

例如：

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

该 Hint 在 `sel_1` 查询块中生效，其参数为 `sel_1` 中的 `t1` 和 `t3` 表（`sel_2` 也包含一个 `t1` 表）。

如上所述，你可以通过以下方式在 Hint 中指定查询块名称：

-   将查询块名称作为 Hint 的第一个参数，并用空格与其他参数分隔。除了 `QB_NAME` 外，本节列出的所有 Hint 还支持一个可选的隐藏参数 `@QB_NAME`。通过该参数，可以指定 Hint 的生效范围。
-   在参数中的表名后追加 `@QB_NAME`，以显式指定该表属于哪个查询块。

> **注意：**
>
> 必须将 Hint 放在其生效的查询块内部或之前。如果 Hint 放在查询块之后，则不会生效。

### QB_NAME {#qb-name}

如果查询语句较为复杂，包含多层嵌套查询，某个查询块的 ID 和名称可能会被误识别。此时可以使用 `QB_NAME` Hint 进行辅助。

`QB_NAME` 表示查询块名称。你可以为查询块指定一个新名称。指定的 `QB_NAME` 和之前的默认名称都有效。例如：

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

该 Hint 指定了外层 `SELECT` 查询块的名称为 `QB1`，此时 `QB1` 和默认名称 `sel_1` 都是该查询块的有效名称。

> **注意：**
>
> 在上述示例中，如果 Hint 将 `QB_NAME` 指定为 `sel_2`，且未为原第二个 `SELECT` 查询块指定新的 `QB_NAME`，则 `sel_2` 对于第二个 `SELECT` 查询块来说变为无效名称。

### MERGE_JOIN(t1_name [, tl_name ...]) {#merge-join-t1-name-tl-name}

`MERGE_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用排序归并连接算法。通常，该算法内存消耗较少，但处理时间较长。如果数据量很大或系统内存不足，建议使用该 Hint。例如：

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **注意：**
>
> `TIDB_SMJ` 是 TiDB 3.0.x 及更早版本中 `MERGE_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_SMJ(t1_name [, tl_name ...])` 语法。对于更高版本，`TIDB_SMJ` 和 `MERGE_JOIN` 都是有效名称，但推荐使用 `MERGE_JOIN`。

### NO_MERGE_JOIN(t1_name [, tl_name ...]) {#no-merge-join-t1-name-tl-name}

`NO_MERGE_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表不使用排序归并连接算法。例如：

```sql
SELECT /*+ NO_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_JOIN(t1_name [, tl_name ...]) {#inl-join-t1-name-tl-name}

> **注意：**
>
> 在某些情况下，`INL_JOIN` Hint 可能不会生效。详情参见 [`INL_JOIN` Hint 不生效](#inl_join-hint-does-not-take-effect)。

`INL_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用索引嵌套循环连接算法。在某些场景下，该算法可能消耗更少的系统资源、处理时间更短，但在其他场景下可能相反。如果外表经过 `WHERE` 条件过滤后结果集小于 10000 行，建议使用该 Hint。例如：

```sql
SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id;
```

在上述 SQL 语句中，`INL_JOIN(t1, t2)` Hint 告诉优化器对 `t1` 和 `t2` 使用索引嵌套循环连接算法。注意，这并不意味着 `t1` 和 `t2` 之间直接使用索引嵌套循环连接，而是表示 `t1` 和 `t2` 分别与其他表（如 `t3`）使用该算法。

`INL_JOIN()` 中给定的参数是在生成查询计划时作为内表的候选表。例如，`INL_JOIN(t1)` 表示 TiDB 只考虑将 `t1` 作为内表生成查询计划。如果候选表有别名，必须使用别名作为 `INL_JOIN()` 的参数；如果没有别名，则使用表的原始名称。例如，在 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` 查询中，必须使用 `t` 表的别名 `t1` 或 `t2`，而不是 `t` 作为 `INL_JOIN()` 的参数。

> **注意：**
>
> `TIDB_INLJ` 是 TiDB 3.0.x 及更早版本中 `INL_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_INLJ(t1_name [, tl_name ...])` 语法。对于更高版本，`TIDB_INLJ` 和 `INL_JOIN` 都是有效名称，但推荐使用 `INL_JOIN`。

### NO_INDEX_JOIN(t1_name [, tl_name ...]) {#no-index-join-t1-name-tl-name}

`NO_INDEX_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表不使用索引嵌套循环连接算法。例如：

```sql
SELECT /*+ NO_INDEX_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_HASH_JOIN {#inl-hash-join}

`INL_HASH_JOIN(t1_name [, tl_name])` Hint 告诉优化器使用索引嵌套循环哈希连接算法。该算法的使用条件与索引嵌套循环连接算法相同。两者的区别在于，`INL_JOIN` 在被连接的内表上构建哈希表，而 `INL_HASH_JOIN` 在被连接的外表上构建哈希表。`INL_HASH_JOIN` 的内存使用有固定上限，而 `INL_JOIN` 的内存消耗取决于内表匹配的行数。

### NO_INDEX_HASH_JOIN(t1_name [, tl_name ...]) {#no-index-hash-join-t1-name-tl-name}

`NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表不使用索引嵌套循环哈希连接算法。

### INL_MERGE_JOIN {#inl-merge-join}

`INL_MERGE_JOIN(t1_name [, tl_name])` Hint 告诉优化器对指定表使用索引嵌套循环归并连接算法。该算法的使用条件与索引嵌套循环连接算法相同。

### NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...]) {#no-index-merge-join-t1-name-tl-name}

`NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表不使用索引嵌套循环归并连接算法。

### HASH_JOIN(t1_name [, tl_name ...]) {#hash-join-t1-name-tl-name}

`HASH_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用哈希连接算法。该算法允许查询并发多线程执行，处理速度更快，但内存消耗更大。例如：

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **注意：**
>
> `TIDB_HJ` 是 TiDB 3.0.x 及更早版本中 `HASH_JOIN` 的别名。如果你使用这些版本，必须使用 `TIDB_HJ(t1_name [, tl_name ...])` 语法。对于更高版本，`TIDB_HJ` 和 `HASH_JOIN` 都是有效名称，但推荐使用 `HASH_JOIN`。

### NO_HASH_JOIN(t1_name [, tl_name ...]) {#no-hash-join-t1-name-tl-name}

`NO_HASH_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表不使用哈希连接算法。例如：

```sql
SELECT /*+ NO_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_BUILD(t1_name [, tl_name ...]) {#hash-join-build-t1-name-tl-name}

`HASH_JOIN_BUILD(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用哈希连接算法，并将这些表作为构建端（Build side）。这样可以指定用哪些表构建哈希表。例如：

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...]) {#hash-join-probe-t1-name-tl-name}

`HASH_JOIN_PROBE(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用哈希连接算法，并将这些表作为探测端（Probe side）。这样可以指定用哪些表作为探测端执行哈希连接。例如：

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE() {#semi-join-rewrite}

`SEMI_JOIN_REWRITE()` Hint 告诉优化器将半连接查询重写为普通连接查询。目前，该 Hint 仅对 `EXISTS` 子查询生效。

如果不使用该 Hint 进行重写，当执行计划选择哈希连接时，半连接查询只能用子查询构建哈希表。此时，如果子查询的结果比外层查询大，执行速度可能低于预期。

同样地，当执行计划选择索引连接时，半连接查询只能用外层查询作为驱动表。此时，如果子查询的结果比外层查询小，执行速度也可能低于预期。

使用 `SEMI_JOIN_REWRITE()` 进行重写后，优化器可以扩展选择范围，选择更优的执行计划。

```sql
-- 未使用 SEMI_JOIN_REWRITE() 重写查询。
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| id                          | estRows | task      | access object          | operator info                                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| MergeJoin_9                 | 7992.00 | root      |                        | semi join, left key:test.t.a, right key:test.t1.a |
| ├─IndexReader_25(Build)     | 9990.00 | root      |                        | index:IndexFullScan_24                            |
| │ └─IndexFullScan_24        | 9990.00 | cop[tikv] | table:t1, index:idx(a) | keep order:true, stats:pseudo                     |
| └─IndexReader_23(Probe)     | 9990.00 | root      |                        | index:IndexFullScan_22                            |
|   └─IndexFullScan_22        | 9990.00 | cop[tikv] | table:t, index:idx(a)  | keep order:true, stats:pseudo                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
```

```sql
-- 使用 SEMI_JOIN_REWRITE() 重写查询。
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT /*+ SEMI_JOIN_REWRITE() */ 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                                                                 |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                 | 1.25    | root      |                        | inner join, inner:IndexReader_15, outer key:test.t1.a, inner key:test.t.a, equal cond:eq(test.t1.a, test.t.a) |
| ├─StreamAgg_39(Build)        | 1.00    | root      |                        | group by:test.t1.a, funcs:firstrow(test.t1.a)->test.t1.a                                                      |
| │ └─IndexReader_34           | 1.00    | root      |                        | index:IndexFullScan_33                                                                                        |
| │   └─IndexFullScan_33       | 1.00    | cop[tikv] | table:t1, index:idx(a) | keep order:true                                                                                               |
| └─IndexReader_15(Probe)      | 1.25    | root      |                        | index:Selection_14                                                                                            |
|   └─Selection_14             | 1.25    | cop[tikv] |                        | not(isnull(test.t.a))                                                                                         |
|     └─IndexRangeScan_13      | 1.25    | cop[tikv] | table:t, index:idx(a)  | range: decided by [eq(test.t.a, test.t1.a)], keep order:false, stats:pseudo                                   |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
```

从上述示例可以看出，使用 `SEMI_JOIN_REWRITE()` Hint 后，TiDB 可以基于驱动表 `t1` 选择 IndexJoin 的执行方式。

### SHUFFLE_JOIN(t1_name [, tl_name ...]) {#shuffle-join-t1-name-tl-name}

`SHUFFLE_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用 Shuffle Join 算法。该 Hint 仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ SHUFFLE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> -   使用该 Hint 前，请确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情参见 [使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。
> -   该 Hint 可与 [`HASH_JOIN_BUILD` Hint](#hash_join_buildt1_name--tl_name-) 和 [`HASH_JOIN_PROBE` Hint](#hash_join_probet1_name--tl_name-) 结合使用，以控制 Shuffle Join 算法的 Build 端和 Probe 端。

### BROADCAST_JOIN(t1_name [, tl_name ...]) {#broadcast-join-t1-name-tl-name}

`BROADCAST_JOIN(t1_name [, tl_name ...])` Hint 告诉优化器对指定表使用 Broadcast Join 算法。该 Hint 仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ BROADCAST_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注意：**
>
> -   使用该 Hint 前，请确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情参见 [使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。
> -   该 Hint 可与 [`HASH_JOIN_BUILD` Hint](#hash_join_buildt1_name--tl_name-) 和 [`HASH_JOIN_PROBE` Hint](#hash_join_probet1_name--tl_name-) 结合使用，以控制 Broadcast Join 算法的 Build 端和 Probe 端。

### NO_DECORRELATE() {#no-decorrelate}

`NO_DECORRELATE()` Hint 告诉优化器不要尝试对指定查询块中的相关子查询进行去相关化。该 Hint 适用于包含相关列（即相关子查询）的 `EXISTS`、`IN`、`ANY`、`ALL`、`SOME` 子查询和标量子查询。

当在查询块中使用该 Hint 时，优化器不会尝试对子查询与外层查询块之间的相关列进行去相关化，而是始终使用 Apply 算子执行查询。

默认情况下，TiDB 会尝试对相关子查询进行[去相关化](/correlated-subquery-optimization.md)，以获得更高的执行效率。但在[某些场景](/correlated-subquery-optimization.md#restrictions)下，去相关化反而可能降低执行效率。此时可以使用该 Hint 手动告知优化器不要进行去相关化。例如：

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

```sql
-- 未使用 NO_DECORRELATE()。
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                                |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b                      |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                                              |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                                           |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                                       |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                               |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                                            |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                                       |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                               |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
```

从上述执行计划可以看出，优化器自动进行了去相关化。去相关化后的执行计划不再有 Apply 算子，而是将子查询与外层查询块之间的原相关列过滤条件（`t2.b = t1.b`）转化为普通的连接条件。

```sql
-- 使用 NO_DECORRELATE()。
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

从上述执行计划可以看出，优化器未进行去相关化，执行计划中仍然包含 Apply 算子，相关列的过滤条件（`t2.b = t1.b`）依然作为访问 `t2` 表时的过滤条件。

### HASH_AGG() {#hash-agg}

`HASH_AGG()` Hint 告诉优化器在指定查询块的所有聚合函数中使用哈希聚合算法。该算法允许查询并发多线程执行，处理速度更快，但内存消耗更大。例如：

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG() {#stream-agg}

`STREAM_AGG()` Hint 告诉优化器在指定查询块的所有聚合函数中使用流式聚合算法。通常，该算法内存消耗较少，但处理时间较长。如果数据量很大或系统内存不足，建议使用该 Hint。例如：

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### MPP_1PHASE_AGG() {#mpp-1phase-agg}

`MPP_1PHASE_AGG()` 告诉优化器在指定查询块的所有聚合函数中使用单阶段聚合算法。该 Hint 仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_1PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **注意：**
>
> 使用该 Hint 前，请确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情参见 [使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### MPP_2PHASE_AGG() {#mpp-2phase-agg}

`MPP_2PHASE_AGG()` 告诉优化器在指定查询块的所有聚合函数中使用两阶段聚合算法。该 Hint 仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_2PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **注意：**
>
> 使用该 Hint 前，请确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情参见 [使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### USE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#use-index-t1-name-idx1-name-idx2-name}

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器仅对指定的 `t1_name` 表使用给定的索引。例如，应用以下 Hint 的效果等同于执行 `select * from t t1 use index(idx1, idx2);` 语句。

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **注意：**
>
> 如果在该 Hint 中只指定了表名而未指定索引名，则执行时不会考虑任何索引，而是全表扫描。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#force-index-t1-name-idx1-name-idx2-name}

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器仅使用给定的索引。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 的用法和效果与 `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 完全相同。

以下 4 个查询效果相同：

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#ignore-index-t1-name-idx1-name-idx2-name}

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器对指定的 `t1_name` 表忽略给定的索引。例如，应用以下 Hint 的效果等同于执行 `select * from t t1 ignore index(idx1, idx2);` 语句。

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#order-index-t1-name-idx1-name-idx2-name}

`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器仅对指定表使用给定索引，并按顺序读取指定索引。

> **警告：**
>
> 该 Hint 可能导致 SQL 语句执行失败。建议先进行测试，如测试报错请移除该 Hint；如测试正常可继续使用。

该 Hint 通常用于如下场景：

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+---------+-----------+---------------------+-------------------------------+
| id                         | estRows | task      | access object       | operator info                 |
+----------------------------+---------+-----------+---------------------+-------------------------------+
| Limit_10                   | 10.00   | root      |                     | offset:0, count:10            |
| └─IndexReader_14           | 10.00   | root      |                     | index:Limit_13                |
|   └─Limit_13               | 10.00   | cop[tikv] |                     | offset:0, count:10            |
|     └─IndexFullScan_12     | 10.00   | cop[tikv] | table:t, index:a(a) | keep order:true, stats:pseudo |
+----------------------------+---------+-----------+---------------------+-------------------------------+
```

优化器会为该查询生成两种计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。使用 `ORDER_INDEX` Hint 时，优化器会选择第一种按顺序读取索引的计划。

> **注意：**
>
> -   如果查询本身不需要按顺序读取索引（即在没有 Hint 的情况下，优化器无论如何都不会生成按顺序读取索引的计划），当使用 `ORDER_INDEX` Hint 时会报错 `Can't find a proper physical plan for this query`。此时需要移除对应的 `ORDER_INDEX` Hint。
> -   分区表上的索引无法按顺序读取，因此不要在分区表及其相关索引上使用 `ORDER_INDEX` Hint。

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#no-order-index-t1-name-idx1-name-idx2-name}

`NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器仅对指定表使用给定索引，并且不按顺序读取指定索引。该 Hint 通常用于如下场景。

以下示例表明该查询语句的效果等同于 `SELECT * FROM t t1 use index(idx1, idx2);`：

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ NO_ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+----------+-----------+---------------------+--------------------------------+
| id                         | estRows  | task      | access object       | operator info                  |
+----------------------------+----------+-----------+---------------------+--------------------------------+
| TopN_7                     | 10.00    | root      |                     | test.t.a, offset:0, count:10   |
| └─IndexReader_14           | 10.00    | root      |                     | index:TopN_13                  |
|   └─TopN_13                | 10.00    | cop[tikv] |                     | test.t.a, offset:0, count:10   |
|     └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t, index:a(a) | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------------+--------------------------------+
```

与 `ORDER_INDEX` Hint 示例类似，优化器会为该查询生成两种计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。使用 `NO_ORDER_INDEX` Hint 时，优化器会选择后一种无序读取索引的计划。

### AGG_TO_COP() {#agg-to-cop}

`AGG_TO_COP()` Hint 告诉优化器将指定查询块中的聚合操作下推到 coprocessor。如果优化器未下推某些适合下推的聚合函数，建议使用该 Hint。例如：

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP() {#limit-to-cop}

`LIMIT_TO_COP()` Hint 告诉优化器将指定查询块中的 `Limit` 和 `TopN` 算子下推到 coprocessor。如果优化器未进行此类下推操作，建议使用该 Hint。例如：

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]]) {#read-from-storage-tiflash-t1-name-tl-name-tikv-t2-name-tl-name}

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` Hint 告诉优化器从指定存储引擎读取指定表。目前该 Hint 支持两个存储引擎参数：`TIKV` 和 `TIFLASH`。如果表有别名，使用别名作为 `READ_FROM_STORAGE()` 的参数；如果没有别名，则使用表的原始名称。例如：

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...]) {#use-index-merge-t1-name-idx1-name-idx2-name}

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` Hint 告诉优化器对指定表使用索引合并访问方式。索引合并分为交集型和并集型两种。详情参见 [Explain 语句中的索引合并](/explain-index-merge.md)。

如果你显式指定了索引列表，TiDB 会从该列表中选择索引构建索引合并；如果未指定索引列表，TiDB 会从所有可用索引中选择。

对于交集型索引合并，Hint 中的索引列表为必选参数；对于并集型索引合并，索引列表为可选参数。示例如下：

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

当对同一张表指定多个 `USE_INDEX_MERGE` Hint 时，优化器会尝试从这些 Hint 指定的索引集合的并集中选择索引。

> **注意：**
>
> `USE_INDEX_MERGE` 的参数为索引名，而不是列名。主键的索引名为 `primary`。

### LEADING(t1_name [, tl_name ...]) {#leading-t1-name-tl-name}

`LEADING(t1_name [, tl_name ...])` Hint 提示优化器在生成执行计划时，按照 Hint 中指定的表名顺序确定多表连接的顺序。例如：

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

在上述多表连接查询中，连接顺序由 `LEADING()` Hint 指定的表名顺序决定。优化器会先连接 `t1` 和 `t2`，再将结果与 `t3` 连接。该 Hint 比 [`STRAIGHT_JOIN`](#straight_join) 更通用。

`LEADING` Hint 在以下情况下不会生效：

-   指定了多个 `LEADING` Hint。
-   `LEADING` Hint 中指定的表名不存在。
-   `LEADING` Hint 中指定了重复的表名。
-   优化器无法按照 `LEADING` Hint 指定的顺序进行连接操作。
-   已存在 `straight_join()` Hint。
-   查询中包含外连接且存在笛卡尔积。

上述情况下会生成警告。

```sql
-- 指定了多个 `LEADING` Hint。
SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- 查看 `LEADING` Hint 失效原因，可执行 `show warnings`。
SHOW WARNINGS;
```

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                           |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | We can only use one leading hint at most, when multiple leading hints are used, all leading hints will be invalid |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
```

> **注意：**
>
> 如果查询语句包含外连接，则 Hint 中只能指定连接顺序可交换的表。如果 Hint 中包含连接顺序不可交换的表，则 Hint 失效。例如，在 `SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;` 中，如果你想控制 `t2`、`t3`、`t4` 的连接顺序，则不能在 `LEADING` Hint 中指定 `t1`。

### MERGE() {#merge}

在包含公共表表达式（CTE）的查询中使用 `MERGE()` Hint，可以禁用子查询的物化，将子查询内联展开为 CTE。该 Hint 仅适用于非递归 CTE。在某些场景下，使用 `MERGE()` 比默认的分配临时空间有更高的执行效率，例如谓词下推或嵌套 CTE 查询：

```sql
-- 使用 Hint 将外层查询的谓词下推。
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a < 18;

-- 在嵌套 CTE 查询中使用 Hint，将 CTE 内联展开到外层查询。
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **注意：**
>
> `MERGE()` 仅适用于简单的 CTE 查询，不适用于以下场景：
>
> -   [递归 CTE](https://docs.pingcap.com/tidb/stable/dev-guide-use-common-table-expression#recursive-cte)
> -   不能内联展开的子查询，如聚合算子、窗口函数和 `DISTINCT`。
>
> 当 CTE 被引用次数过多时，查询性能可能低于默认的物化行为。

## 全局生效的 Hint {#hints-that-take-effect-globally}

全局 Hint 在 [视图](/views.md) 中生效。当指定为全局 Hint 时，查询中定义的 Hint 可以在视图内部生效。要指定全局 Hint，首先使用 `QB_NAME` Hint 定义查询块名称，然后以 `ViewName@QueryBlockName` 的形式添加目标 Hint。

### 步骤 1：使用 <code>QB_NAME</code> Hint 定义视图的查询块名称 {#step-1-define-the-query-block-name-of-the-view-using-the-code-qb-name-code-hint}

使用 [`QB_NAME` Hint](#qb_name) 为视图的每个查询块定义新名称。视图的 `QB_NAME` Hint 定义方式与[查询块](#qb_name)一致，但语法从 `QB_NAME(QB)` 扩展为 `QB_NAME(QB, ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...])`。

> **注意：**
>
> `@QueryBlockName` 与紧随其后的 `.ViewName@QueryBlockName` 之间有空格，否则 `.ViewName@QueryBlockName` 会被当作 `QueryBlockName` 的一部分。例如，`QB_NAME(v2_1, v2@SEL_1 .@SEL_1)` 是合法的，而 `QB_NAME(v2_1, v2@SEL_1.@SEL_1)` 无法正确解析。

-   对于只有单个视图且无子查询的简单语句，以下示例指定了视图 `v` 的第一个查询块名称：

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v;
    ```

    对于视图 `v`，从查询语句开始，列表中的第一个视图名称为 `v@SEL_1`。视图 `v` 的第一个查询块可以声明为 `QB_NAME(v_1, v@SEL_1 .@SEL_1)`，也可以简写为 `QB_NAME(v_1, v)`，省略 `@SEL_1`：

    ```sql
    CREATE VIEW v AS SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM t;

    -- 指定全局 Hint
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

-   对于包含嵌套视图和子查询的复杂语句，以下示例为视图 `v1` 和 `v2` 的每个查询块指定了名称：

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v2 JOIN (
        SELECT /* Comment: The name of the current query block is the default @SEL_2 */ * FROM v2) vv;
    ```

    对于第一个视图 `v2`，从第一个查询语句开始，列表中的第一个视图名称为 `v2@SEL_1`。对于第二个视图 `v2`，第一个视图名称为 `v2@SEL_2`。以下示例只考虑第一个视图 `v2`。

    视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`，第二个查询块可以声明为 `QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`：

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* Comment: For view v2, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* Comment: For view v2, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    对于视图 `v1`，从上述语句开始，列表中的第一个视图名称为 `v2@SEL_1 .v1@SEL_2`。视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`，第二个查询块可以声明为 `QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`：

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* Comment: For view `v1`, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* Comment: For view `v1`, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_2 */
        ) tt;
    ```

> **注意：**
>
> -   在视图中使用全局 Hint 时，必须在视图中定义对应的 `QB_NAME` Hint，否则全局 Hint 不会生效。
>
> -   在视图中使用 Hint 指定多个表名时，需要确保同一 Hint 中出现的表名属于同一视图的同一查询块。
>
> -   在视图的最外层查询块中定义 `QB_NAME` Hint 时：
>
>     -   对于 `QB_NAME` 中视图列表的第一个项，如果未显式声明 `@SEL_`，则默认与定义 `QB_NAME` 的查询块位置一致。即，查询 `SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;` 等价于 `SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`。
>     -   对于 `QB_NAME` 中除第一个项外的其他项，仅 `@SEL_1` 可以省略。即，如果当前视图的第一个查询块声明了 `@SEL_1`，则可以省略；否则不能省略。对于上述示例：
>
>         -   视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2)`。
>         -   视图 `v2` 的第二个查询块可以声明为 `QB_NAME(v2_2, v2.@SEL_2)`。
>         -   视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2.v1@SEL_2)`。
>         -   视图 `v1` 的第二个查询块可以声明为 `QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`。

### 步骤 2：添加目标 Hint {#step-2-add-the-target-hints}

在为视图的查询块定义好 `QB_NAME` Hint 后，可以以 `ViewName@QueryBlockName` 的形式添加所需的[查询块范围内生效的 Hint](#hints-that-take-effect-in-query-blocks)，使其在视图内部生效。例如：

-   为视图 `v2` 的第一个查询块指定 `MERGE_JOIN()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

-   为视图 `v2` 的第二个查询块指定 `MERGE_JOIN()` 和 `STREAM_AGG()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

-   为视图 `v1` 的第一个查询块指定 `HASH_JOIN()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

-   为视图 `v1` 的第二个查询块指定 `HASH_JOIN()` 和 `HASH_AGG()` Hint：

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## 整个查询范围内生效的 Hint {#hints-that-take-effect-in-the-whole-query}

此类 Hint 只能跟在**第一个** `SELECT`、`UPDATE` 或 `DELETE` 关键字后面，相当于在执行该查询时修改指定系统变量的值。Hint 的优先级高于已有的系统变量。

> **注意：**
>
> 此类 Hint 也有一个可选的隐藏变量 `@QB_NAME`，但即使指定该变量，Hint 也会在整个查询中生效。

### NO_INDEX_MERGE() {#no-index-merge}

`NO_INDEX_MERGE()` Hint 禁用优化器的索引合并功能。

例如，以下查询不会使用索引合并：

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

除了该 Hint，还可以通过设置系统变量 `tidb_enable_index_merge` 控制是否启用该功能。

> **注意：**
>
> -   `NO_INDEX_MERGE` 优先级高于 `USE_INDEX_MERGE`。当两者同时使用时，`USE_INDEX_MERGE` 不生效。
> -   对于子查询，`NO_INDEX_MERGE` 仅在放在子查询最外层时生效。

### USE_TOJA(boolean_value) {#use-toja-boolean-value}

`boolean_value` 参数可以为 `TRUE` 或 `FALSE`。`USE_TOJA(TRUE)` Hint 启用优化器将包含子查询的 `in` 条件转换为 join 和聚合操作。相对地，`USE_TOJA(FALSE)` Hint 禁用该功能。

例如，以下查询会将 `in (select t2.a from t2) subq` 转换为对应的 join 和聚合操作：

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

除了该 Hint，还可以通过设置系统变量 `tidb_opt_insubq_to_join_and_agg` 控制是否启用该功能。

### MAX_EXECUTION_TIME(N) {#max-execution-time-n}

`MAX_EXECUTION_TIME(N)` Hint 为语句设置一个最大执行时长 `N`（单位为毫秒），超时后服务器会终止该语句。以下 Hint 中，`MAX_EXECUTION_TIME(1000)` 表示超时时间为 1000 毫秒（即 1 秒）：

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

除了该 Hint，还可以通过系统变量 `global.max_execution_time` 限制语句的执行时间。

### MEMORY_QUOTA(N) {#memory-quota-n}

`MEMORY_QUOTA(N)` Hint 为语句设置一个内存使用上限 `N`（单位为 MB 或 GB）。当语句内存使用超过该限制时，TiDB 会根据超限行为记录日志或直接终止语句。

以下 Hint 中，`MEMORY_QUOTA(1024 MB)` 表示内存使用限制为 1024 MB：

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

除了该 Hint，还可以通过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 系统变量限制语句的内存使用。

### READ_CONSISTENT_REPLICA() {#read-consistent-replica}

`READ_CONSISTENT_REPLICA()` Hint 启用从 TiKV follower 节点读取一致性数据的功能。例如：

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

除了该 Hint，还可以通过设置环境变量 `tidb_replica_read` 为 `'follower'` 或 `'leader'` 控制是否启用该功能。

### IGNORE_PLAN_CACHE() {#ignore-plan-cache}

`IGNORE_PLAN_CACHE()` Hint 提示优化器在处理当前 `prepare` 语句时不使用 Plan Cache。

该 Hint 用于在 [prepare-plan-cache](/sql-prepared-plan-cache.md) 启用时，临时禁用某类查询的 Plan Cache。

以下示例在执行 `prepare` 语句时强制禁用 Plan Cache。

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### SET_VAR(VAR_NAME=VAR_VALUE) {#set-var-var-name-var-value}

你可以通过 `SET_VAR(VAR_NAME=VAR_VALUE)` Hint 在语句执行期间临时修改系统变量的值。语句执行结束后，当前会话中的系统变量值会自动恢复为原值。该 Hint 可用于修改部分与优化器和执行器相关的系统变量。可通过 [系统变量](/system-variables.md) 查看支持通过该 Hint 修改的变量列表。

> **警告：**
>
> -   强烈建议不要修改未明确支持的变量，否则可能导致不可预期的行为。
> -   不要在子查询中写 `SET_VAR`，否则可能不生效。详情参见 [`SET_VAR` 写在子查询中不生效](#set_var-does-not-take-effect-when-written-in-subqueries)。

示例如下：

```sql
SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=1234) */ @@MAX_EXECUTION_TIME;
SELECT @@MAX_EXECUTION_TIME;
```

执行上述 SQL 后，第一条查询返回 Hint 中设置的值 `1234`，而不是 `MAX_EXECUTION_TIME` 的默认值。第二条查询返回变量的默认值。

```sql
+----------------------+
| @@MAX_EXECUTION_TIME |
+----------------------+
|                 1234 |
+----------------------+
1 row in set (0.00 sec)
+----------------------+
| @@MAX_EXECUTION_TIME |
+----------------------+
|                    0 |
+----------------------+
1 row in set (0.00 sec)
```

### STRAIGHT_JOIN() {#straight-join}

`STRAIGHT_JOIN()` Hint 提示优化器在生成连接计划时，按照 `FROM` 子句中表名的顺序进行连接。

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **注意：**
>
> -   `STRAIGHT_JOIN` 优先级高于 `LEADING`。当两者同时使用时，`LEADING` 不生效。
> -   推荐使用更通用的 `LEADING` Hint。

### NTH_PLAN(N) {#nth-plan-n}

`NTH_PLAN(N)` Hint 提示优化器选择物理优化过程中找到的第 `N` 个物理计划。`N` 必须为正整数。

如果指定的 `N` 超出物理优化的搜索范围，TiDB 会返回警告，并在忽略该 Hint 的情况下选择最优物理计划。

当启用 cascades planner 时，该 Hint 不生效。

以下示例强制优化器选择物理优化过程中找到的第三个物理计划：

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **注意：**
>
> `NTH_PLAN(N)` 主要用于测试，后续版本不保证兼容性。**请谨慎使用**。

### RESOURCE_GROUP(resource_group_name) {#resource-group-resource-group-name}

`RESOURCE_GROUP(resource_group_name)` 用于[资源管控](/tidb-resource-control-ru-groups.md)实现资源隔离。该 Hint 临时将当前语句在指定资源组下执行。如果指定的资源组不存在，则该 Hint 会被忽略。

示例：

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

> **注意：**
>
> 从 v8.2.0 开始，TiDB 对该 Hint 引入了权限管控。当系统变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) 设置为 `ON` 时，需具备 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 或 `RESOURCE_GROUP_USER` 权限才能使用该 Hint。否则该 Hint 会被忽略，并返回警告。你可以在查询后执行 `SHOW WARNINGS;` 查看详情。

## 排查 Hint 不生效的常见问题 {#troubleshoot-common-issues-that-hints-do-not-take-effect}

### Hint 不生效是因为 MySQL 命令行客户端会去除 Hint {#hints-do-not-take-effect-because-your-mysql-command-line-client-strips-hints}

5.7.7 之前的 MySQL 命令行客户端默认会去除优化器 Hint。如果你想在这些早期版本中使用 Hint 语法，启动客户端时需加上 `--comments` 选项。例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

### Hint 不生效是因为未指定数据库名 {#hints-do-not-take-effect-because-the-database-name-is-not-specified}

如果连接时未指定数据库名，Hint 可能不会生效。例如：

连接 TiDB 时，使用 `mysql -h127.0.0.1 -P4000 -uroot` 命令（未加 `-D` 选项），然后执行以下 SQL：

```sql
SELECT /*+ use_index(t, a) */ a FROM test.t;
SHOW WARNINGS;
```

由于 TiDB 无法识别表 `t` 所属的数据库，`use_index(t, a)` Hint 不生效。

```sql
+---------+------+----------------------------------------------------------------------+
| Level   | Code | Message                                                              |
+---------+------+----------------------------------------------------------------------+
| Warning | 1815 | use_index(.t, a) is inapplicable, check whether the table(.t) exists |
+---------+------+----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### Hint 不生效是因为跨库查询未显式指定数据库名 {#hints-do-not-take-effect-because-the-database-name-is-not-explicitly-specified-in-cross-table-queries}

执行跨库查询时，需要显式指定数据库名，否则 Hint 可能不会生效。例如：

```sql
USE test1;
CREATE TABLE t1(a INT, KEY(a));
USE test2;
CREATE TABLE t2(a INT, KEY(a));
SELECT /*+ use_index(t1, a) */ * FROM test1.t1, t2;
SHOW WARNINGS;
```

上述语句中，表 `t1` 不在当前 `test2` 数据库中，因此 `use_index(t1, a)` Hint 不生效。

```sql
+---------+------+----------------------------------------------------------------------------------+
| Level   | Code | Message                                                                          |
+---------+------+----------------------------------------------------------------------------------+
| Warning | 1815 | use_index(test2.t1, a) is inapplicable, check whether the table(test2.t1) exists |
+---------+------+----------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此时需要将 Hint 写为 `use_index(test1.t1, a)`，而不是 `use_index(t1, a)`。

### Hint 不生效是因为位置不正确 {#hints-do-not-take-effect-because-they-are-placed-in-wrong-locations}

Hint 不是紧跟在指定关键字后面时不会生效。例如：

```sql
SELECT * /*+ use_index(t, a) */ FROM t;
SHOW WARNINGS;
```

警告如下：

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                 |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use [parser:8066]Optimizer hint can only be followed by certain keywords like SELECT, INSERT, etc. |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

此时需要将 Hint 紧跟在 `SELECT` 关键字后面。详情参见[语法](#syntax)部分。

### <code>INL_JOIN</code> Hint 不生效 {#code-inl-join-code-hint-does-not-take-effect}

#### 使用内置函数对连接列进行操作时 <code>INL_JOIN</code> Hint 不生效 {#code-inl-join-code-hint-does-not-take-effect-when-built-in-functions-are-used-on-columns-for-joining-tables}

在某些情况下，如果你对连接表的列使用了内置函数，优化器可能无法选择 `IndexJoin` 计划，导致 `INL_JOIN` Hint 也不生效。

例如，以下查询在连接列 `tname` 上使用了内置函数 `substr`：

```sql
CREATE TABLE t1 (id varchar(10) primary key, tname varchar(10));
CREATE TABLE t2 (id varchar(10) primary key, tname varchar(10));
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id and SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
```

执行计划如下：

```sql
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                         |
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
| HashJoin_12                  | 12500.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id) eq(Column#5, Column#6)] |
| ├─Projection_17(Build)       | 10000.00 | root      |               | test.t2.id, test.t2.tname, substr(test.t2.tname, 1, 2)->Column#6      |
| │ └─TableReader_19           | 10000.00 | root      |               | data:TableFullScan_18                                                 |
| │   └─TableFullScan_18       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                        |
| └─Projection_14(Probe)       | 10000.00 | root      |               | test.t1.id, test.t1.tname, substr(test.t1.tname, 1, 2)->Column#5      |
|   └─TableReader_16           | 10000.00 | root      |               | data:TableFullScan_15                                                 |
|     └─TableFullScan_15       | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                        |
+------------------------------+----------+-----------+---------------+-----------------------------------------------------------------------+
7 rows in set, 1 warning (0.01 sec)
```

```sql
SHOW WARNINGS;
```

    +---------+------+------------------------------------------------------------------------------------+
    | Level   | Code | Message                                                                            |
    +---------+------+------------------------------------------------------------------------------------+
    | Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1, t2) */ or /*+ TIDB_INLJ(t1, t2) */ is inapplicable |
    +---------+------+------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

如上例所示，`INL_JOIN` Hint 未生效。这是由于优化器限制，不能将 `Projection` 或 `Selection` 算子作为 `IndexJoin` 的 probe 端。

从 TiDB v8.0.0 开始，可以通过将 [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) 设置为 `ON` 避免该问题。

```sql
SET @@tidb_enable_inl_join_inner_multi_pattern=ON;
Query OK, 0 rows affected (0.00 sec)

EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id AND SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows      | task      | access object | operator info                                                                                                                              |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                 | 12500.00     | root      |               | inner join, inner:Projection_14, outer key:test.t1.id, inner key:test.t2.id, equal cond:eq(Column#5, Column#6), eq(test.t1.id, test.t2.id) |
| ├─Projection_32(Build)       | 10000.00     | root      |               | test.t1.id, test.t1.tname, substr(test.t1.tname, 1, 2)->Column#5                                                                           |
| │ └─TableReader_34           | 10000.00     | root      |               | data:TableFullScan_33                                                                                                                      |
| │   └─TableFullScan_33       | 10000.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                                                             |
| └─Projection_14(Probe)       | 100000000.00 | root      |               | test.t2.id, test.t2.tname, substr(test.t2.tname, 1, 2)->Column#6                                                                           |
|   └─TableReader_13           | 10000.00     | root      |               | data:TableRangeScan_12                                                                                                                     |
|     └─TableRangeScan_12      | 10000.00     | cop[tikv] | table:t2      | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo                                                             |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

#### <code>INL_JOIN</code>、<code>INL_HASH_JOIN</code> 和 <code>INL_MERGE_JOIN</code> Hint 因排序规则不兼容不生效 {#code-inl-join-code-code-inl-hash-join-code-and-code-inl-merge-join-code-hints-do-not-take-effect-due-to-collation-incompatibility}

当连接键的排序规则在两张表之间不兼容时，无法使用 `IndexJoin` 算子执行查询，此时 [`INL_JOIN`](#inl_joint1_name--tl_name-)、[`INL_HASH_JOIN`](#inl_hash_join) 和 [`INL_MERGE_JOIN`](#inl_merge_join) Hint 都不会生效。例如：

```sql
CREATE TABLE t1 (k varchar(8), key(k)) COLLATE=utf8mb4_general_ci;
CREATE TABLE t2 (k varchar(8), key(k)) COLLATE=utf8mb4_bin;
EXPLAIN SELECT /*+ tidb_inlj(t1) */ * FROM t1, t2 WHERE t1.k=t2.k;
```

执行计划如下：

```sql
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
| id                          | estRows  | task      | access object        | operator info                                |
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
| HashJoin_19                 | 12487.50 | root      |                      | inner join, equal:[eq(test.t1.k, test.t2.k)] |
| ├─IndexReader_24(Build)     | 9990.00  | root      |                      | index:IndexFullScan_23                       |
| │ └─IndexFullScan_23        | 9990.00  | cop[tikv] | table:t2, index:k(k) | keep order:false, stats:pseudo               |
| └─IndexReader_22(Probe)     | 9990.00  | root      |                      | index:IndexFullScan_21                       |
|   └─IndexFullScan_21        | 9990.00  | cop[tikv] | table:t1, index:k(k) | keep order:false, stats:pseudo               |
+-----------------------------+----------+-----------+----------------------+----------------------------------------------+
5 rows in set, 1 warning (0.00 sec)
```

上述语句中，`t1.k` 和 `t2.k` 的排序规则分别为 `utf8mb4_general_ci` 和 `utf8mb4_bin`，不兼容，导致 `INL_JOIN` 或 `TIDB_INLJ` Hint 不生效。

```sql
SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------+
| Level   | Code | Message                                                                    |
+---------+------+----------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1) */ or /*+ TIDB_INLJ(t1) */ is inapplicable |
+---------+------+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### <code>INL_JOIN</code> Hint 因连接顺序不生效 {#code-inl-join-code-hint-does-not-take-effect-due-to-join-order}

[`INL_JOIN(t1, t2)`](#inl_joint1_name--tl_name-) 或 `TIDB_INLJ(t1, t2)` Hint 的语义是让 `t1` 和 `t2` 作为 `IndexJoin` 算子的内表与其他表连接，而不是直接对它们进行 `IndexJoin`。例如：

```sql
EXPLAIN SELECT /*+ inl_join(t1, t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id AND t1.id = t3.id;
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object | operator info                                                                                                                                                           |
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                    | 15625.00 | root      |               | inner join, inner:TableReader_13, outer key:test.t2.id, test.t1.id, inner key:test.t3.id, test.t3.id, equal cond:eq(test.t1.id, test.t3.id), eq(test.t2.id, test.t3.id) |
| ├─IndexJoin_34(Build)           | 12500.00 | root      |               | inner join, inner:TableReader_31, outer key:test.t2.id, inner key:test.t1.id, equal cond:eq(test.t2.id, test.t1.id)                                                     |
| │ ├─TableReader_40(Build)       | 10000.00 | root      |               | data:TableFullScan_39                                                                                                                                                   |
| │ │ └─TableFullScan_39          | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                                                                                          |
| │ └─TableReader_31(Probe)       | 10000.00 | root      |               | data:TableRangeScan_30                                                                                                                                                  |
| │   └─TableRangeScan_30         | 10000.00 | cop[tikv] | table:t1      | range: decided by [test.t2.id], keep order:false, stats:pseudo                                                                                                          |
| └─TableReader_13(Probe)         | 12500.00 | root      |               | data:TableRangeScan_12                                                                                                                                                  |
|   └─TableRangeScan_12           | 12500.00 | cop[tikv] | table:t3      | range: decided by [test.t2.id test.t1.id], keep order:false, stats:pseudo                                                                                               |
+---------------------------------+----------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

如上例所示，`t1` 和 `t3` 并未直接通过 `IndexJoin` 连接。

如果要让 `t1` 和 `t3` 直接进行 `IndexJoin`，可以先使用 [`LEADING(t1, t3)` Hint](#leadingt1_name--tl_name-) 指定连接顺序，再用 `INL_JOIN` Hint 指定连接算法。例如：

```sql
EXPLAIN SELECT /*+ leading(t1, t3), inl_join(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id AND t1.id = t3.id;
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object | operator info                                                                                                       |
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_12                   | 15625.00 | root      |               | test.t1.id, test.t1.name, test.t2.id, test.t2.name, test.t3.id, test.t3.name                                        |
| └─HashJoin_21                   | 15625.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id) eq(test.t3.id, test.t2.id)]                                           |
|   ├─TableReader_36(Build)       | 10000.00 | root      |               | data:TableFullScan_35                                                                                               |
|   │ └─TableFullScan_35          | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                                      |
|   └─IndexJoin_28(Probe)         | 12500.00 | root      |               | inner join, inner:TableReader_25, outer key:test.t1.id, inner key:test.t3.id, equal cond:eq(test.t1.id, test.t3.id) |
|     ├─TableReader_34(Build)     | 10000.00 | root      |               | data:TableFullScan_33                                                                                               |
|     │ └─TableFullScan_33        | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                                      |
|     └─TableReader_25(Probe)     | 10000.00 | root      |               | data:TableRangeScan_24                                                                                              |
|       └─TableRangeScan_24       | 10000.00 | cop[tikv] | table:t3      | range: decided by [test.t1.id], keep order:false, stats:pseudo                                                      |
+---------------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

### 使用 Hint 导致 <code>Can't find a proper physical plan for this query</code> 错误 {#using-hints-causes-the-code-can-t-find-a-proper-physical-plan-for-this-query-code-error}

在以下场景中，可能会出现 `Can't find a proper physical plan for this query` 错误：

-   查询本身不需要按顺序读取索引。即对于该查询，优化器无论如何都不会生成按顺序读取索引的计划。如果指定了 `ORDER_INDEX` Hint，则会报此错误。此时应移除对应的 `ORDER_INDEX` Hint。
-   通过 `NO_JOIN` 相关 Hint 排除了所有可能的连接方式。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
EXPLAIN SELECT /*+ NO_HASH_JOIN(t1), NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```

-   系统变量 [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740) 设置为 `OFF`，且其他连接类型也被排除。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
set tidb_opt_enable_hash_join=off;
EXPLAIN SELECT /*+ NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): Internal : Can't find a proper physical plan for this query
```

### <code>SET_VAR</code> 写在子查询中不生效 {#code-set-var-code-does-not-take-effect-when-written-in-subqueries}

`SET_VAR` 用于修改当前语句的系统变量值。不要将其写在子查询中，否则由于子查询的特殊处理，`SET_VAR` 可能不会生效。

以下示例中，`SET_VAR` 写在子查询中，因此不生效。

```sql
mysql> SELECT @@MAX_EXECUTION_TIME, a FROM (SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=123) */ 1 as a) t;
+----------------------+---+
| @@MAX_EXECUTION_TIME | a |
+----------------------+---+
|                    0 | 1 |
+----------------------+---+
1 row in set (0.00 sec)
```

以下示例中，`SET_VAR` 未写在子查询中，因此生效。

```sql
mysql> SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=123) */ @@MAX_EXECUTION_TIME, a FROM (SELECT 1 as a) t;
+----------------------+---+
| @@MAX_EXECUTION_TIME | a |
+----------------------+---+
|                  123 | 1 |
+----------------------+---+
1 row in set (0.00 sec)
```
