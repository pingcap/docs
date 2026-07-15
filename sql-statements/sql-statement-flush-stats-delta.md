---
title: FLUSH STATS_DELTA
summary: An overview of the usage of FLUSH STATS_DELTA for the TiDB database.
---

# FLUSH STATS_DELTA <span class="version-mark">New in v8.5.7 and v9.0.0</span>

`FLUSH STATS_DELTA` persists the pending statistics delta buffered in TiDB memory to the [`mysql.stats_meta`](/mysql-schema/mysql-schema.md#statistics-system-tables) system table immediately.

When you change data using DML statements (such as `INSERT`, `UPDATE`, and `DELETE`), TiDB records changes to the total row count and modified row count of each affected table, buffers these changes (called the statistics delta) in the memory of the TiDB node that executes the statements, and persists them to the `mysql.stats_meta` system table every 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease) (60 seconds by default). For more information, see [Automatic update](/statistics.md#automatic-update).

Because the [health state of tables](/sql-statements/sql-statement-show-stats-healthy.md), the output of [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md), and the scheduling of automatic statistics collection depend on the persisted values, `FLUSH STATS_DELTA` is useful when you need the persisted statistics metadata to reflect recent data changes immediately, such as in testing scenarios that verify optimizer behavior. You do not need to execute this statement before [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md), because TiDB automatically flushes the pending statistics delta of a table before collecting statistics on it.

## Synopsis

```ebnf+diagram
FlushStatsDeltaStmt ::=
    'FLUSH' 'STATS_DELTA' FlushTargetList ClusterOption?

FlushTargetList ::=
    FlushTarget (',' FlushTarget)*

FlushTarget ::=
    TableName
  | SchemaWildcard
  | GlobalWildcard

TableName ::=
    Identifier ('.' Identifier)?

SchemaWildcard ::=
    Identifier '.' '*'

GlobalWildcard ::=
    '*' '.' '*'

ClusterOption ::=
    'CLUSTER'
```

## Options

- **Targets (`FlushTargetList`)**: specifies which tables to flush. You must specify at least one target.
    - `table_name`: flushes the statistics delta of a table in the current database. If you do not select a database, TiDB returns the `No database selected` error.
    - `db_name.table_name`: flushes the statistics delta of a table in the specified database.
    - `db_name.*`: flushes the statistics delta of every table in the specified database.
    - `*.*`: flushes the statistics delta of every table.
- **`CLUSTER`**: broadcasts the statement to every TiDB instance in the cluster. Each TiDB instance buffers the statistics delta of the DML statements that it executes. Without this option, TiDB persists only the delta buffered on the instance you are connected to.

Note the following behavior:

- TiDB deduplicates overlapping targets: `*.*` covers all other targets, and `db_name.*` covers tables in that database.
- For a partitioned table, TiDB persists the statistics delta of the table and all its partitions.
- If a specified database or table does not exist, TiDB returns a warning and skips that target.

## Examples

Persist the statistics delta of a single table immediately after data changes:

```sql
USE test;
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
FLUSH STATS_DELTA t;
```

```
Query OK, 0 rows affected (0.01 sec)
```

TiDB has now persisted the row count changes of the table to the `mysql.stats_meta` system table. You can view them using `SHOW STATS_META`. Note that `SHOW STATS_META` reads statistics from the memory of the TiDB instance you are connected to. Because this instance loads the persisted values within [`stats-lease`](/tidb-configuration-file.md#stats-lease) (`3s` by default), the flushed values might appear in the output after a short delay:

```sql
SHOW STATS_META WHERE table_name = 't';
```

```
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| test    | t          |                | 2026-07-13 15:30:00 |            3 |         3 | NULL              |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
1 row in set (0.01 sec)
```

Persist the statistics delta of a table in the current database and every table in the `sales` database:

```sql
FLUSH STATS_DELTA t, sales.*;
```

Persist the statistics delta of all tables buffered on every TiDB instance in the cluster:

```sql
FLUSH STATS_DELTA *.* CLUSTER;
```

## Privileges

To execute `FLUSH STATS_DELTA`, you must have the `SELECT` privilege on the target objects: the target table for `table_name` or `db_name.table_name` targets, the target database for `db_name.*` targets, and the global `SELECT` privilege for `*.*` targets. Unlike other `FLUSH` statements, `FLUSH STATS_DELTA` does not require the `RELOAD` privilege.

## MySQL compatibility

`FLUSH STATS_DELTA` is a TiDB extension to MySQL syntax.

## See also

- [Statistics](/statistics.md)
- [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`REFRESH STATS`](/sql-statements/sql-statement-refresh-stats.md)
