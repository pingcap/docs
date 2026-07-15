---
title: SHOW [GLOBAL|SESSION] VARIABLES | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [GLOBAL|SESSION] VARIABLES の使用法の概要。
---

# SHOW [GLOBAL|SESSION] VARIABLES {#show-global-session-variables}

この文は、スコープ`GLOBAL`または`SESSION`の変数のリストを表示します。スコープが指定されていない場合は、デフォルトのスコープ`SESSION`が適用されます。

## 概要 {#synopsis}

```ebnf+diagram
ShowVariablesStmt ::=
    "SHOW" ("GLOBAL" | "SESSION")? VARIABLES ShowLikeOrWhere?
    
ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

次の例は、`SHOW [GLOBAL|SESSION] VARIABLES` ステートメントを使用して、名前または値が特定のパターンに一致する変数を表示する方法を示しています。これらの変数の詳細については、[システム変数](/system-variables.md)を参照してください。

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

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW [GLOBAL|SESSION] VARIABLES`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [`SET [GLOBAL|SESSION]`](/sql-statements/sql-statement-set-variable.md)
