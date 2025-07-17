---
title: GC 概述
summary: 了解 TiDB 中的垃圾回收（Garbage Collection）。
---

# GC 概述

TiDB 使用 MVCC 来控制事务并发。当你更新数据时，原始数据不会立即删除，而是与新数据一起保留，并带有时间戳以区分版本。垃圾回收（GC）的目标是清理过时的数据。

## GC 过程

每个 TiDB 集群包含一个被选为 GC 领导的 TiDB 实例，负责控制 GC 过程。

TiDB 会定期运行 GC。每次 GC，TiDB 首先计算一个名为 “safe point” 的时间戳，然后在确保所有快照在 safe point 之后仍然保持数据完整的前提下，清理过时的数据。具体来说，每次 GC 过程包括三个步骤：

1. Resolve Locks。 在此步骤中，TiDB 扫描所有 Region 中 safe point 之前的锁，并清除这些锁。
2. Delete Ranges。 在此步骤中，快速清除由 `DROP TABLE` / `DROP INDEX` 操作生成的整个范围的过时数据。
3. Do GC。 在此步骤中，每个 TiKV 节点扫描其上的数据，并删除不再需要的旧版本的每个键。

在默认配置下，GC 每 10 分钟触发一次。每次 GC 保留最近 10 分钟的数据，也就是说，默认的 GC 生命周期为 10 分钟（safe point = 当前时间 - GC 生命周期）。如果一轮 GC 运行时间过长，在本轮 GC 完成之前，即使到了触发下一轮 GC 的时间，也不会开始下一轮 GC。此外，为了确保长事务在超过 GC 生命周期后仍能正常运行，safe point 不会超过正在进行的事务的 start_ts。

## 实现细节

### Resolve Locks

TiDB 的事务模型基于 [Google 的 Percolator](https://ai.google/research/pubs/pub36726) 实现，主要是一个两阶段提交协议，结合了一些实际优化。当第一阶段完成后，所有相关的键都被锁定。在这些锁中，有一个是主锁，其他的是包含指向主锁的指针的次锁；在第二阶段，带有主锁的键会生成一个写入记录，并移除其锁。写入记录表示该键的写入或删除操作，或者是事务的回滚记录。用以替代主锁的写入记录类型表明对应的事务是否成功提交。然后，所有次锁依次被替换。如果由于某些原因（如失败）这些次锁被保留而未被替换，你仍然可以根据次锁中的信息找到主键，并判断整个事务是否已提交。然而，如果主键信息被 GC 清除，而该事务有未提交的次锁，就无法判断这些锁是否可以提交，从而无法保证数据的完整性。

Resolve Locks 步骤会在 safe point 之前清除锁。这意味着，如果锁的主键已提交，则需要提交该锁；否则，需要回滚。如果主键仍被锁定（未提交或已回滚），则视为超时并进行回滚。

Resolve Locks 步骤可以通过以下两种方式实现，且可以使用系统变量 [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) 进行配置：

> **Warning:**
>
> 目前，`PHYSICAL`（Green GC）是一个实验性功能，不建议在生产环境中使用。

- `LEGACY`（默认）：GC 领导会向所有 Region 发送请求，扫描过时的锁，检查扫描到的锁的主键状态，并请求提交或回滚相应的事务。
- `PHYSICAL`：TiDB 绕过 Raft 层，直接扫描每个 TiKV 节点上的数据。

### Delete Ranges

在 `DROP TABLE/INDEX` 等操作中，会删除大量连续键的数据。逐个删除每个键并随后进行 GC，可能导致存储回收效率较低。在这种场景下，TiDB 实际上并不逐个删除每个键，而是只记录待删除的范围和删除的时间戳。然后，Delete Ranges 步骤会对时间戳早于 safe point 的范围进行快速物理删除。

### Do GC

Do GC 步骤会清理所有键的过时版本。为了保证 safe point 之后的所有时间戳都能获得一致的快照，该步骤会删除在 safe point 之前提交的数据，但会保留每个键在 safe point 之前的最后一次写入（只要不是删除操作）。

在此步骤中，TiDB 只需将 safe point 发送给 PD，然后整个 GC 轮次即告完成。TiKV 会自动检测 safe point 的变化，并对当前节点上的所有 Region leader 执行 GC。同时，GC 领导可以继续触发下一轮 GC。

> **Note:**
>
> 从 TiDB 5.0 开始，Do GC 步骤将始终使用 `DISTRIBUTED` gc 模式。这取代了早期的 `CENTRAL` gc 模式，后者由 TiDB 服务器向每个 Region 发送 GC 请求。