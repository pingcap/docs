---
title: TiDB 乐观事务模型
summary: 了解 TiDB 中的乐观事务模型。
---

# TiDB 乐观事务模型

采用乐观事务时，冲突的变更会在事务提交时被检测到。这有助于在并发事务很少修改相同行的情况下提高性能，因为可以跳过获取行锁的过程。在并发事务频繁修改相同行（冲突）的情况下，乐观事务可能比 [Pessimistic Transactions](/pessimistic-transaction.md) 表现更差。

在启用乐观事务之前，请确保你的应用程序正确处理 `COMMIT` 语句可能返回的错误。如果你不确定你的应用程序如何处理，建议改用 Pessimistic Transactions。

> **Note:**
>
> 从 v3.0.8 版本开始，TiDB 默认使用 [pessimistic transaction mode](/pessimistic-transaction.md)。但这不会影响你从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本的现有集群。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 乐观事务的原理

为了支持分布式事务，TiDB 在乐观事务中采用两阶段提交（2PC）。其流程如下：

![2PC in TiDB](/media/2pc-in-tidb.png)

1. 客户端开始一个事务。

    TiDB 从 PD 获取一个时间戳（单调递增且全局唯一），作为当前事务的唯一事务ID，称为 `start_ts`。TiDB 实现了多版本并发控制（MVCC），因此 `start_ts` 也作为该事务所获得的数据库快照的版本。这意味着事务只能读取在 `start_ts` 时刻的数据库数据。

2. 客户端发起读取请求。

    1. TiDB 从 PD 获取路由信息（数据在 TiKV 节点间的分布情况）。
    2. TiDB 从 TiKV 获取 `start_ts` 版本的数据。

3. 客户端发起写入请求。

    TiDB 检查写入的数据是否满足约束（确保数据类型正确，满足 NOT NULL 约束）。**有效数据存储在 TiDB 事务的私有内存中**。

4. 客户端发起提交请求。

5. TiDB 开始 2PC，并在存储中持久化数据，同时保证事务的原子性。

    1. TiDB 从待写入的数据中选择一个主键（Primary Key）。
    2. TiDB 从 PD 获取 Region 分布信息，并将所有键按 Region 分组。
    3. TiDB 向所有涉及的 TiKV 节点发送 prewrite 请求。然后，TiKV 检查是否存在冲突或过期版本。有效数据被锁定。
    4. TiDB 收到所有 prewrite 阶段的响应，prewrite 成功。
    5. TiDB 从 PD 获取提交版本号，并标记为 `commit_ts`。
    6. TiDB 向主键所在的 TiKV 节点发起第二阶段提交。TiKV 检查数据，并清理 prewrite 阶段留下的锁。
    7. TiDB 收到第二阶段成功完成的通知。

6. TiDB 返回消息，通知客户端事务已成功提交。

7. TiDB 异步清理该事务留下的锁。

## 优缺点

从上述 TiDB 事务的流程可以看出，TiDB 事务具有以下优点：

* 易于理解
* 基于单行事务实现跨节点事务
* 去中心化的锁管理

但 TiDB 事务也存在以下缺点：

* 由于 2PC 导致的事务延迟
* 需要集中式的时间戳分配服务
* 在大量数据写入内存时可能出现 OOM（内存溢出）

## 事务重试

> **Note:**
>
> 从 v8.0.0 版本开始，系统变量 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 已被废弃，TiDB 不再支持乐观事务的自动重试。建议使用 [Pessimistic transaction mode](/pessimistic-transaction.md)。如果遇到乐观事务冲突，可以捕获错误并在应用层重试事务。

在乐观事务模型中，由于写入冲突，事务可能无法提交，特别是在高争用场景下。TiDB 默认采用乐观并发控制，而 MySQL 则应用悲观并发控制。这意味着 MySQL 在执行写操作的 SQL 语句时会加锁，其 Repeatable Read 隔离级别允许当前读取，因此提交时通常不会遇到异常。为了降低应用适配难度，TiDB 提供了内部重试机制。

### 自动重试

如果在事务提交过程中发生写写冲突，TiDB 会自动重试包含写操作的 SQL 语句。你可以通过设置 `tidb_disable_txn_auto_retry` 为 `OFF` 来启用自动重试，并通过配置 `tidb_retry_limit` 来设置重试次数限制：

```toml
# Whether to disable automatic retry. ("on" by default)
tidb_disable_txn_auto_retry = OFF
# Set the maximum number of the retries. ("10" by default)
# When "tidb_retry_limit = 0", automatic retry is completely disabled.
tidb_retry_limit = 10
```

你可以在会话级别或全局级别启用自动重试：

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

> **Note:**
>
> `tidb_retry_limit` 变量决定最大重试次数。当设置为 `0` 时，所有事务（包括自动提交的隐式单语句事务）都不会自动重试。这是完全禁用 TiDB 自动重试机制的方式。禁用后，所有冲突事务会以最快速度向应用层报告失败（包括 `try again later` 消息）。

### 重试的限制

默认情况下，TiDB 不会重试事务，以避免出现丢失更新和破坏 [`REPEATABLE READ` isolation](/transaction-isolation-levels.md)。

重试流程如下：

1. 分配一个新时间戳，标记为 `start_ts`。
2. 重试包含写操作的 SQL 语句。
3. 实现两阶段提交。

在第 2 步中，TiDB 只会重试包含写操作的 SQL 语句。然而，在重试过程中，TiDB 会获取一个新的版本号，标记事务的开始。这意味着 TiDB 会用新的 `start_ts` 版本中的数据重试 SQL 语句。如果事务使用其他查询结果更新数据，可能会导致结果不一致，因为违反了 `REPEATABLE READ` 隔离级别。

如果你的应用可以容忍丢失更新，并且不需要 `REPEATABLE READ` 一致性，可以通过设置 `tidb_disable_txn_auto_retry = OFF` 来启用此功能。

## 冲突检测

作为一个分布式数据库，TiDB 在 TiKV 层进行内存中的冲突检测，主要在 prewrite 阶段。TiDB 实例是无状态的，彼此不知情，这意味着它们无法知道其写入是否在集群中引发冲突。因此，冲突检测在 TiKV 层进行。

配置如下：

```toml
# Controls the number of slots. ("2048000" by default）
scheduler-concurrency = 2048000
```

此外，TiKV 还支持监控调度器中等待锁的时间。

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 较高且没有慢写时，可以安全地判断此时存在大量写冲突。