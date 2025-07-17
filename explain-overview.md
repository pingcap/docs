---
title: TiDB 查询执行计划概述
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# TiDB 查询执行计划概述

> **Note:**
>
> 当你使用 MySQL 客户端连接到 TiDB 时，为了更清晰地阅读输出结果且避免换行，可以使用 `pager less -S` 命令。然后，在输出 `EXPLAIN` 结果后，你可以按下键盘上的右箭头 <kbd>→</kbd> 按钮，水平滚动查看输出内容。

SQL 是一种声明式语言。它描述了查询结果应该是什么样子，**而不是获取这些结果的方法**。TiDB 会考虑所有可能的执行方式，包括使用什么顺序连接表以及是否可以利用潜在的索引。 _考虑查询执行计划_ 的过程被称为 SQL 优化。

`EXPLAIN` 语句显示给定语句的所选执行计划。也就是说，在考虑了数百或数千种执行方式后，TiDB 认为这个 _计划_ 将会消耗最少的资源并在最短的时间内执行：


```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a INT NOT NULL, pad1 VARCHAR(255), INDEX(a));
INSERT INTO t VALUES (1, 1, 'aaa'),(2,2, 'bbb');
EXPLAIN SELECT * FROM t WHERE a = 1;
```

```sql
Query OK, 0 rows affected (0.96 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                            | estRows | task      | access object       | operator info                               |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexLookUp_10                | 10.00   | root      |                     |                                             |
| ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t, index:a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

`EXPLAIN` 不会执行实际的查询。可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 来执行查询并显示 `EXPLAIN` 信息。这在诊断所选执行计划是否子优化时非常有用。关于使用 `EXPLAIN` 的更多示例，请参见以下文档：

* [Indexes](/explain-indexes.md)
* [Joins](/explain-joins.md)
* [Subqueries](/explain-subqueries.md)
* [Aggregation](/explain-aggregation.md)
* [Views](/explain-views.md)
* [Partitions](/explain-partitions.md)

## 了解 EXPLAIN 输出

以下描述了上述 `EXPLAIN` 语句的输出内容：

* `id` 描述执行 SQL 语句所需的操作符或子任务的名称。有关更多细节，请参见 [Operator overview](#operator-overview)。
* `estRows` 显示 TiDB 预估将要处理的行数。这个数字可能基于字典信息，例如访问方法基于主键或唯一键，或者基于统计信息，如 CMSketch 或直方图。
* `task` 显示操作符执行工作的地点。有关更多细节，请参见 [Task overview](#task-overview)。
* `access object` 显示被访问的表、分区和索引。索引的部分也会显示，例如上例中使用了索引中的列 `a`。这在你拥有复合索引时非常有用。
* `operator info` 显示关于访问的附加细节。有关更多细节，请参见 [Operator info overview](#operator-info-overview)。

> **Note:**
>
> 在返回的执行计划中，从 v6.4.0 版本开始，`IndexJoin` 和 `Apply` 操作符的所有 probe 端子节点的 `estRows` 含义与 v6.4.0 之前不同。
>
> 在 v6.4.0 之前，`estRows` 表示每个来自构建端的行对应的探测端操作符预估要处理的行数。自 v6.4.0 起，`estRows` 表示 probe 端操作符预估要处理的**总行数**。在 `EXPLAIN ANALYZE` 的结果中显示的实际行数（由 `actRows` 列指示）代表总行数，因此自 v6.4.0 起，`estRows` 和 `actRows` 在 `IndexJoin` 和 `Apply` 操作符的 probe 端子节点中的含义保持一致。
>
>
> 例如：
>
> ```sql
> CREATE TABLE t1(a INT, b INT);
> CREATE TABLE t2(a INT, b INT, INDEX ia(a));
> EXPLAIN SELECT /*+ INL_JOIN(t2) */ * FROM t1 JOIN t2 ON t1.a = t2.a;
> EXPLAIN SELECT (SELECT a FROM t2 WHERE t2.a = t1.b LIMIT 1) FROM t1;
> ```
>
> ```sql
> -- Before v6.4.0:
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 1.25     | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 1.25     | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 1.25     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 1.25     | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 1.00     | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 1.00     | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 1.00     | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 1.00     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> 
> -- Since v6.4.0:
>
> -- 你可以看到 `IndexLookUp_11`、`Selection_10`、`IndexRangeScan_8` 和 `TableRowIDScan_9` 的 `estRows` 值自 v6.4.0 之后与之前不同。
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 12487.50 | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 12487.50 | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 12500.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 12487.50 | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
>
> -- 你可以看到 `Limit_17`、`IndexReader_21`、`Limit_20` 和 `IndexRangeScan_19` 的 `estRows` 值自 v6.4.0 之后与之前不同。
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 10000.00 | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 10000.00 | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 10000.00 | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 10000.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> ```

### Operator 概述

操作符是执行查询结果返回过程中的特定步骤。执行表扫描（包括磁盘或 TiKV 块缓存）的操作符如下：

- **TableFullScan**：全表扫描
- **TableRangeScan**：指定范围的表扫描
- **TableRowIDScan**：基于 RowID 扫描表数据，通常跟在索引读取操作之后，用于获取匹配的数据行
- **IndexFullScan**：类似于“全表扫描”，但扫描的是索引而非表数据
- **IndexRangeScan**：指定范围的索引扫描

TiDB 会对从 TiKV/TiFlash 扫描的数据或计算结果进行聚合。数据聚合操作符可以分为以下几类：

- **TableReader**：聚合底层操作符（如 `TableFullScan` 或 `TableRangeScan`）在 TiKV 中获取的数据
- **IndexReader**：聚合底层操作符（如 `IndexFullScan` 或 `IndexRangeScan`）在 TiKV 中获取的数据
- **IndexLookUp**：先聚合 `Build` 端扫描到的 RowID（在 TiKV 中），然后在 `Probe` 端根据这些 RowID 精确读取 TiKV 中的数据。在 `Build` 端有 `IndexFullScan` 或 `IndexRangeScan` 操作符，在 `Probe` 端有 `TableRowIDScan` 操作符
- **IndexMerge**：类似于 `IndexLookUp`。`IndexMerge` 可以同时读取多个索引。它包含多个 `Build` 和一个 `Probe`。`IndexMerge` 的执行过程与 `IndexLookUp` 相同。

虽然结构表现为树形，但执行查询时并不严格要求子节点在父节点之前完成。TiDB 支持查询内的并行执行，因此更准确的描述是子节点 _流入_ 父节点。父、子和兄弟操作符 _可能_ 会在执行查询的不同部分同时进行。

在前例中，`├─IndexRangeScan_8(Build)` 操作符找到匹配索引 `a(a)` 的行的内部 `RowID`，然后 `└─TableRowIDScan_9(Probe)` 操作符根据这些 RowID 从表中检索对应的行。

#### Range 查询

在 `WHERE` / `HAVING` / `ON` 条件中，TiDB 优化器会分析由主键查询或索引键查询返回的结果。例如，这些条件可能包括数字和日期类型的比较运算符，如 `>`, `<`, `=`, `>=`, `<=`，以及字符类型的 `LIKE`。

> **Note:**
>
> - 为了使用索引，条件必须是 _sargable_。例如，条件 `YEAR(date_column) < 1992` 不能利用索引，但 `date_column < '1992-01-01` 可以。
> - 建议比较相同类型和 [字符集与排序规则](/character-set-and-collation.md) 的数据。类型混用可能需要额外的 `cast` 操作，或导致索引无法使用。
> - 你也可以使用 `AND`（交集）和 `OR`（并集）组合某一列的范围查询条件。对于多维复合索引，可以在多个列上使用条件。例如，关于复合索引 `(a, b, c)`：
>     - 当 `a` 为等值查询时，继续确定 `b` 的查询范围；当 `b` 也为等值查询时，继续确定 `c` 的查询范围。
>     - 否则，如果 `a` 为非等值查询，则只能确定 `a` 的范围。

### Task 概述

目前，TiDB 的计算任务可以分为两类：cop 任务和 root 任务。`cop[tikv]` 任务表示操作在 TiKV 的 coprocessor 内执行，`root` 任务表示在 TiDB 内完成。

SQL 优化的目标之一是尽可能将计算下推到 TiKV。TiKV 中的 Coprocessor 支持大部分内置的 SQL 函数（包括聚合函数和标量函数）、SQL `LIMIT` 操作、索引扫描和表扫描。

### Operator info 概述

`operator info` 可以显示有用的信息，例如哪些条件被成功下推：

* `range: [1,1]` 表示查询的 where 子句中的谓词（`a = 1`）已被下推到 TiKV（任务类型为 `cop[tikv]`）。
* `keep order:false` 表示该查询的语义不要求 TiKV 按顺序返回结果。如果查询被修改为需要排序（如 `SELECT * FROM t WHERE a = 1 ORDER BY id`），则此条件会变为 `keep order:true`。
* `stats:pseudo` 表示 `estRows` 中显示的估算值可能不准确。TiDB 会定期更新统计信息作为后台操作的一部分，也可以通过运行 `ANALYZE TABLE t` 手动更新。

不同的操作符在执行 `EXPLAIN` 后会输出不同的信息。你可以使用优化器提示（hints）来控制优化器的行为，从而控制物理操作符的选择。例如，`/*+ HASH_JOIN(t1, t2) */` 表示优化器使用 `Hash Join` 算法。更多详情请参见 [Optimizer Hints](/optimizer-hints.md)。