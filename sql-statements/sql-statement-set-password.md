---
title: SET PASSWORD | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SET PASSWORD 的概述。
---

# SET PASSWORD

此语句用于更改 TiDB 系统数据库中用户账户的密码。

## 概述

```ebnf+diagram
SetPasswordStmt ::=
    "SET" "PASSWORD" ( "FOR" Username )? "=" ( stringLit | "PASSWORD" "(" stringLit ")" )
```

## 示例

```sql
mysql> SET PASSWORD='test'; -- 更改我的密码
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

mysql> SET PASSWORD FOR newuser = PASSWORD('test'); -- 早期 MySQL 版本中的废弃语法
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SET PASSWORD` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE USER](/sql-statements/sql-statement-create-user.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>