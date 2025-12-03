---
title: Transaction Restraints
summary: 了解 TiDB 中的事务限制。
---

# 事务限制

本文档简要介绍了 TiDB 中的事务限制。

## 隔离级别

TiDB 支持的隔离级别有 **RC (Read Committed)** 和 **SI (Snapshot Isolation)**，其中 **SI** 基本等同于 **RR (Repeatable Read)** 隔离级别。

![isolation level](/media/develop/transaction_isolation_level.png)

## Snapshot Isolation 可以避免幻读

TiDB 的 `SI` 隔离级别可以避免 **Phantom Reads**，但 ANSI/ISO SQL 标准中的 `RR` 隔离级别无法避免。

下面两个例子展示了什么是 **幻读**。

- 示例 1：**事务 A** 首先根据查询获取了 `n` 行，然后 **事务 B** 修改了这 `n` 行之外的 `m` 行，或者新增了 `m` 行满足 **事务 A** 查询条件的数据。当 **事务 A** 再次执行该查询时，发现有 `n+m` 行满足条件。就像出现了幻影一样，因此称为 **幻读**。

- 示例 2：**管理员 A** 将数据库中所有学生的成绩从具体分数改为 ABCDE 等级，但此时 **管理员 B** 插入了一条带有具体分数的记录。当 **管理员 A** 修改完后，发现还有一条记录（即 **管理员 B** 插入的）没有被修改。这也是一次 **幻读**。

## SI 无法避免写偏差

TiDB 的 SI 隔离级别无法避免 **write skew** 异常。你可以使用 `SELECT FOR UPDATE` 语法来避免 **write skew** 异常。

**write skew** 异常发生在两个并发事务分别读取了不同但相关的记录，然后各自更新了自己读取到的数据并最终提交事务。如果这些相关记录之间存在约束，要求不能被多个事务同时修改，那么最终结果就会违反该约束。

例如，假设你正在为医院编写一个医生值班管理程序。医院通常要求有多名医生同时值班，但最低要求是至少有一名医生值班。只要在该班次至少有一名医生值班，医生就可以请假（比如生病）。

现在有这样一种情况，医生 `Alice` 和 `Bob` 正在值班。两人都感觉不适，于是都决定请病假，并且恰好同时点击了请假按钮。我们用下面的程序来模拟这个过程：

<SimpleTab groupId="language">

<div label="Java" value="java">

```java
// 代码略，保持原文
```

</div>

<div label="Golang" value="golang">

要适配 TiDB 事务，请根据以下代码编写一个 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)：

```go
// 代码略，保持原文
```

</div>

</SimpleTab>

SQL 日志：

```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) as `count` FROM `doctors` WHERE `on_call` = 1 AND `shift_id` = 123
    /* txn 2 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 and `shift_id` = 123
/* txn 1 */ UPDATE `doctors` SET `on_call` = 0 WHERE `id` = 1 AND `shift_id` = 123
/* txn 1 */ COMMIT
```

运行结果：

```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       0 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

在两个事务中，应用程序首先检查是否有两名或以上医生值班，如果是，则认为可以安全地让一名医生请假。由于数据库使用了快照隔离，两个检查都返回了 `2`，因此两个事务都进入了下一阶段。`Alice` 将自己的记录更新为不值班，`Bob` 也做了同样的操作。两个事务都成功提交。现在没有医生值班，违反了至少有一名医生值班的要求。下图（引用自 **_Designing Data-Intensive Applications_**）展示了实际发生的情况。

![Write Skew](/media/develop/write-skew.png)

现在我们将示例程序改为使用 `SELECT FOR UPDATE`，以避免写偏差问题：

<SimpleTab groupId="language">

<div label="Java" value="java">

```java
// 代码略，保持原文
```

</div>

<div label="Golang" value="golang">

```go
// 代码略，保持原文
```

</div>

</SimpleTab>

SQL 日志：

```sql
/* txn 1 */ BEGIN
    /* txn 2 */ BEGIN
    /* txn 2 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE on_call = 1 AND `shift_id` = 123 FOR UPDATE
    /* txn 2 */ UPDATE `doctors` SET on_call = 0 WHERE `id` = 2 AND `shift_id` = 123
    /* txn 2 */ COMMIT
/* txn 1 */ SELECT COUNT(*) AS `count` FROM `doctors` WHERE `on_call` = 1 FOR UPDATE
At least one doctor is on call
/* txn 1 */ ROLLBACK
```

运行结果：

```sql
mysql> SELECT * FROM doctors;
+----+-------+---------+----------+
| id | name  | on_call | shift_id |
+----+-------+---------+----------+
|  1 | Alice |       1 |      123 |
|  2 | Bob   |       0 |      123 |
|  3 | Carol |       0 |      123 |
+----+-------+---------+----------+
```

## 对 `savepoint` 和嵌套事务的支持

> **注意：**
>
> 从 v6.2.0 开始，TiDB 支持 [`savepoint`](/sql-statements/sql-statement-savepoint.md) 功能。如果你的 TiDB 集群版本低于 v6.2.0，则不支持 `PROPAGATION_NESTED` 行为。建议升级到 v6.2.0 或更高版本。如果无法升级 TiDB，并且你的应用基于 **Java Spring** 框架且使用了 `PROPAGATION_NESTED` 传播行为，则需要在应用侧适配，移除嵌套事务的相关逻辑。

**Spring** 支持的 `PROPAGATION_NESTED` 传播行为会触发一个嵌套事务，即独立于当前事务启动的子事务。嵌套事务开始时会记录一个 `savepoint`。如果嵌套事务失败，事务会回滚到 `savepoint` 状态。嵌套事务属于外部事务的一部分，会与外部事务一起提交。

下面的示例演示了 `savepoint` 机制：

```sql
mysql> BEGIN;
mysql> INSERT INTO T2 VALUES(100);
mysql> SAVEPOINT svp1;
mysql> INSERT INTO T2 VALUES(200);
mysql> ROLLBACK TO SAVEPOINT svp1;
mysql> RELEASE SAVEPOINT svp1;
mysql> COMMIT;
mysql> SELECT * FROM T2;
+------+
|  ID   |
+------+
|  100 |
+------+
```

## 大事务限制

基本原则是限制事务的大小。在 KV 层，TiDB 对单个事务的大小有限制。在 SQL 层，一行数据映射为一个 KV entry，每增加一个索引会多一个 KV entry。SQL 层的限制如下：

- 单行记录的最大大小为 120 MiB。

    - 你可以通过 [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 配置参数调整（适用于 TiDB v4.0.10 及更高 v4.0.x 版本、TiDB v5.0.0 及更高版本）。v4.0.10 之前的版本该值为 `6 MB`。
    - 从 v7.6.0 开始，你可以使用 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) 系统变量动态修改该配置项的值。

- 单个事务支持的最大大小为 1 TiB。

    - 对于 TiDB v4.0 及更高版本，可以通过 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 配置。更早版本该值为 `100 MB`。
    - 对于 TiDB v6.5.0 及更高版本，不再推荐使用该配置。详情参见 [`performance.txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)。

注意，无论是大小限制还是行数限制，你还需要考虑事务执行过程中编码和额外 key 的开销。为获得最佳性能，建议每 100 ~ 500 行写入一次事务。

## 自动提交的 `SELECT FOR UPDATE` 语句不会等待锁

目前，自动提交的 `SELECT FOR UPDATE` 语句不会加锁。下图展示了在两个独立会话中的效果：

![The situation in TiDB](/media/develop/autocommit_selectforupdate_nowaitlock.png)

这是一个已知的与 MySQL 不兼容的问题。你可以通过显式使用 `BEGIN;COMMIT;` 语句来解决该问题。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
