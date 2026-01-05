# Database Read-Only

Database-level read-only allows you to set a single database to read-only, so that write operations (DDL, DML, and some locking reads) against that database and its objects are rejected. This capability is useful in scenarios such as sharded migration, traffic failback drills, and tenant data export, where you want to reduce the blast radius.

## Usage scenarios

- **Batch migration / failback**: When a shard batch encounters issues and you need to fail traffic back, set the corresponding database to read-only to prevent new writes from continuing.
- **Data export**: Set a tenant database to read-only to avoid inconsistency caused by data changes during export.

## Syntax

```sql
ALTER {DATABASE | SCHEMA} [db_name] READ ONLY [=] {DEFAULT | 0 | 1};
```

- `db_name` is optional. If omitted, TiDB uses the current default database of the session. If there is no default database, the statement fails.
- `DEFAULT` is equivalent to `0` (read-write).
- `READ ONLY` is only supported in `ALTER DATABASE/SCHEMA`, not supported in `CREATE DATABASE`.
- `READ ONLY` must be used alone. It cannot be combined in the same `ALTER DATABASE` statement with other options such as `CHARACTER SET`, `COLLATE`, `PLACEMENT POLICY`, or `SET TIFLASH REPLICA`.

**Examples**

Set a database to read-only:

```sql
ALTER DATABASE test READ ONLY = 1;
```

Set a database back to read-write:

```sql
ALTER DATABASE test READ ONLY = 0;
```

If the database is already in the requested state, the statement succeeds and returns a `Note` (you can check it via `SHOW WARNINGS`).

## Privileges and usage constraints

- **Required privilege**: You must have the `ALTER` privilege on the target database.
- **Interaction with cluster read-only**: When the cluster is in read-only mode (for example, `tidb_restricted_read_only=1`), you cannot change database read-only status. The statement will fail with `Running in read-only mode`.
- **System database restriction**: Database-level read-only is not supported for system databases, including `mysql`, `sys`, `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, and `METRICS_SCHEMA`.

## Database read-only observability

### Using INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS

The `OPTIONS` column of `INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS` shows extended schema properties. If this column's value is `READ ONLY=1`, the database is read-only; if the column is empty, the database is read-write.

```sql
SELECT CATALOG_NAME, SCHEMA_NAME, OPTIONS FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS;

+--------------+--------------------+-------------+
| CATALOG_NAME | SCHEMA_NAME        | OPTIONS     |
+--------------+--------------------+-------------+
| def          | INFORMATION_SCHEMA |             |
| def          | METRICS_SCHEMA     |             |
| def          | mysql              |             |
| def          | PERFORMANCE_SCHEMA |             |
| def          | sys                |             |
| def          | test               | READ ONLY=1 |
+--------------+--------------------+-------------+
```

### Using SHOW CREATE DATABASE

When a database is read-only, `SHOW CREATE DATABASE` appends a comment `/* READ ONLY = 1 */` at the end of the output.

```sql
SHOW CREATE DATABASE test;
+----------+--------------------------------------------------------------------------------------+
| Database | Create Database                                                                      |
+----------+--------------------------------------------------------------------------------------+
| test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ /* READ ONLY = 1 */ |
+----------+--------------------------------------------------------------------------------------+
```

## Behavior of read-only DDL

### Transaction when switching read-only state

`ALTER DATABASE ... READ ONLY = 1` is an online DDL. It first blocks new writes to the target database and then waits for existing transactions related to that database to commit before returning.

If a transaction has not accessed the database at the beginning, but accesses an object in that database after the read-only DDL finishes, it may fail with an error similar to:

- `public schema <db> read only state has changed`

### Troubleshooting when DDL takes a long time

If `ALTER DATABASE ... READ ONLY = 1` takes a long time to finish, it is usually blocked by uncommitted transactions, TiDB periodically outputs the following logs:

```
[INFO] [schema.go:xxx] ["uncommitted txn block read only ddl"] [category=ddl] ["txn ID"=<txn_id>] ["job ID"=<job_id>]
```

You can query transaction information and locate the blocked session to further confirm the scope of the impact:

```sql
SELECT INSTANCE, ID, SESSION_ID, USER, DB, STATE, START_TIME, RELATED_TABLE_IDS FROM INFORMATION_SCHEMA.CLUSTER_TIDB_TRX;
```

## Behavior in a read-only database

When a database is read-only, restricted statements typically fail with:

- `ERROR 3989 (HY000): Schema '<db>' is in read only mode.`

### Rejected operations

- **DDL**:
  - `DROP DATABASE`
  - `ALTER DATABASE` (except changing `READ ONLY` itself)
  - `CREATE TABLE` (including `TEMPORARY` / `GLOBAL TEMPORARY`)
  - `ALTER TABLE` (changes to columns, indexes, partitions, foreign keys, `AUTO_INCREMENT`, etc.)
  - `RENAME TABLE`
  - `TRUNCATE TABLE`
  - `DROP TABLE` / `DROP VIEW`
  - `CREATE INDEX` / `DROP INDEX`
  - `CREATE VIEW` / `CREATE OR REPLACE VIEW`
- **DML**: `INSERT`, `REPLACE`, `UPDATE`, `DELETE`
- **Locking reads**: `SELECT ... FOR UPDATE` and related variants (`NOWAIT/WAIT`, `FOR UPDATE OF ...`, `TABLE ... FOR UPDATE`, etc.)
- **FOR SHARE**: When `tidb_enable_shared_lock_promotion=1`, `SELECT ... FOR SHARE` is also rejected (because it may be promoted to `FOR UPDATE` semantics).
- **Data import**: `LOAD DATA`, `IMPORT INTO`
- **Binding**: Creating bindings for statements that modify data is rejected.
- **PREPARE**: TiDB performs the read-only check during `PREPARE`. Statements that are not executable in a read-only database fail at `PREPARE` time, which may differ from MySQL.
- **EXECUTE**: Executing a prepared statement that modifies data in a read-only database fails.
- **EXPLAIN / EXPLAIN ANALYZE**: Planning also triggers the read-only check. Therefore, `EXPLAIN` / `EXPLAIN ANALYZE` can fail for statements that are not executable in read-only.
- **Foreign Key Cascades**: If a `DELETE/UPDATE` on a parent table triggers cascading changes on child tables, and the child table is in a read-only database, the `DELETE/UPDATE` is rejected with `ERROR 3989`.


> Note: In the current implementation, temporary tables are not exempt. Creating/modifying/writing temporary tables in a read-only database is also rejected.

### Allowed operations

- Regular read-only queries: `SELECT` without `FOR UPDATE/SHARE`, `TABLE t;`

### Replication / synchronization tools

Database-level read-only only applies at the TiDB SQL layer. Paths that bypass the SQL layer are not restricted.

**TiCDC**: Currently, TiCDC does not support replicating this DDL.

**DM**: Replicating this DDL is currently not supported.

**Dumpling**: Exporting a read-only database is supported and requires no extra configuration.

**TiDB Lightning**: Physical import into a read-only database can succeed, while logical import fails.

**BR**: Restoring into a read-only database is allowed.

## MySQL compatibility

This feature is based on MySQL 8.0 database-level read-only. Below are the major incompatibilities between TiDB and MySQL in the current implementation:

- **ALTER DATABASE with multiple options**: MySQL allows setting `READ ONLY` together with `CHARACTER SET`/`COLLATE` in a single `ALTER DATABASE` statement; TiDB only supports setting `READ ONLY` alone (you need to split it into multiple statements).
- **TEMPORARY tables**: MySQL typically does not restrict `TEMPORARY` tables because of database-level read-only; TiDB does not exempt them and rejects creating/modifying/writing temporary tables (including `GLOBAL TEMPORARY`) in a read-only database.
- **PREPARE**: MySQL may allow `PREPARE` to succeed and fail at execution time; TiDB checks at `PREPARE` time and rejects statements that are not executable in a read-only database (commonly `ERROR 3989`).
- **EXPLAIN/EXPLAIN ANALYZE**: MySQL may allow `EXPLAIN` for some statements; TiDB triggers the read-only check during planning, so `EXPLAIN` can also fail for statements not executable in read-only.
- **Cross-database view dependency checks**: MySQL may block structural changes to underlying tables if they are referenced by views in a read-only database; TiDB currently does not block such changes (this may be improved in the future).
