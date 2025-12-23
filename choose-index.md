---
title: 索引选择
summary: 为 TiDB 查询优化选择最佳索引。
---

# 索引选择

从存储引擎读取数据是 SQL 执行过程中最耗时的步骤之一。目前，TiDB 支持从不同的存储引擎和不同的索引读取数据。查询执行性能在很大程度上取决于是否选择了合适的索引。

本文档介绍了如何选择访问表的索引，以及一些控制索引选择的相关方法。

## 访问表

在介绍索引选择之前，首先需要了解 TiDB 访问表的方式、每种方式的触发条件、差异以及优缺点。

### 访问表的运算符

| 运算符 | 触发条件 | 适用场景 | 说明 |
| :------- | :------- | :------- | :---- |
| PointGet / BatchPointGet | 访问表时为一个或多个单点范围。 | 任意场景 | 如果被触发，通常认为是最快的运算符，因为它直接调用 kvget 接口进行计算，而不是调用 coprocessor 接口。 |
| TableReader | 无 | 任意场景 | 该 TableReader 运算符用于 TiKV。通常认为是效率最低的运算符，直接从 TiKV 层扫描表数据。只有在对 `_tidb_rowid` 列进行范围查询，或没有其他可选的访问表运算符时才会被选择。 |
| TableReader | 表在 TiFlash 节点上有副本。 | 需要读取的列较少，但需要评估的行很多。 | 该 TableReader 运算符用于 TiFlash。TiFlash 是列存储，如果只需计算少量列但需要处理大量行，推荐选择此运算符。 |
| IndexReader | 表有一个或多个索引，且计算所需的列包含在索引中。 | 对索引有较小范围查询，或对索引列有排序要求时。 | 当存在多个索引时，会根据成本估算选择合理的索引。 |
| IndexLookupReader | 表有一个或多个索引，且计算所需的列未完全包含在索引中。 | 同 IndexReader。 | 由于索引未完全覆盖计算列，TiDB 需要在读取索引后再从表中取回行。与 IndexReader 运算符相比有额外开销。 |
| IndexMerge | 表有多个索引或多值索引。 | 使用多值索引或多个索引时。 | 要使用该运算符，可以指定 [optimizer hints](/optimizer-hints.md)，或让优化器根据成本估算自动选择。详情参见 [Explain Statements Using Index Merge](/explain-index-merge.md)。 |

> **注意：**
>
> TableReader 运算符基于 `_tidb_rowid` 列索引，TiFlash 使用列存储索引，因此索引的选择即为访问表运算符的选择。

## 索引选择规则

TiDB 根据规则或成本选择索引。基于规则的选择包括预规则和 skyline-pruning。当选择索引时，TiDB 首先尝试预规则。如果某个索引满足预规则，TiDB 直接选择该索引。否则，TiDB 使用 skyline-pruning 排除不合适的索引，然后根据每个访问表运算符的成本估算，选择成本最低的索引。

### 基于规则的选择

#### 预规则

TiDB 使用以下启发式预规则选择索引：

+ 规则 1：如果某个索引满足“唯一索引全匹配 + 不需要从表中取回行（即该索引生成的计划为 IndexReader 运算符）”，TiDB 直接选择该索引。

+ 规则 2：如果某个索引满足“唯一索引全匹配 + 需要从表中取回行（即该索引生成的计划为 IndexLookupReader 运算符）”，TiDB 选择需要从表中取回行数最少的索引作为候选索引。

+ 规则 3：如果某个索引满足“普通索引 + 不需要从表中取回行 + 需要读取的行数小于某个阈值”，TiDB 选择需要读取行数最少的索引作为候选索引。

+ 规则 4：如果根据规则 2 和 3 只选出一个候选索引，则选择该候选索引。如果分别根据规则 2 和 3 各选出一个候选索引，则选择需要读取行数更少的索引（索引行数 + 需要从表中取回的行数）。

上述规则中的“全匹配索引”指每个索引列都有等值条件。执行 `EXPLAIN FORMAT = 'verbose' ...` 语句时，如果预规则命中某个索引，TiDB 会输出 NOTE 级别的警告，提示该索引命中预规则。

如下示例中，由于索引 `idx_b` 满足规则 2 中的“唯一索引全匹配 + 需要从表中取回行”，TiDB 选择 `idx_b` 作为访问路径，`SHOW WARNING` 返回 NOTE，提示索引 `idx_b` 命中预规则。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, UNIQUE INDEX idx_b(b));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT b, c FROM t WHERE b = 3 OR b = 6;
+-------------------+---------+---------+------+-------------------------+------------------------------+
| id                | estRows | estCost | task | access object           | operator info                |
+-------------------+---------+---------+------+-------------------------+------------------------------+
| Batch_Point_Get_5 | 2.00    | 8.80    | root | table:t, index:idx_b(b) | keep order:false, desc:false |
+-------------------+---------+---------+------+-------------------------+------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+-------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                   |
+-------+------+-------------------------------------------------------------------------------------------+
| Note  | 1105 | unique index idx_b of t is selected since the path only has point ranges with double scan |
+-------+------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### Skyline-pruning

Skyline-pruning 是一种索引的启发式过滤规则，可以降低因估算错误导致选错索引的概率。判断一个索引时，需要考虑以下维度：

- 索引列覆盖的访问条件数量。“访问条件”指可以转换为列范围的 where 条件。索引列集覆盖的访问条件越多，在该维度上越优。

- 选择该索引访问表时，是否需要从表中取回行（即该索引生成的计划为 IndexReader 运算符或 IndexLookupReader 运算符）。不需要从表中取回行的索引在该维度上优于需要取回行的索引。如果两个索引都需要从表中取回行，则比较索引列覆盖的过滤条件数量。过滤条件指可以基于索引判断的 where 条件。索引列集覆盖的访问条件越多，需要从表中取回的行数越少，在该维度上越优。

- 是否满足某种排序要求。因为索引读取可以保证某些列集的顺序，满足查询排序要求的索引在该维度上优于不满足的索引。

- 是否为 [全局索引](/global-indexes.md)。在分区表中，全局索引相比普通索引可以有效减少 SQL 的 cop 任务数量，从而提升整体性能。

对于上述维度，如果索引 `idx_a` 在所有三个维度上都不劣于索引 `idx_b`，且在某一维度上优于 `idx_b`，则优先选择 `idx_a`。执行 `EXPLAIN FORMAT = 'verbose' ...` 语句时，如果 skyline-pruning 排除了一些索引，TiDB 会输出 NOTE 级别的警告，列出 skyline-pruning 排除后剩余的索引。

如下示例中，索引 `idx_b` 和 `idx_e` 都劣于 `idx_b_c`，因此被 skyline-pruning 排除。`SHOW WARNING` 的返回结果显示了 skyline-pruning 后剩余的索引。

```sql
mysql> CREATE TABLE t(a INT PRIMARY KEY, b INT, c INT, d INT, e INT, INDEX idx_b(b), INDEX idx_b_c(b, c), INDEX idx_e(e));
Query OK, 0 rows affected (0.01 sec)

mysql> EXPLAIN FORMAT = 'verbose' SELECT * FROM t WHERE b = 2 AND c > 4;
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| id                            | estRows | estCost | task      | access object                | operator info                                      |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
| IndexLookUp_10                | 33.33   | 738.29  | root      |                              |                                                    |
| ├─IndexRangeScan_8(Build)     | 33.33   | 2370.00 | cop[tikv] | table:t, index:idx_b_c(b, c) | range:(2 4,2 +inf], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 33.33   | 2370.00 | cop[tikv] | table:t                      | keep order:false, stats:pseudo                     |
+-------------------------------+---------+---------+-----------+------------------------------+----------------------------------------------------+
3 rows in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;
+-------+------+------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                  |
+-------+------+------------------------------------------------------------------------------------------+
| Note  | 1105 | [t,idx_b_c] remain after pruning paths for t given Prop{SortItems: [], TaskTp: rootTask} |
+-------+------+------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 基于成本估算的选择

使用 skyline-pruning 规则排除不合适的索引后，索引的选择完全基于成本估算。访问表的成本估算需要考虑以下因素：

- 存储引擎中索引数据每行的平均长度。
- 索引生成的查询范围内的行数。
- 从表中取回行的成本。
- 查询执行过程中索引生成的范围数量。

根据这些因素和成本模型，优化器会选择成本最低的索引访问表。

#### 基于成本估算选择的常见调优问题

1. 估算的行数不准确？

    通常是由于统计信息过期或不准确。你可以重新执行 `ANALYZE TABLE` 语句，或修改 `ANALYZE TABLE` 语句的参数。

2. 统计信息准确，且从 TiFlash 读取更快，但为什么优化器选择从 TiKV 读取？

    目前区分 TiFlash 和 TiKV 的成本模型还比较粗糙。你可以降低 [`tidb_opt_seek_factor`](/system-variables.md#tidb_opt_seek_factor) 参数的值，这样优化器会更倾向于选择 TiFlash。

3. 统计信息准确，索引 A 需要从表中取回行，但实际执行比不需要取回行的索引 B 更快，为什么优化器选择了索引 B？

    这种情况下，可能是取回行的成本估算过大。你可以降低 [`tidb_opt_network_factor`](/system-variables.md#tidb_opt_network_factor) 参数的值，以降低取回行的成本。

## 控制索引选择

可以通过 [Optimizer Hints](/optimizer-hints.md) 在单条查询中控制索引选择。

- `USE_INDEX` / `IGNORE_INDEX` 可以强制优化器使用/不使用某些索引。`FORCE_INDEX` 和 `USE_INDEX` 效果相同。

- `READ_FROM_STORAGE` 可以强制优化器为某些表选择 TiKV / TiFlash 存储引擎执行查询。

## 使用多值索引

[多值索引](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) 与普通索引不同。TiDB 目前仅通过 [IndexMerge](/explain-index-merge.md) 访问多值索引。因此，要使用多值索引进行数据访问，请确保系统变量 [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) 的值为 `ON`。

关于多值索引的限制，参见 [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md#limitations)。

### 支持的场景

目前，TiDB 支持通过 IndexMerge 自动转换 `json_member_of`、`json_contains` 和 `json_overlaps` 条件访问多值索引。你可以依赖优化器根据成本自动选择 IndexMerge，也可以通过优化器 hint [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 或 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 指定选择多值索引。如下示例：

```sql
mysql> CREATE TABLE t1 (j JSON, INDEX idx((CAST(j->'$.path' AS SIGNED ARRAY)))); -- Uses '$.path' as the path to create a multi-valued index
Query OK, 0 rows affected (0.04 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE (1 MEMBER OF (j->'$.path'));
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                          |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_memberof(cast(1, json BINARY), json_extract(test.t1.j, "$.path")) |
| └─IndexMerge_8                  | 10.00   | root      |                                                                             | type: union                                                            |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                            |
|   └─TableRowIDScan_7(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                         |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 10.00   | root      |                                                                             | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
5 rows in set (0.00 sec)

mysql> EXPLAIN SELECT /*+ use_index_merge(t1, idx) */ * FROM t1 WHERE JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                               | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 8000.00 | root      |                                                                             | json_overlaps(json_extract(test.t1.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 10.00   | root      |                                                                             | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo                                      |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t1, index:idx(cast(json_extract(`j`, _utf8'$.path') as signed array)) | range:[3,3], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t1                                                                    | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------------------------------------+
6 rows in set, 1 warning (0.00 sec)
```

复合多值索引也可以通过 IndexMerge 访问：

```sql
CREATE TABLE t2 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j->'$.path' AS SIGNED ARRAY)), b), INDEX idx2(b, (CAST(k->'$.path' AS SIGNED ARRAY))));
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
EXPLAIN SELECT /*+ use_index_merge(t2, idx, idx2) */ * FROM t2 WHERE (a=1 AND 1 member of (j->'$.path')) AND (b=1 AND 2 member of (k->'$.path'));
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND (1 MEMBER OF (j->'$.path')) AND b=2;
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                       |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| IndexMerge_7                  | 0.00    | root      |                                                                                   | type: union                                         |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 2,1 1 2], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                      |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_CONTAINS((j->'$.path'), '[1, 2, 3]');
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                   |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+
| IndexMerge_9                  | 0.00    | root      |                                                                                   | type: intersection                              |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx) */ * FROM t2 WHERE a=1 AND JSON_OVERLAPS((j->'$.path'), '[1, 2, 3]');
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| id                              | estRows | task      | access object                                                                     | operator info                                                                    |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| Selection_5                     | 0.24    | root      |                                                                                   | json_overlaps(json_extract(test.t2.j, "$.path"), cast("[1, 2, 3]", json BINARY)) |
| └─IndexMerge_10                 | 0.30    | root      |                                                                                   | type: union                                                                      |
|   ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1,1 1], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_7(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                  |
|   ├─IndexRangeScan_8(Build)     | 0.10    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 3,1 3], keep order:false, stats:pseudo                                  |
|   └─TableRowIDScan_9(Probe)     | 0.30    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                                                   |
+---------------------------------+---------+-----------+-----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t2, idx, idx2) */ * FROM t2 WHERE (a=1 AND 1 member of (j->'$.path')) AND (b=1 AND 2 member of (k->'$.path'));
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                                                                     | operator info                                       |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
| IndexMerge_8                  | 0.00    | root      |                                                                                   | type: intersection                                  |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t2, index:idx(a, cast(json_extract(`j`, _utf8'$.path') as signed array), b) | range:[1 1 1,1 1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t2, index:idx2(b, cast(json_extract(`k`, _utf8'$.path') as signed array))   | range:[1 2,1 2], keep order:false, stats:pseudo     |
| └─TableRowIDScan_7(Probe)     | 0.00    | cop[tikv] | table:t2                                                                          | keep order:false, stats:pseudo                      |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------------+-----------------------------------------------------+
```

TiDB 也可以通过 IndexMerge 同时访问多值索引和普通索引。例如：

```sql
CREATE TABLE t3(j1 JSON, j2 JSON, a INT, INDEX k1((CAST(j1->'$.path' AS SIGNED ARRAY))), INDEX k2((CAST(j2->'$.path' AS SIGNED ARRAY))), INDEX ka(a));
EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') OR a = 3;
EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') AND 2 member of (j2->'$.path') AND (a = 3);
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') OR a = 3;
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_8                  | 19.99   | root      |                                                                             | type: union                                 |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t3, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t3, index:ka(a)                                                       | range:[3,3], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 19.99   | cop[tikv] | table:t3                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

> EXPLAIN SELECT /*+ use_index_merge(t3, k1, k2, ka) */ * FROM t3 WHERE 1 member of (j1->'$.path') AND 2 member of (j2->'$.path') AND (a = 3);
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| id                            | estRows | task      | access object                                                               | operator info                               |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
| IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t3, index:ka(a)                                                       | range:[3,3], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t3, index:k1(cast(json_extract(`j1`, _utf8'$.path') as signed array)) | range:[1,1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t3, index:k2(cast(json_extract(`j2`, _utf8'$.path') as signed array)) | range:[2,2], keep order:false, stats:pseudo |
| └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t3                                                                    | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
```

如果多个 `json_member_of`、`json_contains` 或 `json_overlaps` 条件通过 `OR` 或 `AND` 连接，则需要满足以下要求才能通过 IndexMerge 访问多值索引：

```sql
CREATE TABLE t4(a INT, j JSON, INDEX mvi1((CAST(j->'$.a' AS UNSIGNED ARRAY))), INDEX mvi2((CAST(j->'$.b' AS UNSIGNED ARRAY))));
```

- 对于通过 `OR` 连接的条件，每个条件都需要能够分别通过 IndexMerge 访问。例如：

    ```sql
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_overlaps(j->'$.a', '[3, 4]');
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_length(j->'$.a') = 3;
    SHOW WARNINGS;
    ```

    ```sql
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_overlaps(j->'$.a', '[3, 4]');
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | id                               | estRows | task      | access object                                                               | operator info                                                                                                                                              |
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Selection_5                      | 31.95   | root      |                                                                             | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1, 2]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.a"), cast("[3, 4]", json BINARY))) |
    | └─IndexMerge_11                  | 39.94   | root      |                                                                             | type: union                                                                                                                                                |
    |   ├─IndexRangeScan_6(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_7(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_8(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                |
    |   ├─IndexRangeScan_9(Build)      | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo                                                                                                                |
    |   └─TableRowIDScan_10(Probe)     | 39.94   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                             |
    +----------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    
    -- json_length(j->'$.a') = 3 不能直接通过 IndexMerge 访问，因此 TiDB 无法为该 SQL 语句使用 IndexMerge。
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1, 2]') OR json_length(j->'$.a') = 3;
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
    | id                      | estRows  | task      | access object | operator info                                                                                                                      |
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
    | Selection_5             | 8000.00  | root      |               | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1, 2]", json BINARY)), eq(json_length(json_extract(test.t4.j, "$.a")), 3)) |
    | └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                               |
    |   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t4      | keep order:false, stats:pseudo                                                                                                     |
    +-------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
    
    > SHOW WARNINGS;
    +---------+------+----------------------------+
    | Level   | Code | Message                    |
    +---------+------+----------------------------+
    | Warning | 1105 | IndexMerge is inapplicable |
    +---------+------+----------------------------+
    ```

- 对于通过 `AND` 连接的条件，只要部分条件可以分别通过 IndexMerge 访问，TiDB 就可以使用 IndexMerge 访问这些条件对应的多值索引。例如：

    ```sql
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]');
    EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]') AND json_length(j->'$.a') = 2;
    ```

    ```sql
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]');
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
    | id                            | estRows | task      | access object                                                               | operator info                               |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
    | IndexMerge_10                 | 0.00    | root      |                                                                             | type: intersection                          |
    | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
    | ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo |
    | └─TableRowIDScan_9(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
    
    -- json_length(j->'$.a') = 3 不能直接通过 IndexMerge 访问，因此 TiDB 只对前两个 json_contains 条件使用 IndexMerge，json_length(j->'$.a') = 3 变为 Selection 运算符。
    > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1) */ * FROM t4 WHERE json_contains(j->'$.a', '[1, 2]') AND json_contains(j->'$.a', '[3, 4]') AND json_length(j->'$.a') = 2;
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    | id                            | estRows | task      | access object                                                               | operator info                                      |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    | IndexMerge_11                 | 0.00    | root      |                                                                             | type: intersection                                 |
    | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo        |
    | ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[4,4], keep order:false, stats:pseudo        |
    | └─Selection_10(Probe)         | 0.00    | cop[tikv] |                                                                             | eq(json_length(json_extract(test.t4.j, "$.a")), 2) |
    |   └─TableRowIDScan_9          | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                     |
    +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+----------------------------------------------------+
    ```

- 所有用于 IndexMerge 的条件必须与连接它们的 `OR` 或 `AND` 语义一致。

    - 如果 `json_contains` 通过 `AND` 连接，则语义一致。例如：

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') AND json_contains(j->'$.b', '[2, 3]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2, 3]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') AND json_contains(j->'$.b', '[2, 3]');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

        -- 条件语义不一致，因此 TiDB 无法为该 SQL 语句使用 IndexMerge，如上所述。
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2, 3]');
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                      | estRows  | task      | access object | operator info                                                                                                                                           |
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | TableReader_7           | 10.01    | root      |               | data:Selection_6                                                                                                                                        |
        | └─Selection_6           | 10.01    | cop[tikv] |               | or(json_contains(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_contains(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY))) |
        |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t4      | keep order:false, stats:pseudo                                                                                                                          |
        +-------------------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

    - 如果 `json_overlaps` 通过 `OR` 连接，则语义一致。例如：

        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') OR json_overlaps(j->'$.b', '[2, 3]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2, 3]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') OR json_overlaps(j->'$.b', '[2, 3]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                           |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 23.98   | root      |                                                                             | or(json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY))) |
        | └─IndexMerge_10                 | 29.97   | root      |                                                                             | type: union                                                                                                                                             |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                             |
        |   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                             |
        |   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                             |
        |   └─TableRowIDScan_9(Probe)     | 29.97   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                          |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
        
        -- 条件语义不一致，因此 TiDB 只能对该 SQL 语句的部分条件使用 IndexMerge，如上所述。
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2, 3]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                       |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 15.99   | root      |                                                                             | json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2, 3]", json BINARY)) |
        | └─IndexMerge_8                  | 10.00   | root      |                                                                             | type: union                                                                                                                                         |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                         |
        |   └─TableRowIDScan_7(Probe)     | 10.00   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                      |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

    - 如果 `json_member_of` 通过 `OR` 或 `AND` 连接，则语义一致。例如：
        
        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND 2 member of (j->'$.b') AND 3 member of (j->'$.a');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR 2 member of (j->'$.b') OR 3 member of (j->'$.a');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND 2 member of (j->'$.b') AND 3 member of (j->'$.a');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: intersection                          |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 0.00    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+

        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR 2 member of (j->'$.b') OR 3 member of (j->'$.a');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_9                  | 29.97   | root      |                                                                             | type: union                                 |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo |
        | └─TableRowIDScan_8(Probe)     | 29.97   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        ```

    - 如果包含多个值的 `json_contains` 条件通过 `OR` 连接，或包含多个值的 `json_overlaps` 条件通过 `AND` 连接，则语义不一致，但如果只包含一个值则语义一致。例如：
        
        ```sql
        -- 不匹配语义的条件参见前述示例。以下仅给出匹配语义的条件示例。
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2]');
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2]');
        ```

        ```sql
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_overlaps(j->'$.a', '[1]') AND json_overlaps(j->'$.b', '[2]');
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                              | estRows | task      | access object                                                               | operator info                                                                                                                                    |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
        | Selection_5                     | 8.00    | root      |                                                                             | json_overlaps(json_extract(test.t4.j, "$.a"), cast("[1]", json BINARY)), json_overlaps(json_extract(test.t4.j, "$.b"), cast("[2]", json BINARY)) |
        | └─IndexMerge_9                  | 0.01    | root      |                                                                             | type: intersection                                                                                                                               |
        |   ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                      |
        |   ├─IndexRangeScan_7(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                      |
        |   └─TableRowIDScan_8(Probe)     | 0.01    | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                   |
        +---------------------------------+---------+-----------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+
        
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE json_contains(j->'$.a', '[1]') OR json_contains(j->'$.b', '[2]');
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                               |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        | IndexMerge_8                  | 19.99   | root      |                                                                             | type: union                                 |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo |
        | └─TableRowIDScan_7(Probe)     | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo              |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+---------------------------------------------+
        ```

    - 当同时使用 `OR` 和 `AND` 连接条件（本质上是嵌套的 `OR` 和 `AND`）时，构成 IndexMerge 的条件必须全部匹配 `OR` 语义或全部匹配 `AND` 语义，不能部分匹配 `OR` 语义、部分匹配 `AND` 语义。例如：
        
        ```sql
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND (2 member of (j->'$.b') OR 3 member of (j->'$.a'));
        EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR (2 member of (j->'$.b') AND 3 member of (j->'$.a'));
        ```

        ```sql
        -- 只有 2 member of (j->'$.b') 和 3 member of (j->'$.a') 匹配 OR 语义，构成 IndexMerge。1 member of (j->'$.a') 匹配 AND 语义，不包含在内。
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') AND (2 member of (j->'$.b') OR 3 member of (j->'$.a'));
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                                                                                                                                                                                                     |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | IndexMerge_9                  | 0.00    | root      |                                                                             | type: union                                                                                                                                                                                                       |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi2(cast(json_extract(`j`, _utf8'$.b') as unsigned array)) | range:[2,2], keep order:false, stats:pseudo                                                                                                                                                                       |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                                                                       |
        | └─Selection_8(Probe)          | 0.00    | cop[tikv] |                                                                             | json_memberof(cast(1, json BINARY), json_extract(test.t4.j, "$.a")), or(json_memberof(cast(2, json BINARY), json_extract(test.t4.j, "$.b")), json_memberof(cast(3, json BINARY), json_extract(test.t4.j, "$.a"))) |
        |   └─TableRowIDScan_7          | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                                                                                    |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

        -- 只有 1 member of (j->'$.a') 和 2 member of (j->'$.a') 匹配 OR 语义，构成 IndexMerge。2 member of (j->'$.b') 匹配 AND 语义，不包含在内。
        > EXPLAIN SELECT /*+ use_index_merge(t4, mvi1, mvi2) */ * FROM t4 WHERE 1 member of (j->'$.a') OR (2 member of (j->'$.b') AND 3 member of (j->'$.a'));
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | id                            | estRows | task      | access object                                                               | operator info                                                                                                                                                                                                          |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | IndexMerge_9                  | 0.02    | root      |                                                                             | type: union                                                                                                                                                                                                            |
        | ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[1,1], keep order:false, stats:pseudo                                                                                                                                                                            |
        | ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:t4, index:mvi1(cast(json_extract(`j`, _utf8'$.a') as unsigned array)) | range:[3,3], keep order:false, stats:pseudo                                                                                                                                                                            |
        | └─Selection_8(Probe)          | 0.02    | cop[tikv] |                                                                             | or(json_memberof(cast(1, json BINARY), json_extract(test.t4.j, "$.a")), and(json_memberof(cast(2, json BINARY), json_extract(test.t4.j, "$.b")), json_memberof(cast(3, json BINARY), json_extract(test.t4.j, "$.a")))) |
        |   └─TableRowIDScan_7          | 19.99   | cop[tikv] | table:t4                                                                    | keep order:false, stats:pseudo                                                                                                                                                                                         |
        +-------------------------------+---------+-----------+-----------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        ```

如果条件中包含嵌套的 `OR`/`AND`，或条件经过变换（如展开）后仅对应索引列，TiDB 可能无法使用 IndexMerge 或无法充分利用所有条件。建议对每个具体场景进行验证。

以下是一些示例：

```sql
CREATE TABLE t5 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY))), INDEX idx2(b, (CAST(k as SIGNED ARRAY))));
CREATE TABLE t6 (a INT, j JSON, b INT, k JSON, INDEX idx(a, (CAST(j AS SIGNED ARRAY)), b), INDEX idx2(a, (CAST(k as SIGNED ARRAY)), b));
```

如果 `AND` 嵌套在通过 `OR` 连接的条件中，且通过 `AND` 连接的子条件正好对应多列索引的列，TiDB 通常可以充分利用这些条件。例如：

```sql
EXPLAIN SELECT /*+ use_index_merge(t5, idx, idx2) */ * FROM t5 WHERE (a=1 AND 1 member of (j)) OR (b=2 AND 2 member of (k));
```

```sql
> EXPLAIN SELECT /*+ use_index_merge(t5, idx, idx2) */ * FROM t5 WHERE (a=1 AND 1 member of (j)) OR (b=2 AND 2 member of (k));
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| id                            | estRows | task      | access object                                      | operator info                                   |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
| IndexMerge_8                  | 0.20    | root      |                                                    | type: union                                     |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t5, index:idx(a, cast(`j` as signed array))  | range:[1 1,1 1], keep order:false, stats:pseudo |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t5, index:idx2(b, cast(`k` as signed array)) | range:[2 2,2 2], keep order:false, stats:pseudo |
| └─TableRowIDScan_7(Probe)     | 0.20    | cop[tikv] | table:t5                                           | keep order:false, stats:pseudo                  |
+-------------------------------+---------+-----------+----------------------------------------------------+-------------------------------------------------+
```

如果单个 `OR` 嵌套在通过 `AND` 连接的条件中，且通过 `OR` 连接的子条件经过展开后对应索引列，TiDB 通常可以充分利用这些条件。例如：

```sql
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k));
```

```sql
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                           |
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_9                  | 0.20    | root      |                                                       | type: union                                                                                                             |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1,1 1], keep order:false, stats:pseudo                                                                         |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                                                         |
| └─Selection_8(Probe)          | 0.20    | cop[tikv] |                                                       | eq(test2.t6.a, 1), or(json_memberof(cast(1, json BINARY), test2.t6.j), json_memberof(cast(2, json BINARY), test2.t6.k)) |
|   └─TableRowIDScan_7          | 0.20    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                          |
+-------------------------------+---------+-----------+-------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
```

如果多个 `OR` 嵌套在通过 `AND` 连接的条件中，且通过 `OR` 连接的子条件需要展开后才能对应索引列，TiDB 可能无法充分利用所有条件。例如：

```sql
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k)) and (b = 1 OR b = 2);
EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND ((1 member of (j) AND b = 1) OR (1 member of (j) AND b = 2) OR (2 member of (k) AND b = 1) OR (2 member of (k) AND b = 2));
```

```sql
-- 由于当前实现限制，(b = 1 or b = 2) 不构成 IndexMerge，而是变为 Selection 运算符
> EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND (1 member of (j) OR 2 member of (k)) AND (b = 1 OR b = 2);
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                                                                |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_9                  | 0.20    | root      |                                                       | type: union                                                                                                                                                  |
| ├─IndexRangeScan_5(Build)     | 0.10    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1,1 1], keep order:false, stats:pseudo                                                                                                              |
| ├─IndexRangeScan_6(Build)     | 0.10    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2,1 2], keep order:false, stats:pseudo                                                                                                              |
| └─Selection_8(Probe)          | 0.20    | cop[tikv] |                                                       | eq(test.t6.a, 1), or(eq(test.t6.b, 1), eq(test.t6.b, 2)), or(json_memberof(cast(1, json BINARY), test.t6.j), json_memberof(cast(2, json BINARY), test.t6.k)) |
|   └─TableRowIDScan_7          | 0.20    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                                                               |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- 如果你手动展开通过 AND 连接的两个 OR 条件，TiDB 可以充分利用这些条件
> EXPLAIN SELECT /*+ use_index_merge(t6, idx, idx2) */ * FROM t6 WHERE a=1 AND ((1 member of (j) AND b = 1) OR (1 member of (j) AND b = 2) OR (2 member of (k) AND b = 1) OR (2 member of (k) AND b = 2));
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object                                         | operator info                                                                                                                                                                                                                                                                                                            |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexMerge_11                 | 0.00    | root      |                                                       | type: union                                                                                                                                                                                                                                                                                                              |
| ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1 1,1 1 1], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_6(Build)     | 0.00    | cop[tikv] | table:t6, index:idx(a, cast(`j` as signed array), b)  | range:[1 1 2,1 1 2], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_7(Build)     | 0.00    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2 1,1 2 1], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| ├─IndexRangeScan_8(Build)     | 0.00    | cop[tikv] | table:t6, index:idx2(a, cast(`k` as signed array), b) | range:[1 2 2,1 2 2], keep order:false, stats:pseudo                                                                                                                                                                                                                                                                      |
| └─Selection_10(Probe)         | 0.00    | cop[tikv] |                                                       | eq(test.t6.a, 1), or(or(and(json_memberof(cast(1, json BINARY), test.t6.j), eq(test.t6.b, 1)), and(json_memberof(cast(1, json BINARY), test.t6.j), eq(test.t6.b, 2))), or(and(json_memberof(cast(2, json BINARY), test.t6.k), eq(test.t6.b, 1)), and(json_memberof(cast(2, json BINARY), test.t6.k), eq(test.t6.b, 2)))) |
|   └─TableRowIDScan_9          | 0.00    | cop[tikv] | table:t6                                              | keep order:false, stats:pseudo                                                                                                                                                                                                                                                                                           |
+-------------------------------+---------+-----------+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

受当前多值索引实现限制，使用 [`use_index`](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) 可能会返回 `Can't find a proper physical plan for this query` 错误，而使用 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-) 不会返回此类错误。因此，如果你想使用多值索引，推荐使用 `use_index_merge`。

```sql
mysql> EXPLAIN SELECT /*+ use_index(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
ERROR 1815 (HY000): Internal : Cant find a proper physical plan for this query

mysql> EXPLAIN SELECT /*+ use_index_merge(t3, idx) */ * FROM t3 WHERE ((1 member of (j)) AND (2 member of (j))) OR ((3 member of (j)) AND (4 member of (j)));
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                                                                                                                |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | or(and(json_memberof(cast(1, json BINARY), test.t3.j), json_memberof(cast(2, json BINARY), test.t3.j)), and(json_memberof(cast(3, json BINARY), test.t3.j), json_memberof(cast(4, json BINARY), test.t3.j))) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                                                                                                                                                                                         |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                                                                                                               |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set, 2 warnings (0.00 sec)
```

### 多值索引与计划缓存

使用 `member of` 选择多值索引的查询计划可以被缓存。使用 `JSON_CONTAINS()` 或 `JSON_OVERLAPS()` 函数选择多值索引的查询计划无法被缓存。

以下是可以缓存查询计划的示例：

```sql
mysql> CREATE TABLE t5 (j1 JSON, j2 JSON, INDEX idx1((CAST(j1 AS SIGNED ARRAY))));
Query OK, 0 rows affected (0.04 sec)

mysql> PREPARE st FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE (? member of (j1))';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a=1;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE st USING @a;
Empty set (0.01 sec)

mysql> EXECUTE st USING @a;
Empty set (0.00 sec)

mysql> SELECT @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)

mysql> PREPARE st FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE (? member of (j1)) AND JSON_CONTAINS(j2, ?)';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a=1, @b='[1,2]';
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE st USING @a, @b;
Empty set (0.00 sec)

mysql> EXECUTE st USING @a, @b;
Empty set (0.00 sec)

mysql> SELECT @@LAST_PLAN_FROM_CACHE; -- can hit plan cache if the JSON_CONTAINS doesn't impact index selection
+------------------------+
| @@LAST_PLAN_FROM_CACHE |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

以下是无法缓存查询计划的示例：

```sql
mysql> PREPARE st2 FROM 'SELECT /*+ use_index(t5, idx1) */ * FROM t5 WHERE JSON_CONTAINS(j1, ?)';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @a='[1,2]';
Query OK, 0 rows affected (0.01 sec)

mysql> EXECUTE st2 USING @a;
Empty set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS;  -- cannot hit plan cache since the JSON_CONTAINS predicate might affect index selection
+---------+------+-------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                               |
+---------+------+-------------------------------------------------------------------------------------------------------+
| Warning | 1105 | skip prepared plan-cache: json_contains function with immutable parameters can affect index selection |
+---------+------+-------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```