---
title: Column-Level Privilege Management
summary: TiDB supports a MySQL-compatible column-level privilege management mechanism. You can grant or revoke `SELECT`, `INSERT`, `UPDATE`, and `REFERENCES` privileges on specific columns of a table using `GRANT` or `REVOKE`, achieving finer-grained access control.
---

# Column-Level Privilege Management

Starting from v8.5.6, TiDB supports a MySQL-compatible column-level privilege management mechanism. With column-level privileges, you can grant or revoke `SELECT`, `INSERT`, `UPDATE`, and `REFERENCES` privileges on specific columns in a specified table, achieving finer-grained data access control.

> **Note:**
>
> Although MySQL syntax allows column-level syntax such as `REFERENCES(col_name)`, `REFERENCES` itself is a database-level or table-level privilege used for foreign key-related privilege checks. Therefore, column-level `REFERENCES` does not produce any actual column-level privilege effect in MySQL. TiDB's behavior is consistent with MySQL.

## Syntax

The syntax for granting and revoking column-level privileges is similar to that for table-level privileges, with the following differences:

- Write the column name list after the **privilege type**, not after the **table name**.
- Multiple column names are separated by commas (`,`).

```sql
GRANT priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    TO 'user'@'host';

REVOKE priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    FROM 'user'@'host';
```

Where:

* `priv_type` supports `SELECT`, `INSERT`, `UPDATE`, and `REFERENCES`.
* The `ON` clause must specify a table, for example, `test.tbl`.
* A single `GRANT` or `REVOKE` statement can include multiple privilege items, and each privilege item can specify its own list of column names.

For example, the following statement grants `SELECT` privileges on `col1` and `col2` and `UPDATE` privilege on `col3` to the user:

```sql
GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'user'@'host';
```

## Example: Grant column-level privileges

The following example grants user `newuser` the `SELECT` privilege on `col1` and `col2` in table `test.tbl`, and grants the same user the `UPDATE` privilege on `col3`:

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

DROP TABLE IF EXISTS tbl;
CREATE TABLE tbl (col1 INT, col2 INT, col3 INT);

DROP USER IF EXISTS 'newuser'@'%';
CREATE USER 'newuser'@'%';

GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

```
+---------------------------------------------------------------------+
| Grants for newuser@%                                                |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'                                 |
| GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
+---------------------------------------------------------------------+
```

In addition to using `SHOW GRANTS`, you can also view column-level privilege information by querying `INFORMATION_SCHEMA.COLUMN_PRIVILEGES`.

## Example: Revoke column-level privileges

The following example revokes the `SELECT` privilege on column `col2` from user `newuser`:

```sql
REVOKE SELECT(col2) ON test.tbl FROM 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

```
+---------------------------------------------------------------+
| Grants for newuser@%                                          |
+---------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'                           |
| GRANT SELECT(col1), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
+---------------------------------------------------------------+
```

## Example: Column-level privilege access control

After granting or revoking column-level privileges, TiDB performs privilege checks on columns referenced in SQL statements. For example:

* `SELECT` statements: `SELECT` column privileges affect columns referenced in the `SELECT` list as well as `WHERE`, `ORDER BY`, and other clauses.
* `UPDATE` statements: columns being updated in the `SET` clause require `UPDATE` column privileges. Columns read in expressions or conditions usually also require `SELECT` column privileges.
* `INSERT` statements: columns being written to require `INSERT` column privileges. `INSERT INTO t VALUES (...)` is equivalent to writing values to all columns in table definition order.

In the following example, user `newuser` can only query `col1` and update `col3`:

```sql
-- Execute as newuser
SELECT col1 FROM tbl;
SELECT * FROM tbl; -- Error (missing SELECT column privilege for col2, col3)

UPDATE tbl SET col3 = 1;
UPDATE tbl SET col1 = 2; -- Error (missing UPDATE column privilege for col1)

UPDATE tbl SET col3 = col1;
UPDATE tbl SET col3 = col3 + 1; -- Error (missing SELECT column privilege for col3)
UPDATE tbl SET col3 = col1 WHERE col1 > 0;
```

## Compatibility differences with MySQL

TiDB's column-level privileges are generally compatible with MySQL. However, there are differences in the following scenarios:

| Scenario                                             | TiDB                                                                                                                                                                   | MySQL                                                                                                                                                                            |
| :--------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Revoking column-level privileges not granted to a user | `REVOKE` executes successfully. | When `IF EXISTS` is not used, `REVOKE` returns an error. |
| Execution order of column pruning and `SELECT` privilege check | `SELECT` column privileges are checked before column pruning. For example, executing `SELECT a FROM (SELECT a, b FROM t) s` requires `SELECT` column privileges on both `t.a` and `t.b`. | Column pruning is performed before `SELECT` column privileges are checked. For example, executing `SELECT a FROM (SELECT a, b FROM t) s` only requires the `SELECT` column privilege on `t.a`. |

### Column pruning and privilege checks in view scenarios

When performing `SELECT` privilege checks on views, MySQL and TiDB differ as follows:

- MySQL first prunes columns in the view's internal query and then checks the column privileges of the internal tables, making the checks relatively lenient in some scenarios. 
- TiDB does not perform column pruning before privilege checks, so additional column privileges might be required.

```sql
-- Prepare the environment by logging in as root
DROP USER IF EXISTS 'u'@'%';
CREATE USER 'u'@'%';

DROP TABLE IF EXISTS t;
CREATE TABLE t (a INT, b INT, c INT, d INT);

DROP VIEW IF EXISTS v;
CREATE SQL SECURITY INVOKER VIEW v AS SELECT a, b FROM t WHERE c = 0 ORDER BY d;

GRANT SELECT ON v TO 'u'@'%';

-- Log in as u
SELECT a FROM v;
-- MySQL: Error, missing access privileges for t.a, t.c, t.d
-- TiDB: Error, missing access privileges for t.a, t.b, t.c, t.d

-- Log in as root
GRANT SELECT(a, c, d) ON t TO 'u'@'%';

-- Log in as u
SELECT a FROM v;
-- MySQL: Success (internal query is pruned to `SELECT a FROM t WHERE c = 0 ORDER BY d`)
-- TiDB: Error, missing access privileges for t.b

SELECT * FROM v;
-- MySQL: Error, missing access privileges for t.b
-- TiDB: Error, missing access privileges for t.b

-- Log in as root
GRANT SELECT(b) ON t TO 'u'@'%';

-- Log in as u
SELECT * FROM v;
-- MySQL: Success
-- TiDB: Success
```

## See also

* [Privilege Management](/privilege-management.md)
* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
