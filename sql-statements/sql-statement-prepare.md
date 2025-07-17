---
title: PREPARE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 PREPARE 的概述。
---

# PREPARE

`PREPARE` 语句提供了一个服务器端预处理语句的 SQL 接口。

## 语法概要

```ebnf+diagram
PreparedStmt ::=
    'PREPARE' Identifier 'FROM' PrepareSQL

PrepareSQL ::=
    stringLit
|   UserVariable
```

> **注意：**
>
> 每个 `PREPARE` 语句的占位符最大数量为 65535。

为了限制当前 TiDB 实例中的 `PREPARE` 语句数量，可以使用 [`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count) 系统变量。

## 示例

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `PREPARE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [EXECUTE](/sql-statements/sql-statement-execute.md)
* [DEALLOCATE](/sql-statements/sql-statement-deallocate.md)
