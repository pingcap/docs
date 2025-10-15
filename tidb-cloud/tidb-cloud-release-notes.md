---
title: 2025 年 TiDB Cloud 发布说明
summary: 了解 2025 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2025 年的发布说明。

## 2025 年 10 月 14 日

**通用变更**

- **TiDB Cloud Starter**

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 不再支持数据库审计日志。

        目前，只有 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持数据库审计日志。当前正在使用数据库审计日志的现有 TiDB Cloud Starter 集群不受影响。

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 移除了原地恢复功能，这意味着你无法再将备份直接恢复到同一个集群。此更改有助于防止误覆盖活跃生产数据和潜在数据丢失。

        若需恢复数据，你可以[将备份恢复到新集群](/tidb-cloud/backup-and-restore-serverless.md#perform-the-restore)。在验证恢复的数据后，将你的应用切换到新集群。已在现有集群中恢复的数据保持不变，除非你执行新的恢复，否则无需操作。

        若需更安全、可控且灵活的恢复和迁移流程，建议使用 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)。

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的 [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面新增以下指标，便于更快诊断和容量规划：

        - `Lock-wait (P95/P99)`：监控锁等待时间分位数，定位争用热点。
        - `Idle Connection Duration (P99 incl. not/in txn)`：识别长时间空闲连接（包括事务内和非事务内），以便调整连接池限制和超时设置。

- **TiDB Cloud Essential**

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在 AWS <CustomContent language="en,zh">和阿里云</CustomContent> 上公测。

        对于负载持续增长、需要实时扩展的应用，TiDB Cloud Essential 提供了灵活性和性能，助力业务增长。

        <CustomContent language="en,zh">

        详情参见 [TiDB Cloud Essential 现已在 AWS 和阿里云公测](https://www.pingcap.com/blog/tidb-cloud-essential-now-available-public-preview-aws-alibaba-cloud/)。

        </CustomContent>

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 现已在 [TiDB Cloud 控制台](https://tidbcloud.com) 支持数据库审计日志，并支持自定义轮转设置。

        你可以将数据库审计日志存储在 TiDB Cloud、Amazon S3、Google Cloud Storage、Azure Blob Storage 或阿里云 OSS。

        目前该功能为 Beta 版。详情参见 [TiDB Cloud Essential 数据库审计日志](/tidb-cloud/essential-database-audit-logging.md)。

    - TiDB Cloud Essential 新增事件 `ResourceLimitation`，当集群的 Request Capacity Units（RCUs）消耗在一小时内多次达到配置上限时会通知你。

        超出限制的用量可能会被限流。为避免服务影响，建议提升最大 RCU。

        事件详情参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 的 [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面新增以下指标，便于更快诊断和容量规划：

        - `Capacity vs Usage (RU/s)`：可视化已配置的 Request Unit（RU）容量与实际 RU 消耗，便于发现冗余空间并优化自动扩缩容。
        - `Lock-wait (P95/P99)`：监控锁等待时间分位数，定位争用热点。
        - `Idle Connection Duration (P99 incl. not/in txn)`：识别长时间空闲连接（包括事务内和非事务内），以便调整连接池限制和超时设置。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2025 年 9 月 30 日

**通用变更**

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已正式（GA）支持 Datadog 和 New Relic 集成。
  
        TiDB Cloud 现以集群为粒度管理 Datadog 和 New Relic 集成，提供更细致的控制和配置。该功能可让你将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控指标无缝发送到 Datadog 或 New Relic，实现统一平台下的高级告警。
  
        集成步骤参见 [集成 TiDB Cloud 与 Datadog](/tidb-cloud/monitor-datadog-integration.md) 和 [集成 TiDB Cloud 与 New Relic](/tidb-cloud/monitor-new-relic-integration.md)。
  
        若需将现有 Datadog 和 New Relic 集成迁移到集群级别，参见 [迁移 Datadog 和 New Relic 集成](/tidb-cloud/migrate-metrics-integrations.md)。

## 2025 年 9 月 23 日

**通用变更**

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 支持用户自定义 `UPDATE` 事件拆分。
  
        在 TiDB Cloud Dedicated 集群中，你可以配置是否将 `UPDATE` 事件保留为原始事件，或拆分为单独的 `DELETE` 和 `INSERT` 事件。该功能为高级同步场景提供更大灵活性。
  
        该功能仅支持非 SQL 目的地，如 Apache Kafka 和 Amazon S3。详情参见 [同步到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)、[同步到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md) 和 [同步到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

        拆分行为详情参见 [为非 MySQL sink 拆分主键或唯一键 `UPDATE` 事件](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（Google Cloud 托管）新增节点规格：`32 vCPU, 64 GiB`。
  
        该节点规格适用于 TiDB 节点。

## 2025 年 9 月 16 日

**通用变更**

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（Azure 托管）支持使用客户自管加密密钥（CMEK）进行静态加密。
  
        该功能允许你使用自有加密密钥保护静态数据。CMEK 带来以下优势：
  
        - 数据安全：你拥有并管理加密密钥，确保数据受保护且可控。
        - 合规性：使用 CMEK 有助于满足数据加密的合规和监管要求。
        - 灵活性：你可在创建项目时启用 CMEK，并在创建集群前完成配置。
  
      启用步骤如下：
  
        1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 创建支持 CMEK 的项目。
        2. 完成该项目的 CMEK 配置。
        3. 在与 CMEK 配置相同区域创建 Azure 托管的 TiDB Cloud Dedicated 集群。
  
      详情参见 [在 Azure 上使用客户自管加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)。

## 2025 年 9 月 9 日

**高可用性变更**

- **TiDB Cloud Starter**

    - 新建的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群仅启用可用区级高可用，且不可配置。
    - 2025 年 9 月 9 日前已启用区域级高可用的现有 TiDB Cloud Starter 集群，区域级高可用继续受支持，不受影响。

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - 新建的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群默认启用区域级高可用，你可在创建集群时根据需要切换为可用区级高可用。

  详情参见 [TiDB Cloud Starter 和 Essential 的高可用性](/tidb-cloud/serverless-high-availability.md)。

</CustomContent>

## 2025 年 9 月 2 日

**通用变更**

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群新增支持 3 个阿里云区域：`Jakarta (ap-southeast-5)`、`Mexico (na-south-1)` 和 `Tokyo (ap-northeast-1)`。

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) 升级为 [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)。

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) 升级为 [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/)。

</CustomContent>

## 2025 年 8 月 26 日

**通用变更**

- **TiDB Cloud Starter**

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 引入 Auto Embedding（Beta），可轻松将文本转为向量，无需额外配置。该功能让你能更快在 TiDB Cloud 上开发语义搜索、RAG、重排序和分类等场景，减少集成成本。

        - **支持主流 LLM 提供商的 Auto Embedding**：Amazon Titan、OpenAI、Cohere、Gemini、Jina AI、Hugging Face 和 NVIDIA NIM。
        - **原生集成 AWS Bedrock**：托管嵌入模型并提供免费额度，包括 AWS Bedrock 的 Amazon Titan 和 Cohere 文本嵌入模型。
        - **支持 SQL 和 Python**，并提供创建、存储和查询嵌入的代码示例。

      详情参见 [Auto Embedding](https://docs.pingcap.com/tidbcloud/vector-search-auto-embedding-overview/?plan=starter)。

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 不再支持 Index Insight（Beta）功能。

        推荐使用 [Index Advisor](/index-advisor.md)，适用于 TiDB v8.5.0 及以上版本。Index Advisor 引入了 `RECOMMEND INDEX` SQL 语句，帮助你通过推荐索引优化查询性能。

    - 你现在可以在启用每周备份的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上手动关闭时间点恢复（Point-in-time Restore）功能。

        该优化有助于降低不需要高 RPO 保护的集群的成本。

        详情参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 8 月 12 日

**通用变更**

<CustomContent language="en,zh">

- **TiDB Cloud Starter**

    - 将 “TiDB Cloud Serverless” 重命名为 “TiDB Cloud Starter”。

        自动扩缩容入门方案现称为 “TiDB Cloud Starter”，更好地体现其为新用户提供的角色。所有功能、价格和免费额度保持不变。

        自 2025 年 8 月 12 日（PDT）起，你现有的 Serverless 集群将在 [TiDB Cloud 控制台](https://tidbcloud.com) 中显示为 Starter。你的连接字符串、端点和数据均保持不变，无需修改代码或安排停机。

    - TiDB Cloud Starter 在阿里云公测。

- **TiDB Cloud Essential**

    [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在阿里云公测。

    TiDB Cloud Essential 在阿里云自 2025 年 5 月起已小范围公测。本次是 Essential 首次正式纳入发布说明。目前，Essential 在阿里云提供与 Starter 一致的功能集，支持阿里云新加坡区域。

    体验方式：

    - 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 创建集群时选择阿里云作为云服务商，即可看到 Essential 选项。
    - 你也可以通过 [阿里云 Marketplace 上的 Essential 列表](https://www.alibabacloud.com/en/marketplace/tidb?_p_lc=1) 访问。

  后续计划将扩展阿里云区域覆盖，并增加 AWS 支持。

    若你在公测期间体验 Essential on 阿里云，可通过 Web 控制台反馈，或加入 [Slack 社区](https://tidbcommunity.slack.com/archives/CH7TTLL7P) 或 [Discord 社区](https://discord.gg/ukhXbn69Nx) 交流。

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Google Cloud 上通过优化 NAT 子网分配策略，现支持每区域超过 8 个 Google Private Service Connect（PSC）连接。

        详情参见 [通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)。

    - 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 监控指标：

        - 在 [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) 分类下，新增 **Affected Rows**、**Leader Count** 和 **Region Count** 指标，提升诊断能力。
        - 在 [**Server**](/tidb-cloud/built-in-monitoring.md#server) 分类下，优化 **TiKV IO Bps** 指标，提升准确性和一致性。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Starter**

    将 “TiDB Cloud Serverless” 重命名为 “TiDB Cloud Starter”。

    自动扩缩容入门方案现称为 “TiDB Cloud Starter”，更好地体现其为新用户提供的角色。所有功能、价格和免费额度保持不变。

    自 2025 年 8 月 12 日（PDT）起，你现有的 Serverless 集群将在 [TiDB Cloud 控制台](https://tidbcloud.com) 中显示为 Starter。你的连接字符串、端点和数据均保持不变，无需修改代码或安排停机。

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Google Cloud 上通过优化 NAT 子网分配策略，现支持每区域超过 8 个 Google Private Service Connect（PSC）连接。

        详情参见 [通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)。

    - 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 监控指标：

        - 在 [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) 分类下，新增 **Affected Rows**、**Leader Count** 和 **Region Count** 指标，提升诊断能力。
        - 在 [**Server**](/tidb-cloud/built-in-monitoring.md#server) 分类下，优化 **TiKV IO Bps** 指标，提升准确性和一致性。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>

**API 变更**

- 推出 TiDB Cloud Dedicated API（v1beta1），可自动高效管理以下资源：

    - **Cluster**：更灵活地管理你的 TiDB Cloud Dedicated 集群。
    - **Region**：展示所有可部署 TiDB Cloud Dedicated 集群的云区域。
    - **Private endpoint connection**：为集群配置安全私有连接。
    - **Import**：管理集群的数据导入任务。

  详情参见 [TiDB Cloud Dedicated API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)。

- 推出 TiDB Cloud Starter 和 Essential API（v1beta1），可自动高效管理以下资源：

    - **Cluster**：更灵活地管理你的 TiDB Cloud Starter 或 Essential 集群。
    - **Branch**：管理集群的分支。
    - **Export**：管理集群的数据导出任务。
    - **Import**：管理集群的数据导入任务。

  详情参见 [TiDB Cloud Starter 和 Essential API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/)。

- TiDB Cloud IAM API（v1beta1）支持 API 密钥的基于角色的访问控制（RBAC），可在组织和项目级别管理。

    你可以在组织级或项目级设置 API 密钥角色，提升安全性和访问控制。

    详情参见 [TiDB Cloud IAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/)。

## 2025 年 7 月 31 日

**通用变更**

- 增强版 Datadog 和 New Relic 集成现已公测。

    主要增强点：

    - 重构集成后端，采用优化的隔离架构，最小化指标丢失。
    - 根据用户需求增加更多监控指标。
    - 优化指标规则，提升一致性。

  这些增强带来更准确的监控和更可靠的 Datadog、New Relic 集成。

  发布计划：

  本公测版本现已对未集成 Datadog 或 New Relic 的组织开放。对于已集成的组织，我们将在下月主动联系你，协商迁移方案和时间表。

  详情参见 [集成 TiDB Cloud 与 Datadog（公测）](/tidb-cloud/monitor-datadog-integration.md) 和 [集成 TiDB Cloud 与 New Relic（公测）](/tidb-cloud/monitor-new-relic-integration.md)。

## 2025 年 7 月 22 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（Google Cloud 托管）新增节点规格：`32 vCPU, 128 GiB`。

    该规格适用于 TiDB、TiKV 和 TiFlash 节点。

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 TiKV 扩缩容流程，提升集群稳定性。

    当你[更改 TiKV 节点的 vCPU 和内存规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)时，TiDB Cloud 会自动检查集群内部服务是否需扩容以支持新配置。

    - 若需扩容，TiDB Cloud 会提示你确认后再继续操作。
    - 若当前内部服务容量已大于扩容后所需，TiDB Cloud 会保留现有配置，避免不必要的变更影响集群稳定性。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的云存储数据导入体验。

    导入流程现简化为 3 步向导，并带有智能预检查。新向导引导你完成连接配置、文件映射和存储桶扫描。通过扫描，TiDB Cloud 会在导入前准确展示将被导入的文件及其目标位置，大幅降低配置复杂度并防止导入失败。

    详情参见以下文档：

    - [导入示例数据到 TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md)
    - [从云存储导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从云存储导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 7 月 15 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/) 升级为 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)。

    与 v8.1.2 相比，v8.5.2 包含 [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/)、[v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/)、[v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/)、[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/)、[v8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/) 和 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/) 的新特性、改进和修复。

- 支持审计 `BackupCompleted` 事件，增强备份活动的控制台审计日志。

    该增强可记录备份完成活动，满足安全与合规要求。

    详情参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 支持按列值过滤。

    你现在可以在 changefeed 中使用表达式过滤特定列值，从源头排除无关数据。该功能实现 DML 事件的细粒度过滤，帮助降低资源消耗并提升性能。

    详情参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。

## 2025 年 6 月 24 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 数据库审计日志（Beta）现可按需申请。该功能可记录用户访问详情（如执行的 SQL 语句）历史日志。

    申请方式：在 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角点击 **?**，选择 **Request Support**，在 Description 字段填写 “Apply for TiDB Cloud Serverless database audit logging”，点击 **Submit**。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户自主管理日志脱敏。

    你现在可以为 TiDB Cloud Dedicated 集群启用或关闭日志脱敏，自主管理集群日志的脱敏状态。

    详情参见 [用户自主管理日志脱敏](/tidb-cloud/tidb-cloud-log-redaction.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS 托管）现已正式（GA）支持使用客户自管加密密钥（CMEK）进行静态加密。

    该功能允许你通过 Key Management Service（KMS）管理的对称加密密钥保护静态数据。

    详情参见 [在 AWS 上使用客户自管加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)。

## 2025 年 6 月 17 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中，16 vCPU 和 32 vCPU 的 TiKV 节点最大存储容量由 **6144 GiB** 调整为 **4096 GiB**。

    详情参见 [TiKV 节点存储容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重构左侧导航栏，提升整体导航体验。
  
    - 左上角新增 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，可随时隐藏或显示左侧导航栏。
    - 左上角新增组合框，可快速在组织、项目和集群间切换，集中管理。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏的入口会根据组合框当前选择动态调整，帮助你聚焦最相关功能。
    - **Support**、**Notification** 和账号入口现始终显示在左侧导航栏底部，便于快速访问。

## 2025 年 6 月 4 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 Microsoft Azure 上公测。
  
    本次发布后，TiDB Cloud 已支持三大主流公有云平台 —— AWS、Google Cloud 和 Azure，助你根据业务需求和云战略灵活部署 TiDB Cloud Dedicated 集群。
  
    - AWS 和 Google Cloud 上的所有核心功能在 Azure 上均已支持。
    - 目前 Azure 支持 East US 2、日本东部和东南亚 3 个区域，后续将支持更多区域。
    - Azure 上的 TiDB Cloud Dedicated 集群需 TiDB 版本 v7.5.3 或更高。
  
  快速入门文档：
  
    - [在 Azure 上创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)
    - [通过 Azure Private Endpoint 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 
    - [在 Azure 上导入数据到 TiDB Cloud Dedicated 集群](/tidb-cloud/import-csv-files.md)

- Prometheus 集成为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供更多监控指标。

    你现在可以将 `tidbcloud_disk_read_latency`、`tidbcloud_kv_request_duration` 等更多指标集成到 Prometheus，监控 TiDB Cloud Dedicated 的更多性能维度。

    可用指标及启用方法参见 [集成 TiDB Cloud 与 Prometheus 和 Grafana（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储价格正式发布。

    优惠期自 **2025 年 6 月 5 日 00:00 UTC** 起结束，之后恢复标准价格。详情参见 [TiDB Cloud Dedicated 价格明细](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点规格配置交互体验。

    你现在可以在创建 TiDB Cloud Dedicated 集群时通过开关控制 TiFlash 配置，提升配置的直观性和流畅性。

## 2025 年 5 月 27 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 changefeed 支持将数据流式同步到 [Apache Pulsar](https://pulsar.apache.org)。

    该功能让你能将 TiDB Cloud Dedicated 集群与更多下游系统集成，满足更多数据集成需求。使用该功能需确保集群版本为 v7.5.1 或更高。

    详情参见 [同步到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已支持全文检索（Beta），适用于 AI 应用。

    TiDB Cloud Serverless 现支持全文检索（Beta），使 AI 和 RAG（检索增强生成）应用可通过精确关键词检索内容。该功能补充了向量检索（按语义相似度检索内容），两者结合可显著提升 RAG 工作流的检索准确性和答案质量。主要特性包括：

    - 直接文本检索：可直接查询字符串列，无需嵌入。
    - 多语言支持：自动检测并分析多语言文本，单表内多语言无需指定语言。
    - 基于相关性的排序：结果采用业界标准 BM25 算法排序，相关性最佳。
    - 原生 SQL 兼容：可与 SQL 过滤、分组、关联等功能无缝结合。

  快速入门参见 [使用 SQL 进行全文检索](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [使用 Python 进行全文检索](/tidb-cloud/vector-search-full-text-search-python.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点最大存储容量提升：

    - 8 vCPU TiFlash：由 2048 GiB 提升至 4096 GiB
    - 32 vCPU TiFlash：由 4096 GiB 提升至 8192 GiB

  该增强提升了 TiDB Cloud Dedicated 集群的分析型数据存储能力，提高了负载扩展效率，满足不断增长的数据需求。

    详情参见 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 维护窗口配置体验优化，提供更直观的选项以配置和重新安排维护任务。

    详情参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型优惠期延长至 2025 年 6 月 5 日，届时价格恢复为标准价。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 **Backup Setting** 页面布局，提升备份配置体验。

    详情参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**通用变更**

- 现已支持导出数据到阿里云 OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群现支持使用 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 将数据导出到 [阿里云对象存储 OSS](https://www.alibabacloud.com/en/product/object-storage-service)。

    详情参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群 TiDB 版本由 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3) 升级为 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2025 年 4 月 15 日

**通用变更**

- 支持从 [阿里云对象存储 OSS](https://www.alibabacloud.com/en/product/object-storage-service) 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。

    该功能简化了数据迁移到 TiDB Cloud Serverless 的流程。你可以使用 AccessKey 对进行认证。

    详情参见以下文档：

    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**通用变更**

- [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md) 功能现已在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS 和 Google Cloud 托管）正式发布（GA）。

    该功能支持在单集群内实现**细粒度计算资源隔离**，帮助你为多租户或多业务场景优化性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点分组为逻辑隔离单元，确保一个组的负载不会影响其他组。
        - 防止应用或业务单元间的资源争用。

    - **简化管理**：

        - 在单集群内统一管理所有节点组，降低运维复杂度。
        - 可按需独立扩缩各节点组。

  详细优势参见 [技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。快速入门参见 [管理 TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS 托管）引入 [Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage) 类型的 TiKV 节点。

    Standard 存储类型适用于大多数负载，在性能和成本之间实现平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志预留充足磁盘资源，减少 Raft 与数据存储的 I/O 争用，提升 TiKV 读写性能。
    - **稳定性增强**：将关键 Raft 操作与数据负载隔离，确保性能更可预测。
    - **成本效益**：与原有存储类型相比，提供更高性能且价格更具竞争力。

    **可用性：**

    2025 年 4 月 1 日及以后新建的 AWS 托管 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，且版本 >= 7.5.5、8.1.2 或 8.5.0，自动采用 Standard 存储类型。现有集群仍使用原有 [Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage) 类型，无需迁移。

    Standard 存储类型价格与 Basic 存储不同。详情参见 [价格说明](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持为公网端点配置防火墙规则。

    你现在可以为 TiDB Cloud Serverless 集群配置防火墙规则，控制公网端点的访问。可在 [TiDB Cloud 控制台](https://tidbcloud.com/) 直接指定允许的 IP 地址或范围，提升安全性。

    详情参见 [为 TiDB Cloud Serverless 公网端点配置防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（Google Cloud 部署）支持创建 TiDB 节点组，提升资源管理灵活性。

    详情参见 [TiDB Node Group 概览](/tidb-cloud/tidb-node-group-overview.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS 部署）支持将数据库审计日志文件存储在 TiDB Cloud。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。该功能仅支持按需申请。

    详情参见 [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

- 提升 TiDB Cloud 账号安全性，优化多因素认证（MFA）管理。该功能适用于 TiDB Cloud 的密码登录。

    详情参见 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 推出 Connected Care，TiDB Cloud 的新一代支持服务。

    Connected Care 服务通过现代通信工具、主动支持和先进 AI 能力，增强你与 TiDB Cloud 的连接，带来无缝、以客户为中心的体验。

    Connected Care 服务包括：

    - **Clinic service**：高级监控与诊断，优化性能。
    - **AI chat in IM**：通过即时通讯工具获得 AI 实时帮助。
    - **IM 订阅告警与工单进展**：通过 IM 实时获知告警和工单进度。
    - **IM 工单交互**：可通过 IM 工具创建和跟进支持工单。

  详情参见 [Connected Care 概览](/tidb-cloud/connected-care-overview.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持从 GCS 和 Azure Blob Storage 导入数据。

    你现在可以使用 Google Cloud 服务账号密钥或 Azure SAS Token 认证，从 Google Cloud Storage（GCS）和 Azure Blob Storage 导入数据到 TiDB Cloud Serverless，简化数据迁移。

    详情参见 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群单次任务支持导入最大 250 MiB 的本地 CSV 文件（原上限为 50 MiB）。

    详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增支持 AWS 区域：`Jakarta (ap-southeast-3)`。

- 推出 Notification 功能，可通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 实时获知 TiDB Cloud 更新和告警。

    详情参见 [通知](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持创建 TiDB 节点组，提升资源管理灵活性。

    详情参见 [TiDB Node Group 概览](/tidb-cloud/tidb-node-group-overview.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持通过 Private Connect（Beta）连接 AWS 和 Google Cloud 上的通用 Kafka。

    Private Connect 利用云服务商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 内的 changefeed 可通过私有 IP 连接客户 VPC 内的 Kafka，仿佛 Kafka 部署在 TiDB Cloud VPC 内。该功能有助于避免 VPC CIDR 冲突并满足安全合规要求。

    - AWS 上的 Apache Kafka，参见 [在 AWS 上配置自建 Kafka Private Link 服务](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)。

    - Google Cloud 上的 Apache Kafka，参见 [在 Google Cloud 上配置自建 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)。
  
  注意，使用该功能会产生额外的 [Private Data Link 费用](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    详情参见 [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- Kafka changefeed 新增可配置选项：

    - 支持使用 Debezium 协议。Debezium 是数据库变更捕获工具，将每个变更转为事件消息并发送到 Kafka。详情参见 [TiCDC Debezium 协议](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表定义单一分区分发器，或为不同表定义不同分区分发器。

    - 新增两种分发器类型：按时间戳和按列值分区。

  详情参见 [同步到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- TiDB Cloud 角色增强：

    - 新增 `Project Viewer` 和 `Organization Billing Viewer` 角色，实现更细粒度的访问控制。

    - 以下角色重命名：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  详情参见 [身份访问管理](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群区域级高可用（Beta）。

    该功能适用于对基础设施冗余和业务连续性要求极高的负载。主要特性：

    - 节点分布于多个可用区，确保单区故障时高可用。
    - 关键 OLTP 组件（如 PD、TiKV）跨可用区冗余部署。
    - 主区故障时自动故障转移，最小化服务中断。
  
  目前仅 AWS 东京（ap-northeast-1）区域支持，且仅在集群创建时可启用。
  
    详情参见 [TiDB Cloud Serverless 高可用性](/tidb-cloud/serverless-high-availability.md)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级为 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 数据导出服务增强：

    - [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 导出数据到 Google Cloud Storage 和 Azure Blob Storage。

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 导出 Parquet 文件格式数据。

  详情参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md) 和 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。
