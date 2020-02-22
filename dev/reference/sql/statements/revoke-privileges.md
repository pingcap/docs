---
title: REVOKE <privileges> | TiDB SQL Statement Reference
summary: An overview of the usage of REVOKE <privileges> for the TiDB database.
category: reference
---

# REVOKE <privileges>

This statement removes privileges from an existing user.

## Synopsis

**GrantStmt:**

![GrantStmt](/media/sqlgram-dev/GrantStmt.png)

**PrivElemList:**

![PrivElemList](/media/sqlgram-dev/PrivElemList.png)

**PrivElem:**

![PrivElem](/media/sqlgram-dev/PrivElem.png)

**PrivType:**

![PrivType](/media/sqlgram-dev/PrivType.png)

**ObjectType:**

![ObjectType](/media/sqlgram-dev/ObjectType.png)

**PrivLevel:**

![PrivLevel](/media/sqlgram-dev/PrivLevel.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram-dev/UserSpecList.png)

## Examples

```sql
mysql> CREATE USER newuser IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)

mysql> REVOKE ALL ON test.* FROM 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> DROP USER newuser;
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW GRANTS FOR newuser;
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/dev/report-issue.md) on GitHub.

## See also

* [GRANT <privileges>](/dev/reference/sql/statements/grant-privileges.md)
* [SHOW GRANTS](/dev/reference/sql/statements/show-grants.md)
* [Privilege Management](/dev/reference/security/privilege-system.md)
