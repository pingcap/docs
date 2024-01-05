---
title: Titan Configuration
summary: Learn how to configure Titan.
---

# Titan Configuration

This document introduces how to enable and disable [Titan](/storage-engine/titan-overview.md) using the corresponding configuration items, as well as the relevant parameters and the Level Merge feature.

## Enable Titan

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

After Titan is enabled, the existing data stored in RocksDB is not immediately moved to the Titan engine. As new data is written to the TiKV foreground and RocksDB performs compaction, the values are progressively separated from keys and written to Titan. It's same for the data imported from snapshot restore, PiTR restore or TiDB lightning that initially it's in RocksDB format and converted to Titan during compaction. You can view the **TiKV Details** -> **Titan kv** -> **blob file size** panel to confirm the size of the data stored in Titan.

If you want to speed up the writing process, compact data of the whole TiKV cluster manually using tikv-ctl. For details, see [manual compaction](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually). Because RocksDB has the Block cache and the access pattern in compaction is sequential read and thus the block cache hit rate can be pretty high. In our test, a 670 GiB TiKV data can be converted to Titan in less than 1 hour.  

> **Note:**
>
> Starting from TiDB 7.6.0, the newly created empty cluster will by default enable Titan. And existing clusters' upgrade to TiDB 7.6.0 would keep the original configuration--- if the titan is not explicityly enabled, then it would still use RocksDB. 


> **Warning:**
>
> When Titan is disabled, RocksDB cannot read data that has been migrated to Titan. If Titan is incorrectly disabled on a TiKV instance with Titan already enabled (mistakenly set `rocksdb.titan.enabled` to `false`), TiKV will fail to start, and the `You have disabled titan when its data directory is not empty` error appears in the TiKV log. To correctly disabled Titan, see [Disable Titan](#disable-titan).

## Parameters

To adjust Titan-related parameters using TiUP, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration).

+ Titan GC thread count.

    From the **TiKV Details** -> **Thread CPU** -> **RocksDB CPU** panel, if you observe that the Titan GC threads are at full capacity for a long time, consider increasing the size of the Titan GC thread pool.

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    max-background-gc = 1
    ```

+ Value size threshold.

    When the size of the value written to the foreground is smaller than the threshold, this value is stored in RocksDB; otherwise, this value is stored in the blob file of Titan. Based on the distribution of value sizes, if you increase the threshold, more values are stored in RocksDB and TiKV performs better in reading small values. If you decrease the threshold, more values go to Titan, which further reduces RocksDB compactions. In our [test](/storage-engine/titan-overview.md#min-blob-sizes-performance-implications), 1 KB is a balanced threshold which has far better write throughput with about 10% scan throughput regression compared with RocksDB. 

    ```toml
    [rocksdb.defaultcf.titan]
    min-blob-size = "1KB"
    ```

+ The algorithm used for compressing values in Titan, which takes value as the unit. Starting from TiDB 7.6.0, the default compression is zstd.

    ```toml
    [rocksdb.defaultcf.titan]
    blob-file-compression = "zstd"
    ```

+ By default, zstd-dict-size is 0KB , which means Titan's compression is based on single value. But RocksDB compression is based on block (32 KB size by default)，So when titan value's average size is less than 32 KB, Titan's comression ratio is smaller than RocksdDB。 Taking json as an example, Titan store size can be 30% ~ 50% bigger than RocksDB. The actual compression ratio depends on the value content and the similiarity among different values. A user can set zstd-dict-size (e.g. 16KB) to enable zstd dictionary compression to boost the compression ratio. Though the zstd dictionary compression can achieve similar compression ratio of RocksDB, it does leads to 10% throughput regression in a typical read-write workload.

    ```toml
    [rocksdb.defaultcf.titan]
    zstd-dict-size = "16KB"
    ``` 

+ The size of value caches in Titan.

    Larger cache size means higher read performance of Titan. However, too large a cache size causes Out of Memory (OOM). It is recommended to set the value of `storage.block-cache.capacity` to the store size minus the blob file size and set `blob-cache-size` to `memory size * 50% - block cache size` according to the monitoring metrics when the database is running stably. This maximizes the blob cache size when the block cache is large enough for the whole RocksDB engine.

    ```toml
    [rocksdb.defaultcf.titan]
    blob-cache-size = 0
    ```

+ When the ratio of discardable data (the corresponding key has been updated or deleted) in a blob file exceeds the following threshold, Titan GC is triggered.

    ```toml
    discardable-ratio = 0.5
    ```

    When Titan writes the useful data of this blob file to another file, you can use the `discardable-ratio` value to estimate the upper limits of write amplification and space amplification (assuming the compression is disabled).

    Upper limit of write amplification = 1 / discardable_ratio

    Upper limit of space amplification = 1 / (1 - discardable_ratio)

    From the two equations above, you can see that decreasing the value of `discardable_ratio` can reduce space amplification but causes GC to be more frequent in Titan. Increasing the value reduces Titan GC, the corresponding I/O bandwidth, and CPU consumption but increases disk usage.

+ The following option limits the I/O rate of RocksDB compaction. During peak traffic, limiting RocksDB compaction, its I/O bandwidth, and its CPU consumption reduces its impact on the write and read performance of the foreground.

    When Titan is enabled, this option limits the summed I/O rates of RocksDB compaction and Titan GC. If you find that the I/O and/or CPU consumption of RocksDB compaction and Titan GC is too large, set this option to a suitable value according the disk I/O bandwidth and the actual write traffic.

    ```toml
    [rocksdb]
    rate-bytes-per-sec = 0
    ```

## Disable Titan

To disable Titan, you can configure the `rocksdb.defaultcf.titan.blob-run-mode` option. The optional values for `blob-run-mode` are as follows:

- When the option is set to `normal`, Titan performs read and write operations normally.
- When the option is set to `read-only`, all newly written values are written into RocksDB, regardless of the value size.
- When the option is set to `fallback`, all newly written values are written into RocksDB, regardless of the value size. Also, all compacted values stored in the Titan blob file are automatically moved back to RocksDB.

To fully disable Titan for all existing and future data, you can follow these steps. Note that in general you can skip step 2 as it would greatly impact online traffic performance. And in fact even without step 2, the data convertion takes extra IO and CPU and thus performance degrade (some times as large as 50%) is still observed when TiKV's IO or CPU resource reaches near limit.  

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
    > When `discardable-ratio=1`, it means TiKV will only recycle a Titan blob file when all its data are moved to RocksDB. That means before the convertion completes, these Titan blob files won't be deleted. And therefore, if a TiKV node does not have sufficent disk size to store both Titan and RocksDB data, the parameter should keep the default value instead of `1.0`. However if the disk size is big enough, `discardable-ratio = 1.0` can help to reduce the blob file GC and the disk IO. 
    >

2. [Optional] Perform a full compaction using tikv-ctl. This process will consume large amount of I/O and CPU resources.

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```


3. After the compaction is finished, you should wait for the **Blob file count** metrics under **TiKV-Details**/**Titan - kv** to decrease to `0`.

4. Update the configuration of these TiKV nodes to disable Titan.

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

### Data convertion speed from Titan to RocksDB

Because Blob cache only helps when a value is accessed more than once, in compaction scenario, it's likely not useful. As a result, the data convertion from Titan to RocksDB can be 10x slower than RocksDB to Titan. In our test, a 800 GiB TiKV takes 12 hour to completely convert its data to RocksDB. 

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
