---
title: 2026 年 TiDB Cloud 发布说明
summary: 了解 2026 年 TiDB Cloud 的发布说明。
aliases: ['/zh/tidbcloud/supported-tidb-versions','/zh/tidbcloud/release-notes']
---

# 2026 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2026 年的发布说明。

## 2026 年 3 月 31 日

**通用变更**

- **TiDB Cloud Essential**

    - 支持配置私有端点白名单。

        你现在可以通过在 [TiDB Cloud 控制台](https://tidbcloud.com) 配置白名单，更加安全和便捷地管理私有端点的访问。在白名单中，你可以指定允许连接的 AWS VPC Endpoint ID 和阿里云 endpoint ID。

        详细信息请参见以下文档：

        - [通过 AWS 私有端点连接](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) 
        - [通过阿里云私有端点连接](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    - 启用 Prometheus 统计/指标（信息）集成（预览版）。

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 在集群级别管理 Prometheus 集成。该功能可以让你将 TiDB Cloud Essential 集群的统计/指标（信息）无缝发送到 Prometheus，实现统一平台上的高级报警/告警。

        集成步骤请参见 [将 TiDB Cloud 集成到 Prometheus 和 Grafana](/tidb-cloud/prometheus-grafana-integration.md)。

## 2026 年 3 月 24 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 在 TiDB Cloud 的 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md) 中新增 **Public Endpoint** 状态，以提升安全追踪能力。

**控制台变更**

- 支持对 Y 轴使用对数坐标，以提升大数值差异统计/指标（信息）的可视化效果。高区间和低区间的波动都能清晰可见，更易于识别异常。

## 2026 年 3 月 10 日

**通用变更**

- **TiDB Cloud Essential**

    - 在数据流场景下，私有链路连接支持 Amazon MSK Provisioned。

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 现在支持为 [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) 集群创建私有链路连接。该功能允许变更数据流（changefeed）通过私有网络连接到 Amazon MSK Provisioned 集群，无需暴露流量到公网。

        详细信息请参见 [通过私有链路连接 Amazon MSK Provisioned](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)。

## 2026 年 3 月 3 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 针对 Amazon S3 sink 的 changefeed 支持使用 AWS Role ARN 进行认证。

        你现在可以在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上，为 Amazon S3 sink 的 changefeed 配置 IAM Role ARN 认证，除了现有的 AK/SK 认证方式外。该功能通过启用短时凭证和自动轮换提升安全性，简化密钥管理，并支持最小权限原则。

        详细信息请参见 [同步到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

    - 优化 TiKV 和 TiFlash 的存储用量计算。

        现在，TiKV 和 TiFlash 的存储用量在统计/指标（信息）和报警/告警系统中的计算会包含 WAL 文件和临时文件，从而提供更准确的容量和用量监控。

        详细信息请参见 [TiDB Cloud 内置统计/指标（信息）](/tidb-cloud/built-in-monitoring.md)。

## 2026 年 2 月 10 日

**通用变更**

- **TiDB Cloud Starter**

    - 新建 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本从 [v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6) 升级到 [v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3)。

- **TiDB Cloud Essential**

    - 支持内置报警/告警。

        内置报警/告警允许你通过邮件、Slack、Zoom、Flashduty 和 PagerDuty 订阅并即时接收报警/告警。你还可以为每种报警/告警类型自定义阈值。

        详细信息请参见 [TiDB Cloud 内置报警/告警](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential)。

- **TiDB Cloud Dedicated**

    - 支持通过 Private Link 从 Azure Blob Storage 导入数据。
  
        当你将数据从 Azure Blob Storage 导入到 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群时，现在可以选择 Private Link 作为连接方式，通过 Azure 私有端点进行连接，而无需经过公网。该功能为限制公网访问的存储账户提供了安全、网络隔离的数据导入能力。

        详细信息请参见 [从云存储导入示例数据（SQL 文件）](/tidb-cloud/import-sample-data.md)、[从云存储导入 CSV 文件](/tidb-cloud/import-csv-files.md) 和 [从云存储导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)。

    - 在 TiDB Cloud 的控制台审计日志中新增 “启用/禁用 Public Endpoint” 事件，以提升安全追踪能力。

## 2026 年 2 月 3 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 changefeed 数据同步到 Azure Blob Storage。

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 现在支持将 changefeed 数据直接同步到 Azure Blob Storage。该功能让基于 Azure 的用户能够高效归档变更数据，用于下游分析和长期保存。同时，通过无需中间消息队列降低成本，并保持与现有 Amazon S3 和 Google Cloud Storage (GCS) sink 的格式兼容。

        详细信息请参见 [同步到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2026 年 1 月 27 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 Flashduty 和 PagerDuty 作为报警/告警订阅渠道。
  
        这些集成旨在简化你的事件管理流程并提升运维可靠性。
  
        详细信息请参见 [通过 Flashduty 订阅](/tidb-cloud/monitor-alert-flashduty.md) 和 [通过 PagerDuty 订阅](/tidb-cloud/monitor-alert-pagerduty.md)。

## 2026 年 1 月 20 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（测试版）。

        TiDB Cloud 现在支持客户端 IP 透传，使慢查询视图和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实客户端 IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

- **TiDB Cloud Essential**

    - 支持数据迁移（测试版）。

        你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 使用数据迁移功能，将数据从任意 MySQL 兼容数据库无缝迁移到你的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。

        - 支持的源数据库包括多种 MySQL 兼容系统，如自建 MySQL、Amazon RDS、阿里云 RDS 和 PolarDB。
        - 数据迁移支持的连接方式包括公网连接和 PrivateLink，兼顾易用性和企业级安全：

            - **公网连接**：通过安全加密通道，快速连接到你的源数据库。
            - **PrivateLink**：在你的源 VPC 与 TiDB Cloud 之间建立安全私有连接，绕过公网，确保最大的数据隐私和更低的网络延时。

      目前，数据迁移功能仅支持逻辑模式。
  
        详细信息请参见 [使用数据迁移迁移全量及增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 和 [使用数据迁移迁移增量数据](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图、[数据库审计日志](/tidb-cloud/essential-database-audit-logging.md) 和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（测试版）

        TiDB Cloud 现在支持客户端 IP 透传，使慢查询视图、数据库审计日志和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实客户端 IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

**控制台变更**

- 通过计划感知型支持选项，提升支持体验。

    [TiDB Cloud 控制台](https://tidbcloud.com/) 现在提供计划感知型支持选项，以提升所有订阅计划下的支持体验。更新内容包括：

    - **计划感知型支持跳转**：在集群概览页面，点击 **Get Support** 按钮会根据你的订阅计划跳转到最相关的资源。Basic 计划用户会跳转到 **Support Plan** 面板，付费计划用户会跳转到 **Support Portal**。
    - **优化 Help Center 菜单**：将帮助菜单项重命名为 **Support Options** 和 **Support Tickets**，更准确反映可用服务。新增提示，说明技术支持工单仅对付费计划开放。
    - **社区支持入口更清晰**：在 **Support Plan** 选项中，Slack 和 Discord 被明确标识为 Basic 计划用户的主要技术支持渠道。以下文档已优化，明确支持渠道政策和社区访问方式：[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)、[Connected Care Overview](/tidb-cloud/connected-care-overview.md) 和 [Connected Care Details](/tidb-cloud/connected-care-detail.md)。
    - **面向操作的 Support Plan UI**：重新设计 **Support Plan** 窗口，优先展示你当前订阅计划下可用的支持选项，而不是通用的计划对比。该变更帮助你快速识别基于当前计划的支持方式。

  详细信息请参见 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 2026 年 1 月 15 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本从 [v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/) 升级到 [v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/)。