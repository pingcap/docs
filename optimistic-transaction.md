---
title: TiDB 乐观事务模型
summary: 了解 TiDB 中的乐观事务模型。
---

# TiDB 乐观事务模型

在乐观事务中，**冲突**的变更会在事务提交阶段被检测出来。当并发事务很少修改同一行时，这有助于提升**性能**，因为可以跳过获取行**锁**的过程。如果并发事务频繁修改同一行（发生**冲突**），乐观事务的**性能**可能会比 [悲观事务](/pessimistic-transaction.md) 更差。

在启用乐观事务之前，请确保你的应用程序能够正确**handle** `COMMIT` **statement** 可能**return**的错误。如果你不确定应用程序的处理方式，建议使用悲观事务。

> **注意：**
>
> 从 v3.0.8 开始，TiDB 默认使用 [悲观事务模式](/pessimistic-transaction.md)。但如果你是从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，则不会影响你现有的**cluster**。换句话说，**只有新创建的集群默认使用悲观事务模式**。

## 乐观事务的原理

为了支持分布式事务，TiDB 在乐观事务中采用了两阶段提交（2PC）。流程如下：

```mermaid
---
title: 2PC in TiDB
---
sequenceDiagram
    participant client
    participant TiDB
    participant PD
    participant TiKV

    client->>TiDB: begin
    TiDB->>PD: get ts as start_ts

    loop excute SQL
        alt do read
            TiDB->>PD: get region from PD or cache
            TiDB->>TiKV: get data from TiKV or cache with start_ts
            TiDB-->>client: return read result
        end
        alt do write
            TiDB-->>TiDB: write in cache
            TiDB-->>client: return write result
        end
    end

    client->>TiDB: commit

    opt start 2PC
        TiDB-->>TiDB: for all keys need to write,choose first one as primary
        TiDB->>PD: locate each key
        TiDB-->>TiDB: group keys by region to [](region,keys)

        opt prewrite with start_ts
            TiDB->>TiKV: prewrite(primary_key,start_ts)
            loop prewrite to each region in [](region,keys) parallelly
                TiDB->>TiKV: prewrite(keys,primary_key,start_ts)
            end
        end

        opt commit
            TiDB-->>PD: get ts as commit_ts
            TiDB-->>TiKV: commit primary with commit_ts
            loop send commit to each region in [](region,keys) parallelly
                TiDB->>TiKV: commit(keys,commit_ts)
            end
        end
    end

    TiDB-->>client: success
```

1. **client** 开启一个事务。

    TiDB 从 PD 获取一个**timestamp**（单调递增且**全局**唯一），作为当前事务的唯一事务 ID，称为 `start_ts`。TiDB 实现了多版本并发控制，因此 `start_ts` 也作为该事务获取的数据库**snapshot**的版本。这意味着该事务只能读取 `start_ts` 时刻数据库中的数据。

2. **client** 发起**read request**。

    1. TiDB 从 PD 获取路由信息（数据在 TiKV **node** 之间的分布方式）。
    2. TiDB 从 TiKV 获取 `start_ts` 版本的数据。

3. **client** 发起写**request**。

    TiDB 检查写入的数据是否满足**constraint**（确保数据**type**正确、NOT NULL 约束满足）。**有效数据会存储在 TiDB 中该事务的私有 memory 中**。

4. **client** 发起提交**request**。

5. TiDB 开始 2PC，并在保证事务原子性的同时将数据持久化到存储中。

    1. TiDB 从待写入的数据中选取一个 Primary Key。
    2. TiDB 从 PD 获取 Region 分布信息，并按 Region 对所有 key 进行分组。
    3. TiDB 向所有涉及的 TiKV **node** 发送 prewrite **request**。TiKV 检查是否有**冲突**或**expire**的版本，有效数据会被加锁。
    4. TiDB 收到 prewrite 阶段的所有响应，prewrite 成功。
    5. TiDB 从 PD 获取一个提交版本号，记为 `commit_ts`。
    6. TiDB 向 Primary Key 所在的 TiKV **node** 发起第二次提交。TiKV 检查数据，并清理 prewrite 阶段遗留的锁。
    7. TiDB 收到第二阶段成功完成的消息。

6. TiDB **return** 消息，通知**client**事务提交成功。

7. TiDB 异步清理本事务遗留的锁。

## 优缺点

从上述 TiDB 事务流程可以看出，TiDB 事务具有以下优点：

* 易于理解
* 基于单行事务实现跨**node**事务
* 去中心化的**lock**管理

但 TiDB 事务也有以下缺点：

* 由于 2PC 带来的事务**latency**
* 需要一个中心化的**timestamp**分配**service**
* 大量数据写入**memory**时可能导致 OOM（内存溢出）

## 事务重试

> **注意：**
>
> 从 v8.0.0 开始，[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) **system variable** 已废弃，TiDB 不再支持乐观事务的自动重试。建议使用 [悲观事务模式](/pessimistic-transaction.md)。如果遇到乐观事务**conflict**，可以在应用层捕获错误并重试事务。

在乐观事务模型下，在高**concurrency**的**scenario**中，事务可能因为写-写**conflict**而提交失败。从 v3.0.8 开始，TiDB 默认使用 [悲观事务模式](/pessimistic-transaction.md)，与 MySQL 一致。这意味着 TiDB 和 MySQL 在执行写类型 SQL **statement** 时会加**lock**，其可重复读**isolation level**允许当前**read**，因此提交通常不会遇到**exception**。

### 自动重试

> **注意：**
>
> - 从 TiDB v3.0.0 开始，事务自动重试默认关闭，因为它可能**break**事务的**isolation level**。
> - 从 TiDB v8.0.0 开始，不再支持乐观事务的自动重试。

如果在事务提交过程中发生写-写**conflict**，TiDB 会自动重试包含写操作的 SQL **statement**。你可以通过将 `tidb_disable_txn_auto_retry` 设置为 `OFF` 启用自动重试，并通过配置 `tidb_retry_limit` 设置重试次数上限：

```toml
# 是否禁用自动重试。（默认 "on"）
tidb_disable_txn_auto_retry = OFF
# 设置最大重试次数。（默认 "10"）
# 当 "tidb_retry_limit = 0" 时，完全禁用自动重试。
tidb_retry_limit = 10
```

你可以在**session**级别或**global**级别启用自动重试：

1. **session**级别：

    
    ```sql
    SET tidb_disable_txn_auto_retry = OFF;
    ```

    
    ```sql
    SET tidb_retry_limit = 10;
    ```

2. **global**级别：

    
    ```sql
    SET GLOBAL tidb_disable_txn_auto_retry = OFF;
    ```

    
    ```sql
    SET GLOBAL tidb_retry_limit = 10;
    ```

> **注意：**
>
> `tidb_retry_limit` **variable** 决定最大重试次数。当该**variable**设置为 `0` 时，所有事务都不会自动重试，包括自动提交的隐式单条**statement**事务。这是完全禁用 TiDB 自动重试机制的方法。禁用自动重试后，所有发生**conflict**的事务会以最快速度向应用层**return**失败（包括 `try again later` 消息）。

### 重试的限制

默认情况下，TiDB 不会重试事务，因为这可能导致更新丢失并破坏 [`REPEATABLE READ` 隔离](/transaction-isolation-levels.md)。

原因可以从重试流程中看出：

1. 分配一个新的**timestamp**，记为 `start_ts`。
2. 重试包含写操作的 SQL **statement**。
3. 执行两阶段提交。

在第 2 步，TiDB 只会重试包含写操作的 SQL **statement**。但在重试时，TiDB 会收到一个新的版本号作为事务的起始点。这意味着 TiDB 会用新的 `start_ts` 版本的数据重试 SQL **statement**。此时，如果事务根据其他**query**结果进行**update**，结果可能会不一致，因为违反了 `REPEATABLE READ` **isolation**。

如果你的应用可以**tolerate**更新丢失，并且不要求 `REPEATABLE READ` **isolation**的一致性，可以通过设置 `tidb_disable_txn_auto_retry = OFF` 启用该功能。

## 冲突检测

作为一款**distributed database**，TiDB 在 TiKV 层进行内存**conflict**检测，主要发生在 prewrite 阶段。TiDB **instance** 是**stateless**且彼此不可见，这意味着它们无法知道自己的写操作是否会在整个**cluster**中产生**conflict**。因此，**conflict**检测在 TiKV 层完成。

配置如下：

```toml
# 控制槽位数量。（默认 "2048000"）
scheduler-concurrency = 2048000
```

此外，TiKV 支持监控调度器中等待 latch 的耗时。

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

当 `Scheduler latch wait duration` 较高且没有慢写入时，可以安全地判断此时存在大量写**conflict**。