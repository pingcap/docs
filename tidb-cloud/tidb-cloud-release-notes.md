---
title: 2025 年 TiDB Cloud 发布说明
summary: 了解 2025 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2025 年的发布说明。

## 2025 年 7 月 22 日

**通用变更**

- 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供了新的节点规格：`32 vCPU, 128 GiB`。

    该新规格适用于 TiDB、TiKV 和 TiFlash 节点。

- 优化了 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 中 TiKV 的扩缩容流程，以提升集群稳定性。

    当你 [更改 TiKV 节点的 vCPU 和内存规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 时，TiDB Cloud 会自动检查集群内部服务是否需要额外容量以支持新配置。

    - 如果需要扩容，TiDB Cloud 会在操作前提示你确认。
    - 如果当前内部服务容量在扩容后已大于所需容量，TiDB Cloud 会保留现有内部服务配置，以避免不必要的变更影响集群稳定性。

**控制台变更**

- 优化了 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的云存储数据导入体验。

    导入流程现已简化为 3 步向导，并配备智能预检查。新向导将引导你完成连接设置、文件映射和存储桶扫描。通过扫描，TiDB Cloud 会在导入前准确展示将被导入的文件及其目标位置，大幅降低配置复杂度并防止导入失败。

    详细信息请参见以下文档：

    - [导入示例数据到 TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md)
    - [从云存储导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从云存储导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 7 月 15 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/) 升级为 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)。

    与 v8.1.2 相比，v8.5.2 包含了 [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/)、[v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/)、[v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/)、[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/)、[v8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/) 和 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/) 中发布的新特性、改进和 bug 修复。

- 支持审计 `BackupCompleted` 事件，以增强备份活动的控制台审计日志。

    该增强功能允许你记录备份完成活动，以满足安全和合规要求。

    详细信息请参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

- 支持在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 中过滤列值。

    你现在可以使用表达式在 changefeed 中过滤特定列值，从源头排除无关数据。该功能支持对 DML 事件进行细粒度过滤，帮助你降低资源消耗并提升性能。

    详细信息请参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。

## 2025 年 6 月 24 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据库审计日志（beta）现可按需申请。该功能允许你在日志中记录用户访问详情（如执行的 SQL 语句等）历史。

    如需申请该功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 Description 字段填写“Apply for TiDB Cloud Serverless database audit logging”，并点击 **Submit**。

    详细信息请参见 [TiDB Cloud Serverless 数据库审计日志](/tidb-cloud/serverless-audit-logging.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户自主控制日志脱敏。

    你现在可以为 TiDB Cloud Dedicated 集群启用或禁用日志脱敏，自主管理集群日志的脱敏状态。

    详细信息请参见 [用户自主控制日志脱敏](/tidb-cloud/tidb-cloud-log-redaction.md)。

- 托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已正式（GA）支持使用客户自管加密密钥（CMEK）进行静态加密。

    该功能允许你通过密钥管理服务（KMS）管理的对称加密密钥，保护静态数据安全。

    详细信息请参见 [使用客户自管加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

## 2025 年 6 月 17 日

**通用变更**

- 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，16 vCPU 和 32 vCPU 的 TiKV 节点最大存储容量由 **6144 GiB** 调整为 **4096 GiB**。

    详细信息请参见 [TiKV 节点存储容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 全面升级左侧导航栏，提升整体导航体验。
  
    - 左上角新增 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，可随时便捷地隐藏或显示左侧导航栏。
    - 左上角新增组合框，可在一个中心位置快速切换组织、项目和集群。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏的入口会根据你在组合框中的当前选择动态调整，帮助你聚焦最相关的功能。
    - **Support**、**Notification** 和你的账号入口现始终固定显示在所有控制台页面左侧导航栏底部，便于快速访问。

## 2025 年 6 月 4 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现已在 Microsoft Azure 上公测开放。

    随着本次发布，TiDB Cloud 现已支持三大主流公有云平台 —— AWS、Google Cloud 和 Azure，助你根据业务需求和云战略灵活部署 TiDB Cloud Dedicated 集群。

    - 在 Azure 上，所有 AWS 和 Google Cloud 支持的核心功能均已全面支持。
    - Azure 目前支持的区域包括：美国东部 2、日本东部和东南亚，更多区域即将开放。
    - Azure 上的 TiDB Cloud Dedicated 集群需使用 TiDB v7.5.3 或更高版本。

  快速上手 Azure 上的 TiDB Cloud Dedicated，请参见以下文档：

    - [在 Azure 上创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)
    - [通过 Azure Private Endpoint 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    - [向 Azure 上的 TiDB Cloud Dedicated 集群导入数据](/tidb-cloud/import-csv-files.md)

- Prometheus 集成为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供了更多监控指标。

    你现在可以将 `tidbcloud_disk_read_latency`、`tidbcloud_kv_request_duration` 等更多指标集成到 Prometheus，监控 TiDB Cloud Dedicated 的更多性能维度。

    有关可用指标及如何为新老用户启用的详细信息，请参见 [集成 TiDB Cloud 与 Prometheus 和 Grafana（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储定价已正式发布。

    优惠期自 **2025 年 6 月 5 日 00:00 UTC** 起结束，届时价格恢复为标准价。关于 TiDB Cloud Dedicated 价格的更多信息，请参见 [TiDB Cloud Dedicated 价格详情](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点规格配置的交互体验。

    你现在可以在创建 TiDB Cloud Dedicated 集群时，通过开关按钮控制 TiFlash 配置，使配置过程更加直观流畅。

## 2025 年 5 月 27 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 changefeed 现已支持将数据流式同步到 [Apache Pulsar](https://pulsar.apache.org)。

    该功能使你可以将 TiDB Cloud Dedicated 集群与更多下游系统集成，满足更多数据集成需求。使用该功能需确保集群版本为 v7.5.1 或更高。

    详细信息请参见 [同步到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已支持 AI 应用的全文检索（beta）。

    TiDB Cloud Serverless 现已支持全文检索（beta），使 AI 和 RAG（检索增强生成）应用能够通过精确关键词检索内容。该功能补充了向量检索（按语义相似度检索内容），两者结合可显著提升 RAG 工作流的检索准确性和答案质量。主要特性包括：

    - 直接文本检索：可直接查询字符串列，无需嵌入向量。
    - 多语言支持：自动检测并分析多语言文本，即使在同一张表中也无需指定语言。
    - 相关性排序：结果采用业界标准 BM25 算法进行相关性排序。
    - 原生 SQL 兼容：可无缝结合 SQL 的过滤、分组、关联等功能进行全文检索。

  快速上手请参见 [使用 SQL 进行全文检索](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [使用 Python 进行全文检索](/tidb-cloud/vector-search-full-text-search-python.md)。

- 提升 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点最大存储容量：

    - 8 vCPU TiFlash：由 2048 GiB 提升至 4096 GiB
    - 32 vCPU TiFlash：由 4096 GiB 提升至 8192 GiB

  此增强提升了 TiDB Cloud Dedicated 集群的分析型数据存储能力，提高了工作负载扩展效率，满足不断增长的数据需求。

    详细信息请参见 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 优化维护窗口配置体验，提供更直观的选项以配置和重新安排维护任务。

    详细信息请参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 延长 TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型的优惠期。促销活动现延长至 2025 年 6 月 5 日，届时价格将恢复为标准价。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 **Backup Setting** 页布局，提升备份配置体验。

    详细信息请参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**通用变更**

- 现已支持导出数据到阿里云 OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现支持使用 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 将数据导出到 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service)。

    详细信息请参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 TiDB 版本由 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3) 升级为 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2025 年 4 月 15 日

**通用变更**

- 支持从 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service) 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    该功能简化了向 TiDB Cloud Serverless 的数据迁移。你可以使用 AccessKey 对进行认证。

    详细信息请参见以下文档：

    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**通用变更**

- [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md) 功能现已在托管于 AWS 和 Google Cloud 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上正式（GA）发布。

    该功能支持在单个集群内实现**细粒度计算资源隔离**，帮助你在多租户或多工作负载场景下优化性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点分组为逻辑隔离单元，确保一个组内的工作负载不会影响其他组。
        - 防止应用或业务单元间的资源争用。

    - **简化管理**：

        - 在单个集群内统一管理所有节点组，降低运维负担。
        - 可根据需求独立扩缩各节点组。

  详细优势请参见 [技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。快速上手请参见 [管理 TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md)。

- 在托管于 AWS 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中引入 [Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage) 类型的 TiKV 节点。

    Standard 存储类型适用于大多数工作负载，在性能与成本之间实现平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志预留充足磁盘资源，减少 Raft 与数据存储间的 I/O 争用，从而提升 TiKV 的读写性能。
    - **稳定性增强**：将关键 Raft 操作与数据工作负载隔离，确保更可预测的性能。
    - **成本效益**：与之前的存储类型相比，以更具竞争力的价格提供更高性能。

    **可用性：**

    Standard 存储类型会自动应用于 2025 年 4 月 1 日及以后在 AWS 上新建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，且需支持的版本（>= 7.5.5、8.1.2 或 8.5.0）。现有集群仍使用之前的 [Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage) 类型，无需迁移。

    Standard 存储类型的价格与 Basic 存储类型不同。详细信息请参见 [价格](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现已支持为公网访问端点配置防火墙规则。

    你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中为 TiDB Cloud Serverless 集群配置防火墙规则，控制公网端点的访问。可直接指定允许的 IP 地址或范围，提升安全性。

    详细信息请参见 [为 TiDB Cloud Serverless 公网端点配置防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**通用变更**

- 支持为部署在 Google Cloud 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    详细信息请参见 [TiDB Node Group 概览](/tidb-cloud/tidb-node-group-overview.md)。

- 支持将数据库审计日志文件存储在 TiDB Cloud 中，适用于部署在 AWS 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。注意，该功能仅可按需申请。

    详细信息请参见 [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

- 通过优化多因素认证（MFA）管理，提升 TiDB Cloud 账号安全性。该功能适用于 TiDB Cloud 的密码登录。

    详细信息请参见 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 推出 Connected Care，TiDB Cloud 的全新支持服务。

    Connected Care 服务通过现代通信工具、主动支持和先进的 AI 能力，增强你与 TiDB Cloud 的连接，带来无缝且以客户为中心的体验。

    Connected Care 服务包含以下功能：

    - **Clinic service**：高级监控与诊断，优化性能。
    - **AI chat in IM**：通过即时通讯工具获得 AI 实时协助。
    - **IM subscription for alerts and ticket updates**：通过 IM 实时获取告警和工单进展。
    - **IM interaction for support tickets**：可通过 IM 工具创建和跟进支持工单。

  详细信息请参见 [Connected Care 概览](/tidb-cloud/connected-care-overview.md)。

- 支持从 GCS 和 Azure Blob Storage 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    TiDB Cloud Serverless 现已支持从 Google Cloud Storage（GCS）和 Azure Blob Storage 导入数据。你可以使用 Google Cloud 服务账号密钥或 Azure SAS token 进行认证。该功能简化了向 TiDB Cloud Serverless 的数据迁移。

    详细信息请参见 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 及 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现已支持单次任务导入最大 250 MiB 的本地 CSV 文件（此前为 50 MiB）。

    详细信息请参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已支持新的 AWS 区域：`Jakarta (ap-southeast-3)`。

- 推出 Notification 功能，使你可通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 实时获取 TiDB Cloud 更新和告警。

    详细信息请参见 [Notifications](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**通用变更**

- 支持为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    详细信息请参见 [TiDB Node Group 概览](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过 Private Connect（beta）将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群连接到 AWS 和 Google Cloud 上的通用 Kafka。

    Private Connect 利用云厂商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 内的 changefeed 能通过私有 IP 连接到客户 VPC 内的 Kafka，就像这些 Kafka 直接部署在 TiDB Cloud VPC 内一样。该功能有助于避免 VPC CIDR 冲突并满足安全合规要求。

    - 对于 AWS 上的 Apache Kafka，请参见 [在 AWS 上配置自建 Kafka Private Link 服务](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)。
    - 对于 Google Cloud 上的 Apache Kafka，请参见 [在 Google Cloud 上配置自建 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)。

  注意，使用该功能会产生额外的 [Private Data Link 费用](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    详细信息请参见 [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- Kafka changefeed 新增可配置选项：

    - 支持使用 Debezium 协议。Debezium 是一种数据库变更捕获工具，会将每次捕获的数据库变更转换为事件消息并发送到 Kafka。详细信息请参见 [TiCDC Debezium 协议](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。
    - 支持为所有表定义单一分区分发器，或为不同表定义不同的分区分发器。
    - 新增两种分发器类型：按时间戳和按列值分区分发 Kafka 消息。

  详细信息请参见 [同步到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- TiDB Cloud 角色增强：

    - 新增 `Project Viewer` 和 `Organization Billing Viewer` 角色，实现更细粒度的访问控制。
    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  详细信息请参见 [身份访问管理](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持区域高可用（beta）。

    该功能适用于对基础设施冗余和业务连续性有极高要求的工作负载。主要功能包括：

    - 节点分布在多个可用区，确保单区故障时的高可用性。
    - 关键 OLTP 组件（如 PD 和 TiKV）在可用区间冗余复制。
    - 主可用区故障时自动故障转移，最小化服务中断。

  该功能目前仅在 AWS 东京（ap-northeast-1）区域可用，且仅可在集群创建时启用。

    详细信息请参见 [TiDB Cloud Serverless 高可用](/tidb-cloud/serverless-high-availability.md)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级为 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 数据导出服务增强：

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据导出到 Google Cloud Storage 和 Azure Blob Storage。
    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 导出 Parquet 格式数据。

  详细信息请参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md) 及 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。
