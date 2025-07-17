---
title: SHOW GRANTS | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 SHOW GRANTS 的用法概述。
---

# SHOW GRANTS

此语句显示与某个用户相关联的权限列表。与 MySQL 一样，`USAGE` 权限表示登录 TiDB 的能力。

## 概要

```ebnf+diagram
ShowGrantsStmt ::=
    "SHOW" "GRANTS" ("FOR" Username ("USING" RolenameList)?)?

Username ::=
    "CURRENT_USER" ( "(" ")" )?
| Username ("@" Hostname)?

RolenameList ::=
    Rolename ("@" Hostname)? ("," Rolename ("@" Hostname)? )*
```

## 示例

```sql
mysql> SHOW GRANTS;
+-------------------------------------------+
| Grants for User                           |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'u1';
ERROR 1141 (42000): There is no such grant defined for user 'u1' on host '%'
mysql> CREATE USER u1;
Query OK, 1 row affected (0.04 sec)

mysql> GRANT SELECT ON test.* TO u1;
Query OK, 0 rows affected (0.04 sec)

mysql> SHOW GRANTS FOR u1;
+------------------------------------+
| Grants for u1@%                    |
+------------------------------------+
| GRANT USAGE ON *.* TO 'u1'@'%'     |
| GRANT Select ON test.* TO 'u1'@'%' |
+------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW GRANTS` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [GRANT](/sql-statements/sql-statement-grant-privileges.md)