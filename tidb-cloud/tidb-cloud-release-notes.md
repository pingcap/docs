---
title: TiDB Cloud 2025 年发布说明
summary: 了解 TiDB Cloud 在 2025 年的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud 2025 年发布说明

本页面列出了 TiDB Cloud 在 2025 年的发布说明。

## 2025 年 6 月 24 日

**一般变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据库审计日志（测试版）现已可按需请求。此功能允许你在日志中记录用户访问详情（如执行的任何 SQL 语句）的历史。

    若要请求此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。接着，在描述栏中填写“申请 TiDB Cloud Serverless 数据库审计日志”，并点击 **Submit**。

    更多信息请参见 [TiDB Cloud Serverless Database Audit Logging](/tidb-cloud/serverless-audit-logging.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户控制的日志脱敏。

    你现在可以启用或禁用 TiDB Cloud Dedicated 集群的日志脱敏功能，以自行管理集群日志的脱敏状态。

    更多信息请参见 [User-Controlled Log Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)。

- 现在，AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持 Encryption at Rest with Customer-Managed Encryption Keys (CMEK)，即客户管理的加密密钥（GA 版本）。

    此功能使你能够通过密钥管理服务（KMS）使用对称加密密钥，保障静态数据的安全。

    更多信息请参见 [Encryption at Rest Using Customer-Managed Encryption Keys](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

## 2025 年 6 月 17 日

**一般变更**

- 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，16 vCPU 和 32 vCPU 的 TiKV 节点最大存储容量由 **6144 GiB** 改为 **4096 GiB**。

    更多信息请参见 [TiKV node storage size](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重构左侧导航栏，以提升整体导航体验。
  
    - 新的 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标现已在左上角提供，方便你在需要时隐藏或显示左侧导航栏。
    - 左上角新增组合框，允许你快速在组织、项目和集群之间切换，集中管理。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏显示的条目会根据你在组合框中的当前选择动态调整，帮助你专注于最相关的功能。
    - 为了方便快速访问，**Support**、**Notification** 和你的账户条目现在在所有控制台页面的左侧导航栏底部保持一致显示。

## 2025 年 6 月 4 日

**一般变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Microsoft Azure 上现已进入公开预览。

    通过此发布，TiDB Cloud 现支持所有三大公共云平台——AWS、Google Cloud 和 Azure，允许你根据业务需求和云战略在任何平台部署 TiDB Cloud Dedicated 集群。
  
    - 所有在 AWS 和 Google Cloud 上提供的核心功能在 Azure 上也完全支持。
    - 目前支持的 Azure 区域包括：East US 2、Japan East 和 Southeast Asia，更多区域即将上线。
    - 在 Azure 上的 TiDB Cloud Dedicated 集群需要支持版本 v7.5.3 及以上。
  
  若要快速开始在 Azure 上使用 TiDB Cloud Dedicated，请参见以下文档：
  
    - [Create a TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/create-tidb-cluster.md)
    - [Connect a TiDB Cloud Dedicated Cluster via Azure Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    - [Import Data into TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/import-csv-files.md)

- Prometheus 集成提供更多指标，增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控能力。
  
    现在你可以将 `tidbcloud_disk_read_latency` 和 `tidbcloud_kv_request_duration` 等额外指标集成到 Prometheus，以追踪 TiDB Cloud Dedicated 的更多性能方面。
  
    更多可用指标和启用方法，请参见 [Integrate TiDB Cloud with Prometheus and Grafana (Beta)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储价格正式发布。

    优惠期截止至 **00:00 UTC 2025 年 6 月 5 日**。之后价格恢复到标准水平。关于 TiDB Cloud Dedicated 价格的更多信息，请参见 [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中 TiFlash 节点存储配置的交互体验。

    你现在可以在创建 TiDB Cloud Dedicated 集群时使用切换开关控制 TiFlash 配置，使配置过程更直观、顺畅。

## 2025 年 5 月 27 日

**一般变更**

- 支持通过 changefeeds 将数据流式传输到 [Apache Pulsar](https://pulsar.apache.org) ，适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    此功能使你可以将 TiDB Cloud Dedicated 集群与更广泛的下游系统集成，满足额外的数据集成需求。使用此功能时，请确保你的 TiDB Cloud Dedicated 集群版本为 v7.5.1 或更高。

    更多信息请参见 [Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**一般变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已支持全文搜索（测试版），适用于 AI 应用。

    TiDB Cloud Serverless 现支持全文搜索（测试版），使 AI 和 Retrieval-Augmented Generation (RAG) 应用能够通过关键词精确检索内容。这补充了向量搜索（通过语义相似度检索内容）的功能。结合两者，可显著提升 RAG 工作流中的检索准确性和答案质量。主要特性包括：

    - 直接文本搜索：无需嵌入，直接查询字符串列。
    - 多语言支持：自动检测并分析多种语言文本，即使在同一表中，也无需指定语言。
    - 相关性排序：采用行业标准的 BM25 算法进行排序，确保结果相关性。
    - 原生 SQL 兼容：可无缝使用 SQL 功能（如过滤、分组和连接）结合全文搜索。

  若要开始使用，请参见 [Full Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [Full Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md)。

- 提升 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中 TiFlash 节点的最大存储容量：

    - 8 vCPU TiFlash，从 2048 GiB 提升至 4096 GiB
    - 32 vCPU TiFlash，从 4096 GiB 提升至 8192 GiB

  此增强提升了 TiDB Cloud Dedicated 集群的分析数据存储能力，改善工作负载扩展效率，满足日益增长的数据需求。

    更多信息请参见 [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 改善维护窗口配置体验，提供直观选项以配置和重新调度维护任务。

    更多信息请参见 [Configure maintenance window](/tidb-cloud/configure-maintenance-window.md)。

- 延长 TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型的优惠期。促销现截止至 2025 年 6 月 5 日。之后价格恢复到标准水平。

**控制台变更**

- 优化 [Backup Setting] 页面布局，改善 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的备份配置体验。

    更多信息请参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**一般变更**

- 现已支持将数据导出到 Alibaba Cloud OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现支持使用 [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 将数据导出到 [Alibaba Cloud Object Storage Service (OSS)]。

    更多信息请参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

## 2025 年 4 月 15 日

**一般变更**

- 支持将数据从 [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/en/product/object-storage-service) 导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    此功能简化了数据迁移到 TiDB Cloud Serverless 的流程。你可以使用 AccessKey pair 进行认证。

    更多信息请参见以下文档：

    - [Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**一般变更**

- [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md) 功能现已正式发布（GA），支持在 AWS 和 Google Cloud 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    此功能实现单个集群内的**细粒度计算资源隔离**，帮助你优化多租户或多工作负载场景的性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点划分为逻辑隔离单元，确保一个组内的工作负载不影响其他组。
        - 防止应用或业务单元之间的资源争用。

    - **简化管理**：

        - 在单一集群内管理所有节点组，降低运维复杂度。
        - 根据需求独立扩展各组。

  更多关于优势的信息，请参见 [技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。若要开始使用，请参见 [Manage TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md)。

- 引入 [Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage) 类型，用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中的 TiKV 节点。

    Standard storage 类型适合大多数工作负载，提供性能与成本的平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志预留充足磁盘资源，减少 Raft 和数据存储之间的 I/O 争用，从而提升 TiKV 的读写性能。
    - **稳定性增强**：将关键的 Raft 操作与数据工作负载隔离，确保性能更可预测。
    - **性价比高**：在提供更高性能的同时，价格具有竞争力，优于之前的存储类型。

    **适用范围：**

    该存储类型会在 2025 年 4 月 1 日或之后创建的 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新集群中自动应用，支持版本为 >= 7.5.5、8.1.2 或 8.5.0。已有集群仍使用之前的 [Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage)，无需迁移。

    Standard storage 的价格与 Basic storage 不同，更多信息请参见 [Pricing](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- 支持在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群中配置公共端点的防火墙规则。

    你现在可以在控制台中配置防火墙规则，控制通过公共端点的访问权限。直接在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中指定允许的 IP 地址或范围，以增强安全性。

    更多信息请参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**一般变更**

- 支持为部署在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，以增强资源管理的灵活性。

    更多信息请参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持将数据库审计日志文件存储在 AWS 上的 TiDB Cloud 中。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。注意此功能仅按需请求提供。

    更多信息请参见 [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md)。

- 提升 TiDB Cloud 账户安全性，通过改进多因素认证（MFA）管理。

    详情请参见 [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 引入 Connected Care，这是 TiDB Cloud 的新支持服务。

    Connected Care 旨在通过现代通信工具、主动支持和先进的 AI 功能，增强你与 TiDB Cloud 的连接，提供无缝且以客户为中心的体验。

    该服务提供以下功能：

    - **Clinic service**：高级监控和诊断，优化性能。
    - **AI chat in IM**：通过即时通讯（IM）工具获得即时 AI 支持。
    - **IM subscription for alerts and ticket updates**：通过 IM 获取告警和工单进展通知。
    - **IM interaction for support tickets**：通过 IM 创建和互动支持工单。

  更多信息请参见 [Connected Care Overview](/tidb-cloud/connected-care-overview.md)。

- 支持将数据从 GCS 和 Azure Blob Storage 导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    TiDB Cloud Serverless 现支持从 Google Cloud Storage（GCS）和 Azure Blob Storage 导入数据。你可以使用 Google Cloud 服务账户密钥或 Azure 共享访问签名（SAS）令牌进行认证。此功能简化了数据迁移到 TiDB Cloud Serverless 的流程。

    更多信息请参见 [Import CSV Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [Import Apache Parquet Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- 支持将单个本地 CSV 文件（最大 250 MiB）导入到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，较之前的 50 MiB 限制有所提升。

    更多信息请参见 [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**一般变更**

- 支持在 Google Cloud 上为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建新的区域：`Jakarta (ap-southeast-3)`。

- 引入通知（Notification）功能，让你可以通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 实时获取 TiDB Cloud 的更新和告警。

    更多信息请参见 [Notifications](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**一般变更**

- 支持为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，以增强资源管理的灵活性。

    更多信息请参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过 Private Connect（测试版）将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群连接到 AWS 和 Google Cloud 上的通用 Kafka。

    Private Connect 利用云提供商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 中的 changefeeds 能通过私有 IP 连接到客户 VPC 中的 Kafka，就像这些 Kafka 直接托管在 TiDB Cloud VPC 内一样。此功能有助于避免 VPC CIDR 冲突并满足安全合规要求。

    - 在 AWS 上的 Apache Kafka，请参见 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 以配置网络连接。
    - 在 Google Cloud 上的 Apache Kafka，请参见 [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 以配置网络连接。
  
  注意：使用此功能会产生额外的 [Private Data Link 费用](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    更多信息请参见 [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- 增加 Kafka changefeeds 的可配置选项：

    - 支持使用 Debezium 协议。Debezium 是一种捕获数据库变更的工具，它将每个捕获的数据库变更转换为事件消息，并发送到 Kafka。更多信息请参见 [TiCDC Debezium Protocol](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表定义单一分区调度器，或为不同表定义不同的分区调度器。

    - 引入两种新的调度器类型，用于 Kafka 消息的分布：timestamp 和 column value。

  更多信息请参见 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- 改进 TiDB Cloud 中的角色权限管理：

    - 引入 `Project Viewer` 和 `Organization Billing Viewer` 角色，以实现更细粒度的访问控制。

    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  更多信息请参见 [Identity Access Management](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持区域高可用（测试版）。

    该功能面向需要最大基础设施冗余和业务连续性的工作负载。主要功能包括：

    - 节点分布在多个可用区，确保某一区故障时仍能保持高可用。
    - 关键 OLTP 组件（如 PD 和 TiKV）在多个可用区复制，确保冗余。
    - 自动故障转移，最大程度减少主区域故障时的服务中断。
  
  目前此功能仅在 AWS Tokyo（ap-northeast-1）区域提供，且仅在集群创建时启用。
  
    更多信息请参见 [High Availability in TiDB Cloud Serverless](/tidb-cloud/serverless-high-availability.md)。

- 将新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级至 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 加强数据导出服务：

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据导出到 Google Cloud Storage 和 Azure Blob Storage。
    - 支持导出 Parquet 格式文件。

  更多信息请参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) 和 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md)。