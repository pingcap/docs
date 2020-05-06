---
title: FLUSH TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of FLUSH TABLES for the TiDB database.
category: reference
---

# FLUSH TABLES

This statement is included for compatibility with MySQL. It has no effective usage in TiDB.

## Synopsis

**FlushStmt:**

<<<<<<< HEAD
![FlushStmt](/media/sqlgram-v2.1/FlushStmt.png)

**NoWriteToBinLogAliasOpt:**

![NoWriteToBinLogAliasOpt](/media/sqlgram-v2.1/NoWriteToBinLogAliasOpt.png)

**FlushOption:**

![FlushOption](/media/sqlgram-v2.1/FlushOption.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram-v2.1/TableOrTables.png)

**TableNameListOpt:**

![TableNameListOpt](/media/sqlgram-v2.1/TableNameListOpt.png)

**WithReadLockOpt:**

![WithReadLockOpt](/media/sqlgram-v2.1/WithReadLockOpt.png)
=======
![FlushStmt](/media/sqlgram/FlushStmt.png)

**NoWriteToBinLogAliasOpt:**

![NoWriteToBinLogAliasOpt](/media/sqlgram/NoWriteToBinLogAliasOpt.png)

**FlushOption:**

![FlushOption](/media/sqlgram/FlushOption.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram/TableOrTables.png)

**TableNameListOpt:**

![TableNameListOpt](/media/sqlgram/TableNameListOpt.png)

**WithReadLockOpt:**

![WithReadLockOpt](/media/sqlgram/WithReadLockOpt.png)
>>>>>>> 359cdb7... media: replace sqlgram-dev, sqlgram-3.0, sqlgram-2.1 with sqlgram  (#2434)

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

* [Read historical data](/how-to/get-started/read-historical-data.md)
