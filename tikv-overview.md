---
title: TiKV Overview
category: reference
---

# TiKV Overview

TiKV is a distributed and transactional key-value database, which provides transactional APIs with ACID compliance. With the implementation of the [Raft consensus algorithm](https://raft.github.io/raft.pdf) and consensus state stored in RocksDB, TiKV guarantees data consistency between multiple replicas and high availability. As the storage layer of the TiDB distributed database, it provides the read and write service, and persist the written data from applications. It also stores the statistic data of the TiDB cluster.

## Architecture Overview

TiKV is a distributed Key-Value database which is based on the design of Google Spanner. TiKV implements the multiple raft-group replica mechanism. Region is the basic unit of Key-Value data movement and corresponds to a data range in a Store. Each Region is replicated to multiple nodes. These multiple replicas form a Raft group. A replica of a Region is called a Peer. Typically there are 3 peers in a Region. One of them is the leader, which provides the read and write services. Region is the basic data movement unit, the PD balances all the Regions automatically to guarantee that the read and write throughput is balanced among all the nodes in the TiKV cluster. With PD and carefully designed Raft groups, TiKV excels in horizontal scalability and can easily scale to 100+ TBs of data.

![TiKV Architecture](/media/tikv-arch.png)

### Region and RocksDB

There is a RocksDB database within each store and it stores data into the local disk. All the Region data are stored in the same RocksDB in each store. All the logs used for the Raft consensus algorithm is stored in another RocksDB in each store. This is because the performance of sequential I/O is
better than random I/O. With different RocksDB for raftlog and Region data, TiKV can combine all the data write operation of raft log and TiKV regions into one I/O operation to improve the performance.

### Region and Raft Consensus Algorithm

Data consistency between replicas of a Region is guaranteed by the Raft Consensus Algorithm. Only the leader of the Region can provid the write service, only when the data is written to the majority replicated of a Region, the write operation is succeed.

When the size of a certain Region exceed a threshold, which is 144 MB by default, TiKV splits it to two of more Regions. This operation guarantees the size of all the Regions in the cluster are nearly the same. It helps the PD to balance Regions among nodes in a TiKV cluster. When the size of a certain Region is smaller than a threshold, TiKV merges the two smaller adjacent Regins into one Region.

When PD moves a replica from one TiKV to another, it firstly adds a Learner replica on the destination node, after the data in Follower replica is nearly the same with the Leader replica, PD changes it to the Follower replica and removes the replica on the source node.

Moving Leader replica from one node to another follows nearly the same mechanism, the difference is, after the Learner replica becomes the Follower replica, there is operation to transfer Leader from the source node to the destination node. Finanly the new Leader removes the old replica in the source node.

## Distributed Transaction

TiKV supports distributed transaction. Users can write multiple key-value pairs without worrying about whether they belong to the same Region. TiKV uses two phase commit to achive the ACID constraints, see [TiDB Optimistic Transaction Model](/optimistic-transaction.md) for details.

## TiKV Coprocessor

TiDB pushes some data computation logic to TiKV Coprocessor. TiKV Coprocessor processes the computation for each Region. Each request send to TiKV Coprocessor only involves the data of one Region.
