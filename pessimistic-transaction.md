---
title: TiDB 悲观事务模式
summary: 了解 TiDB 中的悲观事务模式。
---

# TiDB 悲观事务模式

为了让 TiDB 的使用更接近传统数据库并降低迁移成本，从 v3.0 版本开始，TiDB 在乐观事务模型的基础上支持悲观事务模式。本文档描述了 TiDB 悲观事务模式的特性。

> **Note:**
>
> 从 v3.0.8 版本开始，新创建的 TiDB 集群默认使用悲观事务模式。然而，这不会影响你将现有集群从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本时的行为。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 切换事务模式

你可以通过配置 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) 系统变量来设置事务模式。以下命令将集群中新创建会话执行的所有显式事务（即非自动提交事务）设置为悲观事务模式：

```sql
SET GLOBAL tidb_txn_mode = 'pessimistic';
```

你也可以通过执行以下 SQL 语句显式启用悲观事务模式：

```sql
BEGIN PESSIMISTIC;
```

```sql
BEGIN /*T! PESSIMISTIC */;
```

`BEGIN PESSIMISTIC;` 和 `BEGIN OPTIMISTIC;` 语句优先于 `tidb_txn_mode` 系统变量。使用这两个语句启动的事务会忽略系统变量，支持同时使用悲观和乐观事务模式。

## 行为特性

TiDB 中的悲观事务行为与 MySQL 类似。关于与 MySQL InnoDB 的细微差异，请参见 [Differences from MySQL InnoDB](#differences-from-mysql-innodb)。

- 对于悲观事务，TiDB 引入了快照读和当前读。

    - 快照读：是一种未加锁的读取，读取事务开始前已提交的版本。在 `SELECT` 语句中的读取即为快照读。
    - 当前读：是一种加锁的读取，读取最新已提交的版本。在 `UPDATE`、`DELETE`、`INSERT` 或 `SELECT FOR UPDATE` 语句中的读取即为当前读。

    以下示例详细描述了快照读和当前读。

    | 会话 1 | 会话 2 | 会话 3 |
    | :----| :---- | :---- |
    | CREATE TABLE t (a INT); |  |  |
    | INSERT INTO T VALUES(1); |  |  |
    | BEGIN PESSIMISTIC; |  |  |
    | UPDATE t SET a = a + 1; |  |  |
    |  | BEGIN PESSIMISTIC; |  |
    |  | SELECT * FROM t;  -- 使用快照读读取事务开始前已提交的版本，结果返回 a=1。 |  |
    |  |  | BEGIN PESSIMISTIC; |
    |  |  | SELECT * FROM t FOR UPDATE; -- 使用当前读，等待锁。  |
    | COMMIT; -- 释放锁。会话 3 的 SELECT FOR UPDATE 操作获得锁，TiDB 使用当前读读取最新已提交的版本，结果返回 a=2。 |  |  |
    |  | SELECT * FROM t; -- 使用快照读读取事务开始前已提交的版本，结果返回 a=1。 |  |

- 当你执行 `UPDATE`、`DELETE` 或 `INSERT` 语句时，会读取**最新**已提交的数据，修改数据，并对修改的行应用悲观锁。

- 对于 `SELECT FOR UPDATE` 语句，会在最新版本的已提交数据上加悲观锁，而不是在被修改的行上。

- 锁会在事务提交或回滚时释放。其他试图修改数据的事务会被阻塞，等待锁释放。试图**读取**数据的事务不会被阻塞，因为 TiDB 使用多版本并发控制（MVCC）。

- 你可以设置系统变量 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 来控制是否跳过带有唯一约束检查的悲观锁。详情请参见 [constraints](/constraints.md#pessimistic-transactions)。

- 如果多个事务试图获取彼此的锁，将会发生死锁。系统会自动检测到死锁，并随机终止其中一个事务，返回 MySQL 兼容的错误码 `1213`。

- 事务在尝试获取新锁时最多等待 `innodb_lock_wait_timeout` 秒（默认：50 秒）。当超时后，会返回 MySQL 兼容的错误码 `1205`。如果多个事务等待同一把锁，优先级大致根据事务的 `start ts` 来决定。

- TiDB 支持在同一集群中同时使用乐观事务模式和悲观事务模式。你可以为事务执行指定任意一种模式。

- TiDB 支持 `FOR UPDATE NOWAIT` 语法，不会阻塞等待锁释放，而是返回 MySQL 兼容的错误码 `3572`。

- 如果 `Point Get` 和 `Batch Point Get` 操作没有读取数据，它们仍会锁定给定的主键或唯一键，从而阻止其他事务锁定或写入相同的主键或唯一键。

- TiDB 支持 `FOR UPDATE OF TABLES` 语法。对于连接多个表的语句，TiDB 只会对与 `OF TABLES` 中表相关的行加悲观锁。

## 与 MySQL InnoDB 的差异

1. 当 TiDB 执行带范围条件的 DML 或 `SELECT FOR UPDATE` 语句时，范围内的并发 DML 不会被阻塞。

    例如：

    ```sql
    CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY,
     pad1 VARCHAR(100)
    );
    INSERT INTO t1 (id) VALUES (1),(5),(10);
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    SELECT * FROM t1 WHERE id BETWEEN 1 AND 10 FOR UPDATE;
    ```

    ```sql
    BEGIN /*T! PESSIMISTIC */;
    INSERT INTO t1 (id) VALUES (6); -- 只在 MySQL 中阻塞
    UPDATE t1 SET pad1='new value' WHERE id = 5; -- 在 MySQL 和 TiDB 中等待阻塞
    ```

    这是因为 TiDB 目前不支持 _gap locking_。

2. TiDB 不支持 `SELECT LOCK IN SHARE MODE`。

    TiDB 默认不支持 `SELECT LOCK IN SHARE MODE` 语法。你可以启用 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) 以使 TiDB 兼容 `SELECT LOCK IN SHARE MODE` 语法。执行 `SELECT LOCK IN SHARE MODE` 与不加锁的效果相同，不会阻塞其他事务的读写操作。

    从 v8.3.0 版本开始，TiDB 支持通过 [`tidb_enable_shared_lock_promotion`](/system-variables.md#tidb_enable_shared_lock_promotion-new-in-v830) 系统变量启用 `SELECT LOCK IN SHARE MODE` 添加锁，但此时添加的锁并非真正的共享锁，而是与 `SELECT FOR UPDATE` 一致的排他锁。如果你希望在保持 TiDB 兼容 `SELECT LOCK IN SHARE MODE` 语法的同时，阻止写操作以避免在读取期间被写事务并发修改，可以启用此变量。启用后，该变量对 `SELECT LOCK IN SHARE MODE` 语句生效，无论 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) 是否启用。

3. DDL 可能导致悲观事务提交失败。

    在 MySQL 中执行 DDL 时，可能会被正在执行的事务阻塞。而在 TiDB 中，DDL 不会被阻塞，可能导致悲观事务提交失败：`ERROR 1105 (HY000): Information schema is changed. [try again later]`。在事务执行过程中，TiDB 会执行 `TRUNCATE TABLE` 语句，可能会导致 `table doesn't exist` 错误。

4. 执行 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 后，MySQL 仍然可以在其他事务中读取后续创建的表，而 TiDB 不行。

5. 自动提交事务偏好乐观锁。

    在使用悲观模型时，自动提交事务会优先尝试使用开销较小的乐观模型提交语句。如果发生写冲突，会使用悲观模型进行事务重试。因此，如果 `tidb_retry_limit` 设置为 `0`，在发生写冲突时，自动提交事务仍会返回 `Write Conflict` 错误。

    自动提交的 `SELECT FOR UPDATE` 语句不会等待锁。

6. 语句中的 `EMBEDDED SELECT` 所读取的数据不会被锁定。

7. TiDB 中的开启事务不会阻塞垃圾回收（GC）。默认情况下，这将悲观事务的最大执行时间限制为 1 小时。你可以通过修改 TiDB 配置文件中的 `[performance]` 下的 `max-txn-ttl` 来调整此限制。

## 隔离级别

TiDB 在悲观事务模式下支持以下两种隔离级别：

- [Repeatable Read](/transaction-isolation-levels.md#repeatable-read-isolation-level)，与 MySQL 相同。

    > **Note:**
    >
    > 在此隔离级别下，DML 操作基于最新已提交的数据执行。行为与 MySQL 相同，但与 TiDB 中的乐观事务模式不同。详见 [Difference between TiDB and MySQL Repeatable Read](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)。

- [Read Committed](/transaction-isolation-levels.md#read-committed-isolation-level)。你可以通过 [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) 语句设置此隔离级别。

## 悲观事务提交流程

在事务提交流程中，悲观事务和乐观事务的逻辑相同。两者都采用两阶段提交（2PC）模式。悲观事务的关键适配在于 DML 执行。

![TiDB 悲观事务提交流程](/media/pessimistic-transaction-commit.png)

悲观事务在 2PC 之前增加了 `Acquire Pessimistic Lock` 阶段，包括以下步骤：

1. （与乐观事务模式相同）TiDB 接收来自客户端的 `begin` 请求，此时的当前时间戳即为该事务的 start_ts。
2. 当 TiDB 服务器收到客户端的写入请求时，会向 TiKV 服务器发起悲观锁请求，锁信息会被持久化到 TiKV 服务器。
3. （与乐观事务模式相同）当客户端发出提交请求时，TiDB 开始执行类似乐观事务的两阶段提交。

![TiDB 中的悲观事务](/media/pessimistic-transaction-in-tidb.png)

## 管道化锁定流程

增加悲观锁需要将数据写入 TiKV。成功添加锁的响应只有在提交并通过 Raft 应用后才能返回给 TiDB。因此，与乐观事务相比，悲观事务模式不可避免地具有更高的延迟。

为了减少锁的开销，TiKV 实现了管道化锁定流程：当数据满足锁定条件时，TiKV 会立即通知 TiDB 执行后续请求，并异步写入悲观锁。此流程大大减少了延迟，并显著提升了悲观事务的性能。然而，当 TiKV 出现网络分区或某个 TiKV 节点宕机时，异步写入悲观锁可能失败，影响以下方面：

* 其他修改相同数据的事务无法被阻塞。如果应用逻辑依赖锁或等待锁机制，可能影响逻辑正确性。

* 发生事务提交失败的概率较低，但不影响事务的正确性。

<CustomContent platform="tidb">

如果你的应用逻辑依赖锁或等待锁机制，或者你希望在 TiKV 集群异常情况下尽可能保证事务提交成功率，应禁用管道化锁定功能。

![管道化悲观锁](/media/pessimistic-transaction-pipelining.png)

此功能默认启用。若要禁用，可修改 TiKV 配置：

```toml
[pessimistic-txn]
pipelined = false
```

如果 TiKV 集群为 v4.0.9 及以上版本，也可以通过 [动态修改 TiKV 配置](/dynamic-config.md#modify-tikv-configuration-dynamically) 来禁用：

```sql
set config tikv pessimistic-txn.pipelined='false';
```

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你的应用逻辑依赖锁或等待锁机制，或者你希望在 TiKV 集群异常情况下尽可能保证事务提交成功率，可以 [联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 来禁用管道化锁定功能。

</CustomContent>

## 内存悲观锁

在 v6.0.0 版本中，TiKV 引入了内存悲观锁功能。启用此功能后，悲观锁通常只存储在 Region 领导者的内存中，不会持久化到磁盘，也不会通过 Raft 复制到其他副本。此功能可以大大降低获取悲观锁的开销，提高悲观事务的吞吐量。

<CustomContent platform="tidb">

当内存悲观锁的内存使用超过 [Region](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840) 或 [TiKV 节点](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) 的内存阈值时，获取悲观锁将切换到 [管道化锁定流程](#pipelined-locking-process)。当 Region 合并或领导者转移时，为避免悲观锁丢失，TiKV 会将内存中的悲观锁写入磁盘并复制到其他副本。

</CustomContent>

<CustomContent platform="tidb-cloud">

当内存悲观锁的内存使用超过 [Region](https://docs.pingcap.com/tidb/dev/tikv-configuration-file#in-memory-peer-size-limit-new-in-v840) 或 [TiKV 节点](https://docs.pingcap.com/tidb/dev/tikv-configuration-file#in-memory-instance-size-limit-new-in-v840) 的内存阈值时，获取悲观锁将切换到 [管道化锁定流程](#pipelined-locking-process)。当 Region 合并或领导者转移时，为避免悲观锁丢失，TiKV 会将内存中的悲观锁写入磁盘并复制到其他副本。

</CustomContent>

内存悲观锁的表现与管道化锁定流程类似，在集群健康时不会影响锁的获取。然而，当 TiKV 出现网络隔离或某个节点宕机时，已获取的悲观锁可能会丢失。

如果你的应用逻辑依赖锁的获取或等待机制，或者你希望在集群异常时尽可能保证事务提交成功率，需要**禁用**内存悲观锁功能。

此功能默认启用。若要禁用，可修改 TiKV 配置：

```toml
[pessimistic-txn]
in-memory = false
```

也可以通过 [动态修改 TiKV 配置](/dynamic-config.md#modify-tikv-configuration-dynamically) 来禁用：

```sql
set config tikv pessimistic-txn.in-memory='false';
```

<CustomContent platform="tidb">

从 v8.4.0 版本开始，你可以使用 [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-new-in-v840) 或 [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-new-in-v840) 来配置内存悲观锁的内存使用限制：

```toml
[pessimistic-txn]
in-memory-peer-size-limit = "512KiB"
in-memory-instance-size-limit = "100MiB"
```

要动态修改这些限制，可以使用 [动态修改 TiKV 配置](/dynamic-config.md#modify-tikv-configuration-dynamically)：

```sql
SET CONFIG tikv `pessimistic-txn.in-memory-peer-size-limit`="512KiB";
SET CONFIG tikv `pessimistic-txn.in-memory-instance-size-limit`="100MiB";
```

</CustomContent>