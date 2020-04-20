---
title: Execution Plan Binding
summary: Learn about execution plan binding operations in TiDB.
category: reference
---

# Execution Plan Binding

The [Optimizer Hints](/reference/performance/optimizer-hints.md) document introduces how to select a specific execution plan using Hint. However, sometimes you need to interfere with execution selection without modifying SQL statements. Execution Plan Binding provides a set of functionalities to do this.

## Syntax

### Create binding

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt
```

This statement binds SQL execution plans at the GLOBAL or SESSION level. The default scope is SESSION. The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, as long as the parameterized SQL statement and a bound one in the system table are consistent and the system variable `tidb_use_plan_baselines` is set to `on` (the default value is `on`), the corresponding optimizer hint is available. If multiple execution plans are available, the optimizer chooses to bind the plan with the least cost.

`Parameterization` is a process that converts a constant in SQL to a variable parameter, with standardized processing on the spaces and line breaks in the SQL statement, for example,

{{< copyable "sql" >}}

```sql
select * from t where a >    1
-- parameterized:
select * from t where a > ？
```

> **Note:**
>
> The text must be the same before and after parameterization and hint removal for both the original SQL statement and the bound statement, or the binding will fail. Take the following examples:
>
> - This binding can be created successfully because the texts before and after parameterization and hint removal are the same: `select * from t where a > ?`
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
>     ```
>
> - This binding will fail because the original SQL statement is processed as `select * from t where a > ?`, while the bound SQL statement is processed differently as `select * from t where b > ?`.
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
>     ```

### Remove binding

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

### View binding

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level. The default scope is SESSION. Currently `SHOW BINDINGS` outputs eight columns, as shown below:

| Column Name | Note  |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including Using, Deleted, and Invalid |
| create_time | Creating time |
| update_time | Updating time |
| charset | Character set |
| collation | Ordering rule |

### Automatically create binding

To enable automatic binding creation, set `tidb_capture_plan_baselines` to `on`. The default value is `off`.

> **Note:**
>
> Because the automatic binding creation function relies on [Statement Summary](/reference/performance/statement-summary.md), make sure to enable Statement Summary before using automatic binding.

After automatic binding creation is enabled, the historical SQL statements in the Statement Summary are traversed every `bind-info-lease` (the default value is `3s`), and bindings are automatically created for SQL statements that appear at least twice.

### Automatically evolve binding

As data updates, the previously bound execution plan might no longer be optimal. The automatic binding evolution feature can optimize the bound execution plan. Use the following statement to enable automatic binding evolution:

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

The default value of `tidb_evolve_plan_baselines` is `off`.

> **Note:**
>
> The global variable does not take effect in the current session. It only takes effect in a newly created session. To enable automatic binding evolution in the current session, change the keyword `global` to `session`.

After the automatic binding evolution feature is enabled, if the optimal execution plan selected by the optimizer is not among the bound execution plans, the optimizer marks the plan as an execution plan that waits for verification. Every `bind-info-lease` (the default value is `3s`), an execution plan to be verified is selected and compared with a bound execution plan with the least cost, in terms of the actual execution time. If the plan to be verified is better, it is marked as a usable binding. The following use case describes the preceding process.

Let table `t` be defined as:

{{< copyable "sql" >}}

```sql
create table t(a int, b int, key(a), key(b));
```

Perform the following query on table `t`:

{{< copyable "sql" >}}

```sql
select * from t where a < 100 and b < 100;
```

Rows in the table that satisfy condition `a < 100` are rare. However, for some reasons, the optimizer mistakenly chooses the full table scan instead of the optimal execution plan that uses index `a`. Users can use the following statement to create a binding first:

{{< copyable "sql" >}}

```sql
create global binding for select * from t where a < 100 and b < 100 using select * from t use index(a) where a < 100 and b < 100;
```

When the previous query is executed again, the optimizer chooses index `a` under the interference of the binding created previously to reduce the query time.

Assuming that as insertions and deletions are performed on the table, the number of rows that satisfy condition `a < 100` grows while the number of rows that satisfy condition `b < 100` not, still using index `a` under the binding's interference might no longer be optimal.

The binding evolution can address this kind of problems. When the optimizer senses changes in table data, it generates an execution plan against the query that uses index `b`. However, because of the binding's presence, this query plan is not adopted and executed. Instead, it is stored in the backend evolution lists. During the evolution process, if it is verified that the time spent on executing the query plan is significantly shorter than that using index `a` (that is the current binding's execution plan), index `b` is added into available binding lists. After this process, when the query is executed again, the optimizer first generates the execution plan that uses index `b` and makes sure that it is in the binding lists. Then the optimizer adopts and executes it to reduce the query time after data updates.

To reduce the impact that the automatic evolution has on clusters, use the following configurations:

- Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is `600s`.
- Set `tidb_evolve_plan_task_start_time` (`00:00 +0000` by default) and `tidb_evolve_plan_task_end_time` (`23:59 +0000` by default) to limit the time window.
