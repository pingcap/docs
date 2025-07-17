---
title: TiDB 架构
summary: TiDB 平台的关键架构组件
---

# TiDB 架构

与传统的单机数据库相比，TiDB 具有以下优势：

* 具有分布式架构，具有灵活和弹性的扩展能力。
* 完全兼容 MySQL 协议、MySQL 的常用功能和语法。要将你的应用迁移到 TiDB，在大多数情况下无需修改一行代码。
* 支持高可用性，出现少数副本故障时自动故障转移；对应用透明。
* 支持 ACID 事务，适用于需要强一致性的场景，如银行转账。

<CustomContent platform="tidb">

* 提供丰富的 [数据迁移工具](/migration-overview.md)，用于迁移、复制或备份数据。

</CustomContent>

作为一个分布式数据库，TiDB 设计为由多个组件组成。这些组件相互通信，形成一个完整的 TiDB 系统。架构如下：

![TiDB 架构](/media/tidb-architecture-v6.png)

## TiDB 服务器

[TiDB 服务器](/tidb-computing.md) 是一个无状态的 SQL 层，向外部暴露 MySQL 协议的连接端点。TiDB 服务器接收 SQL 请求，进行 SQL 解析和优化，最终生成分布式执行计划。它具有水平扩展能力，并通过如 TiProxy、Linux Virtual Server (LVS)、HAProxy、ProxySQL 或 F5 等负载均衡组件向外提供统一接口。它不存储数据，仅用于计算和 SQL 分析，将实际的数据读取请求传递给 TiKV 节点（或 TiFlash 节点）。

## Placement Driver (PD) 服务器

[PD 服务器](/tidb-scheduling.md) 是整个集群的元数据管理组件。它存储每个 TiKV 节点的实时数据分布元数据和整个 TiDB 集群的拓扑结构，提供 TiDB Dashboard 管理界面，并为分布式事务分配事务 ID。PD 服务器是整个 TiDB 集群的“脑”，因为它不仅存储集群的元数据，还根据 TiKV 节点实时上报的数据分布状态，向特定的 TiKV 节点发送数据调度命令。此外，PD 服务器至少由三个节点组成，具有高可用性。建议部署奇数个 PD 节点。

## 存储服务器

### TiKV 服务器

[TiKV 服务器](/tidb-storage.md) 负责存储数据。TiKV 是一个分布式事务性键值存储引擎。

<CustomContent platform="tidb">

[Region](/glossary.md#regionpeerraft-group) 是存储数据的基本单元。每个 Region 存储特定 Key 范围内的数据，该范围为左闭右开的区间，从 StartKey 到 EndKey。

</CustomContent>

<CustomContent platform="tidb-cloud">

[Region](/tidb-cloud/tidb-cloud-glossary.md#region) 是存储数据的基本单元。每个 Region 存储特定 Key 范围内的数据，该范围为左闭右开的区间，从 StartKey 到 EndKey。

</CustomContent>

每个 TiKV 节点中存在多个 Region。TiKV API 原生支持在键值对层面进行分布式事务，并默认支持 Snapshot Isolation 级别的隔离。这是 TiDB 在 SQL 层支持分布式事务的核心。处理 SQL 语句后，TiDB 服务器会将 SQL 执行计划转换为对 TiKV API 的实际调用。因此，数据存储在 TiKV 中。TiKV 中的所有数据都会自动维护多份副本（默认为三份），因此 TiKV 具有原生的高可用性，并支持自动故障转移。

### TiFlash 服务器

[TiFlash 服务器](/tiflash/tiflash-overview.md) 是一种特殊类型的存储服务器。不同于普通的 TiKV 节点，TiFlash 以列存储数据，主要用于加速分析处理。