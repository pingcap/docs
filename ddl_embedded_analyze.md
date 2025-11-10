---
title: `ANALYZE` Embedded in DDL Statements
summary: This document describes the `ANALYZE` feature embedded in DDL statements for newly created or reorganized indexes, which ensures that statistics for new indexes are updated promptly.
---

# `ANALYZE` Embedded in DDL Statements<span class="version-mark">Introduced in v8.5.4 and v9.0.0</span>

This document describes the `ANALYZE` feature embedded in the following two types of DDL statements:

- DDL statements that create new indexes: [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- DDL statements that reorganize existing indexes: [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) and [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

When this feature is enabled, TiDB automatically runs an `ANALYZE` (statistics collection) operation before the new or reorganized index becomes visible to users. This prevents inaccurate optimizer estimates and potential plan changes caused by temporarily unavailable statistics after index creation or reorganization.

## Usage scenarios

In scenarios where DDL operations alternately add or modify indexes, existing stable queries might suffer from estimation bias because the new index lacks statistics, causing the optimizer to choose suboptimal plans. For more information, see [Issue #57948](https://github.com/pingcap/tidb/issues/57948).

For example:

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

In the preceding plan, because the newly created index has no statistics yet, TiDB can only rely on heuristic rules for path estimation. Unless the index access path requires no table lookup and has a significantly lower cost, the optimizer tends to choose the more stable existing path. In the preceding example, it chooses a full table scan. However, from the data distribution perspective, `t.a > 4` actually returns 0 rows. If the new index `idx_a` were used, the query could quickly locate relevant rows and avoid the full table scan. In this example, because statistics are not promptly collected after the DDL creates the index, the generated plan is not optimal, but the optimizer continues to use the original plan so query performance does not sharply regress. However, according to [Issue #57948](https://github.com/pingcap/tidb/issues/57948), in some cases heuristics might cause an unreasonable comparison between old and new indexes, pruning the index that the original plan relies on and ultimately falling back to a full table scan.

Starting from v8.5.0, TiDB has improved heuristic comparisons between indexes and behaviors when statistics are missing. Still, in some complex scenarios, embedding `ANALYZE` in DDL is the best way to prevent plan changes. You can control whether to run embedded `ANALYZE` during index creation or reorganization with the system variable [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl-new-in-v854-and-v900). The default value is `OFF`.

## `ADD INDEX` DDL

When `tidb_stats_update_during_ddl` is `ON`, executing [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) automatically runs an embedded `ANALYZE` operation after the Reorg phase finishes. This `ANALYZE` operation collects statistics for the newly created index before the index becomes visible to users, and then `ADD INDEX` proceeds with its remaining phases.

Considering that `ANALYZE` can take time, TiDB sets a timeout threshold based on the execution time of the first Reorg. If `ANALYZE` times out, `ADD INDEX` stops waiting synchronously for `ANALYZE` to finish and continues the subsequent process, making the index visible earlier to users. This means the index statistics will be updated after `ANALYZE` completes asynchronously.

For example:

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

From the `ADD INDEX` example, when `tidb_stats_update_during_ddl` is `ON`, you can see that after the execution of the `ADD INDEX` DDL statement, the subsequent `EXPLAIN` output shows that statistics for the index `idx` have been automatically collected and loaded into memory (you can verify it by executing `SHOW STATS_HISTOGRAMS`). As a result, the optimizer can immediately use these statistics for range scans. If index creation or reorganization and `ANALYZE` take a long time, you can check the DDL job status by executing `ADMIN SHOW DDL JOBS`. When the `COMMENTS` column in the output contains `analyzing`, it means that the DDL job is collecting statistics.

## DDL for reorganizing existing indexes

When `tidb_stats_update_during_ddl` is `ON`, executing [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) or [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) that reorganizes an index will also run an embedded `ANALYZE` operation after the Reorg phase completes. The mechanism is the same as for `ADD INDEX`:

- Start collecting statistics before the index becomes visible.
- If `ANALYZE` times out, [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) and [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) stops waiting synchronously for `ANALYZE` to finish and continues the subsequent process, making the index visible earlier to users. This means that the index statistics will be updated when `ANALYZE` finishes asynchronously.

For example:

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

From the `MODIFY COLUMN` example, when `tidb_stats_update_during_ddl` is `ON`, you can see that after the execution of the `MODIFY COLUMN` DDL statement, the subsequent `EXPLAIN` output shows that statistics for the index `idx` have been automatically collected and loaded into memory (you can verify it by executing `SHOW STATS_HISTOGRAMS`). As a result, the optimizer can immediately use these statistics for range scans. If index creation or reorganization and `ANALYZE` take a long time, you can check the DDL job status by executing `ADMIN SHOW DDL JOBS`. When the `COMMENTS` column in the output contains `analyzing`, it means that the DDL job is collecting statistics.
