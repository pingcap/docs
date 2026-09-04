---
title: TiDB Cloud Starter CLI Command Reference
summary: Reference every `ti db` command for Starter clusters, branches, SQL users, connection strings, and SQL execution.
---

# TiDB Cloud Starter CLI Command Reference

Use `ti db` to manage TiDB Cloud Starter clusters, branches, and SQL access. The TiDB Cloud CLI validates the cluster service plan before every cluster-scoped operation and rejects Essential or unverifiable clusters before continuing.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
ti db
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
| `create-db-cluster` | Creates a Starter cluster. Requires `--db-cluster-type starter` and `--db-cluster-name`. Use `--wait` for an `ACTIVE` result. | `ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait` |
| `list-db-clusters` | Lists Starter clusters in the effective region. Requires `--db-cluster-type starter` and supports pagination, filtering, ordering, and queries. | `ti db list-db-clusters --db-cluster-type starter --query 'clusters[].{id:id,name:display_name}'` |
| `describe-db-cluster` | Reads one cluster by `--db-cluster-id`; `--view FULL` requests expanded fields. | `ti db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL` |
| `update-db-cluster` | Changes the name or monthly spending limit of one cluster. Supports `--dry-run`. | `ti db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2` |
| `delete-db-cluster` | Deletes one cluster by ID. Use `--wait` to wait until deletion is observable. | `ti db delete-db-cluster --db-cluster-id "<cluster-id>" --wait` |
| `create-db-cluster-branch` | Creates a branch from a cluster. Requires cluster ID and branch name; supports `--wait`. | `ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait` |
| `list-db-cluster-branches` | Lists branches for one cluster with pagination. | `ti db list-db-cluster-branches --db-cluster-id "<cluster-id>" --output text` |
| `describe-db-cluster-branch` | Reads one branch by cluster ID and branch ID. | `ti db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"` |
| `delete-db-cluster-branch` | Deletes one branch. Supports `--dry-run`. | `ti db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"` |
| `create-db-sql-users` | Idempotently creates or repairs read-only, read-write, and admin users for one cluster. | `ti db create-db-sql-users --db-cluster-id "<cluster-id>"` |
| `format-db-connection-string` | Formats stored SQL credentials as a MySQL URI, JDBC, Go, SQLAlchemy, or environment output. | `ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env` |
| `execute-sql-statement` | Executes exactly one statement using read-write by default or an explicit SQL role. | `ti db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1"` |

## Prerequisites

- Configure `ti` with `ti configure`.
- Ensure the API key can manage Starter clusters in the selected project.
- Use synthetic names in automation so cleanup can identify only resources created by that run.

## Manage clusters

Preview and create a Starter cluster:

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name demo-cluster \
  --dry-run

ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name demo-cluster
```

The TiDB Cloud CLI omits project selection and lets TiDB Cloud select its server-side default project. Any project metadata in the response remains visible. `--db-cluster-type starter` is required for cluster creation and listing; no type is inferred. `--monthly-spending-limit-usd-cents` is optional; setting it can require a payment method.

List and filter clusters:

```bash
ti db list-db-clusters --db-cluster-type starter
ti db list-db-clusters --db-cluster-type starter --page-size 20 --order-by "createTime desc"
ti db list-db-clusters --db-cluster-type starter --query 'clusters[].{id:id,name:display_name,state:state}'
ti --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
```

The list command also accepts `--page-token` and `--filter`. It always scopes the API request to the effective region, which resolves from global `--region`, then `TI_REGION_CODE`, then the selected profile. The shared TiDB Cloud API can return multiple service plans or unverifiable resources, so the TiDB Cloud CLI scans upstream pages and incrementally fills a ti result page with verified Starter clusters in that region. Its opaque `next_page_token` binds the profile, type, region, filter, and ordering; it omits `total_size`, because the server total can include clusters outside the verified result. A user `--filter` is combined with the mandatory region filter and cannot expand the result to another region.

Describe and update a cluster:

```bash
ti db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --view FULL

ti db update-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-name demo-cluster-renamed
```

An update must include a new name or spending limit. Preview mutating commands with `--dry-run`.

Delete a cluster:

```bash
ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run

ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --wait
```

`ti` resolves the cluster name internally; no name-confirmation flag is required. Without `--wait`, delete returns after TiDB Cloud accepts the asynchronous request. The wait flag waits up to 12 minutes and returns when the cluster is `DELETED` or no longer accessible.

## Manage branches

Every branch command verifies that the parent cluster is Starter before calling a branch endpoint.

Create and list branches:

```bash
ti db create-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-name development \
  --wait

ti db list-db-cluster-branches \
  --db-cluster-id "<cluster-id>" \
  --page-size 20
```

Use `--page-token` to continue a paginated branch list. Without `--wait`, branch creation returns after the request is accepted. The wait flag waits up to five minutes for `ACTIVE`.

Describe and delete a branch:

```bash
ti db describe-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>" \
  --view FULL

ti db delete-db-cluster-branch \
  --db-cluster-id "<cluster-id>" \
  --db-cluster-branch-id "<branch-id>"
```

Create and delete support `--dry-run`.

## Create SQL users

SQL access commands verify that the target cluster is Starter before reading or writing local SQL credentials, calling SQL-user APIs, or contacting a SQL endpoint.

Create or repair the three TiDB Cloud CLI-managed SQL roles:

```bash
ti db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

The operation is idempotent. It reuses stable role names and stores generated credentials under `~/.ti/db_users/<cluster-id>/credentials`. It creates:

- `read_only`;
- `read_write`;
- `admin`.

Preview the operation without changing users:

```bash
ti db create-db-sql-users \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

## Format connection strings

Read-write is the default, but explicit role selection is recommended:

```bash
ti db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --format mysql-uri

ti db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --format env \
  --env-prefix TIDB_

ti db format-db-connection-string \
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
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database app \
  --sql "SELECT COUNT(*) AS row_count FROM messages" \
  --output text

ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database app \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello')"

ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS app"
```

The default `--transport https` sends the SQL request over HTTPS without a persistent database connection. Use `--transport mysql` as an explicit compatibility fallback; it opens a connection for the command and closes it afterward.

## What's next

- [Query SQL with Explicit Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md)
- [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
