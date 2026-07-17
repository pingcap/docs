---
title: Query TiDB Cloud Starter with Explicit SQL Roles
summary: Prepare tdc-managed SQL users and run read-only, read-write, and admin statements with clear privilege intent.
---

# Query TiDB Cloud Starter with Explicit SQL Roles

This example lets an agent perform schema, data, and verification work while making the required privilege level explicit for every statement.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The agent problem

An agent that can inspect data often also needs to apply a migration or update a row. Giving it one administrator connection for the complete task is convenient, but a mistaken statement during an inspection step then has the authority to change or delete data. Giving it only a read-only connection prevents legitimate write and schema work.

## Why one native database connection is not enough

TiDB supports SQL privileges, but a conventional client session uses the privileges of the one credential used to connect. Users must create, store, and switch among credentials themselves, and an agent can silently keep using an overly privileged connection across task phases.

## How tdc changes the workflow

`tdc db create-db-sql-users` creates stable read-only, read-write, and admin identities and stores their credentials locally. Each `execute-sql-statement` invocation selects one role explicitly, uses the corresponding credential, and executes one statement. The agent can therefore use admin for schema changes, read-write for data changes, and read-only for verification without handling passwords directly.

## Prerequisites

- Configure tdc.
- Select an active Starter cluster ID.

## Step 1. Prepare users

```bash
tdc db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

The command is idempotent and creates or repairs `read_only`, `read_write`, and `admin` credentials.

## Step 2. Use admin for schema changes

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS role_demo"

tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --database role_demo \
  --sql "CREATE TABLE IF NOT EXISTS messages (id BIGINT PRIMARY KEY, body VARCHAR(255))"
```

## Step 3. Use read-write for data changes

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database role_demo \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello') ON DUPLICATE KEY UPDATE body = VALUES(body)"
```

## Step 4. Use read-only for verification

```bash
tdc db execute-sql-statement \
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
tdc db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --format env \
  --env-include-database-url > .env.tidb
```

Do not commit `.env.tidb`.

## Cleanup

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "DROP DATABASE role_demo"

rm -f .env.tidb
```

## Security notes

- Use the least privileged explicit role for each statement.
- tdc accepts one SQL statement per invocation.
- HTTPS is the default transport; `--transport mysql` is an explicit fallback.
- Connection strings and environment output contain credentials.

## What's next

- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
