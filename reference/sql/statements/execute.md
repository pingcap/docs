---
title: EXECUTE | TiDB SQL Statement Reference
summary: An overview of the usage of EXECUTE for the TiDB database.
category: reference
---

# EXECUTE

The `EXECUTE` statement provides an SQL interface to server-side prepared statements.

## Synopsis

**ExecuteStmt:**

<<<<<<< HEAD
![ExecuteStmt](/media/sqlgram-v3.0/ExecuteStmt.png)

**Identifier:**

![Identifier](/media/sqlgram-v3.0/Identifier.png)
=======
![ExecuteStmt](/media/sqlgram/ExecuteStmt.png)

**Identifier:**

![Identifier](/media/sqlgram/Identifier.png)
>>>>>>> 359cdb7... media: replace sqlgram-dev, sqlgram-3.0, sqlgram-2.1 with sqlgram  (#2434)

## Examples

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [PREPARE](/reference/sql/statements/prepare.md)
* [DEALLOCATE](/reference/sql/statements/deallocate.md)
