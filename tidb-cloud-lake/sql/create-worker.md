---
title: CREATE WORKER
summary: Creates a worker with an optional key-value option list.
---

# CREATE WORKER

> **Note:**
>
> Introduced in v1.3.0.

Creates a worker.

> **Note:**
>
> This command requires cloud control to be enabled.

## Syntax

```sql
CREATE WORKER [ IF NOT EXISTS ] <worker_name>
    [ WITH <option_name> = <option_value> [ , <option_name> = <option_value> ... ] ]
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IF NOT EXISTS` | Optional. Succeeds without changes if the worker already exists. |
| `<worker_name>` | The worker name. |
| `<option_name>` | Worker option key. |
| `<option_value>` | Worker option value. |

## Options

{{{ .lake }}} accepts a single `WITH` clause followed by a comma-separated option list. Common worker options include:

| Option | Example Value | Description |
|--------|---------------|-------------|
| `size` | `'small'` | Controls the compute size of the worker. |
| `auto_suspend` | `'300'` | Idle timeout before automatic suspend. |
| `auto_resume` | `'true'` | Controls whether the worker resumes automatically. |
| `max_cluster_count` | `'3'` | Upper bound for auto-scaling clusters. |
| `min_cluster_count` | `'1'` | Lower bound for auto-scaling clusters. |

- `WITH` appears at most once.
- Options are separated by commas.
- Option names are normalized to lowercase before the request is sent.
- `option_value` can be written as a string literal, bare identifier, unsigned integer, or boolean.
- `CREATE WORKER` does not support a `TAG` clause.

## Examples

Create a worker without options:

```sql
CREATE WORKER read_env;
```

Create a worker with `IF NOT EXISTS`:

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

Create a worker with custom options:

```sql
CREATE WORKER IF NOT EXISTS read_env
WITH size = 'small',
     auto_suspend = '300',
     auto_resume = 'true',
     max_cluster_count = '3',
     min_cluster_count = '1';
```

## Related Topics

- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - Modify worker tags, options, or state
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - List workers and their metadata
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - Remove a worker
