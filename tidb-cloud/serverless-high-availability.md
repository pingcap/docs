---
title: TiDB Cloud Starter 和 Essential 的高可用性
summary: 了解 TiDB Cloud Starter 和 Essential 的高可用性架构。探索可用区级和区域级高可用性选项、自动备份、故障转移流程，以及 TiDB 如何确保数据持久性和业务连续性。
---

# TiDB Cloud Starter 和 Essential 的高可用性

TiDB Cloud 默认设计了强大的机制来保持高可用性和数据持久性，防止单点故障，并确保即使在发生中断时也能持续提供服务。作为基于经过实战验证的 TiDB 开源产品的全托管服务，TiDB Cloud 继承了 TiDB 的核心高可用（HA）特性，并通过云原生能力进行了增强。

## 概述

TiDB 通过 Raft 一致性算法确保高可用性和数据持久性。该算法会将数据变更一致地复制到多个节点，即使在节点故障或网络分区的情况下，TiDB 也能处理读写请求。这种方式既保证了数据的高持久性，也具备容错能力。

TiDB Cloud 通过可用区级高可用性和区域级高可用性扩展了这些能力，以满足不同的运维需求。

> **Note:**
>
> - 对于 TiDB Cloud Starter 集群，仅启用可用区级高可用性，且不可配置。
> - 对于 TiDB Cloud Essential 集群，默认启用区域级高可用性，你可以在集群创建时根据需要切换为可用区级高可用性。

- **可用区级高可用性**：该选项将所有节点部署在同一个可用区内，从而降低网络延迟。它无需应用层跨区冗余即可实现高可用性，适用于优先考虑单区低延迟的应用。更多信息，参见 [可用区级高可用性架构](#zonal-high-availability-architecture)。

- **区域级高可用性（测试版）**：该选项将节点分布在多个可用区，实现最大程度的基础设施隔离和冗余。它提供最高级别的可用性，但需要应用层实现跨区冗余。如果你需要最大程度防护可用区级基础设施故障，建议选择该选项。需要注意的是，该选项会增加延迟，并可能产生跨区数据传输费用。此功能仅在拥有三个以上可用区的区域可用，并且只能在集群创建时启用。更多信息，参见 [区域级高可用性架构](#regional-high-availability-architecture)。

## 可用区级高可用性架构

当你以默认的可用区级高可用性创建集群时，所有组件，包括 Gateway、TiDB、TiKV 和 TiFlash 计算/写入节点，都会运行在同一个可用区内。这些组件在数据平面上的部署通过虚拟机池提供基础设施冗余，从而最大程度减少故障转移时间和由于同地部署带来的网络延迟。

<CustomContent language="en,zh">

- 下图展示了 AWS 上的可用区级高可用性架构：

    ![zonal high availability on AWS](/media/tidb-cloud/zonal-high-avaliability-aws.png)

- 下图展示了阿里云上的可用区级高可用性架构：

    ![zonal high availability on Alibaba Cloud](/media/tidb-cloud/zonal-high-avaliability-alibaba-cloud.png)

</CustomContent>

<CustomContent language="ja">

The following diagram shows the architecture of zonal high availability on AWS:

![zonal high availability on AWS](/media/tidb-cloud/zonal-high-avaliability-aws.png)

</CustomContent>

在可用区级高可用性架构中：

- Placement Driver（PD）部署在多个可用区，实现跨区冗余复制以确保高可用性。
- 数据会在本地可用区内的 TiKV 服务器和 TiFlash 写入节点之间进行复制。
- TiDB 服务器和 TiFlash 计算节点从 TiKV 和 TiFlash 写入节点进行读写，这些节点通过存储级别的复制机制得到保障。

### 故障转移流程

TiDB Cloud 为你的应用确保了透明的故障转移流程。在故障转移期间：

<CustomContent language="en,zh">

- 会创建一个新的副本来替换故障副本。

- 提供存储服务的服务器会从 Amazon S3 或阿里云 OSS（取决于你的云服务商）持久化的数据中恢复本地缓存，使系统与副本保持一致状态。

在存储层，持久化数据会定期推送到 Amazon S3 或阿里云 OSS（取决于你的云服务商），以实现高持久性。此外，实时更新不仅会在多个 TiKV 服务器之间复制，还会存储在每台服务器的 EBS 上，EBS 进一步复制数据以增强持久性。TiDB 会在毫秒级自动通过退避和重试机制解决问题，确保故障转移过程对客户端应用无感知。

</CustomContent>

<CustomContent language="ja">

- A new replica is created to replace the failed one.

- Servers providing storage services recover local caches from persisted data on Amazon S3 (depending on your cloud provider), restoring the system to a consistent state with the replicas.

In the storage layer, persisted data is regularly pushed to Amazon S3 for high durability. Moreover, immediate updates are not only replicated across multiple TiKV servers but also stored on the EBS of each server, which further replicates the data for additional durability. TiDB automatically resolves issues by backing off and retrying in milliseconds, ensuring the failover process remains seamless for client applications.

</CustomContent>

Gateway 和计算层是无状态的，因此故障转移只需立即在其他地方重启即可。应用应实现连接的重试逻辑。虽然可用区级部署提供了高可用性，但无法应对整个可用区的故障。如果可用区不可用，将会发生停机，直到该可用区及其依赖服务恢复。

## 区域级高可用性架构

当你以区域级高可用性创建集群时，关键的 OLTP（联机事务处理）工作负载组件，如 PD 和 TiKV，会部署在多个可用区，实现冗余复制并最大化可用性。在正常运行期间，Gateway、TiDB 和 TiFlash 计算/写入节点等组件会部署在主可用区。这些数据平面组件通过虚拟机池提供基础设施冗余，从而最大程度减少故障转移时间和由于同地部署带来的网络延迟。

> **Note:**
>
> - 区域级高可用性目前为测试版。
> - 区域级高可用性为默认启用，你可以在创建 TiDB Cloud Essential 集群时根据需要切换为可用区级高可用性。

<CustomContent language="en,zh">

下图展示了阿里云上的区域级高可用性架构：

![regional high availability](/media/tidb-cloud/regional-high-avaliability-alibaba-cloud.png)

在区域级高可用性架构中：

- Placement Driver（PD）和 TiKV 部署在多个可用区，数据始终跨区冗余复制，以确保最高级别的可用性。
- 数据会在主可用区内的 TiFlash 写入节点之间进行复制。
- TiDB 服务器和 TiFlash 计算节点从这些 TiKV 和 TiFlash 写入节点进行读写，这些节点通过存储级别的复制机制得到保障。

</CustomContent>

### 故障转移流程

在极少数情况下，主可用区发生故障（可能由自然灾害、配置变更、软件问题或硬件故障引起），关键的 OLTP 工作负载组件（包括 Gateway 和 TiDB）会自动在备用可用区启动。流量会自动重定向到备用可用区，以确保快速恢复并保持业务连续性。

TiDB Cloud 通过以下措施最大程度减少主可用区故障期间的服务中断，并确保业务连续性：

- 在备用可用区自动创建 Gateway 和 TiDB 的新副本。
- 通过弹性负载均衡器检测备用可用区的活跃 Gateway 副本，并将 OLTP 流量从故障主可用区重定向到备用可用区。

除了通过 TiKV 复制提供高可用性外，TiKV 实例还会部署并配置为将每个数据副本放置在不同的可用区。只要有两个可用区正常运行，系统就能保持可用性。为实现高持久性，数据会定期备份到 S3，即使有两个可用区故障，存储在 S3 上的数据依然可访问和恢复。

应用不会受到非主可用区故障的影响，也不会感知到此类事件。在主可用区故障期间，Gateway 和 TiDB 会在备用可用区启动以处理工作负载。请确保你的应用实现重试逻辑，将新请求重定向到备用可用区的活跃服务器。

## 自动备份与持久性

数据库备份对于业务连续性和灾难恢复至关重要，有助于防止数据损坏或意外删除。通过备份，你可以在保留期内将数据库恢复到某一时间点，最大程度减少数据丢失和停机时间。

TiDB Cloud 提供了强大的自动备份机制，确保持续的数据保护：

- **每日全量备份**：每天会创建一次数据库的全量备份，捕获整个数据库的状态。
- **持续事务日志备份**：事务日志会持续备份，大约每 5 分钟一次，具体频率取决于数据库活动量。

这些自动备份使你可以通过全量备份或结合全量备份与持续事务日志，将数据库恢复到某一特定时间点。这种灵活性确保你可以将数据库恢复到事故发生前的精确时间点。

<CustomContent language="en,zh">

> **Note:**
>
> 自动备份（包括基于快照的备份和用于时间点恢复（PITR）的持续备份）会在 Amazon S3 或阿里云 OSS（取决于你的云服务商）上执行，具备区域级高持久性。

</CustomContent>

<CustomContent language="ja">

> **Note:**
>
> Automatic backups, including snapshot-based and continuous backups for Point-in-Time Recovery (PITR), are performed on Amazon S3, which provides regional-level high durability.

</CustomContent>

## 故障期间对会话的影响

在发生故障时，故障服务器上的进行中事务可能会被中断。虽然故障转移对应用是透明的，但你必须实现逻辑来处理活动事务中的可恢复故障。不同的故障场景处理方式如下：

- **TiDB 故障**：如果某个 TiDB 实例故障，客户端连接不会受到影响，因为 TiDB Cloud 会自动通过 Gateway 重路由流量。虽然故障 TiDB 实例上的事务可能会被中断，但系统会确保已提交的数据被保留，新事务会由其他可用的 TiDB 实例处理。
- **Gateway 故障**：如果 Gateway 故障，客户端连接会被中断。但 TiDB Cloud 的 Gateway 是无状态的，可以立即在新的可用区或服务器上重启。流量会自动重定向到新的 Gateway，最大程度减少停机时间。

建议在你的应用中实现重试逻辑以处理可恢复故障。具体实现细节请参考你的驱动或 ORM 文档（例如 [JDBC](https://dev.mysql.com/doc/connector-j/en/connector-j-config-failover.html)）。

## RTO 和 RPO

在制定业务连续性计划时，需要考虑以下两个关键指标：

- 恢复时间目标（RTO）：应用在发生中断事件后完全恢复所能接受的最长时间。
- 恢复点目标（RPO）：在从计划外中断事件中恢复时，应用可容忍丢失的最近数据更新的最长时间间隔。

下表对比了每种高可用性选项的 RTO 和 RPO：

| 高可用性架构 | RTO（停机时间）                | RPO（数据丢失） |
|--------------------------------|-------------------------------|-----------------|
| 可用区级高可用性                         | 近 0 秒                      | 0               |
| 区域级高可用性                      | 通常小于 600 秒 | 0               |