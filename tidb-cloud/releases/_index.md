---
title: TiDB Cloud 发布记录
summary: 了解 TiDB Cloud 的发布说明、内核版本和维护通知。
---

# TiDB Cloud 发布记录

[TiDB Cloud](https://www.pingcap.com/tidb/cloud/) 是一款全托管的数据库即服务（DBaaS），将开源的 HTAP (Hybrid Transactional and Analytical Processing) 数据库 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 部署到云端。

TiDB Cloud 提供两类发布：[云平台发布](#cloud-platform-release-notes) 和 [数据库内核发布](#database-kernel-release-notes)。它们遵循各自独立的发布周期，并分别记录。

## 云平台发布说明

云平台发布涵盖 TiDB Cloud 控制台、API 和控制平面，包括适用于所有 TiDB Cloud 方案的新功能、UI 变更、集成和运维改进。

- [TiDB Cloud 发布说明](/tidb-cloud/releases/tidb-cloud-release-notes.md)

## 数据库内核发布说明

数据库内核是处理 SQL 查询和管理数据的核心引擎。根据你的 TiDB Cloud 方案，你的资源运行在不同的内核上，每种内核都有各自的发布节奏。

| 方案 | 内核信息和发布说明 |
| --- | --- |
| TiDB Cloud **Starter** | 运行在基于经典 [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) 内核定制的 [TiDB X](/tidb-cloud/tidb-x-architecture.md) 引擎上。 |
| TiDB Cloud **Essential** | 默认运行在基于经典 [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) 内核定制的 [TiDB X](/tidb-cloud/tidb-x-architecture.md) 引擎上。 |
| TiDB Cloud **Premium** | 运行在 [TiDB X](/tidb-cloud/tidb-x-architecture.md) 内核的 [`TiDB-X-CLOUD.202510.1`](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) 版本上。 |
| TiDB Cloud **Dedicated** | 运行在经典 TiDB 内核上，其内核版本与 TiDB Self-Managed 版本直接对应。目前，新创建的 TiDB Cloud Dedicated 集群默认 TiDB 版本为 [v8.5.7](https://docs.pingcap.com/tidb/stable/release-8.5.7/)。 |

> **注意：**
>
> 如果你希望 TiDB Cloud Essential 实例运行在与 TiDB Cloud Premium 相同的内核上，请联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

## 维护通知

TiDB Cloud 维护通知提供有关计划维护活动的信息，这些维护活动可能会对你的 TiDB Cloud 服务产生影响。通知列表请参阅左侧导航栏。
