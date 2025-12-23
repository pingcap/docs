---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL 语句参考
summary: 概述 TiDB 数据库中 SET [GLOBAL|SESSION] <variable> 的用法。
---

# `SET [GLOBAL|SESSION] <variable>`

`SET [GLOBAL|SESSION]` 语句用于修改 TiDB 内置的变量。这些变量可以是 [系统变量](/system-variables.md)，其作用域为 `SESSION` 或 `GLOBAL`，也可以是 [用户变量](/user-defined-variables.md)。

> **警告：**
>
> 用户自定义变量仍属于实验特性。**不**建议在生产环境中使用。

> **注意：**
>
> 与 MySQL 类似，对 `GLOBAL` 变量的更改不会影响已存在的连接或本地连接。只有新建的会话会反映变量值的更改。

## 语法

```ebnf+diagram
SetVariableStmt ::=
    "SET" Variable "=" Expression ("," Variable "=" Expression )*

Variable ::=
    ("GLOBAL" | "SESSION") SystemVariable
|   UserVariable 
```

## 示例

获取 `sql_mode` 的值。

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

全局 update `sql_mode` 的值。update 后如果你查看 `SQL_mode` 的值，可以看到 `SESSION` 级别的值并未被 update：

```sql
mysql> SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

使用 `SET SESSION` 会立即生效：

```sql
mysql> SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

用户变量以 `@` 开头。

```sql
SET @myvar := 5;
Query OK, 0 rows affected (0.00 sec)

SELECT @myvar, @myvar + 1;
+--------+------------+
| @myvar | @myvar + 1 |
+--------+------------+
|      5 |          6 |
+--------+------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

存在如下行为差异：

* 在 MySQL 中，使用 `SET GLOBAL` 进行的更改不会应用到副本。但在 TiDB 中，`SET GLOBAL` 的作用域取决于具体的系统变量：
    * 全局变量：对于大多数系统变量（例如影响集群行为或优化器行为的变量），使用 `SET GLOBAL` 进行的更改会应用到集群内所有 TiDB 实例。
    * 实例级变量：对于某些系统变量（例如 `max_connections`），使用 `SET GLOBAL` 进行的更改只会应用到当前连接所使用的 TiDB 实例。

    因此，在使用 `SET GLOBAL` 修改变量时，请务必查阅该变量的 [文档](/system-variables.md)，特别是 “Persists to cluster” 属性，以确认更改的作用范围。

* TiDB 将若干变量同时作为可读和可设置变量暴露。这是为了兼容 MySQL，因为应用程序和连接器通常会读 MySQL 变量。例如：JDBC 连接器会读和设置查询缓存相关设置，尽管并不依赖其行为。
* 使用 `SET GLOBAL` 进行的更改会在 TiDB server 重启后依然保留。这意味着 TiDB 中的 `SET GLOBAL` 行为更类似于 MySQL 8.0 及以上版本中的 `SET PERSIST`。
* TiDB 不支持 `SET PERSIST` 和 `SET PERSIST_ONLY`，因为 TiDB 会持久化全局变量。

## 另请参阅

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/sql-statements/sql-statement-show-variables.md)
