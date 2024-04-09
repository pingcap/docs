---
title: TiDB Storage
summary: Understand the storage layer of a TiDB database.
---

# TiDB Storage

This document introduces some design ideas and key concepts of [TiKV](https://github.com/tikv/tikv).

![storage-architecture](/media/tidb-storage-architecture-1.png)

## Key-Value pairs

The first thing to decide for a data storage system is the data storage model, that is, in what form the data is saved. TiKV's choice is the Key-Value model and provides an ordered traversal method. There are two key points for TiKV data storage model:

+ This is a huge Map (similar to `std::Map` in C++) , which stores Key-Value pairs.
+ The Key-Value pair in the Map is ordered according to Keys' binary order, which means you can Seek the position of a particular Key and then call the Next method to get the Key-Value pairs larger than this Key in incremental order.

Note that the KV storage model for TiKV described in this document has nothing to do with tables of SQL. This document does not discuss any concepts related to SQL and only focuses on how to implement a high-performance, high-reliability, distributed Key-Value storage such as TiKV.

## Local storage (RocksDB)

For any persistent storage engine, data is eventually saved on disk, and TiKV is no exception. TiKV does not write data directly on the disk, but stores data in RocksDB, which is responsible for the data storage. The reason is that it costs a lot to develop a standalone storage engine, especially a high-performance standalone engine that requires careful optimization.

RocksDB is an excellent standalone storage engine open-sourced by Facebook. This engine can meet various requirements of TiKV for a single engine. Here, you can simply consider RocksDB as a single persistent Key-Value Map.

## Raft protocol

What's more, the implementation of TiKV faces a more difficult thing: to secure data safety in case a single machine fails.

A simple way is to replicate data to multiple machines, so that even if one machine fails, the replicas on other machines are still available. In other words, you need a data replication scheme that is reliable, efficient, and able to handle the situation of a failed replica. All of these are made possible by the Raft algorithm.

Raft is a consensus algorithm. This document only briefly introduces Raft. For more details, you can see [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). The Raft has several important features:

- Leader election
- Membership changes (such as adding replicas, deleting replicas, and transferring leaders)
- Log replication

TiKV use Raft to perform data replication. Each data change will be recorded as a Raft log. Through Raft log replication, data is safely and reliably replicated to multiple nodes of the Raft group. However, according to Raft protocol, successful writes only need that data is replicated to the majority of nodes.

![Raft in TiDB](/media/tidb-storage-1.png)

In summary, TiKV can quickly store data on disk via the standalone machine RocksDB, and replicate data to multiple machines via Raft in case of machine failure. Data is written through the interface of Raft instead of to RocksDB. With the implementation of Raft, TiKV becomes a distributed Key-Value storage. Even with a few machine failures, TiKV can automatically complete replicas by virtue of the native Raft protocol, which does not impact the application.

## Region

To make it easy to understand, let's assume that all data only has one replica. As mentioned earlier, TiKV can be regarded as a large, orderly KV Map, so data is distributed across multiple machines in order to achieve horizontal scalability. For a KV system, there are two typical solutions to distributing data across multiple machines:

* Hash: Create Hash by Key and select the corresponding storage node according to the Hash value.
* Range: Divide ranges by Key, where a segment of serial Key is stored on a node.

TiKV chooses the second solution that divides the whole Key-Value space into a series of consecutive Key segments. Each segment is called a Region. Each Region can be described by `[StartKey, EndKey)`, a left-closed and right-open interval. The default size limit for each Region is 96 MiB and the size can be configured.

![Region in TiDB](/media/tidb-storage-2.png)

Note that the Region here has nothing to do with the table in SQL. In this document, forget about SQL and focus on KV for now. After dividing data into Regions, TiKV will perform two important tasks:

* Distributing data to all nodes in the cluster and use Region as the basic unit. Try its best to ensure that the number of Regions on each node is roughly similar.
* Performing Raft replication and membership management in Region.

These two tasks are very important and will be introduced one by one.

* First, data is divided into many Regions according to Key, and the data for each Region is stored on only one node (ignoring multiple replicas). The TiDB system has a PD component that is responsible for spreading Regions as evenly as possible across all nodes in the cluster. In this way, on one hand, the storage capacity is scaled horizontally (Regions on the other nodes are automatically scheduled to the newly added node); on the other hand, load balancing is achieved (the situation where one node has a lot of data while the others have little will not occur).

    At the same time, in order to ensure that the upper client can access the needed data, there is a component (PD) in the system to record the distribution of Regions on the node, that is, the exact Region of a Key and the node of that Region placed through any Key.

* For the second task, TiKV replicates data in Regions, which means that data in one Region will have multiple replicas with the name "Replica". Multiple Replicas of a Region are stored on different nodes to form a Raft Group, which is kept consistent through the Raft algorithm.

    One of the Replicas serves as the Leader of the Group and other as the Follower. By default, all reads and writes are processed through the Leader, where reads are done and write are replicated to followers. The following diagram shows the whole picture about Region and Raft group.

![TiDB Storage](/media/tidb-storage-3.png)

As we distribute and replicate data in Regions, we have a distributed Key-Value system that, to some extent, has the capability of disaster recovery. You no longer need to worry about the capacity, or disk failure and data loss.

## MVCC

TiKV supports multi-version concurrency control (MVCC). Consider a scenario where Client A is writing to a key simultaneously as Client B is reading the same key. Without the MVCC mechanism, these read and write operations would be mutually exclusive, posing performance issues and deadlocks in a distributed scenario. However, With MVCC, as long as Client B performs a read operation at a logical time earlier than the Client A write operation, then Client B can correctly read the original value at the same time Client A performs the write operation. Even if the key is modified multiple times by multiple write operations, Client B can still read the old value according to its logical time.

TiKV MVCC is implemented by appending a version number to the key. Without MVCC, the Key-Value pairs of TiKV are as follows:

```
Key1 -> Value
Key2 -> Value
……
KeyN -> Value
```

With MVCC, the Key-Value pairs of TiKV are as follows:

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

Note that for multiple versions of the same Key, versions with larger numbers are placed first (see the [Key-Value](#key-value-pairs) section where Keys are arranged in order), so that when you obtain Value through Key + Version, the Key of MVCC can be constructed with Key and Version, which is `Key_Version`. Then you can directly locate the first position greater than or equal to this `Key_Version` through RocksDB's `SeekPrefix(Key_Version)` API.

## Distributed ACID transaction

Transaction of TiKV adopts the model used by Google in BigTable: [Percolator](https://research.google.com/pubs/pub36726.html). TiKV's implementation is inspired by this paper, with a lot of optimizations. See [transaction overview](/transaction-overview.md) for details.
