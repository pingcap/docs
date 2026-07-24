---
title: SHOW WORKERS
summary: List workers and their metadata with SHOW WORKERS.
---

# SHOW WORKERS

> **Note:**
>
> Introduced in v1.3.0.

Lists workers in the current tenant.

> **Note:**
>
> This command requires cloud control to be enabled.

## Syntax

```sql
SHOW WORKERS
```

## Output

`SHOW WORKERS` returns the following columns:

| Column | Description |
|--------|-------------|
| `name` | Worker name |
| `tags` | Worker tags in JSON format |
| `options` | Worker options in JSON format |
| `created_at` | Worker creation timestamp |
| `updated_at` | Worker update timestamp |

## Examples

```sql
SHOW WORKERS;
```

Sample output:

```text
read_env,{},"{""auto_resume"":""true"",""auto_suspend"":""300"",""max_cluster_count"":""3"",""min_cluster_count"":""1"",""size"":""small""}",2026-04-23T11:40:27.942797+00:00,2026-04-23T11:40:27.942797+00:00
```

## Related Topics

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - Create a worker
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - Modify worker tags, options, or state
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - Remove a worker
