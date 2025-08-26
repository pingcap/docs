---
title: 确定你的 TiDB 规模
summary: 了解如何确定你的 TiDB Cloud 集群规模。
---

# 确定你的 TiDB 规模

本文档介绍如何确定 TiDB Cloud 专属集群的规模。

> **Note:**
>
> 你无法更改 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的规模。

## TiDB 规模配置

TiDB 仅用于计算，不存储数据，并且支持水平扩展。

你可以为 TiDB 配置节点数量、vCPU 和内存（RAM）。

如需了解不同集群规模的性能测试结果，请参见 [TiDB Cloud 性能参考](/tidb-cloud/tidb-cloud-performance-reference.md)。

### TiDB vCPU 和内存

支持的 vCPU 和内存规格如下：

| 标准规格      | 高内存规格         | 
|:---------:|:----------------:|
| 4 vCPU, 16 GiB  | N/A          |
| 8 vCPU, 16 GiB    | 8 vCPU, 32 GiB        |
| 16 vCPU, 32 GiB  | 16 vCPU, 64 GiB         |
| 32 vCPU, 64 GiB   | 32 vCPU, 128 GiB        |

> **Note:**
>
> 如需使用 TiDB 的 **32 vCPU, 128 GiB** 规格，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
>
> 如果 TiDB 的 vCPU 和内存规格设置为 **4 vCPU, 16 GiB**，请注意以下限制：
>
> - TiDB 的节点数量只能设置为 1 或 2，TiKV 的节点数量固定为 3。
> - 4 vCPU 的 TiDB 只能与 4 vCPU 的 TiKV 搭配使用。
> - TiFlash 不可用。

### TiDB 节点数量

为了高可用，建议你为每个 TiDB Cloud 集群至少配置两个 TiDB 节点。

通常情况下，TiDB 的性能会随着 TiDB 节点数量的增加而线性提升。但当 TiDB 节点数量超过 8 时，性能提升略低于线性增长。每增加 8 个节点，性能偏差系数约为 5%。

例如：

- 当有 9 个 TiDB 节点时，性能偏差系数约为 5%，因此 TiDB 的性能约为 `9 * (1 - 5%) = 8.55` 倍单节点 TiDB 的性能。
- 当有 16 个 TiDB 节点时，性能偏差系数约为 10%，因此 TiDB 的性能为 `16 * (1 - 10%) = 14.4` 倍单节点 TiDB 的性能。

对于指定延迟的 TiDB 节点，TiDB 的性能会根据不同的读写比例有所不同。

8 vCPU, 16 GiB TiDB 节点在不同负载下的性能如下：

| 负载类型 | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
|----------|-------------------|-------------------|-------------------|
| 读       | 18,900            | 9,450             | 6,300             |
| 混合     | 15,500            | 7,750             | 5,200             |
| 写       | 18,000            | 9,000             | 6,000             |

如果 TiDB 节点数量小于 8，性能偏差系数几乎为 0%，因此 16 vCPU, 32 GiB TiDB 节点的性能大约是 8 vCPU, 16 GiB TiDB 节点的两倍。如果 TiDB 节点数量超过 8，建议选择 16 vCPU, 32 GiB TiDB 节点，这样所需节点更少，性能偏差系数也更小。

在规划集群规模时，你可以根据你的负载类型、整体期望性能（QPS）以及单个 TiDB 节点对应负载类型的性能，使用以下公式估算 TiDB 节点数量：

`node count = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

在公式中，你需要先计算 `node count = ceil(overall expected performance ÷ performance per node)` 得到一个大致的节点数量，然后再结合对应的性能偏差系数得到最终节点数量。

例如，你的整体期望性能为 110,000 QPS，负载为混合型，P95 延迟约为 100 ms，并且希望使用 8 vCPU, 16 GiB 的 TiDB 节点。你可以从上表获取 8 vCPU, 16 GiB TiDB 节点的估算性能（即 `15,500`），并按如下方式计算大致的 TiDB 节点数量：

`node count = ceil(110,000 ÷ 15,500) = 8`

由于 8 个节点的性能偏差系数约为 5%，估算的 TiDB 性能为 `8 * 15,500 * (1 - 5%) = 117,800`，可以满足你 110,000 QPS 的期望性能。

因此，推荐你使用 8 个 TiDB 节点（8 vCPU, 16 GiB）。

## TiKV 规模配置

TiKV 负责存储数据，并支持水平扩展。

你可以为 TiKV 配置节点数量、vCPU 和内存，以及存储容量。

如需了解不同集群规模的性能测试结果，请参见 [TiDB Cloud 性能参考](/tidb-cloud/tidb-cloud-performance-reference.md)。

### TiKV vCPU 和内存

支持的 vCPU 和内存规格如下：

| 标准规格      | 高内存规格         | 
|:---------:|:----------------:|
| 4 vCPU, 16 GiB  |  N/A        |
| 8 vCPU, 32 GiB    | 8 vCPU, 64 GiB        |
| 16 vCPU, 64 GiB  | 即将上线       |
| 32 vCPU, 128 GiB   |  N/A  |

> **Note:**
>
> 如果 TiKV 的 vCPU 和内存规格设置为 **4 vCPU, 16 GiB**，请注意以下限制：
>
> - TiDB 的节点数量只能设置为 1 或 2，TiKV 的节点数量固定为 3。
> - 4 vCPU 的 TiKV 只能与 4 vCPU 的 TiDB 搭配使用。
> - TiFlash 不可用。

### TiKV 节点数量

TiKV 节点数量应为 **至少 1 组（3 个节点，分布在 3 个不同的可用区）**。

TiDB Cloud 会将 TiKV 节点均匀部署到你选择的区域内所有可用区（至少 3 个）以实现数据持久性和高可用。在典型的 3 副本设置下，你的数据会在所有可用区的 TiKV 节点之间均匀分布，并持久化到每个 TiKV 节点的磁盘上。

> **Note:**
>
> 当你扩缩 TiDB 集群时，3 个可用区的节点会同时增加或减少。关于如何根据需求扩容或缩容 TiDB 集群，请参见 [扩缩 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)。

虽然 TiKV 主要用于数据存储，但 TiKV 节点的性能也会根据不同负载类型有所不同。因此，在规划 TiKV 节点数量时，你需要根据 [**数据量**](#estimate-tikv-node-count-according-to-data-volume) 和 [期望性能](#estimate-tikv-node-count-according-to-expected-performance) 两方面进行估算，并取两者中较大的值作为推荐节点数量。

#### 根据数据量估算 TiKV 节点数量

你可以根据数据量按如下方式计算推荐的 TiKV 节点数量：

`node count = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

通常建议 TiKV 存储使用率保持在 80% 以下。TiDB Cloud 默认副本数为 3。8 vCPU, 64 GiB TiKV 节点的最大存储容量为 4096 GiB。

根据历史数据，TiKV 的平均压缩比约为 40%。

假设你的 MySQL dump 文件大小为 20 TB，TiKV 压缩比为 40%。则可以按如下方式根据数据量计算推荐的 TiKV 节点数量：

`node count = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### 根据期望性能估算 TiKV 节点数量

与 TiDB 性能类似，TiKV 的性能会随着 TiKV 节点数量的增加而线性提升。但当 TiKV 节点数量超过 8 时，性能提升略低于线性增长。每增加 8 个节点，性能偏差系数约为 5%。

例如：

- 当有 9 个 TiKV 节点时，性能偏差系数约为 5%，因此 TiKV 的性能约为 `9 * (1 - 5%) = 8.55` 倍单节点 TiKV 的性能。
- 当有 18 个 TiKV 节点时，性能偏差系数约为 10%，因此 TiKV 的性能为 `18 * (1 - 10%) = 16.2` 倍单节点 TiKV 的性能。

对于指定延迟的 TiKV 节点，TiKV 的性能会根据不同的读写比例有所不同。

8 vCPU, 32 GiB TiKV 节点在不同负载下的性能如下：

| 负载类型 | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
|----------|-------------------|-------------------|-------------------|
| 读       | 28,000            | 14,000            | 7,000             |
| 混合     | 17,800            | 8,900             | 4,450             |
| 写       | 14,500            | 7,250             | 3,625             |

如果 TiKV 节点数量小于 8，性能偏差系数几乎为 0%，因此 16 vCPU, 64 GiB TiKV 节点的性能大约是 8 vCPU, 32 GiB TiKV 节点的两倍。如果 TiKV 节点数量超过 8，建议选择 16 vCPU, 64 GiB TiKV 节点，这样所需节点更少，性能偏差系数也更小。

在规划集群规模时，你可以根据你的负载类型、整体期望性能（QPS）以及单个 TiKV 节点对应负载类型的性能，使用以下公式估算 TiKV 节点数量：

`node count = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

在公式中，你需要先计算 `node count = ceil(overall expected performance ÷ performance per node)` 得到一个大致的节点数量，然后再结合对应的性能偏差系数得到最终节点数量。

例如，你的整体期望性能为 110,000 QPS，负载为混合型，P95 延迟约为 100 ms，并且希望使用 8 vCPU, 32 GiB 的 TiKV 节点。你可以从上表获取 8 vCPU, 32 GiB TiKV 节点的估算性能（即 `17,800`），并按如下方式计算大致的 TiKV 节点数量：

`node count = ceil(110,000 / 17,800 ) = 7`

由于 7 小于 8，7 个节点的性能偏差系数为 0。估算的 TiKV 性能为 `7 * 17,800 * (1 - 0) = 124,600`，可以满足你 110,000 QPS 的期望性能。

因此，推荐你根据期望性能使用 7 个 TiKV 节点（8 vCPU, 32 GiB）。

接下来，你可以将根据数据量计算的 TiKV 节点数量与根据期望性能计算的节点数量进行比较，取较大的值作为推荐的 TiKV 节点数量。

### TiKV 节点存储容量

不同 TiKV vCPU 支持的节点存储容量如下：

| TiKV vCPU | 最小节点存储 | 最大节点存储 | 默认节点存储 |
|:---------:|:------------:|:------------:|:------------:|
| 4 vCPU    | 200 GiB      | 2048 GiB     | 500 GiB      |
| 8 vCPU    | 200 GiB      | 4096 GiB     | 500 GiB      |
| 16 vCPU   | 200 GiB      | 4096 GiB     | 500 GiB      |
| 32 vCPU   | 200 GiB      | 4096 GiB     | 500 GiB      |

> **Note:**
>
> 集群创建后，TiKV 节点存储容量无法减少。

### TiKV 节点存储类型

TiDB Cloud 为托管在 AWS 上的 [TiDB Cloud 专属](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供以下 TiKV 存储类型：

- [基础存储](#basic-storage)
- [标准存储](#standard-storage)
- [高性能与 Plus 存储](#performance-and-plus-storage)

#### 基础存储

基础存储是一种通用型存储类型，性能低于标准存储。

基础存储类型会自动应用于以下托管在 AWS 上的集群：

- 2025 年 4 月 1 日前创建的现有集群。
- 使用 TiDB 版本低于 v7.5.5、v8.1.2 或 v8.5.0 创建的新集群。

#### 标准存储

标准存储适用于大多数负载，在性能和成本之间实现平衡。与基础存储相比，标准存储为 Raft 日志预留了充足的磁盘资源，从而提升了性能。这样可以减少 Raft I/O 对数据盘 I/O 的影响，提高 TiKV 的读写性能。

标准存储类型会自动应用于使用 TiDB v7.5.5、v8.1.2、v8.5.0 或更高版本创建的新 AWS 集群。

#### 高性能与 Plus 存储

高性能与 Plus 存储提供更高的性能和稳定性，价格也相应更高。目前，这两种存储类型仅可按需为部署在 AWS 上的集群申请。如需申请高性能或 Plus 存储，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写 "Apply for TiKV storage type"，并点击 **Submit**。

## TiFlash 规模配置

TiFlash 实时同步 TiKV 的数据，开箱即用地支持实时分析型负载，并支持水平扩展。

你可以为 TiFlash 配置节点数量、vCPU 和内存，以及存储容量。

### TiFlash vCPU 和内存

支持的 vCPU 和内存规格如下：

- 8 vCPU, 64 GiB
- 16 vCPU, 128 GiB
- 32 vCPU, 128 GiB
- 32 vCPU, 256 GiB

注意，当 TiDB 或 TiKV 的 vCPU 和内存规格设置为 **4 vCPU, 16 GiB** 时，TiFlash 不可用。

### TiFlash 节点数量

TiDB Cloud 会将 TiFlash 节点均匀部署到一个区域内的不同可用区。建议你为每个 TiDB Cloud 集群至少配置两个 TiFlash 节点，并为生产环境中的数据创建至少两个副本以实现高可用。

TiFlash 节点的最小数量取决于特定表的 TiFlash 副本数：

TiFlash 节点最小数量：`min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

例如，如果你在 AWS 上为每个 TiFlash 节点配置 1024 GiB 存储，并为表 A 设置 2 个副本（压缩后大小为 800 GiB），为表 B 设置 1 个副本（压缩后大小为 100 GiB），则所需 TiFlash 节点数量如下：

TiFlash 节点最小数量：`min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlash 节点存储

不同 TiFlash vCPU 支持的节点存储容量如下：

| TiFlash vCPU | 最小节点存储 | 最大节点存储 | 默认节点存储 |
|:---------:|:------------:|:------------:|:------------:|
| 8 vCPU    | 200 GiB      | 4096 GiB     | 500 GiB      |
| 16 vCPU   | 200 GiB      | 4096 GiB     | 500 GiB      |
| 32 vCPU   | 200 GiB      | 8192 GiB     | 500 GiB      |

> **Note:**
>
> 集群创建后，TiFlash 节点存储容量无法减少。

### TiFlash 节点存储类型

TiDB Cloud 为托管在 AWS 上的 [TiDB Cloud 专属](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供以下 TiFlash 存储类型：

- [基础存储](#basic-storage-1)
- [Plus 存储](#plus-storage)

#### 基础存储

基础存储适用于大多数负载，在性能和成本之间实现平衡。

#### Plus 存储

Plus 存储提供更高的性能和稳定性，价格也相应更高。目前，该存储类型仅可按需为部署在 AWS 上的集群申请。如需申请，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写 "Apply for TiFlash storage type"，并点击 **Submit**。