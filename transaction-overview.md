---
title: 事务
summary: 了解 TiDB 中的事务。
---

# 事务

TiDB 支持使用 [pessimistic](/pessimistic-transaction.md) 或 [optimistic](/optimistic-transaction.md) 事务模式进行分布式事务。从 TiDB 3.0.8 版本开始，TiDB 默认使用 pessimistic 事务模式。

本文档介绍常用的事务相关语句、显式和隐式事务、隔离级别、惰性约束检查以及事务大小。

常用变量包括 [`autocommit`](#autocommit)、[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)、[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 和 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)。

> **注意：**
>
> [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 和 [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 变量仅适用于 optimistic 事务，不适用于 pessimistic 事务。

## 常用语句

### 开始事务

语句 [`BEGIN`](/sql-statements/sql-statement-begin.md) 和 [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) 可以互换使用，用于显式开启一个新事务。

语法：


```sql
BEGIN;
```


```sql
START TRANSACTION;
```


```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```


```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

如果在执行这些语句时，当前会话正处于事务中，TiDB 会在开始新事务之前自动提交当前事务。

> **注意：**
>
> 与 MySQL 不同，TiDB 在执行上述语句后会对当前数据库进行快照。MySQL 的 `BEGIN` 和 `START TRANSACTION` 在执行第一个读取数据的 `SELECT` 语句（非 `SELECT FOR UPDATE`）后获取快照，而 TiDB 在执行上述语句时立即获取快照。`START TRANSACTION WITH CONSISTENT SNAPSHOT` 在执行语句过程中获取快照。因此，在 MySQL 中，`BEGIN`、`START TRANSACTION` 和 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 等价于 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。

### 提交事务

语句 [`COMMIT`](/sql-statements/sql-statement-commit.md) 指示 TiDB 将当前事务中的所有更改应用到数据库。

语法：


```sql
COMMIT;
```

> **提示：**
>
> 在启用 [optimistic 事务](/optimistic-transaction.md) 之前，请确保你的应用正确处理 `COMMIT` 语句可能返回的错误。如果你不确定你的应用如何处理，建议使用默认的 [pessimistic 事务](/pessimistic-transaction.md)。

### 回滚事务

语句 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 会回滚并取消当前事务中的所有更改。

语法：


```sql
ROLLBACK;
```

如果客户端连接中断或关闭，事务也会自动回滚。

## Autocommit

为了兼容 MySQL，TiDB 默认会在执行完语句后立即 _autocommit_。

例如：

```sql
mysql> CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+------+
| id | pad1 |
+----+------+
|  1 | test |
+----+------+
1 row in set (0.00 sec)
```

在上述示例中，`ROLLBACK` 语句没有效果。这是因为 `INSERT` 语句在 autocommit 模式下执行。也就是说，它相当于以下单条语句事务：

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

如果显式开启了事务，autocommit 不会生效。在下面的示例中，`ROLLBACK` 成功撤销了 `INSERT` 语句：


```sql
mysql> CREATE TABLE t2 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t2 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

系统变量 [`autocommit`](/system-variables.md#autocommit) 可以在全局或会话级别进行修改。

例如：


```sql
SET autocommit = 0;
```


```sql
SET GLOBAL autocommit = 0;
```

## 显式与隐式事务

> **注意：**
>
> 有些语句会隐式提交。例如，执行 `[BEGIN|START TRANSACTION]` 会隐式提交上一个事务并开启新事务。这种行为是 MySQL 兼容性所必需的。详情请参见 [隐式提交](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

TiDB 支持显式事务（使用 `[BEGIN|START TRANSACTION]` 和 `COMMIT` 来定义事务的开始和结束）以及隐式事务（`SET autocommit = 1`）。

如果你将 `autocommit` 设置为 `1`，并通过 `[BEGIN|START TRANSACTION]` 语句开启新事务，`COMMIT` 或 `ROLLBACK` 之前会禁用 autocommit，使事务变为显式事务。

对于 DDL 语句，事务会自动提交，不支持回滚。如果在当前会话正处于事务中时执行 DDL 语句，DDL 会在当前事务提交后执行。

## 惰性检查约束

默认情况下，optimistic 事务在执行 DML 语句时不会检查 [主键](/constraints.md#primary-key) 或 [唯一约束](/constraints.md#unique-key)，这些检查会在事务 [`COMMIT`] 时进行。

例如：


```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
BEGIN OPTIMISTIC;
INSERT INTO t1 VALUES (1); -- MySQL 返回错误；TiDB 返回成功。
INSERT INTO t1 VALUES (2);
COMMIT; -- 在 MySQL 中成功提交；在 TiDB 中返回错误，事务回滚。
SELECT * FROM t1; -- MySQL 返回 1 2；TiDB 返回 1。
```

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> BEGIN OPTIMISTIC;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1); -- MySQL 返回错误；TiDB 返回成功。
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (2);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT; -- 在 MySQL 中成功提交；在 TiDB 中返回错误，事务回滚。
ERROR 1062 (23000): Duplicate entry '1' for key 't1.PRIMARY'
mysql> SELECT * FROM t1; -- MySQL 返回 1 2；TiDB 返回 1。
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

惰性检查优化通过批量进行约束检查和减少网络通信提升性能。可以通过设置 [`tidb_constraint_check_in_place=ON`](/system-variables.md#tidb_constraint_check_in_place) 来禁用此优化。

> **注意：**
>
> + 该优化仅适用于 optimistic 事务。
> + 该优化不适用于 `INSERT IGNORE` 和 `INSERT ON DUPLICATE KEY UPDATE`，只对普通 `INSERT` 语句生效。

## 语句回滚

TiDB 支持在语句执行失败后进行原子回滚。如果某个语句导致错误，它所做的更改不会生效。事务会保持开启状态，可以在发出 `COMMIT` 或 `ROLLBACK` 之前继续进行其他更改。


```sql
CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
BEGIN;
INSERT INTO test VALUES (1);
INSERT INTO tset VALUES (2);  -- 语句不生效，因为 "test" 拼写为 "tset"。
INSERT INTO test VALUES (1),(2);  -- 整个语句不生效，因为违反了 PRIMARY KEY 约束
INSERT INTO test VALUES (3);
COMMIT;
SELECT * FROM test;
```

```sql
mysql> CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.09 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO test VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO tset VALUES (2);  -- 语句不生效，因为 "test" 拼写为 "tset"。
ERROR 1146 (42S02): Table 'test.tset' doesn't exist
mysql> INSERT INTO test VALUES (1),(2);  -- 整个语句不生效，因为违反了 PRIMARY KEY 约束
ERROR 1062 (23000): Duplicate entry '1' for key 'test.PRIMARY'
mysql> INSERT INTO test VALUES (3);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM test;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

在上述示例中，失败的 `INSERT` 语句不会影响事务的提交，事务仍然保持开启状态，最后成功的 `INSERT` 语句会将更改提交。

## 事务大小限制

由于底层存储引擎的限制，TiDB 要求单行数据不得超过 6 MB。所有列的数据会根据其数据类型转换为字节，并累计估算单行的大小。

TiDB 支持 optimistic 和 pessimistic 事务，optimistic 事务是 pessimistic 事务的基础。由于 optimistic 事务会将更改缓存到私有内存中，TiDB 限制单个事务的大小。

默认情况下，TiDB 将单个事务的总大小限制为不超过 100 MB。你可以通过配置文件中的 `txn-total-size-limit` 修改此默认值。`txn-total-size-limit` 的最大值为 1 TB。单个事务的大小限制还取决于服务器剩余可用内存的大小。这是因为在执行事务时，TiDB 进程的内存使用会随着事务大小线性增长，最多可能达到事务大小的两到三倍甚至更多。

TiDB 之前限制单个事务的 key-value 对总数为 30 万个，此限制在 TiDB v4.0 版本中已被取消。

## 因果一致性

> **注意：**
>
> 具有因果一致性的事务只有在启用异步提交和单阶段提交功能后才会生效。关于这两个功能的详细信息，请参见 [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50) 和 [`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50)。

TiDB 支持启用事务的因果一致性。启用因果一致性的事务在提交时，无需从 PD 获取时间戳，且提交延迟较低。启用因果一致性的语法如下：


```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

默认情况下，TiDB 保证线性一致性。在线性一致性下，如果事务 2 在事务 1 提交后才提交，逻辑上事务 2 应该发生在事务 1 之后。因果一致性比线性一致性弱。在因果一致性下，只有当事务 1 和事务 2 之间存在锁定或写入的交集（即两个事务之间存在数据库已知的因果关系）时，事务的提交顺序和发生顺序才能保证一致。当前，TiDB 不支持传入外部的因果关系。

启用因果一致性的两个事务具有以下特性：

+ [潜在因果关系的事务具有一致的逻辑顺序和物理提交顺序](#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order)
+ [无因果关系的事务不保证一致的逻辑顺序和物理提交顺序](#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order)
+ [无锁读取不创建因果关系](#reads-without-lock-do-not-create-causal-relationship)

### 潜在因果关系的事务具有一致的逻辑顺序和物理提交顺序

假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE | |
| UPDATE t set v = $(x + 1) WHERE id = 2 | |
| COMMIT | |
| | UPDATE t SET v = 2 WHERE id = 1 |
| | COMMIT |

在上述示例中，事务 1 锁定了 `id = 1` 的记录，事务 2 修改了 `id = 1` 的记录。因此，事务 1 和事务 2 存在潜在的因果关系。即使启用了因果一致性，只要事务 2 在事务 1 成功提交后才提交，逻辑上事务 2 必须发生在事务 1 之后。因此，不可能在没有读取事务 1 对 `id = 2` 记录的修改的情况下，读取到事务 2 对 `id = 1` 记录的修改。

### 无因果关系的事务不保证一致的逻辑顺序和物理提交顺序

假设 `id = 1` 和 `id = 2` 的初始值都为 `0`。假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 | 事务 3 |
|-------|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | |
| UPDATE t set v = 3 WHERE id = 2 | | |
| | UPDATE t SET v = 2 WHERE id = 1 | |
| | | BEGIN |
| COMMIT | | |
| | COMMIT | |
| | | SELECT v FROM t WHERE id IN (1, 2) |

在上述示例中，事务 1 没有读取 `id = 1` 的记录，因此事务 1 和事务 2 对数据库来说没有因果关系。即使在启用因果一致性的情况下，事务 2 在物理时间顺序上在事务 1 之后提交，TiDB 也不保证事务 2 在逻辑上发生在事务 1 之后。

如果事务 3 在事务 1 提交之前开始，并且在事务 2 提交后读取 `id = 1` 和 `id = 2` 记录，可能会读取到 `id = 1` 为 `2`，而 `id = 2` 仍为 `0`。

### 无锁读取不创建因果关系

假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1 | |
| UPDATE t set v = 3 WHERE id = 2 | |
| | COMMIT |
| COMMIT | |

在上述示例中，无锁读取不创建因果关系。事务 1 和事务 2 之间存在写入偏差（write skew）。在这种情况下，如果两笔事务仍然具有因果关系，将是不合理的。因此，启用因果一致性的两个事务之间没有确定的逻辑顺序。