---
title: tdc db Command Reference
summary: Reference every tdc db command for Starter clusters, branches, SQL users, connection strings, and SQL execution.
---

# tdc db Command Reference

Use `tdc db` to manage TiDB Cloud Starter clusters, branches, and SQL access.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
tdc db
├── create-db-cluster
├── list-db-clusters
├── describe-db-cluster
├── update-db-cluster
├── delete-db-cluster
├── create-db-cluster-branch
├── list-db-cluster-branches
├── describe-db-cluster-branch
├── delete-db-cluster-branch
├── create-db-sql-users
├── format-db-connection-string
└── execute-sql-statement
```

## Command details

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `create-db-cluster` | Creates a Starter cluster. Requires `--db-cluster-name`; `--db-cluster-type` is optional and defaults to `starter`. Use `--wait` for an `ACTIVE` result. | `tdc db create-db-cluster --db-cluster-name app-db --wait` |
| `list-db-clusters` | Lists Starter clusters with pagination, filter, ordering, and query support. | `tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name}'` |
| `describe-db-cluster` | Reads one cluster by `--db-cluster-id`; `--view FULL` requests expanded fields. | `tdc db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL` |
| `update-db-cluster` | Changes the name or monthly spending limit of one cluster. Supports `--dry-run`. | `tdc db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2` |
| `delete-db-cluster` | Deletes one cluster by ID. Use `--wait` to wait until deletion is observable. | `tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --wait` |
| `create-db-cluster-branch` | Creates a branch from a cluster. Requires cluster ID and branch name; supports `--wait`. | `tdc db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait` |
| `list-db-cluster-branches` | Lists branches for one cluster with pagination. | `tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>" --output text` |
| `describe-db-cluster-branch` | Reads one branch by cluster ID and branch ID. | `tdc db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"` |
| `delete-db-cluster-branch` | Deletes one branch. Supports `--dry-run`. | `tdc db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"` |
| `create-db-sql-users` | Idempotently creates or repairs read-only, read-write, and admin users for one cluster. | `tdc db create-db-sql-users --db-cluster-id "<cluster-id>"` |
| `format-db-connection-string` | Formats stored SQL credentials as a MySQL URI, JDBC, Go, SQLAlchemy, or environment output. | `tdc db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env` |
| `execute-sql-statement` | Executes exactly one statement using read-write by default or an explicit SQL role. | `tdc db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1"` |

## Prerequisites

- Configure tdc with `tdc configure`.
- Ensure the API key can manage Starter clusters in the selected project.
- Use synthetic names in automation so cleanup can identify only resources created by that run.

## Manage clusters

Preview and create a Starter cluster:

```bash
tdc db create-db-cluster \
  --db-cluster-name demo-cluster \
  --dry-run

tdc db create-db-cluster \
  --db-cluster-name demo-cluster
```

The configured virtual project is used unless you provide `--project-id`. `--db-cluster-type` is optional and defaults to `starter`; the only accepted explicit value is `starter`. `--monthly-spending-limit-usd-cents` is optional; setting it can require a payment method.

List and filter clusters:

```bash
tdc db list-db-clusters
tdc db list-db-clusters --page-size 20 --order-by "createTime desc"
tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
```

The list command also accepts `--page-token`, `--filter`, and `--skip`.

Describe and update a cluster:

```bash
tdc db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --view FULL

tdc db update-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-name demo-cluster-renamed
```

An update must include a new name or spending limit. Preview mutating commands with `--dry-run`.

Delete a cluster:

```bash
tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run

tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --wait
```

tdc resolves the cluster name internally; no name-confirmation flag is required. Without `--wait`, delete returns after TiDB Cloud accepts the asynchronous request. The wait flag waits up to 12 minutes and returns when the cluster is `DELETED` or no longer accessible.

## Manage branches

Create and list branches:

```bash
tdc db create-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-name development \
  --wait

tdc db list-db-cluster-branches \
  --db-cluster-id "<cluster-id>" \
  --page-size 20
```

Use `--page-token` to continue a paginated branch list. Without `--wait`, branch creation returns after the request is accepted. The wait flag waits up to five minutes for `ACTIVE`.

Describe and delete a branch:

```bash
tdc db describe-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>" \
  --view FULL

tdc db delete-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>"
```

Create and delete support `--dry-run`.

## Create SQL users

Create or repair the three tdc-managed SQL roles:

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

The operation is idempotent. It reuses stable role names and stores generated credentials under `~/.tdc/db_users/<cluster-id>/credentials`. It creates:

- `read_only`;
- `read_write`;
- `admin`.

Preview the operation without changing users:

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

## Format connection strings

Read-write is the default, but explicit role selection is recommended:

```bash
tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --format mysql-uri

tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --format env \
  --env-prefix TIDB_

tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --format jdbc
```

Supported formats are `mysql-uri`, `jdbc`, `go-sql-driver`, `sqlalchemy`, and `env`. With `env`, `--env-include-database-url` adds a URL variable and `--env-database-url-name` changes its name.

> **Warning:**
>
> Connection strings contain credentials. Do not write them to logs, tickets, or source control.

## Execute SQL

Each invocation accepts exactly one SQL statement. Use an explicit role:

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database app \
  --sql "SELECT COUNT(*) AS row_count FROM messages" \
  --output text

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello')"

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS app"
```

The default `--transport https` sends the SQL request over HTTPS without a persistent database connection. Use `--transport mysql` as an explicit compatibility fallback; it opens a connection for the command and closes it afterward.

## What's next

- [Query SQL with Explicit Roles](/ai/tdc/reference/tdc-query-sql-with-roles-example.md)
- [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)
