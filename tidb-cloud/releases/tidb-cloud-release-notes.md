---
title: 2026 年 TiDB Cloud 发布说明
summary: 了解 2026 年 TiDB Cloud 的发布说明。
aliases: ['/zh/tidbcloud/supported-tidb-versions','/zh/tidbcloud/release-notes']
---

# 2026 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2026 年的发布说明。

## 2026 年 3 月 24 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 在 TiDB Cloud 的 [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md) 中新增 **Public Endpoint** 状态，以提升安全追踪能力。

**控制台变更**

- 支持对 Y 轴使用对数刻度，以提升大数值差异统计/指标（信息）的可视化效果。高区间和低区间的波动都能清晰可见，更易于识别异常。

## 2026 年 3 月 10 日

**通用变更**

- **TiDB Cloud Essential**

    - 在数据流场景下，私有链路连接支持 Amazon MSK Provisioned。

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 现已支持为 [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) 集群创建私有链路连接。该功能允许 changefeed 通过私有网络连接到 Amazon MSK Provisioned 集群，无需暴露流量到公网。

        详情参见 [通过 Private Link 连接 Amazon MSK Provisioned](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)。

## 2026 年 3 月 3 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持使用 AWS Role ARN 对 Amazon S3 sink 的 changefeed 进行认证。

        你现在可以在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上，为 Amazon S3 sink 的 changefeed 配置 IAM Role ARN 认证，除了现有的 AK/SK 认证方式外。该功能通过启用短时凭证和自动轮换提升安全性，简化密钥管理，并支持最小权限实践。

        详情参见 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

    - 优化 TiKV 和 TiFlash 存储用量的统计方式。

        统计/指标（信息）和告警系统中 TiKV 与 TiFlash 的存储用量计算现已纳入 WAL 文件和临时文件，提供更准确的容量与用量监控。

        详情参见 [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md)。

## 2026 年 2 月 10 日

**通用变更**

- **TiDB Cloud Starter**

    - 新建 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本由 [v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6) 升级至 [v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)。

- **TiDB Cloud Essential**

    - 支持内置告警。

        内置告警允许你通过邮件、Slack、Zoom、Flashduty 和 PagerDuty 订阅并即时接收告警。你还可以为每种告警类型自定义阈值。

        详情参见 [TiDB Cloud Built-in Alerting](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential)。

- **TiDB Cloud Dedicated**

    - 支持通过 Private Link 从 Azure Blob Storage 导入数据。
  
        当你将数据从 Azure Blob Storage 导入到 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群时，现在可以选择 Private Link 作为连接方式，通过 Azure 私有端点而非公网进行连接。该功能为限制公网访问的存储账户提供了安全、网络隔离的数据导入能力。

        详情参见 [从云存储导入示例数据（SQL 文件）](/tidb-cloud/import-sample-data.md)、[从云存储导入 CSV 文件](/tidb-cloud/import-csv-files.md) 和 [从云存储导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)。

    - 在 TiDB Cloud 的 Console Audit Logging 中新增 “Enable/Disable Public Endpoint” 事件，以提升安全追踪能力。

## 2026 年 2 月 3 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 changefeed 数据 sink 到 Azure Blob Storage。

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现已支持将 changefeed 数据直接 sink 到 Azure Blob Storage。该功能帮助基于 Azure 的用户高效归档变更数据，便于下游分析和长期保存。同时无需中间消息队列，降低成本，并保持与现有 Amazon S3 及 Google Cloud Storage (GCS) sink 的格式兼容性。

        详情参见 [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2026 年 1 月 27 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持 Flashduty 和 PagerDuty 作为告警订阅渠道。
  
        这些集成旨在简化你的事件管理流程并提升运维可靠性。
  
        详情参见 [通过 Flashduty 订阅](/tidb-cloud/monitor-alert-flashduty.md) 和 [通过 PagerDuty 订阅](/tidb-cloud/monitor-alert-pagerduty.md)。

## 2026 年 1 月 20 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 视图和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（beta）。

        TiDB Cloud 现已支持客户端 IP 透传，使 Slow Query 视图和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实客户端 IP 地址，而非负载均衡器（LB）IP。该功能有助于准确识别数据库请求的真实来源，便于排查和分析。

        目前该功能为 beta，仅在 AWS 区域 `Frankfurt (eu-central-1)` 可用。

- **TiDB Cloud Essential**

    - 支持数据迁移（beta）。

        你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 使用数据迁移功能，将任意 MySQL 兼容数据库的数据无缝迁移到你的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。

        - 支持的源数据库包括多种 MySQL 兼容系统，如自建 MySQL、Amazon RDS、阿里云 RDS 和 PolarDB。
        - 数据迁移支持的连接方式包括公网连接和 PrivateLink，兼顾易用性与企业级安全：

            - **Public connection**：通过安全加密通道，快速通过互联网连接到你的源数据库。
            - **PrivateLink**：在你的源 VPC 与 TiDB Cloud 之间建立安全私有连接，绕过公网，确保数据隐私和降低网络延时。

      目前，数据迁移功能仅支持逻辑模式。
  
        详情参见 [使用数据迁移迁移现有及增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 和 [使用数据迁移迁移增量数据](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

    - 在 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 视图、[DB 审计日志](/tidb-cloud/essential-database-audit-logging.md) 和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（beta）

        TiDB Cloud 现已支持客户端 IP 透传，使 Slow Query 视图、DB 审计日志和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实客户端 IP 地址，而非负载均衡器（LB）IP。该功能有助于准确识别数据库请求的真实来源，便于排查和分析。

        目前该功能为 beta，仅在 AWS 区域 `Frankfurt (eu-central-1)` 可用。

**控制台变更**

- 提升支持体验，提供基于订阅计划的支持选项。

    [TiDB Cloud 控制台](https://tidbcloud.com/) 现已提供基于订阅计划的支持选项，优化了所有订阅计划下的支持体验。具体更新包括：

    - **基于计划的支持跳转**：在集群概览页，点击 **Get Support** 按钮后，会根据你的订阅计划跳转到最相关的资源。Basic 计划用户会跳转到 **Support Plan** 面板，付费计划用户则跳转到 **Support Portal**。
    - **优化 Help Center 菜单**：将帮助菜单项重命名为 **Support Options** 和 **Support Tickets**，更准确反映可用服务。新增提示，说明技术支持工单仅对付费计划开放。
    - **明确社区支持入口**：在 **Support Plan** 选项中，Slack 和 Discord 被明确标识为 Basic 计划用户的主要技术支持渠道。以下文档已简化，明确支持渠道政策及社区访问方式：[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)、[Connected Care Overview](/tidb-cloud/connected-care-overview.md) 和 [Connected Care Details](/tidb-cloud/connected-care-detail.md)。
    - **面向操作的 Support Plan UI**：重新设计 **Support Plan** 窗口，优先展示你当前订阅计划下可用的支持选项，而非通用计划对比。该变更帮助你快速识别基于当前计划的支持方式。

  详情参见 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 2026 年 1 月 15 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/) 升级至 [v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/)。