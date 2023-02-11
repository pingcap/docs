---
title: partitioned raft kv
aliases: ['/docs/dev/partitioned-raft-kv/']
---

# partitioned raft kv

Introduce TiKV's partitioned raft kv as a new raft-based storage engine.

## introduction
Before TiDB v6.6, TiKV's raft-based storage engine uses a single `RocksDB` instance. All Regions' data in a TiKV node are all stored in that single `RocksDB` instance.
In v6.6, we introduced a new raft-based storage engine, that still uses `RocksDB`, but each region's data is stored separately in its own dedicated `RocksDB` instance. That means, the region's data are phyiscally partitioned too. That's where the name `partitioned-raft-kv` comes from. In 6.6, the feature is **experimental** feature and thus is **not** recommended in **production** environment.
The major benefits of this feature is better write performance, faster scale-out or scale-in cluster and support larger data size per TiKV and thus support larger cluster.

## related configuration
### storage.engine
sets engine type, it can only be set when setting up a new cluster and cannot be changed latter (when there's data already). **experimental feature** 
* `raft-kv`: raft-kv is 6.5 or prior versions' engine. It's the default value.
* `partitioned-raft-kv`: partitioned-raft-kv is the new engine introduced in 6.6.

### rocksdb.write-buffer-limit
sets a TiKV node's all RocksDB instances' memtable's memory limit. It's not recommended to be less than 5GB. The option applies only to `partitioned-raft-kv`.**experimental feature**
* Default: 25% total memory
* Unit: KB|MB|GB

### rocksdb.write-buffer-flush-oldest-first
sets the RocksDB's memtable flush strategy when its memory usage hit the `rocksdb.write-buffer-limit`. **experimental feature**
* false，default value. It means flush strategy is to pick up the largest size memtable to flush to SST.
* true，It means the flush strategy is to pick up the oldest memtable to flush to SST. It's used for cold and hot data mixed scenario when you want to eliminate the cold data's memory usage.

## The usage sceanrios of the feature
* Need to store more data per TiKV node
* Has large write throughput (> 50MB/s per TiKV)
* Need better scale-out or scale-in speed
* The workload with large read or write amplification
* Current TiKV node has 5GB or more spare memory.

## Limits
As an experimental feature，the following features are still under development yet. They're not supported in v6.6 when `partitioned-raft-kv` is enabled.
* lightning, TiCDC, BR, dumping, Tikv-ctl are not supported
* TiFlash is not supported
* Rollback to 6.5 or older version or changing the engine type after the setup is not supported.
