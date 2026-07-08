---
title: SET PASSWORD | TiDB SQL Statement Reference
summary: An overview of the usage of SET PASSWORD for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-set-password/','/docs/dev/reference/sql/statements/set-password/']
---

# SET PASSWORD

This statement changes the user password for a user account in the TiDB system database.

## Synopsis

```ebnf+diagram
SetPasswordStmt ::=
    "SET" "PASSWORD" ( "FOR" Username )? "=" ( stringLit | "PASSWORD" "(" stringLit ")" ) ( "RETAIN" "CURRENT" "PASSWORD" )?
```

## Examples

```sql
mysql> SET PASSWORD='test'; -- change my password
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'newuser' IDENTIFIED BY 'test';
Query OK, 1 row affected (0.00 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = 'test';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = PASSWORD('test'); -- deprecated syntax from earlier MySQL releases
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Starting from v9.0.0, `SET PASSWORD ... RETAIN CURRENT PASSWORD` retains the current password as the secondary password while setting the new primary password, so both passwords remain valid during a password rotation. For details, see [Dual password policy](/password-management.md#dual-password-policy).

```sql
SET PASSWORD FOR 'newuser' = 'newpassword' RETAIN CURRENT PASSWORD;
```

```
Query OK, 0 rows affected (0.01 sec)
```

Setting your own password with `RETAIN CURRENT PASSWORD` requires the `APPLICATION_PASSWORD_ADMIN` dynamic privilege. Setting the password of another account requires the `SUPER` privilege.

## MySQL compatibility

The `SET PASSWORD` statement in TiDB is fully compatible with MySQL, except that TiDB does not support the `REPLACE 'current_auth_string'` clause for verifying the current password. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [CREATE USER](/sql-statements/sql-statement-create-user.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>
