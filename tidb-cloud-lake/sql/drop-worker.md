---
title: DROP WORKER
summary: Remove a worker with DROP WORKER.
---

# DROP WORKER

> **Note:**
>
> Introduced in v1.3.0.

Removes a worker.

> **Note:**
>
> This command requires cloud control to be enabled.

## Syntax

```sql
DROP WORKER [ IF EXISTS ] <worker_name>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IF EXISTS` | Optional. Suppresses the error if the worker does not exist. |
| `<worker_name>` | The worker name. |

## Examples

```sql
DROP WORKER read_env;
```

```sql
DROP WORKER IF EXISTS read_env;
```

## Related Topics

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - Create a worker
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - Modify worker tags, options, or state
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - List workers and their metadata
