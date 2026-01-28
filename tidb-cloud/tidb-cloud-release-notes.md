---
title: 2026 年 TiDB Cloud 发布说明
summary: 了解 2026 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2026 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2026 年的发布说明。

## 2026 年 1 月 27 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 支持将 Flashduty 和 PagerDuty 作为报警订阅渠道。
  
        这些集成旨在简化你的事件管理流程，并提升运维可靠性。
  
        详细信息参见 [通过 Flashduty 订阅](/tidb-cloud/monitor-alert-flashduty.md) 和 [通过 PagerDuty 订阅](/tidb-cloud/monitor-alert-pagerduty.md)。

## 2026 年 1 月 20 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实 client IP 地址（测试版）。

        TiDB Cloud 现已支持 client IP 透传，使慢查询视图和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的 client IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库 request 的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

- **TiDB Cloud Essential**

    - 支持数据 migration（测试版）。

        你现在可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 使用数据 migration 功能，将任意 MySQL-compatible 数据库的数据无缝迁移到你的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) cluster。

        - 支持的源数据库包括多种 MySQL-compatible 系统，如自建 MySQL、Amazon RDS、阿里云 RDS 以及 PolarDB。
        - 数据 migration 支持的连接 method 包括公网连接和 PrivateLink，兼顾易用性与企业级安全：

            - **公网连接**：通过安全加密通道，快速通过互联网连接到你的源数据库。
            - **PrivateLink**：在你的源 VPC 与 TiDB Cloud 之间建立安全私有连接，绕过公网，确保数据隐私并降低网络 latency。

      目前，数据 migration 功能仅支持 logic 模式。
  
        详细信息参见 [使用数据 migration 迁移现有及增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 和 [使用数据 migration 迁移增量数据](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图、[数据库审计日志](/tidb-cloud/essential-database-audit-logging.md) 和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实 client IP 地址（测试版）

        TiDB Cloud 现已支持 client IP 透传，使慢查询视图、数据库审计日志和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的 client IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库 request 的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

**控制台变更**

- 通过支持计划感知的支持选项，提升支持体验。

    [TiDB Cloud 控制台](https://tidbcloud.com/) 现已提供计划感知的支持选项，以提升所有订阅计划下的支持体验。此次更新包括：

    - **计划感知的支持重定向**：在 cluster 概览页面，点击 **Get Support** 按钮（位于 **Actions** 列）会根据你的订阅计划将你引导至最相关的资源。Basic 计划用户会被引导至 **Support Plan** 面板，付费计划用户则会被引导至 **Support Portal**。
    - **优化的帮助中心菜单**：将帮助菜单项重命名为 **Support Options** 和 **Support Tickets**，以更好地反映可用服务。新增提示，明确技术支持工单仅对付费计划开放。
    - **清晰的社区支持 access**：在 **Support Plan** 选项中，Slack 和 Discord 被明确标识为 Basic 计划用户的主要技术支持渠道。以下文档已优化，进一步明确支持渠道政策及社区 access：[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)、[Connected Care Overview](/tidb-cloud/connected-care-overview.md) 和 [Connected Care Details](/tidb-cloud/connected-care-detail.md)。
    - **以操作为导向的 Support Plan UI**：重新设计 **Support Plan** 窗口，优先展示你当前订阅计划下可用的支持选项，而非通用计划对比。此更改有助于你快速识别基于当前计划的支持方式。

  详细信息参见 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 2026 年 1 月 15 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster 的默认 TiDB 版本由 [v8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/) 升级至 [v8.5.5](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/)。