---
title: RocksDB Overview
category: reference
---

# RocksDB Overview

RocksDB is an LSM-based storage engine, providing key-value store and read-write functions. It is maintained by Facebook and is based on LevelDB. Key-value pairs put by the user are firstly inserted into Write Ahead Log (WAL) and then written to the SkipList in memory (a data structure called MemTable). LSM-tree engines convert the random modification (insertion) to sequential writes to the WAL file, so they provide better write throughput than B-tree engines.

Once the data in memory reaches a certain size, RocksDB flushes the content into an SST file. SST files are organized in multiple levels (the default is up to 6 levels). When the total size of a level reaches the threshold, RocksDB chooses part of the SST files and merges them into the next level. Each subsequent level is 10 larger than the previous one, so 90% of the data is stored in the last layer.

RocksDB allows users to create multiple Column Families. Column Families have their own SkipList and SST files, and they share the same WAL file. In this way, different Column Family can have different settings according to the application characteristics. It does not increase the number of writes to WAL at the same time.

## TiKV Architecture

The architecture of TiKV is illustrated as follows:

![TiKV RocksDB](/media/tikv-rocksdb.png)

As the storage engine of TiKV, RocksDB is used to store Raft logs and user data. All data in a TiKV node shares two RocksDB instances. One is for Raft log (often called raftdb), and the other is for data (often called kvdb). There are four Column Families (CF) in kvdb: raft, lock, default, and write:

* raft CF: Store metadata of each Region. It occupies only a very small amount of space, and users do not need to care.
* lock CF: Store the pessimistic lock of pessimistic transactions and the Prewrite lock for distributed transactions. After the transaction is committed, the corresponding data in lock CF is deleted quickly. Therefore, the size of data in lock CF is usually very small (less than 1GB). If the data in lock CF increases a lot, it means that there are a large number of transactions waiting to be committed, and the system meets a bug or failure.
* write CF: Store the user's real written data and MVCC metadata (the start timestamp and commit timestamp of the transaction to which the data belongs). When the user writes a row of data, it is stored in the write CF if the data length is less than 255 bytes. Otherwise, it is stored in the default CF. In TiDB, the secondary index only occupies the space of write CF, since the value stored in the non-unique index is empty and the value stored in the unique index is the primary key index.
* default CF: Store data longer than 255 bytes.

## RocksDB Memory Usage

To improve the reading performance and reduce the reading operations to the disk, RocksDB divides the files stored on the disk into blocks based on a certain size (the default is 64KB). When reading a block, it first checks if the data already exists in BlockCache in memory. If true, it can be read directly from memory without accessing the disk.

BlockCache discards the least recently used data according to the LRU algorithm. By default, TiKV devotes 45% of the system memory to BlockCache. Users can also modify the `storage.block-cache.capacit` configuration to an appropriate value by themselves. However, it is not recommended to exceed 60% of the total system memory.

The data written to RocksDB will be written to MemTable firstly. When the size of a MemTable exceeds 128MB, it will switch to a new MemTable. There are 2 RocksDB instances in TiKV, a total of 4 ColumnFamily. The size limit of a single MemTable for each ColumnFamily is 128MB. A maximum of 5 MemTables can exist at the same time, otherwise, the foreground writes will be blocked. The memory occupied by this part is at most 2.5GB (4 x 5 x 128MB). It is not recommended to change since it costs less memory.

## RocksDB Space Usage

* Multi-version: RocksDB is a key-value storage engine with LSM-tree structure, and the data in MemTable will be flushed to L0 first. There may be overlap between the ranges of SSTs at the L0 (because the file is arranged in the order of which they are generated). As a result, there may be multiple versions of the same key in L0. When a file is merged from L0 to L1, it will be cut into multiple files according to a certain size (the default is 8MB). The key range of each file on the same level does not overlap with each other, so there is only one version for each key on L1 and subsequent levels.
* Space amplification: The total size of files on each level is x (the default is 10) times that of the previous level, so 90% of the data is stored in the last level. It also means that the space amplification of RocksDB does not exceed 1.11 (L0 has fewer data and can be ignored).
* Space amplification of TiKV: TiKV has it's own MVCC strategy. When a user writes a key, the real data written to RocksDB is key + commit_ts, that is to say, the update and deletion also write a new key to RocksDB. TiKV deletes the old version of the data (through the Delete interface of RocksDB) at intervals, so it can be considered that the actual space of the data stored by the user on TiKV is enlarged to 1.11 plus the data written in the last 10 minutes (assuming that TiKV cleans up the old data promptly). See [《TiDB in Action》](https://github.com/pingcap-incubator/tidb-in-action/blob/master/session4/chapter7/compact.md#tikv-%E7%9A%84%E7%A9%BA%E9%97%B4%E6%94%BE%E5%A4%A7) for  details.

## RocksDB Background Threads and Compaction

In RocksDB, operations such as converting the MemTable into SST files and merging SST files at various levels are performed in the background thread pool. The default size of the background thread pool is 8. When the number of CPUs in the machine is less than or equal to 8, the default size of the background thread pool is the number of CPUs minus one. Generally speaking, users do not need to change this configuration. If the user deploys multiple TiKV instances on a machine, or the machine has a relatively high read load and a low write load, you can adjust the `rocksdb/max-background-jobs` to 3 or 4 as appropriate.

## WriteStall

The L0 of RocksDB is different from other levels. The SSTs of L0 are arranged in the order of generation. The key ranges between the SSTs can overlap. Therefore, each SST in L0 must be queried in turn when performing a  query. In order not to affect query performance, WriteStall will be triggered to block writing when there are too many files in L0.

When encountering a sudden sharp increase in write delay, you can first check the WriteStall Reason metric on the Grafana RocksDB KV panel. If it is a WriteStall caused by too many L0 files, you can adjust the following configurations to 64, see [《TiDB in Action》](https://github.com/pingcap-incubator/tidb-in-action/blob/master/session4/chapter8/threadpool-optimize.md#5-rocksdb) for details.

```
rocksdb.defaultcf.level0-slowdown-writes-trigger
rocksdb.writecf.level0-slowdown-writes-trigger
rocksdb.lockcf.level0-slowdown-writes-trigger
rocksdb.defaultcf.level0-stop-writes-trigger
rocksdb.writecf.level0-stop-writes-trigger
rocksdb.lockcf.level0-stop-writes-trigger
```
