---
title: DROP USER | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 DROP USER 的概述。
---

# DROP USER

此语句用于从 TiDB 系统数据库中删除一个用户。可选的关键字 `IF EXISTS` 可以用来避免在用户不存在时产生错误。执行此操作需要拥有 `CREATE USER` 权限。

## 概述

```ebnf+diagram
DropUserStmt ::=
    'DROP' 'USER' ( 'IF' 'EXISTS' )? UsernameList

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 示例

```sql
mysql> DROP USER idontexist;
ERROR 1396 (HY000): Operation DROP USER failed for idontexist@%

mysql> DROP USER IF EXISTS 'idontexist';
Query OK, 0 rows affected (0.01 sec)

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

mysql> REVOKE ALL ON test.* FROM 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> DROP USER 'newuser';
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW GRANTS FOR 'newuser';
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

* 使用 `IF EXISTS` 删除不存在的用户在 TiDB 中不会产生警告。[Issue #10196](https://github.com/pingcap/tidb/issues/10196)。

## 相关链接

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>