---
title: SHOW [GLOBAL|SESSION] VARIABLES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [GLOBAL|SESSION] VARIABLES for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-variables/','/docs/dev/reference/sql/statements/show-variables/']
---

# SHOW [GLOBAL|SESSION] VARIABLES

This statement shows a list of variables for the scope of either `GLOBAL` or `SESSION`. If no scope is specified, the default scope of `SESSION` will apply.

## Synopsis

```ebnf+diagram
ShowVariablesStmt ::=
    "SHOW" ("GLOBAL" | "SESSION")? VARIABLES ShowLikeOrWhere?
    
ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

The following example demonstrates how to use the `SHOW [GLOBAL|SESSION] VARIABLES` statement to show variables whose names or values match a specific pattern. For detailed descriptions of these variables, see [System Variables](/system-variables.md).

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'tidb_stmt_summary%';
+-------------------------------------+---------------------+
| Variable_name                       | Value               |
+-------------------------------------+---------------------+
| tidb_stmt_summary_enable_persistent | OFF                 |
| tidb_stmt_summary_file_max_backups  | 0                   |
| tidb_stmt_summary_file_max_days     | 3                   |
| tidb_stmt_summary_file_max_size     | 64                  |
| tidb_stmt_summary_filename          | tidb-statements.log |
| tidb_stmt_summary_history_size      | 24                  |
| tidb_stmt_summary_internal_query    | OFF                 |
| tidb_stmt_summary_max_sql_length    | 4096                |
| tidb_stmt_summary_max_stmt_count    | 3000                |
| tidb_stmt_summary_refresh_interval  | 1800                |
+-------------------------------------+---------------------+
10 rows in set (0.001 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'time_zone%';
+---------------+--------+
| Variable_name | Value  |
+---------------+--------+
| time_zone     | SYSTEM |
+---------------+--------+
1 row in set (0.00 sec)

mysql> SHOW VARIABLES WHERE Variable_name="tidb_window_concurrency";
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| tidb_window_concurrency | -1    |
+-------------------------+-------+
1 row in set (0.00 sec)

mysql> SHOW VARIABLES WHERE Value=300;
+--------------------------------+-------+
| Variable_name                  | Value |
+--------------------------------+-------+
| ddl_slow_threshold             | 300   |
| delayed_insert_timeout         | 300   |
| innodb_purge_batch_size        | 300   |
| key_cache_age_threshold        | 300   |
| slave_checkpoint_period        | 300   |
| tidb_slow_log_threshold        | 300   |
| tidb_wait_split_region_timeout | 300   |
+--------------------------------+-------+
7 rows in set (0.00 sec)
```

## MySQL compatibility

The `SHOW [GLOBAL|SESSION] VARIABLES` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [`SET [GLOBAL|SESSION]`](/sql-statements/sql-statement-set-variable.md)
