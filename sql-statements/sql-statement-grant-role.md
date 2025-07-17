---
title: GRANT <role> | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 GRANT <role> 的概述。
---

# `GRANT <role>`

将之前创建的角色分配给现有用户。用户随后可以使用语句 `SET ROLE <rolename>` 来假设该角色的权限，或使用 `SET ROLE ALL` 来假设已被分配的所有角色。

## 概要

```ebnf+diagram
GrantRoleStmt ::=
    'GRANT' RolenameList 'TO' UsernameList

RolenameList ::=
    Rolename ( ',' Rolename )*

UsernameList ::=
    Username ( ',' Username )*
```

## 示例

以 `root` 用户连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

创建一个新角色 `analyticsteam` 和一个新用户 `jennifer`：

```sql
CREATE ROLE analyticsteam;
Query OK, 0 rows affected (0.02 sec)

GRANT SELECT ON test.* TO analyticsteam;
Query OK, 0 rows affected (0.02 sec)

CREATE USER jennifer;
Query OK, 0 rows affected (0.01 sec)

GRANT analyticsteam TO jennifer;
Query OK, 0 rows affected (0.01 sec)
```

以 `jennifer` 用户连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

注意，默认情况下，`jennifer` 需要执行 `SET ROLE analyticsteam` 才能使用与 `analyticsteam` 角色相关联的权限：

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
2 rows in set (0.00 sec)

SHOW TABLES in test;
ERROR 1044 (42000): Access denied for user 'jennifer'@'%' to database 'test'
SET ROLE analyticsteam;
Query OK, 0 rows affected (0.00 sec)

SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

以 `root` 用户连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

可以使用 `SET DEFAULT ROLE` 语句将 `analyticsteam` 角色关联到 `jennifer`：

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

以 `jennifer` 用户连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

之后，用户 `jennifer` 将拥有与 `analyticsteam` 角色相关联的权限，且无需执行 `SET ROLE` 语句：

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `GRANT <role>` 语句与 MySQL 8.0 中的角色功能完全兼容。如果发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
* [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

* [Role-Based Access Control](/role-based-access-control.md)

</CustomContent>