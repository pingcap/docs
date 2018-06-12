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

- The limit of a TiKV server sending snapshot concurrently
- Default: 32

### `concurrent-recv-snap-limit`

- The limit of a TiKV server receiving snapshot concurrently
- Default: 32

### `snap-max-write-bytes-per-sec`

- The max bytes for a TiKV server writing the snapshot file to the disk in one second. 
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


- Default: "0KB"

### `raft-base-tick-interval`

- Default: "1s"

### `raft-heartbeat-ticks`

- Default: 2

### `raft-election-timeout-ticks`

- Default: 10

### `raft-min-election-timeout-ticks`

- Default: 10

### `raft-max-election-timeout-ticks`

- Default: 20

### `raft-max-size-per-msg`

- Default: "1MB"

### `raft-max-inflight-msgs`

- Default: 256

### `raft-entry-max-size`

- Default: "8MB"

### `raft-log-gc-tick-interval`

- Default: "10s"

### `raft-log-gc-threshold`

- Default: 50

### `raft-log-gc-count-limit`

- Default: 73728

### `raft-log-gc-size-limit`

- Default: "72MB"

### `split-region-check-tick-interval`

- Default: "10s"

### `region-split-check-diff`

- Default: "6MB"

### `region-compact-check-interval`

- Default: "5m"

### `clean-stale-peer-delay`

- Default: "11m"

### `region-compact-check-step`

- Default: 100

### `region-compact-min-tombstones`

- Default: 10000

### `pd-heartbeat-tick-interval`
- Default: "1m"

### `pd-store-heartbeat-tick-interval`

- Default: "10s"

### `snap-mgr-gc-tick-interval`

- Default: "1m"

### `snap-gc-timeout`

- Default: "4h"

### `lock-cf-compact-interval`

- Default: "10m"

### `lock-cf-compact-bytes-threshold`

- Default: "256MB"

### `notify-capacity`

- Default: 40960

### `messages-per-tick`

- Default: 4096

### `max-peer-down-duration`

- Default: "5m"

### `max-leader-missing-duration`

- Default: "2h"

### `abnormal-leader-missing-duration`

- Default: "10m"

### `peer-stale-state-check-interval`

- Default: "5m"

### `snap-apply-batch-size`

- Default: "10MB"

### `consistency-check-interval`

- Default: "0s"

### `report-region-flow-interval`

- Default: "1m"

### `raft-store-max-leader-lease`

- Default: "9s"

### `right-derive-when-split`

- Default: true

### `allow-remove-leader`

- Default: false

### `merge-max-log-gap`

- Default: 10

### `merge-check-tick-interval`

- Default: "10s"

### `use-delete-range`

- Default: false

### `cleanup-import-sst-interval`

- Default: "10m"

## `coprocessor`
### `split-region-on-table`

- Default: true

### `region-max-size`

- Default: "144MB"

### `region-split-size`

- Default: "96MB"

## `rocksdb`
### `wal-recovery-mode`

- Default: 2

### `wal-dir`

- Default: ""

### `wal-ttl-seconds`

- Default: 0
### `wal-size-limit`

- Default: "0KB"
### `max-total-wal-size`
- Default: "4GB"

### `max-background-jobs`

- Default: 6
### `max-manifest-file-size`

- Default: "20MB"
### `create-if-missing`
- Default: true
### `max-open-files`
- Default: 40960
### `enable-statistics`
- Default: true
### `stats-dump-period`
- Default: "10m"
### `compaction-readahead-size`
- Default: "0KB"
### `info-log-max-size`
- Default: "0KB"
### `info-log-roll-time`
- Default: "0s"
### `info-log-dir`
- Default: ""
### `rate-bytes-per-sec`
- Default: "0KB"
### `bytes-per-sync`
- Default: "1MB"
### `wal-bytes-per-sync`
- Default: "512KB"
### `max-sub-compactions`
- Default: 1
### `writable-file-max-buffer-size`
- Default: "1MB"
### `use-direct-io-for-flush-and-compaction`
- Default: false 
### `enable-pipelined-write`
- Default: true
    
### `defaultcf`
#### `block-size`
- Default: "64KB"
#### `block-cache-size`
- Default: "6GB"
#### `disable-block-cache`
- Default: false
#### `cache-index-and-filter-blocks`
- Default: true
#### `pin-l0-filter-and-index-blocks`
- Default: true
#### `use-bloom-filter`
- Default: true
#### `whole-key-filtering`
- Default: true
#### `bloom-filter-bits-per-key`
- Default: 10
#### `block-based-bloom-filter`
- Default: false
#### `read-amp-bytes-per-bit`
- Default: 0
#### `compression-per-level`
- Default: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
#### `write-buffer-size`
- Default: "128MB"
#### `max-write-buffer-number`
- Default: 5
#### `min-write-buffer-number-to-merge`
- Default: 1
#### `max-bytes-for-level-base`
- Default: "512MB"
#### `target-file-size-base`
- Default: "8MB"
#### `level0-file-num-compaction-trigger`
- Default: 4
#### `level0-slowdown-writes-trigger`
- Default: 20
#### `level0-stop-writes-trigger`
- Default: 36
#### `max-compaction-bytes`
- Default: "2GB"
#### `compaction-pri`
- Default: 3
#### `dynamic-level-bytes`
- Default: false
#### `num-levels`
- Default: 7
#### `max-bytes-for-level-multiplier`
- Default: 10
#### `compaction-style`
- Default: 0
#### `disable-auto-compactions`
- Default: false
#### `soft-pending-compaction-bytes-limit`
- Default: "64GB"
#### `hard-pending-compaction-bytes-limit`
- Default: "256GB"

### `writecf`
### `lockcf`  
### `raftcf`
      
 
## `raftdb`
### `defaultcf`
      

## `security`
### `ca-path`
- Default: ""
### `cert-path`
- Default: ""

### `key-path`
- Default: ""
  
## `import`
### `import-dir`
- Default: "/tmp/tikv/import"
### `num-threads`
- Default: 8
### `stream-channel-window`
- Default: 128