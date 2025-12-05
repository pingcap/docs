---
title: 2025 年 TiDB Cloud 发布说明
summary: 了解 2025 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2025 年的发布说明。

## 2025 年 12 月 2 日

**通用变更**

- **TiDB Cloud Dedicated**

    - Prometheus 集成现已在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中正式发布（GA）。

        TiDB Cloud 现在在集群级别管理 Prometheus 集成，提供更细粒度的控制和配置。该功能使你能够无缝地将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控指标发送到 Prometheus，从而在统一平台上实现高级告警。

        集成步骤详见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

        如需将现有 Prometheus 集成迁移到集群级别，请参见 [迁移 Prometheus 集成](/tidb-cloud/migrate-prometheus-metrics-integrations.md)。

## 2025 年 11 月 18 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 增强 changefeed 摘要，包含完整的配置信息。

        之前，你需要暂停 changefeed 才能查看其配置，然后再恢复。现在 **Changefeed** 页面在摘要视图中直接显示完整配置。此次更新保持了编辑和查看模式的一致性，并引入了重新设计的布局以提升可读性。通过本次更新，你可以更高效地审查当前配置。

        详情参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。

## 2025 年 11 月 11 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 当你从备份恢复 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群到新集群时，现在可以为新集群选择节点存储类型（如 [标准存储](/tidb-cloud/size-your-cluster.md#standard-storage)），而不再局限于默认存储类型。

        该功能使你可以精确还原原始配置，或选择更适合需求的存储类型。

        详情参见 [将数据恢复到新集群](/tidb-cloud/backup-and-restore.md#restore-data-to-a-new-cluster)。

## 2025 年 11 月 4 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 当你通过 VPC Peering 连接托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群时，现在可以直接在 [TiDB Cloud 控制台](https://tidbcloud.com/) 配置 `/16` 到 `/18` 之间的 IP 段大小，无需再联系 TiDB Cloud 支持。

        详情参见 [通过 VPC Peering 连接 TiDB Cloud Dedicated](/tidb-cloud/set-up-vpc-peering-connections.md)。

    - TiDB Cloud Dedicated现在为 4 vCPU 节点规格提供更清晰的指引和提示。该节点规格仅适用于测试、学习和探索 TiDB Cloud 功能的非生产环境。

        详情参见 [确定 TiDB 规格](/tidb-cloud/size-your-cluster.md)。

## 2025 年 10 月 28 日

**通用变更**

- **TiDB Cloud Starter 和 TiDB Cloud Essential**

    为提升连接稳定性并防止 TiDB 服务器重启或维护期间出现意外断连，建议你将数据库连接的最大生命周期设置为小于 30 分钟。

    详情参见 [配置连接的生命周期](/develop/dev-guide-connection-parameters.md#configure-the-lifetime-of-connections)。

**API 变更**

- **TiDB Cloud Dedicated**

    新增以下 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) API 端点，用于管理第三方监控集成：

    - 列出集成
    - 创建集成
    - 删除集成

  详情参见 [TiDB Cloud Dedicated API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)。

## 2025 年 10 月 21 日

**通用变更**

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 增强了 [Changefeed](/tidb-cloud/changefeed-overview.md) 的私有端点功能，简化配置、提升安全性，并为数据下游提供更大灵活性。

        - **简化配置**：私有端点的创建现已与 changefeed 创建解耦，同一项目下的多个 changefeed 可共享一个私有端点，减少冗余配置。
        - **MySQL 私有链路下游**：为数据下沉到 MySQL 提供更安全的方式，并支持通过私有链路直接下沉到另一个 TiDB Cloud Dedicated 集群。
        - **自定义域名支持**：使用自建 Kafka 服务时，可为数据下游配置自定义域名，提升安全性，并使监听器更新更灵活，无需重启服务器。

      详情参见 [为 Changefeed 设置私有端点](/tidb-cloud/set-up-sink-private-endpoint.md)。

    - [Prometheus 集成（预览）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) 现已适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

        TiDB Cloud 现在在集群级别管理 Prometheus 集成，提供更细粒度的控制和配置。该功能使你能够无缝地将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控指标发送到 Prometheus，从而在统一平台上实现高级告警。

        详情参见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

## 2025 年 10 月 14 日

**通用变更**

- **TiDB Cloud Starter**

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 不再支持数据库审计日志。

        目前，仅 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持数据库审计日志。现有已启用数据库审计日志的 TiDB Cloud Starter 集群不受影响。

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 移除了原地恢复功能，即不再支持将备份直接恢复到同一集群。此更改有助于防止误覆盖生产数据和潜在数据丢失。

        如需恢复数据，你可以 [将备份恢复到新集群](/tidb-cloud/backup-and-restore-serverless.md#perform-the-restore)。验证恢复数据后，将应用切换到新集群。已在现有集群中恢复的数据不受影响，除非你执行新的恢复操作。

        如需更安全、可控和灵活的数据恢复与迁移流程，建议使用 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)。

    - [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面为 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 新增以下指标，便于更快诊断和容量规划：

        - `Lock-wait (P95/P99)`：监控锁等待时间分位数，定位争用热点。
        - `Idle Connection Duration (P99 incl. not/in txn)`：识别长时间空闲连接（包括事务内和非事务内），以便调整连接池限制和超时。

- **TiDB Cloud Essential**

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在 AWS <CustomContent language="en,zh">和阿里云</CustomContent> 公测中。

        对于业务负载持续增长、需要实时扩展的应用，TiDB Cloud Essential 提供了灵活性和性能，助力业务发展。

        <CustomContent language="en,zh">

        详情参见 [TiDB Cloud Essential 现已在 AWS 和阿里云公测](https://www.pingcap.com/blog/tidb-cloud-essential-now-available-public-preview-aws-alibaba-cloud/)。

        </CustomContent>

    - 数据库审计日志现已在 [TiDB Cloud 控制台](https://tidbcloud.com) 上支持 TiDB Cloud Essential，并支持自定义轮转设置。

        你可以将数据库审计日志存储在 TiDB Cloud、Amazon S3、Google Cloud Storage、Azure Blob Storage 或阿里云 OSS。

        目前该功能为 beta 版。详情参见 [TiDB Cloud Essential 数据库审计日志](/tidb-cloud/essential-database-audit-logging.md)。

    - TiDB Cloud Essential 新增事件 `ResourceLimitation`，当集群的 Request Capacity Units（RCUs）消耗在一小时内多次达到配置上限时通知你。

        超出限制的用量可能会被限流。为避免服务影响，建议提升最大 RCU。

        事件详情参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

    - [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面为 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 新增以下指标，便于更快诊断和容量规划：

        - `Capacity vs Usage (RU/s)`：可视化已配置的 Request Unit（RU）容量与实际消耗，便于发现冗余空间和优化自动扩缩容。
        - `Lock-wait (P95/P99)`：监控锁等待时间分位数，定位争用热点。
        - `Idle Connection Duration (P99 incl. not/in txn)`：识别长时间空闲连接（包括事务内和非事务内），以便调整连接池限制和超时。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2025 年 9 月 30 日

**通用变更**

- **TiDB Cloud Dedicated**

    - Datadog 和 New Relic 集成现已在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中正式发布（GA）。
  
        TiDB Cloud 现在在集群级别管理 Datadog 和 New Relic 集成，提供更细粒度的控制和配置。该功能使你能够无缝地将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控指标发送到 Datadog 或 New Relic，从而在统一平台上实现高级告警。
  
        集成步骤详见 [将 TiDB Cloud 集成到 Datadog](/tidb-cloud/monitor-datadog-integration.md) 和 [将 TiDB Cloud 集成到 New Relic](/tidb-cloud/monitor-new-relic-integration.md)。
  
        如需将现有 Datadog 和 New Relic 集成迁移到集群级别，请参见 [迁移 Datadog 和 New Relic 集成](/tidb-cloud/migrate-metrics-integrations.md)。

## 2025 年 9 月 23 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 中由用户控制 `UPDATE` 事件的拆分。
  
        在 TiDB Cloud Dedicated 集群中，你可以配置是否将 `UPDATE` 事件保留为原始事件，或拆分为单独的 `DELETE` 和 `INSERT` 事件。该功能为高级同步场景提供更大灵活性。
  
        该功能仅支持非 SQL 下游，如 Apache Kafka 和 Amazon S3。详情参见 [下沉到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)、[下沉到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md) 和 [下沉到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

        关于拆分行为的更多信息，参见 [为非 MySQL 下游拆分主键或唯一键 `UPDATE` 事件](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

    - 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的节点规格：`32 vCPU, 64 GiB`。
  
        该节点规格适用于 TiDB 节点。

## 2025 年 9 月 16 日

**通用变更**

- **TiDB Cloud Dedicated**

    - Azure 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已支持使用客户自管加密密钥（CMEK）进行静态加密。
  
        该功能允许你使用自主管理的加密密钥保护静态数据。CMEK 主要优势如下：
  
        - 数据安全：你拥有并管理加密密钥，确保数据受保护且可控。
        - 合规性：使用 CMEK 有助于满足数据加密的合规和监管要求。
        - 灵活性：你可以在创建项目时启用 CMEK，并在创建集群前完成相关配置。
  
      启用步骤如下：
  
        1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 创建启用 CMEK 的项目。
        2. 完成该项目的 CMEK 配置。
        3. 在与 CMEK 配置相同的区域创建 Azure 上的 TiDB Cloud Dedicated 集群。
  
      详情参见 [在 Azure 上使用客户自管加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)。

## 2025 年 9 月 9 日

**高可用性变更**

- **TiDB Cloud Starter**

    - 新创建的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群仅启用可用区级高可用性，且不可配置。
    - 2025 年 9 月 9 日前已启用区域级高可用性的现有 TiDB Cloud Starter 集群不受影响。

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - 新创建的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群默认启用区域级高可用性，你可在集群创建时根据需要切换为可用区级高可用性。

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

    - 在 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 引入 Auto Embedding（Beta），让你无需额外配置即可将文本转换为向量。该功能可加速在 TiDB Cloud 中开发语义搜索、RAG、重排序和分类等场景，降低集成成本。

        - **与主流 LLM 提供商的 Auto Embedding**：Amazon Titan、OpenAI、Cohere、Gemini、Jina AI、Hugging Face 和 NVIDIA NIM。
        - **原生集成 AWS Bedrock**：支持 AWS Bedrock 的托管 embedding 模型（含免费额度），包括 Amazon Titan 和 Cohere 文本 embedding 模型。
        - **支持 SQL 和 Python**，并提供创建、存储和查询 embedding 的代码示例。

      详情参见 [Auto Embedding](https://docs.pingcap.com/tidbcloud/vector-search-auto-embedding-overview/?plan=starter)。

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 不再支持 Index Insight（beta）功能。

        建议改用 [Index Advisor](/index-advisor.md)，该功能适用于 TiDB v8.5.0 及以上版本。Index Advisor 引入了 `RECOMMEND INDEX` SQL 语句，帮助你通过推荐索引优化查询性能。

    - 你现在可以在启用每周备份的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上手动关闭时间点恢复（Point-in-time Restore）功能。

        此优化有助于降低不需要高 RPO 保护的集群的成本。

        详情参见 [备份与恢复 TiDB Cloud Dedicated数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 8 月 12 日

**通用变更**

<CustomContent language="en,zh">

- **TiDB Cloud Starter**

    - 将 “TiDB Cloud Serverless” 更名为 “TiDB Cloud Starter”。

        自动扩缩容入门方案现称为 “TiDB Cloud Starter”，更好地体现其为新用户提供的定位。所有功能、定价和免费额度保持不变。

        自 2025 年 8 月 12 日（PDT）起，你的现有 Serverless 集群将在 [TiDB Cloud 控制台](https://tidbcloud.com) 中显示为 Starter。你的连接字符串、端点和数据均保持不变，无需修改代码或安排停机。

    - TiDB Cloud Starter 在阿里云公测。

- **TiDB Cloud Essential**

    [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在阿里云公测。

    TiDB Cloud Essential on 阿里云自 2025 年 5 月起已小范围公测。本次为首次在发布说明中正式纳入 Essential。当前阶段，Essential on 阿里云的功能集与 Starter 保持一致，现已支持阿里云新加坡区域。

    试用方法：

    - 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 创建集群时选择阿里云作为云服务商，即可看到 Essential 选项。
    - 你也可以通过 [阿里云 Marketplace 上的 Essential 产品页](https://www.alibabacloud.com/en/marketplace/tidb?_p_lc=1) 访问。

  下一步计划扩展阿里云区域覆盖，并增加 AWS 支持。

    如果你在公测期间试用 Essential on 阿里云，可通过 Web 控制台反馈，也欢迎加入 [Slack](https://tidbcommunity.slack.com/archives/CH7TTLL7P) 或 [Discord](https://discord.gg/ukhXbn69Nx) 社区交流。

- **TiDB Cloud Dedicated**

    - Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现已通过优化 NAT 子网分配策略，支持每区域超过 8 个 Google Private Service Connect（PSC）连接。

        详情参见 [通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)。

    - 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 监控指标：

        - 在 [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) 类别下，新增 **Affected Rows**、**Leader Count** 和 **Region Count** 指标，提升诊断能力。
        - 在 [**Server**](/tidb-cloud/built-in-monitoring.md#server) 类别下，优化 **TiKV IO Bps** 指标，提升准确性和一致性。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Starter**

    将 “TiDB Cloud Serverless” 更名为 “TiDB Cloud Starter”。

    自动扩缩容入门方案现称为 “TiDB Cloud Starter”，更好地体现其为新用户提供的定位。所有功能、定价和免费额度保持不变。

    自 2025 年 8 月 12 日（PDT）起，你的现有 Serverless 集群将在 [TiDB Cloud 控制台](https://tidbcloud.com) 中显示为 Starter。你的连接字符串、端点和数据均保持不变，无需修改代码或安排停机。

- **TiDB Cloud Dedicated**

    - Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现已通过优化 NAT 子网分配策略，支持每区域超过 8 个 Google Private Service Connect（PSC）连接。

        详情参见 [通过 Google Cloud Private Service Connect 连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions)。

    - 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 监控指标：

        - 在 [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) 类别下，新增 **Affected Rows**、**Leader Count** 和 **Region Count** 指标，提升诊断能力。
        - 在 [**Server**](/tidb-cloud/built-in-monitoring.md#server) 类别下，优化 **TiKV IO Bps** 指标，提升准确性和一致性。

      详情参见 [TiDB Cloud 内置监控指标](/tidb-cloud/built-in-monitoring.md)。

</CustomContent>

**API 变更**

- 推出 TiDB Cloud Dedicated API（v1beta1），可自动高效地管理以下资源：

    - **Cluster**：更灵活地管理 TiDB Cloud Dedicated 集群。
    - **Region**：展示可部署 TiDB Cloud Dedicated 集群的所有云区域。
    - **Private endpoint connection**：为集群设置安全私有连接。
    - **Import**：管理集群的数据导入任务。

  详情参见 [TiDB Cloud Dedicated API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/)。

- 推出 TiDB Cloud Starter 和 Essential API（v1beta1），可自动高效地管理以下资源：

    - **Cluster**：更灵活地管理 TiDB Cloud Starter 或 Essential 集群。
    - **Branch**：管理集群的分支。
    - **Export**：管理集群的数据导出任务。
    - **Import**：管理集群的数据导入任务。

  详情参见 [TiDB Cloud Starter 和 Essential API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/)。

- TiDB Cloud IAM API（v1beta1）支持 API 密钥的基于角色的访问控制（RBAC），可在组织和项目级别进行管理。

    你可以在组织级或项目级设置 API 密钥角色，以提升安全性和访问控制。

    详情参见 [TiDB Cloud IAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/)。

## 2025 年 7 月 31 日

**通用变更**

- 增强版 Datadog 和 New Relic 集成现已开放预览。

    主要增强点：

    - 重构集成后端，采用优化的隔离架构，最小化监控指标丢失。
    - 根据用户需求新增更多监控指标。
    - 优化指标规则，提升一致性。

  这些增强带来更准确的监控和更可靠的 Datadog、New Relic 集成。

  发布计划：

  该预览版现已面向未使用 Datadog 或 New Relic 集成的组织开放。对于已集成的组织，我们将在下月主动联系你，协商合适的迁移方案和时间表。

  详情参见 [将 TiDB Cloud 集成到 Datadog（预览）](/tidb-cloud/monitor-datadog-integration.md) 和 [将 TiDB Cloud 集成到 New Relic（预览）](/tidb-cloud/monitor-new-relic-integration.md)。

## 2025 年 7 月 22 日

**通用变更**

- 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的节点规格：`32 vCPU, 128 GiB`。

    该规格适用于 TiDB、TiKV 和 TiFlash 节点。

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 TiKV 扩缩容流程，提升集群稳定性。

    当你 [更改 TiKV 节点的 vCPU 和内存规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 时，TiDB Cloud 会自动检查集群内部服务是否需要扩容以支持新配置。

    - 若需扩容，TiDB Cloud 会提示你确认后再执行。
    - 若扩容后内部服务容量已大于所需，TiDB Cloud 会保留现有配置，避免不必要的变更影响集群稳定性。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群的云存储数据导入体验。

    导入流程现已简化为 3 步向导，并配备智能预检查。新向导引导你完成连接设置、文件映射和存储桶扫描。通过扫描，TiDB Cloud 会在导入前准确展示将被导入的文件及其目标位置，大幅降低配置复杂度并防止导入失败。

    详情参见以下文档：

    - [将示例数据导入 TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md)
    - [从云存储导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从云存储导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 7 月 15 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/) 升级为 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/)。

    与 v8.1.2 相比，v8.5.2 包含 [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/)、[v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/)、[v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/)、[v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/)、[v8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/) 和 [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/) 的新特性、改进和修复。

- 支持审计 `BackupCompleted` 事件，增强备份活动的控制台审计日志。

    该增强可记录备份完成活动，满足安全与合规要求。

    详情参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

- 支持在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeed 中按列值过滤。

    你现在可以在 changefeed 中使用表达式过滤特定列值，从源头排除无关数据。该功能实现 DML 事件的细粒度过滤，有助于降低资源消耗并提升性能。

    详情参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。

## 2025 年 6 月 24 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 数据库审计日志（beta）现可按需申请。该功能可记录用户访问详情（如执行的 SQL 语句）历史。

    如需申请该功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，选择 **Request Support**，在 Description 字段填写 “Apply for TiDB Cloud Serverless database audit logging”，然后点击 **Submit**。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持用户自主管理日志脱敏。

    你现在可以为 TiDB Cloud Dedicated 集群启用或禁用日志脱敏，自主管理集群日志的脱敏状态。

    详情参见 [用户自主管理日志脱敏](/tidb-cloud/tidb-cloud-log-redaction.md)。

- AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已正式支持（GA）使用客户自管加密密钥（CMEK）进行静态加密。

    该功能允许你通过 Key Management Service（KMS）管理的对称加密密钥保护静态数据。

    详情参见 [在 AWS 上使用客户自管加密密钥进行静态加密](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)。

## 2025 年 6 月 17 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中，16 vCPU 和 32 vCPU 的 TiKV 节点最大存储容量由 **6144 GiB** 调整为 **4096 GiB**。

    详情参见 [TiKV 节点存储规格](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)。

**控制台变更**

- 重构左侧导航栏，提升整体导航体验。
  
    - 左上角新增 <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> 图标，可随时隐藏或显示左侧导航栏。
    - 左上角新增组合框，可快速在组织、项目和集群间切换，集中管理。
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - 左侧导航栏的入口会根据组合框当前选择动态调整，帮助你聚焦最相关功能。
    - **Support**、**Notification** 和账号入口现始终固定在左侧导航栏底部，便于快速访问。

## 2025 年 6 月 4 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现已在 Microsoft Azure 公测。
  
    随着本次发布，TiDB Cloud 现已支持三大主流公有云平台 —— AWS、Google Cloud 和 Azure，助你根据业务需求和云战略灵活部署 TiDB Cloud Dedicated 集群。
  
    - AWS 和 Google Cloud 上的所有核心功能在 Azure 上均已支持。
    - Azure 目前支持 East US 2、日本东部和东南亚 3 个区域，后续将支持更多区域。
    - Azure 上的 TiDB Cloud Dedicated 集群需 TiDB 版本 v7.5.3 或更高。
  
  快速入门文档：
  
    - [在 Azure 上创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)
    - [通过 Azure 私有端点连接 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 
    - [导入数据到 Azure 上的 TiDB Cloud Dedicated 集群](/tidb-cloud/import-csv-files.md)

- Prometheus 集成提供更多指标，增强 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的监控能力。
  
    你现在可以将 `tidbcloud_disk_read_latency`、`tidbcloud_kv_request_duration` 等更多指标集成到 Prometheus，追踪 TiDB Cloud Dedicated的更多性能维度。
  
    关于可用指标及启用方法，详见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

- TiKV [标准](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [性能](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储定价正式发布。

    优惠期自 **2025 年 6 月 5 日 00:00 UTC** 起结束，届时价格恢复为标准价。TiDB Cloud Dedicated价格详情参见 [TiDB Cloud Dedicated定价详情](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点规格配置交互体验。

    你现在可以在创建 TiDB Cloud Dedicated 集群时通过开关按钮控制 TiFlash 配置，使配置过程更直观流畅。

## 2025 年 5 月 27 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 changefeed 现已支持将数据流式同步到 [Apache Pulsar](https://pulsar.apache.org)。

    该功能使你可以将 TiDB Cloud Dedicated 集群与更多下游系统集成，满足更多数据集成需求。使用该功能需确保集群版本为 v7.5.1 或更高。

    详情参见 [下沉到 Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)。

## 2025 年 5 月 13 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 现已支持全文检索（beta），助力 AI 应用。

    TiDB Cloud Serverless 现已支持全文检索（beta），使 AI 和 RAG（检索增强生成）应用可通过精确关键词检索内容。该功能补充了向量检索（按语义相似度检索内容），两者结合可显著提升 RAG 工作流的检索准确性和答案质量。主要特性包括：

    - 直接文本检索：可直接查询字符串列，无需 embedding。
    - 多语言支持：自动检测并分析多语言文本，单表内多语言无需指定语言。
    - 相关性排序：结果采用业界标准 BM25 算法排序，确保最优相关性。
    - 原生 SQL 兼容：可与 SQL 过滤、分组、关联等功能无缝结合。

  快速入门请参见 [使用 SQL 进行全文检索](/tidb-cloud/vector-search-full-text-search-sql.md) 或 [使用 Python 进行全文检索](/tidb-cloud/vector-search-full-text-search-python.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 TiFlash 节点最大存储容量提升：

    - 8 vCPU TiFlash：由 2048 GiB 提升至 4096 GiB
    - 32 vCPU TiFlash：由 4096 GiB 提升至 8192 GiB

  此增强提升了 TiDB Cloud Dedicated 集群的分析型数据存储能力，提高了工作负载扩展效率，满足不断增长的数据需求。

    详情参见 [TiFlash 节点存储规格](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 优化维护窗口配置体验，提供更直观的选项以配置和重新安排维护任务。

    详情参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 延长 TiKV [标准](/tidb-cloud/size-your-cluster.md#standard-storage) 和 [性能](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) 存储类型的优惠期，现将于 2025 年 6 月 5 日结束。届时价格恢复为标准价。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 **Backup Setting** 页面布局，提升备份配置体验。

    详情参见 [备份与恢复 TiDB Cloud Dedicated数据](/tidb-cloud/backup-and-restore.md)。

## 2025 年 4 月 22 日

**通用变更**

- 现已支持导出数据到阿里云 OSS。

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群现支持使用 [AccessKey 对](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) 将数据导出到 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service)。

    详情参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群 TiDB 版本由 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3) 升级为 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2025 年 4 月 15 日

**通用变更**

- 支持从 [阿里云对象存储服务（OSS）](https://www.alibabacloud.com/en/product/object-storage-service) 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群。

    该功能简化了数据迁移到 TiDB Cloud Serverless 的流程。你可以使用 AccessKey 对进行认证。

    详情参见以下文档：

    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [从 Amazon S3、GCS、Azure Blob Storage 或阿里云 OSS 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## 2025 年 4 月 1 日

**通用变更**

- [TiDB 节点组](/tidb-cloud/tidb-node-group-overview.md) 功能现已在 AWS 和 Google Cloud 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群正式发布（GA）。

    该功能支持在单一集群内实现**细粒度计算资源隔离**，助你在多租户或多工作负载场景下优化性能和资源分配。

    **主要优势：**

    - **资源隔离**：

        - 将 TiDB 节点分组为逻辑隔离单元，确保一个组内的工作负载不会影响其他组。
        - 防止应用或业务单元间的资源争用。

    - **简化管理**：

        - 在单一集群内统一管理所有节点组，降低运维复杂度。
        - 可按需独立扩缩各节点组。

  详细优势参见 [技术博客](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)。快速入门请参见 [管理 TiDB 节点组](/tidb-cloud/tidb-node-group-management.md)。

- 在 AWS 上托管的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 [标准存储](/tidb-cloud/size-your-cluster.md#standard-storage) 类型的 TiKV 节点。

    标准存储类型适用于大多数工作负载，在性能与成本之间实现平衡。

    **主要优势：**

    - **性能提升**：为 Raft 日志预留充足磁盘资源，减少 Raft 与数据存储间的 I/O 争用，提升 TiKV 读写性能。
    - **稳定性增强**：将关键 Raft 操作与数据工作负载隔离，确保性能更可预测。
    - **成本效益**：与原存储类型相比，在更具竞争力的价格下提供更高性能。

    **可用性：**

    2025 年 4 月 1 日及以后在 AWS 上新建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（版本 >= 7.5.5、8.1.2 或 8.5.0）将自动采用标准存储类型。现有集群仍使用原 [基础存储](/tidb-cloud/size-your-cluster.md#basic-storage) 类型，无需迁移。

    标准存储与基础存储价格不同。详情参见 [定价](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 2025 年 3 月 25 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群现已支持为公网端点配置防火墙规则。

    你现在可以为 TiDB Cloud Serverless 集群配置防火墙规则，控制公网端点的访问。可在 [TiDB Cloud 控制台](https://tidbcloud.com/) 直接指定允许的 IP 地址或范围，提升安全性。

    详情参见 [为 TiDB Cloud Serverless 公网端点配置防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 2025 年 3 月 18 日

**通用变更**

- 支持为 Google Cloud 上部署的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    详情参见 [TiDB 节点组概览](/tidb-cloud/tidb-node-group-overview.md)。

- 支持将数据库审计日志文件存储在 TiDB Cloud，用于 AWS 上部署的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    你可以直接从 TiDB Cloud 下载这些审计日志文件。该功能仅支持按需申请。

    详情参见 [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

- 通过优化多因素认证（MFA）管理，提升 TiDB Cloud 账号安全性。该功能适用于 TiDB Cloud 的密码登录。

    详情参见 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2025 年 2 月 18 日

**控制台变更**

- 推出 Connected Care，TiDB Cloud 的全新支持服务。

    Connected Care 服务通过现代通信工具、主动支持和先进 AI 能力，增强你与 TiDB Cloud 的连接，带来无缝、以客户为中心的体验。

    Connected Care 服务包含以下功能：

    - **Clinic 服务**：高级监控与诊断，优化性能。
    - **IM 中的 AI 聊天**：通过即时通讯工具获得 AI 实时协助。
    - **IM 订阅告警与工单进展**：通过 IM 实时获知告警和工单进度。
    - **IM 工单交互**：可通过 IM 工具创建和跟进支持工单。

  详情参见 [Connected Care 概览](/tidb-cloud/connected-care-overview.md)。

- 支持从 GCS 和 Azure Blob Storage 导入数据到 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群。

    TiDB Cloud Serverless 现已支持从 Google Cloud Storage（GCS）和 Azure Blob Storage 导入数据。你可以使用 Google Cloud 服务账号密钥或 Azure 共享访问签名（SAS）令牌进行认证。该功能简化了数据迁移到 TiDB Cloud Serverless 的流程。

    详情参见 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [从 Amazon S3、GCS 或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)。

## 2025 年 1 月 21 日

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群现已支持每次任务导入单个本地 CSV 文件，文件大小上限由 50 MiB 提升至 250 MiB。

    详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2025 年 1 月 14 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增支持 AWS 区域：`Jakarta (ap-southeast-3)`。

- 推出 Notification 功能，使你可通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 实时获知 TiDB Cloud 更新和告警。

    详情参见 [通知](/tidb-cloud/notifications.md)。

## 2025 年 1 月 2 日

**通用变更**

- 支持为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建 TiDB 节点组，提升资源管理灵活性。

    详情参见 [TiDB 节点组概览](/tidb-cloud/tidb-node-group-overview.md)。

- 支持通过 Private Connect（beta）将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群连接到 AWS 和 Google Cloud 上的通用 Kafka。

    Private Connect 利用云服务商的 Private Link 或 Private Service Connect 技术，使 TiDB Cloud VPC 内的 changefeed 可通过私有 IP 连接到客户 VPC 内的 Kafka，就像这些 Kafka 直接托管在 TiDB Cloud VPC 内一样。该功能有助于避免 VPC CIDR 冲突，满足安全合规要求。

    - AWS 上的 Apache Kafka，请参见 [在 AWS 上设置自建 Kafka Private Link 服务](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 配置网络连接。

    - Google Cloud 上的 Apache Kafka，请参见 [在 Google Cloud 上设置自建 Kafka Private Service Connect](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 配置网络连接。
  
  注意，使用该功能会产生额外的 [Private Data Link 费用](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。

    详情参见 [Changefeed 下沉到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)。

- Kafka changefeed 新增可配置选项：

    - 支持使用 Debezium 协议。Debezium 是一种数据库变更捕获工具，将每个捕获的数据库变更转换为事件消息并发送到 Kafka。详情参见 [TiCDC Debezium 协议](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)。

    - 支持为所有表统一定义单一分区分发器，或为不同表定义不同分区分发器。

    - 新增两种分发器类型：按时间戳和按列值分区分发 Kafka 消息。

  详情参见 [下沉到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

- TiDB Cloud 角色增强：

    - 新增 `Project Viewer` 和 `Organization Billing Viewer` 角色，实现更细粒度的访问控制。

    - 重命名以下角色：

        - `Organization Member` 改为 `Organization Viewer`
        - `Organization Billing Admin` 改为 `Organization Billing Manager`
        - `Organization Console Audit Admin` 改为 `Organization Console Audit Manager`

  详情参见 [身份访问管理](/tidb-cloud/manage-user-access.md#organization-roles)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群区域级高可用性（beta）。

    该功能适用于对基础设施冗余和业务连续性要求极高的工作负载。主要功能包括：

    - 节点分布于多个可用区，确保主可用区故障时的高可用性。
    - 关键 OLTP 组件（如 PD 和 TiKV）跨可用区冗余部署。
    - 主可用区故障时自动故障转移，最小化服务中断。
  
  目前仅在 AWS 东京（ap-northeast-1）区域支持，且仅可在集群创建时启用。
  
    详情参见 [TiDB Cloud Serverless 的高可用性](/tidb-cloud/serverless-high-availability.md)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) 升级为 [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)。

**控制台变更**

- 数据导出服务增强：

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 将 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 数据导出到 Google Cloud Storage 和 Azure Blob Storage。

    - 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 导出 Parquet 文件格式数据。

  详情参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md) 和 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/configure-external-storage-access.md)。
