---
title: TiKV Configuration File
summary: Learn the TiKV configuration file.
aliases: ['/docs/stable/tikv-configuration-file/','/docs/v4.0/tikv-configuration-file/','/docs/stable/reference/configuration/tikv-server/configuration-file/']
---

# TiKV Configuration File

<!-- markdownlint-disable MD001 -->

The TiKV configuration file supports more options than command-line parameters. You can find the default configuration file in [etc/config-template.toml](https://github.com/tikv/tikv/blob/release-4.0/etc/config-template.toml) and rename it to `config.toml`.

This document only describes the parameters that are not included in command-line parameters. For more details, see [command-line parameter](/command-line-flags-for-tikv-configuration.md).

## Global configuration

### `log-level`

+ The log level
+ Value options: "trace", "debug", "info", "warning", "error", "critical"
+ Default value: "info"

### `log-file`

+ The log file. If this configuration is not set, logs are output to "stderr" by default.
+ Default value: ""

### `log-format`

+ The log format
+ Value options: "json", "text"
+ Default value: "text"

### `log-rotation-timespan`

+ The timespan between log rotations. When this timespan passes, log files are rotated, that is, a timestamp is appended to the file name of the current log file, and a new file is created.
+ Default value: "24h"

### `log-rotation-size`

+ The size of a log file that triggers log rotation. Once the size of a log file is bigger than the specified threshold value, log files are rotated. The old log file is placed into the new file, and the new file name is the old file name with a timestamp suffix.
+ Default value: "300MB"

### `slow-log-file`

+ The file to store slow logs
+ If this configuration is not set but `log-file` is set, slow logs are output to the log file specified by `log-file`. If neither `slow-log-file` nor `log-file` are set, all logs are output to "stderr".
+ Default value: ""

### `slow-log-threshold`

+ The threshold for outputing slow logs. If the processing time is longer than this threshold, slow logs are output.
+ Default value: "1s"

## server

+ Configuration items related to the server

## `status-thread-pool-size`

+ The number of worker threads for the `HTTP` API service
+ Default value: `1`
+ Minimum value: `1`

### `grpc-compression-type`

+ The compression algorithm for gRPC messages
+ Optional values: `"none"`, `"deflate"`, `"gzip"`
+ Default value: `"none"`

### `grpc-concurrency`

+ The number of gRPC worker threads
+ Default value: `4`
+ Minimum value: `1`

### `grpc-concurrent-stream`

+ The maximum number of concurrent requests allowed in a gRPC stream
+ Default value: `1024`
+ Minimum value: `1`

### `grpc-memory-pool-quota`

+ Limit the memory size that can be used by gRPC
+ Default: No limit
+ Limit the memory in case OOM is observed. Note that limit the usage can lead to potential stall

### `grpc-raft-conn-num`

+ The maximum number of links among TiKV nodes for Raft communication
+ Default: `1`
+ Minimum value: `1`

### `grpc-stream-initial-window-size`

+ The window size of the gRPC stream
+ Default: 2MB
+ Unit: KB|MB|GB
+ Minimum value: `"1KB"`

### `grpc-keepalive-time`

+ The time interval at which that gRPC sends `keepalive` Ping messages
+ Default: `"10s"`
+ Minimum value: `"1s"`

### `grpc-keepalive-timeout`

+ Disables the timeout for gRPC streams
+ Default: `"3s"`
+ Minimum value: `"1s"`

### `concurrent-send-snap-limit`

+ The maximum number of snapshots sent at the same time
+ Default value: `32`
+ Minimum value: `1`

### `concurrent-recv-snap-limit`

+ The maximum number of snapshots received at the same time
+ Default value: `32`
+ Minimum value: `1`

### `end-point-recursion-limit`

+ The maximum number of recursive levels allowed when TiKV decodes the Coprocessor DAG expression
+ Default value: `1000`
+ Minimum value: `1`

### `end-point-request-max-handle-duration`

+ The longest duration allowed for a TiDB's push down request to TiKV for processing tasks
+ Default value: `"60s"`
+ Minimum value: `"1s"`

### `snap-max-write-bytes-per-sec`

+ The maximum allowable disk bandwidth when processing snapshots
+ Default value: `"100MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"1KB"`

### `end-point-slow-log-threshold`

+ The time threshold for a TiDB's push-down request to output slow log. If the processing time is longer than this threshold, the slow logs are output.
+ Default value: `"1s"`
+ Minimum value: `0`

## readpool.unified

> **Warning:**
>
> Unified read pool is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

Configuration items related to the single thread pool serving read requests. This thread pool supersedes the original storage thread pool and coprocessor thread pool since the 4.0 version.

### `min-thread-count`

+ The minimal working thread count of the unified read pool
+ Default value: `1`

### `max-thread-count`

+ The maximum working thread count of the unified read pool
+ Default value: `MAX(4, CPU * 0.8)`

### `stack-size`

+ The stack size of the threads in the unified thread pool
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`

### `max-tasks-per-worker`

+ The maximum number of tasks allowed for a single thread in the unified read pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

## readpool.storage

Configuration items related to storage thread pool.

### `use-unified-pool`

+ Determines whether to use the unified thread pool (configured in [`readpool.unified`](#readpoolunified)) for storage requests. If the value of this parameter is `false`, a separate thread pool is used, which is configured through the rest parameters in this section (`readpool.storage`).
+ Default value: `false`

### `high-concurrency`

+ The allowable number of concurrent threads that handle high-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is greater than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
+ Minimum value: `1`

### `normal-concurrency`

+ The allowable number of concurrent threads that handle normal-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is greater than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
+ Minimum value: `1`

### `low-concurrency`

+ The allowable number of concurrent threads that handle low-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is greater than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
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

+ The stack size of threads in the Storage read thread pool
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`

## `readpool.coprocessor`

Configuration items related to the Coprocessor thread pool.

### `use-unified-pool`

+ Determines whether to use the unified thread pool (configured in [`readpool.unified`](#readpoolunified)) for coprocessor requests. If the value of this parameter is `false`, a separate thread pool is used, which is configured through the rest parameters in this section (`readpool.coprocessor`).
+ Default value: If none of the parameters in this section (`readpool.coprocessor`) are set, the default value is `true`. Otherwise, the default value is `false` for the backward compatibility. Adjust the configuration items in [`readpool.unified`](#readpoolunified) before enabling this parameter.

### `high-concurrency`

+ The allowable number of concurrent threads that handle high-priority Coprocessor requests, such as checkpoints
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `normal-concurrency`

+ The allowable number of concurrent threads that handle normal-priority Coprocessor requests
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `low-concurrency`

+ The allowable number of concurrent threads that handle low-priority Coprocessor requests, such as table scan
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
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`

## storage

Configuration items related to storage

### `scheduler-concurrency`

+ A built-in memory lock mechanism to prevent simultaneous operations on a key. Each key has a hash in a different slot.
+ Default value: `524288`
+ Minimum value: `1`

### `scheduler-worker-pool-size`

+ The number of `scheduler` threads, mainly used for checking transaction consistency before data writing. If the number of CPU cores is greater than or equal to `16`, the default value is `8`; otherwise, the default value is `4`.
+ Default value: `4`
+ Minimum value: `1`

### `scheduler-pending-write-threshold`

+ The maximum size of the write queue. A `Server Is Busy` error is returned for a new write to TiKV when this value is exceeded.
+ Default value: `"100MB"`
+ Unit: MB|GB

### `reserve-space`

+ The size of the temporary file that preoccupies the extra space when TiKV is started. The name of temporary file is `space_placeholder_file`, located in the `storage.data-dir` directory. When TiKV runs out of disk space and cannot be started normally, you can delete this file as an emergency intervention and set `reserve-space` to `"0MB"`.
+ Default value: `"2GB"`
+ Unite: MB|GB

## storage.block-cache

Configuration items related to the sharing of block cache among multiple RocksDB Column Families (CF). When these configuration items are enabled, block cache separately configured for each column family is disabled.

### `shared`

+ Enables or disables the sharing of block cache.
+ Default value: `true`

### `capacity`

+ The size of the shared block cache.
+ Default value: 45% of the size of total system memory
+ Unit: KB|MB|GB

## raftstore

Configuration items related to Raftstore

### `sync-log`

+ Enables or disables synchronous write mode. In the synchronous write mode, each commit is forced to be flushed to raft-log synchronously for persistent storage.
+ Default value: `true`

> **Warning:**
>
> Setting this value to `false` might lead to **data loss**. It is **strongly recommended** that you do not modify this configuration.

### `prevote`

+ Enables or disables `prevote`. Enabling this feature helps reduce jitter on the system after recovery from network partition.
+ Default value: `true`

### `raftdb-path`

+ The path to the Raft library, which is `storage.data-dir/raft` by default
+ Default value: ""

### `raft-base-tick-interval`

+ The time interval at which the Raft state machine ticks
+ Default value: `"1s"`
+ Minimum value: greater than `0`

### `raft-heartbeat-ticks`

+ The number of passed ticks when the heartbeat is sent. This means that a heartbeat is sent at the time interval of `raft-base-tick-interval` * `raft-heartbeat-ticks`.
+ Default value: `2`
+ Minimum value: greater than `0`

### `raft-election-timeout-ticks`

+ The number of passed ticks when Raft election is initiated. This means that if Raft group is missing the leader, a leader election is initiated approximately after the time interval of `raft-base-tick-interval` * `raft-election-timeout-ticks`.
+ Default value: `10`
+ Minimum value: `raft-heartbeat-ticks`

### `raft-min-election-timeout-ticks`

+ The minimum number of ticks during which the Raft election is initiated. If the number is `0`, the value of `raft-election-timeout-ticks` is used. The value of this parameter must be greater than or equal to `raft-election-timeout-ticks`.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-election-timeout-ticks`

+ The maximum number of ticks during which the Raft election is initiated. If the number is `0`, the value of `raft-election-timeout-ticks` * `2` is used.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-size-per-msg`

+ The soft limit on the size of a single message packet
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: MB

### `raft-max-inflight-msgs`

+ The number of Raft logs to be confirmed. If this number is exceeded, log sending slows down.
+ Default value: `256`
+ Minimum value: greater than `0`

### `raft-entry-max-size`

+ The hard limit on the maximum size of a single log
+ Default value: `"8MB"`
+ Minimum value: `0`
+ Unit: MB|GB

### `raft-log-gc-tick-interval`

+ The time interval at which the polling task of deleting Raft logs is scheduled. `0` means that this feature is disabled.
+ Default value: `"10s"`
+ Minimum value: `0`

### `raft-log-gc-threshold`

+ The soft limit on the maximum allowable count of residual Raft logs
+ Default value: `50`
+ Minimum value: `1`

### `raft-log-gc-count-limit`

+ The hard limit on the allowable number of residual Raft logs
+ Default value: the log number that can be accommodated in the 3/4 Region size (calculated as 1MB for each log)
+ Minimum value: `0`

### `raft-log-gc-size-limit`

+ The hard limit on the allowable size of residual Raft logs
+ Default value: 3/4 of the Region size
+ Minimum value: greater than `0`

### `raft-entry-cache-life-time`

+ The maximum remaining time allowed for the log cache in memory.
+ Default value: `"30s"`
+ Minimum value: `0`

### `raft-reject-transfer-leader-duration`

+ The protection time for new nodes, which is used to control the shortest interval to migrate a leader to the newly added node. Setting this value too small might cause the failure of leader transfer.
+ Default value: `"3s"`
+ Minimum value: `0`

### `hibernate-regions` (**Experimental**)

+ Enables or disables Hibernate Region. When this option is enabled, a Region idle for a long time is automatically set as hibernated. This reduces the extra overhead caused by heartbeat messages between the Raft leader and the followers for idle Regions. You can use `peer-stale-state-check-interval` to modify the heartbeat interval between the leader and the followers of hibernated Regions.
+ Default value: false

### `split-region-check-tick-interval`

+ Specifies the interval at which to check whether the Region split is needed. `0` means that this feature is disabled.
+ Default value: `"10s"`
+ Minimum value: `0`

### `region-split-check-diff`

+ The maximum value by which the Region data is allowed to exceed before Region split
+ Default value: 1/16 of the Region size.
+ Minimum value: `0`

### `region-compact-check-interval`

+ The time interval at which to check whether it is necessary to manually trigger RocksDB compaction. `0` means that this feature is disabled.
+ Default value: `"5m"`
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

+ The time interval at which a Region's heartbeat to PD is triggered. `0` means that this feature is disabled.
+ Default value: `"1m"`
+ Minimum value: `0`

### `pd-store-heartbeat-tick-interval`

+ The time interval at which a store's heartbeat to PD is triggered. `0` means that this feature is disabled.
+ Default value: `"10s"`
+ Minimum value: `0`

### `snap-mgr-gc-tick-interval`

+ The time interval at which the recycle of expired snapshot files is triggered. `0` means that this feature is disabled.
+ Default value: `"1m"`
+ Minimum value: `0`

### `snap-gc-timeout`

+ The longest time for which a snapshot file is saved
+ Default value: `"4h"`
+ Minimum value: `0`

### `lock-cf-compact-interval`

+ The time interval at which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: `"256MB"`
+ Default value: `"10m"`
+ Minimum value: `0`

### `lock-cf-compact-bytes-threshold`

+ The size out of which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: `"256MB"`
+ Minimum value: `0`
+ Unit: MB

### `notify-capacity`

+ The longest length of the Region message queue.
+ Default value: `40960`
+ Minimum value: `0`

### `messages-per-tick`

+ The maximum number of messages processed per batch
+ Default value: `4096`
+ Minimum value: `0`

### `max-peer-down-duration`

+ The longest inactive duration allowed for a peer. A peer with timeout is marked as `down`, and PD tries to delete it later.
+ Default value: `"5m"`
+ Minimum value: `0`

### `max-leader-missing-duration`

+ The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer verifies with PD whether the peer has been deleted.
+ Default value: `"2h"`
+ Minimum value: greater than `abnormal-leader-missing-duration`

### `abnormal-leader-missing-duration`

+ The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer is seen as abnormal and marked in metrics and logs.
+ Default value: `"10m"`
+ Minimum value: greater than `peer-stale-state-check-interval`

### `peer-stale-state-check-interval`

+ The time interval to trigger the check for whether a peer is in the state where a Raft group is missing the leader.
+ Default value: `"5m"`
+ Minimum value: greater than `2 * election-timeout`

### `leader-transfer-max-log-lag`

+ The maximum number of missing logs allowed for the transferee during a Raft leader transfer
+ Default value: `128`
+ Minimum value: `10`

### `snap-apply-batch-size`

+ The memory cache size required when the imported snapshot file is written into the disk
+ Default value: `"10MB"`
+ Minimum value: `0`
+ Unit: MB

### `consistency-check-interval`

+ The time interval at which the consistency check is triggered. `0` means that this feature is disabled.
+ Default value: `"0s"`
+ Minimum value: `0`

### `raft-store-max-leader-lease`

+ The longest trusted period of a Raft leader
+ Default value: `"9s"`
+ Minimum value: `0`

### `allow-remove-leader`

+ Determines whether to allow deleting the main switch
+ Default value: `false`

### `merge-max-log-gap`

+ The maximum number of missing logs allowed when `merge` is performed
+ Default value: `10`
+ Minimum value: greater than `raft-log-gc-count-limit`

### `merge-check-tick-interval`

+ The time interval at which TiKV checks whether a Region needs merge
+ Default value: `"10s"`
+ Minimum value: greater than `0`

### `use-delete-range`

+ Determines whether to delete data from the `rocksdb delete_range` interface
+ Default value: `false`

### `cleanup-import-sst-interval`

+ The time interval at which the expired SST file is checked. `0` means that this feature is disabled.
+ Default value: `"10m"`
+ Minimum value: `0`

### `local-read-batch-size`

+ The maximum number of read requests processed in one batch
+ Default value: `1024`
+ Minimum value: greater than `0`

### `apply-max-batch-size`

+ The maximum number of requests for data flushing in one batch
+ Default value: `1024`
+ Minimum value: greater than `0`

### `apply-pool-size`

+ The allowable number of threads in the pool that flushes data to storage
+ Default value: `2`
+ Minimum value: greater than `0`

### `store-max-batch-size`

+ The maximum number of requests processed in one batch
+ Default value: `1024`
+ Minimum value: greater than `0`

### `store-pool-size`

+ The allowable number of threads that process Raft
+ Default value: `2`
+ Minimum value: greater than `0`

### `future-poll-size`

+ The allowable number of threads that drive `future`
+ Default value: `1`
+ Minimum value: greater than `0`

## Coprocessor

Configuration items related to Coprocessor

### `split-region-on-table`

+ Determines whether to split Region by table. It is recommended for you to use the feature only in TiDB mode.
+ Default value: `false`

### `batch-split-limit`

+ The threshold of Region split in batches. Increasing this value speeds up Region split.
+ Default value: `10`
+ Minimum value: `1`

### `region-max-size`

+ The maximum size of a Region. When the value is exceeded, the Region splits into many.
+ Default value: `"144MB"`
+ Unit: KB|MB|GB

### `region-split-size`

+ The size of the newly split Region. This value is an estimate.
+ Default value: `"96MB"`
+ Unit: KB|MB|GB

### `region-max-keys`

+ The maximum allowable number of keys in a Region. When this value is exceeded, the Region splits into many.
+ Default value: `1440000`

### `region-split-keys`

+ The number of keys in the newly split Region. This value is an estimate.
+ Default value: `960000`

## RocksDB

Configuration items related to RocksDB

### `max-background-jobs`

+ The number of background threads in RocksDB
+ Default value: `8`
+ Minimum value: `2`

### `max-background-flushes`

+ The maximum number of concurrent background memtable flush jobs
+ Default value: `2`
+ Minimum value: `1`

### `max-sub-compactions`

+ The number of sub-compaction operations performed concurrently in RocksDB
+ Default value: `3`
+ Minimum value: `1`

### `max-open-files`

+ The total number of files that RocksDB can open
+ Default value: `40960`
+ Minimum value: `-1`

### `max-manifest-file-size`

+ The maximum size of a RocksDB Manifest file
+ Default value: `"128MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `create-if-missing`

+ Determines whether to automatically create a DB switch
+ Default value: `true`

### `wal-recovery-mode`

+ WAL recovery mode
+ Optional values: `0` (`TolerateCorruptedTailRecords`), `1` (`AbsoluteConsistency`), `2` (`PointInTimeRecovery`), `3` (`SkipAnyCorruptedRecords`)
+ Default value: `2`
+ Minimum value: `0`
+ Maximum value: `3`

### `wal-dir`

+ The directory in which WAL files are stored
+ Default value: `"/tmp/tikv/store"`

### `wal-ttl-seconds`

+ The living time of the archived WAL files. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ unit: second

### `wal-size-limit`

+ The size limit of the archived WAL files. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `enable-statistics`

+ Determines whether to enable the statistics of RocksDB
+ Default value: `true`

### `stats-dump-period`

+ The interval at which statistics are output to the log.
+ Default value: `10m`

### `compaction-readahead-size`

+ The size of `readahead` when compaction is being performed
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `writable-file-max-buffer-size`

+ The maximum buffer size used in WritableFileWrite
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ Determines whether to use `O_DIRECT` for both reads and writes in background flush and compactions
+ Default value: `false`

### `rate-bytes-per-sec`

+ The maximum rate permitted by Rate Limiter
+ Default value: `0`
+ Minimum value: `0`
+ Unit: Bytes

### `rate-limiter-mode`

+ Rate LImiter mode
+ Optional values: `1` (`ReadOnly`), `2` (`WriteOnly`), `3` (`AllIo`)
+ Default value: `2`
+ Minimum value: `1`
+ Maximum value: `3`

### `auto-tuned`

+ Determines whether to automatically optimize the configuration of the Rate LImiter
+ Default value: `false`

### `enable-pipelined-write`

+ Enables or disables Pipelined Write
+ Default value: `true`

### `bytes-per-sync`

+ The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `wal-bytes-per-sync`

+ The rate at which OS incrementally synchronizes WAL files to disk while the WAL files are being written
+ Default value: `"512KB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-max-size`

+ The maximum size of Info log
+ Default value: `"1GB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-roll-time`

+ The time interval at which Info logs are truncated. If the value is `0s`, logs are not truncated.
+ Default value: `"0s"`

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

+ Enables or disables Titan
+ Default value: `false`

### `dirname`

+ The directory in which the Titan Blob file is stored
+ Default value: `"titandb"`

### `disable-gc`

+ Determines whether to disable Garbage Collection (GC) that Titan performs to Blob files
+ Default value: `false`

### `max-background-gc`

+ The maximum number of GC threads in Titan
+ Default value: `4`
+ Minimum value: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf

Configuration items related to `rocksdb.defaultcf`, `rocksdb.writecf`, and `rocksdb.lockcf`.

### `block-size`

+ The default size of a RocksDB block
+ Default value for `defaultcf` and `writecf`: `"64KB"`
+ Default value for `lockcf`: `"16KB"`
+ Minimum value: `"1KB"`
+ Unit: KB|MB|GB

### `block-cache-size`

+ The cache size of a RocksDB block
+ Default value for `defaultcf`: `Total machine memory * 25%`
+ Default value for `writecf`: `Total machine memory * 15%`
+ Default value for `lockcf`: `Total machine memory * 2%`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `disable-block-cache`

+ Enables or disables block cache
+ Default value: `false`

### `cache-index-and-filter-blocks`

+ Enables or disables caching index and filter
+ Default value: `true`

### `pin-l0-filter-and-index-blocks`

+ Determines whether to pin the index and filter at L0
+ Default value: `true`

### `use-bloom-filter`

+ Enables or disables bloom filter
+ Default value: `true`

### `optimize-filters-for-hits`

+ Determines whether to optimize the hit ratio of filters
+ Default value for `defaultcf`: `true`
+ Default value for `writecf` and `lockcf`: `false`

### `whole-key-filtering`

+ Determines whether to put the entire key to bloom filter
+ Default value for `defaultcf`and `lockcf`: `true`
+ Default value for `writecf`: `false`

### `bloom-filter-bits-per-key`

+ The length that bloom filter reserves for each key
+ Default value: `10`
+ unit: byte

### `block-based-bloom-filter`

+ Determines whether each block creates a bloom filter
+ Default value: `false`

### `read-amp-bytes-per-bit`

+ Enables or disables statistics of read amplification.
+ Optional values: `0` (disabled), > `0` (enabled).
+ Default value: `0`
+ Minimum value: `0`

### `compression-per-level`

+ The default compression algorithm for each level
+ Default value for `defaultcf`: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ Default value for `writecf`: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ Default value for `lockcf`: ["no", "no", "no", "no", "no", "no", "no"]

### `write-buffer-size`

+ Memtable size
+ Default value for `defaultcf` and `writecf`: `"128MB"`
+ Default value for `lockcf`: `"32MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-write-buffer-number`

+ The maximum number of memtables
+ Default value: `5`
+ Minimum value: `0`

### `min-write-buffer-number-to-merge`

+ The minimum number of memtables required to trigger flush
+ Default value: `1`
+ Minimum value: `0`

### `max-bytes-for-level-base`

+ The maximum number of bytes at base level (L1). Generally, it is set to 4 times the size of a memtable.
+ Default value for `defaultcf` and `writecf`: `"512MB"`
+ Default value for `lockcf`: `"128MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `target-file-size-base`

+ The size of the target file at base level
+ Default: `"8MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `level0-file-num-compaction-trigger`

+ The maximum number of files at L0 that trigger compaction
+ Default value for `defaultcf` and `writecf`: `4`
+ Default value for `lockcf`: `1`
+ Minimum value: `0`

### `level0-slowdown-writes-trigger`

+ The maximum number of files at L0 that trigger write stall
+ Default value: `20`
+ Minimum value: `0`

### `level0-stop-writes-trigger`

+ The maximum number of files at L0 required to completely block write
+ Default value: `36`
+ Minimum value: `0`

### `max-compaction-bytes`

+ The maximum number of bytes written into disk per compaction
+ Default value: `"2GB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `compaction-pri`

+ The priority type of compaction
+ Optional values: `0` (`ByCompensatedSize`), `1` (`OldestLargestSeqFirst`), `2` (`OldestSmallestSeqFirst`), `3` (`MinOverlappingRatio`)
+ Default value for `defaultcf` and `writecf`: `3`
+ Default value for `lockcf`: `0`

### `dynamic-level-bytes`

+ Determines whether to optimize dynamic level bytes
+ Default value: `true`

### `num-levels`

+ The maximum number of levels in a RocksDB file
+ Default value: `7`

### `max-bytes-for-level-multiplier`

+ The default amplification multiple for each layer
+ Default value: `10`

### `compaction-style`

+ Compaction method
+ Optional values (only numbers can be accepted): `0` (`Level`), `1` (`Universal`), `2` (`Fifo`)
+ Default value: `0`

### `disable-auto-compactions`

+ Determines whether to disable auto compaction.
+ Default value: `false`

### `soft-pending-compaction-bytes-limit`

+ The soft limit on the pending compaction bytes
+ Default value: `"64GB"`
+ Unit: KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ The hard limit on the pending compaction bytes
+ Default value: `"256GB"`
+ Unit: KB|MB|GB

## `rocksdb.defaultcf.titan`

Configuration items related to `rocksdb.defaultcf.titan`.

### `min-blob-size`

+ The smallest value stored in a Blob file. Values smaller than the specified size are stored in the LSM-Tree.
+ Default value: `"1KB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `blob-file-compression`

+ The compression algorithm used in a Blob file
+ Optional values: `"no"`, `"snappy"`, `"zlib"`, `"bzip2"`, `"lz4"`, `"lz4hc"`, `"zstd"`
+ Default value: `"lz4"`

### `blob-cache-size`

+ The cache size of a Blob file
+ Default value: `"0GB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `min-gc-batch-size`

+ The minimum total size of Blob files required to perform GC for one time
+ Default value: `"16MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-gc-batch-size`

+ The maximum total size of Blob files allowed to perform GC for one time
+ Default value: `"64MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `discardable-ratio`

+ The ratio at which GC is triggered for Blob files. The Blob file can be selected for GC only if the proportion of the invalid values in a Blob file exceeds this ratio.
+ Default value: `0.5`
+ Minimum value: `0`
+ Maximum value: `1`

### `sample-ratio`

+ The ratio of (data read from a Blob file/the entire Blob file) when sampling the file during GC
+ Default value: `0.1`
+ Minimum value: `0`
+ Maximum value: `1`

### `merge-small-file-threshold`

+ When the size of a Blob file is smaller than this value, the Blob file might still be selected for GC. In this situation, `discardable-ratio` is ignored.
+ Default value: `"8MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `blob-run-mode`

+ Specifies the running mode of Titan.
+ Optional values:
    + `normal`: Writes data to the blob file when the value size exceeds `min-blob-size`.
    + `read_only`: Refuses to write new data to the blob file, but still reads the original data from the blob file.
    + `fallback`: Writes data in the blob file back to LSM.
+ Default value: `normal`

### `level-merge`

+ Determines whether to optimize the read performance. When `level-merge` is enabled, there is more write amplification.
+ Default value: `false`

### `gc-merge-rewrite`

+ Determines whether to use the merge operator to write back blob indexes for Titan GC. When `gc-merge-rewrite` is enabled, it reduces the effect of Titan GC on the writes in the foreground.
+ Default value: `false`

## `raftdb`

Configuration items related to `raftdb`

### `max-background-jobs`

+ The number of background threads in RocksDB
+ Default value: `4`
+ Minimum value: `2`

### `max-sub-compactions`

+ The number of concurrent sub-compaction operations performed in RocksDB
+ Default value: `2`
+ Minimum value: `1`

### `wal-dir`

+ The directory in which WAL files are stored
+ Default value: `"/tmp/tikv/store"`

## security

Configuration items related to security

### `ca-path`

+ The path of the CA file
+ Default value: ""

### `cert-path`

+ The path of the Privacy Enhanced Mail (PEM) file that contains the X509 certificate
+ Default value: ""

### `key-path`

+ The path of the PEM file that contains the X509 key
+ Default value: ""

### `redact-info-log` <span class="version-mark">New in v4.0.8</span>

+ This configuration item enables or disables log redaction. If the configuration value is set to `true`, all user data in the log will be replaced by `?`.
+ Default value: `false`

## security.encryption

Configuration items related to [encryption at rest](/encryption-at-rest.md) (TDE).

### `data-encryption-method`

+ The encryption method for data files
+ Value options: "plaintext", "aes128-ctr", "aes192-ctr", and "aes256-ctr"
+ A value other than "plaintext" means that encryption is enabled, in which case the master key must be specified.
+ Default value: `"plaintext"`

### `data-key-rotation-period`

+ Specifies how often TiKV rotates the data encryption key.
+ Default value: `7d`

### enable-file-dictionary-log

+ Enables the optimization to reduce I/O and mutex contention when TiKV manages the encryption metadata.
+ To avoid possible compatibility issues when this configuration parameter is enabled (by default), see [Encryption at Rest - Compatibility between TiKV versions](/encryption-at-rest.md#compatibility-between-tikv-versions) for details.
+ Default value: `true`

### master-key

+ Specifies the master key if encryption is enabled. To learn how to configure a master key, see [Encryption at Rest - Configure encryption](/encryption-at-rest.md#configure-encryption).

### previous-master-key

+ Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see [Encryption at Rest - Configure encryption](/encryption-at-rest.md#configure-encryption).

## `import`

Configuration items related to TiDB Lightning import and BR restore.

### `num-threads`

+ The number of threads to process RPC requests
+ Default value: `8`
+ Minimum value: `1`

### `num-import-jobs`

+ The number of jobs imported concurrently
+ Default value: `8`
+ Minimum value: `1`
  
## backup

Configuration items related to BR backup.

### `num-threads`

+ The number of worker threads to process backup
+ Default value: `MIN(CPU * 0.75, 32)`.
+ Minimum value: `1` 

## cdc <span class="version-mark">New in v4.0.5</span>

Configuration items related to TiCDC.

### `min-ts-interval`

+ The interval at which Resolved TS is calculated and forwarded.
+ Default value: `"1s"`

### `sink-memory-quota`

+ The upper limit of memory usage by TiCDC data change events.
+ Default value: `512MB`

### `incremental-scan-threads`

+ The number of threads for the task of incrementally scanning historical data.
+ Default value: `4`, which means 4 threads.

### `incremental-scan-concurrency`

+ The maximum number of concurrent executions for the tasks of incrementally scanning historical data.
+ Default value: `6`, which means 6 tasks can be concurrent executed at most.
+ Note: The value of `incremental-scan-concurrency` must be greater than or equal to that of `incremental-scan-threads`; otherwise, TiKV will report an error at startup.

## pessimistic-txn

### `enabled`

- Enables the pessimistic transaction mode. For pessimistic transaction usage, refer to [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md).
- Default value: `true`

### `wait-for-lock-timeout`

- The longest time that a pessimistic transaction in TiKV waits for other transactions to release the lock. If the time is out, an error is returned to TiDB, and TiDB retries to add a lock. The lock wait timeout is set by `innodb_lock_wait_timeout`.
- Default value: `"1s"`
- Minimum value: `"1ms"`

### `wake-up-delay-duration`

- When pessimistic transactions release the lock, among all the transactions waiting for lock, only the transaction with the smallest `start_ts` is woken up. Other transactions will be woken up after `wake-up-delay-duration`.
- Default value: `"20ms"`

### `pipelined`

- This configuration item enables the pipelined process of adding the pessimistic lock. With this feature enabled, after detecting that data can be locked, TiKV immediately notifies TiDB to execute the subsequent requests and write the pessimistic lock asynchronously, which reduces most of the latency and significantly improves the performance of pessimistic transactions. But there is a still low probability that the asynchronous write of the pessimistic lock fails, which might cause the failure of pessimistic transaction commits.
- Default value: `false`
