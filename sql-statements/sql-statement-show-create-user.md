---
title: SHOW CREATE USER | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 SHOW CREATE USER 的用法概述。
---

# SHOW CREATE USER

此语句显示如何使用 `CREATE USER` 语法重新创建用户。

## 概要

```ebnf+diagram
ShowCreateUserStmt ::=
    "SHOW" "CREATE" "USER" (Username ("@" Hostname)? | "CURRENT_USER" ( "(" ")" )? )
```

## 示例

```sql
mysql> SHOW CREATE USER 'root';
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for root@%                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+--------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'root';
+-------------------------------------------+
| Grants for root@%                         |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

<CustomContent platform="tidb">

* `SHOW CREATE USER` 的输出旨在与 MySQL 保持一致，但 TiDB 目前尚不支持部分 `CREATE` 选项。不支持的选项会被解析但忽略。更多详情请参见 [Security compatibility](/security-compatibility-with-mysql.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* `SHOW CREATE USER` 的输出旨在与 MySQL 保持一致，但 TiDB 目前尚不支持部分 `CREATE` 选项。不支持的选项会被解析但忽略。更多详情请参见 [Security compatibility](https://docs.pingcap.com/tidb/stable/security-compatibility-with-mysql/)。

</CustomContent>

## 相关链接

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)