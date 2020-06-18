---
title: GRANT <privileges> | TiDB SQL Statement Reference
summary: An overview of the usage of GRANT <privileges> for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/grant-privileges/']
---

# `GRANT <privileges>`

This statement allocates privileges to a pre-existing user in TiDB. The privilege system in TiDB follows MySQL, where credentials are assigned based on a database/table pattern.
Executing this statement requires the `GRANT OPTION` privilege and all privileges you allocate.

## Synopsis

**GrantStmt:**

![GrantStmt](/media/sqlgram/GrantStmt.png)

**PrivElemList:**

![PrivElemList](/media/sqlgram/PrivElemList.png)

**PrivElem:**

![PrivElem](/media/sqlgram/PrivElem.png)

**PrivType:**

![PrivType](/media/sqlgram/PrivType.png)

**ObjectType:**

![ObjectType](/media/sqlgram/ObjectType.png)

**PrivLevel:**

![PrivLevel](/media/sqlgram/PrivLevel.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

## Examples

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
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
```

## MySQL compatibility

* Similar to MySQL, the `USAGE` privilege denotes the ability to log into a TiDB server.
* Column level privileges are not currently supported.
* Similar to MySQL, when the `NO_AUTO_CREATE_USER` sql mode is not present, the `GRANT` statement will automatically create a new user with an empty password when a user does not exist. Removing this sql-mode (it is enabled by default) presents a security risk.

## See also

* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [Privilege Management](/privilege-management.md)
