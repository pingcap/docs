---
title: ALTER TASK
sidebar_position: 2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

The ALTER TASK statement is used to modify an existing task.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax

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

| Parameter                        | Description                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | Optional. If specified, the task will only be altered if a task of the same name already exists. |
| name                             | The name of the task. This is a mandatory field.                                                       |
| RESUME \| SUSPEND                | Resume or suspend the task.                                                                          |
| SET                              | Change task settings. details parameter descriptions could be found on see [Create Task](01-ddl-create_task.md).                                                                               |
| MODIFY AS                        | Change task SQL.                                                                                     |
| REMOVE AFTER |  Remove predecessor task from the task dag, task would become a standalone task or a root task if no predecessor tasks left. |
| ADD AFTER | Add predecessor task to the task dag. |
| MODIFY WHEN | Change the condition for task execution. |

## Examples

```sql
ALTER TASK IF EXISTS mytask SUSPEND;
```
This command suspends the task named mytask if it exists.

```sql
ALTER TASK IF EXISTS mytask SET
  WAREHOUSE = 'new_warehouse'
  SCHEDULE = USING CRON '0 12 * * * *' 'UTC';
```
This example alters the mytask task, changing its warehouse to new_warehouse and updating its schedule to run daily at noon UTC.

```sql
ALTER TASK IF EXISTS mytask MODIFY 
AS
INSERT INTO new_table SELECT * FROM source_table;
```
Here, the SQL statement executed by mytask is changed to insert data from source_table into new_table.

```sql
ALTER TASK mytaskchild MODIFY WHEN STREAM_STATUS('stream3') = False;
```
In this example, we are modifying the mytaskchild task to change its WHEN condition. The task will now only run if the STREAM_STATUS function for 'stream3' evaluates to False. This means the task will execute when 'stream3' does not contain change data.

```sql
ALTER TASK MyTask1 ADD AFTER 'task2';
```
In this example, we are adding dependencies to the MyTask1 task. It will now run after the successful completion of both 'task2' and 'task3'. This creates a dependency relationship in a Directed Acyclic Graph (DAG) of tasks.

```sql
ALTER TASK MyTask1 REMOVE AFTER 'task2';
```
Here, we are removing a specific dependency for the MyTask1 task. It will no longer run after 'task2'. This can be useful if you want to modify the task's dependencies within a DAG of tasks.

