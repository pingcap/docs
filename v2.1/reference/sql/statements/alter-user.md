---
title: ALTER USER | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER USER for the TiDB database.
category: reference
---

# ALTER USER

This statement changes an existing user inside the TiDB privilege system. In the MySQL privilege system, a user is the combination of a username and the host from which they are connecting from. Thus, it is possible to create a user `'newuser2'@'192.168.1.1'` who is only able to connect from the IP address `192.168.1.1`. It is also possible to have two users have the same user-portion, and different permissions as they login from different hosts.

## Synopsis

**AlterUserStmt:**

![AlterUserStmt](/media/sqlgram-v2.1/AlterUserStmt.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram-v2.1/UserSpecList.png)

**UserSpec:**

![UserSpec](/media/sqlgram-v2.1/UserSpec.png)

## Examples

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.01 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *5806E04BBEE79E1899964C6A04D68BCA69B1A879 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)

mysql> ALTER USER 'newuser' IDENTIFIED BY 'newnewpassword';
Query OK, 0 rows affected (0.02 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *FB8A1EA1353E8775CA836233E367FBDFCB37BE73 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

* In MySQL this statement is used to change attributes such as to expire a password. This functionality is not yet supported by TiDB.

## See also

* [Security Compatibility with MySQL](/v2.1/reference/security/compatibility.md)
* [CREATE USER](/v2.1/reference/sql/statements/create-user.md)
* [DROP USER](/v2.1/reference/sql/statements/drop-user.md)
