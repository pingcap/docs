---
title: Optimizer Hints
summary: 使用优化器提示以影响查询执行计划
---

# Optimizer Hints {#optimizer-hints}

TiDB 支持优化器提示，基于 MySQL 5.7 引入的类似注释的语法。例如，常用的语法之一是 `/*+ HINT_NAME([t1_name [, t2_name] ...]) */`。在 TiDB 优化器选择的查询计划不够优化时，建议使用优化器提示。

如果遇到提示不生效的情况，请参阅 [Troubleshoot common issues that hints do not take effect](#troubleshoot-common-issues-that-hints-do-not-take-effect)。

## Syntax {#syntax}

优化器提示不区分大小写，指定在 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE` 关键字之后的 SQL 语句中的 `/*+ ... */` 注释内。

多个提示可以用逗号分隔。例如，以下查询使用了三种不同的提示：

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

可以在 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 和 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 的输出中观察优化器提示对查询执行计划的影响。

不正确或不完整的提示不会导致语句错误。这是因为提示的语义仅为 *提示*（建议）性质，作用于查询执行。同样，如果提示不适用，TiDB 最多会返回警告。

> **Note:**
>
> 如果注释没有紧跟在指定的关键字后面，它们将被视为普通的 MySQL 注释。这些注释不会生效，也不会报告警告。

目前，TiDB 支持两类提示，作用范围不同。第一类提示在查询块范围内生效，例如 [`/*+ HASH_AGG() */`](#hash_agg)；第二类提示在整个查询范围内生效，例如 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)。

每个语句中的每个子查询对应不同的查询块，每个查询块有自己的名称。例如：

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上述查询语句有三个查询块：最外层的 `SELECT` 对应第一个查询块，名为 `sel_1`；两个子 `SELECT` 语句分别对应第二和第三个查询块，名为 `sel_2` 和 `sel_3`。编号的顺序是根据 `SELECT` 从左到右出现的顺序。如果将第一个 `SELECT` 替换为 `DELETE` 或 `UPDATE`，那么对应的查询块名为 `del_1` 或 `upd_1`。

## Hints that take effect in query blocks {#hints-that-take-effect-in-query-blocks}

此类提示可以跟在 **任何** `SELECT`、`UPDATE` 或 `DELETE` 关键字后。为了控制提示的生效范围，可以在提示中使用查询块的名称。可以通过准确识别查询中的每个表（避免重复的表名或别名）来明确提示参数。如果提示中未指定查询块，默认在当前块生效。

例如：

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

此提示在 `sel_1` 查询块中生效，其参数为 `sel_1` 中的 `t1` 和 `t3` 表（`sel_2` 也包含一个 `t1` 表）。

如上所述，可以通过以下方式在提示中指定查询块的名称：

- 将查询块名作为提示的第一个参数，并用空格与其他参数分隔。除了 `QB_NAME`，本节列出的所有提示还可以使用另一个可选的隐藏参数 `@QB_NAME`。通过使用此参数，可以指定此提示的生效范围。
- 在参数中的表名后附加 `@QB_NAME`，显式指定该表所属的查询块。

> **Note:**
>
> 必须将提示放在或紧跟在提示生效的查询块之前。如果将提示放在查询块之后，则不会生效。

### QB_NAME {#qb-name}

如果查询语句较复杂，包含多个嵌套查询，可能会误识别某个查询块的 ID 和名称。`QB_NAME` 提示可以帮助解决此问题。

`QB_NAME` 表示查询块名称。你可以为查询块指定一个新名称。指定的 `QB_NAME` 和之前的默认名称都有效。例如：

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

此提示将外层 `SELECT` 查询块的名称指定为 `QB1`，使得 `QB1` 和默认的 `sel_1` 都是该查询块的有效名称。

> **Note:**
>
> 在上述示例中，如果提示将 `QB_NAME` 指定为 `sel_2`，且未为原第二个 `SELECT` 查询块指定新的 `QB_NAME`，那么 `sel_2` 将成为第二个查询块的无效名称。

### MERGE_JOIN(t1_name [, tl_name ...]) {#merge-join-t1-name-tl-name}

`MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用排序归并连接算法。通常此算法内存消耗较少，但处理时间较长。如果数据量非常大或系统内存不足，建议使用此提示。例如：

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_SMJ` 是 `MERGE_JOIN` 在 TiDB 3.0.x 及早期版本中的别名。如果你使用这些版本，必须使用 `TIDB_SMJ(t1_name [, tl_name ...])` 语法。对于后续版本，`TIDB_SMJ` 和 `MERGE_JOIN` 都是有效的名称，但建议使用 `MERGE_JOIN`。

### NO_MERGE_JOIN(t1_name [, tl_name ...]) {#no-merge-join-t1-name-tl-name}

`NO_MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不要对指定的表使用排序归并连接算法。例如：

```sql
SELECT /*+ NO_MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_JOIN(t1_name [, tl_name ...]) {#inl-join-t1-name-tl-name}

> **Note:**
>
> 在某些情况下，`INL_JOIN` 提示可能不生效。更多信息请参阅 [`INL_JOIN` hint does not take effect](#inl_join-hint-does-not-take-effect)。

`INL_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用索引嵌套循环连接算法。在某些场景下，此算法可能消耗更少的系统资源、处理时间更短，也可能产生相反的效果。如果在 `WHERE` 条件过滤后，结果集少于 10,000 行，建议使用此提示。例如：

```sql
SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id AND t2.id = t3.id;
```

在上述 SQL 中，`INL_JOIN(t1, t2)` 提示告诉优化器对 `t1` 和 `t2` 使用索引嵌套循环连接算法。注意，这并不意味着 `t1` 和 `t2` 之间一定使用索引嵌套循环连接，而是表示 `t1` 和 `t2` 在与其他表连接时，可能会使用索引嵌套循环。

`INL_JOIN()` 中的参数是内表候选表，用于创建查询计划。例如，`INL_JOIN(t1)` 表示 TiDB 只考虑将 `t1` 作为内表来生成查询计划。如果候选表有别名，必须用别名作为参数；如果没有别名，则用表的原始名称。例如，在 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;` 查询中，参数必须是 `t` 的别名 `t1` 或 `t2`，不能用 `t`。

> **Note:**
>
> `TIDB_INLJ` 是 `INL_JOIN` 在 TiDB 3.0.x 及早期版本中的别名。如果你使用这些版本，必须用 `TIDB_INLJ(t1_name [, tl_name ...])` 语法。对于后续版本，`TIDB_INLJ` 和 `INL_JOIN` 都是有效的名称，但建议使用 `INL_JOIN`。

### NO_INDEX_JOIN(t1_name [, tl_name ...]) {#no-index-join-t1-name-tl-name}

`NO_INDEX_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不要对指定的表使用索引嵌套循环连接算法。例如：

```sql
SELECT /*+ NO_INDEX_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### INL_HASH_JOIN {#inl-hash-join}

`INL_HASH_JOIN(t1_name [, tl_name])` 提示告诉优化器使用索引嵌套循环哈希连接算法。使用此算法的条件与使用索引嵌套循环连接相同。不同之处在于，`INL_JOIN` 在内表上建立哈希表，而 `INL_HASH_JOIN` 在外表上建立哈希表。`INL_HASH_JOIN` 有固定的内存限制，而 `INL_JOIN` 的内存消耗取决于内表匹配的行数。

### NO_INDEX_HASH_JOIN(t1_name [, tl_name ...]) {#no-index-hash-join-t1-name-tl-name}

`NO_INDEX_HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不要对指定的表使用索引嵌套循环哈希连接算法。

### INL_MERGE_JOIN {#inl-merge-join}

`INL_MERGE_JOIN(t1_name [, tl_name])` 提示告诉优化器使用索引嵌套循环归并连接算法。使用此算法的条件与使用索引嵌套循环连接相同。

### NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...]) {#no-index-merge-join-t1-name-tl-name}

`NO_INDEX_MERGE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不要对指定的表使用索引嵌套循环归并连接算法。

### HASH_JOIN(t1_name [, tl_name ...]) {#hash-join-t1-name-tl-name}

`HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器对指定的表使用哈希连接算法。此算法允许查询并发执行，使用多个线程，从而实现更高的处理速度，但会消耗更多内存。例如：

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **Note:**
>
> `TIDB_HJ` 是 `HASH_JOIN` 在 TiDB 3.0.x 及早期版本中的别名。如果你使用这些版本，必须用 `TIDB_HJ(t1_name [, tl_name ...])` 语法。对于后续版本，`TIDB_HJ` 和 `HASH_JOIN` 都是有效的名称，但建议使用 `HASH_JOIN`。

### NO_HASH_JOIN(t1_name [, tl_name ...]) {#no-hash-join-t1-name-tl-name}

`NO_HASH_JOIN(t1_name [, tl_name ...])` 提示告诉优化器不要对指定的表使用哈希连接算法。例如：

```sql
SELECT /*+ NO_HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_BUILD(t1_name [, tl_name ...]) {#hash-join-build-t1-name-tl-name}

`HASH_JOIN_BUILD(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用哈希连接算法，并将这些表作为构建端。这样可以用特定的表建立哈希表。例如：

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...]) {#hash-join-probe-t1-name-tl-name}

`HASH_JOIN_PROBE(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用哈希连接算法，并将这些表作为探测端。例如：

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE() {#semi-join-rewrite}

`SEMI_JOIN_REWRITE()` 提示告诉优化器将半连接查询重写为普通连接查询。目前，此提示仅对 `EXISTS` 子查询有效。

如果不使用此提示进行重写，当执行计划中选择哈希连接时，半连接查询只能用子查询构建哈希表。在子查询结果较大时，执行速度可能低于预期。

类似地，当执行计划中选择索引连接时，半连接查询只能用外层查询作为驱动表。在子查询结果较小时，执行速度可能低于预期。

使用 `SEMI_JOIN_REWRITE()` 进行重写后，优化器可以扩展选择范围，选择更优的执行计划。

```sql
-- 不使用 SEMI_JOIN_REWRITE() 重写查询。
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

从上述示例可以看出，使用 `SEMI_JOIN_REWRITE()` 提示后，TiDB 可以根据驱动表 `t1` 选择 IndexJoin 的执行方式。

### SHUFFLE_JOIN(t1_name [, tl_name ...]) {#shuffle-join-t1-name-tl-name}

`SHUFFLE_JOIN(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用 Shuffle Join 算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ SHUFFLE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **Note:**
>
> - 在使用此提示前，确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情请参阅 [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)。
> - 此提示可以与 [`HASH_JOIN_BUILD`](#hash_join_buildt1_name--tl_name-) 和 [`HASH_JOIN_PROBE`](#hash_join_probet1_name--tl_name-) 结合使用，以控制 Shuffle Join 算法的 Build 端和 Probe 端。

### BROADCAST_JOIN(t1_name [, tl_name ...]) {#broadcast-join-t1-name-tl-name}

`BROADCAST_JOIN(t1_name [, tl_name ...])` 提示告诉优化器在指定的表上使用 Broadcast Join 算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ BROADCAST_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **Note:**
>
> - 在使用此提示前，确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情请参阅 [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)。
> - 此提示可以与 [`HASH_JOIN_BUILD`](#hash_join_buildt1--tl_name-) 和 [`HASH_JOIN_PROBE`](#hash_join_probet1--tl_name-) 结合使用，以控制 Broadcast Join 算法的 Build 端和 Probe 端。

### NO_DECORRELATE() {#no-decorrelate}

`NO_DECORRELATE()` 提示告诉优化器不要尝试对指定查询块中的相关子查询进行去相关化。此提示适用于 `EXISTS`、`IN`、`ANY`、`ALL`、`SOME` 子查询以及包含相关列（即相关子查询）的标量子查询。

当在查询块中使用此提示时，优化器不会尝试对子查询与外层查询块之间的相关列进行去相关化，而始终使用 Apply 操作符执行查询。

默认情况下，TiDB 会尝试对相关子查询进行 [去相关化](/correlated-subquery-optimization.md)，以提高执行效率。但在 [某些场景](/correlated-subquery-optimization.md#restrictions) 下，去相关化反而可能降低效率。这时可以用此提示手动告诉优化器不要去相关化。例如：

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

```sql
-- 不使用 NO_DECORRELATE()。
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

从上述执行计划可以看出，优化器已自动执行了去相关化。去相关化后的执行计划没有 Apply 操作符，而是子查询与外层查询之间的连接操作。原本带有相关列的过滤条件 (`t2.b = t1.b`) 变成了普通的连接条件。

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

从上述执行计划可以看出，优化器没有执行去相关化，执行计划中仍然包含 Apply 操作符。带有相关列的过滤条件 (`t2.b = t1.b`) 仍然是访问 `t2` 表时的过滤条件。

### HASH_AGG() {#hash-agg}

`HASH_AGG()` 提示告诉优化器在指定查询块中的所有聚合函数中使用哈希聚合算法。此算法允许查询并发执行，提升处理速度，但会消耗更多内存。例如：

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG() {#stream-agg}

`STREAM_AGG()` 提示告诉优化器在指定查询块中的所有聚合函数中使用流式聚合算法。通常此算法内存消耗较少，但处理时间较长。如果数据量非常大或系统内存不足，建议使用此提示。例如：

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### MPP_1PHASE_AGG() {#mpp-1phase-agg}

`MPP_1PHASE_AGG()` 告诉优化器对指定查询块中的所有聚合函数使用一阶段聚合算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_1PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **Note:**
>
> 在使用此提示前，确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情请参阅 [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)。

### MPP_2PHASE_AGG() {#mpp-2phase-agg}

`MPP_2PHASE_AGG()` 告诉优化器对指定查询块中的所有聚合函数使用两阶段聚合算法。此提示仅在 MPP 模式下生效。例如：

```sql
SELECT /*+ MPP_2PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **Note:**
>
> 在使用此提示前，确保当前 TiDB 集群支持在查询中使用 TiFlash MPP 模式。详情请参阅 [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)。

### USE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#use-index-t1-name-idx1-name-idx2-name}

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器只使用指定的索引来访问 `t1_name` 表。例如，应用以下提示效果等同于执行 `select * from t t1 use index(idx1, idx2);`。

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **Note:**
>
> 如果只指定了表名而未指定索引名，则不会考虑任何索引，而是扫描整个表。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#force-index-t1-name-idx1-name-idx2-name}

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器只使用指定的索引。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])` 的用法和效果与 `USE_INDEX(t1_name, idx1_name [, idx2_name ...])` 相同。

以下 4 个查询效果相同：

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#ignore-index-t1-name-idx1-name-idx2-name}

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器忽略指定的索引。例如，执行以下提示的效果等同于 `select * from t t1 ignore index(idx1, idx2);`。

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#order-index-t1-name-idx1-name-idx2-name}

`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器只使用指定的索引，并按索引顺序读取。例如：

> **Warning:**
>
> 该提示可能导致 SQL 语句执行失败。建议先测试，若测试中出现错误，则删除此提示；测试正常后可继续使用。

此提示通常在以下场景使用：

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

优化器为此查询生成两种执行计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。当使用 `ORDER_INDEX` 提示时，优化器会选择第一种按索引顺序读取的计划。

> **Note:**
>
> -   如果查询本身不需要按索引顺序读取（即没有提示，优化器在任何情况下都不生成按索引顺序读取的计划），当使用 `ORDER_INDEX` 提示时，会出现 `Can't find a proper physical plan for this query` 错误。此时需要删除对应的 `ORDER_INDEX` 提示。
> -   分区表上的索引不能按顺序读取，因此不要在分区表及其相关索引上使用 `ORDER_INDEX`。

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#no-order-index-t1-name-idx1-name-idx2-name}

`NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器只使用指定的索引，不按索引顺序读取。例如：

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

与 `ORDER_INDEX` 提示类似，优化器为此查询生成两种执行计划：`Limit + IndexScan(keep order: true)` 和 `TopN + IndexScan(keep order: false)`。使用 `NO_ORDER_INDEX` 时，优化器会选择后者以无序读取索引。

### AGG_TO_COP() {#agg-to-cop}

`AGG_TO_COP()` 提示告诉优化器将指定查询块中的聚合操作下推到协处理器。如果优化器未能下推某些适合下推的聚合函数，建议使用此提示。例如：

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP() {#limit-to-cop}

`LIMIT_TO_COP()` 提示告诉优化器将指定查询块中的 `Limit` 和 `TopN` 操作下推到协处理器。如果未执行此操作，建议使用此提示。例如：

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]]) {#read-from-storage-tiflash-t1-name-tl-name-tikv-t2-name-tl-name}

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])` 提示告诉优化器从特定存储引擎读取特定表。例如，目前支持两个存储引擎参数：`TIKV` 和 `TIFLASH`。如果表有别名，使用别名作为参数；如果没有别名，使用表的原始名称。例如：

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...]) {#use-index-merge-t1-name-idx1-name-idx2-name}

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])` 提示告诉优化器对指定的表使用索引合并方法。索引合并有两种类型：交集（intersection）和并集（union）。详情请参阅 [Explain Statements Using Index Merge](/explain-index-merge.md)。

如果明确指定索引列表，TiDB 会从列表中选择索引构建索引合并；如果未指定索引列表，则会从所有可用索引中选择。

对于交集类型的索引合并，索引列表为必填参数；对于并集类型的索引合并，索引列表为可选参数。示例：

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

当对同一表多次使用 `USE_INDEX_MERGE` 提示时，优化器会尝试从这些索引集合的并集选择索引。

> **Note:**
>
> `USE_INDEX_MERGE` 的参数是索引名，而非列名。主键的索引名为 `primary`。

### LEADING(t1_name [, tl_name ...]) {#leading-t1-name-tl-name}

`LEADING(t1_name [, tl_name ...])` 提示提醒优化器在生成执行计划时，根据提示中指定的表名顺序确定多表连接的顺序。例如：

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

在多表连接的场景中，连接顺序由 `LEADING()` 提示中表名的顺序决定。优化器会先连接 `t1` 和 `t2`，再将结果与 `t3` 连接。此提示比 [`STRAIGHT_JOIN`](#straight_join) 更为通用。

在以下情况下，`LEADING` 提示不生效：

- 指定多个 `LEADING` 提示。
- 指定的表名不存在。
- 指定的表名重复。
- 优化器无法按照 `LEADING` 指定的顺序执行连接。
- 已存在 `straight_join()` 提示。
- 查询中包含外连接和笛卡尔积。

在上述情况下，会生成警告。

```sql
-- 指定多个 `LEADING` 提示。
SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- 若想了解 `LEADING` 提示失效原因，可执行 `show warnings`。
SHOW WARNINGS;
```

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                           |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | 最多只能使用一个 leading 提示，当使用多个 leading 提示时，所有 leading 提示都将无效。                                |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
```

> **Note:**
>
> 如果查询语句中包含外连接，且在提示中只指定了可以交换连接顺序的表，若提示中包含无法交换连接顺序的表，则提示无效。例如，`SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;`，若想控制 `t2`、`t3` 和 `t4` 的连接顺序，不能在 `LEADING` 中指定 `t1`。

### MERGE() {#merge}

在带有公共表表达式（CTE）的查询中使用 `MERGE()` 提示，可以禁用子查询的物化，将子查询内联展开到 CTE 中。此提示仅适用于非递归 CTE。在某些场景下，使用 `MERGE()` 比默认的临时空间分配方式具有更高的执行效率，例如下推查询条件或在嵌套 CTE 查询中：

```sql
-- 使用提示下推外层查询的谓词。
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a < 18;

-- 在嵌套 CTE 查询中使用提示，将 CTE 内联展开到外层查询。
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **Note:**
>
> `MERGE()` 仅适用于简单的 CTE 查询。不适用于：
>
> - [递归 CTE](https://docs.pingcap.com/tidb/stable/dev-guide-use-common-table-expression#recursive-cte)
> - 不能展开的内联子查询，例如聚合操作符、窗口函数和 `DISTINCT`。
>
> 当 CTE 引用次数过多时，查询性能可能低于默认的物化行为。

## Hints that take effect globally {#hints-that-take-effect-globally}

全局提示作用于 [视图](/views.md)。作为全局提示时，定义在查询中的提示可以在视图内部生效。要定义全局提示，首先使用 `QB_NAME` 提示定义查询块名称，然后在提示中以 `ViewName@QueryBlockName` 形式添加目标提示。

### Step 1: 使用 <code>QB_NAME</code> 提示定义视图的查询块名称 {#step-1-define-the-query-block-name-of-the-view-using-the-code-qb-name-code-hint}

使用 [`QB_NAME`](#qb_name) 提示为视图的每个查询块定义新名称。视图的 `QB_NAME` 定义与 [查询块](#qb_name) 相同，但语法由 `QB_NAME(QB)` 扩展为 `QB_NAME(QB, ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...])`。

> **Note:**
>
> `@QueryBlockName` 和紧随其后的 `.ViewName@QueryBlockName` 之间有空格，否则 `.ViewName@QueryBlockName` 会被视为 `QueryBlockName` 的一部分。例如，`QB_NAME(v2_1, v2@SEL_1 .@SEL_1)` 是合法的，而 `QB_NAME(v2_1, v2@SEL_1.@SEL_1)` 不能正确解析。

- 对于只有单个视图且无子查询的简单语句，以下示例为视图 `v` 的第一个查询块指定名称：

    ```sql
    SELECT /* Comment: 当前查询块的名称为默认 @SEL_1 */ * FROM v;
    ```

    对于视图 `v`，从查询语句开始，列表中的第一个视图名（`ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...]`）为 `v@SEL_1`。视图 `v` 的第一个查询块可以声明为 `QB_NAME(v_1, v@SEL_1 .@SEL_1)`，也可以简写为 `QB_NAME(v_1, v)`，省略 `@SEL_1`：

    ```sql
    CREATE VIEW v AS SELECT /* Comment: 当前查询块的名称为默认 @SEL_1 */ * FROM t;

    -- 指定全局提示
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

- 对于包含嵌套视图和子查询的复杂语句，以下示例为视图 `v1` 和 `v2` 的两个查询块分别指定名称：

    ```sql
    SELECT /* Comment: 当前查询块的名称为默认 @SEL_1 */ * FROM v2 JOIN (
        SELECT /* Comment: 当前查询块的名称为默认 @SEL_2 */ * FROM v2) vv;
    ```

    对于第一个视图 `v2`，从查询语句开始，列表中的第一个视图名为 `v2@SEL_1`。对于第二个视图 `v2`，第一个视图名为 `v2@SEL_2`。以下示例只考虑第一个视图 `v2`。

    `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`，第二个查询块声明为 `QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`：

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* Comment: 对于视图 v2，当前查询块的名称为默认 @SEL_1。故，当前查询块视图列表为 v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* Comment: 对于视图 v2，当前查询块的名称为默认 @SEL_2。故，当前查询块视图列表为 v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    对于视图 `v1`，从前述语句开始，列表中的第一个视图名为 `v2@SEL_1 .v1@SEL_2`。`v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`，第二个查询块为 `QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`：

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* Comment: 对于视图 `v1`，当前查询块的名称为默认 @SEL_1。故，当前查询块视图列表为 v2@SEL_1 .@SEL_2 .v1@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* Comment: 对于视图 `v1`，当前查询块的名称为默认 @SEL_2。故，当前查询块视图列表为 v2@SEL_1 .@SEL_2 .v1@SEL_2 */
        ) tt;
    ```

> **Note:**
>
> - 若要在视图中使用全局提示，必须在视图中定义相应的 `QB_NAME` 提示，否则全局提示不会生效。
> - 在视图中为外层查询块定义 `QB_NAME` 提示时：
>     - 若视图列表中的第一个项未显式声明 `@SEL_`，则默认值与定义 `QB_NAME` 时所在的查询块位置一致。即，`SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;` 等价于 `SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`。
>     - 除了视图列表中的第一个项外，其他项只允许省略 `@SEL_1`。即，若在当前视图的第一个查询块中声明了 `@SEL_1`，则可以省略，否则不能省略。以前述示例为例：
>         - 视图 `v2` 的第一个查询块可以声明为 `QB_NAME(v2_1, v2)`。
>         - 视图 `v2` 的第二个查询块可以声明为 `QB_NAME(v2_2, v2.@SEL_2)`。
>         - 视图 `v1` 的第一个查询块可以声明为 `QB_NAME(v1_1, v2.v1@SEL_2)`。
>         - 视图 `v1` 的第二个查询块可以声明为 `QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`。

### Step 2: Add the target hints {#step-2-add-the-target-hints}

定义好视图的查询块 `QB_NAME` 提示后，可以在视图内部以 `ViewName@QueryBlockName` 形式添加需要生效的 [在查询块中生效的提示](#hints-that-take-effect-in-query-blocks)。例如：

- 为视图 `v2` 的第一个查询块指定 `MERGE_JOIN()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

- 为视图 `v2` 的第二个查询块指定 `MERGE_JOIN()` 和 `STREAM_AGG()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

- 为视图 `v1` 的第一个查询块指定 `HASH_JOIN()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

- 为视图 `v1` 的第二个查询块指定 `HASH_JOIN()` 和 `HASH_AGG()` 提示：

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## Hints that take effect in the whole query {#hints-that-take-effect-in-the-whole-query}

此类提示只能跟在第一个 `SELECT`、`UPDATE` 或 `DELETE` 关键字后，相当于在执行此查询时修改了系统变量的值。其优先级高于已有的系统变量。

> **Note:**
>
> 此类提示也有一个可选的隐藏变量 `@QB_NAME`，但即使指定了该变量，提示仍在整个查询中生效。

### NO_INDEX_MERGE() {#no-index-merge}

`NO_INDEX_MERGE()` 提示禁用优化器的索引合并功能。

例如，以下查询不会使用索引合并：

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

除了此提示外，还可以通过设置系统变量 `tidb_enable_index_merge` 来控制是否启用此功能。

> **Note:**
>
> -   `NO_INDEX_MERGE` 的优先级高于 `USE_INDEX_MERGE`。当同时使用时，`USE_INDEX_MERGE` 不生效。
> -   对于子查询，`NO_INDEX_MERGE` 仅在其位于子查询最外层时生效。

### USE_TOJA(boolean_value) {#use-toja-boolean-value}

`boolean_value` 可以是 `TRUE` 或 `FALSE`。`USE_TOJA(TRUE)` 提示启用优化器将 `in` 条件（包含子查询）转换为连接和聚合操作。相应地，`USE_TOJA(FALSE)` 禁用此功能。例如：

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

除了此提示外，还可以通过设置系统变量 `tidb_opt_insubq_to_join_and_agg` 来控制是否启用此功能。

### MAX_EXECUTION_TIME(N) {#max-execution-time-n}

`MAX_EXECUTION_TIME(N)` 提示为语句设置超时时间 `N`（毫秒），超时后服务器会终止执行。例如：

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

在此示例中，`MAX_EXECUTION_TIME(1000)` 表示超时时间为 1000 毫秒（即 1 秒）。

除了此提示外，还可以通过系统变量 `global.max_execution_time` 限制语句的执行时间。

### MEMORY_QUOTA(N) {#memory-quota-n}

`MEMORY_QUOTA(N)` 提示为语句设置内存使用上限 `N`（MB 或 GB）。当语句的内存消耗超过此限制时，TiDB 会根据超限行为输出日志或直接终止。例如：

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

除了此提示外，还可以通过系统变量 [`tidb_mem_quota_query`](#tidb_mem_quota_query) 限制语句的内存使用。

### READ_CONSISTENT_REPLICA() {#read-consistent-replica}

`READ_CONSISTENT_REPLICA()` 提示启用从 TiKV follower 节点读取一致性数据的功能。例如：

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

除了此提示外，还可以通过设置环境变量 `tidb_replica_read` 为 `'follower'` 或 `'leader'` 来控制是否启用此功能。

### IGNORE_PLAN_CACHE() {#ignore-plan-cache}

`IGNORE_PLAN_CACHE()` 提示提醒优化器在处理当前 `prepare` 语句时不要使用计划缓存。

此提示用于在启用 [prepare-plan-cache](/sql-prepared-plan-cache.md) 时，临时禁用某类查询的计划缓存。

例如，强制在执行 `prepare` 语句时禁用计划缓存：

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### SET_VAR(VAR_NAME=VAR_VALUE) {#set-var-var-name-var-value}

你可以在语句执行期间临时修改系统变量的值，使用 `SET_VAR(VAR_NAME=VAR_VALUE)` 提示。语句执行完毕后，当前会话中的系统变量值会自动恢复到原始值。此提示可用于修改与优化器和执行器相关的系统变量。支持的系统变量列表请参阅 [System Variables](/system-variables.md)。

> **Warning:**
>
> - 强烈建议不要修改未明确支持的变量，否则可能导致不可预料的行为。
> - 不要在子查询中写 `SET_VAR`，否则可能不生效。更多信息请参阅 [`SET_VAR` does not take effect when written in subqueries](#set_var-does-not-take-effect-when-written-in-subqueries)。

示例：

```sql
SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=1234) */ @@MAX_EXECUTION_TIME;
SELECT @@MAX_EXECUTION_TIME;
```

执行上述 SQL 后，第一条查询会返回提示中设置的值 `1234`，而不是默认值 `MAX_EXECUTION_TIME`。第二条查询返回变量的默认值。

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

`STRAIGHT_JOIN()` 提示提醒优化器按照 `FROM` 子句中的表名顺序进行连接。

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **Note:**
>
> - `STRAIGHT_JOIN` 的优先级高于 `LEADING`。当两者同时使用时，`LEADING` 不生效。
> - 建议使用 `LEADING` 提示，它比 `STRAIGHT_JOIN` 更为通用。

### NTH_PLAN(N) {#nth-plan-n}

`NTH_PLAN(N)` 提示提醒优化器在物理优化过程中选择第 `N` 个找到的物理计划。`N` 必须是正整数。

如果指定的 `N` 超出搜索范围，TiDB 会发出警告，并根据忽略此提示的策略选择最优的物理计划。

启用级联规划器时，此提示不生效。

以下示例中，强制优化器选择在物理优化中找到的第 3 个物理计划：

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **Note:**
>
> `NTH_PLAN(N)` 主要用于测试，其兼容性在后续版本中不保证。请谨慎使用。

### RESOURCE_GROUP(resource_group_name) {#resource-group-resource-group-name}

`RESOURCE_GROUP(resource_group_name)` 用于 [Resource Control](/tidb-resource-control-ru-groups.md)，用于隔离资源。此提示会临时以指定的资源组执行当前语句。如果指定的资源组不存在，则此提示会被忽略。

示例：

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

> **Note:**
>
> 从 v8.2.0 版本开始，TiDB 引入了此提示的权限控制。当系统变量 [`tidb_resource_control_strict_mode`](#tidb_resource_control_strict_mode-new-in-v820) 设置为 `ON` 时，使用此提示需要拥有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 或 `RESOURCE_GROUP_USER` 权限。若没有权限，则此提示会被忽略，TiDB 会返回警告。可以在执行后通过 `SHOW WARNINGS;` 查看详情。

## Troubleshoot common issues that hints do not take effect {#troubleshoot-common-issues-that-hints-do-not-take-effect}

### Hints do not take effect because your MySQL command-line client strips hints {#hints-do-not-take-effect-because-your-mysql-command-line-client-strips-hints}

早于 5.7.7 版本的 MySQL 命令行客户端默认会剥离优化器提示。如果要在这些版本中使用提示语法，启动客户端时需要加上 `--comments` 选项。例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

### Hints do not take effect because the database name is not specified {#hints-do-not-take-effect-because-the-database-name-is-not-specified}

如果在连接时未指定数据库名，提示可能不生效。例如：

连接 TiDB 时，使用 `mysql -h127.0.0.1 -P4000 -uroot` 命令且未加 `-D` 选项，然后执行以下 SQL：

```sql
SELECT /*+ use_index(t, a) */ a FROM test.t;
SHOW WARNINGS;
```

由于 TiDB 无法识别表 `t` 所属的数据库，`use_index(t, a)` 提示不会生效。

```sql
+---------+------+----------------------------------------------------------------------+
| Level   | Code | Message                                                              |
+---------+------+----------------------------------------------------------------------+
| Warning | 1815 | use_index(.t, a) 不适用，请检查表(.t) 是否存在                          |
+---------+------+----------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### Hints do not take effect because the database name is not explicitly specified in cross-table queries {#hints-do-not-take-effect-because-the-database-name-is-not-explicitly-specified-in-cross-table-queries}

执行跨库查询时，必须显式指定数据库名，否则提示可能不生效。例如：

```sql
USE test1;
CREATE TABLE t1(a INT, KEY(a));
USE test2;
CREATE TABLE t2(a INT, KEY(a));
SELECT /*+ use_index(t1, a) */ * FROM test1.t1, t2;
SHOW WARNINGS;
```

在上述语句中，由于 `t1` 不在当前 `test2` 数据库中，`use_index(t1, a)` 提示不会生效。

```sql
+---------+------+----------------------------------------------------------------------------------+
| Level   | Code | Message                                                                          |
+---------+------+----------------------------------------------------------------------------------+
| Warning | 1815 | use_index(test2.t1, a) 不适用，请检查表(test2.t1) 是否存在                        |
+---------+------+----------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此时需要显式指定数据库名，例如用 `use_index(test1.t1, a)` 替代 `use_index(t1, a)`。

### Hints do not take effect because they are placed in wrong locations {#hints-do-not-take-effect-because-they-are-placed-in-wrong-locations}

提示不能生效的原因之一是没有放在特定关键字之后。例如：

```sql
SELECT * /*+ use_index(t, a) */ FROM t;
SHOW WARNINGS;
```

警告信息如下：

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                 |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1064 | 你有语法错误；请检查与你的 TiDB 版本对应的手册，正确的语法应为 [parser:8066]Optimizer hint can only be followed by certain keywords like SELECT, INSERT, etc. |
+---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

此时应将提示放在 `SELECT` 关键字之后。详细请参阅 [Syntax](#syntax) 部分。

### <code>INL_JOIN</code> hint does not take effect {#code-inl-join-code-hint-does-not-take-effect}

#### <code>INL_JOIN</code> hint does not take effect when built-in functions are used on columns for joining tables {#code-inl-join-code-hint-does-not-take-effect-when-built-in-functions-are-used-on-columns-for-joining-tables}

在某些情况下，如果在连接表的列上使用了内置函数，优化器可能无法选择 `IndexJoin` 计划，导致 `INL_JOIN` 提示不生效。

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
    | Warning | 1815 | 优化器提示 /*+ INL_JOIN(t1, t2) */ 或 /*+ TIDB_INLJ(t1, t2) */ 不适用             |
    +---------+------+------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

可以看到，`INL_JOIN` 提示未生效。这是因为优化器限制了不能将 `Projection` 或 `Selection` 操作符作为 `IndexJoin` 的探测端。

从 TiDB v8.0.0 起，可以通过设置 [`tidb_enable_inl_join_inner_multi_pattern`](#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) 为 `ON` 来避免此问题。

```sql
SET @@tidb_enable_inl_join_inner_multi_pattern=ON;
Query OK, 0 rows affected (0.00 sec)

EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id=t2.id AND SUBSTR(t1.tname,1,2)=SUBSTR(t2.tname,1,2);
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows      | task      | access object | operator info                                                                                                                              |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_18                 | 12500.00     | root      |               | inner join, inner:Projection_14, outer key:test.t1.id, inner key:test.t2.id, equal cond:eq(test.t1.id, test.t2.id), eq(test.t1.id, test.t2.id) |
| ├─Projection_32(Build)       | 10000.00     | root      |               | test.t1.id, test.t1.tname, substr(test.t1.tname, 1, 2)->Column#5                                                                           |
| │ └─TableReader_34           | 10000.00     | root      |               | data:TableFullScan_33                                                                                                                      |
| │   └─TableFullScan_33       | 10000.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                                                             |
| └─Projection_14(Probe)       | 100000000.00 | root      |               | test.t2.id, test.t2.tname, substr(test.t2.tname, 1, 2)->Column#6                                                                           |
|   └─TableReader_13           | 10000.00     | root      |               | data:TableRangeScan_12                                                                                                                     |
|     └─TableRangeScan_12      | 10000.00     | cop[tikv] | table:t2      | range: decided by [eq(test.t2.id, test.t1.id)], keep order:false, stats:pseudo                                                             |
+------------------------------+--------------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------+
7 rows in set (0.00 sec)
```

#### <code>INL_JOIN</code>、<code>INL_HASH_JOIN</code> 和 <code>INL_MERGE_JOIN</code> 提示因字符集不兼容而不生效 {#code-inl-join-code-code-inl-hash-join-code-and-code-inl-merge-join-code-hints-do-not-take-effect-due-to-collation-incompatibility}

当两个表的连接键字符集不兼容时，无法使用 `IndexJoin` 操作符执行查询。此时，`INL_JOIN`、`INL_HASH_JOIN` 和 `INL_MERGE_JOIN` 提示都不生效。例如：

```sql
CREATE TABLE t1 (k varchar(8), key(k)) COLLATE=utf8mb4_general_ci;
CREATE TABLE t2 (k varchar(8), key(k)) COLLATE=utf8mb4_bin;
EXPLAIN SELECT /*+ tidb_inlj(t1) */ * FROM t1, t2 WHERE t1.k=t2.k;
```

执行计划如下：

```sql
+------------------------------+----------+-----------+----------------------+----------------------------------------------+
| id                           | estRows  | task      | access object        | operator info                                |
+------------------------------+----------+-----------+----------------------+----------------------------------------------+
| HashJoin_19                  | 12487.50 | root      |                      | inner join, equal:[eq(test.t1.k, test.t2.k)] |
| ├─IndexReader_24(Build)      | 9990.00  | root      |                      | index:IndexFullScan_23                       |
| │ └─IndexFullScan_23         | 9990.00  | cop[tikv] | table:t2, index:k(k) | keep order:false, stats:pseudo               |
| └─IndexReader_22(Probe)      | 9990.00  | root      |                      | index:IndexFullScan_21                       |
|   └─IndexFullScan_21         | 9990.00  | cop[tikv] | table:t1, index:k(k) | keep order:false, stats:pseudo               |
+------------------------------+----------+-----------+----------------------+----------------------------------------------+
5 rows in set, 1 warning (0.00 sec)
```

在上述语句中，`t1.k` 和 `t2.k` 的字符集不兼容（`utf8mb4_general_ci` 和 `utf8mb4_bin`），导致 `INL_JOIN` 或 `TIDB_INLJ` 提示不生效。

```sql
SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------+
| Level   | Code | Message                                                                    |
+---------+------+----------------------------------------------------------------------------+
| Warning | 1815 | 优化器提示 /*+ INL_JOIN(t1) */ 或 /*+ TIDB_INLJ(t1) */ 不适用             |
+---------+------+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

#### <code>INL_JOIN</code> 提示不生效的原因之一是连接顺序 {#code-inl-join-code-hint-does-not-take-effect-due-to-join-order}

`INL_JOIN(t1, t2)` 或 `TIDB_INLJ(t1, t2)` 提示在语义上指示 `t1` 和 `t2` 作为 `IndexJoin` 的内表与其他表连接，而不是直接用 `IndexJoin` 连接它们。例如：

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

在上述示例中，`t1` 和 `t3` 并未直接用 `IndexJoin` 连接。

如果希望 `t1` 和 `t3` 直接用 `IndexJoin` 连接，可以先用 [`LEADING(t1, t3)`](#leadingt1_name--tl_name-) 提示指定连接顺序，然后用 `INL_JOIN` 指定连接算法。例如：

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

### 使用提示导致 <code>Can't find a proper physical plan for this query</code> 错误 {#using-hints-causes-the-code-can-t-find-a-proper-physical-plan-for-this-query-code-error}

出现 `Can't find a proper physical plan for this query` 错误的场景包括：

- 查询本身不需要按顺序读取索引。即在没有提示的情况下，优化器在任何情况下都不生成按索引顺序读取的计划。此时若指定 `ORDER_INDEX` 提示，会出现此错误。解决方案是删除对应的 `ORDER_INDEX` 提示。
- 查询通过使用 `NO_JOIN` 相关提示排除了所有可能的连接方法。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
EXPLAIN SELECT /*+ NO_HASH_JOIN(t1), NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): 内部错误：找不到合适的物理计划
```

- 系统变量 [`tidb_opt_enable_hash_join`](#tidb_opt_enable_hash_join-new-in-v656-v712-and-v740) 设置为 `OFF`，且排除了所有其他连接类型。

```sql
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT);
set tidb_opt_enable_hash_join=off;
EXPLAIN SELECT /*+ NO_MERGE_JOIN(t1) */ * FROM t1, t2 WHERE t1.a=t2.a;
ERROR 1815 (HY000): 内部错误：找不到合适的物理计划
```

### <code>SET_VAR</code> 在子查询中写入时不生效 {#code-set-var-code-does-not-take-effect-when-written-in-subqueries}

`SET_VAR` 用于修改当前语句的系统变量值。不要在子查询中写 `SET_VAR`，否则可能不生效。原因在于子查询的特殊处理。

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

以下示例中，`SET_VAR` 未写在子查询中，因此会生效。

```sql
mysql> SELECT /*+ SET_VAR(MAX_EXECUTION_TIME=123) */ @@MAX_EXECUTION_TIME, a FROM (SELECT 1 as a) t;
+----------------------+---+
| @@MAX_EXECUTION_TIME | a |
+----------------------+---+
|                  123 | 1 |
+----------------------+---+
1 row in set (0.00 sec)
```
