---
title: TiDB Cloud Release Notes in 2022
summary: 了解 2022 年 TiDB Cloud 的发布说明。
---

# 2022 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2022 年的发布说明。

## 2022 年 12 月 28 日

**通用变更**

- 目前，在将所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0) 升级到 [v6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0) 后，在某些情况下冷启动变慢。因此我们将所有 Serverless Tier 集群的默认 TiDB 版本从 v6.4.0 回滚到 v6.3.0，随后会尽快修复该问题，并在之后再次升级。

## 2022 年 12 月 27 日

**通用变更**

- 将所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0) 升级到 [v6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0)。

- 专属集群（Dedicated Tier）现已正式支持时间点恢复（PITR）。

    PITR 支持将任意时间点的数据恢复到新集群。要使用 PITR 功能，请确保你的 TiDB 集群版本至少为 v6.4.0，且 TiKV 节点规格至少为 8 vCPU 和 16 GiB。

    你可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 的 **Backup Settings** 中启用或禁用 PITR 功能。

    详细信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

- 支持管理多个 changefeed 并编辑已有的 changefeed。

    - 你现在可以根据需要创建多个 changefeed 来管理不同的数据同步任务。目前每个集群最多可有 10 个 changefeed。详情参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。
    - 你可以在 changefeed 处于暂停状态时编辑其配置。更多信息参见 [编辑 changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

- 支持将 Amazon Aurora MySQL、Amazon RDS MySQL 或自建 MySQL 兼容数据库的数据直接在线迁移到 TiDB Cloud。该功能现已正式发布。

    - 在以下 6 个区域提供服务：
        - AWS Oregon (us-west-2)
        - AWS N. Virginia (us-east-1)
        - AWS Mumbai (ap-south-1)
        - AWS Singapore (ap-southeast-1)
        - AWS Tokyo (ap-northeast-1)
        - AWS Frankfurt (eu-central-1)
    - 支持多种规格。你可以根据所需性能选择合适的规格，以获得最佳的数据迁移体验。

  有关如何迁移数据到 TiDB Cloud，请参见 [用户文档](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。计费详情参见 [数据迁移计费](/tidb-cloud/tidb-cloud-billing-dm.md)。

- 支持将本地 CSV 文件导入到 TiDB Cloud。

    只需几步点击即可完成任务配置，随后你的本地 CSV 数据即可快速导入到 TiDB 集群。使用该方式时，无需提供云存储桶路径和 Role ARN，整个导入过程快捷流畅。

    详细信息参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2022 年 12 月 20 日

**通用变更**

- 在 [Datadog](/tidb-cloud/monitor-datadog-integration.md) Dashboard 中新增 `project name` 标签作为筛选项，以便提供项目信息。

    你可以通过 `project name` 筛选器快速找到目标集群。

## 2022 年 12 月 13 日

**通用变更**

- 为 Serverless Tier 引入 TiDB Cloud SQL Editor（Beta）。

    这是一个基于 Web 的 SQL 编辑器，允许你直接编辑并运行针对 Serverless Tier 数据库的 SQL 查询。你可以在 Serverless Tier 集群的左侧导航栏中轻松找到它。

    对于 Serverless Tier，Web SQL Shell 已被 SQL Editor 替代。

- 支持使用 [Changefeeds](/tidb-cloud/changefeed-overview.md) 为 Dedicated Tier 实现数据流式传输。

    - 支持 [将数据变更日志流式同步到 MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)。

      当你从 MySQL/Aurora 迁移数据到 TiDB 时，通常需要使用 MySQL 作为备用数据库以防止意外的数据迁移问题。在这种情况下，你可以使用 MySQL sink 将数据从 TiDB 流式同步到 MySQL。

    - 支持 [将数据变更日志流式同步到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)（Beta）。

      将 TiDB 数据流式同步到消息队列是数据集成场景中的常见需求。你可以使用 Kafka sink 实现与其他数据处理系统（如 Snowflake）的集成，或支持业务消费。

    更多信息参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。

- 组织所有者可以在 **Organization Settings** 中编辑组织名称。

**控制台变更**

- 优化 [TiDB Cloud 控制台](https://tidbcloud.com) 的导航布局，为用户带来全新的导航体验。

    新布局包括以下变化：

    - 引入左侧导航栏，最大化屏幕使用效率。
    - 采用更扁平的导航层级。

- 改进 [**Connect**](/tidb-cloud/connect-to-tidb-cluster-serverless.md) 体验，提升 Serverless Tier 用户的连接便捷性。

    现在开发者只需几步点击即可连接到 SQL 编辑器或自己喜欢的工具，无需切换上下文。

## 2022 年 12 月 6 日

**通用变更**

- 将新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2) 升级到 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)。

## 2022 年 11 月 29 日

**通用变更**

- 优化来自 AWS Marketplace 和 Google Cloud Marketplace 的用户体验。

    无论你是 TiDB Cloud 新用户还是已有账号，现在都可以关联 AWS 或 GCP 计费账号，更便捷地完成 AWS 或 GCP Marketplace 订阅。

    关联方法参见 [云服务商 Marketplace 计费](/tidb-cloud/tidb-cloud-billing.md#billing-from-cloud-provider-marketplace)。

## 2022 年 11 月 22 日

**通用变更**

* 支持将 Amazon Aurora MySQL、Amazon RDS MySQL 或自建 MySQL 兼容数据库的数据直接在线迁移到 TiDB Cloud（Beta）。

    之前，你需要暂停业务并离线导入数据，或使用第三方工具迁移数据到 TiDB Cloud，过程较为复杂。现在，通过 **Data Migration** 功能，你只需在 TiDB Cloud 控制台操作，即可安全地将数据以最小停机时间迁移到 TiDB Cloud。

    此外，Data Migration 提供全量和增量数据迁移能力，可将源端的现有数据和持续变更同步到 TiDB Cloud。

    目前，Data Migration 功能仍处于 **Beta** 阶段，仅支持 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，且仅在 AWS Oregon (us-west-2) 和 AWS Singapore (ap-southeast-1) 区域开放。每个组织可免费创建一个迁移任务。如需为组织创建多个迁移任务，请 [提交工单](/tidb-cloud/tidb-cloud-support.md)。

    详细信息参见 [使用 Data Migration 迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

## 2022 年 11 月 15 日

**通用变更**

* 支持 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的时间点恢复（PITR）（Beta）。

    PITR 支持将任意时间点的数据恢复到新集群。你可以用它来：

    * 降低灾备场景下的 RPO。
    * 通过恢复到错误事件前的时间点，解决数据写入错误。
    * 审计业务的历史数据。

  要使用 PITR 功能，请确保 TiDB 集群版本至少为 v6.3.0，且 TiKV 节点规格至少为 8 vCPU 和 16 GiB。

  默认情况下，备份数据存储在集群创建所在的同一区域。在日本，对于启用 PITR 的 GCP 托管 TiDB 集群，你可以选择将备份数据存储在一个或两个区域（东京和/或大阪）。从备用区域恢复数据可提升数据安全性，并容忍区域故障。

  详细信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

  该功能仍处于 Beta 阶段，仅支持申请开通：

    * 点击 TiDB Cloud 控制台右下角的 **Help**。
    * 在弹窗中，**Description** 字段填写 "Apply for PITR"，然后点击 **Send**。

* 数据库审计日志功能现已正式发布（GA）。

    你可以使用数据库审计日志记录用户访问详情（如执行的 SQL 语句）历史，并定期分析数据库审计日志，有助于保障数据库安全。

    详细信息参见 [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。

## 2022 年 11 月 8 日

**通用变更**

* 优化用户反馈渠道。

    现在你可以在 TiDB Cloud 控制台的 **Support** > **Give Feedback** 中申请演示或额度。如果你想进一步了解 TiDB Cloud，这将非常有帮助。

    我们收到你的请求后会尽快与你联系并提供帮助。

## 2022 年 10 月 28 日

**通用变更**

* Developer Tier 升级为 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter)。Serverless Tier 是 TiDB 的全托管、自动弹性部署方案，现已开放 Beta 并可免费使用。

    * Serverless Tier 集群依然具备与 Dedicated Tier 集群相同的 HTAP 能力。
    * Serverless Tier 提供更快的集群创建速度和瞬时冷启动时间。与 Developer Tier 相比，创建时间从分钟级缩短到秒级。
    * 你无需关心部署拓扑，Serverless Tier 会根据你的请求自动调整。
    * Serverless Tier [强制要求集群使用 TLS 连接以保障安全](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    * 现有 Developer Tier 集群将在未来几个月内自动迁移到 Serverless Tier。你的集群使用不会受到影响，且在 Beta 期间使用 Serverless Tier 集群不会产生费用。

  立即开始体验 [快速上手](/tidb-cloud/tidb-cloud-quickstart.md)。

## 2022 年 10 月 25 日

**通用变更**

- 支持动态修改并持久化部分 TiDB 系统变量（Beta）。

    你可以使用标准 SQL 语句为支持的系统变量设置新值。

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    例如：

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    如果变量在 `GLOBAL` 级别设置，则会应用到整个集群并持久化（即使重启或重载服务器后依然生效）。`SESSION` 级别的变量不持久化，仅在当前会话内生效。

    **该功能仍处于 Beta 阶段**，目前仅支持有限数量的变量。不建议修改其他 [系统变量](/system-variables.md)，以避免不可预期的副作用。基于 TiDB v6.1，支持的变量如下：

    - [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    - [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    - [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    - [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    - [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    - [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    - [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    - [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    - [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

- 将新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1) 升级到 [v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)。

## 2022 年 10 月 19 日

**集成变更**

* 在 [Vercel Integration Marketplace](https://vercel.com/integrations#databases) 发布 [TiDB Cloud Vercel Integration](https://vercel.com/integrations/tidb-cloud)。

    [Vercel](https://vercel.com) 是面向前端开发者的平台，提供创新所需的速度与可靠性。通过 TiDB Cloud Vercel Integration，你可以轻松将 Vercel 项目连接到 TiDB Cloud 集群。详情参见文档 [将 TiDB Cloud 集成到 Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。

* 在 [Vercel 模板列表](https://vercel.com/templates) 发布 [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter)。

    你可以使用该模板作为起点，体验 Vercel 与 TiDB Cloud。在使用模板前，你需要先 [导入数据到 TiDB Cloud 集群](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data)。

## 2022 年 10 月 18 日

**通用变更**

* 对于 Dedicated Tier 集群，TiKV 或 TiFlash 节点的最小存储规格从 500 GiB 降低到 200 GiB。对于小数据量场景的用户，这将更具性价比。

    详情参见 [TiKV 节点存储](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size) 和 [TiFlash 节点存储](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)。

* 引入在线合同，支持自定义 TiDB Cloud 订阅并满足合规需求。

    在 TiDB Cloud 控制台的 **Billing** 页面新增 [**Contract** 标签](/tidb-cloud/tidb-cloud-billing.md#contract)。如果你已与销售达成合同并收到在线处理邮件，可前往 **Contract** 标签页查看并接受合同。如需了解更多合同信息，欢迎 [联系我们的销售](https://www.pingcap.com/contact-us/)。

**文档变更**

* 新增 [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) 的 [文档](/tidb-cloud/terraform-tidbcloud-provider-overview.md)。

    TiDB Cloud Terraform Provider 是一个插件，允许你使用 [Terraform](https://www.terraform.io/) 管理 TiDB Cloud 资源，如集群、备份和恢复。如果你希望简化资源自动化配置和基础设施工作流，可以参考 [文档](/tidb-cloud/terraform-tidbcloud-provider-overview.md) 体验该插件。

## 2022 年 10 月 11 日

**通用变更**

* 将新建 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0) 升级到 [v6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0)。

**控制台变更**

* 优化 [账单明细页面](/tidb-cloud/tidb-cloud-billing.md#billing-details) 的计费信息：

    * 在 **Summary By Service** 部分提供更细粒度的节点级计费信息。
    * 新增 **Usage Details** 部分，并支持将使用明细下载为 CSV 文件。

## 2022 年 9 月 27 日

**通用变更**

* 支持通过邀请加入多个组织。

    在 TiDB Cloud 控制台，你可以查看已加入的所有组织并进行切换。详情参见 [组织间切换](/tidb-cloud/manage-user-access.md#view-and-switch-between-organizations)。

* 新增 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 页面用于 SQL 诊断。

    在慢查询页面，你可以搜索并查看 TiDB 集群中的所有慢查询，并通过查看其 [执行计划](https://docs.pingcap.com/tidbcloud/explain-overview)、SQL 执行信息等细节，分析每条慢查询的瓶颈。

* 当你重置账号密码时，TiDB Cloud 会将新密码与你最近 4 次使用的密码进行比对，并提醒你避免使用这些密码。最近 4 次使用过的密码均不可再次使用。

    详情参见 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2022 年 9 月 20 日

**通用变更**

* 为自助用户引入 [基于消费额度的账单](/tidb-cloud/tidb-cloud-billing.md#invoices)。

    当你的消费达到额度时，TiDB Cloud 会生成账单。如需提升额度或按月收取账单，请联系 [我们的销售](https://www.pingcap.com/contact-us/)。

* 数据备份费用中免除存储操作费。最新价格信息参见 [TiDB Cloud 价格详情](https://www.pingcap.com/tidb-cloud-pricing-details/)。

**控制台变更**

* 提供全新 Web UI 用于数据导入。新 UI 提升了用户体验，使数据导入更高效。

    通过新 UI，你可以预览待导入数据、查看导入进度，并轻松管理所有导入任务。

**API 变更**

* TiDB Cloud API（Beta）现已对所有用户开放。

    你可以在 TiDB Cloud 控制台创建 API Key 后开始使用 API。更多信息参见 [API 文档](/tidb-cloud/api-overview.md)。

## 2022 年 9 月 15 日

**通用变更**

* 支持通过 TLS 连接到 TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    对于 Dedicated Tier 集群，[Connect](/tidb-cloud/connect-via-standard-connection.md) 对话框的 **Standard Connection** 标签页现在提供下载 TiDB 集群 CA 的链接，并提供 TLS 连接的连接字符串和示例代码。你可以使用第三方 MySQL 客户端、MyCLI 以及 JDBC、Python、Go、Node.js 等多种方式 [通过 TLS 连接 Dedicated Tier 集群](/tidb-cloud/connect-via-standard-connection.md)。该功能保障了应用到 TiDB 集群的数据传输安全。

## 2022 年 9 月 14 日

**控制台变更**

* 优化 [Clusters](https://tidbcloud.com/project/clusters) 页面和集群概览页的 UI，提升用户体验。

    新设计中，升级到 Dedicated Tier、集群连接和数据导入的入口更加突出。

* 为 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群引入 Playground。

    Playground 预置了 GitHub events 数据集，让你无需导入数据或连接客户端，即可通过查询快速体验 TiDB Cloud。

## 2022 年 9 月 13 日

**通用变更**

* 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 Google Cloud 区域：`N. Virginia (us-east4)`。

## 2022 年 9 月 9 日

**通用变更**

* 在 Datadog 中为 Dedicated Tier 集群提供 [更多监控指标](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog)，帮助你更好地了解集群性能状态。

    如果你已 [集成 TiDB Cloud 与 Datadog](/tidb-cloud/monitor-datadog-integration.md)，可直接在 Datadog dashboard 查看这些指标。

## 2022 年 9 月 6 日

**通用变更**

* 将新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) 升级到 [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)。

**控制台变更**

* 现在你可以通过 TiDB Cloud 控制台右上角入口 [申请 PoC](/tidb-cloud/tidb-cloud-poc.md)。

**API 变更**

* 支持通过 [TiDB Cloud API](/tidb-cloud/api-overview.md) 扩容 TiKV 或 TiFlash 节点的存储。你可以通过 API 接口的 `storage_size_gib` 字段进行扩容。

    目前，TiDB Cloud API 仍处于 Beta 阶段，仅支持申请开通。

    详情参见 [修改 Dedicated Tier 集群](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)。

## 2022 年 8 月 30 日

**通用变更**

* 支持基于 AWS PrivateLink 的 endpoint 连接，作为 TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的新网络访问管理选项。

    endpoint 连接安全、私有，不会将你的数据暴露在公网。此外，endpoint 连接支持 CIDR 重叠，便于网络管理。

    详细信息参见 [设置 Private Endpoint 连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

* 在 [Connect](/tidb-cloud/connect-to-tidb-cluster.md) 对话框的 **VPC Peering** 和 **Private Endpoint** 标签页，为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供 MySQL、MyCLI、JDBC、Python、Go、Node.js 的示例连接字符串。

    你只需复制粘贴连接代码到应用，即可轻松连接 Dedicated Tier 集群。

## 2022 年 8 月 24 日

**通用变更**

* 支持暂停或恢复 Dedicated Tier 集群。

    你可以在 TiDB Cloud [暂停或恢复 Dedicated Tier 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。集群暂停期间不会产生 Node Compute Cost。

## 2022 年 8 月 23 日

**通用变更**

* 将新建 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) 升级到 [v6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0)。

**API 变更**

* 引入 TiDB Cloud API（Beta）。

    通过该 API，你可以自动高效地管理 TiDB Cloud 资源（如集群）。更多信息参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta)。

    目前，TiDB Cloud API 仍处于 Beta 阶段，仅支持申请开通。你可以通过提交请求申请 API 访问：

    * 点击 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters) 右下角的 **Help**。
    * 在弹窗的 **Description** 字段填写 "Apply for TiDB Cloud API"，然后点击 **Send**。

## 2022 年 8 月 16 日

* 新增 TiDB 和 TiKV 的 `2 vCPU, 8 GiB (Beta)` 节点规格（Beta）。

    * 每个 `2 vCPU, 8 GiB (Beta)` TiKV 节点的存储规格为 200 GiB 到 500 GiB。

    * 建议使用场景：

        * SMB 的低负载生产环境
        * PoC 和预发布环境
        * 开发环境

* 为 PoC 用户引入 [Credits](/tidb-cloud/tidb-cloud-billing.md#credits)（原名 trial points）。

    你现在可以在 **Billing** 页的 **Credits** 标签下查看组织的 credits 信息，credits 可用于支付 TiDB Cloud 费用。你可以 <a href="mailto:tidbcloud-support@pingcap.com">联系我们</a> 获取 credits。

## 2022 年 8 月 9 日

* 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建新增 GCP 区域 `Osaka` 支持。

## 2022 年 8 月 2 日

* `4 vCPU, 16 GiB` 规格的 TiDB 和 TiKV 节点现已正式发布（GA）。

    * 每个 `4 vCPU, 16 GiB` TiKV 节点的存储规格为 200 GiB 到 2 TiB。
    * 建议使用场景：

        * SMB 的低负载生产环境
        * PoC 和预发布环境
        * 开发环境

* 在 [Dedicated Tier 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)的 **Diagnosis** 标签下新增 [监控页面](/tidb-cloud/built-in-monitoring.md)。

    监控页面为整体性能诊断提供系统级入口。根据自顶向下的性能分析方法，监控页面按数据库时间分解组织 TiDB 性能指标，并以不同颜色展示。通过颜色区分，你可以一眼识别系统整体的性能瓶颈，大幅缩短性能诊断时间，简化分析流程。

* 在 **Data Import** 页为 CSV 和 Parquet 源文件新增 **Custom Pattern** 开关。

    **Custom Pattern** 功能默认关闭。当你需要将文件名符合某一模式的 CSV 或 Parquet 文件导入到同一目标表时，可开启该功能。

    详细信息参见 [导入 CSV 文件](/tidb-cloud/import-csv-files.md) 和 [导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)。

* 新增 TiDB Cloud 支持计划（Basic、Standard、Enterprise、Premium），以满足不同客户组织的支持需求。详情参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

* 优化 [Clusters](https://tidbcloud.com/project/clusters) 页面和集群详情页的 UI：

    * 在 **Clusters** 页面新增 **Connect** 和 **Import data** 按钮。
    * 在集群详情页将 **Connect** 和 **Import data** 按钮移动到右上角。

## 2022 年 7 月 28 日

* 在 **Security Quick Start** 对话框新增 **Allow Access from Anywhere** 按钮，允许你的集群被任意 IP 地址访问。详情参见 [配置集群安全设置](/tidb-cloud/configure-security-settings.md)。

## 2022 年 7 月 26 日

* 支持新建 [Developer Tier 集群](/tidb-cloud/select-cluster-tier.md#starter) 的自动休眠与恢复。

    Developer Tier 集群在 7 天无活动后不会被删除，你可以在一年免费试用期内随时使用。若 24 小时无活动，集群将自动休眠。要恢复集群，可向集群发起新连接或在 TiDB Cloud 控制台点击 **Resume** 按钮。集群将在 50 秒内自动恢复并重新提供服务。

* 为新建 [Developer Tier 集群](/tidb-cloud/select-cluster-tier.md#starter) 增加用户名前缀限制。

    每当你使用或设置数据库用户名时，必须在用户名中包含集群的前缀。详情参见 [用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

* 禁用 [Developer Tier 集群](/tidb-cloud/select-cluster-tier.md#starter) 的备份与恢复功能。

    Developer Tier 集群的备份与恢复功能（包括自动和手动备份）已被禁用。你仍可使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出数据作为备份。

* 将 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的存储规格从 500 MiB 提升至 1 GiB。
* 在 TiDB Cloud 控制台新增面包屑导航，提升导航体验。
* 支持在导入数据到 TiDB Cloud 时配置多条过滤规则。
* 从 **Project Settings** 移除 **Traffic Filters** 页面，并从 **Connect to TiDB** 对话框移除 **Add Rules from Default Set** 按钮。

## 2022 年 7 月 19 日

* 为 [TiKV 节点规格](/tidb-cloud/size-your-cluster.md#tikv-vcpu-and-ram)新增 `8 vCPU, 32 GiB` 选项。你可以为 8 vCPU TiKV 节点选择 `8 vCPU, 32 GiB` 或 `8 vCPU, 64 GiB`。
* 在 [**Connect to TiDB**](/tidb-cloud/connect-via-standard-connection.md) 对话框的示例代码中支持语法高亮，提升代码可读性。你可以更容易地识别需要替换的参数。
* 在 [**Data Import Task**](/tidb-cloud/import-sample-data.md) 页面确认导入任务后，支持自动校验 TiDB Cloud 是否能访问你的源数据。
* 更改 TiDB Cloud 控制台的主题色，使其与 [PingCAP 官网](https://www.pingcap.com/) 保持一致。

## 2022 年 7 月 12 日

* 在 [**Data Import Task**](/tidb-cloud/import-sample-data.md) 页面为 Amazon S3 新增 **Validate** 按钮，帮助你在数据导入前检测数据访问问题。
* 在 [**Payment Method**](/tidb-cloud/tidb-cloud-billing.md#payment-method) 标签下新增 **Billing Profile**。在 **Billing Profile** 中填写税务登记号后，部分税费可能会从发票中免除。详情参见 [编辑账单信息](/tidb-cloud/tidb-cloud-billing.md#billing-profile)。

## 2022 年 7 月 5 日

* 列式存储 [TiFlash](/tiflash/tiflash-overview.md) 现已正式发布（GA）。

    - TiFlash 让 TiDB 成为真正的 HTAP（混合事务/分析处理）数据库。你的应用数据首先存储在 TiKV，然后通过 Raft 共识算法实时同步到 TiFlash，因此是行存到列存的实时复制。
    - 对于有 TiFlash 副本的表，TiDB 优化器会根据代价估算自动选择使用 TiKV 还是 TiFlash 副本。

    体验 TiFlash 带来的优势，请参见 [TiDB Cloud HTAP 快速上手指南](/tidb-cloud/tidb-cloud-htap-quickstart.md)。

* 支持为 Dedicated Tier 集群 [扩容 TiKV 和 TiFlash 存储](/tidb-cloud/scale-tidb-cluster.md#change-storage)。
* 支持在节点规格字段显示内存信息。

## 2022 年 6 月 28 日

* 将 TiDB Cloud Dedicated Tier 从 [TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1) 升级到 [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)。

## 2022 年 6 月 23 日

* 提升 TiDB Cloud 上 [TiKV 存储容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)上限。

    * 8 vCPU 或 16 vCPU TiKV：支持最大 4 TiB 存储容量。
    * 4 vCPU TiKV：支持最大 2 TiB 存储容量。

## 2022 年 6 月 21 日

* 为 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群创建新增 GCP 区域 `Taiwan` 支持。
* 支持在 TiDB Cloud 控制台 [更新用户信息](/tidb-cloud/manage-user-access.md#manage-user-profiles)，包括名、姓、公司名、国家和手机号。
* 在 [**Connect to TiDB**](/tidb-cloud/connect-via-standard-connection.md) 对话框中提供 MySQL、MyCLI、JDBC、Python、Go、Node.js 的连接字符串，便于你快速连接 TiDB 集群。
* 在数据导入时自动从 bucket URI 获取 bucket 区域，无需手动填写。

## 2022 年 6 月 16 日

* 简化 [集群创建流程](/tidb-cloud/create-tidb-cluster.md)。

    - 创建集群时，TiDB Cloud 会提供默认集群名，你可以直接使用或自定义。
    - 创建集群时，无需在 **Create a Cluster** 页面设置密码。
    - 在集群创建过程中或创建后，你可以在 **Security Quick Start** 对话框设置 root 密码和允许连接的 IP 地址。

## 2022 年 6 月 14 日

* 将 Developer Tier 的 TiDB Cloud 升级到 [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)。
* 优化 **Project Settings** 入口。在 TiDB Cloud 控制台中，你可以选择目标项目并通过 **Project Settings** 标签页快速进入设置。
* 优化密码过期体验，在 TiDB Cloud 控制台提供过期提示信息。

## 2022 年 6 月 7 日

* 新增 [Try Free](https://tidbcloud.com/free-trial) 注册页面，便于快速注册 TiDB Cloud。
* 从方案选择页面移除 **Proof of Concept plan** 选项。如需申请 14 天免费 PoC 试用，<a href="mailto:tidbcloud-support@pingcap.com">联系我们</a>。详情参见 [TiDB Cloud PoC 试用](/tidb-cloud/tidb-cloud-poc.md)。
* 提升系统安全性，要求使用邮箱和密码注册 TiDB Cloud 的用户每 90 天重置一次密码。详情参见 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)。

## 2022 年 5 月 24 日

* 支持在 [创建](/tidb-cloud/create-tidb-cluster.md) 或 [恢复](/tidb-cloud/backup-and-restore.md#restore) Dedicated Tier 集群时自定义 TiDB 端口号。

## 2022 年 5 月 19 日

* 为 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群创建新增 AWS 区域 `Frankfurt` 支持。

## 2022 年 5 月 18 日

* 支持使用 GitHub 账号 [注册](https://tidbcloud.com/signup) TiDB Cloud。

## 2022 年 5 月 13 日

* 支持使用 Google 账号 [注册](https://tidbcloud.com/signup) TiDB Cloud。

## 2022 年 5 月 1 日

* 支持在 [创建](/tidb-cloud/create-tidb-cluster.md) 或 [恢复](/tidb-cloud/backup-and-restore.md#restore) [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群时配置 TiDB、TiKV、TiFlash 的 vCPU 规格。
* 新增 AWS 区域 `Mumbai` 支持集群创建。
* 更新 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md) 的计算、存储和数据传输费用。

## 2022 年 4 月 7 日

* 将 Developer Tier 的 TiDB Cloud 升级到 [TiDB v6.0.0](https://docs-archive.pingcap.com/tidb/v6.0/release-6.0.0-dmr)。

## 2022 年 3 月 31 日

TiDB Cloud 现已正式发布。你可以 [注册](https://tidbcloud.com/signup) 并选择以下方式之一：

* 免费体验 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter)。
* <a href="mailto:tidbcloud-support@pingcap.com">联系我们</a> 申请 14 天免费 PoC 试用。
* 通过 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 获得完整访问权限。

## 2022 年 3 月 25 日

新功能：

* 支持 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

    通过 TiDB Cloud 内置告警功能，当你项目中的 TiDB Cloud 集群触发内置告警条件时，你会收到邮件通知。

## 2022 年 3 月 15 日

通用变更：

* 不再有固定集群规格的集群类型。你可以轻松自定义 TiDB、TiKV、TiFlash 的 [集群规格](/tidb-cloud/size-your-cluster.md)。
* 支持为已有无 TiFlash 的集群添加 [TiFlash](/tiflash/tiflash-overview.md) 节点。
* 支持在 [新建集群](/tidb-cloud/create-tidb-cluster.md) 时指定存储规格（500 到 2048 GiB）。集群创建后存储规格不可更改。
* 新增公共区域：`eu-central-1`。
* 废弃 8 vCPU TiFlash，提供 16 vCPU TiFlash。
* 分离 CPU 和存储价格（均享 30% 公测折扣）。
* 更新 [计费信息](/tidb-cloud/tidb-cloud-billing.md) 和 [价格表](https://www.pingcap.com/pricing/)。

新功能：

* 支持 [Prometheus 和 Grafana 集成](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)。

    通过 Prometheus 和 Grafana 集成，你可以配置 [Prometheus](https://prometheus.io/) 服务从 TiDB Cloud endpoint 读取关键指标，并使用 [Grafana](https://grafana.com/) 查看这些指标。

* 支持根据新集群所选区域分配默认备份时间。

    详细信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)。

## 2022 年 3 月 4 日

新功能：

* 支持 [Datadog 集成](/tidb-cloud/monitor-datadog-integration.md)。

    通过 Datadog 集成，你可以配置 TiDB Cloud 将集群的指标数据发送到 [Datadog](https://www.datadoghq.com/)。之后你可以直接在 Datadog dashboard 查看这些指标。

## 2022 年 2 月 15 日

通用变更：

* 将 Developer Tier 的 TiDB Cloud 升级到 [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)。

改进：

* 支持在导入 [CSV 文件](/tidb-cloud/import-csv-files.md) 或 [Apache Parquet 文件](/tidb-cloud/import-parquet-files.md) 到 TiDB Cloud 时自定义文件名。

## 2022 年 1 月 11 日

通用变更：

* 将 TiDB Operator 升级到 [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)。

改进：

* 在 [**Connect**](/tidb-cloud/connect-via-standard-connection.md) 页面为 MySQL 客户端新增建议参数 `--connect-timeout 15`。

Bug 修复：

* 修复了当密码包含单引号时用户无法创建集群的问题。
* 修复了即使组织只有一位 owner，该 owner 也可以被删除或更改为其他角色的问题。