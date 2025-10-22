---
title: 什么是 TiDB Cloud
summary: 了解 TiDB Cloud 及其架构。
category: intro
---

# 什么是 TiDB Cloud

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 是一款全托管的数据库即服务（DBaaS），将 [TiDB](https://docs.pingcap.com/tidb/stable/overview) —— 一个开源的 HTAP（混合事务与分析处理）数据库 —— 带到你的云端。TiDB Cloud 提供了一种简单的方式来部署和管理数据库，让你专注于应用程序本身，而无需关注数据库的复杂性。<CustomContent language="en,zh">你可以在 Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云上创建 TiDB Cloud 集群，快速构建关键业务应用。</CustomContent><CustomContent language="ja">You can create TiDB Cloud clusters to quickly build mission-critical applications on Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.</CustomContent>

![TiDB Cloud 概览](/media/tidb-cloud/tidb-cloud-overview.png)

## 为什么选择 TiDB Cloud

TiDB Cloud 让你几乎无需培训即可轻松处理如基础设施管理和集群部署等复杂任务。

- 开发者和数据库管理员（DBA）可以轻松应对大量在线流量，并能快速分析跨多个数据集的大规模数据。

- 各类规模的企业都可以轻松部署和管理 TiDB Cloud，无需预付费用，灵活应对业务增长。

观看下方视频，进一步了解 TiDB Cloud：

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

使用 TiDB Cloud，你可以获得以下关键特性：

- **Fast and Customized Scaling**

    弹性且透明地扩展至数百个节点以应对关键负载，同时保持 ACID 事务。无需进行分片操作。你还可以根据业务需求分别扩展计算节点和存储节点。

- **MySQL Compatibility**

    借助 TiDB 的 MySQL 兼容性，提高开发效率并缩短应用上线时间。可以轻松地从现有 MySQL 实例迁移数据，无需重写代码。

- **High Availability and Reliability**

    天生高可用的架构设计。数据在多个可用区间进行复制，支持每日备份和自动故障转移，无论遇到硬件故障、网络分区还是数据中心丢失，都能保障业务连续性。

- **Real-Time Analytics**

    内置分析引擎，实时获取分析查询结果。TiDB Cloud 能在当前数据上运行一致性的分析查询，不会影响关键业务应用。

- **Enterprise Grade Security**

    在专用网络和专用机器上保护你的数据，支持传输加密和静态加密。TiDB Cloud 已通过 SOC 2 Type 2、ISO 27001:2013、ISO 27701 认证，并完全符合 GDPR 要求。

- **Fully-Managed Service**

    通过易用的 Web 管理平台，仅需几次点击即可部署、扩展、监控和管理 TiDB 集群。

- **Multi-Cloud Support**

    <CustomContent language="en,zh">

    保持灵活性，避免云厂商锁定。TiDB Cloud 目前支持 AWS、Azure、Google Cloud 和阿里云。

    </CustomContent>

    <CustomContent language="ja">

    Stay flexible without cloud vendor lock-in. TiDB Cloud is currently available on AWS, Azure, and Google Cloud.

    </CustomContent>

- **Simple Pricing Plans**

    只为实际使用的资源付费，价格透明，无隐藏费用。

- **World-Class Support**

    通过我们的支持门户、<a href="mailto:tidbcloud-support@pingcap.com">电子邮件</a>、聊天或视频会议，获得世界级的技术支持。

## 部署选项

TiDB Cloud 提供以下部署选项：

- TiDB Cloud Starter

    TiDB Cloud Starter 是一款全托管的多租户 TiDB 服务。它提供即时、自动扩缩容的 MySQL 兼容数据库，并在超出免费额度后按用量计费。

    <CustomContent language="en,zh">

    目前，TiDB Cloud Starter 已在 AWS 上正式发布，并在阿里云上公测。

    </CustomContent>

- TiDB Cloud Essential

    针对业务负载持续增长、需要实时扩展的应用，TiDB Cloud Essential 提供了灵活性和性能，助力你的业务持续发展。

    <CustomContent language="en,zh">

    目前，TiDB Cloud Essential 在 AWS 和阿里云上处于公测阶段。

    关于 TiDB Cloud Starter 与 TiDB Cloud Essential 在阿里云上的功能对比，详见 [TiDB on Alibaba Cloud](https://www.pingcap.com/partners/alibaba-cloud/)。

    </CustomContent>

    <CustomContent language="ja">

    Currently, TiDB Cloud Essential is in public preview on AWS.

    </CustomContent>

- TiDB Cloud Dedicated

    TiDB Cloud Dedicated 专为关键业务场景设计，支持跨多个可用区的高可用、横向扩展以及完整的 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 能力。

    目前，TiDB Cloud Dedicated 已在 AWS 和 Google Cloud 上正式发布，并在 Azure 上公测。更多信息请参见 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated)。

## 架构

![TiDB Cloud 架构](/media/tidb-cloud/tidb-cloud-architecture.png)

- TiDB VPC（虚拟私有云）

    对于每个 TiDB Cloud 集群，所有 TiDB 节点及辅助节点（包括 TiDB Operator 节点和日志节点）都部署在同一个 VPC 内。

- TiDB Cloud 中央服务

    中央服务（包括计费、告警、元数据存储、Dashboard UI 等）独立部署。你可以通过互联网访问 Dashboard UI 来操作 TiDB 集群。

- 你的 VPC

    你可以通过私有终端节点连接或 VPC 对等连接接入 TiDB 集群。详细信息请参见 [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md) 或 [Set up VPC Peering Connection](/tidb-cloud/set-up-vpc-peering-connections.md)。