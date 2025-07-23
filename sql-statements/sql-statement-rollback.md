---
title: ROLLBACK | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 ROLLBACK 的概述。
---

# ROLLBACK

此语句用于还原 TiDB 当前事务中的所有更改。它与 `COMMIT` 语句相反。

## 概述

```ebnf+diagram
RollbackStmt ::=
    'ROLLBACK' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
Empty set (0.01 sec)
```

## MySQL 兼容性

* TiDB 解析但忽略语法 `ROLLBACK AND [NO] RELEASE`。此功能在 MySQL 中用于在回滚事务后立即断开客户端会话。在 TiDB 中，建议使用你的客户端驱动的 `mysql_close()` 功能。
* TiDB 解析但忽略语法 `ROLLBACK AND [NO] CHAIN`。此功能在 MySQL 中用于在当前事务回滚的同时立即以相同的隔离级别启动一个新事务。在 TiDB 中，建议改为启动一个新事务。

## 相关链接

* [SAVEPOINT](/sql-statements/sql-statement-savepoint.md)
* [COMMIT](/sql-statements/sql-statement-commit.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)