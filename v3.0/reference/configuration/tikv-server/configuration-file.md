---
title: Description of TiKV Configuration File
summary: Learn the TiKV configuration file.
category: reference
---

# Description of TiKV Configuration File

<!-- markdownlint-disable MD001 -->

The configuration files of TiKV support more options than the command-line parameters. You can find the default configuration file in [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) and rename it to `config.toml`.

This document only describes the parameters that are not included in the command-line parameters. For more details, see [command-line parameter](/v3.0/reference/configuration/tikv-server/configuration.md).

### `status-thread-pool-size`

+ The number of worker threads for the `HTTP` API service
+ Default value: `1`
+ Minimum value: `1`

### `grpc-compression-type`

+ The compression algorithm for gRPC messages. Value options: `none`, `deflate`, `gzip`.
+ Default value: `none`

### `grpc-concurrency`

+ The number of gRPC worker threads
+ Default value: `4`
+ Minimum value: `1`

### `grpc-concurrent-stream`

+ The maximum number of concurrent requests allowed in a gRPC link
+ Default value: `1024`
+ Minimum value: `1`

### `server.grpc-raft-conn-num`

+ The maximum number of links among TiKV nodes for Raft communication
+ Default: `10`
+ Minimum value: `1`

### `server.grpc-stream-initial-window-size`

+ The window size of the gRPC stream
+ Default: 2MB
+ Unit: KB|MB|GB
+ Minimum value: `1KB`

### `server.grpc-keepalive-time`

+ The time interval at which that gRPC sends `keepalive` ping messages
+ Default: `10s`
+ Minimum value: `1s`

### `server.grpc-keepalive-timeout`

+ To turn off the timeout for gRPC links
+ Default: 3s
+ Minimum value: 1s

### `server.concurrent-send-snap-limit`

+ The maximum number of snapshots sent at the same time
+ Default value: `32`
+ Minimum value: `1`

### `server.concurrent-recv-snap-limit`

+ To accept the maximum number of snapshots at the same time, Default value: 32
+ Default value: `32`
+ Minimum value: `1`

### `server.end-point-recursion-limit`

+ The maximum number of recursive layers allowed when TiKV decodes the Coprocessor DAG expression
+ Default value: `1000`
+ Minimum value: `1`

### `server.end-point-request-max-handle-duration`

+ The maximum length of time allowed for a TiDB request to TiKV for processing tasks
+ Default value: 60s
+ Minimum value: `1s`

### `server.snap-max-write-bytes-per-sec`

+ The maximum allowable disk bandwidth when snapshot is being processed
+ Default value: 1000MB
+ Unit: KB|MB|GB
+ Minimum value: 1KB

## readpool.storage

Configuration items related to storage thread pool

### `high-concurrency`

+ The number of threads in the thread pools that handle `read` requests of high priority
+ Default value: `4`
+ Minimum value: `1`

### `normal-concurrency`

+ The number of threads in the thread pools that handle `read` requests of normal priority
+ Default value: `4`
+ Minimum value: `1`

### `low-concurrency`

+ The number of threads in the thread pools that handle `read` requests of low priority
+ Default value: `4`
+ Minimum value: `1`

### `max-tasks-per-worker-high`

+ The maximum number of tasks allowed for a single thread in a high-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-normal`

+ The maximum number of tasks allowed for a single thread in a normal-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-low`

+ The maximum number of tasks allowed for a single thread in a low-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `stack-size`

+ The stack size of threads in the `Storage Read` thread pool
+ Default value: 10MB
+ Unit: KB|MB|GB
+ Minimum value: 2MB

## `readpool.coprocessor`

 Configuration items related to the Coprocessor thread pool

### `high-concurrency`

+ The number of threads in thread pool that handle high-priority Coprocessor requests, such as checkpoints
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `normal-concurrency`

+ The number of threads in thread pool that handle normal priority Coprocessor requests
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `low-concurrency`

+ The number of threads in thread pool that handle low priority Coprocessor requests, such as table scan
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `max-tasks-per-worker-high`

+ The number of tasks allowed for a single thread in a high-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-normal`

+ The number of tasks allowed for a single thread in a normal-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-low`

+ The number of tasks allowed for a single thread in a low-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `stack-size`

+ The stack size of the thread in the Coprocessor thread pool
+ Default value: 10MB
+ Unit: KB|MB|GB
+ Minimum value: 2MB

## storage

Configuration items related to storage

### `scheduler-notify-capacity`

+ The maximum number of messages that `scheduler` gets each time
+ Default value: `10240`
+ Minimum value: `1`

### `scheduler-concurrency`

+ A built-in memory lock mechanism to prevent simultaneous operations on a key. Each key has a hash in a different slot.
+ Default value: `2048000`
+ Minimum value: `1`

### `scheduler-worker-pool-size`

+ The number of `scheduler` threads, mainly used for checking transaction consistency before data writing
+ Default value: `4`
+ Minimum value: `1`

### `scheduler-pending-write-threshold`

+ The maximum value written to the data queue. A `Server Is Busy` error is returned for a new write to TiKV when this value is exceeded.
+ Default value: 100MB
+ Unit: MB|GB

## raftstore

Configuration items related to Raftstore

### `sync-log`

+ Whether to perform replication for the data and logs stored on disks

    > **Note:**
    >
    > Setting the value to `false` might lead to data loss.

+ Default value: `true`

### `prevote`

+ The switch of `prevote`. Enabling this feature helps reduce jitter on the system after recovery from isolation.
+ Default value: `true`

### `raftdb-path`

+ The path to the Raft library, which is `storage.data-dir/raft` by default
+ Default value: ""

### `raft-base-tick-interval`

+ The time interval at which the Raft state machine ticks
+ Default value: 1s
+ Minimum value: greater than `0`

### `raft-heartbeat-ticks`

+ The number of passing ticks when the heartbeat is sent. This means that a heartbeat is sent at the time interval of `raft-base-tick-interval` * `raft-heartbeat-ticks`.
+ Default value: `2`
+ Minimum value: greater than `0`

### `raft-election-timeout-ticks`

+ The number of passing ticks when Raft election is initiated. This means that if Raft group is in an leaderless state, the Leader election is initiated approximately after the time interval of `raft-base-tick-interval` * `raft-election-timeout-ticks`.
+ Default value: `10`
+ Minimum value: `raft-heartbeat-ticks`

### `raft-min-election-timeout-ticks`

+ The minimum number of passing ticks when Raft election is initiated. If the number is `0`, the item uses the value of `raft-election-timeout-ticks`. This value of this item must be no smaller than `raft-election-timeout-ticks`.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-election-timeout-ticks`

+ The maximum number of passing ticks when Raft election is initiated. If the number is `0`, the item uses the value of `raft-election-timeout-ticks` * `2`.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-size-per-message`

+ The soft limit on the size of a single message packet
+ Default value: 1MB
+ Minimum value: `0`
+ Unit: MB

### `raft-max-inflight-msgs`

+ The number of logs to be confirmed. If this number is exceeded, log sending will slow down.
+ Default value: `256`
+ Minimum value: greater than `0`

### `raft-entry-max-size`

+ The hard limit on the maximum size of a single log
+ Default value: 8MB
+ Minimum value: `0`
+ Unit: MB|GB

### `raft-log-gc-tick-interval`

+ The time interval at which the polling task of deleting Raft logs is scheduled. `0` means that this feature is not enabled.
+ Default value: 10s
+ Minimum value: `0`

### `raft-log-gc-threshold`

+ The soft limit on the maximum allowable count of residual Raft logs
+ Default value: `50`
+ Minimum value: `1`

### `raft-log-gc-count-limit`

+ The hard limit on the allowable count of residual Raft logs. The default value is the log count that can be accommodated in the 3/4 Region size (calculated as 1MB for each log).
+ Minimum value: `0`

### `raft-log-gc-size-limit`

+ The hard limit on the allowable size of residual Raft logs, defaulting to 3/4 of the Region size.
+ Minimum value: greater than `0`

### `raft-entry-cache-life-time`

+ The maximum remaining time allowed for the log cache in memory.
+ Default value: 30s
+ Minimum value: `0`

### `raft-reject-transfer-leader-duration`

+ The protection time for new nodes, which is used to control the shortest time to migrate Raft Leader to the newly added node. Setting this value too small might lead to the failure of Leader migration.
+ Default value: 3s
+ Minimum value: `0`

### `split-region-check-tick-interval`

+ Check whether the Region needs time interval for Region splitting. `0` means that this feature is not enabled.
+ Default value: 10s
+ Minimum value: `0`

### `region-split-check-diff`

+ The maximum value allowed for the Region data to exceed the specified size, defaulting to 1/16 of the Region size.
+ Minimum value: `0`

### `region-compact-check-interval`

+ The time interval at which to check whether it is necessary to manually trigger RocksDB compaction. `0` means that this feature is not enabled.
+ Default value: 5m
+ Minimum value: `0`

### `clean-stale-peer-delay`

+ To delay the time in deleting expired copy data
+ Default value: 10m
+ Minimum value: `0`

### `region-compact-check-step`

+ The number of Regions checked at one time for each round of manual compaction
+ Default value: `100`
+ Minimum value: `0`

### `region-compact-min-tombstones`

+ The number of tombstones required to trigger RocksDB compaction
+ Default value: `10000`
+ Minimum value: `0`

### `region-compact-tombstones-percent`

+ The proportion of tombstone required to trigger RocksDB compaction
+ Default value: `30`
+ Minimum value: `1`
+ Maximum value: `100`

### `pd-heartbeat-tick-interval`

+ The time interval at which a Region's heartbeat to PD is triggered. `0` means that this feature is not enabled.
+ Default value: 1m
+ Minimum value: `0`

### `pd-store-heartbeat-tick-interval`

+ The time interval at which a store's heartbeat to PD is triggered. `0` means that this feature is not enabled.
+ Default value: 10s
+ Minimum value: `0`

### `snap-mgr-gc-tick-interval`

+ The time interval at which the recycle of expired snapshot files is triggered. `0` means that this feature is not enabled.
+ Default value: 5s
+ Minimum value: `0`

### `snap-gc-timeout`

+ The longest time for which a snapshot file is saved
+ Default value: 4h
+ Minimum value: `0`

### `lock-cf-compact-interval`

+ The time interval at which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: 256MB
+ Default value: 10m
+ Minimum value: `0`

### `lock-cf-compact-bytes-threshold`

+ The size out of which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: 256MB
+ Minimum value: `0`
+ Unit: MB

### `notify-capacity`

+ The longest length of the Region message queue.
+ Default value: `40960`
+ Minimum value: `0`

### `messages-per-tick`

+ The maximum number of messages processed per round
+ Default value: `4096`
+ Minimum value: `0`

### `max-peer-down-duration`

+ The longest inactive time allowed for a peer. A peer with timeout is marked as `down`, and PD tries to delete it later.
+ Default value: 5m
+ Minimum value: `0`

### `max-leader-missing-duration`

+ The longest time allowed for a peer to be in the leaderless state. If this value is exceeded, the peer verifies with PD whether the peer has been deleted.
+ Default value: 2h
+ Minimum value: greater than `abnormal-leader-missing-duration`

### `abnormal-leader-missing-duration`

+ The longest time allowed for a peer to be in the leaderless state. If this value is exceeded, the peer is seen as abnormal and marked in metrics and logs.
+ Default value: `10m`
+ Minimum value: greater than `peer-stale-state-check-interval`

### `peer-stale-state-check-interval`

+ The time interval at which the check for whether a peer is in the leaderless state is triggered
+ Default value: 5m
+ Minimum value: greater than `2 * election-timeout`

### `leader-transfer-max-log-lag`

+ The maximum number of missing logs allowed by the transferee in an attempt to transfer Raft leadership
+ Default value: `10`
+ Minimum value: `10`

### `snap-apply-batch-size`

+ The memory cache size when the imported snapshot file needs to be written into disk
+ Default value: 10MB
+ Minimum value: `0`
+ Unit: MB

### `consistency-check-interval`

+ The time interval at which the consistency check is triggered. `0` means that this feature is not enabled.
+ Default value: 0s
+ Minimum value: `0`

### `raft-store-max-leader-lease`

+ The longest trusted period of a Raft leader
+ Default value: 9s
+ Minimum value: `0`

### `allow-remove-leader`

+ Allow deleting the main switch
+ Default value: `false`

### `merge-max-log-gap`

+ The maximum number of missing logs allowed when `merge` is performed
+ Default value: `10`
+ Minimum value: greater than `raft-log-gc-count-limit`

### `merge-check-tick-interval`

+ The time interval at which TiKV checks whether a Region needs merge
+ Default value: 10s
+ Minimum value: greater than `0`

### `use-delete-range`

+ Turn on the switch that deletes data from the `rocksdb delete_range` interface.
+ Default value: `false`

### `cleanup-import-sst-interval`

+ The time interval at which the expired SST file is checked. `0` means that this feature is not enabled.
+ Default value: 10m
+ Minimum value: `0`

### `local-read-batch-size`

+ The maximum number of read requests processed in one round
+ Default value: `1024`
+ Minimum value: greater than `0`

### `apply-max-batch-size`

+ The maximum number of requests for processing data placement in one round
+ Default value: `1024`
+ Minimum value: greater than `0`

### `apply-pool-size`

+ The number of threads in the thread pool that handles data placement
+ Default value: `2`
+ Minimum value: greater than `0`

### `store-max-batch-size`

+ The maximum number of requests processed in one round
+ Default value: `1024`
+ Minimum value: greater than `0`

### `store-pool-size`

+ The number of threads in the thread pool that process Raft
+ Default value: `2`
+ Minimum value: greater than `0`

### `future-poll-size`

+ The number of thread in the thread pool that drives `future`
+ Default value: `1`
+ Minimum value: greater than `0`

## Coprocessor

Configuration items related to Coprocessor

### `split-region-on-table`

+ To turn on the switch to split Region by table. It is recommended for you to use the feature only in TiDB mode.
+ Default value: `true`

### `batch-split-limit`

+ The threshold of Region splitting. Increasing this value speeds up Region splitting.
+ Default value: `10`
+ Minimum value: `1`

### `region-max-size`

+ The maximum space of a Region. When the value is exceeded, the system splits a Region into many.
+ Default value: 144MB`
+ Unit: KB|MB|GB

### `region-split-size`

+ The size of the newly split Region. This value is an estimate.
+ Default value: 96MB
+ Unit: KB|MB|GB

### `region-max-keys`

+ The maximum number keys allowed in a Region. When this value is exceeded, the system splits a Region into many.
+ Default value: `1440000`

### `region-split-keys`

+ The number of keys in the newly split Region. This value is an estimate.
+ Default value: `960000`

## RocksDB

Configuration items related to RocksDB

### `max-background-jobs`

+ The number of background threads in RocksDB
+ Default value: `8`
+ Minimum value: `1`

### `max-sub-compactions`

+ The number of concurrent sub-compactions in RocksDB
+ Default value: `1`
+ Minimum value: `1`

### `max-open-files`

+ The total number of files that RocksDB can open
+ Default value: `40960`
+ Minimum value: `-1`

### `max-manifest-file-size`

+ The maximum size of the RocksDB Manifest file
+ Default value: 128MB
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `create-if-missing`

+ Automatically create a DB switch
+ Default value: `true`

### `wal-recovery-mode`

+ The WAL recovery mode. Optional values: `0` (`TolerateCorruptedTailRecords`), `1` (`AbsoluteConsistency`), `2` (`PointInTimeRecovery`), `3`(`SkipAnyCorruptedRecords`).
+ Default value: `2`
+ Minimum value: `0`
+ Maximum value: `3`

### `wal-dir`

+ The directory in which WAL is stored
+ Default value: `/tmp/tikv/store`

### `wal-ttl-seconds`

+ The life cycle of the archived WAL. When the value is exceeded, the system deletes the relevant WAL.
+ Default value: `0`
+ Minimum value: `0`
+ unit: second

### `wal-size-limit`

+ The size limit of the archived WAL. When the value is exceeded, the system deletes the relevant WAL.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `enable-statistics`

+ To turn on the switch that automatically optimizes the configuration of Rate LImiter
+ Default value: `false`

### `stats-dump-period`

+ To turn on the switch of Pipelined Write
+ Default value: `true`

### `compaction-readahead-size`

+ The size of `readahead` when compaction is being performed
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `writable-file-max-buffer-size`

+ The maximum buffer size used by WritableFileWrite
+ Default value: 1MB
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ To use `O_DIRECT` for both reads and writes in background flush and compactions
+ Default value: `false`

### `rate-bytes-per-sec`

+ Rate Limiter limits the rate.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: Bytes

### `rate-limiter-mode`

+ Rate LImiter mode. Optional values: `1` (`ReadOnly`), `2` (`WriteOnly`), `3` (`AllIo`).
+ Default value: `2`
+ Minimum value: `1`
+ Maximum value: `3`

### `auto-tuned`

+ Turn on the switch that automatically optimizes the configuration of the Rate LImiter
+ Default value: `false`

### `enable-pipelined-write`

+ Turn on the switch of Pipelined Write
+ Default value: `true`

### `bytes-per-sync`

+ The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously
+ Default value: 1MB
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `wal-bytes-per-sync`

+ The rate at which OS incrementally synchronizes WAL to disk while WAL is being written
+ Default value: 512KB
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-max-size`

+ The maximum size of Info log
+ Default value: 1GB
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-roll-time`

+ The time interval at which logs are truncated. If the value is `0`, logs are not truncated.
+ Default value: `0`

### `info-log-keep-log-file-num`

+ The maximum number of kept log files
+ Default value: `10`
+ Minimum value: `0`

### `info-log-dir`

+ The directory in which logs are stored
+ Default value: ""

## rocksdb.titan

Configuration items related to Titan

### `enabled`

+ Turn on the Titan switch
+ Default value: `false`

### `dirname`

+ The directory in which the Titan Blob file is stored
+ Default value: `titandb`

### `disable-gc`

+ To turn off Titan's switch to GC of the Blob file
+ Default value: `false`

### `max-background-gc`

+ The number of GC threads in the Titan background
+ Default value: `1`
+ Minimum value: `1`

## rocksdb.defaultcf

Configuration items related to `rocksdb.defaultcf`

### `block-size`

+ The default size of a RocksDB block
+ Default value: 64KB
+ Minimum value: `1KB`
+ Unit: KB|MB|GB

### `block-cache-size`

+ The cache size of a RocksDB block
+ Default value: `Total machine memory / 4`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `disable-block-cache`

+ To turn on the switch of block cache
+ Default value: `false`

### `cache-index-and-filter-blocks`

+ Turn on the switch of caching index and filter
+ Default value: `true`

### `pin-l0-filter-and-index-blocks`

+ Whether to pin the index and filter of L0
+ Default value: `true`

### `use-bloom-filter`

+ To turn on the switch of bloom filter
+ Default value: `true`

### `optimize-filters-for-hits`

+ To turn on the switch that optimizes the hit ratio of the filter
+ Default value: `true`

### `whole_key_filtering`

+ To turn on the switch that puts the entire key into the bloom filter
+ Default value: `true`

### `bloom-filter-bits-per-key`

+ The length that the bloom filter reserves for each key
+ Default value: `10`
+ unit: byte

### `block-based-bloom-filter`

+ To turn on the switch that each block creates a bloom filter
+ Default value: `false`

### `read-amp-bytes-per-bit`

+ To turn on the switch of statistics of read amplification. `0`: not enabled. > `0`: enabled.
+ Default value: `0`
+ Minimum value: `0`

### `compression-per-level`

+ The default compression algorithm for each layer. Default value: the first two layers are `No`, and the next five layers are `lz4`.
+ Default value: [`no`, `no`, `lz4`, `lz4`, `lz4`, `zstd`, `zstd`]

### `write-buffer-size`

+ Memtable size
+ Default value: 128MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-write-buffer-number`

+ The maximum number of memtables
+ Default value: `5`
+ Minimum value: `0`

### `min-write-buffer-number-to-merge`

+ The minimum number of memtables to trigger flush
+ Default value: `1`
+ Minimum value: `0`

### `max-bytes-for-level-base`

+ The maximum number of bytes at the base level (L1). Generally, it is set to 4 times the size of memtable.
+ Default value: 512MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `target-file-size-base`

+ The size of the target file at the base level
+ Default: 8MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `level0-file-num-compaction-trigger`

+ The maximum number of L0 files that trigger compaction
+ Default value: `4`
+ Minimum value: `0`

### `level0-slowdown-writes-trigger`

+ The maximum number of L0 files that trigger write stall
+ Default value: `20`
+ Minimum value: `0`

### `level0-stop-writes-trigger`

+ The maximum number of L0 files to completely block write
+ Default value: `36`
+ Minimum value: `0`

### `max-compaction-bytes`

+ The maximum number of written bytes per compaction
+ Default value: 2GB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `compaction-pri`

The priority type of compaction. Optional values: `3` (`MinOverlappingRatio`), `0` (`ByCompensatedSize`), `1` (`OldestLargestSeqFirst`), `2` (`OldestSmallestSeqFirst`).

+ Default value: `3`

### `dynamic-level-bytes`

+ To turn on the switch of optimizing dynamic level bytes
+ Default value: `true`

### `num-levels`

+ The maximum number of layers in the RocksDB file
+ Default value: `7`

### `max-bytes-for-level-multiplier`

+ The default amplification for each layer
+ Default value: `10`

### `rocksdb.defaultcf.compaction-style`

+ Compaction method. Optional values: `level`, `universal`.
+ Default value: `level`

### `disable-auto-compactions`

+ Turn on the switch of automatic compaction
+ Default value: `false`

### `soft-pending-compaction-bytes-limit`

+ The soft limit on the pending compaction bytes
+ Default value: 64GB
+ Unit: KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ The hard limit on the pending compaction bytes
+ Default value: 256GB
+ Unit: KB|MB|GB

## `rocksdb.defaultcf.titan`

Configuration items related to `rocksdb.defaultcf.titan`

### `min-blob-size`

+ The smallest value stored in the Blob file, values below which are stored in the LSM-Tree
+ Default value: 1KB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `blob-file-compression`

+ The compression algorithm used by the Blob file. Optional values: `no`, `snappy`, `zlib`, `bzip2`, `lz4`, `lz4hc`, `zstd`.
+ Default value: `lz4`

### `blob-cache-size`

+ The cache size of the Blob file
+ Default value: 0GB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `min-gc-batch-size`

+ The minimum total size of the Blob files required by GC each time
+ Default value: 16MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-gc-batch-size`

+ The maximum total size of the Blob files required by GC each time
+ Default value: 64MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `discardable-ratio`

+ The triggering ratio of GC for a Blob file. The file might be selected by GC only if the proportion of the invalid value in a Blob file is higher than this ratio.
+ Default value: `0.5`
+ Minimum value: `0`
+ Maximum value: `1`

### `sample-ratio`

+ The ratio of the read data in the entire Blob file when GC is being performed and the Blob file sampled
+ Default value: `0.1`
+ Minimum value: `0`
+ Maximum value: `1`

### `merge-small-file-threshold`

+ When the size of the Blob file is smaller than this value, the file might still be selected by GC regardless of the discardable-ratio.
+ Default value: 8MB
+ Minimum value: `0`
+ Unit: KB|MB|GB

## rocksdb.writecf

Configuration items related to `rocksdb.writecf`

### `block-cache-size`

+ Block cache size
+ Default value: `Total machine memory * 15%`
+ Unit: MB|GB

### `optimize-filters-for-hits`

+ To turn on the switch that optimizes the hit ratio of the filter
+ Default value: `false`

### `whole-key-filtering`

+ To turn on the switch that puts the entire key into the bloom filter
+ Default value: `false`

## rocksdb.lockcf

Configuration items related to `rocksdb.lockcf`

### `block-cache-size`

+ Block cache size
+ Default value: `Total machine memory * 2%`
+ Unit: MB|GB

### `optimize-filters-for-hits`

+ To turn on the switch that optimizes the hit ratio of the filter
+ Default value: `false`

### `level0-file-num-compaction-trigger`

+ The number of L0 files that trigger compaction
+ Default value: `1`

## `raftdb`

Configuration items related to `raftdb`

### `max-background-jobs`

+ The number of background threads in RocksDB
+ Default value: `2`
+ Minimum value: `1`

### `max-sub-compactions`

+ The number of concurrency for the sub-compaction performed by RocksDB
+ Default value: `1`
+ Minimum value: `1`

### `wal-dir`

+ The directory in which WAL is stored
+ Default value: `/tmp/tikv/store`

## `import`

Configuration items related to `import`

### `num-threads`

+ The number of threads when processing the RPC request
+ Default value: `8`
+ Minimum value: `1`

### `num-import-jobs`

+ The number of the concurrent import tasks
+ Default value: `8`
+ Minimum value: `1`
