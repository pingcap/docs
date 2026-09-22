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
