---
title: Recovery Group Overview (Beta)
summary: 了解如何通过 TiDB Cloud recovery group 保护你的数据库免受灾难影响。
---

# Recovery Group Overview (Beta)

TiDB Cloud recovery group 允许你在 TiDB Cloud Dedicated 集群之间复制数据库，以防范区域性灾难。你可以编排数据库从一个集群到另一个集群的故障切换。在故障切换到辅助集群后，如果原主集群重新可用，你可以反向重新建立复制，以重新保护你的数据库。

## 架构

一个 recovery group 由一组可以在两个 TiDB Cloud Dedicated 集群之间一起进行故障切换的复制数据库组成。每个 recovery group 都分配有一个主集群，主集群上的数据库会与该组关联，并被复制到辅助集群。

![Recovery Group](/media/tidb-cloud/recovery-group/recovery-group-overview.png)

- Recovery Group：在两个集群之间进行复制的一组数据库
- Primary Cluster：应用主动写入数据库的集群
- Secondary Cluster：数据库副本所在的集群

> **Note**
>
> Recovery Group 功能不会强制客户端连接到副本数据库时为只读。确保连接到副本数据库的应用只执行只读查询是应用自身的责任。

## 主要特性与限制

- 目前，仅托管在 AWS 上的 TiDB Cloud Dedicated 集群支持 recovery group。
- recovery group 是在两个集群之间建立的。
- recovery group 不支持数据库的双向复制。

> **Warning**
>
> 此功能处于 beta 阶段，不建议在生产环境中使用。

## 后续操作

- 若要开始使用 recovery group，请参见 [Create Database Recovery Group](/tidb-cloud/recovery-group-get-started.md)。
- 若要了解如何使用 recovery group，请参见 [Failover and Reprotect Databases](/tidb-cloud/recovery-group-failover.md)。