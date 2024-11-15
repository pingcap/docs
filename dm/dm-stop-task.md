---
title: Stop a Data Migration Task
summary: Learn how to stop a data migration task.
---

# Stop a Data Migration Task

You can use the `stop-task` command to stop a data migration task. For differences between `stop-task` and `pause-task`, refer to [Pause a Data Migration Task](/dm/dm-pause-task.md).

{{< copyable "" >}}

```bash
help stop-task
```

```
stop a specified task

Usage:
 dmctl stop-task [-s source ...] <task-name | task-file> [flags]

Flags:
 -h, --help   help for stop-task

Global Flags:
 -s, --source strings   MySQL Source ID
```

## Usage example

{{< copyable "" >}}

```bash
stop-task [-s "mysql-replica-01"]  task-name
```

## Flags description

- `-s`: (Optional) Specifies the MySQL source where the subtasks of the migration task (that you want to stop) run. If it is set, only subtasks on the specified MySQL source are stopped.
- `task-name | task-file`: (Required) Specifies the task name or task file path.

## Returned results

{{< copyable "" >}}

```bash
stop-task test
```

```
{
    "op": "Stop",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

> **Note:**
>
> After you stop a migration task with the `stop-task` command, running [`query-status`](/dm/dm-query-status.md) will no longer display the task. However, the checkpoint and other related information for this task is still retained in the `dm_meta` database.
>
> + To start over the migration task, add the `--remove-meta` option when running the [`start-task`](/dm/dm-create-task.md) command.
> + To completely remove the migration task, manually delete the four tables that use the task name as a prefix from the `dm_meta` database.