---
title: RENAME USER
summary: 关于 TiDB 数据库中 RENAME USER 用法的概述。
---

# RENAME USER

`RENAME USER` 用于重命名现有用户。

## 概要

```ebnf+diagram
RenameUserStmt ::=
    'RENAME' 'USER' UserToUser ( ',' UserToUser )*
UserToUser ::=
    Username 'TO' Username
Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 示例

```sql
CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
```

```sql
Query OK, 1 row affected (0.02 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```sql
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)
```

```sql
RENAME USER 'newuser' TO 'testuser';
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW GRANTS FOR 'testuser';
```

```sql
+--------------------------------------+
| Grants for testuser@%                |
+--------------------------------------+
| GRANT USAGE ON *.* TO 'testuser'@'%' |
+--------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```sql
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

`RENAME USER` 预计与 MySQL 完全兼容。如果你发现任何兼容性差异，可以 [report a bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)