---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH TABLES for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/flush-tables/']
---

# FLUSH TABLES

This statement is included for compatibility with MySQL. It has no effective usage in TiDB.

## Synopsis

**FlushStmt:**

![FlushStmt](/media/sqlgram/FlushStmt.png)

**NoWriteToBinLogAliasOpt:**

![NoWriteToBinLogAliasOpt](/media/sqlgram/NoWriteToBinLogAliasOpt.png)

**FlushOption:**

![FlushOption](/media/sqlgram/FlushOption.png)

**LogTypeOpt:**

![LogTypeOpt](/media/sqlgram/LogTypeOpt.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram/TableOrTables.png)

**TableNameListOpt:**

![TableNameListOpt](/media/sqlgram/TableNameListOpt.png)

**WithReadLockOpt:**

![WithReadLockOpt](/media/sqlgram/WithReadLockOpt.png)

## Examples

```sql
mysql> FLUSH TABLES;
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH TABLES WITH READ LOCK;
ERROR 1105 (HY000): FLUSH TABLES WITH READ LOCK is not supported.  Please use @@tidb_snapshot
```

## MySQL compatibility

* TiDB does not have a concept of table cache as in MySQL.  Thus, `FLUSH TABLES` is parsed but ignored in TiDB for compatibility.
* The statement `FLUSH TABLES WITH READ LOCK` produces an error, as TiDB does not currently support locking tables. It is recommended to use [Historical reads] for this purpose instead.

## See also

* [Read historical data](/read-historical-data.md)
