---
title: Titan Configuration
aliases: ['/docs-cn/dev/storage-engine/titan-configuration/','/docs-cn/dev/reference/titan/configuration/','/docs-cn/dev/titan-configuration/']
---

# Titan Configuration

Titan 是基于 RocksDB 开发的存储引擎插件，通过把 key 和 value 分离存储，在 value 较大的场景下，减少写放大，降低 RocksDB 后台 compaction 对 I/O 带宽和 CPU 的占用，以提高性能。详情参阅 [Titan 介绍](/storage-engine/titan-overview.md)。

本文档介绍如何如何通过 Titan 配置项来开启、关闭 Titan，相关参数介绍，以及 level merge 功能。

Titan is a RocksDB-based plugin for key-value separation. The goal of Titan is to reduce write amplification in RocksDB and make compaction operations occupy less I/O bandwidth and CPU resources when using large values. For more details of Titan, see [Titan Overview](/storage-engine/titan-overview.md).

This document introduces how to enable and disable Titan using the corresponding configuration items, the relevant parameters, and the Level Merge feature.

## Enable Titan

Titan is compatible with RocksDB, that is, you can directly enable Titan on the existing TiKV instances that use RocksDB. You can use one of the following two methods to enable Titan.

+ Method 1: If you have deployed the cluster using TiUP, you can execute the `tiup cluster edit-config ${cluster-name}` command and edit the TiKV configuration file as the following example shows:

    {{< copyable "shell-regular" >}}

    ```shell
      tikv:
        rocksdb.titan.enabled: true
    ```

    Reload the configuration and TiKV will be rolling restarted online:

    {{< copyable "shell-regular" >}}

    ```shell
    `tiup cluster reload ${cluster-name} -R tikv`
    ```

    For the detailed command, see [Modify the configuration using TiUP](/maintain-tidb-using-tiup.md#modify-the-configuration).

+ Method 2: Directly edit the TiKV configuration file to enable Titan (**NOT** recommended for the production environment).

    {{< copyable "" >}}

    ``` toml
    [rocksdb.titan]
    enabled = true
    ```

开启 Titan 以后，原有的数据并不会马上移入 Titan 引擎，而是随着前台写入和 RocksDB compaction 的进行，逐步进行 key-value 分离并写入 Titan。可以通过观察 **TiKV Details** - **Titan kv** - **blob file size** 监控面版确认数据保存在 Titan 中部分的大小。

如果需要加速数据移入 Titan，可以通过 tikv-ctl 执行一次全量 compaction，具体参考[手动 compact](/tikv-control.md#手动-compact-整个-tikv-集群的数据)。

After Titan is enabled, the existing data is not immediately written to the Titan engine but . As new data is written to the TiKV foreground and RocksDB performs compaction, the values are progressively separated from keys and written to Titan. You can view the **TiKV Details** -> **Titan kv** -> **blob file size** panel to confirm the size of the data stored in Titan.

If you want to speed up the writing process, you can compact data of the whole TiKV cluster manually using tikv-ctl. For details, see [manual compaction](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually).

> **Note:**
>
> 在不开启 Titan 功能的情况下，RocksDB 无法读取已经迁移到 Titan 的数据。如果在打开过 Titan 的 TiKV 实例上错误地关闭了 Titan（误设置 `rocksdb.titan.enabled = false`），启动 TiKV 会失败，TiKV log 中出现 `You have disabled titan when its data directory is not empty` 错误。如需要关闭 Titan，参考[关闭 Titan](#关闭-titan实验功能) 一节。
> When Titan is disabled, RocksDB cannot read data that has been migrated to Titan. If Titan is incorrectly disabled on a TiKV instance with Titan enabled (mistakenly set `rocksdb.titan.enabled` to `false`), TiKV will fail to start, and the `You have disabled titan when its data directory is not empty` error appears in the TiKV log. To correctly disabled Titan, see [Disable Titan](#disable-titan-experimental)

## Parameters

To adjust parameters using TiUP, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration).

+ Titan GC thread count

    From the **TiKV Details** -> **Thread CPU** -> **RocksDB CPU** panel, if you observe that the Titan GC threads are at full capacity for a long time, consider increase the size of the Titan GC thread pool.

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    max-background-gc = 1
    ```

+ Threshold of value size

    当写入的 value 小于这个值时，value 会保存在 RocksDB 中，反之则保存在 Titan 的 blob file 中。根据 value 大小的分布，增大这个值可以使更多 value 保存在 RocksDB，读取这些小 value 的性能会稍好一些；减少这个值可以使更多 value 保存在 Titan 中，进一步减少 RocksDB compaction。
    When the value to write is smaller than the threshold, this value is stored in RocksDB; otherwise, this value is stored in the blob file of Titan. Based on the distribution of value sizes, if you increase the threshold, more values are stored in RocksDB, which performs better in reading small values. If you decrease the threshold, more values go to Titan, which reduces RocksDB compactions.

    ```toml
    [rocksdb.defaultcf.titan]
    min-blob-size = "1KB"
    ```

+ Titan 中 value 所使用的压缩算法。Titan 中压缩是以 value 为单元的。

+ The compression algorithm used for values in Titan, which takes value as the unit.

    ```toml
    [rocksdb.defaultcf.titan]
    blob-file-compression = "lz4"
    ```

+ The cache size of value in Titan

    更大的缓存能提高 Titan 读性能，但过大的缓存会造成 OOM。建议在数据库稳定运行后，根据监控把 RocksDB block cache (storage.block-cache.capacity) 设置为 store size 减去 blob file size 的大小，`blob-cache-size` 设置为 `内存大小 * 50% 再减去 block cache 的大小`。这是为了保证 block cache 足够缓存整个 RocksDB 的前提下，blob cache 尽量大。

    Larger cache size means higher read performance of Titan. However, too large 

    ```toml
    [rocksdb.defaultcf.titan]
    blob-cache-size = 0
    ```

+ 当一个 blob file 中无用数据（相应的 key 已经被更新或删除）比例超过以下阈值时，将会触发 Titan GC 。

    ```toml
    discardable-ratio = 0.5
    ```

    将此文件有用的数据重写到另一个文件。这个值可以估算 Titan 的写放大和空间放大的上界（假设关闭压缩）。公式是：

    写放大上界 = 1 / discardable_ratio

    空间放大上界 = 1 / (1 - discarable_ratio)

    可以看到，减少这个阈值可以减少空间放大，但是会造成 Titan 更频繁 GC；增加这个值可以减少 Titan GC，减少相应的 I/O 带宽和 CPU 消耗，但是会增加磁盘空间占用。

+ 以下选项限制 RocksDB compaction 的 I/O 速率，以达到在流量高峰时，限制 RocksDB compaction 减少其 I/O 带宽和 CPU 消耗对前台读写性能的影响。

    当开启 Titan 时，该选项限制 RocksDB compaction 和 Titan GC 的 I/O 速率总和。当发现在流量高峰时 RocksDB compaction 和 Titan GC 的 I/O 和/或 CPU 消耗过大，可以根据磁盘 I/O 带宽和实际写入流量适当配置这个选项。

    ```toml
    [rocksdb]
    rate-bytes-per-sec = 0
    ```

## 关闭 Titan（实验功能）

通过设置 `rocksdb.defaultcf.titan.blob-run-mode` 参数可以关闭 Titan。`blob-run-mode` 可以设置为以下几个值之一：

- 当设置为 `kNormal` 时，Titan 处于正常读写的状态。
- 当设置为 `kReadnly` 时，新写入的 value 不论大小均会写入 RocksDB。
- 当设置为 `kFallback` 时，新写入的 value 不论大小均会写入 RocksDB，并且当 RocksDB 进行 compaction 时，会自动把所碰到的存储在 Titan blob file 中的 value 移回 RocksDB。

当需要关闭 Titan 时，可以设置 `blob-run-mode = "kFallback"`，并通过 tikv-ctl 执行全量 compaction。此后通过监控确认 blob file size 降到 0 以后，可以更改 rocksdb.titan.enabled = false 并重启 TiKV。

> **注意：**
>
> 关闭 Titan 是实验性功能，非必要不建议使用。

## Level Merge（实验功能）

TiKV 4.0 中 Titan 提供新的算法提升范围查询性能并降低 Titan GC 对前台写入性能的影响。这个新的算法称为 level merge。Level merge 可以通过以下选项开启：

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

开启 level merge 的好处如下：

- 大幅提升 Titan 的范围查询性能。
- 减少了 Titan GC 对前台写入性能的影响，提升写入性能。
- 减少 Titan 空间放大，减少磁盘空间占用（默认配置下的比较）。

相应地，level merge 写放大会比 Titan 稍高，但依然低于原生的 RocksDB。
