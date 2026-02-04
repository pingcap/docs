---
title: TiDB 架构
summary: TiDB 平台的关键架构组件
---

# TiDB 架构

<CustomContent platform="tidb-cloud">

TiDB 提供两种架构：经典 TiDB 架构和 [TiDB X 架构](/tidb-cloud/tidb-x-architecture.md)。本文介绍经典 TiDB 架构。

</CustomContent>

与传统的单机数据库相比，TiDB 具有以下优势：

* 拥有分布式架构，具备灵活和弹性的扩展性。
* 完全兼容 MySQL 协议、MySQL 的常用特性和语法。在许多情况下，应用迁移到 TiDB 无需修改一行代码。
* 支持高可用，当少数副本故障时可自动故障转移，对应用透明。
* 支持 ACID 事务，适用于如银行转账等需要强一致性的场景。

<CustomContent platform="tidb">

* 提供丰富的 [数据迁移工具](/migration-overview.md) 用于数据迁移、同步或备份。

</CustomContent>

作为分布式数据库，TiDB 由多个组件组成。这些组件之间相互通信，形成完整的 TiDB 系统。架构如下所示：

![TiDB Architecture](/media/tidb-architecture-v6.png)

## TiDB server

[TiDB server](/tidb-computing.md) 是无状态的 SQL 层，向外暴露 MySQL 协议的连接端点。TiDB server 接收 SQL 请求，进行 SQL 解析和优化，最终生成分布式执行计划。它支持水平扩展，并通过 TiProxy、Linux Virtual Server (LVS)、HAProxy、ProxySQL 或 F5 等负载均衡组件对外提供统一接口。TiDB server 不存储数据，仅用于计算和 SQL 分析，将实际的数据读请求转发到 TiKV 节点（或 TiFlash 节点）。

## Placement Driver (PD) server

[PD server](/tidb-scheduling.md) 是整个集群的元信息管理组件。它存储每个 TiKV 节点的实时数据分布元信息和整个 TiDB 集群的拓扑结构，提供 TiDB Dashboard 管理界面，并为分布式事务分配事务 ID。PD server 是整个 TiDB 集群的“大脑”，不仅存储集群的元信息，还会根据 TiKV 节点实时上报的数据分布状态，向特定 TiKV 节点发送数据调度命令。此外，PD server 至少由三个节点组成，具备高可用性。建议部署奇数个 PD 节点。

## 存储服务器

### TiKV server

[TiKV server](/tidb-storage.md) 负责存储数据。TiKV 是分布式事务型键值存储引擎。

<CustomContent platform="tidb">

[Region](/glossary.md#regionpeerraft-group) 是存储数据的基本单元。每个 Region 存储特定 Key Range 的数据，该范围是一个左闭右开的区间，从 StartKey 到 EndKey。

</CustomContent>

<CustomContent platform="tidb-cloud">

[Region](/tidb-cloud/tidb-cloud-glossary.md#region) 是存储数据的基本单元。每个 Region 存储特定 Key Range 的数据，该范围是一个左闭右开的区间，从 StartKey 到 EndKey。

</CustomContent>

每个 TiKV 节点中存在多个 Region。TiKV API 在键值对层面原生支持分布式事务，并默认支持 Snapshot Isolation 级别的隔离。这是 TiDB 在 SQL 层支持分布式事务的核心。TiDB server 在处理 SQL 语句后，会将 SQL 执行计划转化为对 TiKV API 的实际调用。因此，数据存储在 TiKV 中。TiKV 中的所有数据会自动维护多副本（默认三副本），因此 TiKV 原生具备高可用性，并支持自动故障转移。

### TiFlash server

[TiFlash server](/tiflash/tiflash-overview.md) 是一种特殊类型的存储服务器。与普通 TiKV 节点不同，TiFlash 以列存方式存储数据，主要用于加速分析型处理。