---
title: 什么是 TiDB Cloud
summary: 了解 TiDB Cloud 及其架构。
category: intro
---

# 什么是 TiDB Cloud

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 是一款完全托管的云原生数据库即服务（DBaaS），基于 [TiDB](https://docs.pingcap.com/tidb/stable/overview) —— 一个开源 HTAP (Hybrid Transactional and Analytical Processing) 数据库。TiDB Cloud 提供了一种简单的方式来部署和管理数据库，让你专注于应用程序开发，而无需关注数据库的复杂性。<CustomContent language="en,zh">你可以在 Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云上创建 TiDB Cloud 集群，快速构建关键业务应用。</CustomContent><CustomContent language="ja">You can create TiDB Cloud clusters to quickly build mission-critical applications on Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.</CustomContent>

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## 为什么选择 TiDB Cloud

TiDB Cloud 让你几乎无需培训即可轻松完成如基础设施管理和集群部署等复杂任务。

- 开发者和数据库管理员（DBA）可以轻松应对大量在线流量，并能快速分析跨多个数据集的大规模数据。

- 各类规模的企业都可以轻松部署和管理 TiDB Cloud，无需预付费用，灵活应对业务增长。

观看下方视频，进一步了解 TiDB Cloud：

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

使用 TiDB Cloud，你可以获得以下关键特性：

- **Fast and Customized Scaling**

    弹性且透明地扩展至数百个节点，满足关键业务负载，同时保持 ACID 事务。无需关注分片（动词或动名词）。你还可以根据业务需求分别扩展计算和存储节点。

- **MySQL Compatibility**

    借助 TiDB 的 MySQL 兼容性，提高开发效率并缩短应用上线时间。可以轻松将现有 MySQL 实例中的数据迁移过来，无需重写代码。

- **High Availability and Reliability**

    天生高可用的架构设计。数据在多个可用区间复制，支持每日备份和故障自恢复，确保业务可持续性，无论是硬件故障、网络分区还是数据中心丢失。

- **Real-Time Analytics**

    内置分析引擎，实时获得分析查询结果。TiDB Cloud 能在当前数据上运行一致性的分析查询，不会影响关键业务应用。

- **Enterprise Grade Security**

    在专用网络和机器上保护你的数据，支持传输和静态加密。TiDB Cloud 通过了 SOC 2 Type 2、ISO 27001:2013、ISO 27701 认证，并完全符合 GDPR 要求。

- **Fully-Managed Service**

    通过易用的基于 Web 的管理平台，仅需几次点击即可部署、扩展、监控和管理 TiDB 集群。

- **Multi-Cloud Support**

    <CustomContent language="en,zh">

    保持灵活，避免云厂商锁定。TiDB Cloud 目前支持 AWS、Azure、Google Cloud 和阿里云。

    </CustomContent>

    <CustomContent language="ja">

    Stay flexible without cloud vendor lock-in. TiDB Cloud is currently available on AWS, Azure, and Google Cloud.

    </CustomContent>

- **Simple Pricing Plans**

    只为实际使用付费，价格透明，无隐藏费用。

- **World-Class Support**

    通过我们的支持门户、<a href="mailto:tidbcloud-support@pingcap.com">电子邮件</a>、聊天或视频会议，获得世界级支持。

## 部署选项

TiDB Cloud 提供以下部署选项：

- TiDB Cloud Starter

    TiDB Cloud Starter 是一款完全托管的多租户 TiDB 产品。它提供即时、自动扩展的 MySQL 兼容数据库，并在超出免费额度后按用量计费。

    <CustomContent language="en,zh">

    目前，TiDB Cloud Starter 已在 AWS 上正式发布，并在阿里云上公测。

    </CustomContent>

- TiDB Cloud Essential

    针对业务负载持续增长、需要实时扩展性的应用，TiDB Cloud Essential 提供灵活性和性能，助力你的业务增长。

    <CustomContent language="en,zh">

    目前，TiDB Cloud Essential 在 AWS 和阿里云上公测。

    关于 TiDB Cloud Starter 与 TiDB Cloud Essential 在阿里云上的功能对比，参见 [TiDB on Alibaba Cloud](https://www.pingcap.com/partners/alibaba-cloud/)。

    </CustomContent>

    <CustomContent language="ja">

    Currently, TiDB Cloud Essential is in public preview on AWS.

    </CustomContent>

<CustomContent plan="premium">

- TiDB Cloud Premium

    TiDB Cloud Premium 专为对实时无限扩展有极高要求的关键业务设计。它提供基于负载的自动扩展和全面的企业级能力。

    目前，TiDB Cloud Premium 在 AWS 和阿里云上私测。

</CustomContent>

- TiDB Cloud Dedicated

    TiDB Cloud Dedicated 面向关键业务，提供跨多个可用区的高可用、横向扩展和完整的 HTAP 能力。

    目前，TiDB Cloud Dedicated 已在 AWS 和 Google Cloud 上正式发布，并在 Azure 上公测。更多信息，参见 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated)。

## 架构

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

- TiDB VPC（虚拟私有云）

    对于每个 TiDB Cloud 集群，所有 TiDB 节点及辅助节点（包括 TiDB Operator 节点和日志节点）都部署在同一个 VPC 中。

- TiDB Cloud Central Services

    中央服务（包括计费、告警、元数据存储、Dashboard UI）独立部署。你可以通过互联网访问 Dashboard UI 来操作 TiDB 集群。

- 你的 VPC

    你可以通过私有端点连接或 VPC 对等连接访问你的 TiDB 集群。详情请参考 [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md) 或 [Set up VPC Peering Connection](/tidb-cloud/set-up-vpc-peering-connections.md)。