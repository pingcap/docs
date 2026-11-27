---
title: Database-Level Read-Only Mode
summary: Learn how to set individual TiDB databases to read-only for migration and validation, and understand write restrictions and privileges.
---

# Database-Level Read-Only Mode

Database-level read-only mode restricts writes to an individual database while keeping ordinary queries available. Use it for migration cutover or validation while other databases remain writable.

<!-- TODO: Confirm the first release that includes database-level read-only mode and the SQL sequence restore fix. -->

New databases are writable. The setting persists across TiDB nodes and restarts. For cluster-wide control, use [`tidb_super_read_only`](/system-variables.md#tidb_super_read_only-new-in-v531) or [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520).

## Prerequisites

- All TiDB nodes must support this feature before you enable it or restore read-only database metadata.
- Changing the setting requires the `ALTER` privilege on the database.
- System databases, including `mysql`, `sys`, `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, and `METRICS_SCHEMA`, cannot be set to read-only.

## Set and check read-only mode

Create a database and enable read-only mode:

```sql
CREATE DATABASE app;
CREATE TABLE app.orders (id INT PRIMARY KEY);
INSERT INTO app.orders VALUES (1);
ALTER DATABASE app READ ONLY = 1;
```

Queries remain available:

```sql
SELECT * FROM app.orders;
```

Without the bypass privilege, writes fail:

```sql
INSERT INTO app.orders VALUES (2);
```

```text
ERROR 3989 (HY000): Schema 'app' is in read only mode.
```

Check [`INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS`](/information-schema/information-schema-schemata-extensions.md):

```sql
SELECT SCHEMA_NAME, OPTIONS
FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS
WHERE SCHEMA_NAME = 'app';
```

`OPTIONS` is `READ ONLY=1` for a read-only database, or empty for a writable database. [`SHOW CREATE DATABASE app`](/sql-statements/sql-statement-show-create-database.md) also shows `/* READ ONLY = 1 */` for read-only databases.

To restore write access:

```sql
ALTER DATABASE app READ ONLY = 0;
```

`READ ONLY = DEFAULT` also restores write access. For complete syntax, see [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md).

## Transaction behavior

Enabling read-only mode waits for existing transactions that accessed tables in the database to finish, including read transactions on other nodes. New writes are rejected after the flag propagates. Wait for `ALTER DATABASE ... READ ONLY = 1` to complete before treating the transition as finished.

Finish blocking transactions or cancel the DDL using [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md). Failed or canceled transitions roll back the setting. Disabling read-only mode does not require transaction draining.

An older transaction first accessing the database after a state change can fail with error `8028`. Retry the transaction.

## SQL behavior and privileges

Without the bypass privilege, the following restrictions apply:

| Operation | Behavior |
| --- | --- |
| Ordinary `SELECT`, `SHOW`, and `USE` | Allowed. |
| `INSERT`, `REPLACE`, `UPDATE`, `DELETE`, `LOAD DATA`, and `IMPORT INTO` | Rejected for read-only write targets. |
| DDL that changes databases, tables, views, indexes, or sequences | Rejected, except changing `READ ONLY` itself or compacting TiFlash replicas. |
| Locking reads | Rejected when the actual lock target is in a read-only database. |
| `NEXTVAL` and `SETVAL` | Rejected for sequences in a read-only database. |
| Temporary tables | Creation and writes are restricted, including writes to existing local temporary tables. |
| TTL deletion | Cannot delete rows in a read-only database. |

Cross-database checks cover write targets, foreign-key cascades, and both databases in table moves. Reading a read-only database while writing to a writable database is allowed.

Explicitly granting [`RESTRICTED_REPLICA_WRITER_ADMIN`](/privilege-management.md#dynamic-privileges) to a user or active role permits bypassing read-only restrictions. Operation-specific privileges are still required. `SUPER` alone is insufficient. Prepared execution rechecks current bypass privileges and roles.

## Compatibility and limitations

- `READ ONLY` is supported by `ALTER DATABASE`, but not `CREATE DATABASE`. Specify it separately from character set, collation, or placement options.
- Compared with MySQL 8.0, TiDB also restricts local temporary tables and can reject write statements during `PREPARE`. `EXPLAIN` of restricted writes can also return error `3989`.
- Cluster-wide read-only restrictions still apply. Setting a database to writable does not override them.
- `IMPORT INTO` checks read-only mode at statement entry. A physical import that already started can continue after the database becomes read-only. Finish or cancel such imports before relying on unchanged data.
- With the deprecated batch DML feature enabled (`tidb_enable_batch_dml = ON`, `tidb_batch_insert = ON`, and `tidb_dml_batch_size > 0`), an `INSERT` can partially commit before a read-only transition and then fail. Previously committed batches are not rolled back. Let the statement finish before enabling read-only mode, and check for committed rows before retrying a failed statement.

### Interaction with other tools

| Tool | Behavior |
| --- | --- |
| TiDB Lightning | Physical imports using the `local` backend can write directly to TiKV into existing tables despite read-only mode. Control these imports separately. Logical imports obey SQL restrictions. |
| BR and SQL `BACKUP` / `RESTORE` | Snapshot restore preserves backed-up read-only metadata when it creates a database. If the target database already exists, restore retains its current read-only setting. Authorized restores can restore tables and sequences into read-only databases; ordinary writes to read-only databases remain restricted afterward. After restoring to an existing database, check `INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS`. If you require read-only protection, run `ALTER DATABASE ... READ ONLY = 1` as needed and wait for it to complete. PITR restores the state at the selected time. |
| Dumpling | Can export read-only databases. Replaying the SQL read-only comment does not enable read-only mode. |
| TiCDC v8.5.8 | Does not replicate database read-only DDL to MySQL downstream databases. |
| DM v8.5.8 | Pauses with a parsing error on upstream `ALTER DATABASE ... READ ONLY` statements. Explicitly skip these statements to resume. Writes to a read-only downstream database are rejected without the bypass privilege. |

## See also

- [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)
- [`SCHEMATA_EXTENSIONS`](/information-schema/information-schema-schemata-extensions.md)
- [Privilege Management](/privilege-management.md)
