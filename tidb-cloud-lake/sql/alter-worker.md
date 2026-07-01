---
title: ALTER WORKER
summary: Modify worker tags, options, or state with ALTER WORKER.
---

# ALTER WORKER

> **Note:**
>
> Introduced in v1.3.0.

Modifies a worker's tags, options, or state.

> **Note:**
>
> This command requires cloud control to be enabled.

## Syntax

```sql
ALTER WORKER <worker_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WORKER <worker_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WORKER <worker_name> SET <option_name> = <option_value> [ , <option_name> = <option_value> ... ]

ALTER WORKER <worker_name> UNSET <option_name> [ , <option_name> ... ]

ALTER WORKER <worker_name> SUSPEND

ALTER WORKER <worker_name> RESUME
```

## Parameters

| Form | Description |
|------|-------------|
| `SET TAG` | Adds or updates worker tags. Tag values must be string literals. |
| `UNSET TAG` | Removes one or more worker tags. |
| `SET` | Adds or updates worker options. Option names are normalized to lowercase. |
| `UNSET` | Removes one or more worker options. |
| `SUSPEND` | Suspends the worker. |
| `RESUME` | Resumes the worker. |

## Examples

Set tags on a worker:

```sql
ALTER WORKER read_env
SET TAG purpose = 'sandbox', owner = 'ci';
```

Update worker options:

```sql
ALTER WORKER read_env
SET size = 'medium', auto_suspend = '600';
```

Remove a tag and an option:

```sql
ALTER WORKER read_env UNSET TAG owner;
ALTER WORKER read_env UNSET auto_suspend;
```

Change worker state:

```sql
ALTER WORKER read_env SUSPEND;
ALTER WORKER read_env RESUME;
```

## Related Topics

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - Create a worker
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - List workers and their metadata
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - Remove a worker
