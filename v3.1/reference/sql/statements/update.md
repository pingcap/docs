---
title: UPDATE | TiDB SQL Statement Reference
summary: An overview of the usage of UPDATE for the TiDB database.
category: reference
---

# UPDATE

The `UPDATE` statement is used to modify data in a specified table.

## Synopsis

**UpdateStmt:**

![UpdateStmt](/media/sqlgram-v3.0/UpdateStmt.png)

**TableRef:**

![TableRef](/media/sqlgram-v3.0/TableRef.png)

**TableRefs:**

![TableRefs](/media/sqlgram-v3.0/TableRefs.png)

**AssignmentList:**

![AssignmentList](/media/sqlgram-v3.0/AssignmentList.png)

**WhereClauseOptional:**

![WhereClauseOptional](/media/sqlgram-v3.0/WhereClauseOptional.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> UPDATE t1 SET c1=5 WHERE c1=3;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v3.1/report-issue.md) on GitHub.

## See also

* [INSERT](/v3.1/reference/sql/statements/insert.md)
* [SELECT](/v3.1/reference/sql/statements/select.md)
* [DELETE](/v3.1/reference/sql/statements/delete.md)
* [REPLACE](/v3.1/reference/sql/statements/replace.md)
