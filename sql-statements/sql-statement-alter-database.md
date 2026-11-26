---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER DATABASE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-database/','/docs/dev/reference/sql/statements/alter-database/']
---

# ALTER DATABASE

`ALTER DATABASE` is used to specify or modify the default character set and collation of a database, or to change its read-only setting. `ALTER SCHEMA` has the same effect as `ALTER DATABASE`.

## Synopsis

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' ( 'DATABASE' | 'SCHEMA' ) DBName? AlterDatabaseOptionList

AlterDatabaseOptionList ::=
    DatabaseOptionList
|   'READ' 'ONLY' '='? ( '0' | '1' | 'DEFAULT' )

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## Read-only setting

Use `READ ONLY = 1` to enable database-level read-only mode. Use `READ ONLY = 0` or `READ ONLY = DEFAULT` to restore write access. The equals sign is optional. If you omit the database name, the statement applies to the current database.

Changing the setting requires the `ALTER` privilege on the database. System databases cannot be set to read-only. Enabling read-only mode waits for existing transactions that have accessed the database to finish across TiDB nodes.

Specify `READ ONLY` separately from other database options. The option is not supported in `CREATE DATABASE`.

For write restrictions, privileges, and operational limitations, see [Database-Level Read-Only Mode](/database-read-only.md).

## Examples

Modify the test database schema to use the utf8mb4 character set:

{{< copyable "sql" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

Currently, TiDB only supports some character sets and collations. See [Character Set and Collation Support](/character-set-and-collation.md) for details.

Enable read-only mode for the `test` database:

```sql
ALTER DATABASE test READ ONLY = 1;
```

Restore write access:

```sql
ALTER DATABASE test READ ONLY = DEFAULT;
```

## MySQL compatibility

The `READ ONLY` option accepts `0`, `1`, and `DEFAULT`, as in MySQL 8.0. However, TiDB also restricts local temporary tables in read-only databases and can reject write statements during `PREPARE`. For more information, see [Compatibility and limitations](/database-read-only.md#compatibility-and-limitations).

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
