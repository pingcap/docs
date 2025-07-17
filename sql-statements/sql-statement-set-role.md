---
title: SET ROLE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SET ROLE 的概述。
---

# SET ROLE

`SET ROLE` 语句用于在当前会话中启用角色。启用角色后，用户可以使用该角色的权限。

## 语法概述

```ebnf+diagram
SetRoleStmt ::=
    "SET" "ROLE" ( "DEFAULT" | "ALL" ( "EXCEPT" Rolename ("," Rolename)* )? | "NONE" | Rolename ("," Rolename)* )?
```

## 示例

创建一个用户 `'u1'@'%'` 和三个角色：`'r1'@'%'`、`'r2'@'%'` 和 `'r3'@'%'`。将这些角色授予 `'u1'@'%'`，并将 `'r1'@'%'` 设置为 `'u1'@'%'` 的默认角色。

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

以 `'u1'@'%'` 登录，并执行以下 `SET ROLE` 语句以启用所有角色。

```sql
SET ROLE ALL;
SELECT CURRENT_ROLE();
```

```
+----------------------------+
| CURRENT_ROLE()             |
+----------------------------+
| `r1`@`%`,`r2`@`%`,`r3`@`%` |
+----------------------------+
1 row in set (0.000 sec)
```

执行以下 `SET ROLE` 语句以启用 `'r2'` 和 `'r3'`。

```sql
SET ROLE 'r2', 'r3';
SELECT CURRENT_ROLE();
```

```
+-------------------+
| CURRENT_ROLE()    |
+-------------------+
| `r2`@`%`,`r3`@`%` |
+-------------------+
1 row in set (0.000 sec)
```

执行以下 `SET ROLE` 语句以启用默认角色。

```sql
SET ROLE DEFAULT;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `r1`@`%`       |
+----------------+
1 row in set (0.000 sec)
```

执行以下 `SET ROLE` 语句以取消所有已启用的角色。

```sql
SET ROLE NONE;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
|                |
+----------------+
1 row in set (0.000 sec)
```

## MySQL 兼容性

TiDB 中的 `SET ROLE` 语句与 MySQL 8.0 中的角色功能完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE ROLE](/sql-statements/sql-statement-create-role.md)
* [DROP ROLE](/sql-statements/sql-statement-drop-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [SET DEFAULT ROLE](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

* [Role-Based Access Control](/role-based-access-control.md)

</CustomContent>