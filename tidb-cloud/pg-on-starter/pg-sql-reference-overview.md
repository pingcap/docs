---
title: Explore PostgreSQL SQL with TiDB Cloud
summary: Learn about the basic PostgreSQL SQL statements supported by PostgreSQL-compatible TiDB Cloud Starter.
---

# Explore PostgreSQL SQL with TiDB Cloud

PostgreSQL-compatible {{{ .starter }}} supports the PostgreSQL wire protocol and common PostgreSQL SQL syntax. You can use most PostgreSQL clients, drivers, and ORMs to work with your instance.

This page walks you through basic PostgreSQL SQL operations, including DDL, DML, DQL, DCL, and transaction control.

For PostgreSQL features that are unsupported or behave differently, see [PostgreSQL Compatibility](/tidb-cloud/pg-on-starter/postgresql-compatibility.md).

## Category

SQL statements can be grouped into the following categories according to their functions:

- **DDL (Data Definition Language)**: defines and manages database objects, including databases, schemas, tables, views, indexes, sequences, and types.
- **DML (Data Manipulation Language)**: inserts, updates, and deletes table data.
- **DQL (Data Query Language)**: queries data using `SELECT`, filtering, joins, aggregation, subqueries, common table expressions (CTEs), and other query features.
- **DCL (Data Control Language)**: manages database roles and privileges.
- **Transaction control**: manages transactions using statements such as `BEGIN`, `COMMIT`, `ROLLBACK`, and `SAVEPOINT`.

Common DDL operations include creating, modifying, and deleting objects. The corresponding commands are `CREATE`, `ALTER`, and `DROP`.

## Show, create, and drop a database

To list databases, query the `pg_database` system catalog:

{{< copyable "sql" >}}

```sql
SELECT datname
FROM pg_database
ORDER BY datname;
```

To create a database named `samp_db`, use the `CREATE DATABASE` statement:

{{< copyable "sql" >}}

```sql
CREATE DATABASE samp_db;
```

To connect to the database when using `psql`, use the `\connect` command:

```text
\connect samp_db
```

> **Note:**
>
> `\connect` is a `psql` client command, not a SQL statement.

To delete a database, first connect to another database:

```text
\connect postgres
```

Then use the `DROP DATABASE` statement:

{{< copyable "sql" >}}

```sql
DROP DATABASE samp_db;
```

## Create, show, and drop a table

To create a table, use the `CREATE TABLE` statement.

For example, create a table named `person`:

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE
);
```

To list tables in the `public` schema:

{{< copyable "sql" >}}

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

To view the columns of the `person` table:

{{< copyable "sql" >}}

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'person'
ORDER BY ordinal_position;
```

To delete the table, use the `DROP TABLE` statement:

{{< copyable "sql" >}}

```sql
DROP TABLE person;
```

## Create, show, and drop an index

Indexes can improve query performance on indexed columns.

To create an index on the `name` column:

{{< copyable "sql" >}}

```sql
CREATE INDEX person_name_idx ON person (name);
```

To create a unique index:

{{< copyable "sql" >}}

```sql
CREATE UNIQUE INDEX person_name_unique_idx ON person (name);
```

To list the indexes on the `person` table:

{{< copyable "sql" >}}

```sql
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'person'
ORDER BY indexname;
```

To delete an index, use the `DROP INDEX` statement:

{{< copyable "sql" >}}

```sql
DROP INDEX person_name_idx;
```

For supported PostgreSQL index methods and compatibility differences, see [PostgreSQL Compatibility](/tidb-cloud/pg-on-starter/postgresql-compatibility.md).

## Insert, update, and delete data

Common DML operations use the `INSERT`, `UPDATE`, and `DELETE` statements.

To insert a row into the `person` table:

{{< copyable "sql" >}}

```sql
INSERT INTO person (name, birthday)
VALUES ('Tom', DATE '1990-09-12');
```

To insert multiple rows:

{{< copyable "sql" >}}

```sql
INSERT INTO person (name, birthday)
VALUES
    ('Alice', DATE '1992-05-01'),
    ('Bob', DATE '1993-08-08');
```

PostgreSQL-compatible {{{ .starter }}} supports `RETURNING`. For example, return the generated ID after inserting a row:

{{< copyable "sql" >}}

```sql
INSERT INTO person (name, birthday)
VALUES ('Carol', DATE '1994-03-15')
RETURNING id, name;
```

To update a row:

{{< copyable "sql" >}}

```sql
UPDATE person
SET birthday = DATE '1990-10-12'
WHERE name = 'Tom';
```

To delete a row:

{{< copyable "sql" >}}

```sql
DELETE FROM person
WHERE name = 'Bob';
```

> **Note:**
>
> `UPDATE` and `DELETE` statements without a `WHERE` clause operate on all rows in the table.

### Upsert data

Use `INSERT ... ON CONFLICT` to insert a row or handle a uniqueness conflict.

For example:

{{< copyable "sql" >}}

```sql
CREATE TABLE account (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT
);

INSERT INTO account (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

## Query data

Use the `SELECT` statement to query data.

To query all columns:

{{< copyable "sql" >}}

```sql
SELECT *
FROM person;
```

To query specific columns:

{{< copyable "sql" >}}

```sql
SELECT id, name
FROM person;
```

Use a `WHERE` clause to filter rows:

{{< copyable "sql" >}}

```sql
SELECT id, name, birthday
FROM person
WHERE birthday >= DATE '1992-01-01'
ORDER BY birthday;
```

PostgreSQL-compatible {{{ .starter }}} also supports common PostgreSQL query features such as joins, subqueries, CTEs, recursive CTEs, window functions, and set operations.

For example, use a CTE to filter data:

{{< copyable "sql" >}}

```sql
WITH recent_people AS (
    SELECT id, name, birthday
    FROM person
    WHERE birthday >= DATE '1992-01-01'
)
SELECT *
FROM recent_people
ORDER BY birthday;
```

## Manage transactions

Use `BEGIN` and `COMMIT` to execute multiple statements in a transaction:

{{< copyable "sql" >}}

```sql
BEGIN;

UPDATE account
SET name = 'Alice Chen'
WHERE email = 'alice@example.com';

COMMIT;
```

To discard changes in the current transaction, use `ROLLBACK`:

{{< copyable "sql" >}}

```sql
BEGIN;

DELETE FROM account
WHERE email = 'alice@example.com';

ROLLBACK;
```

Savepoints are also supported:

{{< copyable "sql" >}}

```sql
BEGIN;

UPDATE account
SET name = 'Alice'
WHERE email = 'alice@example.com';

SAVEPOINT before_second_update;

UPDATE account
SET name = 'Alice Updated'
WHERE email = 'alice@example.com';

ROLLBACK TO SAVEPOINT before_second_update;

COMMIT;
```

For supported transaction isolation levels and PostgreSQL compatibility differences, see [PostgreSQL Compatibility](/tidb-cloud/pg-on-starter/postgresql-compatibility.md).

## Create, authorize, and delete a database user

DCL statements are used to manage database roles and privileges.

To create a role that can log in:

{{< copyable "sql" >}}

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

Grant the role access to the `public` schema and permission to query the `person` table:

{{< copyable "sql" >}}

```sql
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON person TO app_user;
```

To check table privileges granted to the role:

{{< copyable "sql" >}}

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'app_user'
ORDER BY table_schema, table_name, privilege_type;
```

To revoke the privileges:

{{< copyable "sql" >}}

```sql
REVOKE SELECT ON person FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

To delete the role:

{{< copyable "sql" >}}

```sql
DROP ROLE app_user;
```
