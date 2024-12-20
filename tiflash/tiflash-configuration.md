---
title: Configure TiFlash
summary: TiFlashの設定方法を学習します。
---

# TiFlashを設定する {#configure-tiflash}

このドキュメントでは、 TiFlashの展開と使用に関連する構成パラメータについて説明します。

## PD スケジューリングパラメータ {#pd-scheduling-parameters}

[pd-ctl](/pd-control.md)使用して PD スケジューリング パラメータを調整できます。tiup を使用してクラスターをデプロイおよび管理する場合は、 `pd-ctl -u <pd_ip:pd_port>`代わりに`tiup ctl:v<CLUSTER_VERSION> pd`使用できることに注意してください。

-   [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit) : レプリカ関連のオペレータが生成されるレートを決定します。このパラメータは、ノードをオフラインにしたり、レプリカを追加したりする操作に影響します。

    > **注記：**
    >
    > このパラメータの値は`region-schedule-limit`未満である必要があります。そうでない場合、TiKV ノード間の通常のリージョンスケジューリングが影響を受けます。

-   `store-balance-rate` : 各 TiKV/ TiFlashストアの領域がスケジュールされるレートを制限します。このパラメータは、ストアがクラスターに新しく参加した場合にのみ有効になることに注意してください。既存のストアの設定を変更する場合は、次のコマンドを使用します。

    > **注記：**
    >
    > v4.0.2 以降、 `store-balance-rate`パラメータは非推奨となり、 `store limit`コマンドに変更が加えられました。詳細については[店舗制限](/configure-store-limit.md)参照してください。

    -   指定されたストアのスケジューリング レートを設定するには、 `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>`コマンドを実行します。( `store_id`取得するには、 `pd-ctl -u <pd_ip:pd_port> store`コマンドを実行できます。
    -   指定されたストアのリージョンのスケジュール レートを設定しない場合、このストアは`store-balance-rate`の設定を継承します。
    -   `pd-ctl -u <pd_ip:pd_port> store limit`コマンドを実行すると、現在の設定値`store-balance-rate`を表示できます。

-   [`replication.location-labels`](/pd-configuration-file.md#location-labels) : TiKV インスタンスのトポロジ関係を示します。キーの順序は、異なるラベルの階層関係を示します。TiFlashが有効になっている場合は、 [`pd-ctl config placement-rules`](/pd-control.md#config-show--set-option-value--placement-rules)使用してデフォルト値を設定する必要があります。詳細については、 [地理的に分散された展開トポロジ](/geo-distributed-deployment-topology.md)参照してください。

## TiFlash構成パラメータ {#tiflash-configuration-parameters}

このセクションでは、 TiFlashの設定パラメータについて説明します。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>tiflash.toml</code>ファイルを設定する {#configure-the-code-tiflash-toml-code-file}

```toml
## The listening host for supporting services such as TPC/HTTP. It is recommended to configure it as "0.0.0.0", which means to listen on all IP addresses of this machine.
listen_host = "0.0.0.0"
## The TiFlash TCP service port. This port is used for internal testing and is set to 9000 by default. Before TiFlash v7.1.0, this port is enabled by default with a security risk. To enhance security, it is recommended to apply access control on this port to only allow access from whitelisted IP addresses. Starting from TiFlash v7.1.0, you can avoid the security risk by commenting out the configuration of this port. When the TiFlash configuration file does not specify this port, it will be disabled. 
## It is **NOT** recommended to configure this port in any TiFlash deployment. (Note: Starting from TiFlash v7.1.0, TiFlash deployed by TiUP >= v1.12.5 or TiDB Operator >= v1.5.0 disables the port by default and is more secure.)
# tcp_port = 9000
## The cache size limit of the metadata of a data block. Generally, you do not need to change this value.
mark_cache_size = 1073741824
## The cache size limit of the min-max index of a data block. Generally, you do not need to change this value.
minmax_index_cache_size = 1073741824
## The cache size limit of the DeltaIndex. The default value is 0, which means no limit.
delta_index_cache_size = 0

## The storage path of TiFlash data. If there are multiple directories, separate each directory with a comma.
## path and path_realtime_mode are deprecated since v4.0.9. Use the configurations
## in the [storage] section to get better performance in the multi-disk deployment scenarios
## Since TiDB v5.2.0, if you need to use the storage.io_rate_limit configuration, you need to set the storage path of TiFlash data to storage.main.dir at the same time.
## When the [storage] configurations exist, both path and path_realtime_mode configurations are ignored.
# path = "/tidb-data/tiflash-9000"
## or
# path = "/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"
## The default value is false. If you set it to true and multiple directories
## are set in the path, the latest data is stored in the first directory and older
## data is stored in the rest directories.
# path_realtime_mode = false

## The path in which the TiFlash temporary files are stored. By default it is the first directory in path
## or in storage.latest.dir appended with "/tmp".
# tmp_path = "/tidb-data/tiflash-9000/tmp"

## Storage paths settings take effect starting from v4.0.9
[storage]

    ## DTFile format
    ## * format_version = 2, the default format for versions < v6.0.0.
    ## * format_version = 3, the default format for v6.0.0 and v6.1.x, which provides more data validation features.
    ## * format_version = 4, the default format for versions from v6.2.0 to v7.3.0, which reduces write amplification and background task resource consumption
    ## * format_version = 5, introduced in v7.3.0, the default format for versions from v7.4.0 to v8.3.0, which reduces the number of physical files by merging smaller files.
    ## * format_version = 6, introduced in v8.4.0, which partially supports the building and storage of vector indexes.
    ## * format_version = 7, introduced in v8.4.0, the default format for v8.4.0 and later versions, which supports the build and storage of vector indexes
    # format_version = 7

    [storage.main]
    ## The list of directories to store the main data. More than 90% of the total data is stored in
    ## the directory list.
    dir = [ "/tidb-data/tiflash-9000" ]
    ## or
    # dir = [ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]

    ## The maximum storage capacity of each directory in storage.main.dir.
    ## If it is not set, or is set to multiple 0, the actual disk (the disk where the directory is located) capacity is used.
    ## Note that human-readable numbers such as "10GB" are not supported yet.
    ## Numbers are specified in bytes.
    ## The size of the capacity list should be the same with the dir size.
    ## For example:
    # capacity = [ 10737418240, 10737418240 ]

    [storage.latest]
    ## The list of directories to store the latest data. About 10% of the total data is stored in
    ## the directory list. The directories (or directory) listed here require higher IOPS
    ## metrics than those in storage.main.dir.
    ## If it is not set (by default), the values of storage.main.dir are used.
    # dir = [ ]
    ## The maximum storage capacity of each directory in storage.latest.dir.
    ## If it is not set, or is set to multiple 0, the actual disk (the disk where the directory is located) capacity is used.
    # capacity = [ 10737418240, 10737418240 ]

    ## [storage.io_rate_limit] settings are new in v5.2.0.
    [storage.io_rate_limit]
    ## This configuration item determines whether to limit the I/O traffic, which is disabled by default. This traffic limit in TiFlash is suitable for cloud storage that has the disk bandwidth of a small and specific size.
    ## The total I/O bandwidth for disk reads and writes. The unit is bytes and the default value is 0, which means the I/O traffic is not limited by default.
    # max_bytes_per_sec = 0
    ## max_read_bytes_per_sec and max_write_bytes_per_sec have similar meanings to max_bytes_per_sec. max_read_bytes_per_sec means the total I/O bandwidth for disk reads, and max_write_bytes_per_sec means the total I/O bandwidth for disk writes.
    ## These configuration items limit I/O bandwidth for disk reads and writes separately. You can use them for cloud storage that calculates the limit of I/O bandwidth for disk reads and writes separately, such as the Persistent Disk provided by Google Cloud.
    ## When the value of max_bytes_per_sec is not 0, max_bytes_per_sec is prioritized.
    # max_read_bytes_per_sec = 0
    # max_write_bytes_per_sec = 0

    ## The following parameters control the bandwidth weights assigned to different I/O traffic types. Generally, you do not need to adjust these parameters.
    ## TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads.
    ## When the I/O traffic limit is initialized, TiFlash assigns the bandwidth according to the following weight ratio.
    ## The following  default configurations indicate that each type of traffic gets a weight of 25% (25 / (25 + 25 + 25 + 25) = 25%).
    ## If the weight is configured to 0, the corresponding I/O traffic is not limited.
    # foreground_write_weight = 25
    # background_write_weight = 25
    # foreground_read_weight = 25
    # background_read_weight = 25
    ## TiFlash supports automatically tuning the traffic limit for different I/O types according to the current I/O load. Sometimes, the tuned bandwidth might exceed the weight ratio set above.
    ## auto_tune_sec indicates the interval of automatic tuning. The unit is seconds. If the value of auto_tune_sec is 0, the automatic tuning is disabled.
    # auto_tune_sec = 5

    ## The following configuration items only take effect for the TiFlash disaggregated storage and compute architecture mode. For details, see documentation at https://docs.pingcap.com/tidb/dev/tiflash-disaggregated-and-s3.
    # [storage.s3]
    # endpoint: http://s3.{region}.amazonaws.com # S3 endpoint address
    # bucket: mybucket                           # TiFlash stores all data in this bucket
    # root: /cluster1_data                       # Root directory where data is stored in the S3 bucket
    # access_key_id: {ACCESS_KEY_ID}             # Access S3 with ACCESS_KEY_ID
    # secret_access_key: {SECRET_ACCESS_KEY}     # Access S3 with SECRET_ACCESS_KEY
    # [storage.remote.cache]
    # dir: /data1/tiflash/cache        # Local data cache directory of the Compute Node
    # capacity: 858993459200           # 800 GiB

[flash]
    ## The listening address of TiFlash coprocessor services.
    service_addr = "0.0.0.0:3930"

    ## Introduced in v7.4.0. When the gap between the `applied_index` advanced by the current Raft state machine and the `applied_index` at the last disk spilling exceeds `compact_log_min_gap`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk. Increasing this gap might reduce the disk spilling frequency of TiFlash, thus reducing read latency in random write scenarios, but it might also increase memory overhead. Decreasing this gap might increase the disk spilling frequency of TiFlash, thus alleviating memory pressure in TiFlash. However, at this stage, the disk spilling frequency of TiFlash will not be higher than that of TiKV, even if this gap is set to 0.
    ## It is recommended to keep the default value.
    # compact_log_min_gap = 200
    ## Introduced in v5.0. When the number or the size of rows in the Regions cached by TiFlash exceeds either of the following thresholds, TiFlash executes the `CompactLog` command from TiKV and spills data to disk.
    ## It is recommended to keep the default value.
    # compact_log_min_rows = 40960 # 40k
    # compact_log_min_bytes = 33554432 # 32MB

    ## The following configuration item only takes effect for the TiFlash disaggregated storage and compute architecture mode. For details, see documentation at https://docs.pingcap.com/tidb/dev/tiflash-disaggregated-and-s3.
    # disaggregated_mode = tiflash_write # The supported mode is `tiflash_write` or `tiflash_compute.

[flash.proxy]
    ## The listening address of proxy. If it is left empty, 127.0.0.1:20170 is used by default.
    addr = "127.0.0.1:20170"
    ## The external access address of addr. If it is left empty, "addr" is used by default.
    ## Should guarantee that other nodes can access through `advertise-addr` when you deploy the cluster on multiple nodes.
    advertise-addr = ""
    ## The listening address from which the proxy pulls metrics or status information. If it is left empty, 127.0.0.1:20292 is used by default.
    status-addr = "127.0.0.1:20292"
    ## The external access address of status-addr. If it is left empty, the value of "status-addr" is used by default.
    ## Should guarantee that other nodes can access through `advertise-status-addr` when you deploy the cluster on multiple nodes.
    advertise-status-addr = ""
    ## The external access address of the TiFlash coprocessor service.
    engine-addr = "10.0.1.20:3930"
    ## The data storage path of proxy.
    data-dir = "/tidb-data/tiflash-9000/flash"
    ## The configuration file path of proxy.
    config = "/tidb-deploy/tiflash-9000/conf/tiflash-learner.toml"
    ## The log path of proxy.
    log-file = "/tidb-deploy/tiflash-9000/log/tiflash_tikv.log"

[logger]
    ## Note that the following parameters only take effect in tiflash.log and tiflash_error.log. If you need to configure log parameters of TiFlash Proxy, specify them in tiflash-learner.toml.
    ## log level (available options: "trace", "debug", "info", "warn", "error"). The default value is "info".
    level = "info"
    ## The log of TiFlash.
    log = "/tidb-deploy/tiflash-9000/log/tiflash.log"
    ## The error log of TiFlash. The "warn" and "error" level logs are also output to this log file.
    errorlog = "/tidb-deploy/tiflash-9000/log/tiflash_error.log"
    ## Size of a single log file. The default value is "100M".
    size = "100M"
    ## Maximum number of log files to save. The default value is 10. For TiFlash logs and TiFlash error logs, the maximum number of log files to save is `count` respectively.
    count = 10

[raft]
    ## PD service address. Multiple addresses are separated with commas.
    pd_addr = "10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"

[status]
    ## The port through which Prometheus pulls metrics information. The default value is 8234.
    metrics_port = 8234

[profiles]

[profiles.default]
    ## The default value is false. This parameter determines whether the segment
    ## of DeltaTree Storage Engine uses logical split.
    ## Using the logical split can reduce the write amplification.
    ## However, these are at the cost of disk space waste.
    ## It is strongly recommended to keep the default value `false` and
    ## not to change it to `true` in v6.2.0 and later versions. For details,
    ## see known issue [#5576](https://github.com/pingcap/tiflash/issues/5576).
    # dt_enable_logical_split = false

    ## `max_threads` indicates the internal thread concurrency when TiFlash executes an MPP task.
    ## The default value is 0. When it is set to 0,
    ## TiFlash uses the number of CPU cores as the execution concurrency.
    ## This parameter only takes effect
    ## when the system variable `tidb_max_tiflash_threads` is set to -1.
    max_threads = 0
    
    ## The memory usage limit for the generated intermediate data in a single query.
    ## When the value is an integer, the unit is byte. For example, 34359738368 means 32 GiB of memory limit, and 0 means no limit.
    ## When the value is a floating-point number in the range of [0.0, 1.0), it means the ratio of the allowed memory usage to the total memory of the node. For example, 0.8 means 80% of the total memory, and 0.0 means no limit.
    ## The default value is 0, which means no limit.
    ## When a query attempts to consume memory that exceeds this limit, the query is terminated and an error is reported.
    max_memory_usage = 0

    ## The memory usage limit for the generated intermediate data in all queries.
    ## When the value is an integer, the unit is byte. For example, 34359738368 means 32 GiB of memory limit, and 0 means no limit.
    ## When the value is a floating-point number in the range of [0.0, 1.0), it means the ratio of the allowed memory usage to the total memory of the node. For example, 0.8 means 80% of the total memory, and 0.0 means no limit.
    ## The default value is 0.8, which means 80% of the total memory.
    ## When the queries attempt to consume memory that exceeds this limit, the queries are terminated and an error is reported.
    max_memory_usage_for_all_queries = 0.8

    ## New in v5.0. This item specifies the maximum number of cop requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to 0 or not set, the default value is used, which is twice the number of physical cores.
    cop_pool_size = 0
    ## New in v5.0. This item specifies the maximum number of batch requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to 0 or not set, the default value is used, which is twice the number of physical cores.
    batch_cop_pool_size = 0
    ## New in v6.1.0. This item specifies the number of requests that TiFlash can concurrently process when it receives ALTER TABLE ... COMPACT from TiDB.
    ## If the value is set to 0, the default value 1 prevails.
    manual_compact_pool_size = 1
    ## New in v5.4.0. This item enables or disables the elastic thread pool feature, which significantly improves CPU utilization in high concurrency scenarios of TiFlash. The default value is true.
    enable_elastic_threadpool = true
    ## Compression algorithm of the TiFlash storage engine. The value can be LZ4, zstd, or LZ4HC, and is case-insensitive. By default, LZ4 is used.
    dt_compression_method = "LZ4"
    ## Compression level of the TiFlash storage engine. The default value is 1.
    ## It is recommended that you set this value to 1 if dt_compression_method is LZ4.
    ## It is recommended that you set this value to -1 (smaller compression rate, but better read performance) or 1 if dt_compression_method is zstd.
    ## It is recommended that you set this value to 9 if dt_compression_method is LZ4HC.
    dt_compression_level = 1

    ## New in v6.2.0. This item specifies the minimum ratio of valid data in a PageStorage data file. When the ratio of valid data in a PageStorage data file is less than the value of this configuration, GC is triggered to compact data in the file. The default value is 0.5.
    dt_page_gc_threshold = 0.5

    ## New in v7.0.0. This item specifies the maximum memory available for the HashAggregation operator with group by key before a disk spill is triggered. When the memory usage exceeds the threshold, HashAggregation reduces memory usage by spilling to disk. This item defaults to 0, which means that the memory usage is unlimited and spill to disk is never used for HashAggregation.
    max_bytes_before_external_group_by = 0

    ## New in v7.0.0. This item specifies the maximum memory available for the sort or topN operator before a disk spill is triggered. When the memory usage exceeds the threshold, the sort or topN operator reduces memory usage by spilling to disk. This item defaults to 0, which means that the memory usage is unlimited and spill to disk is never used for sort or topN.
    max_bytes_before_external_sort = 0

    ## New in v7.0.0. This item specifies the maximum memory available for the HashJoin operator with EquiJoin before a disk spill is triggered. When the memory usage exceeds the threshold, HashJoin reduces memory usage by spilling to disk. This item defaults to 0, which means that the memory usage is unlimited and spill to disk is never used for HashJoin with EquiJoin.
    max_bytes_before_external_join = 0

    ## New in v7.4.0. This item controls whether to enable the TiFlash resource control feature. When it is set to true, TiFlash uses the pipeline execution model.
    enable_resource_control = true

    ## New in v6.0.0. This item is used for the MinTSO scheduler. It specifies the maximum number of threads that one resource group can use. The default value is 5000. For details about the MinTSO scheduler, see https://docs.pingcap.com/tidb/dev/tiflash-mintso-scheduler.
    task_scheduler_thread_soft_limit = 5000

    ## New in v6.0.0. This item is used for the MinTSO scheduler. It specifies the maximum number of threads in the global scope. The default value is 10000. For details about the MinTSO scheduler, see https://docs.pingcap.com/tidb/dev/tiflash-mintso-scheduler.
    task_scheduler_thread_hard_limit = 10000

    ## New in v6.4.0. This item is used for the MinTSO scheduler. It specifies the maximum number of queries that can run simultaneously in a TiFlash instance. The default value is 0, which means twice the number of vCPUs. For details about the MinTSO scheduler, see https://docs.pingcap.com/tidb/dev/tiflash-mintso-scheduler.
    task_scheduler_active_set_soft_limit = 0

## Security settings take effect starting from v4.0.5.
[security]
    ## New in v5.0. This configuration item enables or disables log redaction. Value options: `true`, `false`, `"on"`, `"off"`, and `"marker"`. The `"on"`, `"off"`, and `"marker"` options are introduced in v8.2.0.
    ## If the configuration item is set to `false` or `"off"`, log redaction is disabled.
    ## If the configuration item is set to `true` or `"on"`, all user data in the log is replaced by `?`.
    ## If the configuration item is set to `"marker"`, all user data in the log is wrapped in `‹ ›`. If user data contains `‹` or `›`, `‹` is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.
    ## The default value is `false`.
    ## Note that you also need to set security.redact-info-log for tiflash-learner's logging in tiflash-learner.toml.
    # redact_info_log = false

    ## Path of the file that contains a list of trusted SSL CAs. If set, the following settings
    ## cert_path and key_path are also needed.
    # ca_path = "/path/to/ca.pem"
    ## Path of the file that contains X509 certificate in PEM format.
    # cert_path = "/path/to/tiflash-server.pem"
    ## Path of the file that contains X509 key in PEM format.
    # key_path = "/path/to/tiflash-server-key.pem"
```

### <code>tiflash-learner.toml</code>ファイルを設定する {#configure-the-code-tiflash-learner-toml-code-file}

`tiflash-learner.toml`のパラメータは基本的に TiKV のパラメータと同じです。TiFlash Proxyの設定については[TiKV 構成](/tikv-configuration-file.md)を参照してください。以下はよく使用されるパラメータのみです。次の点に注意してください。

-   TiKV と比較して、 TiFlash Proxy には`raftstore.snap-handle-pool-size`の追加パラメーターがあります。
-   キーが`engine`の`label`予約されており、手動で構成することはできません。

```toml
[log]
    ## The log level of TiFlash Proxy (available options: "trace", "debug", "info", "warn", "error"). The default value is "info". Introduced in v5.4.0.
    level = "info"

[log.file]
    ## The maximum number of log files to save. Introduced in v5.4.0.
    ## If this parameter is not set or set to the default value `0`, TiFlash Proxy saves all log files.
    ## If this parameter is set to a non-zero value, TiFlash Proxy retains at most the number of old log files specified by `max-backups`. For example, if you set it to `7`, TiFlash Proxy retains at most 7 old log files.
    max-backups = 0
    ## The maximum number of days that the log files are retained. Introduced in v5.4.0.
    ## If this parameter is not set or set to the default value `0`, TiFlash Proxy retains all log files.
    ## If this parameter is set to a non-zero value, TiFlash Proxy cleans up outdated log files after the number of days specified by `max-days`.
    max-days = 0

[raftstore]
    ## The allowable number of threads in the pool that flushes Raft data to storage.
    apply-pool-size = 4

    ## The allowable number of threads that process Raft, which is the size of the Raftstore thread pool.
    store-pool-size = 4

    ## The number of threads that handle snapshots.
    ## The default value is 2. If you set it to 0, the multi-thread optimization is disabled.
    ## A specific parameter of TiFlash Proxy, introduced in v4.0.0.
    snap-handle-pool-size = 2

[security]
    ## New in v5.0. This configuration item enables or disables log redaction. Value options: `true`, `false`, `"on"`, `"off"`, and `"marker"`. The `"on"`, `"off"`, and `"marker"` options are introduced in v8.3.0.
    ## If the configuration item is set to `false` or `"off"`, log redaction is disabled.
    ## If the configuration item is set to `true` or `"on"`, all user data in the log is replaced by `?`.
    ## If the configuration item is set to `"marker"`, all user data in the log is wrapped in `‹ ›`. If user data contains `‹` or `›`, `‹` is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.
    ## The default value is `false`.
    redact-info-log = false

[security.encryption]
    ## The encryption method for data files.
    ## Value options: "aes128-ctr", "aes192-ctr", "aes256-ctr", "sm4-ctr" (supported since v6.4.0), and "plaintext".
    ## Default value: `"plaintext"`, which means encryption is disabled by default. A value other than "plaintext" means that encryption is enabled, in which case the master key must be specified.
    data-encryption-method = "aes128-ctr"
    ## Specifies how often the data encryption key is rotated. Default value: `7d`.
    data-key-rotation-period = "168h" # 7 days

[security.encryption.master-key]
    ## Specifies the master key if encryption is enabled. To learn how to configure a master key, see Configure encryption: https://docs.pingcap.com/tidb/dev/encryption-at-rest#configure-encryption .

[security.encryption.previous-master-key]
    ## Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see  Configure encryption: https://docs.pingcap.com/tidb/dev/encryption-at-rest#configure-encryption .
```

### トポロジラベルによるレプリカのスケジュール {#schedule-replicas-by-topology-labels}

[利用可能なゾーンを設定する](/tiflash/create-tiflash-replicas.md#set-available-zones)参照。

### マルチディスク展開 {#multi-disk-deployment}

TiFlash は、マルチディスク展開をサポートしています。TiFlash ノードに複数のディスクがある場合は、次のセクションで説明するパラメータを設定することで、それらのディスクを最大限に活用できますTiUPに使用するTiFlashの設定テンプレートについては、 [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)参照してください。

#### TiDB バージョン v4.0.9 より前のマルチディスク展開 {#multi-disk-deployment-with-tidb-version-earlier-than-v4-0-9}

v4.0.9 より前の TiDB クラスターの場合、 TiFlash はstorageエンジンのメイン データを複数のディスクに保存することのみをサポートします`path` ( TiUPでは`data_dir` ) および`path_realtime_mode`構成を指定することで、複数のディスクにTiFlashノードを設定できます。

`path`に複数のデータstorageディレクトリがある場合は、それぞれをコンマで区切ります。たとえば、 `/nvme_ssd_a/data/tiflash,/sata_ssd_b/data/tiflash,/sata_ssd_c/data/tiflash`です。環境内に複数のディスクがある場合は、各ディレクトリを 1 つのディスクに対応させ、すべてのディスクのパフォーマンスを最大化するために、パフォーマンスが最も優れたディスクを先頭に配置することをお勧めします。

TiFlashノードに同様の I/O メトリックを持つディスクが複数ある場合は、 `path_realtime_mode`パラメータをデフォルト値のままにしておくことができます (または明示的に`false`に設定することもできます)。これは、データがすべてのstorageディレクトリ間で均等に分散されることを意味します。ただし、最新のデータは最初のディレクトリにのみ書き込まれるため、対応するディスクは他のディスクよりもビジー状態になります。

TiFlashノードに I/O メトリックが異なる複数のディスクがある場合は、 `path_realtime_mode`から`true`に設定し、最も優れた I/O メトリックを持つディスクを`path`の先頭に配置することをお勧めします。これは、最初のディレクトリには最新のデータのみが保存され、古いデータは他のディレクトリに均等に分散されることを意味します。この場合、最初のディレクトリの容量は、すべてのディレクトリの合計容量の 10% として計画する必要があることに注意してください。

#### TiDB v4.0.9 以降を使用したマルチディスク展開 {#multi-disk-deployment-with-tidb-v4-0-9-or-later}

v4.0.9 以降のバージョンの TiDB クラスターの場合、 TiFlash はstorageエンジンのメイン データと最新データを複数のディスクに保存することをサポートします。TiFlash ノードを複数のディスクに展開する場合は、ノードを最大限に活用するために、 `[storage]`セクションでstorageディレクトリを指定することをお勧めしますTiFlashより前の構成 ( `path`および`path_realtime_mode` ) も引き続きサポートされていることに注意してください。

TiFlashノードに類似した I/O メトリックを持つ複数のディスクがある場合は、リスト`storage.main.dir`で対応するディレクトリを指定し、 `storage.latest.dir`空のままにしておくことをお勧めします。TiFlashは、 I/O 負荷とデータをすべてのディレクトリに分散します。

TiFlashノードに I/O メトリックが異なる複数のディスクがある場合は、 `storage.latest.dir`リストでメトリックの高いディレクトリを指定し、 `storage.main.dir`リストでメトリックの低いディレクトリを指定することをお勧めします。たとえば、1 つの NVMe-SSD と 2 つの SATA-SSD の場合、 `storage.latest.dir` `["/nvme_ssd_a/data/tiflash"]`に、 `storage.main.dir`を`["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`に設定できます。TiFlashは、 I/O プレッシャーとデータをそれぞれこの 2 つのディレクトリ リストに分散します。この場合、容量`storage.latest.dir`は、計画された総容量の 10% として計画する必要があることに注意してください。

> **警告：**
>
> `[storage]`構成は、TiUP v1.2.5 以降でサポートされています。TiDB クラスターのバージョンが v4.0.9 以降の場合は、 TiUPバージョンが v1.2.5 以降であることを確認してください。そうでない場合、 `[storage]`で定義されているデータ ディレクトリはTiUPによって管理されません。
