---
title: Task
---

This page provides a comprehensive overview of task operations in Databend, organized by functionality for easy reference.

## Task Management

| Command | Description |
|---------|-------------|
| [CREATE TASK](01-ddl-create_task.md) | Creates a new scheduled task |
| [ALTER TASK](02-ddl-alter-task.md) | Modifies an existing task |
| [DROP TASK](03-ddl-drop-task.md) | Removes a task |
| [EXECUTE TASK](04-ddl-execute-task.md) | Manually executes a task |

## Task Information

| Command | Description |
|---------|-------------|
| [SHOW TASKS](05-show-tasks.md) | Lists tasks visible to the current role |
| [TASK HISTORY](../../../20-sql-functions/17-table-functions/task_histroy.md) | Shows run history for one or more tasks |
| [TASK ERROR INTEGRATION PAYLOAD](10-task-error-integration-payload.md) | Shows the error payload format for task error notifications |

:::note
Tasks in Databend allow you to schedule and automate SQL commands for execution at specified intervals.
:::
