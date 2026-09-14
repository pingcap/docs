---
title: Query TiDB Cloud Starter with Explicit SQL Roles
summary: Prepare TiDB Cloud CLI-managed SQL users and run read-only, read-write, and admin statements with explicit privilege intent.
---

# Query TiDB Cloud Starter with Explicit SQL Roles

This workflow prepares three SQL roles once and then explicitly selects the least-privileged role for each statement. Use it for interactive or automated schema, data, and verification work without handling database passwords in every command.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

A conventional database connection uses one credential and retains that credential's privileges for the session. By contrast, `ti db create-db-sql-users` creates three stable identities and stores their credentials locally. Each `execute-sql-statement` invocation selects one identity and executes one statement, so an inspection step does not need to retain write or administrator privileges.

| Role | Use it for |
| --- | --- |
| `admin` | Schema changes and privilege management |
| `read-write` | Application data changes |
| `read-only` | Queries and verification |

## Prerequisites

- Configure `ti`.
- Select an active TiDB Cloud Starter instance ID.

## Step 1. Prepare SQL users

```bash
ti db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

The command is idempotent and creates or repairs `read_only`, `read_write`, and `admin` credentials.

## Step 2. Use admin for schema changes

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS role_demo"

ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --database role_demo \
  --sql "CREATE TABLE IF NOT EXISTS messages (id BIGINT PRIMARY KEY, body VARCHAR(255))"
```

## Step 3. Use read-write for data changes

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database role_demo \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello') ON DUPLICATE KEY UPDATE body = VALUES(body)"
```

## Step 4. Use read-only for verification

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --sql "SELECT id, body FROM messages ORDER BY id" \
  --output text
```

Expected result contains ID `1` and body `hello`.

## Step 5. Format a connection environment

Write the output directly to a protected local file instead of displaying it:

```bash
umask 077
ti db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --format env \
  --env-include-database-url > .env.tidb
```

Do not commit `.env.tidb`.

With `--format env`, the command writes separate `TIDB_` connection variables such as `TIDB_HOST`, `TIDB_USER`, and `TIDB_PASSWORD`. The `--env-include-database-url` option also adds a `DATABASE_URL` value for applications that accept a single MySQL connection URL.

## Cleanup

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "DROP DATABASE role_demo"

rm -f .env.tidb
```

## Security notes

- Use the least privileged explicit role for each statement.
- `ti` accepts one SQL statement per invocation.
- HTTPS is the default SQL execution transport. To open a direct TLS MySQL connection instead, specify `--transport mysql`; the CLI does not switch transports automatically.
- Connection strings and environment output contain credentials.

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
