---
title: COMMIT | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 COMMIT 的用法概述。
---

# COMMIT

此语句用于提交 TiDB 服务器中的一个事务。

在没有使用 `BEGIN` 或 `START TRANSACTION` 语句的情况下，TiDB 的默认行为是每个语句都作为一个独立的事务并自动提交。此行为确保了与 MySQL 的兼容性。

## 概述

```ebnf+diagram
CommitStmt ::=
    'COMMIT' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

## 示例

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

* 目前，TiDB 默认使用 Metadata Locking (MDL) 来防止 DDL 语句修改被事务使用的表。TiDB 和 MySQL 在元数据锁的行为上存在差异。更多详情请参见 [Metadata Lock](/metadata-lock.md)。
* 默认情况下，TiDB 3.0.8 及更高版本使用 [Pessimistic Locking](/pessimistic-transaction.md)。当使用 [Optimistic Locking](/optimistic-transaction.md) 时，需要注意 `COMMIT` 语句可能会失败，因为行已被其他事务修改。
* 启用 Optimistic Locking 时，`UNIQUE` 和 `PRIMARY KEY` 约束的检查会延迟到语句提交时。这会导致在某些情况下 `COMMIT` 语句可能会失败。可以通过设置 `tidb_constraint_check_in_place=ON` 来改变此行为。
* TiDB 解析但忽略语法 `ROLLBACK AND [NO] RELEASE`。此功能在 MySQL 中用于在提交事务后立即断开客户端会话。在 TiDB 中，建议使用客户端驱动的 `mysql_close()` 功能。
* TiDB 解析但忽略语法 `ROLLBACK AND [NO] CHAIN`。此功能在 MySQL 中用于在当前事务提交时立即开启一个具有相同隔离级别的新事务。在 TiDB 中，建议改为开启新事务。

## 相关链接

* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [Lazy checking of constraints](/transaction-overview.md#lazy-check-of-constraints)