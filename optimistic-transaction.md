---
title: TiDB Optimistic Transaction Model
summary: 了解 TiDB 中的乐观事务模型。
---

# TiDB 乐观事务模型

在乐观事务中，冲突的变更会在事务提交阶段被检测出来。当并发事务很少修改相同行时，这有助于提升性能，因为可以跳过获取行锁的过程。如果并发事务频繁修改相同行（即发生冲突），乐观事务的性能可能会比 [悲观事务](/pessimistic-transaction.md) 更差。

在启用乐观事务之前，请确保你的应用程序能够正确处理 `COMMIT` 语句可能返回的错误。如果你不确定应用程序的处理方式，建议使用悲观事务。

> **注意：**
>
> 从 v3.0.8 开始，TiDB 默认使用 [悲观事务模式](/pessimistic-transaction.md)。但如果你是从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，这一更改不会影响现有集群。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 乐观事务的原理

为了支持分布式事务，TiDB 在乐观事务中采用了两阶段提交（2PC）。流程如下：

![2PC in TiDB](/media/2pc-in-tidb.png)

1. 客户端开始一个事务。

    TiDB 从 PD 获取一个时间戳（单调递增且全局唯一），作为当前事务的唯一事务 ID，称为 `start_ts`。TiDB 实现了多版本并发控制，因此 `start_ts` 也作为该事务获取的数据库快照的版本。这意味着该事务只能读取 `start_ts` 时刻数据库中的数据。

2. 客户端发起读请求。

    1. TiDB 从 PD 获取路由信息（数据在 TiKV 节点间的分布情况）。
    2. TiDB 从 TiKV 获取 `start_ts` 版本的数据。

3. 客户端发起写请求。

    TiDB 检查写入的数据是否满足约束条件（确保数据类型正确、满足 NOT NULL 约束）。**合法的数据会存储在 TiDB 中该事务的私有内存中**。

4. 客户端发起提交请求。

5. TiDB 开始两阶段提交，并在保证事务原子性的同时将数据持久化到存储中。

    1. TiDB 从待写入的数据中选择一个主键（Primary Key）。
    2. TiDB 从 PD 获取 Region 分布信息，并按 Region 对所有 key 进行分组。
    3. TiDB 向所有涉及的 TiKV 节点发送 prewrite 请求。随后，TiKV 检查是否存在冲突或过期的版本。合法数据会被加锁。
    4. TiDB 收到 prewrite 阶段的所有响应，prewrite 成功。
    5. TiDB 从 PD 获取一个提交版本号，标记为 `commit_ts`。
    6. TiDB 向主键所在的 TiKV 节点发起第二次提交。TiKV 检查数据，并清理 prewrite 阶段遗留的锁。
    7. TiDB 收到第二阶段成功完成的消息。

6. TiDB 返回消息，通知客户端事务已成功提交。

7. TiDB 异步清理本次事务遗留的锁。

## 优缺点

从上述 TiDB 事务的流程可以看出，TiDB 事务具有以下优点：

* 易于理解
* 基于单行事务实现跨节点事务
* 去中心化的锁管理

但 TiDB 事务也存在以下缺点：

* 由于两阶段提交导致的事务延迟
* 需要一个中心化的时间戳分配服务
* 当内存中写入大量数据时，可能发生 OOM（内存溢出）

## 事务重试

> **注意：**
>
> 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 系统变量已废弃，TiDB 不再支持乐观事务的自动重试。建议使用 [悲观事务模式](/pessimistic-transaction.md)。如果你遇到乐观事务冲突，可以在应用层捕获错误并重试事务。

在乐观事务模型下，在高并发争用场景中，事务可能因为写-写冲突而提交失败。从 v3.0.8 开始，TiDB 默认使用 [悲观事务模式](/pessimistic-transaction.md)，与 MySQL 一致。这意味着 TiDB 和 MySQL 在执行写类型 SQL 语句时会加锁，并且其可重复读隔离级别允许当前读，因此提交通常不会遇到异常。

### 自动重试

> **注意：**
>
> - 从 TiDB v3.0.0 开始，事务的自动重试默认关闭，因为它可能**破坏事务隔离级别**。
> - 从 TiDB v8.0.0 开始，不再支持乐观事务的自动重试。

如果在事务提交时发生写-写冲突，TiDB 会自动重试包含写操作的 SQL 语句。你可以通过将 `tidb_disable_txn_auto_retry` 设置为 `OFF` 来开启自动重试，并通过配置 `tidb_retry_limit` 设置重试次数上限：

```toml
# 是否禁用自动重试。（默认 "on"）
tidb_disable_txn_auto_retry = OFF
# 设置最大重试次数。（默认 "10"）
# 当 "tidb_retry_limit = 0" 时，完全禁用自动重试。
tidb_retry_limit = 10
```

你可以在会话级别或全局级别开启自动重试：

1. 会话级别：

    
    ```sql
    SET tidb_disable_txn_auto_retry = OFF;
    ```

    
    ```sql
    SET tidb_retry_limit = 10;
    ```

2. 全局级别：

    
    ```sql
    SET GLOBAL tidb_disable_txn_auto_retry = OFF;
    ```

    
    ```sql
    SET GLOBAL tidb_retry_limit = 10;
    ```

> **注意：**
>
> `tidb_retry_limit` 变量决定了最大重试次数。当该变量设置为 `0` 时，所有事务都不会自动重试，包括自动提交的隐式单语句事务。这是完全禁用 TiDB 自动重试机制的方式。自动重试被禁用后，所有冲突事务会以最快的方式向应用层报告失败（包括 `try again later` 消息）。

### 重试的限制

默认情况下，TiDB 不会重试事务，因为这可能导致更新丢失并破坏 [`REPEATABLE READ` 隔离级别](/transaction-isolation-levels.md)。

原因可以从重试流程中看出：

1. 分配一个新的时间戳，标记为 `start_ts`。
2. 重试包含写操作的 SQL 语句。
3. 执行两阶段提交。

在第 2 步，TiDB 只会重试包含写操作的 SQL 语句。然而，在重试过程中，TiDB 会收到一个新的版本号作为事务的起始点。这意味着 TiDB 会在新的 `start_ts` 版本下重试 SQL 语句。在这种情况下，如果事务是基于其他查询结果进行数据更新，结果可能会不一致，因为违反了 `REPEATABLE READ` 隔离级别。

如果你的应用可以容忍更新丢失，并且不需要 `REPEATABLE READ` 隔离级别的一致性，可以通过设置 `tidb_disable_txn_auto_retry = OFF` 启用该特性。

## 冲突检测

作为分布式数据库，TiDB 在 TiKV 层进行内存冲突检测，主要发生在 prewrite 阶段。TiDB 实例是无状态的，彼此之间也不了解对方的存在，这意味着它们无法知道自己的写入是否会在整个集群中产生冲突。因此，冲突检测是在 TiKV 层完成的。

相关配置如下：

```toml
# 控制槽的数量。（默认 "2048000"）
scheduler-concurrency = 2048000
```

此外，TiKV 支持监控调度器中等待 latch 的耗时。

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 较高且没有慢写入时，可以安全地判断此时存在大量写入冲突。