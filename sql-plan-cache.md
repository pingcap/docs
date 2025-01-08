---
title: SQL Plan Cache
summary: Learn about SQL Plan Cache in TiDB.
aliases: ['/tidb/dev/sql-plan-cache']
---

# Introduction

TiDB supports using Plan Cache to cache execution plans in memory and reuse them for the same queries, which avoids repeatedly compiling plans and brings some performance improvements.

TiDB supports both Session Plan Cache and Instance Plan Cache. Session Plan Cache maintains cache for each session, plans can't be shared across different sessions, while Instance Plan Cache maintains one single cache in the instance for all sessions.

We recommend you to use Plan Cache with `Prepare/Execute` statements or `COM_STMT_PREPARE/EXECUTE` protocol, but for normal Non-Prepared statements, TiDB also support Non-Prepared Plan Cache.

# Usage

## Use Session Plan Cache

To enable Session Plan Cache, you need to set `tidb_enable_prepared_plan_cache` to true and set `tidb_enable_instance_plan_cache` to false.

And you can use `@@last_plan_from_cach` to check whether the last statement hits the Plan Cache:

```sql
myaql> set global tidb_enable_prepared_plan_cache=1;
Query OK, 0 rows affected (0.00 sec)

myaql> set global tidb_enable_instance_plan_cache=0;
Query OK, 0 rows affected (0.00 sec)

mysql> prepare st from "select a from t";
Query OK, 0 rows affected (0.00 sec)

mysql> execute st;
Empty set (0.00 sec)

mysql> execute st;
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
```

## Use Instance Plan Cache

> **Warning:**
>
> Instance Plan Cache is an experimental feature.

TiDB starts supporting Instance Plan Cache after v8.4.

To enable Instance Plan Cache, you need to set `tidb_enable_prepared_plan_cache` to true and set `tidb_enable_instance_plan_cache` to true.

Cached plans can shared across different sessions when enabling this feature:

```sql
-- execute below SQLs in session-1
mysql> set global tidb_enable_instance_plan_cache=1;
Query OK, 0 rows affected (0.01 sec)

mysql> prepare st from "select a from t";
Query OK, 0 rows affected (0.01 sec)

mysql> execute st;
Empty set (0.00 sec)

-- execute below SQLs in session-2
mysql> prepare st from "select a from t";
Query OK, 0 rows affected (0.00 sec)

mysql> execute st;
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
```

## Comparison of Session and Instance Plan Cache
Session Plan Cache means each session has its own Plan Cache, for example, if there are 10 sessions executing the same query `select a from t`, then there are 10 same plans cached in memory. In the opposite, if you are using Instance Plan Cache, then there is only 1 plan cached in memory for this query.

Session Plan Cache has a slightly better performance (around 1~3%), but incurs more memory usage. Below is a test based on Sysbench-oltp_read_only with 120 concurrency, where Session Plan Cache costs more than 1GB memory usage while Instance Plan Cache only costs 58MB.

![comparison](/media/plancache-session-instance-comparison.PNG)

## Non-Prepared Plan Cache

Set `tidb_enable_non_prepared_plan_cache` to true to enable this feature:

```sql
mysql> SET tidb_enable_non_prepared_plan_cache = ON;
Query OK, 0 rows affected (0.00 sec)

mysql> select * from t where a<10 and b=1;
Empty set (0.01 sec)

mysql> select * from t where a<20 and b=20;
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
```

Non-Prepared Plan Cache needs to parameterizes the query (for example, parameterize `SELECT * FROM t WHERE b < 10 AND a = 1` to `SELECT * FROM t WHERE b < ? and a = ?`) and use it to search the plan cache, which might incur additional overhead, so it's not suitable for all situations. Please decide whether to use this feature according to your workload.

# Management and diagnosis of Plan Cache

## Related Metrics

In [the Grafana dashboard](/grafana-tidb-dashboard.md) on the TiDB page in the Executor section, there are the Queries Using Plan Cache OPS and Plan Cache Miss OPS graphs, and they can help you to know the number quereis can and can't hit Plan Cache:

![`sql_plan_cache`](/media/performance/sql_plan_cache.png)

To view the total memory consumption by the cached execution plans of all sessions in each TiDB instance, you can use [**Plan Cache Memory Usage** monitoring panel](/grafana-tidb-dashboard.md) in Grafana.

To view the total number of execution plans cached in each TiDB instance, you can use [**Plan Cache Plan Num** panel](/grafana-tidb-dashboard.md) in Grafana.

The following is an example of the Plan Cache Memory Usage and Plan Cache Plan Num panels in Grafana:

![grafana_panels](/media/planCache-memoryUsage-planNum-panels.png)

## Memory Usage Management

### Session Plan Cache

Starting from v7.1.0, you can control the maximum number of plans that can be cached in each session by configuring the system variable [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710). For different environments, the recommended value is as follows and you can adjust it according to the monitoring panels:

- When the memory threshold of the TiDB server instance is <= 64 GiB, set `tidb_session_plan_cache_size` to 50.
- When the memory threshold of the TiDB server instance is > 64 GiB, set `tidb_session_plan_cache_size` to 100.

Starting from v7.1.0, you can control the maximum size of a plan that can be cached using the system variable [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710). The default value is 2 MB. If the size of a plan exceeds this value, the plan will not be cached.

When the unused memory of the TiDB server is less than a certain threshold, the memory protection mechanism of plan cache is triggered, through which some cached plans will be evicted.

You can control the threshold by configuring the system variable `tidb_prepared_plan_cache_memory_guard_ratio`. The threshold is 0.1 by default, which means when the unused memory of the TiDB server is less than 10% of the total memory (90% of the memory is used), the memory protection mechanism is triggered.

### Instance Plan Cache

Use `tidb_instance_plan_cache_max_size` to set the total memory limitation of Instance Plan Cache. For example, `set global tidb_instance_plan_cache_max_size=200MiB` .

TiDB purges the Instance Plan Cache periodically, and you can set `tidb_instance_plan_cache_reserved_percentage` to control the amount of memory to purge each time. For example, the default percentage is `0.1`, and if the max size is `200MiB`, then TiDB purges `200*0.1=20MiB` memory each time.

## Why the query can't hit Plan Cache

Optimzier outputs the reason why the current query can't hit Plan Cache as warnings, so you can use `SHOW WARNINGS` statement to check the reason:

```sql
mysql> PREPARE st FROM 'SELECT * FROM t WHERE a > (SELECT MAX(a) FROM t)';  -- The query contains a subquery and cannot be cached.
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;  -- Checks the reason why the query plan cannot be cached.
+---------+------+-----------------------------------------------+
| Level   | Code | Message                                       |
+---------+------+-----------------------------------------------+
| Warning | 1105 | skip plan-cache: sub-queries are un-cacheable |
+---------+------+-----------------------------------------------+
1 row in set (0.00 sec)

mysql> prepare st from 'select * from t where a<?';
Query OK, 0 rows affected (0.00 sec)

mysql> set @a='1';
Query OK, 0 rows affected (0.00 sec)

mysql> execute st using @a;  -- The optimization converts a non-INT type to an INT type, and the execution plan might change with the change of the parameter, so TiDB does not cache the plan.
Empty set, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------+
| Level   | Code | Message                                      |
+---------+------+----------------------------------------------+
| Warning | 1105 | skip plan-cache: '1' may be converted to INT |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)
```

## Which queries can't hit Plan Cache in your workload

The `Statements Summary` table contains two fields, `plan_cache_unqualified` and `plan_cache_unqualified_last_reason`, which respectively indicate the number of times and the reason why the corresponding query is unable to use the plan cache. 

You can use these two fields for diagnostic purposes:

```sql
mysql> SELECT digest_text, plan_cache_unqualified, plan_cache_unqualified_last_reason 
        FROM information_schema.statements_summary 
        WHERE plan_cache_unqualified > 0 ORDER BY plan_cache_unqualified DESC
        LIMIT 10;
+---------------------------------+------------------------+----------------------------------------+
| digest_text                     | plan_cache_unqualified | plan_cache_unqualified_last_reason     |
+---------------------------------+------------------------+----------------------------------------+
| select * from `t` where `a` < ? |                     10 | '1' may be converted to INT            |
| select * from `t` order by ?    |                      4 | query has 'order by ?' is un-cacheable |
| select database ( ) from `t`    |                      2 | query has 'database()' is un-cacheable |
...
+---------------------------------+------------------------+----------------------------------------+
```

## Cached Plans in Instance Plan Cache

For Instance Plan Cache, TiDB provides 2 system views (after v8.5) `information_schema.tidb_plan_cache` and `information_schema.cluster_tidb_plan_cache` to see the internal information of the Instance Plan Cache of the current instance and the whole cluster: 

```sql
mysql> select *, tidb_decode_binary_plan(binary_plan) from information_schema.tidb_plan_cache\G;
*************************** 1. row ***************************
                          SQL_DIGEST: 3689d7f367e2fdaf53c962c378efdf47799143b9af12f47e13ec247332269eac
                            SQL_TEXT: select a from t where a<?
                           STMT_TYPE: Select
                          PARSE_USER: root
                         PLAN_DIGEST: 6285ba7cabe7b19459668d62ec201ecbea63ac5f23e5b9166f02fbb86cdf4807
                         BINARY_PLAN: iQKYCoYCCg1UYWJsZVJlYWRlcl83ErYBCgtTZWxlY3Rpb25fNhJqCg9UASFMRnVsbFNjYW5fNSEAAAAAiKFSQSkBCeAAiMNAOAJAAkoLCgkKBHRlc3QSAXRSHmtlZXAgb3JkZXI6ZmFsc2UsIHN0YXRzOnBzZXVkb3D///8JAgQBeAkIDP///wEFWSzWiFRBKauqqqqq9qkFWRBSD2x0KAFYHC50LmEsIDEpWj0AGE8b6LShwhYdPSQBQAFSEGRhdGE6HdFWPgA=
                             BINDING: 
                             OPT_ENV: f20c20a72b2a33c5c44e805dbea0fa97028e6f047320928cf367f74c8c94737b
                        PARSE_VALUES: 1
                            MEM_SIZE: 13322
                          EXECUTIONS: 1
                      PROCESSED_KEYS: 0
                          TOTAL_KEYS: 0
                         SUM_LATENCY: 5919417
                           LOAD_TIME: 2024-12-05 15:41:43
                    LAST_ACTIVE_TIME: 2024-12-05 15:41:43
tidb_decode_binary_plan(binary_plan): 
| id                  | estRows  | estCost    | task      | access object | operator info                   |
| TableReader_7       | 3323.33  | 372904.43  | root      |               | data:Selection_6                |
| └─Selection_6       | 3323.33  | 5383000.00 | cop[tikv] |               | lt(test.t.a, 1)                 |
|   └─TableFullScan_5 | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo  |

*************************** 2. row ***************************
                          SQL_DIGEST: e46ac1d144fbf88c80d4eb9eeb43e8c57d92ed6cb7a6afbbe37a3f7651fa9446
                            SQL_TEXT: select a from t where a=? and b=?
                           STMT_TYPE: Select
                          PARSE_USER: root
                         PLAN_DIGEST: 88a275584ffbf1f6ae20629c677efecc8dc2bb3ec02f8a5859323d7755a4ff22
                         BINARY_PLAN: 5AKwCuECCg5UYWJsZVJlYWRlcl8xMRKPAgoMUHJvamVjdGlvbl81EsgBCgxTZWxlCRAUMTASagoPBTRMRnVsbFNjYW5fOSEAAAAAiKFSQSkBCeAAiMNAOAJAAkoLCgkKBHRlc3QSAXRSHmtlZXAgb3JkZXI6ZmFsc2UsIHN0YXRzOnBzZXVkb3D///8JAgQBeAkIDP///wEFWTAkcFZBKXsUrkfheoQ/AVkQUiBlcSgBWCAudC5hLCAxKSwdEQBiARFaTgAM6lkQAEZOAAAIEUtaNgAYhEEHaxXvFx2EJAFAAVIRZGF0YTouKgFWPwA=
                             BINDING: 
                             OPT_ENV: 88676ae6596aa2968e2ddd45ec0756ca71e7ccc3f3d16f6f3e4db4737335af2c
                        PARSE_VALUES: (1, 1)
                            MEM_SIZE: 19630
                          EXECUTIONS: 7
                      PROCESSED_KEYS: 0
                          TOTAL_KEYS: 0
                         SUM_LATENCY: 9134791
                           LOAD_TIME: 2024-12-05 15:41:56
                    LAST_ACTIVE_TIME: 2024-12-05 15:42:02
tidb_decode_binary_plan(binary_plan): 
| id                    | estRows  | estCost    | task      | access object | operator info                     |
| TableReader_11        | 0.01     | 392133.35  | root      |               | data:Projection_5                 |
| └─Projection_5        | 0.01     | 5882000.00 | cop[tikv] |               | test.t.a                          |
|   └─Selection_10      | 0.01     | 5882000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1)  |
|     └─TableFullScan_9 | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo    |
```

You can even add predicates to filter cached plans you want:

```sql
select * from information_schema.tidb_plan_cache where sql_digest=?;
select * from information_schema.tidb_plan_cache where sql_text like ?;
select * from information_schema.tidb_plan_cache where executions > 100;
```

# When to Recompile

Sometimes the optimizer has to recompile a cached plan due to environment changes, for example, if the user changes the table schema, the optimizer has to recompile related queries:

```sql
create table t (a int, b int, key(a));
prepare st from "select a from t where a=?";
set @a=1;
execute st using @a;
execute st using @a;
select @@last_plan_from_cache;                  -- return 1 since it can hit the last plan

alter table t drop index a;                     -- drop an index on this table
execute st using @a;
select @@last_plan_from_cache;                  -- return 0 since the DDL change triggers plan recompile
```

Below list all cases that the optimizer has to recompile the plan:

- The current DB name, user name, timezone, charset, collation are changed.
- Values of these variables or config are changed: `tidb_restricted_read_only`, `sql_mode`, `tidb_super_read_only`, `foreign_key_checks`, `tidb_enable_shared_lock_promotion`, `pessimistic-auto-commit`.
- Table schema is changed.
- Table statistics is changed and `tidb_plan_cache_invalidation_on_fresh_stats` is true.
- Numbers in Limit-Clause like `limit ?` is changed and `tidb_enable_plan_cache_for_param_limit` is true.
- Whether this query is in a transaction or not.
- A new SQL binding is created for this SQL.

# Limitations

## Plan Cache

In the current version of TiDB, if the statement meets any of the following conditions, the query or the plan is not cached:

- The query contains SQL statements other than `SELECT`, `UPDATE`, `INSERT`, `DELETE`, `Union`, `Intersect`, and `Except`.
- The query accesses temporary tables, or a table that contains generated columns, or uses static mode (that is, [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) is set to `static`) to access partitioning tables.
- The query contains non-correlated sub-queries, such as `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`.
- The query contains correlated sub-queries with `PhysicalApply` operators in the execution plan, such as `SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`.
- The query contains the `ignore_plan_cache` or `set_var` hint, such as `SELECT /*+ ignore_plan_cache() */ * FROM t` or `SELECT /*+ set_var(max_execution_time=1) */ * FROM t`.
- The query contains variables other than `?` (including system variables or user-defined variables), such as `select * from t where a>? and b>@x`.
- The query contains the functions that cannot be cached: `database()`, `current_user`, `current_role`, `user`, `connection_id`, `last_insert_id`, `row_count`, `version`, and `like`.
- The query uses a variable as the `LIMIT` parameter (such as `LIMIT ?` and `LIMIT 10, ?`) and the variable value is greater than 10000.
- The query contains `?` after `Order By`, such as `Order By ?`. Such queries sort data based on the column specified by `?`. If the queries targeting different columns use the same execution plan, the results will be wrong. Therefore, such queries are not cached. However, if the query is a common one, such as `Order By a+?`, it is cached.
- The query contains `?` after `Group By`, such as `Group By?`. Such queries group data based on the column specified by `?`. If the queries targeting different columns use the same execution plan, the results will be wrong. Therefore, such queries are not cached. However, if the query is a common one, such as `Group By a+?`, it is cached.
- The query contains `?` in the definition of the `Window Frame` window function, such as `(partition by year order by sale rows ? preceding)`. If `?` appears elsewhere in the window function, the query is cached.
- The query contains parameters for comparing `int` and `string`, such as `c_int >= ?` or `c_int in (?, ?)`, in which `?` indicates the string type, such as `set @x='123'`. To ensure that the query result is compatible with MySQL, parameters need to be adjusted in each query, so such queries are not cached.
- The plan attempts to access `TiFlash`.
- In most cases, the plan that contains `TableDual` is not cached, unless the current `Prepare` statement does not have parameters.
- The query accesses TiDB system views, such as `information_schema.columns`. It is not recommended to use `Prepare` and `Execute` statements to access system views.
- TiDB has a limitation on the number of `?` in a query. If a query contains more than 65535 `?`, an error `Prepared statement contains too many placeholders` is reported.

## Non-Prepared Plan Cache

Non-Prepared Plan Cache has all limitations that Prepared Plan Cache has, and besides that, Non-Prepared Plan Cache only supports simple TP queries.

Below are its limitations:

- Queries or plans that are not supported by the Prepared plan cache are also not supported by the non-prepared plan cache.
- Queries or plans that are not supported by the [Prepared plan cache](/sql-plan-cache.md) are also not supported by the non-prepared plan cache.
- Queries that contain complex operators such as `Window` or `Having` are not supported.
- Queries that contain three or more `Join` tables or subqueries are not supported.
- Queries that contain numbers or expressions directly after `ORDER BY` or `GROUP BY` are not supported, such as `ORDER BY 1` and `GROUP BY a+1`. Only `ORDER BY column_name` and `GROUP BY column_name` are supported.
- Queries that filter on columns of `JSON`, `ENUM`, `SET`, or `BIT` type are not supported, such as `SELECT * FROM t WHERE json_col = '{}'`.
- Queries that filter on `NULL` values are not supported, such as `SELECT * FROM t WHERE a is NULL`.
- Queries with more than 200 parameters after parameterization are not supported by default, such as `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`. Starting from v7.3.0, you can modify this limit by setting the [`44823`](/optimizer-fix-controls.md#44823-new-in-v730) fix in the [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) system variable.
- Queries that access virtual columns, temporary tables, views, or memory tables are not supported, such as `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`, where `COLUMNS` is a TiDB memory table.
- Queries with hints or bindings are not supported.
- DML statements or `SELECT` statements with the `FOR UPDATE` clause are not supported by default. To remove this restriction, you can execute `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`.

After you enable this feature, the optimizer quickly evaluates the query. If it does not meet the support conditions for non-prepared plan cache, the query falls back to the regular optimization process.

# Others

## Ignore the `COM_STMT_CLOSE` command and the `DEALLOCATE PREPARE` statement

To reduce the syntax parsing cost of SQL statements, it is recommended that you run `prepare stmt` once, then `execute stmt` multiple times before running `deallocate prepare`:

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;  -- Execute once
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- Execute multiple times
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

In real practice, you may be used to running `deallocate prepare` each time after running `execute stmt`, as shown below:

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
MySQL [test]> prepare stmt from '...'; -- Prepare twice
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

In such practice, the plan obtained by the first executed statement cannot be reused by the second executed statement.

To address the problem, you can set the system variable [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) to `ON` so TiDB ignores commands to close `prepare stmt`:

{{< copyable "sql" >}}

```sql
mysql> set @@tidb_ignore_prepared_cache_close_stmt=1;  -- Enable the variable
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- Prepare once
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- Execute once
Empty set (0.00 sec)

mysql> deallocate prepare stmt;             -- Release after the first execute
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- Prepare twice
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- Execute twice
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;       -- Reuse the last plan
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```