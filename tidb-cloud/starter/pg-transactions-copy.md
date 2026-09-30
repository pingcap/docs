---
title: PostgreSQL Transactions and COPY
summary: Learn about transaction control and COPY support in PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Transactions and COPY

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL transaction control, savepoints, common transaction isolation levels, and the PostgreSQL `COPY` protocol for bulk data transfer.

## Transaction control

Use `BEGIN` to start an explicit transaction and `COMMIT` to persist the changes:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

Use `ROLLBACK` to discard all changes in the current transaction:

```sql
BEGIN;

DELETE FROM orders
WHERE id = 100;

ROLLBACK;
```

## Autocommit

Statements executed outside an explicit `BEGIN` block run in autocommit mode.

Each statement runs in its own transaction and is committed automatically if it succeeds. If the statement fails, the transaction is rolled back.

## Savepoints

Use savepoints to roll back part of a transaction without discarding the entire transaction.

For example:

```sql
BEGIN;

INSERT INTO users (name)
VALUES ('Alice');

SAVEPOINT sp1;

INSERT INTO users (name)
VALUES ('Bob');

ROLLBACK TO SAVEPOINT sp1;

RELEASE SAVEPOINT sp1;

COMMIT;
```

In this example, the insert for `Bob` is rolled back, while the insert for `Alice` is committed.

Savepoint behavior follows PostgreSQL semantics:

- Duplicate savepoint names are allowed. The most recently created savepoint with that name is used.
- `ROLLBACK TO SAVEPOINT` rolls back changes after the savepoint and keeps the savepoint available for reuse.
- `RELEASE SAVEPOINT` removes the specified savepoint and savepoints created after it.

## Transaction isolation

The default transaction isolation level is `READ COMMITTED`.

The following isolation levels can be requested:

| Isolation level | Behavior |
| --- | --- |
| `READ COMMITTED` | Default. Each statement sees rows committed before that statement starts. |
| `READ UNCOMMITTED` | Behaves as `READ COMMITTED`. |
| `REPEATABLE READ` | Uses one snapshot for the lifetime of the transaction. |
| `SERIALIZABLE` | PostgreSQL Serializable Snapshot Isolation is not implemented. Over the PostgreSQL wire protocol, the transaction is downgraded to `REPEATABLE READ`. |

Start a transaction at a specific isolation level:

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;

SELECT *
FROM accounts;

COMMIT;
```

You can check the effective isolation level:

```sql
SHOW transaction_isolation;
```

> **Note:**
>
> If `SERIALIZABLE` is requested over the PostgreSQL wire protocol, PostgreSQL-compatible {{{ .starter }}} uses `REPEATABLE READ` instead. Applications that require PostgreSQL Serializable Snapshot Isolation should be reviewed before migration. For more information, see [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md).

## Read-only transactions

Use `BEGIN READ ONLY` to start a read-only transaction:

```sql
BEGIN READ ONLY;

SELECT *
FROM users;

COMMIT;
```

You can also set a transaction to read-only after `BEGIN`:

```sql
BEGIN;

SET TRANSACTION READ ONLY;

SELECT *
FROM users;

COMMIT;
```

DML and DDL writes are rejected in a read-only transaction.

You can also set the default mode for new transactions in the current session:

```sql
SET default_transaction_read_only = on;
```

## Sequence behavior in transactions

Sequence operations such as `nextval()` are non-transactional, matching PostgreSQL behavior.

If a transaction calls `nextval()` and later rolls back, the generated sequence value is not reused.

For example:

```sql
BEGIN;

SELECT nextval('order_seq');

ROLLBACK;
```

The sequence remains advanced after the rollback. Do not rely on sequences for gap-free numbering.

## Failed transaction state

If a statement fails inside an explicit transaction, the transaction enters a failed state.

For example:

```sql
BEGIN;

INSERT INTO users (id, name)
VALUES (1, 'Alice');

-- If a statement fails here, the transaction enters a failed state.

ROLLBACK;
```

After a transaction enters the failed state, either use `ROLLBACK` or roll back to a prior savepoint before continuing with normal SQL operations.

## COPY

The PostgreSQL `COPY` protocol provides efficient bulk data transfer over the PostgreSQL wire protocol.

PostgreSQL-compatible {{{ .starter }}} supports the table form of `COPY` for text and CSV data.

### Import data with `COPY FROM STDIN`

Use `COPY ... FROM STDIN` to stream data from a PostgreSQL client:

```sql
COPY users (name, email)
FROM STDIN
WITH (FORMAT csv);
```

When using `psql`, you can use the `\copy` client command to read a local file and send the data through the PostgreSQL connection:

```text
\copy users (name, email) FROM 'users.csv' WITH (FORMAT csv, HEADER)
```

> **Note:**
>
> `\copy` is a `psql` client command, not a SQL statement.

### Export data with COPY

The table form of `COPY ... TO STDOUT` can be used to stream table data to the client.

For example:

```sql
COPY users (id, name, email)
TO STDOUT
WITH (FORMAT csv, HEADER);
```

When using `psql`, you can use `\copy` to write table data to a local file:

```text
\copy users TO 'users.csv' WITH (FORMAT csv, HEADER)
```

### COPY formats

The following common formats are supported:

| Format | Support |
| --- | --- |
| Text | Supported |
| CSV | Supported |
| Binary | Not supported |

Parquet import is also available through the `parquet` extension. For more information, see [Import Parquet Data](/tidb-cloud/starter/pg-parquet-import.md).

### COPY limitations

Keep the following limitations in mind:

- Use the table form `COPY table_name [(columns)] ...`.
- Binary `COPY` is not supported.
- `COPY (SELECT ...) TO STDOUT` is not supported.
- For local files, use the `psql` `\copy` command so that the file is read by the client and transferred over the PostgreSQL connection.
