---
title: TiDB Cloud 高可用
summary: 了解 TiDB Cloud 的高可用架构。探索分区高可用与区域高可用选项、自动备份、故障转移流程，以及 TiDB 如何确保数据持久性和业务可持续性。
---

# TiDB Cloud 高可用

TiDB Cloud 通过强大的机制，默认保障高可用和数据持久性，防止单点故障，并确保即使在发生中断时也能持续提供 service。作为基于经过实战检验的 TiDB 开源产品的全托管 service，TiDB Cloud 继承了 TiDB 的核心高可用（HA）特性，并结合了额外的云原生能力。

> **注意：**
>
> - 本文档仅适用于 <CustomContent plan="starter,essential">TiDB Cloud Starter 和 TiDB Cloud Essential</CustomContent><CustomContent plan="premium">TiDB Cloud Starter、TiDB Cloud Essential 和 TiDB Cloud Premium</CustomContent>。
> - 关于 TiDB Cloud Dedicated 的高可用，请参见 [TiDB Cloud Dedicated 高可用](/tidb-cloud/high-availability-with-multi-az.md)。

## 概述

TiDB 通过 Raft 一致性算法保障高可用和数据持久性。该算法会持续地在多个 node 之间复制数据修改，使 TiDB 即使在 node 故障或网络分区时也能处理读写 request。这种方式同时提供了高数据持久性和容错能力。

TiDB Cloud 在此基础上，扩展了分区高可用和区域高可用能力，以满足不同的运维需求。

<CustomContent plan="starter,essential">

> **注意：**
>
> - 对于 TiDB Cloud Starter cluster，仅启用分区高可用，且不可配置。
> - 对于部署在 AWS 东京（ap-northeast-1）Region 或任意阿里云 Region 的 TiDB Cloud Essential cluster，默认启用区域高可用。你可以在创建 cluster 时根据需要切换为分区高可用。对于部署在其他 Region 的 TiDB Cloud Essential cluster，仅启用分区高可用，且不可配置。

</CustomContent>

<CustomContent plan="premium">

> **注意：**
>
> - 对于 TiDB Cloud Starter cluster，仅启用分区高可用，且不可配置。
> - 对于 TiDB Cloud Premium cluster，仅启用区域高可用，且不可配置。
> - 对于部署在 AWS 东京（ap-northeast-1）Region 或任意阿里云 Region 的 TiDB Cloud Essential cluster，默认启用区域高可用。你可以在创建 cluster 时根据需要切换为分区高可用。对于部署在其他 Region 的 TiDB Cloud Essential cluster，仅启用分区高可用，且不可配置。

</CustomContent>

- **分区高可用**：该选项将所有 node 部署在同一可用区内，降低网络延时。它无需在应用层实现跨区冗余即可保障高可用，适用于对单区低延时有较高要求的应用。详细信息参见 [分区高可用架构](#zonal-high-availability-architecture)。

- **区域高可用（beta）**：该选项将 node 分布在多个可用区，实现最大程度的基础设施隔离和冗余。它提供最高级别的可用性，但需要应用层实现跨区冗余。如果你需要最大程度防护单区基础设施故障，建议选择该选项。需要注意的是，该模式会增加延时，并可能产生跨区数据传输费用。该功能仅在拥有三个及以上可用区的 Region 可用，且只能在 cluster 创建时启用。详细信息参见 [区域高可用架构](#regional-high-availability-architecture)。

## 分区高可用架构

当你以默认分区高可用创建 cluster 时，所有组件（包括 Gateway、TiDB、TiKV 和 TiFlash 计算/写 node）均运行在同一可用区内。数据面组件的部署通过虚拟机池提供基础设施冗余，从而最大程度减少故障转移时间和因同区部署带来的网络延时。

<CustomContent language="en,zh">

- 下图展示了 AWS 上分区高可用的架构：

    ![zonal high availability on AWS](/media/tidb-cloud/zonal-high-avaliability-aws.png)

- 下图展示了阿里云上分区高可用的架构：

    ![zonal high availability on Alibaba Cloud](/media/tidb-cloud/zonal-high-avaliability-alibaba-cloud.png)

</CustomContent>

<CustomContent language="ja">

下图展示了 AWS 上分区高可用的架构：

![zonal high availability on AWS](/media/tidb-cloud/zonal-high-avaliability-aws.png)

</CustomContent>

在分区高可用架构下：

- Placement Driver（PD）跨多个可用区部署，通过跨区冗余复制数据保障高可用。
- 数据在本地可用区内的 TiKV server 和 TiFlash 写 node 之间复制。
- TiDB server 和 TiFlash 计算 node 负责从 TiKV 和 TiFlash 写 node 读写数据，这些 node 通过存储层复制机制保障数据安全。

### 故障转移流程

TiDB Cloud 为你的应用保障透明的故障转移流程。在故障转移期间：

<CustomContent language="en,zh">

- 会创建新的副本以替换故障副本。

- 提供存储 service 的 server 会从 Amazon S3 或阿里云 OSS（取决于你的云服务商）持久化数据中恢复本地 cache，将系统恢复到与副本一致的状态。

在存储层，持久化数据会定期 push 到 Amazon S3 或阿里云 OSS（取决于你的云服务商），以实现高持久性。此外，实时 update 不仅会在多个 TiKV server 之间复制，还会存储在每台 server 的 EBS 上，EBS 也会进一步复制数据以增强持久性。TiDB 会自动在毫秒级别进行退避和重试，确保故障转移过程对 client 应用无感。

</CustomContent>

<CustomContent language="ja">

- 会创建新的副本以替换故障副本。

- 提供存储 service 的 server 会从 Amazon S3（取决于你的云服务商）持久化数据中恢复本地 cache，将系统恢复到与副本一致的状态。

在存储层，持久化数据会定期 push 到 Amazon S3，以实现高持久性。此外，实时 update 不仅会在多个 TiKV server 之间复制，还会存储在每台 server 的 EBS 上，EBS 也会进一步复制数据以增强持久性。TiDB 会自动在毫秒级别进行退避和重试，确保故障转移过程对 client 应用无感。

</CustomContent>

Gateway 和计算层为无状态的，因此故障转移时会立即在其他位置重启。应用应实现连接的重试 logic。分区高可用虽然能提供高可用，但无法应对整个可用区故障。如果可用区不可用，将会发生停机，直到该区及其依赖的 service 恢复。

## 区域高可用架构

当你以区域高可用创建 cluster 时，关键 OLTP（联机事务处理）负载组件（如 PD 和 TiKV）会跨多个可用区部署，以实现冗余复制并最大化可用性。正常运行时，Gateway、TiDB 和 TiFlash 计算/写 node 等组件部署在主可用区。数据面组件通过虚拟机池提供基础设施冗余，从而最大程度减少故障转移时间和因同区部署带来的网络延时。

> **注意：**
>
> 区域高可用目前为 beta 版本。

<CustomContent language="en,zh">

- 下图展示了 AWS 上区域高可用的架构：

    ![regional high availability on AWS](/media/tidb-cloud/regional-high-avaliability-aws.png)

- 下图展示了阿里云上区域高可用的架构：

    ![regional high availability on Alibaba Cloud](/media/tidb-cloud/regional-high-avaliability-alibaba-cloud.png)

</CustomContent>

<CustomContent language="ja">

下图展示了 AWS 上区域高可用的架构：

![regional high availability](/media/tidb-cloud/regional-high-avaliability-aws.png)

</CustomContent>

在区域高可用架构下：

- Placement Driver（PD）和 TiKV 跨多个可用区部署，数据始终在各区冗余复制，以确保最高级别的可用性。
- 数据在主可用区内的 TiFlash 写 node 之间复制。
- TiDB server 和 TiFlash 计算 node 负责从这些 TiKV 和 TiFlash 写 node 读写数据，这些 node 通过存储层复制机制保障数据安全。

### 故障转移流程

在极少数主可用区故障的场景下（可能由自然灾害、配置变更、软件问题或硬件故障引起），关键 OLTP 负载组件（包括 Gateway 和 TiDB）会自动在备用可用区启动。流量会自动切换到备用区，以确保快速恢复并保障业务可持续性。

TiDB Cloud 通过以下措施，最大程度减少主可用区故障时的 service 中断，并保障业务可持续性：

- 自动在备用可用区创建新的 Gateway 和 TiDB 副本。
- 通过弹性负载均衡器检测备用可用区的活跃 Gateway 副本，并将 OLTP 流量从故障主区重定向到备用区。

除了通过 TiKV 复制提供高可用外，TiKV 实例还会部署并配置为将每个数据副本放置在不同的可用区。只要有两个可用区正常运行，系统就能保持可用。为实现高持久性，数据会定期备份到 S3。即使两个可用区同时故障，存储在 S3 的数据依然可访问和恢复。

应用不会受到非主可用区故障的影响，也不会感知到此类事件。在主可用区故障时，Gateway 和 TiDB 会在备用可用区启动以处理负载。请确保你的应用实现重试 logic，将新 request 重定向到备用可用区的活跃 server。

## 自动备份与持久性

数据库备份对于业务可持续性和容灾至关重要，有助于防止数据损坏或误删。通过备份，你可以在保留时间内将数据库恢复到任意时间点，最大程度减少数据丢失和停机时间。

TiDB Cloud 提供强大的自动备份机制，持续保护你的数据：

- **每日全量备份**：每天对数据库进行一次全量备份，捕获数据库的完整状态。
- **持续事务日志备份**：事务日志会持续备份，约每 5 分钟一次，具体频率取决于数据库活动量。

这些自动备份机制支持你通过全量备份或结合全量备份与持续事务日志，将数据库恢复到任意时间点。这种灵活性确保你可以将数据库恢复到事故发生前的精确时刻。

<CustomContent language="en,zh">

> **注意：**
>
> 自动备份（包括基于快照的备份和用于时间点恢复（PITR）的持续备份）会存储在 Amazon S3 或阿里云 OSS（取决于你的云服务商），具备区域级高持久性。

</CustomContent>

<CustomContent language="ja">

> **注意：**
>
> 自动备份（包括基于快照的备份和用于时间点恢复（PITR）的持续备份）会存储在 Amazon S3，具备区域级高持久性。

</CustomContent>

## 故障期间对会话的影响

在故障期间，正在故障 server 上运行的事务可能会被中断。虽然故障转移对应用是透明的，但你必须实现相应 logic 以处理活跃事务中的可恢复故障。不同故障场景的处理方式如下：

- **TiDB 故障**：如果 TiDB 实例故障，client 连接不会受影响，因为 TiDB Cloud 会自动通过 Gateway 重定向流量。虽然故障 TiDB 实例上的事务可能会中断，但系统会确保已提交数据被保留，新事务会由其他可用 TiDB 实例处理。
- **Gateway 故障**：如果 Gateway 故障，client 连接会被中断。但 TiDB Cloud 的 Gateway 为无状态的，可以立即在新可用区或 server 上重启。流量会自动重定向到新的 Gateway，最大程度减少停机时间。

建议你在应用中实现重试 logic，以处理可恢复故障。具体实现方式请参考你的驱动或 ORM 文档（例如 [JDBC](https://dev.mysql.com/doc/connector-j/en/connector-j-config-failover.html)）。

## RTO 和 RPO

在制定业务可持续性计划时，请重点关注以下两个关键指标：

- 恢复时间目标（RTO）：应用在发生中断事件后，完全恢复所能容忍的最长时间。
- 恢复点目标（RPO）：应用在从非计划中断事件恢复时，所能容忍的最近数据 update 的最长时间间隔。

下表对比了不同高可用选项的 RTO 和 RPO：

| 高可用架构 | RTO（停机时间）                | RPO（数据丢失） |
|--------------------------------|-------------------------------|-----------------|
| 分区高可用                         | 近 0 秒                      | 0               |
| 区域高可用                        | 通常小于 600 秒 | 0               |