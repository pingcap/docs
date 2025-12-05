---
title: "`ANALYZE` 嵌入 DDL 语句"
summary: 本文档介绍了在新建或重组索引的 DDL 语句中嵌入的 `ANALYZE` 功能，该功能确保新索引的统计信息能够及时更新。
---

# `ANALYZE` 嵌入 DDL 语句 <span class="version-mark">v8.5.4 引入</span>

本文档介绍了在以下两类 DDL 语句中嵌入的 `ANALYZE` 功能：

- 创建新索引的 DDL 语句：[**ADD INDEX**](/sql-statements/sql-statement-add-index.md)
- 重组已有索引的 DDL 语句：[**MODIFY COLUMN**](/sql-statements/sql-statement-modify-column.md) 和 [**CHANGE COLUMN**](/sql-statements/sql-statement-change-column.md)

当该功能开启时，TiDB 会在新建或重组的索引对用户可见之前，自动执行一次 `ANALYZE`（统计信息收集）操作。这可以防止在索引创建或重组后，由于统计信息暂时不可用而导致优化器估算不准确及潜在的执行计划变更。

## 使用场景

在交替进行索引添加或修改的 DDL 操作场景下，现有的稳定查询可能因为新索引缺乏统计信息而出现估算偏差，导致优化器选择次优的执行计划。更多信息可参考 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)。

例如：

```sql
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t SELECT * FROM t; -- * N times

ALTER TABLE t ADD INDEX idx_a (a);

EXPLAIN SELECT * FROM t WHERE a > 4;
```

```
+-------------------------+-----------+-----------+---------------+--------------------------------+
| id                      | estRows   | task      | access object | operator info                  |
+-------------------------+-----------+-----------+---------------+--------------------------------+
| TableReader_8           | 131072.00 | root      |               | data:Selection_7               |
| └─Selection_7           | 131072.00 | cop[tikv] |               | gt(test.t.a, 4)                |
|   └─TableFullScan_6     | 393216.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+-----------+-----------+---------------+--------------------------------+
3 rows in set (0.002 sec)
```

在上述执行计划中，由于新建索引尚未有统计信息，TiDB 只能依赖启发式规则进行路径估算。除非索引访问路径无需回表且成本显著更低，否则优化器更倾向于选择更稳定的现有路径。在上述例子中，选择了全表扫描。但从数据分布来看，`t.a > 4` 实际返回 0 行，如果使用新索引 `idx_a`，查询可以快速定位相关行，避免全表扫描。此例中，由于 DDL 创建索引后未及时收集统计信息，生成的执行计划并不最优，但优化器仍然沿用原有计划，因此查询性能不会出现明显回退。然而，根据 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)，在某些情况下，启发式规则可能导致对新旧索引的不合理比较，剪枝掉原计划依赖的索引，最终退化为全表扫描。

自 v8.5.0 起，TiDB 已改进了索引间的启发式比较及统计信息缺失时的行为。但在某些复杂场景下，在 DDL 中嵌入 `ANALYZE` 是防止计划变更的最佳方式。你可以通过系统变量 [**tidb_stats_update_during_ddl**](/system-variables.md#tidb_stats_update_during_ddl-new-in-v854) 控制在索引创建或重组时是否执行嵌入式 `ANALYZE`。该变量默认值为 `OFF`。

## `ADD INDEX` DDL

当 `tidb_stats_update_during_ddl` 为 `ON` 时，执行 [**ADD INDEX**](/sql-statements/sql-statement-add-index.md) 会在 Reorg 阶段结束后自动执行一次嵌入式 `ANALYZE` 操作。该操作会在新建索引对用户可见前收集索引的统计信息，随后 `ADD INDEX` 进入后续阶段。

考虑到 `ANALYZE` 可能耗时较长，TiDB 会根据首次 Reorg 的执行时间设置超时阈值。如果 `ANALYZE` 超时，`ADD INDEX` 会停止同步等待 `ANALYZE` 完成，直接进入后续流程，使索引更早对用户可见。这意味着索引统计信息会在 `ANALYZE` 异步完成后再更新。

例如：

```sql
CREATE TABLE t (a INT, b INT, c INT);
Query OK, 0 rows affected (0.011 sec)

INSERT INTO t VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE t ADD INDEX idx (a, b);
Query OK, 0 rows affected (0.049 sec)
```

```sql
EXPLAIN SELECT a FROM t WHERE a > 1;
```

```
+------------------------+---------+-----------+--------------------------+----------------------------------+
| id                     | estRows | task      | access object            | operator info                    |
+------------------------+---------+-----------+--------------------------+----------------------------------+
| IndexReader_7          | 4.00    | root      |                          | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 4.00    | cop[tikv] | table:t, index:idx(a, b) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+--------------------------+----------------------------------+
2 rows in set (0.002 sec)
```

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "t";
```

```
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | t          |                | a           |        0 | 2025-10-30 20:17:57 |              3 |          0 |          0.5 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | t          |                | idx         |        1 | 2025-10-30 20:17:57 |              3 |          0 |            0 |           0 | allLoaded   |             182 |              0 |            182 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
2 rows in set (0.013 sec)
```

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
| JOB_ID | DB_NAME | TABLE_NAME               | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                               |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
|    151 | test    | t                        | add index     | write reorganization |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | NULL                       | running | analyzing, txn-merge, max_node_count=3 |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
1 rows in set (0.001 sec)
```

从 `ADD INDEX` 示例可以看到，当 `tidb_stats_update_during_ddl` 为 `ON` 时，在执行 `ADD INDEX` DDL 语句后，后续的 `EXPLAIN` 输出显示索引 `idx` 的统计信息已被自动收集并加载到内存（可通过执行 `SHOW STATS_HISTOGRAMS` 验证）。因此，优化器可以立即利用这些统计信息进行范围扫描。如果索引创建或重组及 `ANALYZE` 耗时较长，你可以通过执行 `ADMIN SHOW DDL JOBS` 查看 DDL 任务状态。当输出的 `COMMENTS` 列包含 `analyzing` 时，表示该 DDL 任务正在收集统计信息。

## 重组已有索引的 DDL

当 `tidb_stats_update_during_ddl` 为 `ON` 时，执行 [**MODIFY COLUMN**](/sql-statements/sql-statement-modify-column.md) 或 [**CHANGE COLUMN**](/sql-statements/sql-statement-change-column.md) 等重组索引的操作，也会在 Reorg 阶段完成后执行一次嵌入式 `ANALYZE` 操作。其机制与 `ADD INDEX` 相同：

- 在索引对用户可见前开始收集统计信息。
- 如果 `ANALYZE` 超时，[**MODIFY COLUMN**](/sql-statements/sql-statement-modify-column.md) 和 [**CHANGE COLUMN**](/sql-statements/sql-statement-change-column.md) 会停止同步等待 `ANALYZE` 完成，直接进入后续流程，使索引更早对用户可见。这意味着索引统计信息会在 `ANALYZE` 异步完成后再更新。

例如：

```sql
CREATE TABLE s (a VARCHAR(10), INDEX idx (a));
Query OK, 0 rows affected (0.012 sec)

INSERT INTO s VALUES (1), (2), (3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE s MODIFY COLUMN a INT;
Query OK, 0 rows affected (0.056 sec)

EXPLAIN SELECT * FROM s WHERE a > 1;
```

```
+------------------------+---------+-----------+-----------------------+----------------------------------+
| id                     | estRows | task      | access object         | operator info                    |
+------------------------+---------+-----------+-----------------------+----------------------------------+
| IndexReader_7          | 2.00    | root      |                       | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 2.00    | cop[tikv] | table:s, index:idx(a) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+-----------------------+----------------------------------+
2 rows in set (0.005 sec)
```
  
```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "s";
```

```
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            2 |           1 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            1 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             155 |              0 |            155 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
4 rows in set (0.008 sec)
```

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
| JOB_ID | DB_NAME | TABLE_NAME       | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                    |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
|    153 | test    | s                | modify column | write reorganization |         2 |      148 |  12582912 | 2025-10-29 00:26:49.240000 | 2025-10-29 00:26:49.244000 | NULL                       | running | analyzing                   |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
1 rows in set (0.001 sec)
```

从 `MODIFY COLUMN` 示例可以看到，当 `tidb_stats_update_during_ddl` 为 `ON` 时，在执行 `MODIFY COLUMN` DDL 语句后，后续的 `EXPLAIN` 输出显示索引 `idx` 的统计信息已被自动收集并加载到内存（可通过执行 `SHOW STATS_HISTOGRAMS` 验证）。因此，优化器可以立即利用这些统计信息进行范围扫描。如果索引创建或重组及 `ANALYZE` 耗时较长，你可以通过执行 `ADMIN SHOW DDL JOBS` 查看 DDL 任务状态。当输出的 `COMMENTS` 列包含 `analyzing` 时，表示该 DDL 任务正在收集统计信息。