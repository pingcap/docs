---
title: TiDB Cloud 术语表
summary: 了解 TiDB Cloud 中使用的术语。
category: glossary
aliases: ['/tidbcloud/glossary']
---

# TiDB Cloud 术语表

## A

### ACID

ACID 指的是事务的四个关键属性：原子性（atomicity）、一致性（consistency）、隔离性（isolation）和持久性（durability）。每个属性的说明如下：

- **原子性** 意味着一个操作的所有更改要么全部完成，要么全部不做。TiDB 通过保证存储主键的 [TiDB Region](#region) 的原子性来实现事务的原子性。

- **一致性** 意味着事务总是将数据库从一个一致的状态带到另一个一致的状态。在 TiDB 中，数据在写入内存前会确保一致性。

- **隔离性** 意味着正在进行的事务对其他事务是不可见的，直到其完成。这允许并发事务在不牺牲一致性的情况下读写数据。TiDB 当前支持 `REPEATABLE READ` 隔离级别。

- **持久性** 意味着一旦事务提交，即使系统故障也会保持提交状态。TiKV 使用持久化存储来保证持久性。

## C

### Chat2Query

Chat2Query 是集成在 SQL Editor 中的 AI 驱动功能，帮助用户通过自然语言指令生成、调试或重写 SQL 查询。更多信息，参见 [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md)。

此外，TiDB Cloud 为托管在 AWS 上的 TiDB Cloud Starter 实例提供 Chat2Query API。启用后，TiDB Cloud 会自动创建一个名为 **Chat2Query** 的系统 Data App，并在 Data Service 中创建一个 Chat2Data endpoint。你可以调用该 endpoint，通过指令让 AI 生成并执行 SQL 语句。更多信息，参见 [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

### Cluster

在 TiDB Cloud 中，cluster 是一种专用云部署，包含明确的基础设施细节，例如节点拓扑、实例类型、存储配置和扩缩容模型。

在 TiDB Cloud 的各类套餐中，只有 TiDB Cloud Dedicated 集群使用这种部署模型。

### Credit

TiDB Cloud 为概念验证（PoC）用户提供一定数量的 credit。1 个 credit 等同于 1 美元。你可以在 credit 过期前使用它们支付费用。

## D

### Data App

[Data Service (beta)](#data-service) 中的 Data App 是一组 endpoint 的集合，你可以用来为特定应用访问数据。你可以通过 API key 配置授权设置，限制对 Data App 中 endpoint 的访问。

更多信息，参见 [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md)。

### Data Service

Data Service（beta）允许你通过自定义 API [endpoint](#endpoint) 以 HTTPS 请求方式访问 TiDB Cloud 数据。该功能采用无服务器架构，自动处理计算资源和弹性扩缩容，因此你可以专注于 endpoint 中的查询逻辑，无需担心基础设施或运维成本。

更多信息，参见 [Data Service Overview](/tidb-cloud/data-service-overview.md)。

### Direct Customer

Direct customer 指直接从 PingCAP 购买 TiDB Cloud 并直接支付账单的终端客户。与 [MSP customer](#msp-customer) 区分。

## E

### Endpoint

Data Service 中的 endpoint 是你可以自定义的 Web API，用于执行 SQL 语句。你可以为 SQL 语句指定参数，例如 `WHERE` 子句中使用的值。当 client 调用 endpoint 并在请求 URL 中提供参数值时，endpoint 会用这些参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

更多信息，参见 [Manage an endpoint](/tidb-cloud/data-service-manage-endpoint.md)。

## F

### Full-text search

与关注语义相似度的 [Vector Search](/ai/concepts/vector-search-overview.md) 不同，全文检索允许你通过精确关键字检索文档。在 RAG（Retrieval-Augmented Generation）场景中，你可以将全文检索与向量检索结合使用，以提升检索质量。

更多信息，参见 [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md) 和 [Full-Text Search with Python](/ai/guides/vector-search-full-text-search-python.md)。

## M

### member

被邀请加入 TiDB Cloud 中某个 [organization](#organization) 的用户。

### MPP

自 v5.0 起，TiDB 通过 TiFlash 节点引入了大规模并行处理（MPP）架构，将大型 join 查询的执行负载分摊到多个 TiFlash 节点。当启用 MPP 模式时，TiDB 会根据成本决定是否使用 MPP framework 进行计算。在 MPP 模式下，join key 会在计算过程中通过 Exchange 操作重新分布，将计算压力分散到每个 TiFlash 节点，从而加速计算。更多信息，参见 [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md)。

### MSP Customer

MSP customer（托管服务提供商客户）指通过 MSP 渠道购买 TiDB Cloud 并支付账单的终端客户。与 [direct customer](#direct-customer) 区分。

### Managed Service Provider (MSP)

托管服务提供商（MSP）是 TiDB Cloud 的合作伙伴，负责转售 TiDB Cloud 并提供增值服务，包括但不限于 TiDB Cloud organization 管理、计费服务和技术支持。

## N

### node

指数据实例（TiKV）、计算实例（TiDB）或分析实例（TiFlash）。

## O

### organization

TiDB Cloud 中用于管理账户（包括一个管理账户和任意数量的成员账户）、[project](#project) 和 [resource](#tidb-cloud-resource) 的顶层容器。

### organization members

organization members 是由 organization owner 或 project owner 邀请加入 organization 的用户。organization members 可以查看 organization 的成员，并可被邀请加入 organization 下的项目。

## P

### policy

定义应用于角色、用户或 organization 的权限的文档，例如对特定操作或资源的访问权限。

### project

在 TiDB Cloud 中，你可以使用 project 对 TiDB 资源进行分组和管理。

- 对于 TiDB X 实例（包括 {{{ .starter }}}、Essential 和 Premium 实例），project 是可选的，这意味着你既可以将这些实例归入某个 project，也可以将这些实例保留在 organization 层级。
- 对于 {{{ .dedicated }}} 集群，project 是必需的。

project 的功能因 project 类型而异。目前共有三种类型的 project：

- **TiDB Dedicated project**：此类 project 仅用于 {{{ .dedicated }}} 集群。它帮助你按 project 分别管理 {{{ .dedicated }}} 集群的设置，例如 RBAC、网络、维护、告警订阅和加密访问。
- **TiDB X project**：此类 project 仅用于 TiDB X 实例。它帮助你按 project 管理 TiDB X 实例的 RBAC。TiDB X project 是你在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面创建 project 时的默认 project 类型。
- **TiDB X virtual project**：此类 project 是虚拟的，不提供任何管理能力。它作为不属于任何 project 的 TiDB X 实例的虚拟容器，使这些实例能够通过使用 project ID 的 TiDB Cloud API 进行访问。每个 organization 都有一个唯一的 virtual project ID。你可以通过 TiDB Cloud API 的 [List all accessible projects](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project/operation/ListProjects) 端点获取此 ID。

有关这些 project 类型之间差异的更多信息，参见 [Projects](/tidb-cloud/manage-user-access.md#projects)。

### project members

project members 是被邀请加入 organization 下一个或多个 project 的用户。

## R

### Recycle Bin

用于存放已删除且有有效备份的 [TiDB Cloud resource](#tidb-cloud-resource) 数据的地方。

一旦已备份的 TiDB Cloud resource 被删除，其现有的备份文件会被移动到 Recycle Bin。对于自动备份产生的备份文件，Recycle Bin 会保留指定时间。你可以在 **Backup Setting** 中配置备份保留时间，默认是 7 天。对于手动备份产生的备份文件，则没有过期时间。为避免数据丢失，请及时将数据恢复到新的 TiDB Cloud resource。注意，如果 TiDB Cloud resource **没有备份**，则不会在 Recycle Bin 中显示已删除的 resource。

目前，只有 {{{ .premium }}} 实例和 {{{ .dedicated }}} 集群支持 Recycle Bin 功能。

### region

- TiDB Cloud region

    TiDB Cloud resource 部署的地理区域。一个 TiDB Cloud region 至少包含 3 个可用区，集群或实例会跨这些可用区部署。

- TiDB Region

    TiDB 中数据的基本单元。TiKV 将 Key-Value 空间划分为一系列连续的 Key 段，每个段称为 Region。每个 Region 的默认大小上限为 96 MB，可配置。

### replica

可以位于同一 region 或不同 region 的独立数据库，包含相同数据。replica 通常用于容灾或提升性能。

### Replication Capacity Unit (RCU)

TiDB Cloud 以 TiCDC Replication Capacity Unit（RCU）衡量 [changefeeds](/tidb-cloud/changefeed-overview.md) 的容量。创建 changefeed 时，你可以选择合适的规格。RCU 越高，replication 性能越好。你需要为这些 TiCDC changefeed RCU 付费。更多信息，参见 [Changefeed Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost)。

### Request Capacity Unit (RCU)

对于 {{{ .essential }}} 和 {{{ .premium }}}，Request Capacity Unit（RCU）是用于表示 {{{ .essential }}} 或 {{{ .premium }}} 实例预配置计算能力的单位。1 个 RCU 提供固定数量的计算资源，可处理一定数量的 RU 每秒。你预配置的 RCU 数量决定了实例的基线性能和吞吐能力。不过，{{{ .essential }}} 和 {{{ .premium }}} 的 RCU 管理方式有所不同：

- {{{ .essential }}} 会根据你的工作负载自动预配置 RCU。随着 QPS 增加，TiDB Cloud 会动态扩容已预配置的 RCU 以维持性能。更多信息，参见 [{{{ .essential }}} Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)。
- {{{ .premium }}} 允许你为工作负载指定最大 RCU 数量（`RCU_max`）。TiDB Cloud 会根据实时需求，在 `0.25 * RCU_max` 到 `RCU_max` 的范围内自动扩缩容。更多信息，参见 [{{{ .premium }}} 中的请求单位与容量](/tidb-cloud/architecture-concepts.md#request-units-and-capacity-in-premium)。

### Request Unit (RU)

对于 {{{ .starter }}}、Essential 和 Premium，Request Unit（RU）是用于表示单个请求消耗资源量的单位。一个请求消耗的 RU 数量取决于多种因素，如操作类型和检索或修改的数据量。但这些套餐的计费模式不同：

- {{{ .starter }}} 按消耗的 RU 总数计费。更多信息，参见 [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。
- {{{ .essential }}} 按预配置的 [Request Capacity Unit (RCU)](#request-capacity-unit-rcu) 数量计费。1 个 RCU 提供固定数量的计算资源，可处理一定数量的每秒 RU。更多信息，参见 [{{{ .essential }}} Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)。
- {{{ .premium }}} 按工作负载实际消耗的 Request Capacity Unit（RCU）计费。TiDB Cloud 会每分钟计算一次平均每秒 RU，并将该平均值用作计费的 [Request Capacity Units (RCUs)](#request-capacity-unit-rcu)。更多信息，参见 [{{{ .premium }}} 中的请求单位与容量](/tidb-cloud/architecture-concepts.md#request-units-and-capacity-in-premium)。

对于 TiDB Cloud Dedicated 和 TiDB Self-Managed，Request Unit（RU）是表示系统资源消耗的抽象单位，目前包括 CPU、IOPS 和 IO 带宽等指标。它被资源控制功能用于限制、隔离和管理数据库请求消耗的资源，**不用于计费**。更多信息，参见 [Use Resource Control to Achieve Resource Group Limitation and Flow Control](/tidb-resource-control-ru-groups.md)。

## S

### Spending limit

[Spending limit](/tidb-cloud/manage-serverless-spend-limit.md) 指你每月愿意为某个 workload 支付的最大金额。它是一种成本控制机制，使你可以为 TiDB Cloud Starter 实例设置预算。如果 spending limit 设置为 0，TiDB Cloud Starter 实例保持免费；如果大于 0，则需要添加信用卡。

## T

### TiDB cluster

在 TiDB Cloud 中，cluster 是 TiDB 的一种专用云部署，包含明确的基础设施细节，例如节点拓扑（你可以指定 [TiDB](/tidb-computing.md) 节点、[TiKV](/tidb-storage.md) 节点和 [TiFlash](/tiflash/tiflash-overview.md) 节点的数量）、存储配置和扩缩容模型。

### TiDB node

聚合来自事务型或分析型存储查询结果的计算节点。增加 TiDB node 数量可以提升 {{{ .dedicated }}} 集群可处理的并发查询数。

### TiDB Cloud resource

TiDB Cloud resource 是可管理的 TiDB Cloud 部署单元。它可以是以下之一：

- TiDB X 实例（一种基于 [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md) 构建的面向服务的 TiDB Cloud 产品），例如 {{{ .starter }}}、Essential 或 Premium 实例
- {{{ .dedicated }}} 集群

### TiDB X

一种全新的分布式 SQL 架构，将云原生对象存储作为 TiDB 的核心。通过计算与存储解耦，TiDB X 使 TiDB 能够智能扩展，实时适应 workload 模式、业务周期和数据特性。

TiDB X 架构现已在 {{{ .starter }}}、Essential 和 Premium 中提供。更多信息，参见 [Introducing TiDB X: A New Foundation for Distributed SQL in the Era of AI](https://www.pingcap.com/blog/introducing-tidb-x-a-new-foundation-distributed-sql-ai-era/) 和 [PingCAP Launches TiDB X and New AI Capabilities at SCaiLE Summit 2025](https://www.pingcap.com/press-release/pingcap-launches-tidb-x-new-ai-capabilities/)。

### TiDB X instance

TiDB X instance 是一种基于 [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md) 构建的面向服务的 TiDB Cloud 产品。它不需要你管理或了解底层集群拓扑。

在 TiDB Cloud 的各类套餐中，{{{ .starter }}}、Essential 和 Premium 使用 TiDB X architecture。因此，当提到 “TiDB X instance” 时，它指的是 {{{ .starter }}}、Essential 或 Premium 实例。

### TiFlash node

实时从 TiKV 复制数据并支持实时分析 workload 的分析型存储节点。

### TiKV node

存储在线事务处理（OLTP）数据的存储节点。以 3 的倍数（如 3、6、9）扩展以实现高可用，其中两个节点作为副本。增加 TiKV node 数量可以提升总吞吐量。

### traffic filter

允许通过 SQL client 访问 TiDB Cloud resource 的 IP 地址和 CIDR 地址列表。traffic filter 默认为空。

## V

### Vector search

[Vector search](/ai/concepts/vector-search-overview.md) 是一种以数据语义为核心、提供相关性结果的检索方法。与依赖精确关键字匹配和词频的传统全文检索不同，vector search 会将多种数据类型（如文本、图片或音频）转换为高维向量，并基于这些向量间的相似度进行查询。该方法能够捕捉数据的语义和上下文信息，更准确理解用户意图。即使检索词与数据库内容不完全匹配，vector search 也能通过分析数据语义，返回符合用户意图的结果。

### Virtual Private Cloud

逻辑隔离的虚拟网络分区，为你的资源提供托管网络服务。

### VPC

Virtual Private Cloud 的缩写。

### VPC peering

允许你连接 Virtual Private Cloud（[VPC](#vpc)）网络，使不同 VPC 网络中的 workload 能够私有通信。

### VPC peering connection

两个 Virtual Private Cloud（VPC）之间的网络连接，使你可以通过私有 IP 地址在它们之间路由流量，便于数据传输。
