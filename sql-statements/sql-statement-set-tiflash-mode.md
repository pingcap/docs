---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: An overview of the usage of ALTER TABLE ... SET TIFLASH MODE ... for the TiDB database.
---

# `ALTER TABLE ... SET TIFLASH MODE ...`

> **Warning:**
>
> This statement is still an experimental feature.
> The form and usage of related experimental features may change in subsequent versions.

You can use the `ALTER TABLE...SET TIFLASH MODE...` statement to switch the FastScan option for the corresponding table in TiFlash. The following options are currently supported.

- `Normal Mode`. The default option, means disabling FastScan. In this option, TiFlash guarantees the accuracy of query results and data consistency.
- `Fast Mode`. The FastScan option, means enableing FastScan. In this option, TiFlash provides more efficient query performance, but does not guarantee the accuracy of query results and data consistency.

This statement executes without blocking the execution of existing SQL statements or the running of TiDB features, such as transactions, DDL, and GC, and without changing the data content accessed through the SQL statement. The statement will end normally when the option switch is completed.

This statement only supports switching the FastScan option for tables in TiFlash, so the switch only affects reads involving the TiFlash table.

The FastScan switch takes effect only if the table has a TiFlash Replica. If the TiFlash Replica of the table is empty when you switch the option, the option will take effect only after the TiFlash Replica is subsequently reset. You can use [`ALTER TABLE ... SET TIFLASH REPLICA ...`](/sql-statements/sql-statement-alter-table.md) to reset the TiFlash Replica.

You can query the current TiFlash table switch of the corresponding table using the system table `information_schema.tiflash_replica`.

## Synopsis

```ebnf+diagram
AlterTableSetTiFlashModeStmt ::=
    'ALTER' 'TABLE' TableName 'SET' 'TIFLASH' 'MODE' mode
```

## Example

Assume that the `test` table has a TiFlash replica.

```sql
USE TEST;
CREATE TABLE test (a INT NOT NULL, b INT);
ALTER TABLE test SET TIFLASH REPLICA 1;
```

The default option of the `test` table is Normal Mode. You can query the table option with the following statement.

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| NORMAL     |
+------------+
```

If you want to enable FastScan to query the `test` table, execute the following statement to switch the option, and you can query the option of the current table.

```sql
ALTER TABLE test SET tiflash mode FAST
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| FAST       |
+------------+
```

If you want to disable FastScan, execute the following statement to switch.

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL compatibility

`ALTER TABLE ... SET TiFLASH MODE ...` is an extension to the standard SQL syntax introduced by TiDB. Although there is no equivalent MySQL syntax, you can still execute this statement from a MySQL client, or from database drivers that follow the MySQL protocol.

## TiDB Binlog and TiCDC compatibility

When the downstream is also TiDB, `ALTER TABLE ... SET TiFLASH MODE ...` will be synchronized downstream by TiDB Binlog. In other scenarios, TiDB Binlog does not synchronize this statement.

FastScan does not support TiCDC.

## See also

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)