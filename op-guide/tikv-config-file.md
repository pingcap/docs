---
title: TiKV Configuration File Description
category: deployment
---

# TiKV Configuration File Description

The TiKV configuration file supports more options than command line options. You can find the default configuration file in [etc/config-template.toml](https://github.com/pingcap/tikv/blob/master/etc/config-template.toml) and rename it to `config.toml`.

This document describes the options that are not involved in command line options. For command line options, see [here](configuration.md).
  
## `server`

### `grpc-compression-type`

- Compression type for the gRPC channel
- Default: "none"
- The value options are "none", "deflate" and "gzip"

### `grpc-concurrency`

- Size of the thread pool for the gRPC server.
- Default: 4
- Enlarge it if you find your gRPC thread becomes the bottleneck.

### `grpc-concurrent-stream`

- The number of max concurrent streams/requests on a connection.
- Default: 1024

### `grpc-raft-conn-num`

- The number of the gRPC connections between two TiKV servers for sending Raft messages
- Default: 10

### `grpc-stream-initial-window-size`

- The amount read ahead size for the gRPC stream
- Default: "2MB"

### `grpc-keepalive-time`

- The interval time for the gRPC connection sending a `ping` message to keep alive 
- Default: "10s"

### `grpc-keepalive-timeout`

- The timeout after the gRPC connection sends a `ping` message but receives no acknowledgement
- Default: "3s"
- The connection will be closed after timeout

### `concurrent-send-snap-limit`

- The maximum number of snapshots a TiKV server can send concurrently
- Default: 32

### `concurrent-recv-snap-limit`

- The maximum number of snapshots a TiKV server can receive concurrently
- Default: 32

### `snap-max-write-bytes-per-sec`

- The max bytes per second that TiKV server can write the snapshot file to the disk. 
- Default: "100MB"

### `snap-max-total-size`

- The max disk space to hold the snapshot files. 
- Default: 0, means unlimited
- TiKV will try to remove the snapshot files after exceeding this value. 

### `end-point-recursion-limit`

- Max recursion level allowed when decoding DAG expression
- Default: 1000

### `end-point-stream-channel-size`

- Default: 8

### `end-point-batch-row-limit`

- The count to handle rows in one batch
- Default: 64

### `end-point-stream-batch-row-limit`

- The count to handle rows in one batch in the streaming mode
- Default: 128

### `end-point-request-max-handle-duration`

- The max allowed time when handling a request. 
- Default: "1m"
- If the request takes a long time execeeding this value, an Outdated error returns. 

### `labels`

- Attributes about this server, e.g. { zone = "us-west-1", disk = "ssd" }
- Default: {}

## `storage`

### `gc-ratio-threshold`

- The threshold to run garbage collection.
- Default: 1.1
- Even the GC is triggered, the GC will really be run when the value is less than 1, or there are many versions exceeding this threshold.

### `max-key-size`

- Max size for a key
- Default: 4096
- If the key is larger than this value, a KeyTooLarge error returns.

### `scheduler-notify-capacity`

- The channel capacity for the scheduler thread
- Default: 10240

### `scheduler-concurrency`

### `scheduler-worker-pool-size`

- The size for the scheduler worker pool
- Default: 4

### `scheduler-pending-write-threshold`

- The max total size for all the pending write request
- Default: "100MB"
- If exceeding the value, latter write request will be disarded and a SchedTooBusy error returns

## `readpool`

### `storage`

#### `high-concurrency`

- The pool size for the thread pool which runs high priroty tasks
- Default: 4

#### `normal-concurrency`

- The pool size for the thread pool which runs normal priroty tasks
- Default: 4

#### `low-concurrency`

- The pool size for the thread pool which runs low priroty tasks
- Default: 4

#### `max-tasks-per-worker-high`

- The max allowed high priority tasks pending in one worker
- Default: 2000

#### `max-tasks-per-worker-normal`

- The max allowed normal priority tasks pending in one worker
- Default: 2000

#### `max-tasks-per-worker-low`

- The max allowed low priority tasks pending in one worker
- Default: 2000

#### `stack-size`

- The stack size for the worker thread
- Default: "10MB"

### `coprocessor`

The `coprocessor` read pool has the same configurations with `storage`'s. The different default values are listed below:

- `high-concurrency`: 8
- `normal-concurrency`: 8 
- `low-concurrency`: 8

## `metric`
### `interval`

- The interval time to push the metrics to the Prometheus Push Gateway server
- Default: "15s"

### `address`

- The address of the Prometheus Push Gateway server
- Default: ""

### `job`

- The job name when pushing to the Gateway server
- Default: "tikv"

## `raftstore`

### `sync-log`

- Sync the Raft log every time to guarantee high reliability and prevent data loss.
- Default: true 
- Setting it to false can improve the performance but may lose the data if your system crashed or machine powered off. Your data will be safe even the TiKV process crashes because the data will be still kept in the system's page cache and flushed to the disk after the process restarts.

### `raftdb-path`

- The directory to save the Raft data. 
- Default: ""
- If not set, the default `$data-dir/raft` will be used.

### `capacity`

- The cpacity for a TiKV server to hold data
- Default: "0KB"
- If the PD server finds the save data size of one TiKV nearly reaches the capacity, PD will try to move data from this TiKV server
- 0 means that the TiKV server will use the current disk capacity as its capacity

### `raft-base-tick-interval`

- The interval to tick Raft
- Default: "1s"
- If you have many regions and find that your raftstore thread CPU utilization is very high, you can increase this value to relieve the pressure but this may also increase the cluster recover time when your cluster is restarted

### `raft-heartbeat-ticks`

- The tick number for heartbeat
- Default: 2
- The Raft leader will send a Raft heartbeat message after ticking Raft `raft-heartbeat-ticks` times.

### `raft-election-timeout-ticks`

- The tick number for election
- Default: 10
- The followers will re-campaign the leader if they don't receive any message from the leader after ticking Raft the times in the range [`raft-election-timeout-ticks`, 2 x `raft-election-timeout-ticks`)

### `raft-min-election-timeout-ticks`

- The minimal election timeout tick number
- Default: 0
- If 0, it will be set as `raft-election-timeout-ticks`
- The followers will re-campaign after the ticking times in the range [`raft-min-election-timeout-ticks`, `raft-max-election-timeout-ticks`)


### `raft-max-election-timeout-ticks`

- The maximum election timeout tick number
- Default: 0
- If 0, it will be set as 2 x `raft-election-timeout-ticks`

### `raft-max-size-per-msg`

- The maximum size to append the Raft logs in one message
- Default: "1MB"

### `raft-max-inflight-msgs`

- The maximum number of `infligh` messages during Raft optimisic replication phase
- Default: 256

### `raft-entry-max-size`

- The maximum size for the Raft entry
- Default: "8MB"

### `raft-log-gc-tick-interval`

- The intervel to trigger garbage collection for the Raft committed logs
- Default: "10s"

### `raft-log-gc-threshold`

- The threshold to run Raft log garbage collection
- Default: 50
- The the leader finds the lastest Raft replicated log which has already been replicated to all followers but the replicated log ID minus the first log ID is less or equal than the threshold, the leader will skip the log GC

### `raft-log-gc-count-limit`

- The count limit for Raft log GC
- Default: 73728 (96 MB * 3 / 4 / 1KB)

### `raft-log-gc-size-limit`

- The size limit for Raft log GC
- Default: "72MB" (96 MB * 3 / 4)

### `split-region-check-tick-interval`

- The interval to check whether the region needs to be split or not
- Default: "10s"

### `region-split-check-diff`

- The size diff to decide whether to check the region split or not
- Default: "6MB"
- If a region's size change is leass than the diff, the check will not be triggered

### `clean-stale-peer-delay`

- The delay time to delete a stale peer
- Default: "10m"
- If the peer is removed, the data will be really deleted after the delay time

### `region-compact-check-interval`

- The interval to check whether the region needs to be manunally compacted or not
- Default: "5m"

### `region-compact-check-step`

- The number of regions needs to be check in the compact check.
- Default: 100

### `region-compact-min-tombstones`

- The minimal number of tombstone keys to tigger the manual compaction.
- Default: 10000

### `pd-heartbeat-tick-interval`

- The interval to send a region heartbeat message to PD
- Default: "1m"

### `pd-store-heartbeat-tick-interval`

- The interval to send a store heartbeat message to PD
- Default: "10s"

### `snap-mgr-gc-tick-interval`

- The interval to check whether a snapshot file needs to be GC or not
- Default: "1m"

### `snap-gc-timeout`

- The maximum expired time for a snapshot file to be GC.
- Default: "4h"

### `lock-cf-compact-interval`

- The interval to compact the lock column family manually
- Default: "10m"

### `lock-cf-compact-bytes-threshold`

- The threshold to compact the lock column family 
- Default: "256MB"
- The compaction can only be triggered when the size exceeds the threshold

### `notify-capacity`

- The capacity for the notify channel
- Default: 40960

### `messages-per-tick`

- The number of messages handled in one tick
- Default: 4096

### `max-peer-down-duration`

- The duration to treat a non-active peer as "down"
- Default: "5m"

### `max-leader-missing-duration`

- The duration to treat a peer as "missing" if it doesn't receive any message from otheer peers
- Default: "2h"

### `abnormal-leader-missing-duration`

- The duration to log a "missing" message and report to the monitoring system if the peer is considered "missing"
- Default: "10m"

### `peer-stale-state-check-interval`

- The interval to check a peer's state
- Default: "5m"

### `snap-apply-batch-size`

- The maximum size to apply keys in the snapshot file in batch
- Default: "10MB"

### `consistency-check-interval`

- The interval to check whether all the peers are consistent or not
- Default: "0s"

### `report-region-flow-interval`

- The interval to report the region's read/write flow to the PD
- Default: "1m"

### `raft-store-max-leader-lease`

- The max time for a Raft leader to provice local read (not through Raft) in the lease
- Default: "9s"

### `right-derive-when-split`

- The flag to let the new right/or left split region inherit the meta data from the parent
- Default: true
- The region will be split into two new regions left + right. If true, the right will inherit from the parent

### `allow-remove-leader`

- The flag to allow removing the Raft leader in the RemoveNode request 
- Default: false

### `merge-max-log-gap`

- The maximum gap to allow merge or not
- Default: 10
- If two peers's log gap is larger than the threshold, the `merge` request will be skipped

### `merge-check-tick-interval`

- The interval to check whether a region needs to be merged with other region.
- Default: "10s"

### `use-delete-range`

- Use RocksDB `DeleteRange` to clear the data or not
- Default: false
- It is not suggested to enable it now
- After performance problem of `DeleteRange` is fixed, the flag will be enabled by default

### `cleanup-import-sst-interval`

- The interval to cleanup the stable SST files generated in the load phase
- Default: "10m"

## `coprocessor`
### `split-region-on-table`

- To split the region by table or not
- Default: true
- If enabled, the region can only hold one table's data. If a region has multipy tables' data, the region will be split

### `region-max-size`

- The maximum size for a region
- Default: "144MB"
- If a region's size exceeds this, the region will be split

### `region-split-size`

- The size for a region to be split
- Default: "96MB"
- If a region's size exceeds `region-max-size`, the region will be split, a split key will be chosen after scanning `region-split-size` data

## `rocksdb`

### `wal-recovery-mode`

- WAL recovery mode
- Default: 2
- 0 : TolerateCorruptedTailRecords, tolerate incomplete record in trailing data on all logs
- 1 : AbsoluteConsistency, We don't expect to find any corruption in the WAL
- 2 : PointInTimeRecovery, Recover to point-in-time consistency
- 3 : SkipAnyCorruptedRecords, Recovery after a disaster

### `wal-dir`

- The directory for the RocksDB WAL
- Default: ""

### `wal-ttl-seconds`

- The time to live seconds for a WAL
- Default: 0
- Every TTL seconds / 2, the WAL which is older than `wal-ttl-seconds` will be deleted

### `wal-size-limit`

- The size limit for a WAL
- Default: "0KB"
- If the total WAL's size exceeds the limit, the WALs will be deleted from the earliest one

### `max-total-wal-size`

- The maximum size for a WAL file
- Default: "4GB"

### `max-background-jobs`

- The maximum number of concurrent background jobs
- Default: 6

### `max-manifest-file-size`

- The maximum size of manifest file
- Default: "20MB"

### `create-if-missing`

- Create the database if it is missing
- Default: true

### `max-open-files`

- The maximum number of open files that can be used
- Default: 40960

### `enable-statistics`

- Enable the RocksDB statistics
- Default: true

### `stats-dump-period`

- The period time to dump the RocksDB statistics into RocksDB log
- Default: "10m"

### `compaction-readahead-size`

- The readahead size when compacting
- Default: "0KB"

### `info-log-max-size`

- The maximum size for the RocksDB log
- Default: "0KB"

### `info-log-roll-time`

- The interval to rotate a new log file
- Default: "0s"

### `info-log-dir`

- The directory for the info log
- Default: ""

### `rate-bytes-per-sec`

- The bytes per sec that the RocksDB writes to disk
- Default: "0KB"

### `bytes-per-sync`

- The bytes of SST files that the RocksDB syncs to the disk incrementally 
- Default: "1MB"

### `wal-bytes-per-sync`

- The bytes of WAL that the RocksDB syncs to the disk incrementally 
- Default: "512KB"

### `max-sub-compactions`

- The maximum number of threads to perform a sub-compaction
- Default: 1

### `writable-file-max-buffer-size`

- The maximum buffer size that is used by WritableFileWrite
- Default: "1MB"

### `use-direct-io-for-flush-and-compaction`

- Use O_DIRECT for both reads and writes in background flush and compaction job
- Default: false 

### `enable-pipelined-write`

- Enable or disable the pipelined write
- Default: true

### `allow-concurrent-memtable-write`

- Enable or disable writing MemTable concurrently
- Default: true
    
### `defaultcf`
#### `block-size`

- The approximate size for the user data in one block
- Default: "64KB"

#### `block-cache-size`

- The cache size for the block data
- The size is calculated by the machine memory dynamically if not set

#### `cache-index-and-filter-blocks`

- Cache the index and bloom filter data into the block cache
- Default: true

#### `pin-l0-filter-and-index-blocks`

- Pin Level0 filter and index data in the block cache
- Default: true


#### `bloom-filter-bits-per-key`

- The bits per key for the bloom filter
- Default: 10
- 10 yields ~1% false positive rate. Larger value will reduce the false positive rate but increases memory usage and space amplification

#### `block-based-bloom-filter`

- Use bloom filter for one block
- Default: false
- False means using bloom filter for one SST file rather than one block

#### `read-amp-bytes-per-bit`

- Enable read amplification statistics
- Default: 0

#### `compression-per-level`

- Compression type for per level
- Default: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

#### `write-buffer-size`

- The write buffer size
- Default: "128MB"

#### `max-write-buffer-number`

- The maximum number of write buffers that can be in memory until being flushed to the disk
- Default: 5

#### `min-write-buffer-number-to-merge`

- The minimum number of write buffers that will be merged together before being flushed to the disk
- Default: 1

#### `max-bytes-for-level-base`

- The maximum data size for base level 1
- Default: "512MB"

#### `target-file-size-base`

- The target SST file size for compaction
- Default: "8MB"

#### `level0-file-num-compaction-trigger`

- The allowed number of level 0 files
- Default: 4
- If the number exceeds this value, a compaction will be triggered to compact the level 0 files

#### `level0-slowdown-writes-trigger`

- The soft limit number of level 0 files
- Default: 20
- The write will be slowed down after the file number exceeds this value

#### `level0-stop-writes-trigger`

- The maximum number of level 0 files
- Default: 36
- The write will be stopped after the file number exceeds this value

#### `max-compaction-bytes`

- The maximum bytes for compaction
- Default: "2GB"

#### `compaction-pri`

- The different algorithms for compaction
- Default: 3
- 0 : ByCompensatedSize
- 1 : OldestLargestSeqFirst
- 2 : OldestSmallestSeqFirst
- 3 : MinOverlappingRatio

#### `dynamic-level-bytes`

- Pick target size of each level dynamically
- Default: false


#### `disable-auto-compactions`

- Disable auto compaction or not
- Default: false

#### `soft-pending-compaction-bytes-limit`

- The soft limit bytes for pending compaction
- Default: "64GB"
- The write will be slowed down if the pending compaction bytes exceed the limit

#### `hard-pending-compaction-bytes-limit`

- The hard limit bytes for pending compaction
- Default: "256GB"
- The write will be stopped if the pending compaction bytes exceed the limit


### `writecf`

`rocksdb.writecf` shares the same configuration with `rocksdb.default`. The different default values are listed below:

- compaction-pri = 3

### `rocksdb.lockcf`  

`rocksdb.lockcf` shares the same configuration with `rocksdb.default`. The different default values are listed below:

- compression-per-level = ["no", "no", "no", "no", "no", "no", "no"]
- block-size = "16KB"
- level0-file-num-compaction-trigger = 1

### `rocksdb.raftcf`

`rocksdb.raftcf` shares the same configuration with `rocksdb.default`. The different default values are listed below:

- compression-per-level = ["no", "no", "no", "no", "no", "no", "no"]
- block-size = "16KB"
 
## `raftdb`

`raftdb` shares the same configuration with `rocksdb`. The different default values are listed below:

- allow-concurrent-memtable-write = false

      
## `security`
### `ca-path`

- The path for your SSL certificate authority
- Default: ""

### `cert-path`

- The path for your SSL certificate
- Default: ""

### `key-path`

- The path for your SSL key
- Default: ""
  
## `import`

### `import-dir`

- The directory for importing data
- Default: "/tmp/tikv/import"

### `num-threads`

- The maximum number of threads for importing concurrently
- Default: 8

### `stream-channel-window`

- The maximum window size for the gRPC stream channel
- Default: 128