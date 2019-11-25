---
title: SET PASSWORD | TiDB SQL Statement Reference
summary: An overview of the usage of SET PASSWORD for the TiDB database.
category: reference
---

# SET PASSWORD

This statement changes the user password for a user account in the TiDB system database.

## Synopsis

**SetStmt:**

![SetStmt](/media/sqlgram-v2.1/SetStmt.png)

## Examples

```sql
mysql> SET PASSWORD='test'; -- change my password
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'newuser' IDENTIFIED BY 'test';
Query OK, 1 row affected (0.00 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = 'test';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = PASSWORD('test'); -- deprecated syntax from earlier MySQL releases
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v2.1/report-issue.md) on GitHub.

## See also

* [CREATE USER](/v2.1/reference/sql/statements/create-user.md)
* [Privilege Management](/v2.1/reference/security/privilege-system.md)
