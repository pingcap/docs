---
title: 可扩展性
summary: 了解 TiDB Cloud 的可扩展性相关概念。
---

# 可扩展性

TiDB Cloud 提供多种部署选项，具备灵活的可扩展性，以满足不同工作负载的需求。

- [Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 非常适合原型开发、开发环境和早期阶段的工作负载。它为你提供了一种简化且具性价比的方式来快速上手 TiDB Cloud，并内置了自动扩缩容功能。
- [Essential](/tidb-cloud/select-cluster-tier.md#essential) 适用于需要更强可扩展性和在流量或数据量增长时具备可预测性能的生产级工作负载。
- TiDB Cloud Dedicated 支持分别调整计算和存储资源，以适应数据量或工作负载的变化。TiDB Cloud Dedicated 可以在不中断服务的情况下进行扩缩容。这种灵活性使组织能够在保持高性能和高可用性的同时，优化基础设施成本。

> **Tip:**
>
> 关于如何确定 TiDB Cloud Dedicated 集群的规模，请参见 [Determine Your TiDB Size](/tidb-cloud/size-your-cluster.md)。

## 垂直与水平扩展

TiDB Cloud Dedicated 支持垂直扩展（scale up）和水平扩展（scale out）。

- 水平扩展是指向你的专用集群中添加节点，以分担工作负载。
- 垂直扩展是指为你的专用集群增加 vCPU 和内存（RAM）。

在 TiDB Cloud Dedicated 中，也支持垂直扩展和水平扩展的组合使用。

## TiDB 可扩展性

TiDB 仅负责计算，不存储数据。你可以为 TiDB 配置节点数量、vCPU 和内存（RAM）。

通常情况下，TiDB 的性能会随着 TiDB 节点数量的增加而线性提升。

## TiKV 可扩展性

TiKV 负责存储行存数据。你可以为 TiKV 配置节点数量、vCPU、内存（RAM）和存储空间。TiKV 节点数量至少为 1 组（3 个节点，分布在 3 个不同的可用区），并以 3 个节点为单位进行扩展。

TiDB Cloud 会将 TiKV 节点均匀部署在你选择的区域内的 3 个可用区，以实现数据的持久性和高可用性。在典型的 3 副本部署中，你的数据会在所有可用区的 TiKV 节点之间均匀分布，并持久化到每个 TiKV 节点的磁盘上。虽然 TiKV 主要用于数据存储，但 TiKV 节点的性能也会根据不同的工作负载有所变化。

## TiFlash 可扩展性

TiFlash 负责存储列存数据。TiFlash 能够实时从 TiKV 同步数据，并原生支持实时分析型工作负载。你可以为 TiFlash 配置节点数量、vCPU、内存（RAM）和存储空间。

TiDB Cloud 会将 TiFlash 节点均匀部署在一个区域内的不同可用区。建议你在每个 TiDB Cloud 集群中至少配置 2 个 TiFlash 节点，并为数据创建至少 2 个副本，以确保生产环境下的高可用性。