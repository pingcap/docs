---
title: EXECUTE TASK
sidebar_position: 4
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

The EXECUTE TASK statement is used to execute an existing task manually

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax

```sql
EXECUTE TASK  <name>
```

| Parameter                        | Description                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| name                             | The name of the task. This is a mandatory field.                                                       |

## Usage Notes:
- The SQL command can only execute a standalone task or the root task in a DAG. If a child task is input, the command returns a user error.

## Usage Examples

```sql
EXECUTE TASK  mytask;
```

This command executes the task named mytask.
