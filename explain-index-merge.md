---
title: 使用索引合并解释语句
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# 使用索引合线解释语句

索引合线（Index merge）是 TiDB 在 v4.0 版本中引入的一种访问表的方法。通过这种方法，TiDB 优化器可以对每个表使用多个索引，并合并每个索引返回的结果。在某些场景下，这种方法可以避免全表扫描，从而提高查询效率。

TiDB 中的索引合线有两种类型：交集型（intersection）和并集型（union）。前者适用于 `AND` 表达式，后者适用于 `OR` 表达式。并集型索引合线在 TiDB v4.0 中作为实验性功能引入，已在 v5.4.0 版本中正式成为 GA（一般可用）。交集型则在 TiDB v6.5.0 中引入，且只能在指定 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 提示时使用。

## 启用索引合线

在 v5.4.0 或更高版本的 TiDB 中，索引合线默认已开启。在其他情况下，如果未启用索引合线，则需要将变量 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) 设置为 `ON` 以启用此功能。

```sql
SET session tidb_enable_index_merge = ON;
```

## 示例

```sql
CREATE TABLE t(a int, b int, c int, d int, INDEX idx_a(a), INDEX idx_b(b), INDEX idx_c(c), INDEX idx_d(d));
```

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a = 1 OR b = 1;

+-------------------------+----------+-----------+---------------+--------------------------------------+
| id                      | estRows  | task      | access object | operator info                        |
+-------------------------+----------+-----------+---------------+--------------------------------------+
| TableReader_7           | 19.99    | root      |               | data:Selection_6                     |
| └─Selection_6           | 19.99    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+----------+-----------+---------------+--------------------------------------+
EXPLAIN SELECT /*+ USE_INDEX_MERGE(t) */ * FROM t WHERE a > 1 OR b > 1;
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_8                  | 5555.56 | root      |                         | type: union                                    |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 5555.56 | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

在上述查询中，过滤条件是一个使用 `OR` 连接的 `WHERE` 子句。如果没有索引合线，你每个表只能使用一个索引。`a = 1` 不能被下推到索引 `a`，`b = 1` 也不能被下推到索引 `b`。当 `t` 中存在大量数据时，全表扫描效率较低。为应对这种场景，TiDB 引入索引合线以访问表。

对于上述查询，优化器选择了并集型索引合线来访问表。索引合线允许优化器在每个表上使用多个索引，合并每个索引返回的结果，从而生成上述输出中的执行计划。

在输出中，`operator info` 中的 `type: union` 表示该 `IndexMerge_8` 操作符是一个并集型索引合线。它有三个子节点：`IndexRangeScan_5` 和 `IndexRangeScan_6` 根据范围扫描满足条件的 `RowID`，然后 `TableRowIDScan_7` 操作符根据这些 `RowID` 精确读取所有满足条件的数据。

对于在特定范围数据上执行的扫描操作（如 `IndexRangeScan` / `TableRangeScan`），在结果的 `operator info` 列中会比其他扫描操作（如 `IndexFullScan` / `TableFullScan`）提供额外的扫描范围信息。在上述示例中，`IndexRangeScan_5` 操作符中的 `range:(1,+inf]` 表示该操作符从 1 扫描到正无穷。

```sql
EXPLAIN SELECT /*+ NO_INDEX_MERGE() */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- 不使用索引合线

+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                             | estRows | task      | access object           | operator info                               |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexLookUp_19                 | 1.11    | root      |                         |                                             |
| ├─IndexRangeScan_16(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo |
| └─Selection_18(Probe)          | 1.11    | cop[tikv] |                         | gt(test.t.a, 1), gt(test.t.b, 1)            |
|   └─TableRowIDScan_17          | 10.00   | cop[tikv] | table:t                 | keep order:false, stats:pseudo              |
+--------------------------------+---------+-----------+-------------------------+---------------------------------------------+

EXPLAIN SELECT /*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */ * FROM t WHERE a > 1 AND b > 1 AND c = 1;  -- 使用索引合线
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| id                            | estRows | task      | access object           | operator info                                  |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
| IndexMerge_9                  | 1.11    | root      |                         | type: intersection                            |
| ├─IndexRangeScan_5(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_a(a) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 3333.33 | cop[tikv] | table:t, index:idx_b(b) | range:(1,+inf], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t, index:idx_c(c) | range:[1,1], keep order:false, stats:pseudo    |
| └─TableRowIDScan_8(Probe)     | 1.11    | cop[tikv] | table:t                 | keep order:false, stats:pseudo                 |
+-------------------------------+---------+-----------+-------------------------+------------------------------------------------+
```

从上述示例可以看出，过滤条件是一个使用 `AND` 连接的 `WHERE` 子句。在启用索引合线之前，优化器只能选择三个索引中的一个（`idx_a`、`idx_b` 或 `idx_c`）。

如果其中一个过滤条件的选择性较低，优化器会直接选择对应的索引以实现理想的执行效率。但如果满足以下三个条件中的所有条件，可以考虑使用交集型索引合线：

- 整个表的数据量较大，直接读取整个表效率低下。
- 每个过滤条件的选择性都非常高，因此单个索引的 `IndexLookUp` 执行效率不理想。
- 三个过滤条件的整体选择性较低。

在使用交集型索引合线访问表时，优化器可以选择在一张表上使用多个索引，并合并每个索引返回的结果，从而生成上述输出中的 `IndexMerge` 执行计划。`operator info` 中的 `type: intersection` 表示该 `IndexMerge_9` 操作符是交集型索引合线。其他部分的执行计划与前述的并集型索引合线示例类似。

> **Note:**
>
> - 索引合线功能从 v5.4.0 开始默认启用，即 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) 为 `ON`。
>
> - 你可以使用 SQL 提示 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 强制优化器应用索引合线，无论 `tidb_enable_index_merge` 的设置如何。若过滤条件中包含无法下推的表达式，必须使用此提示启用索引合线。
>
> - 如果优化器能为某个查询计划选择单一索引扫描方式（非全表扫描），则不会自动使用索引合线。要让优化器使用索引合线，你需要使用优化器提示。从 v8.1.0 开始，可以通过设置 [Optimizer Fix Control 52869](/optimizer-fix-controls.md#52869-new-in-v810) 来移除此限制。移除后，优化器可以在更多查询中自动选择索引合线，但可能会忽略最优执行计划。因此，建议在实际用例中充分测试后再移除此限制，以确保不会引起性能回归。
>
> - 目前索引合线不支持 [临时表](/temporary-tables.md)。
>
> - 交集型索引合线不会被优化器自动选择，必须通过 [`USE_INDEX_MERGE`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 提示明确指定表名和索引名，才能被选中。
