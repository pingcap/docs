---
title: SHOW TASKS
sidebar_position: 5
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.900"/>

Lists the tasks that are visible to the current role.

**NOTICE:** This command works out of the box only in Databend Cloud. For self-hosted deployments, configure Cloud Control to query tasks.

## Syntax

```sql
SHOW TASKS [LIKE '<pattern>' | WHERE <expr>]
```

| Parameter | Description |
|-----------|-------------|
| LIKE      | Filters task names using case-sensitive pattern matching with the `%` wildcard. |
| WHERE     | Filters the result set using an expression on the output columns.               |

### Output

`SHOW TASKS` returns the following columns:

- `created_on`: Timestamp when the task was created.
- `name`: Task name.
- `id`: Internal task identifier.
- `owner`: Role that owns the task.
- `comment`: Optional comment.
- `warehouse`: Warehouse assigned to the task.
- `schedule`: Interval or CRON schedule, when present.
- `state`: Current status (`Started` or `Suspended`).
- `definition`: SQL the task runs.
- `condition_text`: WHEN condition for the task.
- `after`: Comma-separated list of upstream tasks in a DAG.
- `suspend_task_after_num_failures`: Number of consecutive failures before suspension.
- `error_integration`: Notification integration for failures.
- `next_schedule_time`: Timestamp of the next scheduled run.
- `last_committed_on`: Timestamp when the task definition was last updated.
- `last_suspended_on`: Timestamp when the task was last suspended, if any.
- `session_parameters`: Session parameters applied when the task runs.

## Examples

List all tasks available to the current role:

```sql
SHOW TASKS;
+----------------------------+---------------+------+---------------+---------+-----------+---------------------------------+----------+-------------------------------------------+------------------------+---------+-------------------------------------+-------------------+----------------------------+----------------------------+----------------------------+---------------------------------------------------+
| created_on                 | name          | id   | owner         | comment | warehouse | schedule                        | state    | definition                                | condition_text         | after   | suspend_task_after_num_failures     | error_integration | next_schedule_time         | last_committed_on          | last_suspended_on          | session_parameters                                  |
+----------------------------+---------------+------+---------------+---------+-----------+---------------------------------+----------+-------------------------------------------+------------------------+---------+-------------------------------------+-------------------+----------------------------+----------------------------+----------------------------+---------------------------------------------------+
| 2024-07-01 08:00:00.000000 | ingest_sales  | 101  | ACCOUNTADMIN  | NULL    | etl_wh    | CRON 0 5 * * * * TIMEZONE UTC   | Started  | COPY INTO sales FROM @stage PATTERN '.*'  | STREAM_STATUS('s1')    |         |                                   3 | slack_errors      | 2024-07-01 08:05:00.000000 | 2024-07-01 08:00:00.000000 | NULL                       | {"enable_query_result_cache":"1"}                   |
| 2024-07-01 09:00:00.000000 | hourly_checks | 102  | SYSADMIN      | health  | etl_wh    | INTERVAL 3600 SECOND            | Suspended | CALL run_health_check()                   |                        | ingest_sales |                                NULL | NULL              | 2024-07-01 10:00:00.000000 | 2024-07-01 09:05:00.000000 | 2024-07-01 09:10:00.000000 | {"query_result_cache_min_execute_secs":"5"}         |
+----------------------------+---------------+------+---------------+---------+-----------+---------------------------------+----------+-------------------------------------------+------------------------+---------+-------------------------------------+-------------------+----------------------------+----------------------------+----------------------------+---------------------------------------------------+
```

Show only tasks whose names start with `ingest_`:

```sql
SHOW TASKS LIKE 'ingest_%';
```
