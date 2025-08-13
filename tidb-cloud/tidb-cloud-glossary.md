---
title: TiDB Cloud 术语表
summary: 了解 TiDB Cloud 中使用的术语。
category: glossary
aliases: ['/tidbcloud/glossary']
---

# TiDB Cloud 术语表

## A

### ACID

ACID 指的是事务的四个关键特性：原子性（atomicity）、一致性（consistency）、隔离性（isolation）和持久性（durability）。每个特性如下所述。

- **原子性** 意味着一个操作的所有更改要么全部执行，要么全部不执行。TiDB 通过保证存储主键的 [TiDB Region](#region) 的原子性来实现事务的原子性。

- **一致性** 意味着事务总是将数据库从一个一致的状态带到另一个一致的状态。在 TiDB 中，数据在写入内存前会确保一致性。

- **隔离性** 意味着正在执行的事务在完成之前对其他事务是不可见的。这允许并发事务在不牺牲一致性的情况下读写数据。TiDB 目前支持 `REPEATABLE READ` 隔离级别。

- **持久性** 意味着一旦事务提交，即使系统发生故障也会保持提交状态。TiKV 通过持久化存储来保证持久性。

## C

### Chat2Query

Chat2Query 是集成在 SQL 编辑器中的一项 AI 驱动功能，能够帮助用户通过自然语言指令生成、调试或重写 SQL 查询。更多信息，参见 [使用 AI 辅助 SQL 编辑器探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

此外，TiDB Cloud 为 Serverless 集群提供了 Chat2Query API。启用后，TiDB Cloud 会自动创建一个名为 **Chat2Query** 的系统 Data App，并在 Data Service 中创建一个 Chat2Data 端点。你可以调用该端点，通过指令让 AI 生成并执行 SQL 语句。更多信息，参见 [开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

### Credit

TiDB Cloud 为概念验证（PoC）用户提供一定数量的 Credit。一个 Credit 等同于一美元。你可以在 Credit 过期前使用它们支付 TiDB 集群费用。

## D

### Data App

[Data Service (beta)](#data-service) 中的 Data App 是一组端点的集合，你可以用来访问特定应用的数据。你可以通过 API 密钥配置授权设置，限制对 Data App 中端点的访问。

更多信息，参见 [管理 Data App](/tidb-cloud/data-service-manage-data-app.md)。

### Data Service

Data Service（beta）允许你通过自定义 API [端点](#endpoint) 以 HTTPS 请求方式访问 TiDB Cloud 数据。该功能采用无服务器架构，自动处理计算资源和弹性扩缩容，因此你可以专注于端点中的查询逻辑，无需担心基础设施或运维成本。

更多信息，参见 [Data Service 概览](/tidb-cloud/data-service-overview.md)。

### Direct Customer

Direct Customer（直客）指的是直接从 PingCAP 购买 TiDB Cloud 并直接支付账单的最终客户。与 [MSP 客户](#msp-customer) 区分。

## E

### Endpoint

Data Service 中的端点是你可以自定义以执行 SQL 语句的 Web API。你可以为 SQL 语句指定参数，例如 `WHERE` 子句中使用的值。当客户端调用端点并在请求 URL 中提供参数值时，端点会使用这些参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

更多信息，参见 [管理端点](/tidb-cloud/data-service-manage-endpoint.md)。

## F

### 全文检索（Full-text search）

与关注语义相似度的 [向量检索](/vector-search/vector-search-overview.md) 不同，全文检索允许你通过精确关键词检索文档。在 RAG（Retrieval-Augmented Generation）场景下，你可以将全文检索与向量检索结合使用，以提升检索质量。

更多信息，参见 [使用 SQL 进行全文检索](/tidb-cloud/vector-search-full-text-search-sql.md) 和 [使用 Python 进行全文检索](/tidb-cloud/vector-search-full-text-search-python.md)。

## M

### member

被邀请加入某个组织的用户，拥有访问该组织及其集群的权限。

### MPP

自 v5.0 起，TiDB 通过 TiFlash 节点引入了大规模并行处理（Massively Parallel Processing，MPP）架构，将大型 Join 查询的执行负载分摊到多个 TiFlash 节点。当启用 MPP 模式时，TiDB 会根据成本判断是否使用 MPP 框架进行计算。在 MPP 模式下，Join 键会在计算过程中通过 Exchange 操作重新分布，将计算压力分散到每个 TiFlash 节点，从而加速计算。更多信息，参见 [使用 TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### MSP Customer

MSP 客户（Managed Service Provider Customer）指的是通过 MSP 渠道购买 TiDB Cloud 并通过 MSP 支付账单的最终客户。与 [直客](#direct-customer) 区分。

### Managed Service Provider (MSP)

MSP（托管服务提供商）是指转售 TiDB Cloud 并提供增值服务的合作伙伴，包括但不限于 TiDB Cloud 组织管理、计费服务和技术支持。

## N

### node

指数据实例（TiKV）、计算实例（TiDB）或分析实例（TiFlash）。

## O

### organization

你创建用于管理 TiDB Cloud 账户的实体，包括一个管理账户和任意数量的成员账户。

### organization members

组织成员是由组织所有者或项目所有者邀请加入组织的用户。组织成员可以查看组织成员，并可被邀请加入组织内的项目。

## P

### policy

定义适用于角色、用户或组织的权限的文档，例如对特定操作或资源的访问权限。

### project

基于组织创建的项目，可以按项目分别管理人员、实例、网络等资源，项目之间的资源互不干扰。

### project members

项目成员是被邀请加入组织中一个或多个项目的用户。项目成员可以管理集群、网络访问、备份等资源。

## R

### 回收站（Recycle Bin）

用于存放已删除且有有效备份的集群数据的地方。一旦已备份的 TiDB Cloud 专属集群被删除，该集群现有的备份文件会被移动到回收站。对于自动备份产生的备份文件，回收站会保留指定时间。你可以在 **Backup Setting** 中配置备份保留时间，默认是 7 天。对于手动备份产生的备份文件，则没有过期时间。为避免数据丢失，请及时将数据恢复到新集群。注意，如果集群 **没有备份**，则删除的集群不会显示在此处。

### region

- TiDB Cloud region

    TiDB Cloud 集群部署的地理区域。一个 TiDB Cloud region 至少包含 3 个可用区，集群会跨这些可用区部署。

- TiDB Region

    TiDB 中数据的基本单位。TiKV 将 Key-Value 空间划分为一系列连续的 Key 段，每个段称为一个 Region。每个 Region 的默认大小上限为 96 MB，可进行配置。

### replica

可以位于同一区域或不同区域的独立数据库，包含相同的数据。副本通常用于灾备或提升性能。

### Replication Capacity Unit

变更数据流（changefeed）的复制按计算资源计费，即 TiCDC 复制容量单位。

### Request Unit

Request Unit（RU）是用于表示单个数据库请求消耗资源量的计量单位。一个请求消耗的 RU 数量取决于多种因素，如操作类型或检索/修改的数据量。更多信息，参见 [TiDB Cloud Serverless 计费详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

## S

### Spending limit

Spending limit（消费上限）指的是你每月愿意为某个工作负载支付的最大金额。它是一种成本控制机制，可以让你为 TiDB Cloud Serverless 集群设置预算。对于 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)，消费上限至少需设置为 $0.01。此外，若可扩展集群符合条件，可享有免费额度，集群会优先消耗免费额度。

## T

### TiDB cluster

由 [TiDB](https://docs.pingcap.com/tidb/stable/tidb-computing)、[TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage)、[Placement Driver](https://docs.pingcap.com/tidb/stable/tidb-scheduling)（PD）和 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 节点组成的功能性数据库集群。

### TiDB node

聚合来自事务型或分析型存储查询结果的计算节点。增加 TiDB 节点数量可以提升集群可处理的并发查询数。

### TiFlash node

实时从 TiKV 复制数据并支持实时分析型负载的分析型存储节点。

### TiKV node

存储在线事务处理（OLTP）数据的存储节点。为高可用性，按 3 的倍数（如 3、6、9）扩容，其中两个节点作为副本。增加 TiKV 节点数量可以提升总吞吐量。

### traffic filter

允许通过 SQL 客户端访问 TiDB Cloud 集群的 IP 地址和无类别域间路由（CIDR）地址列表。默认情况下，traffic filter 为空。

## V

### 向量检索（Vector search）

[向量检索](/vector-search/vector-search-overview.md) 是一种以数据语义为核心、提供相关性结果的检索方式。与依赖精确关键词匹配和词频的传统全文检索不同，向量检索会将多种数据类型（如文本、图片或音频）转换为高维向量，并基于这些向量之间的相似度进行查询。这种检索方式能够捕捉数据的语义和上下文信息，更准确地理解用户意图。即使检索词与数据库内容不完全匹配，向量检索也能通过分析数据语义，返回符合用户意图的结果。

### Virtual Private Cloud

逻辑隔离的虚拟网络分区，为你的资源提供托管网络服务。

### VPC

Virtual Private Cloud 的缩写。

### VPC peering

允许你连接多个 Virtual Private Cloud（[VPC](#vpc)）网络，使不同 VPC 网络中的工作负载可以私有通信。

### VPC peering connection

两个 Virtual Private Cloud（VPC）之间的网络连接，使你可以通过私有 IP 地址在它们之间路由流量，便于数据传输。