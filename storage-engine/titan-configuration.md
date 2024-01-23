---
title: Titan Configuration
summary: Learn how to configure Titan.
---

# Titan Configuration

This document introduces how to enable and disable [Titan](/storage-engine/titan-overview.md) using the corresponding configuration items, as well as the relevant parameters and the Level Merge feature.

## Enable Titan

> **Note:**
>
> - Starting from TiDB v7.6.0, Titan is enabled by default to enhance the performance of writing wide tables and JSON data as well as point queries. 
> - For existing clusters upgraded to v7.6.0 or later versions retain the original configuration, which means that if Titan is not explicitly enabled, it still uses RocksDB.

Titan is compatible with RocksDB, so you can directly enable Titan on the existing TiKV instances that use RocksDB. You can use one of the following two methods to enable Titan:

+ Method 1: If you have deployed the cluster using TiUP, you can execute the `tiup cluster edit-config ${cluster-name}` command and edit the TiKV configuration file as the following example shows:

    {{< copyable "shell-regular" >}}

    ```shell
      tikv:
        rocksdb.titan.enabled: true
    ```

    Reload the configuration and TiKV will be rolling restarted dynamically:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    For the detailed command, see [Modify the configuration using TiUP](/maintain-tidb-using-tiup.md#modify-the-configuration).

+ Method 2: Directly edit the TiKV configuration file to enable Titan (**NOT** recommended for the production environment).

    {{< copyable "" >}}

    ``` toml
    [rocksdb.titan]
    enabled = true
    ```

+ Method 3: Edit the `${cluster_name}/tidb-cluster.yaml` configuration file for TiDB-Operator:

     {{< copyable "" >}}
 
    ``` yaml
      tikv:
        ## Base image of the component
        baseImage: pingcap/tikv
        ## tikv-server configuration
        ## Ref: https://docs.pingcap.com/tidb/stable/tikv-configuration-file
        config: |
          log-level = "info"
          [rocksdb]
            [rocksdb.titan]
              enabled = true
    ```
    Apply the configuration to trigger an online rolling restart of the TiDB cluster for the changes to take effect:

   {{< copyable "" >}}

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    For more information, refer to [Configuring a TiDB Cluster in Kubernetes](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster).

## Data Convertion

> **Warning:**
>
> When Titan is disabled, RocksDB cannot read data that has been moved to Titan. If Titan is incorrectly disabled on a TiKV instance with Titan already enabled (mistakenly set `rocksdb.titan.enabled` to `false`), TiKV will fail to start, and the `You have disabled titan when its data directory is not empty` error appears in the TiKV log. To correctly disabled Titan, see [Disable Titan](#disable-titan).

After Titan is enabled, the existing data stored in RocksDB is not immediately moved to the Titan engine. As new data is written to the TiKV and RocksDB performs compaction, the values are progressively separated from keys and written to Titan. Similarly, the data restored through BR snapshot/log and imported via TiDB Lightning, is not written directly into Titan. As compaction proceeds, the large values exceeding the [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) default of `32KB`` in the processed SST files are separated into Titan. Users can monitor the size of files stored in Titan by observing the **TiKV Details - Titan kv - blob file size** panel to confirm the size of the data stored in Titan.

If you want to speed up the writing process, compact data of the whole TiKV cluster manually using tikv-ctl. For details, see [manual compaction](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually). RocksDB has the Block cache and the continuous data access during the transition from RocksDB to Titan, the Block Cache significantly accelerates the data convertion process. In the test, by using tikv-ctl, a volume of 670 GiB TiKV data can be converted to Titan in one hour.  

While the values in Titan Blob files are not contiguous, and Titan's cache is at the value level, the Blob Cache does not help during compaction. The speed from Titan to RocksDB is an order of magnitude slower than the speed from RocksDB to Titan. In the test, it takes 12 hours to convert a volume of 800 GiB Titan data on a TiKV node to RocksDB by tikv-ctl in a full compaction.

## Parameters

The [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) sets the threshold for the value's size, determining which data is stored in RocksDB and which is stored in Titan's blob file. According to the [test](/storage-engine/titan-overview.md#performance-implications-of-min-blob-size), `32 KB` is a conservative threshold that has better write throughput without scan throughput regression compared with RocksDB. If you want further improve write performance and meanwhile accept scan performance regression, the value can be adjust to `1 KB`。

The [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) parameter specifies the compression algorithm used for values in Titan, while enabling zstd dictionary compression with [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) can improve compression rates.

The [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) parameter controls the cache size of values in Titan. Larger cache size means higher read performance of Titan. However, too large a cache size causes Out of Memory (OOM). It is recommended to set the value of `storage.block-cache.capacity` to the store size minus the blob file size and set `blob-cache-size` to `memory size * 50% - block cache size` according to the monitoring metrics when the database is running stably. This maximizes the blob cache size when the block cache is large enough for the whole RocksDB engine.

The [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) parameter and [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) parameter significantly impact Titan's read performance and garbage collection process. 

Finally, by adjusting [`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec), you can limit the I/O rate of RocksDB compaction, reducing its impact on foreground read and write performance during high traffic.

The following is an example Titan configuration file. You have the option to either use TiUP to [modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration) or make adjustments in a TiDB cluster [configured within Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster).

    {{< copyable "" >}}

``` toml
    [rocksdb]
    rate-bytes-per-sec = 0

    [rocksdb.titan]
    enabled = true
    max-background-gc = 1

    [rocksdb.defaultcf.titan]
    min-blob-size = "32KB"
    blob-file-compression = "zstd"
    zstd-dict-size = "16KB"
    blob-cache-size = "0GB"
    discardable-ratio = 0.5
    blob-run-mode = "normal"
    level-merge = false
```

## Disable Titan

To disable Titan, you can configure the `rocksdb.defaultcf.titan.blob-run-mode` option. The optional values for `blob-run-mode` are as follows:

- When the option is set to `normal`, Titan performs read and write operations normally.
- When the option is set to `read-only`, all newly written values are written into RocksDB, regardless of the value size.
- When the option is set to `fallback`, all newly written values are written into RocksDB, regardless of the value size. Also, all compacted values stored in the Titan blob file are automatically moved back to RocksDB.

To fully disable Titan for all existing and future data, you can follow these steps. Note that in general you can skip Step 2 because it can greatly impact online traffic performance. In fact even without Step 2, the data compaction consumes extra I/O and CPU resources when it migrates data from Titan to RocksDB, and performance will degrade (sometimes as much as 50%) when TiKV's I/O or CPU resources are limited.  

1. Update the configuration of the TiKV nodes you wish to disable Titan for. You can update configuration in two methods:

    + Execute `tiup cluster edit-config`, edit the configuration file, and execute `tiup cluster reload -R tikv`.
    + Manually update the configuration file and restart TiKV.

    ```toml
    [rocksdb.defaultcf.titan]
    blob-run-mode = "fallback"
    discardable-ratio = 1.0
    ```

    > **Note:**
    >
    > When there is insufficient disk space to accommodate both Titan and RocksDB data, it is recommended to use the default value of `0.5` for [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio). In general, if the free disk space is below 50%, it is advisable to use the default value. This is because when `discardable-ratio = 1.0`, the RocksDB data keeps growing. At the same time, the recovery of Titan's original blob file requires all the data in that file to be migrated to RocksDB, which is a slow process. However, if the disk size is large enough, setting `discardable-ratio = 1.0` can reduce the GC of the blob file itself during compaction, which saves bandwidth.

2. (Optional) Perform a full compaction using tikv-ctl. This process will consume a large amount of I/O and CPU resources.

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3. After the compaction is finished, you should wait for the **Blob file count** metrics under **TiKV-Details**/**Titan - kv** to decrease to `0`.

4. Update the configuration of these TiKV nodes to disable Titan.

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

## Level Merge (experimental)

In TiKV 4.0, [Level Merge](/storage-engine/titan-overview.md#level-merge), a new algorithm, is introduced to improve the performance of range query and to reduce the impact of Titan GC on the foreground write operations. You can enable Level Merge using the following option:

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

Enabling Level Merge has the following benefits:

- Greatly improve the performance of Titan range query.
- Reduce the impact of Titan GC on the foreground write operations and improve write performance.
- Reduce space amplification of Titan and the disk usage (compared to the disk usage with the default configuration).

Accordingly, the write amplification with Level Merge enabled is slightly higher than that of Titan but is still lower than that of the native RocksDB.
