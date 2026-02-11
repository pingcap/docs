---
title: 2026 年 TiDB Cloud 发布说明
summary: 了解 2026 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2026 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2026 年的发布说明。

## 2026 年 2 月 10 日

**通用变更**

- **TiDB Cloud Starter**

    - 将新建 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6) 升级到 [v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)。

- **TiDB Cloud Essential**

    - 支持内置报警/告警。

        内置报警/告警允许你通过 email、Slack、Zoom、Flashduty 和 PagerDuty 订阅并接收即时报警/告警。你还可以通过为每种报警/告警类型定义特定阈值，来自定义报警/告警。

        更多信息，参见 [TiDB Cloud 内置报警/告警](/tidb-cloud/monitor-built-in-alerting.md)。

- **TiDB Cloud Dedicated**

    - 支持通过 Private Link 从 Azure Blob Storage 导入数据。

        当你将数据从 Azure Blob Storage 导入到 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群时，现在可以选择 Private Link 作为连接方式，通过 Azure 私有端点进行连接，而不是通过公网。该功能为限制公网访问的存储账户提供了安全、网络隔离的数据导入能力。

        更多信息，参见 [从云存储导入示例数据（SQL 文件）](/tidb-cloud/import-sample-data.md)、[从云存储导入 CSV 文件](/tidb-cloud/import-csv-files.md) 和 [从云存储导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)。

    - 在 TiDB Cloud 的 Console 审计日志中新增“启用/禁用公网端点”事件，以提升安全追踪能力。

## 2026 年 2 月 3 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 changefeed 数据下沉到 Azure Blob Storage。

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现在支持将 changefeed 数据直接下沉到 Azure Blob Storage。该功能使基于 Azure 的用户能够高效归档变更数据，用于下游分析和长期保存。同时，通过省去中间消息队列，降低了成本，并保持了与现有 Amazon S3 和 Google Cloud Storage (GCS) sink 的格式兼容性。

        更多信息，参见 [下沉到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2026 年 1 月 27 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 Flashduty 和 PagerDuty 作为报警/告警订阅渠道。

        这些集成旨在简化你的事件管理流程，并提升运维可靠性。

        更多信息，参见 [通过 Flashduty 订阅](/tidb-cloud/monitor-alert-flashduty.md) 和 [通过 PagerDuty 订阅](/tidb-cloud/monitor-alert-pagerduty.md)。

## 2026 年 1 月 20 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实 client IP 地址（测试版）。

        TiDB Cloud 现已支持 client IP 透传，使慢查询视图和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的 client IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

- **TiDB Cloud Essential**

    - 支持数据迁移（测试版）。

        你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 使用数据迁移功能，将数据从任意 MySQL 兼容数据库无缝迁移到你的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。

        - 支持的源数据库包括多种 MySQL 兼容系统，如自建 MySQL、Amazon RDS、阿里云 RDS 和 PolarDB。
        - 数据迁移支持的连接方式包括公网连接和 PrivateLink，兼顾易用性和企业级安全：

            - **公网连接**：通过安全加密通道，快速通过互联网连接到你的源数据库。
            - **PrivateLink**：在你的源 VPC 与 TiDB Cloud 之间建立安全私有连接，绕过公网，确保数据隐私和降低网络延时。

      目前，数据迁移功能仅支持逻辑模式。

        更多信息，参见 [使用数据迁移迁移现有及增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 和 [使用数据迁移迁移增量数据](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图、[数据库审计日志](/tidb-cloud/essential-database-audit-logging.md) 和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实 client IP 地址（测试版）

        TiDB Cloud 现已支持 client IP 透传，使慢查询视图、数据库审计日志和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的 client IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

**控制台变更**

- 通过计划感知型支持选项，提升支持体验。

    [TiDB Cloud 控制台](https://tidbcloud.com/) 现已提供计划感知型支持选项，提升所有订阅计划下的支持体验。此次更新包括：

    - **计划感知型支持跳转**：在集群概览页面，点击 **Get Support** 按钮（在 **Actions** 列），会根据你的订阅计划跳转到最相关的资源。Basic 计划用户会被引导至 **Support Plan** 面板，付费计划用户则跳转至 **Support Portal**。
    - **优化的帮助中心菜单**：将帮助菜单项重命名为 **Support Options** 和 **Support Tickets**，更好地反映可用服务。新增提示，说明技术支持工单仅对付费计划开放。
    - **清晰的社区支持入口**：在 **Support Plan** 选项中，Slack 和 Discord 被明确标识为 Basic 计划用户的主要技术支持渠道。以下文档已优化，明确支持渠道政策和社区访问方式：[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)、[Connected Care Overview](/tidb-cloud/connected-care-overview.md) 和 [Connected Care Details](/tidb-cloud/connected-care-detail.md)。
    - **以操作为导向的 Support Plan UI**：重新设计 **Support Plan** 窗口，优先展示你当前订阅计划下可用的支持选项，而非通用计划对比。此更改有助于你快速识别基于当前计划的支持获取方式。

  更多信息，参见 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 2026 年 1 月 15 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 将新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/) 升级到 [v8.5.5](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/)。