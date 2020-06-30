
---
title: Storage of TiDB database

summary: Understand the storage layer of a TiDB database

category: introduction

---
# Storage of TiDB database
This article mainly introduces some design ideas and key concepts of TIKV.

![storage-architecture](/media/tidb-storage-architecture.png)

## Key-Value Pairs
As a data storage system, the first thing to decide is the data storage model, that is, in what form the data is saved. TiKV's choice is the Key-Value model and provides an ordered traversal method. Two key points for TIKV data storage:

1、This is a huge Map (analogous to C++'s std::Map) , which stores Key-Value Pairs.

2、The Key-Value pair in the Map is ordered in the binary order of the Key, which means you can Seek to a particular Key location, and then continually call the Next method to get the Key-Value larger than the Key in an incremental order.

Note that the KV storage model for TiKV described in this article has nothing to do with Table in SQL. This article does not discuss any concepts in SQL and focuses on how to implement a high-performance, high-reliability, distributed Key-Value storage such as TiKV.

## Local storage
For any persistent storage engine, data will eventually be saved on disk, and TiKV is no exception. But TiKV did not choose to write data directly to the disk, but stored the data in RocksDB, which is responsible for the data landing. The reason for this choice is that there is a lot of work to be done to develop a stand-alone storage engine, especially to make a high-performance stand-alone engine that requires careful optimization,
and RocksDB is an excellent stand-alone storage engine open source by Facebook, it can meet various requirements of single engine for Tikv. Here, we can simply consider RocksDB as a single persistent Key-Value Map.

## Raft protocol
Next, the implementation of TiKV faces a more difficult thing: how to ensure that the single failure of the case, data is not lost, error-free?

In simple terms, you need to find a way to copy data to multiple machines, so that one machine doesn't work, and the replicas on other machines do; in complex terms, you need the data replication scheme to be reliable and efficient, and be able to handle the failure of a copy. Tikv chose the Raft algorithm.

Raft is a consistent protocol, this article will only do a brief introduction to Raft, the details can refer to its [paper](https://raft.github.io/raft.pdf). The Raft offers several important functions:

- Leader election

- Member changes (such as adding copies, deleting copies, transferring leaders, and so on)

- Log replication

TiKV use Raft to do data replication, each data change will be landed as a Raft log, through the Raft log replication function, the data will be safe and reliable synchronization to the replication group of each node. However, in the actual writing, according to Raft's protocol, it only needs to be synchronously copied to most nodes, and it can be safely considered that the data is successfully written.

![Raft in TiDB](/media/tidb-storage-1.png)

To summarize, TIKV can store data on disk quickly via single machine RocksDB, and copy data to multiple machines via Raft to prevent single machine failure. Instead of writing RocksDB directly, the data is written via the Raft interface. With the implementation of Raft,TiKV becomes a distributed Key-Value storage, and a few machines can automatically complete the copy through the native Raft protocol, which makes it insensitive to the service.

## Region

First, for ease of understanding, in this section, it is assumed that there is only one copy of all data. As mentioned earlier, TiKV can be thought of as a large, ordered KV Map, so data will be distributed across multiple machines in order to achieve a horizontal expansion of storage.
For a KV system, there are two typical solutions for distributing data on multiple machines:

* Hash: Hash by Key, according to the Hash Value Selection of the corresponding storage node

* Range: Divides a Range by Key, where a contiguous Key is stored on a storage node


TiKV chose the second way to divide the whole Key-Value space into a series of consecutive Key segments, each segment is called a Region, and will try to keep the data in each Region within a certain size, currently the default is 96 mb in TiKV. Each Region can be described with [StartKey, EndKey] such a left-closed and right-open interval.

![Region in TiDB](/media/tidb-storage-2.png)

Note that the Region here has nothing to do with the table in SQL. The discussion here still does not involve SQL, only related to KV. After dividing the data into Regions, TiKV will do two important things:

* The data is distributed across all nodes in the cluster in terms of Region, and a similar number of regions is ensured for each node as far as possible

* Replication and membership management of Raft based on Region

These two points are important:

* First, the data is split into many regions according to Key, and the data for each Region is kept on only one node (let alone multiple replicas) . The TIDB system has a component (PD) responsible for spreading the Region as evenly as possible across all nodes in the cluster,
 on the one hand, the storage capacity is expanded horizontally (the Region on the other nodes is automatically scheduled after the new nodes are added) , on the other hand, load balancing is achieved (there is no situation where one node has a lot of data and the others don't).
 At the same time, in order to ensure that the upper client can access the required data, there will be a component (PD) in the system to record the distribution of Region above the node, that is, through any Key can query which Region the Key is in, and which node the Region is currently on (that is, the location routing information for the Key) . The Component (PD) responsible for these two important tasks will be covered later.
 
* For the second point, TiKV replicates the data in Region, that is, multiple copies of the data in one Region are saved, and TiKV calls each copy a Replica. Multiple replicas of a Region are kept on different nodes to form a Raft Group, which is used to keep the data consistent through Raft. One of the replicas will be the Leader of the Group and the other replicas will be the followers. By default, all reading and writing takes place through a Leader, where reading is done and writing is copied to followers. Having understood Region, the following picture should be understood:

![TiDB Storage](/media/tidb-storage-3.png)

With Region as the unit for data dispersion and replication, TiKV has become a distributed KeyValue system with certain disaster tolerance capabilities. There is no need to worry about data storage or disk failure and data loss.

* MVCC

Many databases implement multi-version concurrency control (MVCC), and TiKV is no exception. Imagine a scenario where two clients modify the value of a Key at the same time. If there is no multi-version control of the data, the data needs to be locked. In a distributed scenario, it may cause performance and deadlock problems. TiKV's MVCC implementation is achieved by adding a version number after Key. In short, before MVCC, TiKV can be seen as this:

```
Key1 -> Value
Key2 -> Value
……
KeyN -> Value
```

With MVCC, the key arrangement of TiKV is like this:


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

Note that for multiple versions of the same Key, the version with the larger version number will be placed in the front, and the version with the smaller version number will be placed in the back (see the Key-Value section, Keys are arranged in order), so that when the user obtaining Value through a Key + Version, the Key of MVCC can be constructed from Key and Version, which is Key_Version. Then you can directly locate the first position greater than or equal to this Key_Version through RocksDB's SeekPrefix(Key_Version) API.

## Distributed ACID transaction

TiKV's transaction uses the transaction model used by Google in BigTable: [Percolator](https://research.google.com/pubs/pub36726.html), TiKV is implemented according to this paper, and a lot of optimizations have been made. See the transaction overview for a detailed introduction.


