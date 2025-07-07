---
title: TiDB Cloud 2025年发布说明
summary: 了解2025年TiDB Cloud的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025年TiDB Cloud发布说明

本页面列出了2025年TiDB Cloud的发布说明。

## 2025年6月24日

**一般变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据库审计日志（测试版）现已可按需请求使用。该功能允许你在日志中记录用户访问详情（如执行的SQL语句）历史。

    若要申请此功能，请点击[TiDB Cloud控制台](https://tidbcloud.com)右下角的**?**，选择**Request Support**。然后，在描述栏中填写“申请TiDB Cloud Serverless数据库审计日志”，并点击**Submit**。

    更多信息请参见 [TiDB Cloud Serverless Database Audit Logging](/tidb-cloud/serverless-audit-logging.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户控制的日志脱敏。

    你现在可以启用或禁用TiDB Cloud Dedicated集群的日志脱敏功能，以自行管理集群日志的脱敏状态。

    更多信息请参见 [User-Controlled Log Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)。

- 现已正式发布（GA）支持在AWS托管的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中使用Customer-Managed Encryption Keys (CMEK)的Rest加密。

    该功能允许你通过密钥管理服务（KMS）管理对称加密密钥，保障静态数据的安全。

    更多信息请参见 [Encryption at Rest Using Customer-Managed Encryption Keys](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

## 2025年6月17日

**一般变更**

- 对于[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群，16 vCPU和32 vCPU的TiKV节点最大存储容量由**6144 GiB**调整为**4096 GiB**。

    更多信息请参见 [TiKV节点存储容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重新设计左侧导航栏，提升整体导航体验。
  
    - 新增<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，现已在左上角显示，方便你在需要时隐藏或显示左侧导航栏。
    - 左上角新增组合框，允许你快速在组织、项目和集群之间切换，集中管理。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏显示的条目会根据你在组合框中的当前选择动态调整，帮助你专注于最相关的功能。
    - 为了方便快速访问，**Support**、**Notification**和你的账户信息现在在所有控制台页面的左侧导航栏底部保持一致显示。

## 2025年6月4日

**一般变更**

- 在Microsoft Azure上的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)现已进入公开预览。

    通过此次发布，TiDB Cloud支持所有三大公共云平台——AWS、Google Cloud和Azure，允许你根据业务需求和云战略在任意平台部署TiDB Cloud Dedicated集群。
  
    - AWS和Google Cloud上的所有核心功能已全面支持Azure。
    - 当前Azure支持的区域包括：East US 2、Japan East和Southeast Asia，更多区域即将上线。
    - 在Azure上的TiDB Cloud Dedicated集群需要支持TiDB版本v7.5.3或更高版本。
  
  若要快速开始在Azure上的TiDB Cloud Dedicated，请参见以下文档：
  
    - [Create a TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/create-tidb-cluster.md)
    - [Connect a TiDB Cloud Dedicated Cluster via Azure Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    - [Import Data into TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/import-csv-files.md)

- Prometheus集成提供更多指标，增强[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群的监控能力。
  
    现在你可以将`tidbcloud_disk_read_latency`、`tidbcloud_kv_request_duration`等额外指标集成到Prometheus中，追踪TiDB Cloud Dedicated的更多性能方面。
  
    更多关于可用指标和启用方法的信息，见 [Integrate TiDB Cloud with Prometheus and Grafana (Beta)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储价格正式发布。

    优惠期截止至 **00:00 UTC 2025年6月5日**。之后价格恢复到标准价格。关于TiDB Cloud Dedicated的价格详情，见 [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中TiFlash节点存储容量配置体验。

    你现在可以在创建TiDB Cloud Dedicated集群时，通过切换开关控制TiFlash配置，使配置过程更直观、顺畅。

## 2025年5月27日

**一般变更**

- 支持通过changefeeds将数据流式传输到[Apache Pulsar](https://pulsar.apache.org)，适用于[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群。

    该功能使你可以将TiDB Cloud Dedicated集群与更广泛的下游系统集成，满足更多数据集成需求。使用此功能前，请确保你的TiDB Cloud Dedicated版本为v7.5.1或更高。

    更多信息请参见 [Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025年5月13日

**一般变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)现已支持全文搜索（测试版），适用于AI应用。

    TiDB Cloud Serverless现支持全文搜索（测试版），使AI和Retrieval-Augmented Generation（RAG）应用能够通过关键词精确检索内容。这补充了向量搜索（通过语义相似度检索内容）的能力。结合两者，可显著提升RAG工作流中的检索准确性和答案质量。主要功能包括：

    - 直接文本搜索：无需嵌入，直接查询字符串列。
    - 多语言支持：自动检测并分析多种语言文本，即使在同一表中也无需指定语言。
    - 相关性排序：采用行业标准的BM25算法进行排序，确保结果相关性。
    - 原生SQL支持：可无缝结合SQL的过滤、分组和连接功能。

  若要开始使用，请参见 [Full Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [Full Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md)。

- 提升[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中TiFlash节点的最大存储容量：

    - 8 vCPU TiFlash，从2048 GiB提升至4096 GiB
    - 32 vCPU TiFlash，从4096 GiB提升至8192 GiB

  此增强提升了TiDB Cloud Dedicated集群的分析数据存储能力，改善工作负载扩展效率，满足日益增长的数据需求。

    更多信息请参见 [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 改善维护窗口配置体验，提供更直观的选项以配置和重新调度维护任务。

    更多信息请参见 [Configure maintenance window](/tidb-cloud/configure-maintenance-window.md)。

- 延长TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型的优惠期。促销截止至2025年6月5日，之后价格恢复到标准水平。

**控制台变更**

- 优化[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中备份设置页面布局，提升备份配置体验。

    更多信息请参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 2025年4月22日

**一般变更**

- 现已支持将数据导出到Alibaba Cloud OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群现支持通过[AccessKey对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)将数据导出到[Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)。

    更多信息请参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

## 2025年4月15日

**一般变更**

- 支持将数据从[Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)导入到[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群。

    该功能简化了迁移到TiDB Cloud Serverless的数据流程。你可以使用AccessKey对进行认证。

    更多信息请参见以下文档：

    - [Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025年4月1日

**一般变更**

- [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md)功能现已正式发布（GA），支持在AWS和Google Cloud上的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中使用。

    该功能实现**细粒度计算资源隔离**，帮助你优化多租户或多工作负载场景下的性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将TiDB节点划分为逻辑隔离单元，确保一个组的工作负载不影响其他组。
        - 防止应用或业务单元之间的资源争用。

    - **管理简化**：

        - 在单一集群内管理所有节点组，降低运维复杂度。
        - 根据需求独立扩缩节点组。

  更多关于优势的信息，见 [the technical blog](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。若要开始使用，参见 [Manage TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md)。

- 引入[Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage)类型，用于[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中的TiKV节点。

    Standard存储类型适合大多数工作负载，提供性能与成本的平衡。

    **主要优势：**

    - **性能提升**：为Raft日志预留充足磁盘资源，减少Raft与数据存储的I/O争用，提升TiKV的读写性能。
    - **稳定性增强**：将关键的Raft操作与数据工作负载隔离，确保性能更可预测。
    - **性价比高**：在提供更高性能的同时，价格具有竞争力。

    **适用范围：**

    Standard存储类型会在2025年4月1日或之后新建的AWS上的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中自动应用（支持版本>=7.5.5、8.1.2或8.5.0），无需迁移。已有集群仍使用之前的[Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage)，无需操作。

    Standard存储的价格与Basic存储不同，详情请参见 [Pricing](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025年3月25日

**控制台变更**

- 支持在[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群中配置公网端点的防火墙规则。

    你现在可以在[TiDB Cloud控制台](https://tidbcloud.com/)中配置防火墙规则，控制通过公网端点的访问权限。直接指定允许的IP地址或范围，以增强安全性。

    更多信息请参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025年3月18日

**一般变更**

- 支持为部署在Google Cloud上的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群创建TiDB节点组，以增强资源管理的灵活性。

    更多信息请参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持将数据库审计日志文件存储在TiDB Cloud中，适用于在AWS上部署的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群。

    你可以直接从TiDB Cloud下载这些审计日志文件。注意此功能仅按需提供。

    更多信息请参见 [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md)。

- 提升TiDB Cloud账户安全性，改进多因素认证（MFA）管理。此功能适用于TiDB Cloud的密码登录。

    更多信息请参见 [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025年2月18日

**控制台变更**

- 引入Connected Care，这是TiDB Cloud的新支持服务。

    Connected Care旨在通过现代通信工具、主动支持和先进的AI能力，增强你与TiDB Cloud的连接，提供无缝且以客户为中心的体验。

    该服务包括以下功能：

    - **Clinic service**：高级监控与诊断，优化性能。
    - **AI chat in IM**：通过即时通讯（IM）工具获得即时AI协助。
    - **IM subscription for alerts and ticket updates**：通过IM获取告警和工单进展通知。
    - **IM interaction for support tickets**：通过IM创建和互动支持工单。

  更多信息请参见 [Connected Care Overview](/tidb-cloud/connected-care-overview.md)。

- 支持将数据从GCS和Azure Blob Storage导入[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群。

    TiDB Cloud Serverless现支持从Google Cloud Storage（GCS）和Azure Blob Storage导入数据。你可以使用Google Cloud服务账号密钥或Azure共享访问签名（SAS）令牌进行认证。此功能简化了迁移到TiDB Cloud Serverless的数据流程。

    更多信息请参见 [Import CSV Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [Import Apache Parquet Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025年1月21日

**控制台变更**

- 支持将单个本地CSV文件（最大250 MiB）导入到[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群，较之前的50 MiB限制有所提升。

    更多信息请参见 [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025年1月14日

**一般变更**

- 支持在AWS和Google Cloud上的[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群中新增Jakarta（ap-southeast-3）区域。

- 引入通知（Notification）功能，让你通过[TiDB Cloud控制台](https://tidbcloud.com/)即时获知TiDB Cloud的更新和告警。

    更多信息请参见 [Notifications](/tidb-cloud/notifications.md)。

## 2025年1月2日

**一般变更**

- 支持为[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群创建TiDB节点组，以增强资源管理的灵活性。

    更多信息请参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过Private Connect（测试版）将[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群连接到AWS和Google Cloud的通用Kafka。

    Private Connect利用云提供商的Private Link或Private Service Connect技术，使TiDB Cloud VPC中的changefeeds能通过私有IP连接到客户VPC中的Kafka，就像Kafka直接托管在TiDB Cloud VPC内一样。此功能有助于避免VPC CIDR冲突并满足安全合规要求。

    - 在AWS上配置自托管Kafka的Private Link服务，请参见 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)。
    - 在Google Cloud上配置自托管Kafka的Private Service Connect，请参见 [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)。

    使用此功能会产生额外的[Private Data Link费用](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    更多信息请参见 [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- 增加Kafka changefeeds的可配置选项：

    - 支持使用Debezium协议。Debezium是一个捕获数据库变更的工具，它将每个捕获的变更转化为事件消息，并发送到Kafka。更多信息请参见 [TiCDC Debezium Protocol](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表定义单一分区调度器，或为不同表定义不同的分区调度器。

    - 引入两种新的调度器类型，用于Kafka消息的分区分布：timestamp和column value。

  更多信息请参见 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- 改进TiDB Cloud中的角色管理：

    - 引入`Project Viewer`和`Organization Billing Viewer`角色，以实现更细粒度的权限控制。

    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  更多信息请参见 [Identity Access Management](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)集群支持区域高可用（测试版）。

    该功能适用于对基础设施冗余和业务连续性要求极高的工作负载。主要功能包括：

    - 节点分布在多个可用区，确保某一区故障时仍能保持高可用。
    - 关键OLTP（联机事务处理）组件，如PD和TiKV，在多个可用区复制以实现冗余。
    - 自动故障转移，最大程度减少主区域故障时的服务中断。
  
  该功能目前仅在AWS东京（ap-northeast-1）区域提供，且仅在集群创建时启用。
  
    更多信息请参见 [High Availability in TiDB Cloud Serverless](/tidb-cloud/serverless-high-availability.md)。

- 将新建[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)集群的默认TiDB版本由[v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1)升级至[v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 加强数据导出服务：

    - 支持通过[TiDB Cloud控制台](https://tidbcloud.com/)将[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)中的数据导出到Google Cloud Storage和Azure Blob Storage。
    - 支持导出Parquet格式的数据文件。

  更多信息请参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) 和 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md)。
