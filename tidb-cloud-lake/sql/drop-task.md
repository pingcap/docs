---
title: DROP TASK
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

The DROP TASK statement is used to delete an existing task.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax

```sql
DROP TASK [ IF EXISTS ] <name>
```

| Parameter                        | Description                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | Optional. If specified, the task will only be dropped if a task of the same name already exists. |
| name                             | The name of the task. This is a mandatory field.                                                       |

## Usage Notes:

- If a predecessor task in a DAG is dropped, then all former child tasks that identified this task as the predecessor become either standalone tasks or root tasks, depending on whether other tasks identify these former child tasks as their predecessor. These former child tasks are suspended by default and must be resumed manually.
- Root Task must be suspended before DROP

## Usage Examples

```sql
DROP TASK IF EXISTS mytask;
```

This command deletes the task named mytask if it exists.