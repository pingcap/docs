---
title: ADD INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of ADD INDEX for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-add-index/','/docs/dev/reference/sql/statements/add-index/']
---

# ADD INDEX

The `ALTER TABLE.. ADD INDEX` statement adds an index to an existing table. This operation is online in TiDB, which means that neither reads or writes to the table are blocked by adding an index.

> **Tip:**
>
> The [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md) can be used to speed up the operation of this statement.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> For [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters with 4 vCPU, it is recommended to manually disable [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) to prevent resource limitations from affecting cluster stability during index creation. Disabling this setting allows indexes to be created using transactions, which reduces the overall impact on the cluster.

</CustomContent>

<CustomContent platform="tidb">

> **Warning:**
>
> - **DO NOT** upgrade a TiDB cluster when a DDL statement is being executed in the cluster (usually for the time-consuming DDL statements such as `ADD INDEX` and the column type changes).
> - Before the upgrade, it is recommended to use the [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) command to check whether the TiDB cluster has an ongoing DDL job. If the cluster has a DDL job, to upgrade the cluster, wait until the DDL execution is finished or use the [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) command to cancel the DDL job before you upgrade the cluster.
> - In addition, during the cluster upgrade, **DO NOT** execute any DDL statement. Otherwise, the issue of undefined behavior might occur.
>
> When you upgrade TiDB from v7.1.0 to a later version, you can ignore the preceding limitations. For details, see [the limitations of TiDB smooth upgrade](/smooth-upgrade-tidb.md).

</CustomContent>

## Synopsis

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | 'USING' IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'
           | 'GLOBAL'
           | 'LOCAL'
           | 'PRE_SPLIT_REGIONS' '='? 'AUTO'
           | 'WHERE' Expression

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
```

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## Automatic Region pre-splitting

<span class="version-mark">New in v9.0.0</span>

When adding an index to a large existing table, you can specify `PRE_SPLIT_REGIONS AUTO` to let TiDB derive Region split boundaries from existing column statistics. This can reduce initial write hotspots without requiring you to choose split boundaries manually.

> **Note:**
>
> Automatic Region pre-splitting is an experimental feature.

### Usage

The `PRE_SPLIT_REGIONS [=] AUTO` option is supported by `ALTER TABLE ... ADD INDEX`, `ALTER TABLE ... ADD PRIMARY KEY`, and [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md). The equals sign (`=`) is optional. For primary keys, the existing restriction that only `NONCLUSTERED` primary keys can be added still applies.

For an existing non-partitioned table `t` with at least 1,000,000 rows, collect Version 2 statistics on the leading index column before adding the index:

```sql
SET SESSION tidb_analyze_version = 2;
ANALYZE TABLE t COLUMNS a;
ALTER TABLE t ADD INDEX idx_a (a) PRE_SPLIT_REGIONS AUTO;
```

`AUTO` applies only to the index operation that specifies it. For example, in the following statement, only `idx_a` enables automatic pre-splitting:

```sql
ALTER TABLE t
    ADD INDEX idx_a (a) PRE_SPLIT_REGIONS AUTO,
    ADD INDEX idx_b (b);
```

Automatic pre-splitting is disabled for indexes that omit this option. Existing manual `PRE_SPLIT_REGIONS` options remain available. If both a manual option and `AUTO` are specified for the same index, the manual option takes precedence regardless of their order.

### Requirements and limitations

TiDB skips automatic pre-splitting for an index if any of the following conditions apply:

- The table is partitioned, or the index is a partial index.
- The leading index column is a string column with an index prefix, such as `INDEX idx (a(10))`.
- The table has fewer than 1,000,000 rows according to statistics, or its [statistics health score](/statistics.md#health-state-of-tables) is unavailable or below 80. You can use [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) to check the health score.
- The leading index column does not have usable [Version 2 statistics](/statistics.md#versions-of-statistics). Missing, pseudo, or outdated statistics cannot provide reliable split boundaries. If needed, run `ANALYZE TABLE ... COLUMNS ...` to refresh the statistics before adding the index.
- The leading column distribution does not provide a usable split boundary.

Automatic pre-splitting uses only the leading column of a composite index. It does not use later columns to further split rows that share the same leading-column value. Columnar, vector, and full-text indexes are outside the scope of this option. `AUTO` cannot be used as a `CREATE TABLE` table option.

### Split behavior

TiDB combines NULL counts, Top-N value counts, and histogram bucket counts from the leading column statistics into an ordered distribution. It selects split boundaries at fixed 2% cumulative intervals, producing at most 49 distribution-derived boundaries per index. Repeated values contribute at most one boundary, so the actual number can be smaller. TiDB also adds index keyspace boundaries as needed.

The target Regions depend on the index backfilling mode, following the behavior of manual `PRE_SPLIT_REGIONS`:

- Transactional backfilling splits normal index Regions.
- Ingest and transactional-merge backfilling split temporary index Regions used by concurrent DML. This step does not additionally split normal index Regions.

Each index that specifies `AUTO` is split and scattered separately, even when multiple indexes share the same leading column. With fast reorganization, after garbage collection removes the temporary index data, empty Regions can remain until PD's [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval) has elapsed (one hour by default). Actual merging also depends on PD's normal Region merge conditions.

All `AUTO` indexes in a DDL job share a time budget of 30 seconds plus [`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout), which defaults to 300 seconds. This budget starts before the first index is processed. Time spent on manual pre-splitting in the same job also consumes this budget.

Automatic pre-splitting is best-effort. If loading or decoding any part of the complete leading-column distribution fails, TiDB skips `AUTO` for that index instead of using partial statistics. Planning, split, scatter, or timeout failures do not cancel index creation. DDL pause and cancellation requests still take effect. Successful index creation does not guarantee that any Regions were pre-split.

To check the outcome, inspect the TiDB server log for `skip auto presplit index region`, `auto presplit index region failed, continue add-index`, or `split table index region finished`. The log entries include the table and index names and, depending on the outcome, a skip reason, an error, or split and scatter counts. These decisions and outcomes are not recorded in [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md).

## Partial indexes <span class="version-mark">New in v8.5.7 and v9.0.0</span>

A partial index is an index built on a subset of rows in a table. When adding a partial index, you can specify a conditional expression, also known as a predicate, to define that subset of rows. The index contains entries only for the rows that satisfy the predicate.

### Usage scenarios

In the following scenarios, using partial indexes helps improve query performance or reduce index maintenance overhead:

- **Selective filtering**: when you frequently query a small subset of rows based on specific conditions, you can use partial indexes. For queries that satisfy the partial index predicate, TiDB can use the partial index to avoid scanning irrelevant rows and reduce the storage space occupied by the index.
- **Conditional uniqueness**: when you only need to enforce a uniqueness constraint on rows that satisfy specific conditions, you can use a unique partial index to avoid applying the uniqueness constraint to the entire table.
- **Reduced DML overhead**: when many `INSERT`, `UPDATE`, or `DELETE` operations affect rows that do not need to be indexed, you can use partial indexes. Compared with maintaining a full index, maintaining a partial index can reduce index maintenance overhead.

### Add partial indexes

You can add a partial index by appending a `WHERE` clause to the index definition. For example:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, c3 TEXT);
ALTER TABLE t1 ADD INDEX idx1 (c1) WHERE c2 > 10;
```

You can also add a unique partial index:

```sql
ALTER TABLE t1 ADD UNIQUE INDEX idx2 (c1, c2) WHERE c3 = 'abc';
```

### Usage examples

The following examples demonstrate how to use partial indexes effectively.

Create a table with user data:

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    status VARCHAR(20),
    created_at DATETIME,
    score INT
);
```

Add partial indexes for common query patterns:

```sql
ALTER TABLE users ADD INDEX idx_active_users (name) WHERE status = 'active';
ALTER TABLE users ADD INDEX idx_high_score_users (created_at) WHERE score > 1000;
ALTER TABLE users ADD INDEX idx_pending_status (status) WHERE status = 'pending';
```

Then the following queries can use the partial index:

```sql
mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' AND name = 'John';
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                             | operator info                                         |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| IndexLookUp_9                 | 1.00    | root      |                                           |                                                       |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:users, index:idx_active_users(name) | range:["John","John"], keep order:false, stats:pseudo |
| └─Selection_8(Probe)          | 1.00    | cop[tikv] |                                           | eq(test.users.status, "active")                       |
|   └─TableRowIDScan_7          | 10.00   | cop[tikv] | table:users                               | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' ORDER BY name;
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| id                            | estRows  | task      | access object                             | operator info                   |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| IndexLookUp_18                | 10.00    | root      |                                           |                                 |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_active_users(name) | keep order:true, stats:pseudo   |
| └─Selection_17(Probe)         | 10.00    | cop[tikv] |                                           | eq(test.users.status, "active") |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                               | keep order:false, stats:pseudo  |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE score > 10000 ORDER BY created_at;
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| id                            | estRows  | task      | access object                                       | operator info                  |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| IndexLookUp_18                | 3333.33  | root      |                                                     |                                |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_high_score_users(created_at) | keep order:true, stats:pseudo  |
| └─Selection_17(Probe)         | 3333.33  | cop[tikv] |                                                     | gt(test.users.score, 10000)     |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                                         | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'pending';
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| id                            | estRows | task      | access object                                 | operator info                                               |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                                               |                                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:users, index:idx_pending_status(status) | range:["pending","pending"], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:users                                   | keep order:false, stats:pseudo                              |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

If the predicate for a query does not satisfy the conditions defined by the partial index, TiDB does not select the partial index, even with a hint. For example, the following statement cannot use the partial index `idx_high_score_users`, because the query predicate `score > 100` does not satisfy the partial index definition `score > 1000`:

```sql
mysql> EXPLAIN SELECT * FROM users USE INDEX(idx_high_score_users) WHERE score > 100 ORDER BY created_at;
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Sort_5                    | 3333.33  | root      |               | test.users.created_at          |
| └─TableReader_10          | 3333.33  | root      |               | data:Selection_9               |
|   └─Selection_9           | 3333.33  | cop[tikv] |               | gt(test.users.score, 100)      |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
```

### Limitations

- The `WHERE` clause in partial indexes supports basic comparison operators (`=`, `!=`, `<`, `<=`, `>`, `>=`), `IS NULL`, `IS NOT NULL`, and `IN` predicates with constant values.
- The columns and constant values in the predicate must be of the same data type.
- The predicate can only reference columns from the same table.
- Partial indexes cannot be created on expression indexes.

## MySQL compatibility

* TiDB accepts index types such as `HASH`, `BTREE` and `RTREE` in syntax for compatibility with MySQL, but ignores them.
* `SPATIAL` indexes are not supported.
* TiDB Self-Managed and TiDB Cloud Dedicated support parsing the `FULLTEXT` syntax but do not support using the `FULLTEXT` indexes.

    >**Note:**
    >
    > Currently, only {{{ .starter }}} and {{{ .essential }}} instances in certain AWS regions support [`FULLTEXT` syntax and indexes](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql).

* Descending indexes are not supported (similar to MySQL 5.7).
* Adding the primary key of the `CLUSTERED` type to a table is not supported. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
* Setting a `PRIMARY KEY` or `UNIQUE INDEX` as a [global index](/global-indexes.md) with the `GLOBAL` index option is a TiDB extension for [partitioned tables](/partitioned-table.md) and is not compatible with MySQL.
* `PRE_SPLIT_REGIONS AUTO` is a TiDB extension and is not compatible with MySQL.

## See also

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)
