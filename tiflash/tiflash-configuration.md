---
title: Configure TiFlash
summary: Learn how to configure TiFlash.
---

# TiFlashを構成する {#configure-tiflash}

このドキュメントでは、 TiFlashの展開と使用に関連する構成パラメータを紹介します。

## PD スケジューリングパラメータ {#pd-scheduling-parameters}

[PD-CTL](/pd-control.md)を使用して PD スケジュール パラメータを調整できます。 tiup を使用してクラスターをデプロイおよび管理する場合は、 `pd-ctl -u <pd_ip:pd_port>`を`tiup ctl:v<CLUSTER_VERSION> pd`に置き換えることができることに注意してください。

-   [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit) : レプリカ関連のオペレーターが生成される速度を決定します。このパラメーターは、ノードのオフライン化やレプリカの追加などの操作に影響します。

    > **注記：**
    >
    > このパラメータの値は`region-schedule-limit`より小さい必要があります。そうしないと、TiKV ノード間の通常のリージョンスケジューリングが影響を受けます。

-   `store-balance-rate` : 各 TiKV/ TiFlashストアのリージョンがスケジュールされるレートを制限します。このパラメーターは、ストアがクラスターに新しく参加した場合にのみ有効であることに注意してください。既存のストアの設定を変更する場合は、次のコマンドを使用します。

    > **注記：**
    >
    > v4.0.2 以降、 `store-balance-rate`パラメータは非推奨となり、 `store limit`コマンドに変更が加えられました。詳細は[店舗限定](/configure-store-limit.md)を参照してください。

    -   `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>`コマンドを実行して、指定したストアのスケジューリング レートを設定します。 ( `store_id`を取得するには、 `pd-ctl -u <pd_ip:pd_port> store`コマンドを実行します。
    -   指定したストアのリージョンのスケジュール レートを設定しない場合、このストアは`store-balance-rate`の設定を継承します。
    -   `pd-ctl -u <pd_ip:pd_port> store limit`コマンドを実行すると、 `store-balance-rate`の現在の設定値を表示できます。

-   [`replication.location-labels`](/pd-configuration-file.md#location-labels) : TiKV インスタンスのトポロジー関係を示します。キーの順序は、さまざまなラベルの階層関係を示します。 TiFlashが有効な場合は、 [`pd-ctl config placement-rules`](/pd-control.md#config-show--set-option-value--placement-rules)を使用してデフォルト値を設定する必要があります。詳細は[地理分散展開トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

## TiFlash設定パラメータ {#tiflash-configuration-parameters}

このセクションでは、 TiFlashの設定パラメータを紹介します。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

### <code>tiflash.toml</code>ファイルを構成する {#configure-the-code-tiflash-toml-code-file}

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
    ## * format_version = 4, the default format for v6.2.0 and later versions, which reduces write amplification and background task resource consumption
    # format_version = 4

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

    ## The following configuration items only take effect for the TiFlash disaggregated storage and compute architecture mode. For details, see documentation at https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3.
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
    tidb_status_addr = TiDB status port and address. # Multiple addresses are separated with commas.
    service_addr = The listening address of TiFlash Raft services and coprocessor services.

    ## The following configuration item only takes effect for the TiFlash disaggregated storage and compute architecture mode. For details, see documentation at https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3.
    # disaggregated_mode = tiflash_write # The supported mode is `tiflash_write` or `tiflash_compute.

## Multiple TiFlash nodes elect a master to add or delete placement rules to PD,
## and the configurations in flash.flash_cluster control this process.
[flash.flash_cluster]
    refresh_interval = Master regularly refreshes the valid period.
    update_rule_interval = Master regularly gets the status of TiFlash replicas and interacts with PD.
    master_ttl = The valid period of the elected master.
    cluster_manager_path = The absolute path of the pd buddy directory.
    log = The pd buddy log path.

[flash.proxy]
    addr = The listening address of proxy. If it is left empty, 127.0.0.1:20170 is used by default.
    advertise-addr = The external access address of addr. If it is left empty, "addr" is used by default.
    data-dir = The data storage path of proxy.
    config = The configuration file path of proxy.
    log-file = The log path of proxy.
    log-level = The log level of proxy. "info" is used by default.
    status-addr = The listening address from which the proxy pulls metrics | status information. If it is left empty, 127.0.0.1:20292 is used by default.
    advertise-status-addr = The external access address of status-addr. If it is left empty, "status-addr" is used by default.

[logger]
    ## log level (available options: "trace", "debug", "info", "warn", "error"). The default value is "debug".
    level = "debug"
    log = TiFlash log path
    errorlog = TiFlash error log path
    ## Size of a single log file. The default value is "100M".
    size = "100M"
    ## Maximum number of log files to save. The default value is 10.
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

## Security settings take effect starting from v4.0.5.
[security]
    ## New in v5.0. This configuration item enables or disables log redaction. If the configuration value
    ## is set to true, all user data in the log will be replaced by ?.
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

### <code>tiflash-learner.toml</code>ファイルを構成する {#configure-the-code-tiflash-learner-toml-code-file}

```toml
[server]
    engine-addr = The external access address of the TiFlash coprocessor service.
[raftstore]
    ## The allowable number of threads in the pool that flushes Raft data to storage.
    apply-pool-size = 4

    ## The allowable number of threads that process Raft, which is the size of the Raftstore thread pool.
    store-pool-size = 4

    ## The number of threads that handle snapshots.
    ## The default number is 2.
    ## If you set it to 0, the multi-thread optimization is disabled.
    snap-handle-pool-size = 2

    ## The shortest interval at which Raft store persists WAL.
    ## You can properly increase the latency to reduce IOPS usage.
    ## The default value is "4ms".
    ## If you set it to 0ms, the optimization is disabled.
    store-batch-retry-recv-timeout = "4ms"
[security]
    ## New in v5.0. This configuration item enables or disables log redaction.
    ## If the configuration value is set to true,
    ## all user data in the log will be replaced by ?. The default value is false.
    redact-info-log = false

[security.encryption]
    ## The encryption method for data files.
    ## Value options: "aes128-ctr", "aes192-ctr", "aes256-ctr", "sm4-ctr" (supported since v6.4.0), and "plaintext".
    ## Default value: `"plaintext"`, which means encryption is disabled by default. A value other than "plaintext" means that encryption is enabled, in which case the master key must be specified.
    data-encryption-method = "aes128-ctr"
    ## Specifies how often the data encryption key is rotated. Default value: `7d`.
    data-key-rotation-period = "168h" # 7 days

[security.encryption.master-key]
    ## Specifies the master key if encryption is enabled. To learn how to configure a master key, see Configure encryption: https://docs.pingcap.com/tidb/v7.1/encryption-at-rest#configure-encryption .

[security.encryption.previous-master-key]
    ## Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see  Configure encryption: https://docs.pingcap.com/tidb/v7.1/encryption-at-rest#configure-encryption .
```

上記以外のパラメータはTiKVと同様です。キーが`engine`の`label`予約されており、手動で構成できないことに注意してください。

### トポロジ ラベルごとにレプリカをスケジュールする {#schedule-replicas-by-topology-labels}

[利用可能なゾーンを設定する](/tiflash/create-tiflash-replicas.md#set-available-zones)を参照してください。

### マルチディスク展開 {#multi-disk-deployment}

TiFlash はマルチディスク展開をサポートしています。 TiFlashノードに複数のディスクがある場合は、次のセクションで説明するパラメータを構成することで、それらのディスクを最大限に活用できます。 TiUPに使用される TiFlash の構成テンプレートについては、 [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)を参照してください。

#### v4.0.9 より前の TiDB バージョンを使用したマルチディスク展開 {#multi-disk-deployment-with-tidb-version-earlier-than-v4-0-9}

v4.0.9 より前の TiDB クラスターの場合、 TiFlash はstorageエンジンのメイン データの複数のディスクへの保存のみをサポートします。 `path` ( TiUPでは`data_dir` ) および`path_realtime_mode`構成を指定することにより、複数のディスク上にTiFlashノードをセットアップできます。

`path`に複数のデータstorageディレクトリがある場合は、それぞれをカンマで区切ります。たとえば、 `/nvme_ssd_a/data/tiflash,/sata_ssd_b/data/tiflash,/sata_ssd_c/data/tiflash` 。環境内に複数のディスクがある場合は、各ディレクトリを 1 つのディスクに対応させ、すべてのディスクのパフォーマンスを最大化するために、最高のパフォーマンスを持つディスクを前面に配置することをお勧めします。

TiFlashノード上に同様の I/O メトリクスを持つディスクが複数ある場合は、 `path_realtime_mode`パラメータをデフォルト値のままにすることができます (または明示的に`false`に設定することもできます)。これは、データがすべてのstorageディレクトリに均等に分散されることを意味します。ただし、最新のデータは最初のディレクトリにのみ書き込まれるため、対応するディスクは他のディスクよりもビジーになります。

TiFlashノード上に異なる I/O メトリクスを持つ複数のディスクがある場合は、 `path_realtime_mode` ～ `true`を設定し、最良の I/O メトリクスを持つディスクを`path`の前に置くことをお勧めします。これは、最初のディレクトリには最新のデータのみが保存され、古いデータは他のディレクトリに均等に分散されることを意味します。この場合、最初のディレクトリの容量は、すべてのディレクトリの合計容量の 10% として計画する必要があることに注意してください。

#### TiDB v4.0.9 以降を使用したマルチディスク展開 {#multi-disk-deployment-with-tidb-v4-0-9-or-later}

v4.0.9 以降のバージョンの TiDB クラスターの場合、 TiFlash は、storageエンジンのメイン データと最新データの複数のディスクへの保存をサポートします。 TiFlashノードを複数のディスクにデプロイする場合は、ノードを最大限に活用するために`[storage]`セクションでstorageディレクトリを指定することをお勧めします。 v4.0.9 より前の構成 ( `path`および`path_realtime_mode` ) は引き続きサポートされることに注意してください。

TiFlashノード上に同様の I/O メトリクスを持つ複数のディスクがある場合は、 `storage.main.dir`リストに対応するディレクトリを指定し、 `storage.latest.dir`空のままにすることをお勧めします。 TiFlash は、 I/O プレッシャーとデータをすべてのディレクトリに分散します。

TiFlashノード上に異なる I/O メトリクスを持つ複数のディスクがある場合は、 `storage.latest.dir`リストでより高いメトリクスを持つディレクトリを指定し、 `storage.main.dir`のリストでより低いメトリクスを持つディレクトリを指定することをお勧めします。たとえば、1 つの NVMe-SSD と 2 つの SATA-SSD の場合、 `storage.latest.dir` ～ `["/nvme_ssd_a/data/tiflash"]`および`storage.main.dir` ～ `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`を設定できます。 TiFlash は、 I/O プレッシャーとデータをこれら 2 つのディレクトリ リストにそれぞれ分散します。この場合、 `storage.latest.dir`という容量は、計画された総容量の 10% として計画される必要があることに注意してください。

> **警告：**
>
> `[storage]`構成は、 TiUP v1.2.5 以降でサポートされています。 TiDB クラスターのバージョンが v4.0.9 以降の場合は、 TiUP のバージョンが v1.2.5 以降であることを確認してください。そうしないと、 `[storage]`で定義したデータ ディレクトリがTiUPによって管理されなくなります。
