---
title: Worker
summary: Worker-related SQL commands for deployments with cloud control enabled.
---

# Worker

Worker-related SQL commands for deployments with cloud control enabled.

> **Note:**
>
> Worker management commands require cloud control. If `cloud_control_grpc_server_address` is not configured, {{{ .lake }}} returns a `CloudControlNotEnabled` error when you run these commands.

## Supported Statements

| Statement | Purpose |
|-----------|---------|
| `CREATE WORKER` | Creates a worker with an optional key-value option list |
| `ALTER WORKER` | Updates worker tags or options, or changes worker state |
| `DROP WORKER` | Deletes a worker |
| `SHOW WORKERS` | Lists workers in the current tenant |

## Command Reference

| Command | Description |
|---------|-------------|
| [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) | Creates a worker definition |
| [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) | Modifies worker tags, options, or state |
| [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) | Removes a worker definition |
| [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) | Lists workers and their metadata |
| [Examples](/tidb-cloud-lake/sql/worker-examples.md) | Shows validated worker SQL examples |

## Notes

- Option names are case-insensitive. {{{ .lake }}} normalizes them to lowercase during planning.
- `SHOW WORKERS` returns the columns `name`, `tags`, `options`, `created_at`, and `updated_at`.
- `ALTER WORKER` supports `SET TAG`, `UNSET TAG`, `SET`, `UNSET`, `SUSPEND`, and `RESUME`.
- `CREATE WORKER` does not support a `TAG` clause.
