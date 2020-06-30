---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
category: reference
---

# SQL Prepare Execution Plan Cache

TiDB supports execution plan caching for `Prepare` / `Execute` queries.

There are two forms of `Prepare` / `Execute` queries:

- in the binary communication protocol, use `COM_STMT_PREPARE` and
  `COM_STMT_EXECUTE` to execute general parameterized queries;
- in the text communication protocol, use `COM_QUERY` to execute `Prepare` and
  `Execution` queries.

The optimizer handles these two types of queries in the same way: in preparing, the parameterized query will be parsed into an AST (Abstract Syntax Tree) and cached; in later executing, the execution plan will be generated based on saved AST and specific parameter values.

When the execution plan cache is turned on, in the first execution every `Prepare` statement will check whether the current query can use the execution plan cache, and if it can be used, then put the generated execution plan into a cache implemented by LRU (Least Recently Used) linked list. In the subsequent `Execute` queries, the execution plan will be obtained from the cache and checked for availability. If the check succeeds, the step of generating an execution plan is skipped, otherwise, the execution plan is regenerated and saved in the cache.

In the current version, when the `Prepare` statement meets any of the following conditions, the query cannot use the execution plan cache:

- the query contains variables other than `?` (including system variables or user-defined
variables);
- the query contains sub-queries;
- the query contains functions that cannot be cached, such as `current_user()`, `database()`, and `last_insert_id()`, etc.;
- the `Order By` statement of the query contains `?`;
- the `Group By` statement of the query contains `?`;
- the `Limit [Offset]` statement of the query contains `?`;
- the window frame definition of the `Window` function contains `?`;
- partition tables are involved in the query.

The LRU linked list is designed as a session-level cache because `Prepare` /
`Execute` cannot be executed across sessions. Each element of the LRU list is a
key-value pair, value is the execution plan, and the key is composed of the
following parts:

- the name of the database where `Execute` is executed;
- the identifier of the `Prepare` statement, the name after the `PREPARE`
  keyword;
- the current schema version, which will be updated after every successful DDL statement;
- the SQL Mode when executing `Execute`;
- the current time zone, which is the value of the system variable
  `time_zone`.

Any change in the above information (e.g. switching databases, renaming `Prepare` statement, executing DDL statements, or modifying the value of SQL mode / `time_zone`), or the LRU cache elimination mechanism will cause the execution plan cache miss in executing.

After the execution plan cache is obtained from the cache, TiDB will first check whether the execution plan is still valid. If the current `Execute` statement is executed in an explicit transaction, and the referenced table is modified in the transaction pre-order statement, the cached execution plan accessing this table does not contain the `UnionScan` operator, then it cannot be executed.

After the validation test is passed, the scan range of the execution plan will
be adjusted accordingly according to the current parameter values, and then used
to perform data querying.

There are two points worth noting about execution plan caching and query
performance:

- Considering that the parameters of `Execute` will be different, the execution plan cache will prohibit some aggressive query optimization methods that are closely related to specific parameter values to ensure adaptability, resulting in the query plan may not be optimal for certain parameter values. For example, the filter condition of the query is `where a > ? And a < ?`, the parameters of the first `Execute` statement are 2 and 1 respectively, considering that these two parameters maybe be 1 and 2 in the next execution time, the optimizer will not generate the optimal `TableDual` execution plan that is specific to current parameter values;
- If cache invalidation and elimination are not considered, an execution plan cache is applied to various parameter values, which in theory will also result in non-optimal execution plans for certain values. For example, if the filter condition is `where a < ?` and the parameter value used for the first execution is 1, then the optimizer generates the optimal `IndexScan` execution plan and puts it into the cache. In the subsequent executions, if the value becomes 10000, the `TableScan` plan will be the better. Due to the execution plan, the previously generated `IndexScan` will be used for execution. Therefore, the execution plan cache is more suitable for business scenarios where the query is simple (the ratio of compilation is high) and the execution plan is relatively fixed.

The execution plan cache is currently disabled by default. You can enable this function by turning on the [`prepare-plan-cache`](/tidb-configuration-file.md#prepared-plan-cache) in the configuration file.

> **Note：**
>
> The execution plan cache function applies only for `Prepare` / `Execute` queries and does not take effect for normal queries.

After the execution plan cache function is enabled, you can use the session-level system variable `last_plan_from_cache` to see whether the previous `Execute` statement used the cached execution plan, for example:

{{< copyable "sql" >}}

```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
-- The first execution generates an execution plan and saves it in the cache
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
-- The second execution hits the cache
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 1                      |
+------------------------+
1 row in set (0.00 sec)
```

If you find that a certain set of `Prepare` / `Execute` caused unexpected behavior due to the execution plan cache, you can use SQL Hint `ignore_plan_cache()` to skip using the execution plan cache for the current statement. Still using the above statement as an example:

{{< copyable "sql" >}}

```sql
MySQL [test]> prepare stmt from 'select /*+ ignore_plan_cache() */ * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
```
