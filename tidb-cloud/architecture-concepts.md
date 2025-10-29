---
title: 架构
summary: 了解 TiDB Cloud 的架构概念。
---

# 架构

<CustomContent language="en,zh">

TiDB Cloud 是一款全托管的数据库即服务（DBaaS），将 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 的灵活性与强大功能带到 Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云。TiDB 是一款开源的 HTAP（混合事务与分析处理）数据库。

</CustomContent>

<CustomContent language="ja">

TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings the flexibility and power of [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source HTAP (Hybrid Transactional and Analytical Processing) database, to Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.

</CustomContent>

TiDB 兼容 MySQL，使得迁移和对接现有应用变得简单，同时具备无缝扩展能力，能够从小型负载到大规模高性能集群灵活应对。它在同一系统中同时支持事务型（OLTP）和分析型（OLAP）负载，简化运维并实现实时洞察。

TiDB Cloud 让你轻松扩展数据库，处理复杂的管理任务，专注于开发可靠且高性能的应用。

<CustomContent language="en,zh">

- 在 AWS 上，TiDB Cloud 提供 **TiDB Cloud Starter**，适用于自动扩缩、成本高效的工作负载，**TiDB Cloud Essential**，适用于具备预配置容量的生产级工作负载，以及 **TiDB Cloud Dedicated**，适用于企业级应用，具备专属资源和高级能力。
- 在 Google Cloud 和 Azure 上，TiDB Cloud 提供 **TiDB Cloud Dedicated**，适用于企业级应用，具备专属资源和高级能力。
- 在阿里云上，TiDB Cloud 提供 **TiDB Cloud Starter**，适用于自动扩缩、成本高效的工作负载，以及 **TiDB Cloud Essential**，适用于具备预配置容量的生产级工作负载。

</CustomContent>

<CustomContent language="ja">

- For AWS, TiDB Cloud provides **TiDB Cloud Starter** for auto-scaling, cost-efficient workloads, **TiDB Cloud Essential** for production-ready workloads with provisioned capacity, and **TiDB Cloud Dedicated** for enterprise-grade applications with dedicated resources and advanced capabilities.
- For Google Cloud and Azure, TiDB Cloud provides **TiDB Cloud Dedicated** for enterprise-grade applications with dedicated resources and advanced capabilities.

</CustomContent>

## TiDB Cloud Starter

TiDB Cloud Starter 是一款全托管的多租户 TiDB 服务，提供即开即用、自动扩缩的 MySQL 兼容数据库。

Starter 集群方案非常适合刚开始使用 TiDB Cloud 的用户。它为开发者和小型团队提供以下特性：

- **免费**：该方案完全免费，无需信用卡即可开始使用。
- **存储**：提供初始 5 GiB 的行存储和 5 GiB 的列存储。
- **请求单元**：包含 5000 万 [请求单元（RUs）](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 用于数据库操作。

## TiDB Cloud Essential

对于负载持续增长、需要实时扩展的应用，Essential 集群方案提供灵活性和性能，助力你的业务持续发展，具备以下特性：

- **增强能力**：包含 Starter 方案的全部能力，并具备处理更大、更复杂负载的能力，以及高级安全特性。
- **自动扩缩**：自动调整存储和计算资源，高效应对不断变化的负载需求。
- **高可用性**：内置容错和冗余机制，即使在基础设施故障时，也能确保你的应用持续可用且具备弹性。
- **可预测的定价**：根据存储和计算资源的请求容量单元（RCUs）计费，提供透明、按用量计费的定价模式，随需扩展，让你只为实际使用的资源付费，无额外意外支出。

TiDB Cloud Essential 提供两种高可用性选项，以满足不同的运维需求。

- 默认情况下，采用分区高可用（Zonal High Availability）选项的集群，其所有组件都位于同一可用区，带来更低的网络延迟。
- 对于需要最大基础设施隔离和冗余的应用，可以选择区域高可用（Regional High Availability）选项，将节点分布在多个可用区。

更多信息，参见 [TiDB Cloud Starter 和 Essential 的高可用性](/tidb-cloud/serverless-high-availability.md)。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 专为关键业务场景设计，提供跨多个可用区的高可用性、水平扩展能力和完整的 HTAP 能力。

该方案基于隔离的云资源（如 VPC、VM、托管 Kubernetes 服务和云存储）构建，充分利用主流云服务商的基础设施。TiDB Cloud Dedicated 集群支持完整的 TiDB 功能集，实现快速扩展、可靠备份、在指定 VPC 内部署以及地理级别的灾备能力。

![TiDB Cloud Dedicated 架构](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud 控制台

[TiDB Cloud 控制台](https://tidbcloud.com/) 是 TiDB Cloud 集群的基于 Web 的管理界面。你可以通过该平台管理集群、导入或迁移数据、监控性能指标、配置备份、设置安全控制，并与其他云服务集成，所有操作均可在一个用户友好的平台上完成。

## TiDB Cloud CLI（Beta）

TiDB Cloud CLI，即 `ticloud`，允许你通过简单命令在终端直接管理 TiDB Cloud 集群。你可以执行如下任务：

- 创建、删除和列出集群。
- 向集群导入数据。
- 从集群导出数据。

更多信息，参见 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## TiDB Cloud API（Beta）

TiDB Cloud API 是基于 REST 的接口，提供对 TiDB Cloud Starter 和 TiDB Cloud Dedicated 资源的编程化管理。它支持自动化、高效地处理项目、集群、备份、恢复、数据导入、计费以及 [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md) 中的其他资源管理任务。

更多信息，参见 [TiDB Cloud API 概览](/tidb-cloud/api-overview.md)。

## 节点

在 TiDB Cloud 中，每个集群由 TiDB、TiKV 和 TiFlash 节点组成。

- 在 TiDB Cloud Dedicated 集群中，你可以根据性能需求完全自主管理专属 TiDB、TiKV 和 TiFlash 节点的数量和规格。更多信息，参见 [可扩展性](/tidb-cloud/scalability-concepts.md)。
- 在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群中，TiDB、TiKV 和 TiFlash 节点的数量和规格由系统自动管理，确保无缝扩展，无需用户手动配置或管理节点。

### TiDB 节点

[TiDB 节点](/tidb-computing.md) 是无状态的 SQL 层，通过 MySQL 兼容的端点与应用连接。它负责解析、优化 SQL 查询，并生成分布式执行计划。

你可以部署多个 TiDB 节点以实现水平扩展，承载更高的负载。这些节点通常与负载均衡器（如 TiProxy 或 HAProxy）配合使用，提供无缝的访问接口。TiDB 节点本身不存储数据——它们会将数据请求转发给 TiKV 节点（行存储）或 TiFlash 节点（列存储）。

### TiKV 节点

[TiKV 节点](/tikv-overview.md) 是 TiDB 架构中数据存储的核心，作为分布式事务型键值存储引擎，具备高可靠性、可扩展性和高可用性。

**主要特性：**

- **基于 Region 的数据存储**

    - 数据被划分为多个 [Region](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)，每个 Region 覆盖特定的 Key Range（左闭右开区间：`StartKey` 到 `EndKey`）。
    - 每个 TiKV 节点内可包含多个 Region，实现高效的数据分布。

- **事务支持**

    - TiKV 节点在键值层面原生支持分布式事务，默认隔离级别为快照隔离（Snapshot Isolation）。
    - TiDB 节点将 SQL 执行计划转化为对 TiKV 节点 API 的调用，实现无缝的 SQL 级事务支持。

- **高可用性**

    - TiKV 节点中的所有数据都会被复制（默认三副本），以保证数据持久性。
    - TiKV 原生支持高可用和自动故障转移，防止节点故障带来的影响。

- **可扩展性与可靠性**

    - TiKV 节点设计用于应对不断扩展的数据集，同时保持分布式一致性和容错能力。

### TiFlash 节点

[TiFlash 节点](/tiflash/tiflash-overview.md) 是 TiDB 架构中的一种专用存储节点。与普通 TiKV 节点不同，TiFlash 采用列式存储模型，专为分析加速设计。

**主要特性：**

- **列式存储**

    TiFlash 节点以列式格式存储数据，针对分析型查询进行了优化，大幅提升了读密集型负载的性能。

- **向量检索索引支持**

    向量检索索引功能利用表的 TiFlash 副本，实现高级检索能力，并提升复杂分析场景下的效率。