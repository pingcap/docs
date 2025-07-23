---
title: 事务概述
summary: 对 TiDB 中事务的简要介绍。
---

# 事务概述

TiDB 支持完整的分布式事务，提供 [乐观事务](/optimistic-transaction.md) 和 [悲观事务](/pessimistic-transaction.md)（在 TiDB 3.0 中引入）。本文主要介绍事务语句、乐观事务和悲观事务、事务隔离级别，以及应用端的重试和乐观事务中的错误处理。

## 常用语句

本章介绍如何在 TiDB 中使用事务。以下示例演示了一个简单事务的流程：

Bob 想要向 Alice 转账 20 美元。该事务包括两个操作：

- Bob 的账户余额减少 20 美元。
- Alice 的账户余额增加 20 美元。

事务可以确保上述两个操作要么都成功执行，要么都失败。

使用 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `users` 表插入一些示例数据：

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

运行以下事务，并说明每个语句的含义：

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

在上述事务成功执行后，表格应如下所示：

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+
```

### 开始事务

要显式开启一个新事务，可以使用 `BEGIN` 或 `START TRANSACTION`。

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

TiDB 的默认事务模式为悲观。你也可以显式指定 [乐观事务模型](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

```sql
BEGIN OPTIMISTIC;
```

启用 [悲观事务模式](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)：

```sql
BEGIN PESSIMISTIC;
```

如果在执行上述语句时，当前会话正处于事务中，TiDB 会先提交当前事务，然后再开启新事务。

### 提交事务

你可以使用 `COMMIT` 语句提交当前事务中 TiDB 所做的所有修改。

```sql
COMMIT;
```

在启用乐观事务之前，确保你的应用能够正确处理 `COMMIT` 语句可能返回的错误。如果不确定你的应用如何处理，建议使用悲观事务模式。

### 回滚事务

你可以使用 `ROLLBACK` 语句回滚当前事务的修改。

```sql
ROLLBACK;
```

在前述转账示例中，如果你回滚整个事务，Alice 和 Bob 的余额将保持不变，当前事务的所有修改都将被取消。

```sql
TRUNCATE TABLE `users`;

INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (1, 'Alice', 100), (2, 'Bob', 200);

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+

BEGIN;
  UPDATE `users` SET `balance` = `balance` - 20 WHERE `nickname`='Bob';
  UPDATE `users` SET `balance` = `balance` + 20 WHERE `nickname`='Alice';
ROLLBACK;

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+
```

如果客户端连接中断或关闭，事务也会自动回滚。

## 事务隔离级别

事务隔离级别是数据库事务处理的基础。**ACID** 中的 "I"（Isolation）指的是事务的隔离性。

SQL-92 标准定义了四个隔离级别：

- read uncommitted (`READ UNCOMMITTED`)
- read committed (`READ COMMITTED`)
- repeatable read (`REPEATABLE READ`)
- serializable (`SERIALIZABLE`)

详见下表：

| 隔离级别           | 脏写 | 脏读 | 模糊读 | 幻读 |
| ------------------ | ------ | ------ | -------- | -------- |
| READ UNCOMMITTED   | 不可能 | 可能   | 可能     | 可能     |
| READ COMMITTED     | 不可能 | 不可能 | 可能     | 可能     |
| REPEATABLE READ    | 不可能 | 不可能 | 不可能   | 可能     |
| SERIALIZABLE       | 不可能 | 不可能 | 不可能   | 不可能   |

TiDB 支持以下隔离级别：`READ COMMITTED` 和 `REPEATABLE READ`：

```sql
mysql> SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
ERROR 8048 (HY000): The isolation level 'READ-UNCOMMITTED' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
mysql> SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 8048 (HY000): The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

TiDB 实现了 Snapshot Isolation（SI）级别的一致性，也称为 "repeatable read" 以保持与 MySQL 的一致性。该隔离级别不同于 [ANSI Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read) 和 [MySQL Repeatable Read Isolation Level](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)。更多详情请参见 [TiDB Transaction Isolation Levels](/transaction-isolation-levels.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>