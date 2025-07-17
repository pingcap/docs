---
title: TiDB 存储
summary: 了解 TiDB 数据库的存储层。
---

# TiDB 存储

本文介绍了 [TiKV](https://github.com/tikv/tikv) 的一些设计思想和关键概念。

![storage-architecture](/media/tidb-storage-architecture-1.png)

## Key-Value 对

对于一个数据存储系统，首先要决定的是数据存储模型，即以何种形式保存数据。TiKV 选择了 Key-Value 模型，并提供有序遍历的方法。TiKV 数据存储模型的两个关键点是：

+ 这类似于一个巨大的 Map（类似于 C++ 中的 `std::Map`），存储 Key-Value 对。
+ Map 中的 Key-Value 对是按照 Keys 的二进制顺序排序的，这意味着你可以 Seek 到某个特定的 Key，然后调用 Next 方法，按增量顺序获取比这个 Key 更大的 Key-Value 对。

注意，本文所描述的 TiKV KV 存储模型与 SQL 表无关。本文不讨论任何与 SQL 相关的概念，只关注如何实现高性能、高可靠性的分布式 Key-Value 存储系统，如 TiKV。

## 本地存储（RocksDB）

对于任何持久存储引擎，数据最终都存储在磁盘上，TiKV 也不例外。TiKV 不会直接将数据写入磁盘，而是将数据存储在 RocksDB 中，后者负责数据存储。原因在于开发一个独立的存储引擎成本很高，尤其是需要经过精心优化的高性能独立引擎。

RocksDB 是 Facebook 开源的一个优秀的独立存储引擎。这个引擎可以满足 TiKV 对单一引擎的各种需求。在这里，你可以简单地将 RocksDB 视为一个持久化的单一 Key-Value Map。

## Raft 协议

更重要的是，TiKV 的实现面临一项更困难的任务：在单机失败的情况下保障数据安全。

一种简单的方式是将数据复制到多台机器上，这样即使一台机器失败，其他机器上的副本仍然可用。换句话说，你需要一种可靠、高效、能够应对副本失效的的数据复制方案。这一切都由 Raft 算法实现。

Raft 是一种共识算法。本文只简要介绍 Raft，更多细节可以参考 [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)。Raft 具有几个重要特性：

- Leader 选举
- 成员变更（如添加副本、删除副本、转移 Leader）
- 日志复制

TiKV 使用 Raft 进行数据复制。每次数据变更都会被记录为 Raft 日志。通过 Raft 日志复制，数据可以安全、可靠地复制到 Raft 组中的多个节点。然而，根据 Raft 协议，成功的写操作只需要数据复制到多数节点即可。

![Raft in TiDB](/media/tidb-storage-1.png)

总结来说，TiKV 可以通过单机 RocksDB 快速将数据存储到磁盘，并通过 Raft 将数据复制到多台机器，以应对机器故障。数据是通过 Raft 接口写入的，而不是直接写入 RocksDB。随着 Raft 的实现，TiKV 变成了一个分布式的 Key-Value 存储系统。即使出现少数机器故障，TiKV 也能自动完成副本复制，且不会影响应用。

## Region

为了便于理解，假设所有数据只有一个副本。如前所述，TiKV 可以看作一个大型有序的 KV Map，因此数据会在多台机器上分布，以实现水平扩展。对于一个 KV 系统，常见的两种数据分布方案是：

* Hash：通过 Key 计算 Hash，然后根据 Hash 值选择对应的存储节点。
* Range：按 Key 划分区间，将连续的 Key 段存储在一个节点上。

TiKV 选择了第二种方案，即将整个 Key-Value 空间划分为一系列连续的 Key 段。每个段称为一个 Region。每个 Region 可以用 `[StartKey, EndKey)` 描述，是一个左闭右开的区间。每个 Region 的默认大小限制为 256 MiB，大小可以配置。

![Region in TiDB](/media/tidb-storage-2.png)

注意，这里的 Region 与 SQL 中的表无关。在本文中，暂时忘记 SQL，专注于 KV。将数据划分为 Regions 后，TiKV 会执行两个重要任务：

* 将数据分布到集群中的所有节点，并以 Region 作为基本单元。尽量确保每个节点上的 Region 数量大致相当。
* 在 Region 内进行 Raft 副本复制和成员管理。

这两个任务非常重要，下面逐一介绍。

* 首先，按照 Key 将数据划分为多个 Regions，每个 Region 的数据只存储在一台节点上（忽略多副本的情况）。TiDB 系统中有一个 PD 组件，负责尽可能均匀地将 Regions 分布在所有节点上。这样，一方面可以实现存储容量的水平扩展（其他节点上的 Regions 会自动调度到新加入的节点）；另一方面可以实现负载均衡（避免某个节点存储大量数据而其他节点存储较少的情况）。

    同时，为了确保上层客户端可以访问所需数据，系统中还存在一个组件（PD），用来记录节点上 Regions 的分布情况，即通过任何 Key 可以定位到某个 Key 所在的 Region 及其所在节点。

* 第二个任务是，TiKV 在 Regions 内进行数据复制，即一个 Region 内的数据会有多个副本，称为 "Replica"。多个 Region 副本存储在不同节点上，形成一个 Raft Group，通过 Raft 算法保持一致。

    其中一个副本作为 Group 的 Leader，其他作为 Follower。默认情况下，所有的读写操作都通过 Leader 进行，读操作在 Leader 上完成，写操作会复制到 Followers。下图展示了关于 Region 和 Raft Group 的整体情况。

![TiDB Storage](/media/tidb-storage-3.png)

随着数据在 Regions 中的分布和复制，我们拥有了一个具有灾难恢复能力的分布式 Key-Value 系统。你不再需要担心存储容量、磁盘故障或数据丢失的问题。

## MVCC

TiKV 支持多版本并发控制（MVCC）。考虑一个场景：客户端 A 正在写入某个 Key，同时客户端 B 正在读取同一个 Key。如果没有 MVCC 机制，这些读写操作会互斥，导致性能问题和死锁，尤其在分布式场景中。然而，有了 MVCC，只要客户端 B 在比客户端 A 写操作的逻辑时间早的时间点进行读取，就可以正确读取到原始值，即使该 Key 被多次写入，客户端 B 仍然可以根据其逻辑时间读取到旧值。

TiKV 的 MVCC 通过在 Key 上附加版本号来实现。没有 MVCC 时，TiKV 的 Key-Value 对如下：

```
Key1 -> Value
Key2 -> Value
……
KeyN -> Value
```

有了 MVCC 后，TiKV 的 Key-Value 对如下：

```
Key1_Version3 -> Value
Key1_Version2 -> Value
Key1_Version1 -> Value
……
Key2_Version4 -> Value
Key2_Version3 -> Value
Key2_Version2 -> Value
Key2_Version1 -> Value
……
KeyN_Version2 -> Value
KeyN_Version1 -> Value
……
```

注意，对于同一 Key 的多个版本，版本号较大的版本会排在前面（参见 [Key-Value](#key-value-pairs) 部分，Keys 按顺序排列），因此通过 Key + Version 构造的 MVCC Key 可以用 `Key_Version` 表示。然后，可以通过 RocksDB 的 `SeekPrefix(Key_Version)` API 直接定位到第一个大于或等于这个 `Key_Version` 的位置。

## 分布式 ACID 事务

TiKV 的事务采用 Google 在 BigTable 中提出的模型：[Percolator](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)。TiKV 的实现借鉴了这篇论文，并进行了大量优化。详细内容请参见 [transaction overview](/transaction-overview.md)。