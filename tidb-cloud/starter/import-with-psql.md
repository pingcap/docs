---
title: Migrate from PostgreSQL to PostgreSQL-compatible TiDB Cloud Starter
summary: Learn how to migrate schema and data from PostgreSQL to a PostgreSQL-compatible TiDB Cloud Starter instance using `psql` and `\copy`.
---

# Migrate from PostgreSQL to PostgreSQL-compatible TiDB Cloud Starter

This document describes how to migrate an existing PostgreSQL database to a PostgreSQL-compatible {{{ .starter }}} instance.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in public preview. The preview is intended for development and evaluation and is not recommended for production workloads.
>
> During the public preview, PostgreSQL-compatible {{{ .starter }}} supports migration using `psql` and `\copy`. This guide uses `pg_dump` to export schema and data from the source PostgreSQL database, and uses `psql` and `\copy` to import them into the target instance.

The overall migration procedure is as follows:

1. Prepare the source database, target instance, and migration tools.
2. Check the source PostgreSQL database for compatibility.
3. Export and review the source schema.
4. Import the schema to the PostgreSQL-compatible {{{ .starter }}} instance.
5. Migrate the data using `psql` and `\copy`.
6. Verify the migrated schema and data.

## Prerequisites

Before migration, make sure that you have the following:

- Access to the source PostgreSQL database.
- A PostgreSQL-compatible {{{ .starter }}} instance.
- The connection string of the target instance. To get the connection string, open the target instance in the TiDB Cloud console, click **Connect**, and select **PostgreSQL CLI**.
- Network access from the machine where you run the migration commands to both the source PostgreSQL database and the target instance.

Before migrating, review [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md) and [PostgreSQL Extensions](/tidb-cloud/starter/pg-extensions-overview.md).

## Prepare tools

Install the following PostgreSQL client tools on the machine where you perform the migration:

- `pg_dump`: exports schema and data from the source PostgreSQL database.
- `psql`: imports schema and data into the PostgreSQL-compatible {{{ .starter }}} instance.

It is recommended to use a `pg_dump` version that is from the same major PostgreSQL release as the source PostgreSQL database.

## Check PostgreSQL compatibility

PostgreSQL-compatible {{{ .starter }}} supports common PostgreSQL workloads, but some PostgreSQL features are unsupported or behave differently. Before migration, check whether your source database depends on these features.

### Check database roles and permissions

If your application uses row-level security (RLS), run the following query on the source PostgreSQL database to identify roles referenced by RLS policies:

```sql
SELECT DISTINCT r AS policy_role
FROM pg_policies, unnest(roles) AS r
WHERE r <> 'public';
```

Make sure the required application roles are created in the target instance before importing the schema.

### Check unsupported schema features

Run the following queries against the source PostgreSQL database:

```sql
-- Table partitioning
SELECT count(*) AS partitioned_tables
FROM pg_partitioned_table;

-- Table inheritance
SELECT count(*) AS inherited_tables
FROM pg_inherits;

-- Foreign data wrappers
SELECT count(*) AS fdw_servers
FROM pg_foreign_server;

-- Logical replication publications
SELECT count(*) AS publications
FROM pg_publication;
```

If any of these queries return a non-zero count, review the affected objects before migration.

PostgreSQL-compatible {{{ .starter }}} does not support table partitioning, table inheritance, foreign data wrappers, or logical replication.

### Check deferred foreign-key constraints

PostgreSQL-compatible {{{ .starter }}} does not support deferred foreign-key enforcement. Foreign-key constraints declared as `DEFERRABLE` are enforced immediately.

Before migration, run the following query against the source PostgreSQL database to identify deferrable foreign-key constraints:

```sql
SELECT
    conrelid::regclass AS table_name,
    conname AS constraint_name
FROM pg_constraint
WHERE contype = 'f'
  AND condeferrable;
```

Review any application transactions that depend on deferred foreign-key enforcement before migrating.

### Check extensions

Run the following query to list the extensions installed on the source database:

```sql
SELECT extname
FROM pg_extension
ORDER BY extname;
```

Compare the result with [PostgreSQL Extensions](/tidb-cloud/starter/pg-extensions-overview.md).

Custom or third-party PostgreSQL extensions cannot be installed on PostgreSQL-compatible {{{ .starter }}}. Remove or replace dependencies on unsupported extensions before migration.

### Check PL/pgSQL

PostgreSQL-compatible {{{ .starter }}} supports common PL/pgSQL constructs, but some constructs are not supported.

The following query can help identify PL/pgSQL routines that might require changes:

```sql
SELECT proname, prosrc
FROM pg_proc
WHERE prolang = (SELECT oid FROM pg_language WHERE lanname = 'plpgsql')
  AND (
    prosrc ~* '\m(WHILE|FOREACH|CURSOR|REFCURSOR)\M'
    OR prosrc ~* '\mEXCEPTION\s+WHEN\M'
    OR prosrc ~* '\mBEGIN\M.*\mBEGIN\M'
  );
```

Review any matching routines before migration. In particular:

- `WHILE` and `FOREACH` loops are not supported.
- Cursor and `REFCURSOR` operations are not supported.
- Exception handling with `BEGIN ... EXCEPTION` is supported only in `DO` blocks.
- Nested procedural blocks are supported only in `DO` blocks.

For more compatibility details, see [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md).

## Migrate a full database

For a PostgreSQL database migration, import the schema before importing the data.

> **Important:**
>
> Do not import a standard full `pg_dump` file into PostgreSQL-compatible {{{ .starter }}} in a single pass. A standard PostgreSQL dump can add primary keys and other constraints after table data is loaded, while PostgreSQL-compatible {{{ .starter }}} might not be able to add a primary key to a non-empty table.
>
> Import the schema first while the tables are empty, and then import the data.
>
> This migration method does not support zero-downtime migration or logical replication. Plan a maintenance window for the final migration and application cutover.
>
> For the final migration, stop all writes and schema changes to the source database and wait for any in-progress operations to complete before exporting the schema and data. Keep the source database unchanged until migration validation and application cutover are complete.
>
> You can perform a trial migration without stopping source writes, but changes made after the export begins might not be included in the target database.

### Step 1: Export the schema

Export the source schema in plain SQL format:

```shell
pg_dump \
  --schema-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  > schema.sql
```

Use the default plain SQL format. Do not use the custom (`-Fc`) or directory (`-Fd`) format for this workflow.

### Step 2: Review and update the schema

Review `schema.sql` for unsupported PostgreSQL features before importing it.

For example:

```shell
# Extensions
grep -i "CREATE EXTENSION" schema.sql

# Table partitioning
grep -Ei "PARTITION BY|PARTITION OF" schema.sql

# Table inheritance
grep -i "INHERITS" schema.sql

# Foreign data wrappers
grep -Ei "CREATE SERVER|CREATE FOREIGN TABLE" schema.sql

# Replication
grep -Ei "CREATE PUBLICATION|CREATE SUBSCRIPTION" schema.sql

# Rules
grep -i "CREATE RULE" schema.sql
```

Remove or rewrite unsupported statements before importing the schema.

Also review the schema for unsupported data types, index access methods, PL/pgSQL constructs, and extensions. For more information, see [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md).

#### Row-level security

Keep the row-level security (RLS) statements in the exported schema, including `ENABLE ROW LEVEL SECURITY`, `FORCE ROW LEVEL SECURITY`, and `CREATE POLICY`.

Before importing data, make sure the role in `<TARGET_DATABASE_URL>` has the required table privileges. If RLS policies apply to this role, each imported row must satisfy the target table's policies. Otherwise, `COPY FROM STDIN` fails with `new row violates row-level security policy`.

If you need to import rows that these policies would reject, ask your database administrator to perform the import using a separate migration role authorized to bypass RLS. Do not grant `BYPASSRLS` to application roles for the migration. Remove any privileges granted only for the migration after it is complete.

The `pg_dump` utility does not export database roles. If an RLS policy references a specific role, create that role in the target instance before importing the schema.

For example:

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "CREATE ROLE app_user LOGIN PASSWORD '<PASSWORD>'"
```

The `--no-owner` option omits object ownership statements, and `--no-privileges` omits `GRANT` and `REVOKE` statements.

After importing the schema and data, restore the required schema, table, and sequence privileges, as well as role memberships, for the application roles. For more information, see [PostgreSQL Authentication and Roles](/tidb-cloud/starter/pg-auth-roles.md).

#### SERIAL and identity columns

A schema generated by `pg_dump` can contain PostgreSQL-specific forms for `SERIAL` defaults and identity columns that require adjustment before import.

For `SERIAL` or `BIGSERIAL` defaults, remove the `::regclass` cast from `nextval()` expressions. For example:

```sql
-- PostgreSQL dump output
DEFAULT nextval('public.users_id_seq'::regclass)

-- Compatible form
DEFAULT nextval('public.users_id_seq')
```

If the dump contains identity columns added through `ALTER TABLE ... ALTER COLUMN ... ADD GENERATED ... AS IDENTITY`, rewrite them to use a sequence and a `DEFAULT nextval(...)` expression before importing the schema.

### Step 3: Import the schema

Import the reviewed schema into the target PostgreSQL-compatible {{{ .starter }}} instance using `psql`:

```shell
psql \
  "<TARGET_DATABASE_URL>" \
  -v ON_ERROR_STOP=1 \
  -f schema.sql
```

The `ON_ERROR_STOP=1` option causes `psql` to stop when an import error occurs, making it easier to identify and fix unsupported statements.

### Step 4: Migrate the data

After the schema is successfully imported, stream the data from the source PostgreSQL database to the target instance:

```shell
pg_dump \
  --data-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  | psql "<TARGET_DATABASE_URL>" -v ON_ERROR_STOP=1
```

By default, the plain `pg_dump` data stream uses PostgreSQL `COPY` statements. When the stream is piped to `psql`, the `COPY ... FROM stdin` statements import data into PostgreSQL-compatible {{{ .starter }}} through the PostgreSQL wire protocol.

PostgreSQL-compatible {{{ .starter }}} supports `COPY` data transfer in text and CSV formats. Binary `COPY` is not supported.

### Migrate individual tables using `\copy`

You can also migrate individual tables using `psql` and `\copy`.

To export a table from the source PostgreSQL database:

```shell
psql "<SOURCE_DATABASE_URL>" \
  -c "\copy public.users TO 'users.csv' WITH (FORMAT csv, HEADER)"
```

To import the table into the target instance:

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "\copy public.users FROM 'users.csv' WITH (FORMAT csv, HEADER)"
```

Make sure that the target table exists before importing the data.

#### Restore sequence values

When migrating individual tables using `\copy`, sequence values are not transferred automatically.

If your table uses `SERIAL`, `BIGSERIAL`, or an explicitly created sequence, restore the sequence state after importing the data to prevent duplicate key errors during subsequent inserts.

While source writes are stopped, run the following query against the source PostgreSQL database to retrieve the sequence state:

```sql
SELECT last_value, is_called
FROM public.users_id_seq;
```

After importing the table data, restore the sequence state in the target instance using `setval()`.

For example, if the source sequence has `last_value = 3` and `is_called = true`, run:

```sql
SELECT setval('public.users_id_seq', 3, true);
```

Replace the values with the actual `last_value` and `is_called` values retrieved from the source database.

Repeat this process for each sequence associated with the migrated tables.

> **Note:**
>
> The SQL-level `COPY (SELECT ...) TO STDOUT` syntax is not supported. Use the table form of `\copy` instead.

## Verify the migrated data

After the migration is complete, verify the target database before directing application traffic to it.

### Verify the schema

Use `psql` to inspect the migrated schema and verify that the required tables, indexes, constraints, sequences, functions, and other objects exist.

For example:

```shell
psql "<TARGET_DATABASE_URL>" -c "\dt"
```

### Verify row counts

Compare row counts between the source and target databases.

For example:

```sql
SELECT count(*) FROM users;
SELECT count(*) FROM orders;
```

### Verify sequences

If your application uses sequences, `SERIAL`, or `BIGSERIAL`, verify that sequence values are consistent with the imported data.

For example:

```sql
SELECT last_value FROM users_id_seq;
SELECT max(id) FROM users;
```

### Verify your application

Connect your application to the PostgreSQL-compatible {{{ .starter }}} instance and run your application test suite.

Pay particular attention to application logic that depends on PostgreSQL features that are unsupported or behave differently. For more information, see [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md).

## Limitations

Keep the following limitations in mind when planning a migration:

- During the public preview, PostgreSQL-compatible {{{ .starter }}} supports migration using `psql` with `pg_dump` `COPY` data streams and table-form `\copy`.
- PostgreSQL logical replication and streaming replication are not supported. For the final migration, stop source writes before exporting the schema and data, and keep them paused until migration validation and application cutover are complete.
- The `COPY` protocol supports text and CSV formats. Binary `COPY` is not supported.
- The SQL-level `COPY (SELECT ...) TO STDOUT` syntax is not supported. For individual-table migration, use the table form of `\copy`.
- Some PostgreSQL schema objects, data types, index access methods, extensions, and PL/pgSQL constructs are unsupported or behave differently. Review [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md) before migration.
- Migrated text data must use valid UTF-8 encoding.
