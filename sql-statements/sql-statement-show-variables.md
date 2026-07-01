---
title: SHOW [GLOBAL|SESSION] VARIABLES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [GLOBAL|SESSION] VARIABLES for the TiDB database.
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

The following example shows part of the TiDB-specific global variables. For detailed descriptions, refer to [System Variables](/system-variables.md).

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'tidb%';
+--------------------------------------+-------------+
| Variable_name                        | Value       |
+--------------------------------------+-------------+
| tidb_accelerate_user_creation_update | OFF         |
| tidb_adaptive_closest_read_threshold | 4096        |
| tidb_advancer_check_point_lag_limit  | 48h0m0s     |
| tidb_allow_batch_cop                 | 1           |
| tidb_allow_fallback_to_tikv          |             |
| tidb_allow_mpp                       | ON          |
| ...                                  | ...         |
| tidb_txn_commit_batch_size           | 16384       |
| tidb_txn_entry_size_limit            | 0           |
| tidb_txn_mode                        | pessimistic |
| tidb_use_plan_baselines              | ON          |
| tidb_wait_split_region_finish        | ON          |
| tidb_wait_split_region_timeout       | 300         |
| tidb_window_concurrency              | -1          |
+--------------------------------------+-------------+
338 rows in set

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