---
title: CREATE TASK
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

The CREATE TASK statement is used to define a new task that executes a specified SQL statement on a scheduled basis or dag based task graph.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax

```sql
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
 WAREHOUSE = <string>
 SCHEDULE = { <num> MINUTE | <num> SECOND | USING CRON <expr> <time_zone> }
 [ AFTER <string>
 [ WHEN <boolean_expr> ]
 [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
 [ ERROR_INTEGRATION = <string> ]
 [ COMMENT = '<string_literal>' ]
 [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
AS
{ <sql_statement>
| BEGIN
    <sql_statement>;
    [ <sql_statement>; ... ]
  END;
}
```

Wrap multiple SQL statements in a `BEGIN ... END;` block so the task executes them sequentially as a script.

| Parameter                                        | Description                                                                                                                                                                  |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IF NOT EXISTS                                    | Optional. If specified, the task will only be created if a task of the same name does not already exist.                                                                     |
| name                                             | The name of the task. This is a mandatory field.                                                                                                                             |
| WAREHOUSE                                        | Required. Specifies the virtual warehouse to use for the task.                                                                                                               |
| SCHEDULE                                         | Required. Defines the schedule on which the task will run. Can be specified in minutes or using a CRON expression along with a time zone.                                    |
| SUSPEND_TASK_AFTER_NUM_FAILURES                  | Optional. The number of consecutive failures after which the task will be automatically suspended.                                                                           |
| AFTER                                            | List task that must be completed before this task starts.                                                                                                                  |
| WHEN boolean_expr                                | A condition that must be true for the task to run.                                                                                                                           |
| [ERROR_INTEGRATION](../16-notification/index.md) | Optional. The name of the notification integration to use for the task error notification with specific [task error payload ](./10-task-error-integration-payload.md)applied |
| COMMENT                                          | Optional. A string literal that serves as a comment or description for the task.                                                                                             |
| session_parameter                                | Optional. Specifies session parameters to use for the task during task run. Note that session parameters must be placed after all other task parameters in the CREATE TASK statement. |
| sql                                              | The SQL statement that the task will execute. It can be a single statement or a script wrapped in `BEGIN ... END;`. This is a mandatory field.                                |

### Usage Notes

- A schedule must be defined for a standalone task or the root task in a DAG of tasks; otherwise, the task only runs if manually executed using EXECUTE TASK.
- A schedule cannot be specified for child tasks in a DAG.
- After creating a task, you must execute ALTER TASK … RESUME before the task will run based on the parameters specified in the task definition.
- When Condition only support a subset of `<boolean_expression>`
  The following are supported in a task WHEN clause:

  - [STREAM_STATUS](../../../20-sql-functions/17-table-functions/stream-status.md) is supported for evaluation in the SQL expression. This function indicates whether a specified stream contains change tracking data. You can use this function to evaluate whether the specified stream contains change data before starting the current run. If the result is FALSE, then the task does not run.
  - Boolean operators such as AND, OR, NOT, and others.
  - Casts between numeric, string and boolean types.
  - Comparison operators such as equal, not equal, greater than, less than, and others.
 
   :::note
  Warning: When using STREAM_STATUS in tasks, you must include the database name when referencing the stream (e.g., `STREAM_STATUS('mydb.stream_name')`).
   :::

- Multiple tasks that consume change data from a single table stream retrieve different deltas. When a task consumes the change data in a stream using a DML statement, the stream advances the offset. The change data is no longer available for the next task to consume. Currently, we recommend that only a single task consumes the change data from a stream. Multiple streams can be created for the same table and consumed by different tasks.
- Tasks will not retry on each execution; each execution is serial. Each script SQL is executed one by one, with no parallel execution. This ensures that the sequence and dependencies of task execution are maintained.
- Interval-based tasks follow a fixed interval spot in a tight way. This means that if the current task execution time exceeds the interval unit, the next task will execute immediately. Otherwise, the next task will wait until the next interval unit is triggered. For example, if a task is defined with a 1-second interval and one task execution takes 1.5 seconds, the next task will execute immediately. If one task execution takes 0.5 seconds, the next task will wait until the next 1-second interval tick starts.
- While session parameters can be specified during task creation, you can also modify them later using the ALTER TASK statement. For example:
  ```sql
  ALTER TASK simple_task SET 
      enable_query_result_cache = 1, 
      query_result_cache_min_execute_secs = 5;
  ```

### Important Notes on Cron Expressions

- The cron expression used in the `SCHEDULE` parameter must contain **exactly 6 fields**.
- The fields represent the following:
  1. **Second** (0-59)
  2. **Minute** (0-59)
  3. **Hour** (0-23)
  4. **Day of the Month** (1-31)
  5. **Month** (1-12 or JAN-DEC)
  6. **Day of the Week** (0-6, where 0 is Sunday, or SUN-SAT)

 #### Example Cron Expressions:

- **Daily at 9:00:00 AM Pacific Time:**
  - `USING CRON '0 0 9 * * *' 'America/Los_Angeles'`

- **Every minute:**
  - `USING CRON '0 * * * * *' 'UTC'`
  - This runs the task every minute at the start of the minute.

- **Every hour at the 15th minute:**
  - `USING CRON '0 15 * * * *' 'UTC'`
  - This runs the task every hour at 15 minutes past the hour.

- **Every Monday at 12:00:00 PM:**
  - `USING CRON '0 0 12 * * 1' 'UTC'`
  - This runs the task every Monday at noon.

- **On the first day of every month at midnight:**
  - `USING CRON '0 0 0 1 * *' 'UTC'`
  - This runs the task at midnight on the first day of every month.

- **Every weekday at 8:30:00 AM:**
  - `USING CRON '0 30 8 * * 1-5' 'UTC'`
  - This runs the task every weekday (Monday to Friday) at 8:30 AM.

## Usage Examples

### CRON Schedule

```sql
CREATE TASK my_daily_task
 WAREHOUSE = 'compute_wh'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 COMMENT = 'Daily summary task'
AS
 INSERT INTO summary_table SELECT * FROM source_table;
```

In this example, a task named `my_daily_task` is created. It uses the **compute_wh** warehouse to run a SQL statement that inserts data into summary_table from source_table. The task is scheduled to run using a **CRON expression** that executes **daily at 9 AM Pacific Time**.

### Multiple Statements

```sql
CREATE TASK IF NOT EXISTS nightly_refresh
 WAREHOUSE = 'etl'
 SCHEDULE = USING CRON '0 0 2 * * *' 'UTC'
AS
BEGIN
    DELETE FROM staging.events WHERE event_time < DATEADD(DAY, -1, CURRENT_TIMESTAMP());
    INSERT INTO mart.events SELECT * FROM staging.events;
END;
```

This example creates a task named `nightly_refresh` that executes a script containing multiple statements. The script is wrapped in `BEGIN ... END;` so the DELETE runs before the INSERT each time the task executes.

### Dynamic SQL (EXECUTE IMMEDIATE)

```sql
CREATE OR REPLACE TASK log_ingestion
  WAREHOUSE = 'default'
  SCHEDULE = 1 MINUTE
AS
EXECUTE IMMEDIATE $$
BEGIN
    LET path := CONCAT('@mylog/', DATE_FORMAT(CURRENT_DATE - INTERVAL 3 DAY, '%m/%d/'));

    LET sql := CONCAT(
        'COPY INTO logs.web_logs FROM ', path,
        ' PATTERN = ''.*[.]gz'' FILE_FORMAT = (type = NDJSON compression = AUTO) MAX_FILES = 10000'
    );

    EXECUTE IMMEDIATE :sql;
END;
$$;
```

This example creates a task that runs every minute. It dynamically computes the stage path for **3 days ago** (for example, `@mylog/12/15/`), builds a `COPY INTO` statement, and executes it via `EXECUTE IMMEDIATE`.

### Automatic Suspension

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'system'
 SCHEDULE = 2 MINUTE
 SUSPEND_TASK_AFTER_NUM_FAILURES = 3
AS
 INSERT INTO compaction_test.test VALUES((1));
```

This example creates a task named `mytask`, if it doesn't already exist. The task is assigned to the **system** warehouse and is scheduled to run **every 2 minutes**. It will be **automatically suspended** if it **fails three times consecutively**. The task performs an INSERT operation into the compaction_test.test table.

### Second-Level Scheduling

```sql
CREATE TASK IF NOT EXISTS daily_sales_summary
 WAREHOUSE = 'analytics'
 SCHEDULE = 30 SECOND
AS
 SELECT sales_date, SUM(amount) AS daily_total
 FROM sales_data
 GROUP BY sales_date;
```

In this example, a task named `daily_sales_summary` is created with **second-level scheduling**. It is scheduled to run **every 30 SECOND**. The task uses the **analytics** warehouse and calculates the daily sales summary by aggregating data from the sales_data table.

### Task Dependencies

```sql
CREATE TASK IF NOT EXISTS process_orders
 WAREHOUSE = 'etl'
 AFTER task1
AS
 INSERT INTO data_warehouse.orders SELECT * FROM staging.orders;
```

In this example, a task named `process_orders` is created, and it is defined to run **after the successful completion** of **task1** and **task2**. This is useful for creating **dependencies** in a **Directed Acyclic Graph (DAG)** of tasks. The task uses the **etl** warehouse and transfers data from the staging area to the data warehouse.

> Tip: Using the AFLTER parameter does not require setting the SCHEDULE parameter.

### Conditional Execution

```sql
CREATE TASK IF NOT EXISTS hourly_data_cleanup
 WAREHOUSE = 'maintenance'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 WHEN STREAM_STATUS('db1.change_stream') = TRUE
AS
 DELETE FROM archived_data
 WHERE archived_date < DATEADD(HOUR, -24, CURRENT_TIMESTAMP());

```

In this example, a task named `hourly_data_cleanup` is created. It uses the **maintenance** warehouse and is scheduled to run **every hour**. The task deletes data from the archived_data table that is older than 24 hours. The task only runs **if the condition is met** using the **STREAM_STATUS** function to check if the `db1.change_stream` contains change data.

### Error Integration

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'mywh'
 SCHEDULE = 30 SECOND
 ERROR_INTEGRATION = 'myerror'
AS
 BEGIN
    BEGIN;
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
    DELETE FROM mytable WHERE ts < DATEADD(MINUTE, -5, CURRENT_TIMESTAMP());
    COMMIT;
 END;
```

In this example, a task named `mytask` is created. It uses the **mywh** warehouse and is scheduled to run **every 30 seconds**. The task executes a **BEGIN block** that contains an INSERT statement and a DELETE statement. The task commits the transaction after both statements are executed. When the task fails, it will trigger the **error integration** named **myerror**.

### Session Parameters

```sql
CREATE TASK IF NOT EXISTS cache_enabled_task
 WAREHOUSE = 'analytics'
 SCHEDULE = 5 MINUTE
 COMMENT = 'Task with query result cache enabled'
 enable_query_result_cache = 1,
 query_result_cache_min_execute_secs = 5
AS
 SELECT SUM(amount) AS total_sales
 FROM sales_data
 WHERE transaction_date >= DATEADD(DAY, -7, CURRENT_DATE())
 GROUP BY product_category;
```

In this example, a task named `cache_enabled_task` is created with **session parameters** that enable query result caching. The task is scheduled to run **every 5 minutes** and uses the **analytics** warehouse. The session parameters **`enable_query_result_cache = 1`** and **`query_result_cache_min_execute_secs = 5`** are specified **after all other task parameters**, enabling the query result cache for queries that take at least 5 seconds to execute. This can **improve performance** for subsequent executions of the same task if the underlying data hasn't changed.

### View Task Run History

Use the `TASK_HISTORY()` table function to see when and how tasks ran:

```sql
SELECT *
FROM TASK_HISTORY(
  TASK_NAME   => 'daily_sales_summary',
  RESULT_LIMIT => 20
)
ORDER BY scheduled_time DESC;
```

See [TASK HISTORY](../../../20-sql-functions/17-table-functions/task_histroy.md) for all options, including filtering by time range or root task ID in a DAG.
