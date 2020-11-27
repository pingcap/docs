---
title: Configure TiFlash
summary: Learn how to configure TiFlash.
aliases: ['/docs/dev/tiflash/tiflash-configuration/','/docs/dev/reference/tiflash/configuration/']
---

# Configure TiFlash

This document introduces the configuration parameters related to the deployment and use of TiFlash.

## PD scheduling parameters

You can adjust the PD scheduling parameters using [pd-ctl](/pd-control.md). Note that you can use `tiup ctl pd` to replace `pd-ctl -u <pd_ip:pd_port>` when using tiup to deploy and manage your cluster.

- [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit): determines the rate at which the replica-related operator is generated. The parameter affects operations such as making nodes offline and add replicas.

    > **Notes:**
    >
    > The value of this parameter should be less than that of `region-schedule-limit`. Otherwise, the normal Region scheduling among TiKV nodes is affected.

- [`store-balance-rate`](/pd-configuration-file.md#store-balance-rate): limits the rate at which Regions of each TiKV/TiFlash store are scheduled. Note that this parameter takes effect only when the stores have newly joined the cluster. If you want to change the setting for existing stores, use the following command.

    > **Note:**
    >
    > Since v4.0.2, the `store-balance-rate` parameter has been deprecated and changes have been made to the `store limit` command. See [store-limit](/configure-store-limit.md) for details.

    - Execute the `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` command to set the scheduling rate of a specified store. (To get `store_id`, you can execute the `pd-ctl -u <pd_ip:pd_port> store` command. 
    - If you do not set the scheduling rate for Regions of a specified store, this store inherits the setting of `store-balance-rate`.
    - You can execute the `pd-ctl -u <pd_ip:pd_port> store limit` command to view the current setting value of `store-balance-rate`.

## TiFlash configuration parameters

This section introduces the configuration parameters of TiFlash.

### Configure the `tiflash.toml` file

```toml
# The listening host for supporting services such as TPC/HTTP. It is recommended to configure it as "0.0.0.0".
listen_host = "0.0.0.0"
tcp_port = 9000 # The TiFlash TCP service port.
http_port = 8123 # The TiFlash HTTP service port.
mark_cache_size = 5368709120 # The cache size limit of the metadata of a data block. Generally, you do not need to change this value.
minmax_index_cache_size = 5368709120 # The cache size limit of the min-max index of a data block. Generally, you do not need to change this value.

# The TiFlash data storage path. If there are multiple directories, separate each directory with a comma.
# `path` and `path_realtime_mode` is deprecated since v4.0.9. Use the configurations in `[storage]` section to get better performance under multi-disk deployment
# path = "/tidb-data/tiflash-9000"
# or
# path = "/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"
# The default value is `false`. If you set it to `true` and multiple directories are set in the path, the latest data is stored in the first directory and older data is stored in the rest directories.
# path_realtime_mode = false 

# The path in which the TiFlash temporary files are stored.
# tmp_path = "/tidb-data/tiflash-9000/tmp"

## Storage paths settings since v4.0.9
[storage]
    ## If there are multiple SSD disks on the TiFlash node, specify the path list on `storage.main.dir` to make full use of the node.

    ## If there are multiple disks with different IO metrics (e.g. one SSD and some HDDs) on the TiFlash node, you can make full use of the node by:
    ## * setting `storage.latest.dir` to store the latest data on SSD (disks with higher IOPS metrics)
    ## * setting `storage.main.dir` to store the main data on HDD (disks with lower IOPS metrics)

    [storage.main]
    ## The path to store main data.
    dir = [ "/tidb-data/tiflash-9000" ] 
    # or
    # dir = [ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]

    ## Store capacity of each path, i.e. max data size allowed.
    ## If it is not set, or is set to 0s, the actual disk capacity is used.
    ## Note that we don't support human-readable big numbers(like "10GB") yet.
    ## Please set in the specified number of bytes.
    ## The size of `capacity` list should be the same with `dir` size.
    # e.g.
    # capacity = [ 10737418240, 10737418240 ]

    [storage.latest]
    ## The path(s) to store latest data.
    ## If not set, it will be the same with `storage.main.dir`.
    # dir = [ ]
    ## Store capacity of each path, i.e. max data size allowed.
    ## If it is not set, or is set to 0s, the actual disk capacity is used.
    # capacity = [ 10737418240, 10737418240 ]

    [storage.raft]
    ## The path(s) to store Raft data.
    ## If not set, it will be the paths in `storage.latest.dir` appended with "/kvstore".
    # dir = [ ]

[flash]
    tidb_status_addr = TiDB status port and address. # Multiple addresses are separated with commas.
    service_addr = The listening address of TiFlash Raft services and coprocessor services.

# Multiple TiFlash nodes elect a master to add or delete placement rules to PD, and you need three parameters to control this process.
[flash.flash_cluster]
    refresh_interval = Master regularly refreshes the valid period.
    update_rule_interval = Master regularly gets the status of TiFlash replicas and interacts with PD.
    master_ttl = The valid period of the elected master.
    cluster_manager_path = The absolute path of the pd buddy directory.
    log = The pd buddy log path.

[flash.proxy]
    addr = The listening address of proxy.
    advertise-addr = The external access address of addr. If it is left empty, addr is used by default.
    data-dir = The data storage path of proxy.
    config = The proxy configuration file path.
    log-file = The proxy log path.
    status-addr = The listening address from which the proxy metrics | status information is pulled.
    advertise-status-addr = The external access address of status-addr. If it is left empty, status-addr is used by default.

[logger]
    level = log level (available options: trace, debug, information, warning, error).
    log = The TiFlash log path.
    errorlog = The TiFlash error log path.
    size = The size of a single log file.
    count = The maximum number of log files to save.

[raft]
    pd_addr = PD service address. # Multiple addresses are separated with commas.
    # The storage path of the Raft data. The default setting is "{the first directory of the path}/kvstore"
    # `raft.kvstore_path` is deprecated since v4.0.9. Use `storage.raft.dir` instead to get better performance on multi-disk deployment.
    # kvstore_path = "/tidb-data/tiflash-9000/kvstore"

[status]
    metrics_port = The port through which Prometheus pulls metrics information.

[profiles]

[profiles.default]
    # The default value is `true`. This parameter determines whether the segment of DeltaTree Storage Engine uses logical split. Using the logical split can reduce the write amplification, and improve the write speed. However, these are at the cost of disk space waste.
    dt_enable_logical_split = true 
    max_memory_usage = 0 # The memory usage limit for the generated intermediate data when a single coprocessor query is executed. The default value is 0, which means no limit.
    max_memory_usage_for_all_queries = 0 # The memory usage limit for the generated intermediate data when all queries are executed. The default value is 0 (in bytes), which means no limit.
```

### Configure the `tiflash-learner.toml` file

```toml
[server]
    engine-addr = The external access address of the TiFlash coprocessor service.
[raftstore]
    # Specifies the number of threads that handle snapshot. The default number is 2. If you set it to 0, the multi-thread optimization is disabled.
    snap-handle-pool-size = 2 
    # Specifies the shortest interval at which Raft store persists WAL. You can properly increase the latency to reduce IOPS usage. The default value is 4ms. If you set it to 0ms, the optimization is disabled.
    store-batch-retry-recv-timeout = "4ms"
```

In addition to the items above, other parameters are the same with those of TiKV. Note that the configuration items in `tiflash.toml [flash.proxy]` will override the overlapping parameters in `tiflash-learner.toml`; The `label` whose key is `engine` is reserved and cannot be configured manually.

### Multi-disk deployment

TiFlash supports multi-disk deployment. If there are multiple disks in your TiFlash node, you can make full use of those disks by following configurations.

#### Deploying a new TiFlash node

If the TiDB cluster version >= v4.0.9:

You can setup TiFlash node on multiple disks by specifying the `[storage]` section in the [`tiflash.toml` file](#configure-the-tiflashtoml-file). The `path` and `path_realtime_mode` are still supported. But TiFlash support storing Raft data and the latest data of storage engine on multiple disks since v4.0.9 to get better performance. It is recommended to specify your storage directories by the `[storage]` section.

If there are multiple disks on your TiFlash node, it is recommended that each directory corresponds to one disk and set the list to `storage.main.dir`.

If there are multiple disks with different IO metrics on the TiFlash node, you can make full use of the node by specifying `storage.latest.dir` and `storage.main.dir`. For example, there are one SSD and two HDDs, you can set `storage.latest.dir` to `["/ssd_a/data/tiflash"]` and `storage.main.dir` to `["/hdd_b/data/tiflash", "/hdd_c/data/tiflash"]`.

> **Notes:**
>
> The configuration [storage] is supported in TiUP since v1.2.5. Please make sure that or the data directories defined in [storage] won't be managed by TiUP.

If the TiDB cluster version < v4.0.9:

You can setup TiFlash node on multiple disks by specifying the `path` and `path_realtime_mode` configuration in the [`tiflash.toml` file](#configure-the-tiflashtoml-file).

If there are multiple data storage directories in `path`, separate each with a comma. For example, `/ssd_a/data/tiflash,/hdd_b/data/tiflash,/hdd_c/data/tiflash`. If there are multiple disks on your TiFlash node, it is recommended that each directory corresponds to one disk and you put disks with the best performance at the front to maximize the performance of all disks.

The default value of the `path_realtime_mode` parameter is `false`, which means that data are evenly distributed on all storage directories. This is suit for deploying TiFlash on a node with multiple SSD disks.

If `path_realtime_mode` is set to `true`, and `path` contains multiple directories, it means that the first directory only stores the latest data, and the older data are evenly distributed on other directories. This is suit for deploying TiFlash on a node with one SSD disk and multiple SSD disks.

#### Upgrading TiFlash node to v4.0.9 or higher

For version is lower than v4.0.9, TiFlash only support storing the main data of storage engine on multiple disks. For version v4.0.9 and higher, TiFlash support storing the main data and the latest data of storage engine and the Raft data on multiple disks.

If the TiFlash node only use one directory to store data, or the data directories are composed of one SSD with multiple HDDs, the new configurations won't impact TiFlash performance. It is ok to keep your old configurations unchanged.

But if the data directories is composed of multiple SSDs, properly specifying the new configurations can better make use of I/O resources. If your TiFlash node happen to meets I/O bottleneck, you can update the configurations to try to fix it. Guidelines to update your configurations by using TiUP:

> **Notes:**
>
> After turn to use the [storage] configurations, downgrading your cluster version to less than v4.0.9 may make some TiFlash data lost.

1. Make sure your TiUP version is v1.2.5 or higher, or the data directories in new configurations won't be managed by TiUP

2. Use TiUP to [upgrade your cluster](/upgrade-tidb-using-tiup.md) to the version you wanted

3. Read the following comparsion between old and new configurations and ensure the behavior of TiFlash

4. Use TiUP to [modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration) of TiFlash node. Add `storage.main.dir` and `storage.latest.dir` in `config` section. You can check the format in here [The complex template for the TiFlash topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml). 

Comparsion between old and new configurations:

For `path_realtime_mode` is not set or is set to `false`:

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/nvme_ssd1/tiflash"
    config:
      # path_realtime_mode: false # by default
```

is equaivalent to following configurations. Check the comment lines to know that adjusting the value of `storage.latest.dir` can get better performance

```yaml
tiflash_servers:
  - host: 10.0.1.14
    # `data_dir` will be overwrite by `storage.*` configurations
    data_dir: "/nvme_ssd0/tiflash,/nvme_ssd1/tiflash"
    config:
      storage.main.dir:     [ "/nvme_ssd0/tiflash", "/nvme_ssd1/tiflash" ]
      ## is equivalent to old ones, latest data will be written to the first directory
      storage.latest.dir:   [ "/nvme_ssd0/tiflash" ]
      ## you can extend the `storage.latest.dir` list to make full use of multiple disks
      # storage.latest.dir: [ "/nvme_ssd0/tiflash", "/nvme_ssd1/tiflash" ]
```

For `path_realtime_mode` is set to `true`:

```yaml
tiflash_servers:
  - host: 10.0.1.14
    data_dir: "/nvme_ssd0/tiflash,/hdd1/tiflash,/hdd2/tiflash"
    config:
      path_realtime_mode: true
```

is equaivalent to following configurations.

```yaml
tiflash_servers:
  - host: 10.0.1.14
    # `data_dir` will be overwrite by `storage.*` configurations
    data_dir: "/nvme_ssd0/tiflash,/hdd1/tiflash,/hdd2/tiflash"
    config:
      ## use HDD to store main data
      storage.main.dir:   [ "/hdd1/tiflash", "/hdd2/tiflash" ]
      ## use SSD to store latest data (required higher I/O metrics)
      storage.latest.dir: [ "/nvme_ssd0/tiflash" ]
```

> **Notes:**
>
> For those TiDB cluster not managed by TiUP, you can modify corresponding configurations in tiflash.toml
