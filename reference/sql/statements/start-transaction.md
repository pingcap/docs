---
title: START TRANSACTION | TiDB SQL Statement Reference
summary: An overview of the usage of START TRANSACTION for the TiDB database.
category: reference
---

# START TRANSACTION

This statement starts a new transaction inside of TiDB. It is similar to the statements `BEGIN` and `SET autocommit=0`.

In the absence of a `START TRANSACTION` statement, every statement will by default autocommit in its own transaction. This behavior ensures MySQL compatibility.

## Synopsis

**BeginTransactionStmt:**

<<<<<<< HEAD
![BeginTransactionStmt](/media/sqlgram-v2.1/BeginTransactionStmt.png)
=======
![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)
>>>>>>> 359cdb7... media: replace sqlgram-dev, sqlgram-3.0, sqlgram-2.1 with sqlgram  (#2434)

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

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [COMMIT](/reference/sql/statements/commit.md)
* [ROLLBACK](/reference/sql/statements/rollback.md)
* [BEGIN](/reference/sql/statements/begin.md)
