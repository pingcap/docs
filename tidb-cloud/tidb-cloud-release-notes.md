---
title: 2025 年 TiDB Cloud 发布说明
summary: 了解 2025 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2025 年的发布说明。

## 2025 年 9 月 23 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 中由用户控制 `UPDATE` 事件的拆分。

        在 TiDB Cloud Dedicated 集群中，你可以配置是否将 `UPDATE` 事件保留为原始事件，或将其拆分为单独的 `DELETE` 和 `INSERT` 事件。该功能为高级同步场景提供了更大的灵活性。

        此功能仅支持非 SQL 目的地，如 Apache Kafka 和 Amazon S3。更多信息，参见 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)、[Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md) 和 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

        有关拆分行为的详细信息，参见 [Split primary or unique key `UPDATE` events for non-MySQL sinks](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

    - 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的节点规格：`32 vCPU, 64 GiB`。

        该节点规格适用于 TiDB 节点。

## 2025 年 9 月 16 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 托管在 Azure 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已支持使用客户自管加密密钥（CMEK）的静态加密。

        该功能允许你使用自己控制的加密密钥保护静态数据。CMEK 提供以下优势：

        - 数据安全：你拥有并管理加密密钥，确保数据受到保护且完全受你控制。
        - 合规性：使用 CMEK 有助于满足数据加密的合规和监管要求。
        - 灵活性：你可以在创建项目时启用 CMEK，并在创建集群前完成 CMEK 配置。

      启用该功能的步骤如下：

        1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 创建启用 CMEK 的项目。
        2. 完成该项目的 CMEK 配置。
        3. 在与你的 CMEK 配置相同区域的 Azure 上创建 TiDB Cloud Dedicated 集群。

      更多信息，参见 [Encryption at Rest Using Customer-Managed Encryption Keys on Azure](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)。

## 2025 年 9 月 9 日

**高可用性变更**

- **TiDB Cloud Starter**

    - 新创建的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群仅启用分区高可用性（zonal high availability），且不可配置。
    - 对于 2025 年 9 月 9 日前已启用区域高可用性的现有 TiDB Cloud Starter 集群，区域高可用性仍然受支持，不受影响。

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - 新创建的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群默认启用区域高可用性，你可以在集群创建时根据需要切换为分区高可用性。

  更多信息，参见 [High Availability in TiDB Cloud Starter and Essential](/tidb-cloud/serverless-high-availability.md)。

</CustomContent>

## 2025 年 9 月 2 日

**通用变更**

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群现已支持 3 个新的阿里云区域：`Jakarta (ap-southeast-5)`、`Mexico (na-south-1)` 和 `Tokyo (ap-northeast-1)`。

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) 升级至 [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)。

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) 升级至 [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)。

</CustomContent>

## 2025 年 8 月 26 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 中引入 Auto Embedding（Beta），让你无需额外配置即可轻松将文本转换为向量。该功能可加速在 TiDB Cloud 中开发语义搜索、RAG、重排序和分类等场景，减少集成成本。

        - **与主流 LLM 提供商的 Auto Embedding**：Amazon Titan、OpenAI、Cohere、Gemini、Jina AI、Hugging Face 和 NVIDIA NIM。
        - **与 AWS Bedrock 的原生集成**：支持 Amazon Titan 和 Cohere 文本嵌入模型，享有免费额度。
        - **支持 SQL 和 Python**，并提供创建、存储和查询 embedding 的代码示例。

      更多信息，参见 [Auto Embedding](https://docs.pingcap.com/tidbcloud/vector-search-auto-embedding-overview/?plan=starter)。

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 不再支持 Index Insight（beta）功能。

        推荐使用 [Index Advisor](/index-advisor.md)，该功能适用于 TiDB v8.5.0 及以上版本。Index Advisor 引入了 `RECOMMEND INDEX` SQL 语句，可通过推荐索引优化查询性能。

    - 你现在可以在启用每周备份的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上手动禁用时间点恢复（Point-in-time Restore）功能。

        该优化有助于降低不需要高 RPO 保护的集群的成本。

        更多信息，参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 2025 年 8 月 12 日

**通用变更**

<CustomContent language="en,zh">

- **TiDB Cloud Starter**

    - 将 “TiDB Cloud Serverless” 重命名为 “TiDB Cloud Starter”。

        自动弹性入门方案现更名为 “TiDB Cloud Starter”，以更好地体现其为新用户提供的角色。所有功能、价格和免费额度保持不变。

        自 2025 年 8 月 12 日（PDT）起，你现有的 Serverless 集群将在 [TiDB Cloud 控制台](https://tidbcloud.com) 中显示为 Starter。你的连接字符串、端点和数据均保持不变，无需修改代码或安排停机。

    - TiDB Cloud Starter 在阿里云上进入预览阶段。

- **TiDB Cloud Essential**

    [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在阿里云上进入预览阶段。

    TiDB Cloud Essential 在阿里云自 2025 年 5 月起已进行有限公测。本次是 Essential 首次正式纳入发布说明。在此阶段，Essential 在阿里云上的功能集与 Starter 保持一致，现已在阿里云新加坡区域提供。

    体验方式：

    - 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 创建集群时选择阿里云作为云服务商，即可看到 Essential 选项。
    - 你也可以通过 [阿里云 Marketplace 上的 Essential 产品页](https://www.alibabacloud.com/en/marketplace/tidb?_p_lc=1) 访问 Essential。

  下一步，我们计划扩展阿里云的区域覆盖，并增加对 AWS 的支持。

    如果你在预览期间体验了阿里云上的 Essential，欢迎通过 Web 控制台反馈，或加入我们的 [Slack 社区](https://tidbcommunity.slack.com/archives/CH7TTLL7P) 或 [Discord 社区](https://discord.gg/ukhXbn69Nx) 交流。

- **TiDB Cloud Dedicated**

    - 通过优化 NAT 子网分配策略，托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现支持每个区域超过 8 个 Google Private Service Connect（PSC）连接。

        更多信息，参见 [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)。

    - 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 指标：

        - 在 [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) 分类下，新增 **Affected Rows**、**Leader Count** 和 **Region Count** 指标，提升诊断能力。
        - 在 [**Server**](/tidb-cloud/built-in-monitoring.md#server) 分类下，优化 **TiKV IO Bps** 指标，提升准确性和一致性。

      更多信息，参见 [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Starter**

    Rename "TiDB Cloud Serverless" to "TiDB Cloud Starter".

    The auto-scaling entry plan is now named "TiDB Cloud Starter" to better reflect its role for new users. All features, pricing, and the free usage quota remain unchanged.

    Starting August 12, 2025 (PDT), your existing Serverless clusters will appear as Starter in the [TiDB Cloud console](https://tidbcloud.com). Your connection strings, endpoints, and data will remain unchanged, so you do not need to make any code changes or schedule downtime.

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) on Google Cloud now supports more than 8 Google Private Service Connect (PSC) connections per region by optimizing the NAT subnet allocation strategy.

        For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions).

    - Optimize [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) metrics:

        - In the [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) category, add the **Affected Rows**, **Leader Count**, and **Region Count** metrics to improve diagnostics.
        - In the [**Server**](/tidb-cloud/built-in-monitoring.md#server) category, refine the **TiKV IO Bps** metric to improve accuracy and consistency.

      For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

</CustomContent>

**API 变更**

- 推出 TiDB Cloud Dedicated API（v1beta1），可自动高效地管理以下资源：

    - **Cluster**：更灵活地管理你的 TiDB Cloud Dedicated 集群。
    - **Region**：展示所有可部署 TiDB Cloud Dedicated 集群的云区域。
    - **Private endpoint connection**：为集群配置安全的私有连接。
    - **Import**：管理集群的数据导入任务。

  更多信息，参见 [TiDB Cloud Dedicated API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)。

- 推出 TiDB Cloud Starter 和 Essential API（v1beta1），可自动高效地管理以下资源：

    - **Cluster**：更灵活地管理你的 TiDB Cloud Starter 或 Essential 集群。
    - **Branch**：管理集群的分支。
    - **Export**：管理集群的数据导出任务。
    - **Import**：管理集群的数据导入任务。

  更多信息，参见 [TiDB Cloud Starter and Essential API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/)。

- TiDB Cloud IAM API（v1beta1）支持 API 密钥管理的基于角色的访问控制（RBAC），可在组织和项目级别设置 API 密钥角色，提升安全性和访问控制能力。

    更多信息，参见 [TiDB Cloud IAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/)。

## 2025 年 7 月 31 日

**通用变更**

- 增强版 Datadog 和 New Relic 集成现已开放预览。

    主要增强点：

    - 重构集成后端，采用优化的隔离架构，最大限度减少指标丢失。
    - 根据用户需求增加更多监控指标。
    - 优化指标规则，提升一致性。

  这些增强带来更准确的监控，并提升 Datadog 和 New Relic 集成的可靠性。

  发布计划：

  该预览版本现已对尚未集成 Datadog 或 New Relic 的组织开放。对于已集成的组织，我们将在下月主动联系你，协商合适的迁移方案和时间表。

  更多信息，参见 [Integrate TiDB Cloud with Datadog (Preview)](/tidb-cloud/monitor-datadog-integration.md) 和 [Integrate TiDB Cloud with New Relic (Preview)](/tidb-cloud/monitor-new-relic-integration.md)。

## 2025 年 7 月 22 日

**通用变更**

- 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的节点规格：`32 vCPU, 128 GiB`。

    该规格适用于 TiDB、TiKV 和 TiFlash 节点。

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 中 TiKV 的扩缩容流程，提升集群稳定性。

    当你 [更改 TiKV 节点的 vCPU 和内存规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 时，TiDB Cloud 会自动检查集群内部服务是否需要扩容以支持新配置。

    - 如需扩容，TiDB Cloud 会在操作前提示你确认。
    - 如果扩容后内部服务容量已大于所需，TiDB Cloud 会保留现有配置，避免不必要的变更影响集群稳定性。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的云存储数据导入体验。

    导入流程现已简化为 3 步向导，并配备智能预检查。新向导将引导你完成连接设置、文件映射和存储桶扫描。通过扫描，TiDB Cloud 会在导入前准确展示将被导入的文件及其目标位置，大幅降低配置复杂度并防止导入失败。

    更多信息，参见以下文档：

    - [Import Sample Data into TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md)
    - [Import CSV Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 7 月 15 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/) 升级至 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)。

    与 v8.1.2 相比，v8.5.2 包含了 [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/)、[v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/)、[v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/)、[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/)、[v8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/) 和 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/) 的新特性、改进和修复。

- 支持审计 `BackupCompleted` 事件，增强备份活动的控制台审计日志。

    该增强可记录备份完成活动，满足安全与合规需求。

    更多信息，参见 [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md)。

- 支持在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 中按列值过滤。

    你现在可以在 changefeed 中使用表达式过滤特定列值，从源头排除无关数据。该功能实现 DML 事件的细粒度过滤，有助于降低资源消耗并提升性能。

    更多信息，参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。

## 2025 年 6 月 24 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据库审计日志（beta）现可按需申请。该功能允许你在日志中记录用户访问详情（如执行的 SQL 语句）历史。

    申请方式：在 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角点击 **?**，选择 **Request Support**，在 Description 字段填写 “Apply for TiDB Cloud Serverless database audit logging”，然后点击 **Submit**。

    更多信息，参见 [TiDB Cloud Serverless Database Audit Logging](/tidb-cloud/serverless-audit-logging.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户自主管理日志脱敏。

    你现在可以为 TiDB Cloud Dedicated 集群启用或禁用日志脱敏，自主管理集群日志的脱敏状态。

    更多信息，参见 [User-Controlled Log Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)。

- 托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已正式（GA）支持使用客户自管加密密钥（CMEK）的静态加密。

    该功能允许你通过密钥管理服务（KMS）管理的对称加密密钥保护静态数据。

    更多信息，参见 [Encryption at Rest Using Customer-Managed Encryption Keys on AWS](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)。

## 2025 年 6 月 17 日

**通用变更**

- 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，16 vCPU 和 32 vCPU 的 TiKV 节点最大存储容量由 **6144 GiB** 调整为 **4096 GiB**。

    更多信息，参见 [TiKV node storage size](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重构左侧导航栏，提升整体导航体验。

    - 左上角新增 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，可随时隐藏或显示左侧导航栏。
    - 左上角新增组合框，可快速在组织、项目和集群间切换，集中管理。

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏的入口会根据组合框当前选择动态调整，帮助你聚焦最相关的功能。
    - **Support**、**Notification** 和账号入口现始终固定在左侧导航栏底部，便于快速访问。

## 2025 年 6 月 4 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Microsoft Azure 上现已公测。

    随着本次发布，TiDB Cloud 现已支持三大主流公有云平台 —— AWS、Google Cloud 和 Azure，助你根据业务需求和云战略灵活部署 TiDB Cloud Dedicated 集群。

    - AWS 和 Google Cloud 上的所有核心功能在 Azure 上均已支持。
    - Azure 目前支持 East US 2、日本东部和东南亚 3 个区域，后续将支持更多区域。
    - Azure 上的 TiDB Cloud Dedicated 集群需使用 TiDB v7.5.3 或更高版本。

  快速上手指南：

    - [Create a TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/create-tidb-cluster.md)
    - [Connect a TiDB Cloud Dedicated Cluster via Azure Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    - [Import Data into TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/import-csv-files.md)

- Prometheus 集成现提供更多指标，增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控能力。

    你现在可以将 `tidbcloud_disk_read_latency`、`tidbcloud_kv_request_duration` 等更多指标集成到 Prometheus，监控 TiDB Cloud Dedicated 的更多性能维度。

    有关可用指标及如何为新老用户启用，参见 [Integrate TiDB Cloud with Prometheus and Grafana (Beta)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型价格正式发布。

    优惠期自 **2025 年 6 月 5 日 00:00 UTC** 起结束，届时价格恢复为标准价。更多 TiDB Cloud Dedicated 价格信息，参见 [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点规格配置交互体验。

    你现在可以在创建 TiDB Cloud Dedicated 集群时通过开关按钮控制 TiFlash 配置，提升配置的直观性和流畅性。

## 2025 年 5 月 27 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 changefeed 现已支持向 [Apache Pulsar](https://pulsar.apache.org) 流式同步数据。

    该功能可将 TiDB Cloud Dedicated 集群与更多下游系统集成，满足更多数据集成需求。使用该功能需确保集群版本为 v7.5.1 或更高。

    更多信息，参见 [Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已支持全文检索（beta），助力 AI 应用。

    TiDB Cloud Serverless 现已支持全文检索（beta），使 AI 和 RAG（检索增强生成）应用可通过精确关键词检索内容。该功能补充了向量检索（按语义相似度检索内容），两者结合可显著提升 RAG 工作流的检索准确性和答案质量。主要特性包括：

    - 直接文本检索：可直接查询字符串列，无需 embedding。
    - 多语言支持：自动检测并分析多语言文本，即使同一表中包含多种语言，无需指定语言。
    - 相关性排序：结果采用业界标准 BM25 算法排序，确保最优相关性。
    - 原生 SQL 兼容：可与 SQL 过滤、分组、关联等功能无缝结合。

  快速上手，参见 [Full Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [Full Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md)。

- 提升 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点最大存储容量：

    - 8 vCPU TiFlash：由 2048 GiB 提升至 4096 GiB
    - 32 vCPU TiFlash：由 4096 GiB 提升至 8192 GiB

  该增强提升了 TiDB Cloud Dedicated 集群的分析型数据存储能力，提高了工作负载扩展效率，满足不断增长的数据需求。

    更多信息，参见 [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 优化维护窗口配置体验，提供更直观的选项以配置和重新安排维护任务。

    更多信息，参见 [Configure maintenance window](/tidb-cloud/configure-maintenance-window.md)。

- 延长 TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型的优惠期，现将于 2025 年 6 月 5 日结束。届时价格将恢复为标准价。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 **Backup Setting** 页面布局，提升备份配置体验。

    更多信息，参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**通用变更**

- 现已支持导出数据到阿里云 OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现支持使用 [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 导出数据到 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service)。

    更多信息，参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 TiDB 版本由 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3) 升级至 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2025 年 4 月 15 日

**通用变更**

- 支持从 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service) 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    该功能简化了向 TiDB Cloud Serverless 的数据迁移。你可以使用 AccessKey pair 进行认证。

    更多信息，参见以下文档：

    - [Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**通用变更**

- [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md) 功能现已在托管于 AWS 和 Google Cloud 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上正式发布（GA）。

    该功能支持在单个集群内实现**细粒度计算资源隔离**，帮助你在多租户或多工作负载场景下优化性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点分组为逻辑隔离单元，确保一个组内的工作负载不会影响其他组。
        - 防止应用或业务单元间的资源争用。

    - **简化管理**：

        - 在单个集群内统一管理所有节点组，降低运维负担。
        - 可按需独立扩缩各节点组。

  更多优势，参见 [技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。快速上手，参见 [Manage TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md)。

- 在托管于 AWS 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中引入 [Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage) 类型的 TiKV 节点。

    Standard 存储类型适用于大多数工作负载，在性能和成本之间实现平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志预留充足磁盘资源，减少 Raft 与数据存储的 I/O 争用，提升 TiKV 读写性能。
    - **稳定性增强**：将关键 Raft 操作与数据工作负载隔离，确保性能更可预测。
    - **成本效益**：与之前的存储类型相比，以更具竞争力的价格提供更高性能。

    **可用性：**

    Standard 存储类型会自动应用于 2025 年 4 月 1 日及以后在 AWS 上新建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，需使用支持的版本（>= 7.5.5、8.1.2 或 8.5.0）。现有集群仍使用之前的 [Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage) 类型，无需迁移。

    Standard 存储类型的价格与 Basic 存储类型不同。更多信息，参见 [Pricing](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现已支持为公网端点配置防火墙规则。

    你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中为 TiDB Cloud Serverless 集群配置防火墙规则，控制公网端点的访问。可直接指定允许的 IP 地址或范围，提升安全性。

    更多信息，参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**通用变更**

- 支持为部署在 Google Cloud 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    更多信息，参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持将数据库审计日志文件存储在 TiDB Cloud，用于部署在 AWS 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。该功能仅支持按需申请。

    更多信息，参见 [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md)。

- 通过优化多因素认证（MFA）管理，提升 TiDB Cloud 账号安全性。该功能适用于 TiDB Cloud 的密码登录。

    更多信息，参见 [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 推出 Connected Care，TiDB Cloud 的全新支持服务。

    Connected Care 服务通过现代通信工具、主动支持和先进的 AI 能力，增强你与 TiDB Cloud 的连接，带来无缝且以客户为中心的体验。

    Connected Care 服务包含以下功能：

    - **Clinic service**：高级监控与诊断，优化性能。
    - **AI chat in IM**：通过即时通讯工具获得 AI 实时协助。
    - **IM subscription for alerts and ticket updates**：通过 IM 实时获取告警和工单进展。
    - **IM interaction for support tickets**：可通过 IM 工具创建和跟进支持工单。

  更多信息，参见 [Connected Care Overview](/tidb-cloud/connected-care-overview.md)。

- 支持从 GCS 和 Azure Blob Storage 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    TiDB Cloud Serverless 现已支持从 Google Cloud Storage（GCS）和 Azure Blob Storage 导入数据。你可以使用 Google Cloud 服务账号密钥或 Azure SAS token 进行认证。该功能简化了向 TiDB Cloud Serverless 的数据迁移。

    更多信息，参见 [Import CSV Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [Import Apache Parquet Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现已支持每次任务导入单个本地 CSV 文件，文件大小上限由 50 MiB 提升至 250 MiB。

    更多信息，参见 [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已支持新的 AWS 区域：`Jakarta (ap-southeast-3)`。

- 推出 Notification 功能，让你可通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 实时获取 TiDB Cloud 更新和告警。

    更多信息，参见 [Notifications](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**通用变更**

- 支持为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    更多信息，参见 [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过 Private Connect（beta）将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群连接到 AWS 和 Google Cloud 上的通用 Kafka。

    Private Connect 利用云服务商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 内的 changefeed 可通过私有 IP 连接到客户 VPC 内的 Kafka，就像这些 Kafka 直接托管在 TiDB Cloud VPC 内一样。该功能有助于避免 VPC CIDR 冲突，满足安全合规要求。

    - 对于 AWS 上的 Apache Kafka，请参见 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 配置网络连接。

    - 对于 Google Cloud 上的 Apache Kafka，请参见 [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 配置网络连接。

  注意，使用该功能会产生额外的 [Private Data Link costs](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    更多信息，参见 [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- Kafka changefeed 新增可配置选项：

    - 支持使用 Debezium 协议。Debezium 是一种数据库变更捕获工具，将每个捕获的数据库变更转换为事件消息并发送到 Kafka。更多信息，参见 [TiCDC Debezium Protocol](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表定义单一分区分发器，或为不同表定义不同的分区分发器。

    - 新增两种分区分发器类型：按时间戳和按列值分发。

  更多信息，参见 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- TiDB Cloud 角色增强：

    - 新增 `Project Viewer` 和 `Organization Billing Viewer` 角色，实现更细粒度的访问控制。

    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  更多信息，参见 [Identity Access Management](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群区域高可用性（beta）。

    该功能适用于对基础设施冗余和业务连续性要求极高的工作负载。主要功能包括：

    - 节点分布在多个可用区，确保单区故障时的高可用性。
    - 关键 OLTP 组件（如 PD 和 TiKV）在可用区间冗余部署。
    - 主区故障时自动故障转移，最小化服务中断。

  该功能目前仅在 AWS 东京（ap-northeast-1）区域提供，且只能在集群创建时启用。

    更多信息，参见 [High Availability in TiDB Cloud Serverless](/tidb-cloud/serverless-high-availability.md)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级至 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 数据导出服务增强：

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据导出到 Google Cloud Storage 和 Azure Blob Storage。

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 导出 Parquet 文件格式数据。

  更多信息，参见 [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) 和 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md)。
