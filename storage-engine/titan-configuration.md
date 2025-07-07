---
title: Titan 配置
summary: 了解如何配置 Titan。
---

# Titan 配置

本文介绍如何通过相应的配置项、数据转换机制、相关参数以及 Level Merge 特性，启用和禁用 [Titan](/storage-engine/titan-overview.md)。

## 启用 Titan

> **注意事项：**
>
> - 从 TiDB v7.6.0 版本开始，为了提升写入宽表和 JSON 数据的性能，新集群默认启用 Titan。`[min-blob-size]`(/tikv-configuration-file.md#min-blob-size) 阈值的默认值由 `1KB` 改为 `32KB`。
> - 升级到 v7.6.0 或更高版本的现有集群会保留原有配置，即如果没有显式启用 Titan，仍然使用 RocksDB。
> - 如果在升级集群到 TiDB v7.6.0 或更高版本之前已启用 Titan，升级后 Titan 将自动启用，并且升级前的 `[min-blob-size]`(/tikv-configuration-file.md#min-blob-size) 配置也会被保留。如果在升级前没有显式配置该值，则会保留旧版本的默认值 `1KB`，以确保升级后集群配置的稳定性。

Titan 与 RocksDB 兼容，因此你可以直接在使用 RocksDB 的现有 TiKV 实例上启用 Titan。可以使用以下方法之一启用 Titan：

+ 方法一：如果你通过 TiUP 部署了集群，可以执行 `tiup cluster edit-config ${cluster-name}` 命令，编辑 TiKV 配置文件，示例如下：

    ```shell
    tikv:
      rocksdb.titan.enabled: true
    ```

    重新加载配置后，TiKV 将会进行滚动重启以应用配置：

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    详细命令请参考 [使用 TiUP 修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration)。

+ 方法二：直接编辑 TiKV 配置文件以启用 Titan（**不推荐用于生产环境**）。

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

+ 方法三：编辑 `${cluster_name}/tidb-cluster.yaml` 配置文件以用于 TiDB Operator：

    ```yaml
    spec:
      tikv:
        ## 组件的基础镜像
        baseImage: pingcap/tikv
        ## tikv-server 配置
        ## 参考文档：https://docs.pingcap.com/tidb/stable/tikv-configuration-file
        config: |
          log-level = "info"
          [rocksdb]
            [rocksdb.titan]
              enabled = true
    ```

    应用配置以触发 TiDB 集群的在线滚动重启，使配置生效：

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    更多信息请参考 [在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster)。

## 数据转换

> **警告：**
>
> 当 Titan 被禁用时，RocksDB 无法读取已迁移到 Titan 的数据。如果在 Titan 已启用（错误设置 `rocksdb.titan.enabled` 为 `false`）的 TiKV 实例上错误禁用 Titan，TiKV 将无法启动，并在日志中出现 `You have disabled titan when its data directory is not empty` 错误。要正确禁用 Titan，请参见 [禁用 Titan](#disable-titan)。

启用 Titan 后，存储在 RocksDB 中的现有数据不会立即迁移到 Titan 引擎。随着新数据写入 TiKV 和 RocksDB 执行压缩，**值会逐步与键分离并写入 Titan**。同样，通过 BR 快照/日志还原的数据、扩容过程中转换的数据或通过 TiDB Lightning 物理导入模式导入的数据，也不会直接写入 Titan。随着压缩的进行，超出默认值 (`32KB`) 的大值会被分离到 Titan 中。你可以通过观察 **TiKV 详情 > Titan kv > blob file size** 面板，监控存储在 Titan 中的文件大小，以估算数据规模。

如果你希望加快写入速度，可以使用 tikv-ctl 手动对整个 TiKV 集群进行压缩。详情请参见 [手动压缩](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually)。在从 RocksDB 转换到 Titan 的过程中，数据访问是连续的，因此 RocksDB 的块缓存极大地加快了数据转换速度。在测试中，使用 tikv-ctl 可以在一小时内将 670 GiB 的 TiKV 数据转换为 Titan。

注意：Titan Blob 文件中的值不是连续存储的，Titan 的缓存是基于值的，因此 Blob Cache 在压缩过程中不起作用。从 Titan 转回 RocksDB 的速度比从 RocksDB 转 Titan 慢一个数量级。在测试中，将 800 GiB 的 Titan 数据通过 tikv-ctl 完整压缩转换为 RocksDB 需要 12 小时。

## 参数

通过合理配置 Titan 参数，可以有效提升数据库性能和资源利用率。本节介绍一些关键参数。

### `min-blob-size`

你可以使用 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 设置值大小的阈值，以决定哪些数据存储在 RocksDB 中，哪些存储在 Titan 的 blob 文件中。根据测试，`32KB` 是一个合适的阈值，确保 Titan 的性能不逊色于 RocksDB。然而，在许多场景下，该值并非最优。建议参考 [`min-blob-size` 对性能的影响](/storage-engine/titan-overview.md#impact-of-min-blob-size-on-performance)，选择合适的值。如果你希望进一步提升写入性能且能容忍扫描性能下降，可以将其设置为最小值 `1KB`。

### `blob-file-compression` 和 `zstd-dict-size`

你可以使用 [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) 指定 Titan 中值的压缩算法，也可以通过 [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) 启用 `zstd` 字典压缩，以提升压缩比。

### `blob-cache-size`

你可以使用 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) 控制 Titan 中值的缓存大小。较大的缓存提升 Titan 的读取性能，但过大的缓存可能导致内存溢出（OOM）。

建议将 `storage.block-cache.capacity` 设置为存储容量减去 blob 文件大小，并根据监控指标在数据库稳定运行时，将 `blob-cache-size` 设置为 `内存大小 * 50% - 块缓存大小`，以最大化 blob 缓存的利用率，前提是块缓存足够大以容纳整个 RocksDB 引擎。

### `discardable-ratio` 和 `max-background-gc`

[`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 和 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) 参数对 Titan 的读取性能和垃圾回收过程影响显著。

当 blob 文件中的过时数据（对应的键已被更新或删除）比例超过 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 设置的阈值时，会触发 Titan GC。降低此阈值可以减少空间放大，但会导致 Titan GC 更频繁。提高此值可以减少 Titan GC、I/O 带宽和 CPU 消耗，但会增加磁盘空间占用。

如果你在 **TiKV 详情** - **Thread CPU** - **RocksDB CPU** 中观察到 Titan GC 线程长时间处于满载状态，可以考虑调整 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc)，以增加 Titan GC 线程池的大小。

### `rate-bytes-per-sec`

你可以调整 [`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec)，限制 RocksDB 压缩的 I/O 速率，减少其在高流量期间对前台读写性能的影响。

### `shared-blob-cache`（v8.0.0 新增）

你可以通过 [`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800) 控制是否启用 Titan blob 文件和 RocksDB 块文件的共享缓存。默认值为 `true`。启用共享缓存后，块文件具有更高的优先级。这意味着 TiKV 会优先满足块文件的缓存需求，然后将剩余缓存用于 blob 文件。

### Titan 配置示例

以下是 Titan 配置文件的示例。你可以 [使用 TiUP 修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration) 或 [在 Kubernetes 上配置 TiDB 集群](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster)。

```toml
[rocksdb]
rate-bytes-per-sec = 0

[rocksdb.titan]
enabled = true
max-background-gc = 1

[rocksdb.defaultcf.titan]
min-blob-size = "32KB"
blob-file-compression = "zstd"
zstd-dict-size = "16KB"
discardable-ratio = 0.5
blob-run-mode = "normal"
level-merge = false
```

## 禁用 Titan

要禁用 Titan，可以配置 `rocksdb.defaultcf.titan.blob-run-mode` 选项。`blob-run-mode` 的可选值如下：

- 设置为 `normal` 时，Titan 正常进行读写操作。
- 设置为 `read-only` 时，所有新写入的值都写入 RocksDB，无论值的大小。
- 设置为 `fallback` 时，所有新写入的值都写入 RocksDB，无论值的大小。同时，存储在 Titan blob 文件中的所有压缩值会自动迁移回 RocksDB。

要禁用所有现有和未来的数据中的 Titan，可以按照以下步骤操作。注意，你可以跳过步骤2，因为它会极大影响在线流量的性能。实际上，即使不执行步骤2，数据从 Titan 转移到 RocksDB 时的压缩也会消耗额外的 I/O 和 CPU 资源，且在 TiKV I/O 或 CPU 资源有限时，性能可能会下降（有时高达 50%）。

> **警告：**
>
> 在 TiDB 版本低于 v8.5.0 时禁用 Titan，不建议修改 TiKV 配置项 [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled) 为 `false`，否则可能导致 TiKV 崩溃。只执行步骤1即可禁用 Titan。

1. 更新你希望禁用 Titan 的 TiKV 节点的配置。可以通过两种方法更新配置：

    + 执行 `tiup cluster edit-config`，编辑配置文件，然后执行 `tiup cluster reload -R tikv`。
    + 手动更新配置文件并重启 TiKV。

        ```toml
        [rocksdb.defaultcf.titan]
        blob-run-mode = "fallback"
        discardable-ratio = 1.0
        ```

    > **注意：**
    >
    > 当磁盘空间不足以容纳 Titan 和 RocksDB 的数据时，建议使用 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 的默认值 `0.5`。一般情况下，当可用磁盘空间少于 50% 时，推荐使用默认值。这是因为当 `discardable-ratio = 1.0` 时，RocksDB 的数据会持续增长。同时，Titan 中现有 blob 文件的回收需要将该文件中的所有数据迁移到 RocksDB，这个过程较慢。但如果磁盘空间足够大，设置 `discardable-ratio = 1.0` 可以减少在压缩过程中对 blob 文件的 GC，从而节省带宽。

2. （可选）使用 tikv-ctl 执行完整压缩。此过程会消耗大量 I/O 和 CPU 资源。

    > **警告：**
    >
    > 当磁盘空间不足时，执行以下命令可能导致整个集群空间耗尽，无法写入数据。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3. 压缩完成后，等待 **TiKV-Details** / **Titan - kv** 下的 **Blob file count** 指标降至 `0`。

## Level Merge（实验性功能）

在 TiKV 4.0 中，引入了 [Level Merge](/storage-engine/titan-overview.md#level-merge) 新算法，以提升范围查询性能并减少 Titan GC 对前台写操作的影响。你可以通过以下配置启用 Level Merge：

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

启用 Level Merge 后的好处包括：

- 大幅提升 Titan 范围查询的性能。
- 减少 Titan GC 对前台写操作的影响，提升写入性能。
- 降低 Titan 的空间放大和磁盘使用（相较于默认配置的磁盘使用）。

相应地，启用 Level Merge 后的写入放大略高于 Titan，但仍低于原生 RocksDB。