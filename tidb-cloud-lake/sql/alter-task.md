---
title: ALTER TASK
summary: ALTER TASK 语句用于修改现有任务。
---

# ALTER TASK

`ALTER TASK` 语句用于修改现有任务。

**注意：** 此功能仅在 {{{ .lake }}} 中开箱即用。

## 语法 {#syntax}

```sql
--- suspend or resume a task
ALTER TASK [ IF EXISTS ] <name> RESUME | SUSPEND

--- change task settings
ALTER TASK [ IF EXISTS ] <name> SET
  [ WAREHOUSE = <string> ]
  [ SCHEDULE = { <number> MINUTE | <number> SECOND | USING CRON <expr> <time_zone> } ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num ]
  [ ERROR_INTEGRATION = <string> ]
   [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
  [ COMMENT = <string> ]

--- change task SQL
ALTER TASK [ IF EXISTS ] <name> MODIFY AS <sql>

--- modify DAG when condition and after condition
ALTER TASK [ IF EXISTS ] <name> REMOVE AFTER <string> | ADD AFTER <string>
--- allow to change condition for task execution
ALTER TASK [ IF EXISTS ] <name> MODIFY WHEN <boolean_expr>
```

| 参数 | 描述 |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | 可选。如果指定了该选项，仅当已存在同名任务时才会修改该任务。 |
| name                             | 任务名称。这是必填字段。 |
| RESUME \| SUSPEND                | 恢复或暂停任务。 |
| SET                              | 更改任务设置。有关详细参数说明，请参见 [Create Task](/tidb-cloud-lake/sql/create-task.md)。 |
| MODIFY AS                        | 更改任务 SQL。 |
| REMOVE AFTER | 从任务 DAG 中移除前置任务；如果没有剩余前置任务，该任务将变为独立任务或根任务。 |
| ADD AFTER | 向任务 DAG 中添加前置任务。 |
| MODIFY WHEN | 更改任务执行条件。 |

## 示例 {#examples}

```sql
ALTER TASK IF EXISTS mytask SUSPEND;
```

此命令会在任务 `mytask` 存在时将其暂停。

```sql
ALTER TASK IF EXISTS mytask SET
  WAREHOUSE = 'new_warehouse'
  SCHEDULE = USING CRON '0 12 * * * *' 'UTC';
```

此示例修改了 `mytask` 任务，将其计算集群更改为 `new_warehouse`，并将其调度更新为每天 UTC 中午运行。

```sql
ALTER TASK IF EXISTS mytask MODIFY
AS
INSERT INTO new_table SELECT * FROM source_table;
```

这里，`mytask` 执行的 SQL 语句被更改为将数据从 `source_table` 插入到 `new_table`。

```sql
ALTER TASK mytaskchild MODIFY WHEN STREAM_STATUS('stream3') = False;
```

在此示例中，我们修改了 `mytaskchild` 任务的 `WHEN` 条件。现在，只有当 `stream3` 的 `STREAM_STATUS` 函数结果为 `False` 时，该任务才会运行。这意味着当 `stream3` 不包含变更数据时，任务会执行。

```sql
ALTER TASK MyTask1 ADD AFTER 'task2';
```

在此示例中，我们为 `MyTask1` 任务添加了依赖关系。现在，它将在 `task2` 和 `task3` 都成功完成后运行。这会在任务的有向无环图（DAG）中创建依赖关系。

```sql
ALTER TASK MyTask1 REMOVE AFTER 'task2';
```

这里，我们移除了 `MyTask1` 任务的一项特定依赖关系。它将不再在 `task2` 之后运行。如果你想修改任务 DAG 中的依赖关系，这会很有用。