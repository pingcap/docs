---
title: Configure TiFlash
summary: Learn how to configure TiFlash.
---

# Configure TiFlash

This document introduces the configuration parameters related to the deployment and use of TiFlash.

## PD scheduling parameters

You can adjust the PD scheduling parameters using [pd-ctl](/pd-control.md). Note that you can use `tiup ctl:v<CLUSTER_VERSION> pd` to replace `pd-ctl -u <pd_ip:pd_port>` when using tiup to deploy and manage your cluster.

- [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit): determines the rate at which the replica-related operator is generated. The parameter affects operations such as making nodes offline and add replicas.

  > **Note:**
  >
  > The value of this parameter should be less than that of `region-schedule-limit`. Otherwise, the normal Region scheduling among TiKV nodes is affected.

- `store-balance-rate`: limits the rate at which Regions of each TiKV/TiFlash store are scheduled. Note that this parameter takes effect only when the stores have newly joined the cluster. If you want to change the setting for existing stores, use the following command.

  > **Note:**
  >
  > Since v4.0.2, the `store-balance-rate` parameter has been deprecated and changes have been made to the `store limit` command. See [store-limit](/configure-store-limit.md) for details.

    - Execute the `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` command to set the scheduling rate of a specified store. To get `store_id`, you can execute the `pd-ctl -u <pd_ip:pd_port> store` command.
    - If you do not set the scheduling rate for Regions of a specified store, this store inherits the setting of `store-balance-rate`.
    - You can execute the `pd-ctl -u <pd_ip:pd_port> store limit` command to view the current setting value of `store-balance-rate`.

- [`replication.location-labels`](/pd-configuration-file.md#location-labels): indicates the topological relationship of TiKV instances. The order of the keys indicates the layering relationship of different labels. If TiFlash is enabled, you need to use [`pd-ctl config placement-rules`](/pd-control.md#config-show--set-option-value--placement-rules) to set the default value. For details, see [geo-distributed-deployment-topology](/geo-distributed-deployment-topology.md).

## TiFlash configuration parameters

This section introduces the configuration parameters of TiFlash.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration).

### Configure the `tiflash.toml` file

#### `listen_host`

- The listening host for supporting services such as TPC/HTTP.
- It is recommended to configure it as `"0.0.0.0"`, which means listening on all IP addresses of this machine.

#### `tcp_port`

- The TiFlash TCP service port. This port is used for internal testing and is set to 9000 by default.
- Before TiFlash v7.1.0, this port is enabled by default with a security risk. To enhance security, it is recommended to apply access control on this port to only allow access from whitelisted IP addresses. Starting from TiFlash v7.1.0, you can avoid the security risk by commenting out the configuration of this port. When the TiFlash configuration file does not specify this port, it will be disabled. 
- It is **NOT** recommended to configure this port in any TiFlash deployment. (Note: Starting from TiFlash v7.1.0, TiFlash deployed by TiUP >= v1.12.5 or TiDB Operator >= v1.5.0 disables the port by default and is more secure.)
- Default value: `9000`

#### `mark_cache_size`

- The cache size limit of the metadata of a data block. Generally, you do not need to change this value.
- Default value: `1073741824`

#### `minmax_index_cache_size`

- The cache size limit of the min-max index of a data block. Generally, you do not need to change this value.
- Default value: `1073741824`

#### `delta_index_cache_size`

- The cache size limit of the DeltaIndex.
- Default value: `0`, which means no limit.

#### `path`

- The storage path of TiFlash data. If there are multiple directories, separate each directory with a comma.
- Starting from TiDB v4.0.9, `path` and [`path_realtime_mode`](#path_realtime_mode) are deprecated. Use the configurations in the [`storage`](#storage-new-in-v409) section to get better performance in the multi-disk deployment scenarios.
- Starting from TiDB v5.2.0, if you need to use the [`storage.io_rate_limit`](#storageio_rate_limit-new-in-v520) configuration, you need to set the storage path of TiFlash data to [`storage.main.dir`](#dir) at the same time.
- When the `storage` configurations exist, both `path` and [`path_realtime_mode`](#path_realtime_mode) configurations are ignored.

<!-- Example: `"/tidb-data/tiflash-9000"` or `"/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"` -->

#### `path_realtime_mode`

- If you set it to `true` and multiple directories are set in the `path`, the latest data is stored in the first directory and older data is stored in the rest directories.
- Starting from TiDB v4.0.9, [`path`](#path) and `path_realtime_mode` are deprecated. Use the configurations in the [`storage`](#storage-new-in-v409) section to get better performance in the multi-disk deployment scenarios.
- When the `storage` configurations exist, both [`path`](#path) and `path_realtime_mode` configurations are ignored.
- Default value: `false`

#### `tmp_path`

- The path in which the TiFlash temporary files are stored.
- By default, it is the first directory in [`path`](#path) or in [`storage.latest.dir`](#dir-1) appended with `"/tmp"`.

<!-- Example: `"/tidb-data/tiflash-9000/tmp"` -->

#### storage <span class="version-mark">New in v4.0.9</span>

Configure storage path related settings.

##### `format_version`

- The DTFile format.
- Default value: `7`
- Value options: `2`, `3`, `4`, `5`, `6`, `7`
    - `format_version = 2`: the default format for versions < v6.0.0.
    - `format_version = 3`: the default format for v6.0.0 and v6.1.x, which provides more data validation features.
    - `format_version = 4`: the default format for versions from v6.2.0 to v7.3.0, which reduces write amplification and background task resource consumption.
    - `format_version = 5`: introduced in v7.3.0, the default format for versions from v7.4.0 to v8.3.0, which reduces the number of physical files by merging smaller files.
    - `format_version = 6`: introduced in v8.4.0, which partially supports the building and storage of vector indexes.
    - `format_version = 7`: introduced in v8.4.0, the default format for v8.4.0 and later versions, which supports the build and storage of vector indexes.

#### storage.main

##### `dir`

- The list of directories to store the main data. For example: `[ "/tidb-data/tiflash-9000" ]` or `[ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]`.
- More than 90% of the total data is stored in the directory list.

##### `capacity`

- The maximum storage capacity of each directory in [`storage.main.dir`](#dir). For example `[10737418240, 10737418240]`.
- If it is not set, or is set to multiple `0`, the actual disk (the disk where the directory is located) capacity is used.
- Unit: Byte. Note that human-readable numbers such as `"10GB"` are not supported yet.
- The size of the `capacity` list should be the same with the [`storage.main.dir`](#dir) size.

#### storage.latest

##### `dir`

- The list of directories to store the latest data. About 10% of the total data is stored in the directory list. The directories (or directory) listed here require higher IOPS metrics than those [`storage.main.dir`](#dir).
- If it is not set (by default), the values of [`storage.main.dir`](#dir) are used.

<!-- Example: `[]` -->

##### `capacity`

- The maximum storage capacity of each directory in [`storage.latest.dir`](#dir-1). If it is not set, or is set to multiple `0`, the actual disk (the disk where the directory is located) capacity is used.

<!-- Example: `[10737418240, 10737418240]` -->

#### storage.io_rate_limit <span class="version-mark">New in v5.2.0</span>

Configure the I/O traffic limit settings.

##### `max_bytes_per_sec`

- The total I/O bandwidth for disk reads and writes. This configuration item determines whether to limit the I/O traffic, which is disabled by default. This traffic limit in TiFlash is suitable for cloud storage that has the disk bandwidth of a small and specific size.
- Default value: `0`, which means the I/O traffic is not limited by default.
- Unit: Byte

##### `max_read_bytes_per_sec`

- The total I/O bandwidth for disk reads.
- `max_read_bytes_per_sec` and `max_write_bytes_per_sec` configuration items limit I/O bandwidth for disk reads and writes separately. You can use them for cloud storage that calculates the limit of I/O bandwidth for disk reads and writes separately, such as the Persistent Disk provided by Google Cloud.
- When the value of `max_bytes_per_sec` is not `0`, [`max_bytes_per_sec`](#max_bytes_per_sec) is prioritized.
- Default value: `0`

##### `max_write_bytes_per_sec`

- The total I/O bandwidth for disk writes.
- `max_read_bytes_per_sec` and `max_write_bytes_per_sec` configuration items limit I/O bandwidth for disk reads and writes separately. You can use them for cloud storage that calculates the limit of I/O bandwidth for disk reads and writes separately, such as the Persistent Disk provided by Google Cloud.
- When the value of `max_bytes_per_sec` is not `0`, [`max_bytes_per_sec`](#max_bytes_per_sec) is prioritized.
- Default value: `0`

##### `foreground_write_weight`

<!-- The following  default configurations indicate that each type of traffic gets a weight of 25% (25 / (25 + 25 + 25 + 25) = 25%) -->

- TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads. `foreground_write_weight` controls the bandwidth weights assigned to foreground write I/O traffic type. Generally, you do not need to adjust these parameters.
- When the I/O traffic limit is initialized, TiFlash allocates bandwidth for these four types of requests according to the ratio of `foreground_write_weight`, [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight), [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight), and [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight).
- If the weight is configured to `0`, the corresponding I/O traffic is not limited.
- Default value: `25`, representing an allocation of 25% of the bandwidth.

##### `background_write_weight`

- TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads. `background_write_weight` controls the bandwidth weights assigned to background write I/O traffic type. Generally, you do not need to adjust these parameters.
- When the I/O traffic limit is initialized, TiFlash allocates bandwidth for these four types of requests according to the ratio of [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight), `background_write_weight`, [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight), and [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight).
- If the weight is configured to `0`, the corresponding I/O traffic is not limited.
- Default value: `25`, representing an allocation of 25% of the bandwidth.

##### `foreground_read_weight`

- TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads. `foreground_read_weight` controls the bandwidth weights assigned to foreground read I/O traffic type. Generally, you do not need to adjust these parameters.
- When the I/O traffic limit is initialized, TiFlash allocates bandwidth for these four types of requests according to the ratio of [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight), [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight), `foreground_read_weight`, and [`background_read_weight`](/tiflash/tiflash-configuration.md#background_read_weight).
- If the weight is configured to `0`, the corresponding I/O traffic is not limited.
- Default value: `25`, representing an allocation of 25% of the bandwidth.

##### `background_read_weight`

- TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads. `background_read_weight` controls the bandwidth weights assigned to background read I/O traffic type. Generally, you do not need to adjust these parameters.
- When the I/O traffic limit is initialized, TiFlash allocates bandwidth for these four types of requests according to the ratio of [`foreground_write_weight`](/tiflash/tiflash-configuration.md#foreground_write_weight), [`background_write_weight`](/tiflash/tiflash-configuration.md#background_write_weight), [`foreground_read_weight`](/tiflash/tiflash-configuration.md#foreground_read_weight), and `background_read_weight`.
- If the weight is configured to `0`, the corresponding I/O traffic is not limited.
- Default value: `25`, representing an allocation of 25% of the bandwidth.

##### `auto_tune_sec`

- TiFlash supports automatically tuning the traffic limit for different I/O types according to the current I/O load. Sometimes, the tuned bandwidth might exceed the weight ratio set above.
- `auto_tune_sec` indicates the interval of automatic tuning. If the value of auto_tune_sec is `0`, the automatic tuning is disabled.
- Default value: `5`
- Unit: Seconds

#### storage.s3

The following configuration items only take effect for the TiFlash disaggregated storage and compute architecture mode. For details, see [TiFlash Disaggregated Storage and Compute Architecture and S3 Support](/tiflash/tiflash-disaggregated-and-s3.md).

##### `endpoint`

- The S3 endpoint address. For example: `http://s3.{region}.amazonaws.com`.

##### `bucket`

- TiFlash stores all data in this bucket.

##### `root`

- The root directory where data is stored in the S3 bucket. For example: `/cluster1_data`.

##### `access_key_id`

- The ACCESS_KEY_ID used to access S3.

##### `secret_access_key`

- The SECRET_ACCESS_KEY used to access S3.

#### storage.remote.cache

##### `dir`

- The local data cache directory of the Compute Node in the disaggregated storage and compute architecture.

<!-- Example: `"/data1/tiflash/cache"` -->

##### `capacity`

- Example: `858993459200` (800 GiB)

#### flash

##### `service_addr`

- The listening address of TiFlash coprocessor services.

<!-- Example: `"0.0.0.0:3930"` -->

##### `compact_log_min_gap` <span class="version-mark">New in v7.4.0</span>

- When the gap between the `applied_index` advanced by the current Raft state machine and the `applied_index` at the last disk spilling exceeds `compact_log_min_gap`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk.
- Increasing this gap might reduce the disk spilling frequency of TiFlash, thus reducing read latency in random write scenarios, but it might also increase memory overhead. Decreasing this gap might increase the disk spilling frequency of TiFlash, thus alleviating memory pressure in TiFlash. However, at this stage, the disk spilling frequency of TiFlash will not be higher than that of TiKV, even if this gap is set to `0`.
- It is recommended to keep the default value.
- Default value: `200`

##### `compact_log_min_rows` <span class="version-mark">New in v5.0</span>

- When the number or the size of rows in the Regions cached by TiFlash exceeds either `compact_log_min_rows` or `compact_log_min_bytes`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk.
- It is recommended to keep the default value.
- Default value: `40960`

##### `compact_log_min_bytes` <span class="version-mark">New in v5.0</span>

- When the number or the size of rows in the Regions cached by TiFlash exceeds either `compact_log_min_rows` or `compact_log_min_bytes`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk.
- It is recommended to keep the default value.
- Default value: `33554432`

##### `disaggregated_mode`

- This configuration item only takes effect for the TiFlash disaggregated storage and compute architecture mode. For details, see [TiFlash Disaggregated Storage and Compute Architecture and S3 Support](/tiflash/tiflash-disaggregated-and-s3.md).
- Value options: `"tiflash_write"`, `"tiflash_compute"`

#### flash.proxy

##### `addr`

- The listening address of proxy.
- Default value: `"127.0.0.1:20170"`

##### `advertise-addr`

- The external access address of `addr`. If it is left empty, `addr` is used by default.
- You should guarantee that other nodes can access through `advertise-addr` when you deploy the cluster on multiple nodes.

##### `status-addr`

- The listening address from which the proxy pulls metrics or status information.
- Default value: `"127.0.0.1:20292"`

##### `advertise-status-addr`

- The external access address of status-addr. If it is left empty, the value of `status-addr` is used by default.
- You should guarantee that other nodes can access it through `advertise-status-addr` when you deploy the cluster on multiple nodes.

##### `engine-addr`

- The external access address of the TiFlash coprocessor service.

<!-- Example: `"10.0.1.20:3930"` -->

##### `data-dir`

- The data storage path of proxy.

<!-- Example: `"/tidb-data/tiflash-9000/flash"` -->

##### `config`

- The configuration file path of proxy.

<!-- Example: `"/tidb-deploy/tiflash-9000/conf/tiflash-learner.toml"` -->

##### `log-file`

- The log path of proxy.

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash_tikv.log"` -->

#### logger

Note that the following parameters only take effect in TiFlash logs and TiFlash error logs. If you need to configure log parameters of TiFlash Proxy, specify them in [`tiflash-learner.toml`](#configure-the-tiflash-learnertoml-file).

##### `level`

- The log level.
- Default value: `"info"`
- Value options: `"trace"`, `"debug"`, `"info"`, `"warn"`, `"error"`

##### `log`

- The log of TiFlash.

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash.log"` -->

##### `errorlog`

- The error log of TiFlash. The `"warn"` and `"error"` level logs are also output to this log file.

<!-- Example: `"/tidb-deploy/tiflash-9000/log/tiflash_error.log"` -->

##### `size`

- The size of a single log file.
- Default value: `"100M"`

##### `count`

- The maximum number of log files to save. For TiFlash logs and TiFlash error logs, the maximum number of log files to save is `count` respectively.
- Default value: `10`

#### raft

##### `pd_addr`

- The PD service address.
- Multiple addresses are separated with commas. For example, `"10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"`.

#### status

##### `metrics_port`

- The port through which Prometheus pulls metrics information.
- Default value: `8234`

#### profiles.default

##### `dt_enable_logical_split`

- Determines whether the segment of DeltaTree Storage Engine uses logical split. Using the logical split can reduce the write amplification. However, these are at the cost of disk space waste.
- It is strongly recommended to keep the default value `false` and not to change it to `true` in v6.2.0 and later versions. For details, see known issue [#5576](https://github.com/pingcap/tiflash/issues/5576).
- Default value: `false`

##### `max_threads`

- `max_threads` indicates the internal thread concurrency when TiFlash executes an MPP task. When it is set to `0`, TiFlash uses the number of logical CPU cores as the execution concurrency.
- This parameter only takes effect when the system variable [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) is set to `-1`.
- Default value: `0`

##### `max_memory_usage`

- The memory usage limit for the generated intermediate data in a single query.
- When the value is an integer, the unit is byte. For example, `34359738368` means 32 GiB of memory limit.
- When the value is a floating-point number in the range of `[0.0, 1.0)`, it means the ratio of the allowed memory usage to the total memory of the node. For example, `0.8` means 80% of the total memory, and `0.0` means no limit.
- When a query attempts to consume memory that exceeds this limit, the query is terminated and an error is reported.
- Default value: `0`, which means no limit.

##### `max_memory_usage_for_all_queries`

- The memory usage limit for the generated intermediate data in all queries.
- When the value is an integer, the unit is byte. For example, `34359738368` means 32 GiB of memory limit, and `0` means no limit.
- Starting from v6.6.0, you can set the value to a floating-point number in the range of `[0.0, 1.0)`. This number represents the ratio of the allowed memory usage to the total node memory. For example, `0.8` means 80% of the total memory, and `0.0` means no limit.
- When the queries attempt to consume memory that exceeds this limit, the queries are terminated and an error is reported.
- Default value: `0.8`, which means 80% of the total memory. Before v6.6.0, the default value is `0`, which means no limit.

##### `cop_pool_size` <span class="version-mark">New in v5.0</span>

- Specifies the maximum number of cop requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to `0` or not set, the default value is used, which is twice the number of physical cores.
- Default value: twice the number of physical cores

##### `cop_pool_handle_limit` <span class="version-mark">New in v5.0</span>

- Specifies the maximum number of cop requests that TiFlash Coprocessor handles at the same time, including the requests being executed and the requests waiting in the queue. If the number of requests exceeds the specified value, the error `TiFlash Server is Busy` is returned.
- `-1` indicates no limit; `0` indicates using the default value, which is `10 * cop_pool_size`.

##### `cop_pool_max_queued_seconds` <span class="version-mark">New in v5.0</span>

- Specifies the maximum time that a cop request can queue in TiFlash. If a cop request waits in the queue for a time longer than the value specified by this configuration, the error `TiFlash Server is Busy` is returned.
- A value less than or equal to `0` indicates no limit.
- Default value: `15`

##### `batch_cop_pool_size` <span class="version-mark">New in v5.0</span>

- Specifies the maximum number of batch requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to `0` or not set, the default value is used, which is twice the number of physical cores.
- Default value: twice the number of physical cores

##### `manual_compact_pool_size` <span class="version-mark">New in v6.1</span>

- Specifies the number of requests that TiFlash can concurrently process when it receives `ALTER TABLE ... COMPACT` from TiDB.
- If the value is set to `0`, the default value `1` prevails.
- Default value: `1`

##### `enable_elastic_threadpool` <span class="version-mark">New in v5.4.0</span>

- Controls whether to enable the elastic thread pool feature, which significantly improves CPU utilization in high concurrency scenarios of TiFlash.
- Default value: `true`

##### `dt_compression_method`

- Compression algorithm of the TiFlash storage engine.
- Default value: `LZ4`
- Value options: `LZ4`, `zstd`, `LZ4HC`. The value is case-insensitive.

##### `dt_compression_level`

- Compression level of the TiFlash storage engine.
- It is recommended that you set this value to `1` if `dt_compression_method` is `LZ4`.
- It is recommended that you set this value to `-1` (smaller compression rate, but better read performance) or `1` if `dt_compression_method` is `zstd`.
- It is recommended that you set this value to `9` if `dt_compression_method` is `LZ4HC`.
- Default value: `1`

##### `dt_page_gc_threshold` <span class="version-mark">New in v6.2.0</span>

- Specifies the minimum ratio of valid data in a PageStorage data file. When the ratio of valid data in a PageStorage data file is less than the value of this configuration, GC is triggered to compact data in the file.
- Default value: `0.5`

##### `max_bytes_before_external_group_by` <span class="version-mark">New in v7.0.0</span>

- Specifies the maximum memory available for the Hash Aggregation operator with the `GROUP BY` key before a disk spill is triggered. When the memory usage exceeds the threshold, Hash Aggregation reduces memory usage by [spilling to disk](/tiflash/tiflash-spill-disk.md).
- Default value: `0`, which means that the memory usage is unlimited and spill to disk is never used for Hash Aggregation.

##### `max_bytes_before_external_sort` <span class="version-mark">New in v7.0.0</span>

- Specifies the maximum memory available for the sort or topN operator before a disk spill is triggered. When the memory usage exceeds the threshold, the sort or topN operator reduces memory usage by [spilling to disk](/tiflash/tiflash-spill-disk.md).
- Default value: `0`, which means that the memory usage is unlimited and spill to disk is never used for sort or topN.

##### `max_bytes_before_external_join` <span class="version-mark">New in v7.0.0</span>

- Specifies the maximum memory available for the Hash Join operator with equi-join conditions before a disk spill is triggered. When the memory usage exceeds the threshold, HashJoin reduces memory usage by [spilling to disk](/tiflash/tiflash-spill-disk.md).
- Default value: `0`, which means that the memory usage is unlimited and spill to disk is never used for Hash Join with equi-join conditions.

##### `enable_resource_control` <span class="version-mark">New in v7.4.0</span>

- Controls whether to enable the TiFlash resource control feature. When it is set to `true`, TiFlash uses the [pipeline execution model](/tiflash/tiflash-pipeline-model.md).

##### `task_scheduler_thread_soft_limit` <span class="version-mark">New in v6.0.0</span>

- This item is used for the MinTSO scheduler. It specifies the maximum number of threads that one resource group can use. For more information, see [TiFlash MinTSO Scheduler](/tiflash/tiflash-mintso-scheduler.md).
- Default value: `5000`

##### `task_scheduler_thread_hard_limit` <span class="version-mark">New in v6.0.0</span>

- This item is used for the MinTSO scheduler. It specifies the maximum number of threads in the global scope. For more information, see [TiFlash MinTSO Scheduler](/tiflash/tiflash-mintso-scheduler.md).
- Default value: `10000`

##### `task_scheduler_active_set_soft_limit` <span class="version-mark">New in v6.4.0</span>

- This item is used for the MinTSO scheduler. It specifies the maximum number of queries that can run simultaneously in a TiFlash instance. For more information, see [TiFlash MinTSO Scheduler](/tiflash/tiflash-mintso-scheduler.md).
- Default value: Before v7.4.0, the default value is `vcpu * 0.25`, which means a quarter of the number of vCPUs. Starting from v7.4.0, the default value is `vcpu * 2`, which means twice the number of vCPUs.

#### security <span class="version-mark">New in v4.0.5</span>

Configure security related settings.

##### `redact_info_log` <span class="version-mark">New in v5.0</span>

- Controls whether to enable log redaction.
- Default value: `false`
- Value options: `true`, `false`, `"on"`, `"off"`, and `"marker"`. The `"on"`, `"off"`, and `"marker"` options are introduced in v8.2.0.
- If the configuration item is set to `false` or `"off"`, log redaction is disabled.
- If the configuration item is set to `true` or `"on"`, all user data in the log is replaced by `?`.
- If the configuration item is set to `"marker"`, all user data in the log is wrapped in `‹ ›`. If user data contains `‹` or `›`, `‹` is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.
- Note that you also need to set `security.redact-info-log` for tiflash-learner's logging in [`tiflash-learner.toml`](#configure-the-tiflash-learnertoml-file).

##### `ca_path`

- Path of the file that contains a list of trusted SSL CAs. If set, [`cert_path`](#cert_path) and [`key_path`](#key_path) are also needed.

<!-- Example: `"/path/to/ca.pem"` -->

##### `cert_path`

- Path of the file that contains X509 certificate in PEM format.

<!-- Example: `"/path/to/tiflash-server.pem"` -->

##### `key_path`

- Path of the file that contains X509 key in PEM format.

<!-- Example: `"/path/to/tiflash-server-key.pem"` -->

### Configure the `tiflash-learner.toml` file

The parameters in `tiflash-learner.toml` are basically the same as those in TiKV. You can refer to [TiKV configuration](/tikv-configuration-file.md) for TiFlash Proxy configuration. The following are only commonly used parameters. Note that:

- Compared with TiKV, TiFlash Proxy has an extra [`raftstore.snap-handle-pool-size`](#snap-handle-pool-size-new-in-v400) parameter.
- The `label` whose key is `engine` is reserved and cannot be configured manually.

#### log

##### `level` <span class="version-mark">New in v5.4.0</span>

- The log level of TiFlash Proxy.
- Default value: `"info"`
- Value options: `"trace"`, `"debug"`, `"info"`, `"warn"`, `"error"`

#### log.file

##### `max-backups` <span class="version-mark">New in v5.4.0</span>

- The maximum number of log files to save.
- If this parameter is not set or set to the default value `0`, TiFlash Proxy saves all log files.
- If this parameter is set to a non-zero value, TiFlash Proxy retains at most the number of old log files specified by `max-backups`. For example, if you set it to `7`, TiFlash Proxy retains at most 7 old log files.
- Default value: `0`

##### `max-days` <span class="version-mark">New in v5.4.0</span>

- The maximum number of days that the log files are retained.
- If this parameter is not set or set to the default value `0`, TiFlash Proxy retains all log files.
- If this parameter is set to a non-zero value, TiFlash Proxy cleans up outdated log files after the number of days specified by `max-days`.
- Default value: `0`

#### raftstore

##### `apply-pool-size`

- The allowable number of threads in the pool that flushes Raft data to storage.

<!-- Example: `4` -->

##### `store-pool-size`

- The allowable number of threads that process Raft, which is the size of the Raftstore thread pool.

<!-- Example: `4` -->

##### `snap-handle-pool-size` <span class="version-mark">New in v4.0.0</span>

- The number of threads that handle snapshots. If you set it to `0`, the multi-thread optimization is disabled.
- Default value: `2`

#### security

##### `redact-info-log` <span class="version-mark">New in v5.0</span>

- Controls whether to enable log redaction.
- Default value: `false`
- Value options: `true`, `false`, `"on"`, `"off"`, and `"marker"`. The `"on"`, `"off"`, and `"marker"` options are introduced in v8.3.0.
- If the configuration item is set to `false` or `"off"`, log redaction is disabled.
- If the configuration item is set to `true` or `"on"`, all user data in the log is replaced by `?`.
- If the configuration item is set to `"marker"`, all user data in the log is wrapped in `‹ ›`. If user data contains `‹` or `›`, `‹` is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.

#### security.encryption

##### `data-encryption-method`

- The encryption method for data files. A value other than `"plaintext"` means that encryption is enabled, in which case the master key must be specified.
- Default value: `"plaintext"`, which means encryption is disabled by default.
- Value options: `"aes128-ctr"`, `"aes192-ctr"`, `"aes256-ctr"`, `"sm4-ctr"`, `"plaintext"`. `"sm4-ctr"` is introduced in v6.4.0.

##### `data-key-rotation-period`

- Specifies how often the data encryption key is rotated.
- Default value: `7d`

#### security.encryption.master-key

- Specifies the master key if encryption is enabled. To learn how to configure a master key, see [Configure encryption](/encryption-at-rest.md#configure-encryption).

#### security.encryption.previous-master-key

- Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see [Configure encryption](/encryption-at-rest.md#configure-encryption).

### Schedule replicas by topology labels

See [Set available zones](/tiflash/create-tiflash-replicas.md#set-available-zones).

### Multi-disk deployment

TiFlash supports multi-disk deployment. If there are multiple disks in your TiFlash node, you can make full use of those disks by configuring the parameters described in the following sections. For TiFlash's configuration template to be used for TiUP, see [The complex template for the TiFlash topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml).

#### Multi-disk deployment with TiDB version earlier than v4.0.9

For TiDB clusters earlier than v4.0.9, TiFlash only supports storing the main data of the storage engine on multiple disks. You can set up a TiFlash node on multiple disks by specifying the `path` (`data_dir` in TiUP) and `path_realtime_mode` configuration.

If there are multiple data storage directories in `path`, separate each with a comma. For example, `/nvme_ssd_a/data/tiflash,/sata_ssd_b/data/tiflash,/sata_ssd_c/data/tiflash`. If there are multiple disks in your environment, it is recommended that each directory corresponds to one disk and you put disks with the best performance at the front to maximize the performance of all disks.

If there are multiple disks with similar I/O metrics on your TiFlash node, you can leave the `path_realtime_mode` parameter to the default value (or you can explicitly set it to `false`). It means that data will be evenly distributed among all storage directories. However, the latest data is written only to the first directory, so the corresponding disk is busier than other disks.

If there are multiple disks with different I/O metrics on your TiFlash node, it is recommended to set `path_realtime_mode` to `true` and put disks with the best I/O metrics at the front of `path`. It means that the first directory only stores the latest data, and the older data are evenly distributed among the other directories. Note that in this case, the capacity of the first directory should be planned as 10% of the total capacity of all directories.

#### Multi-disk deployment with TiDB v4.0.9 or later

For TiDB clusters with v4.0.9 or later versions, TiFlash supports storing the main data and the latest data of the storage engine on multiple disks. If you want to deploy a TiFlash node on multiple disks, it is recommended to specify your storage directories in the `[storage]` section to make full use of your node. Note that the configurations earlier than v4.0.9 (`path` and `path_realtime_mode`) are still supported.

If there are multiple disks with similar I/O metrics on your TiFlash node, it is recommended to specify corresponding directories in the `storage.main.dir` list and leave `storage.latest.dir` empty. TiFlash will distribute I/O pressure and data among all directories.

If there are multiple disks with different I/O metrics on your TiFlash node, it is recommended to specify directories with higher metrics in the `storage.latest.dir` list, and specify directories with lower metrics in the `storage.main.dir` list. For example, for one NVMe-SSD and two SATA-SSDs, you can set `storage.latest.dir` to `["/nvme_ssd_a/data/tiflash"]` and `storage.main.dir` to `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`. TiFlash will distribute I/O pressure and data among these two directories list respectively. Note that in this case, the capacity of `storage.latest.dir` should be planned as 10% of the total planned capacity.

> **Warning:**
>
> The `[storage]` configuration is supported in TiUP since v1.2.5. If your TiDB cluster version is v4.0.9 or later, make sure that your TiUP version is v1.2.5 or later. Otherwise, the data directories defined in `[storage]` will not be managed by TiUP.
