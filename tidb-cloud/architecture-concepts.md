---
title: 架构
summary: 了解 TiDB Cloud 的架构概念。
---

# 架构

TiDB Cloud 是一款全托管的数据库即服务（DBaaS），将 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 的灵活性与强大功能带到 AWS、Azure 和 Google Cloud。TiDB 是一款开源的 HTAP（混合事务与分析处理）数据库。

TiDB 兼容 MySQL，便于迁移和对接现有应用，同时具备无缝扩展能力，能够应对从小型负载到大规模高性能集群的各种需求。它在同一系统中同时支持事务型（OLTP）和分析型（OLAP）负载，简化运维并实现实时洞察。

TiDB Cloud 提供两种部署选项：**TiDB Cloud** **Serverless**，适用于自动弹性伸缩、成本高效的负载；以及 **TiDB Cloud Dedicated**，为企业级应用提供专属资源和高级能力。TiDB Cloud 让你轻松扩展数据库，处理复杂的管理任务，专注于开发可靠且高性能的应用。

## TiDB Cloud Serverless

TiDB Cloud Serverless 是一款全托管的无服务器解决方案，提供与传统 TiDB 类似的 HTAP 能力，并通过自动弹性伸缩，减轻用户在容量规划和管理复杂性方面的负担。它包含一个免费额度，超出免费额度的部分按用量计费。TiDB Cloud Serverless 提供两种高可用性选项，以满足不同的运维需求。

默认情况下，选择 Zonal High Availability 选项的集群，其所有组件都位于同一个可用区内，从而带来更低的网络延迟。

![TiDB Cloud Serverless zonal high availability](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

对于需要最大基础设施隔离和冗余的应用，可以选择 Regional High Availability 选项，将节点分布在多个可用区。

![TiDB Cloud Serverless regional high availability](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 专为关键业务场景设计，提供跨多个可用区的高可用性、水平扩展能力以及完整的 HTAP 能力。

该方案基于隔离的云资源（如 VPC、VM、托管 Kubernetes 服务和云存储）构建，充分利用主流云服务商的基础设施。TiDB Cloud Dedicated 集群支持完整的 TiDB 功能集，实现快速扩容、可靠备份、在指定 VPC 内部署以及地理级别的灾备能力。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud 控制台

[TiDB Cloud 控制台](https://tidbcloud.com/) 是 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 的基于 Web 的管理界面。你可以通过该平台管理集群、导入或迁移数据、监控性能指标、配置备份、设置安全控制，并与其他云服务集成，所有操作均可在一个用户友好的平台上完成。

## TiDB Cloud CLI（Beta）

TiDB Cloud CLI，即 `ticloud`，允许你通过简单命令在终端直接管理 TiDB Cloud Serverless 和 TiDB Cloud Dedicated。你可以执行如下任务：

- 创建、删除和列出集群
- 向集群导入数据
- 从集群导出数据

更多信息，请参见 [TiDB Cloud CLI Reference](/tidb-cloud/cli-reference.md)。

## TiDB Cloud API（Beta）

TiDB Cloud API 是基于 REST 的接口，提供对 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 资源的编程访问能力。它支持自动化、高效地处理项目、集群、备份、恢复、数据导入、计费以及 [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md) 中的其他资源管理任务。

更多信息，请参见 [TiDB Cloud API Overview](/tidb-cloud/api-overview.md)。

## 节点

在 TiDB Cloud 中，每个集群由 TiDB、TiKV 和 TiFlash 节点组成。

- 在 TiDB Cloud Dedicated 集群中，你可以根据性能需求，完全管理专属 TiDB、TiKV 和 TiFlash 节点的数量和规格。更多信息，请参见 [Scalability](/tidb-cloud/scalability-concepts.md)。
- 在 TiDB Cloud Serverless 集群中，TiDB、TiKV 和 TiFlash 节点的数量和规格由系统自动管理，实现无缝扩展，无需用户手动配置或管理节点。

### TiDB 节点

[TiDB 节点](/tidb-computing.md) 是无状态的 SQL 层，通过兼容 MySQL 的端点与应用连接。它负责解析、优化 SQL 查询，并生成分布式执行计划。

你可以部署多个 TiDB 节点以实现水平扩展，满足更高的负载需求。这些节点通常与负载均衡器（如 TiProxy 或 HAProxy）配合使用，提供无缝的访问接口。TiDB 节点本身不存储数据——它们会将数据请求转发给 TiKV 节点（行存储）或 TiFlash 节点（列存储）。

### TiKV 节点

[TiKV 节点](/tikv-overview.md) 是 TiDB 架构中数据存储的核心，作为分布式事务型键值存储引擎，具备高可靠性、可扩展性和高可用性。

**主要特性：**

- **基于 Region 的数据存储**

    - 数据被划分为多个 [Region](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)，每个 Region 覆盖特定的 Key Range（左闭右开区间：`StartKey` 到 `EndKey`）。
    - 每个 TiKV 节点内可包含多个 Region，以实现高效的数据分布。

- **事务支持**

    - TiKV 节点在键值层面原生支持分布式事务，默认隔离级别为快照隔离（Snapshot Isolation）。
    - TiDB 节点会将 SQL 执行计划转换为对 TiKV 节点 API 的调用，从而实现无缝的 SQL 级事务支持。

- **高可用性**

    - TiKV 节点中的所有数据都会进行副本复制（默认三副本），以保证数据持久性。
    - TiKV 原生支持高可用和自动故障转移，保障节点故障时的数据安全。

- **可扩展性与可靠性**

    - TiKV 节点设计用于处理不断扩展的数据集，同时保持分布式一致性和容错能力。

### TiFlash 节点

[TiFlash 节点](/tiflash/tiflash-overview.md) 是 TiDB 架构中的一种专用存储节点。与普通 TiKV 节点不同，TiFlash 采用列式存储模型，专为分析加速设计。

**主要特性：**

- **列式存储**

    TiFlash 节点以列式格式存储数据，针对分析型查询进行了优化，大幅提升了读密集型负载的性能。

- **向量检索索引支持**

    向量检索索引功能利用表的 TiFlash 副本，实现高级检索能力，并提升复杂分析场景下的效率。