---
title: TiDB Cloud 常见问题
summary: 了解与 TiDB Cloud 相关的最常见问题（FAQs）。
---

# TiDB Cloud 常见问题

<!-- markdownlint-disable MD026 -->

本文档列出了关于 TiDB Cloud 的最常见问题。

## 通用常见问题

### 什么是 TiDB Cloud？

TiDB Cloud 通过一个直观的控制台，让你能够更简单地部署、管理和维护 TiDB 集群，提供了完全托管的云实例。你可以轻松地在 Amazon Web Services (AWS)、Google Cloud 或 Microsoft Azure 上部署，以便快速构建关键业务应用。

TiDB Cloud 让开发者和 DBA 即使没有或几乎没有培训，也能轻松处理曾经复杂的任务，如基础设施管理和集群部署，从而专注于你的应用，而不是数据库的复杂性。通过一键横向扩展或缩容 TiDB 集群，你可以根据实际需求灵活配置数据库资源，避免资源浪费。

### TiDB 和 TiDB Cloud 之间是什么关系？

TiDB 是一个开源数据库，非常适合希望在自有数据中心、自管云环境或两者混合环境中运行 TiDB 自管版的组织。

TiDB Cloud 是 TiDB 的完全托管云数据库服务（Database as a Service）。它提供了易用的基于 Web 的管理控制台，帮助你管理关键生产环境下的 TiDB 集群。

### TiDB Cloud 兼容 MySQL 吗？

目前，TiDB Cloud 支持大部分 MySQL 5.7 和 MySQL 8.0 语法，但不支持触发器、存储过程和用户自定义函数。更多详情，参见 [与 MySQL 的兼容性](/mysql-compatibility.md)。

### 我可以用哪些编程语言操作 TiDB Cloud？

你可以使用任何被 MySQL 客户端或驱动支持的语言。

### 我可以在哪里运行 TiDB Cloud？

TiDB Cloud 目前可在 Amazon Web Services (AWS)、Google Cloud 和 Microsoft Azure 上使用。

### TiDB Cloud 支持不同云服务商之间的 VPC 对等连接吗？

不支持。

### TiDB Cloud 支持哪些 TiDB 版本？

- 对于新建的 TiDB Cloud 专属集群，自 2025 年 7 月 15 日起，默认 TiDB 版本为 [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2)。
- 对于 TiDB Cloud Serverless 集群，自 2025 年 4 月 22 日起，TiDB 版本为 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

更多信息，参见 [TiDB Cloud 发布说明](/tidb-cloud/tidb-cloud-release-notes.md)。

### 哪些公司在生产环境中使用 TiDB 或 TiDB Cloud？

TiDB 已被全球 1500 多家企业信赖，覆盖金融服务、游戏、电商等多个行业。我们的用户包括 Square（美国）、Shopee（新加坡）和中国银联（中国）。具体案例请参见我们的 [客户案例](https://www.pingcap.com/customers/)。

### SLA 是什么样的？

TiDB Cloud 提供 99.99% 的 SLA。详情参见 [TiDB Cloud 服务级别协议](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)。

### TiDB Cloud 中的 BETA 是什么意思？

BETA 是 TiDB Cloud 某项功能或服务在正式发布（GA）前的公开预览阶段。

### 如何进一步了解 TiDB Cloud？

了解 TiDB Cloud 的最佳方式是按照我们的分步教程操作。你可以从以下主题开始：

- [TiDB Cloud 简介](/tidb-cloud/tidb-cloud-intro.md)
- [快速入门](/tidb-cloud/tidb-cloud-quickstart.md)
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)

### 删除集群时，`XXX's Org/default project/Cluster0` 指的是什么？

在 TiDB Cloud 中，一个集群由组织名、项目名和集群名唯一标识。为了确保你删除的是目标集群，你需要提供该集群的全限定名称，例如 `XXX's Org/default project/Cluster0`。

## 架构常见问题

### 我的 TiDB 集群中有不同的组件。什么是 TiDB、TiKV 和 TiFlash 节点？

TiDB 是 SQL 计算层，用于聚合来自 TiKV 或 TiFlash 存储的查询数据。TiDB 支持水平扩展，增加 TiDB 节点数量可以提升集群的并发查询能力。

TiKV 是事务型存储，用于存储 OLTP 数据。TiKV 中的所有数据会自动维护多副本（默认三副本），因此 TiKV 天生具备高可用性并支持自动故障转移。TiKV 支持水平扩展，增加事务存储节点可以提升 OLTP 吞吐量。

TiFlash 是分析型存储，实时从事务存储（TiKV）同步数据，支持实时 OLAP 负载。与 TiKV 不同，TiFlash 以列存方式存储数据，加速分析型处理。TiFlash 也支持水平扩展，增加 TiFlash 节点可以提升 OLAP 存储和计算能力。

PD（Placement Driver）是整个 TiDB 集群的“大脑”，负责存储集群元数据。它根据 TiKV 节点实时上报的数据分布状态，向特定 TiKV 节点下发数据调度命令。在 TiDB Cloud 上，每个集群的 PD 由 PingCAP 统一管理，你无法直接查看或维护。

### TiDB 如何在 TiKV 节点之间复制数据？

TiKV 将键值空间划分为多个键区间，每个区间称为一个 “Region”。在 TiKV 中，数据以 Region 为基本单位分布在集群所有节点上。PD 负责将 Region 尽可能均匀地调度到集群所有节点。

TiDB 采用 Raft 共识算法，通过 Region 进行数据复制。存储在不同节点上的同一个 Region 的多个副本组成一个 Raft Group。

每次数据变更都会被记录为一条 Raft 日志。通过 Raft 日志复制，数据能够安全可靠地同步到 Raft Group 的多个节点。

## 高可用性常见问题

### TiDB Cloud 如何保证高可用性？

TiDB 采用 Raft 共识算法，确保数据在 Raft Group 内高度可用并安全复制。数据会在 TiKV 节点之间冗余复制，并分布在不同的可用区，以防止机器或数据中心故障。通过自动故障转移，TiDB 能确保你的服务始终可用。

作为 SaaS（软件即服务）提供商，我们高度重视数据安全。我们已建立了严格的信息安全政策和流程，符合 [SOC 2 Type 1 合规性](https://www.pingcap.com/press-release/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud/) 的要求。这确保了你的数据安全、可用且保密。

## 迁移常见问题

### 从其他关系型数据库迁移到 TiDB Cloud 是否有便捷路径？

TiDB 高度兼容 MySQL。你可以顺利地将数据从任何 MySQL 兼容数据库迁移到 TiDB，无论数据来自自建 MySQL 实例还是公有云提供的 RDS 服务。更多信息，参见 [使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 备份与恢复常见问题

### TiDB Cloud 支持增量备份吗？

不支持。如果你需要在集群备份保留期内恢复到任意时间点，可以使用 PITR（时间点恢复）。更多信息，参见 [在 TiDB Cloud 专属集群中使用 PITR](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup) 或 [在 TiDB Cloud Serverless 集群中使用 PITR](/tidb-cloud/backup-and-restore-serverless.md#restore)。

## HTAP 常见问题

### 如何利用 TiDB Cloud 的 HTAP 能力？

传统上，数据库分为联机事务处理（OLTP）和联机分析处理（OLAP）两类，OLTP 和 OLAP 请求通常在不同且隔离的数据库中处理。在这种架构下，将数据从 OLTP 数据库迁移到数据仓库或数据湖进行 OLAP 分析是一个漫长且易出错的过程。

作为混合事务与分析处理（HTAP）数据库，TiDB Cloud 通过在 OLTP（TiKV）存储和 OLAP（TiFlash）存储之间自动可靠地复制数据，帮助你简化系统架构，降低运维复杂度，并支持对事务数据的实时分析。典型 HTAP 场景包括用户个性化、AI 推荐、欺诈检测、商业智能和实时报表。

更多 HTAP 场景，参见 [我们如何构建简化数据平台的 HTAP 数据库](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform)。

### 我可以直接将数据导入 TiFlash 吗？

不可以。当你向 TiDB Cloud 导入数据时，数据会被导入到 TiKV。导入完成后，你可以通过 SQL 语句指定哪些表需要同步到 TiFlash。随后，TiDB 会在 TiFlash 中为指定表创建副本。更多信息，参见 [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)。

### 我可以将 TiFlash 数据导出为 CSV 格式吗？

不可以。TiFlash 数据无法导出。

## 安全性常见问题

### TiDB Cloud 安全吗？

在 TiDB Cloud 中，所有静态数据都经过加密，所有网络流量均通过传输层安全协议（TLS）加密。

- 静态数据加密通过加密存储卷自动完成。
- 客户端与集群之间的数据传输加密通过 TiDB Cloud Web 服务器 TLS 和 TiDB 集群 TLS 自动完成。

### TiDB Cloud 如何加密我的业务数据？

TiDB Cloud 默认对你的静态业务数据（包括数据库数据和备份数据）使用存储卷加密。TiDB Cloud 要求传输中的数据必须使用 TLS 加密，同时也要求数据库集群内部（TiDB、PD、TiKV、TiFlash 之间）进行组件级 TLS 加密。

如需获取 TiDB Cloud 业务数据加密的详细信息，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

### TiDB Cloud 支持哪些 TLS 版本？

TiDB Cloud 支持 TLS 1.2 或 TLS 1.3。

### 我可以在自己的 VPC 中运行 TiDB Cloud 吗？

不可以。TiDB Cloud 是数据库即服务（DBaaS），仅运行在 TiDB Cloud 的 VPC 中。作为云计算托管服务，TiDB Cloud 提供数据库访问，无需你搭建物理硬件和安装软件。

### 我的 TiDB 集群安全吗？

在 TiDB Cloud 中，你可以根据需求选择 TiDB Cloud 专属集群或 TiDB Cloud Serverless 集群。

对于 TiDB Cloud 专属集群，TiDB Cloud 通过以下措施保障集群安全：

- 为每个集群创建独立的子账号和 VPC。
- 设置防火墙规则，隔离外部连接。
- 为每个集群创建服务端 TLS 证书和组件级 TLS 证书，加密集群内传输数据。
- 为每个集群提供 IP 访问规则，确保只有允许的源 IP 地址可以访问你的集群。

对于 TiDB Cloud Serverless 集群，TiDB Cloud 通过以下措施保障集群安全：

- 为每个集群创建独立的子账号。
- 设置防火墙规则，隔离外部连接。
- 提供集群服务端 TLS 证书，加密集群内传输数据。

### 如何连接 TiDB 集群中的数据库？

<SimpleTab>
<div label="TiDB Cloud Dedicated">

对于 TiDB Cloud 专属集群，连接集群的步骤简化如下：

1. 授权你的网络。
2. 设置数据库用户和登录凭证。
3. 下载并配置集群服务器的 TLS。
4. 选择 SQL 客户端，在 TiDB Cloud UI 上获取自动生成的连接字符串，然后通过该字符串在 SQL 客户端中连接集群。

更多信息，参见 [连接到你的 TiDB Cloud 专属集群](/tidb-cloud/connect-to-tidb-cluster.md)。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，连接集群的步骤简化如下：

1. 设置数据库用户和登录凭证。
2. 选择 SQL 客户端，在 TiDB Cloud UI 上获取自动生成的连接字符串，然后通过该字符串在 SQL 客户端中连接集群。

更多信息，参见 [连接到你的 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。

</div>
</SimpleTab>

## 支持常见问题

### 客户可以获得哪些支持？

TiDB Cloud 由 TiDB 背后的同一团队提供支持，该团队已为全球 1500 多家企业的关键业务场景提供服务，覆盖金融服务、电商、企业应用和游戏等行业。TiDB Cloud 为每位用户提供免费基础支持计划，你也可以升级为付费计划以获得更全面的服务。更多信息，参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

### 如何检查 TiDB Cloud 是否宕机？

你可以在 [系统状态](https://status.tidbcloud.com/) 页面查看 TiDB Cloud 当前的运行状态。