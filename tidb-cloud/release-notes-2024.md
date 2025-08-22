---
title: 2024 年 TiDB Cloud 发布说明
summary: 了解 2024 年 TiDB Cloud 的发布说明。
---

# 2024 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2024 年的发布说明。

## 2024 年 12 月 17 日

**通用变更**

- TiDB Cloud Serverless 备份与恢复变更

    - 支持将数据恢复到新集群，提供更大的灵活性，并确保你当前集群的操作不受影响。

    - 优化备份与恢复策略，使其与集群计划相匹配。更多信息，参见 [备份与恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#learn-about-the-backup-setting)。

    - 应用以下兼容性策略，帮助你平滑过渡：

        - 2024-12-17T10:00:00Z 之前创建的备份将在所有集群中遵循之前的保留时长。
        - 可扩展集群的备份时间将保留当前配置，而免费集群的备份时间将重置为默认设置。

## 2024 年 12 月 3 日

**通用变更**

- 为部署在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入灾备恢复组（beta）功能。

    该功能允许你在 TiDB Cloud Dedicated 集群之间复制数据库，确保在区域性灾难发生时能够快速恢复。如果你拥有 Project Owner 角色，可以通过创建新的恢复组并将数据库分配到该组来启用此功能。通过使用恢复组复制数据库，你可以提升灾备能力，满足更严格的可用性 SLA，并实现更激进的恢复点目标（RPO）和恢复时间目标（RTO）。
  
    更多信息，参见 [快速开始使用恢复组](/tidb-cloud/recovery-group-get-started.md)。

## 2024 年 11 月 26 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4) 升级到 [v8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 针对以下场景的大数据写入成本最多降低 80%：

    - 在 [autocommit 模式](/transaction-overview.md#autocommit)下执行大于 16 MiB 的写入操作时。
    - 在 [乐观事务模型](/optimistic-transaction.md)下执行大于 16 MiB 的写入操作时。
    - [导入数据到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) 时。

  该优化提升了数据操作的效率和性价比，随着工作负载的增长可带来更大节省。

## 2024 年 11 月 19 日

**通用变更**

- [TiDB Cloud Serverless 分支（beta）](/tidb-cloud/branch-overview.md)为分支管理引入以下改进：

    - **灵活的分支创建**：创建分支时，你可以选择特定集群或分支作为父级，并指定父级的精确时间点，从而精确控制分支中的数据。

    - **分支重置**：你可以将分支重置为与其父级的最新状态同步。

    - **改进的 GitHub 集成**： [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub 应用引入了 [`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode) 参数，用于控制拉取请求同步时的行为。在默认的 `reset` 模式下，应用会将分支重置为与拉取请求中的最新更改保持一致。

  更多信息，参见 [管理 TiDB Cloud Serverless 分支](/tidb-cloud/branch-manage.md) 和 [将 TiDB Cloud Serverless 分支（Beta）集成到 GitHub](/tidb-cloud/branch-github-integration.md)。

## 2024 年 11 月 12 日

**通用变更**

- 为 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群增加暂停时长限制。

    TiDB Cloud Dedicated 现在将最大暂停时长限制为 7 天。如果你未在 7 天内手动恢复集群，TiDB Cloud 将自动恢复该集群。

    此变更仅适用于 **2024 年 11 月 12 日后创建的组织**。2024 年 11 月 12 日及之前创建的组织将在提前通知后逐步过渡到新的暂停行为。

    更多信息，参见 [暂停或恢复 TiDB Cloud Dedicated 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

- [Datadog 集成（beta）](/tidb-cloud/monitor-datadog-integration.md) 新增对 `AP1`（日本）区域的支持。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增支持 AWS 区域：`Mumbai (ap-south-1)`。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群移除对 AWS `São Paulo (sa-east-1)` 区域的支持。

## 2024 年 10 月 29 日

**通用变更**

- 新增指标：为 Prometheus 集成添加 `tidbcloud_changefeed_checkpoint_ts`。

    该指标用于跟踪 changefeed 的检查点时间戳，表示已成功写入下游的最大 TSO（时间戳 Oracle）。更多可用指标信息，参见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana（Beta）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)。

## 2024 年 10 月 22 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3) 升级到 [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)。

## 2024 年 10 月 15 日

**API 变更**

* [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp) 自 2024 年 10 月 15 日起弃用，未来将被移除。如果你当前在使用 MSP API，请迁移到 [TiDB Cloud Partner](https://partner-console.tidbcloud.com/signin) 中的 Partner Management API。

## 2024 年 9 月 24 日

**通用变更**

- 为托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiFlash vCPU 和内存规格](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram)：`32 vCPU, 128 GiB`

**CLI 变更**

- 发布 [TiDB Cloud CLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2)。

    TiDB Cloud CLI 提供以下新特性：

    - 支持通过 [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md) 管理 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 SQL 用户。
    - 允许在 [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md) 和 [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) 中禁用 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的公网访问端点。
    - 新增 [`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md) 命令，在使用 OAuth 认证时获取当前用户信息。
    - 在 [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中支持 `--sql`、`--where` 和 `--filter` 参数，灵活选择源表。
    - 支持将数据导出为 CSV 和 Parquet 文件。
    - 支持使用角色 ARN 作为凭证将数据导出到 Amazon S3，同时支持导出到 Google Cloud Storage 和 Azure Blob Storage。
    - 支持从 Amazon S3、Google Cloud Storage 和 Azure Blob Storage 导入数据。
    - 支持从分支和指定时间戳创建分支。

  TiDB Cloud CLI 优化了以下功能：

    - 改进调试日志记录。现在可以记录凭证和 user-agent。
    - 本地导出文件下载速度从每秒几十 KiB 提升到每秒几十 MiB。

  TiDB Cloud CLI 替换或移除了以下功能：

    - [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中的 `--s3.bucket-uri` 参数被 `--s3.uri` 替代。
    - [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) 中移除了 `--database` 和 `--table` 参数。你可以使用 `--sql`、`--where` 和 `--filter` 参数替代。
    - [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) 不再支持更新 annotations 字段。

## 2024 年 9 月 10 日

**通用变更**

- 启动 TiDB Cloud Partner Web 控制台和 Open API，提升 TiDB Cloud 合作伙伴的资源与账单管理能力。

    通过 AWS Marketplace Channel Partner Private Offer（CPPO）的托管服务提供商（MSP）和经销商现在可以利用 [TiDB Cloud Partner Web 控制台](https://partner-console.tidbcloud.com/) 和 Open API 简化日常运营。

    更多信息，参见 [TiDB Cloud Partner Web 控制台](/tidb-cloud/tidb-cloud-partners.md)。

## 2024 年 9 月 3 日

**控制台变更**

- 支持通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 从 TiDB Cloud Serverless 集群导出数据。 
  
    之前，TiDB Cloud 仅支持通过 [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 导出数据。现在，你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中轻松将 TiDB Cloud Serverless 集群的数据导出到本地文件和 Amazon S3。 
  
    更多信息，参见 [从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md) 和 [为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的连接体验。

    - 优化 **Connect** 对话框界面，为 TiDB Cloud Dedicated 用户提供更简洁高效的连接体验。
    - 新增集群级 **Networking** 页面，简化集群的网络配置。
    - 用新的 **Password Settings** 页面替换 **Security Settings** 页面，并将 IP 访问列表设置迁移到新的 **Networking** 页面。
  
  更多信息，参见 [连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-to-tidb-cluster.md)。

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据导入体验：

    - 优化 **Import** 页面的布局，使其更清晰。
    - 统一 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群的导入步骤。
    - 简化 AWS Role ARN 创建流程，便于连接设置。

  更多信息，参见 [从文件导入数据到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)。

## 2024 年 8 月 20 日

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中新建私有端点连接页面的布局，提升创建新私有端点连接的用户体验。

    更多信息，参见 [通过 AWS 私有端点连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections.md) 和 [通过 Google Cloud Private Service Connect 连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

## 2024 年 8 月 6 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 在 AWS 上的负载均衡计费变更。

    自 2024 年 8 月 1 日起，TiDB Cloud Dedicated 账单将包含 AWS 公网 IPv4 地址的新费用，与 [AWS 自 2024 年 2 月 1 日起生效的定价变更](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/) 保持一致。每个公网 IPv4 地址的费用为 $0.005/小时，每个托管在 AWS 上的 TiDB Cloud Dedicated 集群每月约 $10。

    该费用将显示在 [账单明细](/tidb-cloud/tidb-cloud-billing.md#billing-details) 的 **TiDB Cloud Dedicated - Data Transfer - Load Balancing** 服务下。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2) 升级到 [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的集群规格配置体验。

    优化 [**创建集群**](/tidb-cloud/create-tidb-cluster.md) 和 [**修改集群**](/tidb-cloud/scale-tidb-cluster.md) 页面中的 **Cluster Size** 部分布局。此外，**Cluster Size** 部分现在包含节点规格推荐文档的链接，帮助你选择合适的集群规格。

## 2024 年 7 月 23 日

**通用变更**

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持自动生成向量检索端点。

    如果你的表包含 [向量数据类型](/vector-search/vector-search-data-types.md)，你可以自动生成一个向量检索端点，并根据所选距离函数计算向量距离。

    该功能可无缝集成到 [Dify](https://docs.dify.ai/guides/tools) 和 [GPTs](https://openai.com/blog/introducing-gpts) 等 AI 平台，为你的应用带来先进的自然语言处理和 AI 能力，助力更复杂的任务和智能解决方案。

    更多信息，参见 [自动生成端点](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically) 和 [将数据应用集成到第三方工具](/tidb-cloud/data-service-integrations.md)。

- 引入预算功能，帮助你跟踪实际 TiDB Cloud 成本与计划支出，防止意外费用。

    你需要拥有组织的 `Organization Owner` 或 `Organization Billing Admin` 角色才能访问该功能。

    更多信息，参见 [管理 TiDB Cloud 预算](/tidb-cloud/tidb-cloud-budget.md)。

## 2024 年 7 月 9 日

**通用变更**

- 优化 [系统状态](https://status.tidbcloud.com/) 页面，提供更全面的 TiDB Cloud 系统健康和性能洞察。

    你可以直接访问 <https://status.tidbcloud.com/>，或在 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角点击 **?** 并选择 **System Status** 进入。

**控制台变更**

- 优化 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群 [创建 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md) 的 **VPC Peering** 页面布局，提升用户体验。

## 2024 年 7 月 2 日

**通用变更**

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 提供端点库，内置预定义系统端点，可直接添加到你的数据应用中，减少端点开发工作量。

    当前库中仅包含 `/system/query` 端点，你只需在预定义的 `sql` 参数中传入 SQL 语句，即可执行任意 SQL 查询。该端点便于即时执行 SQL 查询，提升灵活性和效率。

    更多信息，参见 [添加预定义系统端点](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint)。

- 优化慢查询数据存储。

    [TiDB Cloud 控制台](https://tidbcloud.com) 的慢查询访问现在更加稳定，不会影响数据库性能。

## 2024 年 6 月 25 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持向量检索（beta）。

    向量检索（beta）功能为多种数据类型（如文档、图片、音频和视频）提供语义相似性检索的高级解决方案。该功能让开发者可用熟悉的 MySQL 技能轻松构建具备生成式人工智能（AI）能力的可扩展应用。主要特性包括：

    - [向量数据类型](/vector-search/vector-search-data-types.md)、[向量索引](/vector-search/vector-search-index.md) 及 [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)。
    - 与 [LangChain](/vector-search/vector-search-integrate-with-langchain.md)、[LlamaIndex](/vector-search/vector-search-integrate-with-llamaindex.md) 和 [JinaAI](/vector-search/vector-search-integrate-with-jinaai-embedding.md) 的生态集成。
    - Python 语言支持：[SQLAlchemy](/vector-search/vector-search-integrate-with-sqlalchemy.md)、[Peewee](/vector-search/vector-search-integrate-with-peewee.md) 和 [Django ORM](/vector-search/vector-search-integrate-with-django-orm.md)。
    - 示例应用与教程：使用 [Python](/vector-search/vector-search-get-started-using-python.md) 或 [SQL](/vector-search/vector-search-get-started-using-sql.md) 进行文档语义检索。

  更多信息，参见 [向量检索（beta）概览](/vector-search/vector-search-overview.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现为组织所有者提供每周邮件报告。

    这些报告可洞察集群的性能和活动。通过自动每周更新，你可以及时了解集群状况，并据此做出数据驱动的优化决策。

- 发布 Chat2Query API v3 端点，并弃用 Chat2Query API v1 端点 `/v1/chat2data`。

    通过 Chat2Query API v3 端点，你可以基于会话开启多轮 Chat2Query。

    更多信息，参见 [快速开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

**控制台变更**

- 将 Chat2Query（beta）重命名为 SQL Editor（beta）。

    原 Chat2Query 界面现更名为 SQL Editor。此更名明确区分了手动 SQL 编辑与 AI 辅助查询生成，提升了可用性和整体体验。

    - **SQL Editor**：TiDB Cloud 控制台中用于手动编写和执行 SQL 查询的默认界面。
    - **Chat2Query**：AI 辅助的文本转查询功能，允许你用自然语言与数据库交互，生成、重写和优化 SQL 查询。

  更多信息，参见 [使用 AI 辅助 SQL Editor 探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

## 2024 年 6 月 18 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 16 vCPU TiFlash 和 32 vCPU TiFlash 节点最大存储从 2048 GiB 提升至 4096 GiB。

    此增强提升了 TiDB Cloud Dedicated 集群的分析型数据存储能力，提高了工作负载扩展效率，并满足不断增长的数据需求。

    更多信息，参见 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1) 升级到 [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)。

## 2024 年 6 月 4 日

**通用变更**

- 为部署在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入灾备恢复组（beta）功能。

    该功能允许你在 TiDB Cloud Dedicated 集群之间复制数据库，确保在区域性灾难发生时能够快速恢复。如果你拥有 `Project Owner` 角色，可以通过创建新的恢复组并将数据库分配到该组来启用此功能。通过使用恢复组复制数据库，你可以提升灾备能力，满足更严格的可用性 SLA，并实现更激进的恢复点目标（RPO）和恢复时间目标（RTO）。

    更多信息，参见 [快速开始使用恢复组](/tidb-cloud/recovery-group-get-started.md)。

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 列式存储 [TiFlash](/tiflash/tiflash-overview.md) 引入计费与计量（beta）。

    截至 2024 年 6 月 30 日，TiDB Cloud Serverless 集群的列式存储仍享受 100% 折扣免费。此日期后，每个 TiDB Cloud Serverless 集群将包含 5 GiB 列式存储免费额度，超出部分将按量计费。

    更多信息，参见 [TiDB Cloud Serverless 价格详情](https://www.pingcap.com/tidb-serverless-pricing-details/#storage)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持 [生存时间（TTL）](/time-to-live.md)。

## 2024 年 5 月 28 日

**通用变更**

- Google Cloud `Taiwan (asia-east1)` 区域支持 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能。

    托管在 Google Cloud `Taiwan (asia-east1)` 区域的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群现已支持数据迁移（DM）功能。如果你的上游数据存储在该区域或附近，现在可以更快、更可靠地将数据从 Google Cloud 迁移到 TiDB Cloud。

- 为托管在 AWS 和 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiDB 节点规格](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)：`16 vCPU, 64 GiB`

**API 变更**

- 引入 TiDB Cloud Data Service API，实现以下资源的自动高效管理：

    * **Data App**：一组端点的集合，可用于访问特定应用的数据。
    * **Data Source**：与 Data App 关联的集群，用于数据操作与检索。
    * **Endpoint**：可自定义执行 SQL 语句的 Web API。
    * **Data API Key**：用于安全访问端点。
    * **OpenAPI 规范**：Data Service 支持为每个 Data App 生成 OpenAPI Specification 3.0，便于你以标准格式与端点交互。

  这些 TiDB Cloud Data Service API 端点已在 TiDB Cloud API v1beta1 中发布，该版本为 TiDB Cloud 的最新 API 版本。

    更多信息，参见 [API 文档（v1beta1）](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)。

## 2024 年 5 月 21 日

**通用变更**

- 为托管在 Google Cloud 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiDB 节点规格](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)：`8 vCPU, 16 GiB`

## 2024 年 5 月 14 日

**通用变更**

- 扩展 [**Time Zone**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization) 区域的时区选择，更好地满足来自不同地区客户的需求。

- 支持在你的 VPC 与 TiDB Cloud 的 VPC 不同区域时 [创建 VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)。

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持路径参数与查询参数。

    该功能通过结构化 URL 增强资源标识，提升用户体验、搜索引擎优化（SEO）和客户端集成，为开发者提供更大灵活性，更好地契合行业标准。

    更多信息，参见 [基本属性](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)。

## 2024 年 4 月 16 日

**CLI 变更**

- 发布基于新 [TiDB Cloud API](/tidb-cloud/api-overview.md) 的 [TiDB Cloud CLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)。新 CLI 带来以下新特性：

    - [从 TiDB Cloud Serverless 集群导出数据](/tidb-cloud/serverless-export.md)
    - [从本地存储导入数据到 TiDB Cloud Serverless 集群](/tidb-cloud/ticloud-import-start.md)
    - [通过 OAuth 认证](/tidb-cloud/ticloud-auth-login.md)
    - [通过 TiDB Bot 提问](/tidb-cloud/ticloud-ai.md)

  升级 TiDB Cloud CLI 前，请注意新 CLI 与旧版本不兼容。例如，CLI 命令中的 `ticloud cluster` 现已更新为 `ticloud serverless`。更多信息，参见 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2024 年 4 月 9 日

**通用变更**

- 为托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供新的 [TiDB 节点规格](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)：`8 vCPU, 32 GiB`。

## 2024 年 4 月 2 日

**通用变更**

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入两种服务计划：**Free** 和 **Scalable**。

    为满足不同用户需求，TiDB Cloud Serverless 提供免费和可扩展服务计划。无论你是刚刚起步还是需要应对不断增长的应用需求，这些计划都能为你提供所需的灵活性和能力。

    更多信息，参见 [集群计划](/tidb-cloud/select-cluster-tier.md#cluster-plans)。

- 修改 TiDB Cloud Serverless 集群达到使用配额后的限流行为。现在，一旦集群达到使用配额，将立即拒绝所有新连接请求，从而确保现有操作的服务不中断。

    更多信息，参见 [使用配额](/tidb-cloud/serverless-limitations.md#usage-quota)。

## 2024 年 3 月 5 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0) 升级到 [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)。

**控制台变更**

- 在 [**Billing**](https://tidbcloud.com/org-settings/billing/payments) 页面新增 **Cost Explorer** 标签页，为你的组织提供直观的成本分析和自定义报表界面。

    你可以在组织的 **Billing** 页面点击 **Cost Explorer** 标签页使用该功能。

    更多信息，参见 [Cost Explorer](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 为 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server) 显示 **limit** 标签。

    **limit** 标签展示了集群中各组件的 CPU、内存和存储等资源最大使用量。该优化简化了集群资源使用率的监控流程。

    你可以在集群的 **Monitoring** 页面，**Metrics** 标签下的 **Server** 分类中查看这些指标限制。

    更多信息，参见 [TiDB Cloud Dedicated 集群指标](/tidb-cloud/built-in-monitoring.md#server)。

## 2024 年 2 月 21 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 TiDB 版本从 [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0) 升级到 [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)。

## 2024 年 2 月 20 日

**通用变更**

- 支持在 Google Cloud 上创建更多 TiDB Cloud 节点。

    - 通过为 Google Cloud [配置区域 CIDR 大小](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)为 `/19`，你现在可以在项目的任意区域内创建最多 124 个 TiDB Cloud 节点。
    - 如果你希望在项目的任意区域内创建超过 124 个节点，可联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 协助自定义 IP 范围大小（/16 到 /18）。

## 2024 年 1 月 23 日

**通用变更**

- 为 TiDB、TiKV 和 TiFlash 增加 32 vCPU 作为节点规格选项。

    每个 `32 vCPU, 128 GiB` TiKV 节点的存储范围为 200 GiB 到 6144 GiB。

    推荐在以下场景中使用此类节点：

    - 高负载生产环境
    - 极高性能需求

## 2024 年 1 月 16 日

**通用变更**

- 优化项目的 CIDR 配置。

    - 你可以为每个项目直接设置区域级 CIDR。
    - 你可以从更广泛的 CIDR 值范围中选择 CIDR 配置。

    注意：之前的项目全局级 CIDR 设置已废弃，但所有处于激活状态的区域级 CIDR 不受影响。现有集群的网络不会受到影响。

    更多信息，参见 [为区域设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

- TiDB Cloud Serverless 用户现在可以为集群禁用公网访问端点。

    更多信息，参见 [禁用公网访问端点](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)。

- [数据服务（beta）](https://tidbcloud.com/project/data-service) 支持为 Data App 配置自定义域名访问端点。

    默认情况下，TiDB Cloud Data Service 提供 `<region>.data.tidbcloud.com` 域名访问每个 Data App 的端点。为提升个性化和灵活性，你现在可以为 Data App 配置自定义域名，替代默认域名。该功能支持为数据库服务使用品牌化 URL，并提升安全性。

    更多信息，参见 [数据服务中的自定义域名](/tidb-cloud/data-service-custom-domain.md)。

## 2024 年 1 月 3 日

**通用变更**

- 支持 [组织 SSO](https://tidbcloud.com/org-settings/authentication)，简化企业认证流程。

    通过该功能，你可以使用 [安全断言标记语言（SAML）](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) 或 [OpenID Connect（OIDC）](https://openid.net/developers/how-connect-works/) 无缝集成 TiDB Cloud 与任意身份提供商（IdP）。

    更多信息，参见 [组织 SSO 认证](/tidb-cloud/tidb-cloud-org-sso-authentication.md)。

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1) 升级到 [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的双区域备份功能现已正式发布（GA）。

    通过该功能，你可以在 AWS 或 Google Cloud 的不同地理区域间复制备份。该功能为数据保护和灾备能力提供了额外保障。

    更多信息，参见 [双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。