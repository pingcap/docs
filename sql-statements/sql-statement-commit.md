---
title: COMMIT | TiDB SQL Statement Reference
summary: An overview of the usage of COMMIT for the TiDB database.
aliases: ['/docs/v2.1/sql-statements/sql-statement-commit/','/docs/v2.1/reference/sql/statements/commit/']
---

# COMMIT

This statement commits a transaction inside of the TIDB server.

In the absence of a `BEGIN` or `START TRANSACTION` statement, the default behavior of TiDB is that every statement will be its own transaction and autocommit. This behavior ensures MySQL compatibility.

## Synopsis

**CommitStmt:**

![CommitStmt](/media/sqlgram/CommitStmt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

* TiDB 2.1 uses [Optimistic Locking](/optimistic-transaction.md). It is important to consider that a `COMMIT` statement might fail because rows have been modified by another transaction. This changes in later versions of TiDB, where pessimistic locking is available.
* By default, `UNIQUE` and `PRIMARY KEY` constraint checks are deferred until statement commit. This behavior can be changed by setting `tidb_constraint_check_in_place=TRUE`.

## See also

* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [Lazy checking of constraints](/transaction-overview.md#lazy-check-of-constraints)
