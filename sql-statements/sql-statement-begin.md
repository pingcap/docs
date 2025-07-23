---
title: BEGIN | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 BEGIN 的用法概述。
---

# BEGIN

此语句在 TiDB 中启动一个新的事务。它类似于 `START TRANSACTION` 和 `SET autocommit=0` 语句。

在没有使用 `BEGIN` 语句的情况下，默认情况下每个语句都会在自己的事务中自动提交。这一行为确保了与 MySQL 的兼容性。

## 概要

```ebnf+diagram
BeginTransactionStmt ::=
    'BEGIN' ( 'PESSIMISTIC' | 'OPTIMISTIC' )?
|   'START' 'TRANSACTION' ( 'READ' ( 'WRITE' | 'ONLY' ( 'WITH' 'TIMESTAMP' 'BOUND' TimestampBound )? ) | 'WITH' 'CONSISTENT' 'SNAPSHOT' )?
```

## 示例

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

TiDB 支持 `BEGIN PESSIMISTIC` 或 `BEGIN OPTIMISTIC` 的语法扩展。这使你可以覆盖默认的事务模型。

## 相关链接

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB optimistic transaction model](/optimistic-transaction.md)
* [TiDB pessimistic transaction mode](/pessimistic-transaction.md)