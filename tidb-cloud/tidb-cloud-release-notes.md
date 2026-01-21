---
title: 2026 年 TiDB Cloud 发布说明
summary: 了解 2026 年 TiDB Cloud 的发布说明。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2026 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2026 年的发布说明。

## 2026 年 1 月 20 日

**通用变更**

- **TiDB Cloud Starter**

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图和 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（测试版）。

        TiDB Cloud 现已支持客户端 IP 透传，使慢查询视图和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的客户端 IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

- **TiDB Cloud Essential**

    - 支持数据迁移（测试版）。

        现在，你可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 中使用数据迁移功能，将数据从任意 MySQL 兼容数据库无缝迁移到你的 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群。

        - 支持的源数据库包括多种 MySQL 兼容系统，如自建 MySQL、Amazon RDS、阿里云 RDS 以及 PolarDB。
        - 数据迁移支持的连接方法包括公网连接和 PrivateLink，兼顾易用性与企业级安全性：

            - **公网连接**：通过安全加密通道，快速通过互联网连接到你的源数据库。
            - **PrivateLink**：在你的源 VPC 与 TiDB Cloud 之间建立安全私有连接，绕过公网，确保数据隐私并降低网络延时。

      目前，数据迁移功能仅支持逻辑模式。
  
        详细信息参见 [使用数据迁移迁移现有及增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 和 [使用数据迁移迁移增量数据](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

    - 在 [慢查询](/tidb-cloud/tune-performance.md#slow-query) 视图、[数据库审计日志](/tidb-cloud/essential-database-audit-logging.md) 以及 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 表中显示真实客户端 IP 地址（测试版）

        TiDB Cloud 现已支持客户端 IP 透传，使慢查询视图、数据库审计日志和 `INFORMATION_SCHEMA.PROCESSLIST` 表能够显示真实的客户端 IP 地址，而不是负载均衡器（LB）IP。该功能有助于更准确地识别数据库请求的真实来源，便于排查和分析。

        目前，该功能为测试版，仅在 AWS 区域 `Frankfurt (eu-central-1)` 提供。

**控制台变更**

- 提升支持体验，提供基于订阅计划的支持选项。

    [TiDB Cloud 控制台](https://tidbcloud.com/) 现已提供基于订阅计划的支持选项，提升所有订阅计划下的支持体验。此次更新包括：

    - **基于计划的支持跳转**：在集群总览页面，点击 **Get Support** 按钮（位于 **Actions** 列）后，将根据你的订阅计划跳转到最相关的资源。Basic 计划用户会跳转到 **Support Plan** 面板，付费计划用户则跳转到 **Support Portal**。
    - **优化 Help Center 菜单**：将帮助菜单项重命名为 **Support Options** 和 **Support Tickets**，更准确地反映可用服务。新增提示，说明技术支持工单仅对付费计划开放。
    - **清晰的社区支持入口**：在 **Support Plan** 选项中，Slack 和 Discord 被明确标识为 Basic 计划用户的主要技术支持渠道。以下文档已优化，进一步明确支持渠道政策及社区访问方式：[TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)、[Connected Care Overview](/tidb-cloud/connected-care-overview.md) 和 [Connected Care Details](/tidb-cloud/connected-care-detail.md)。
    - **以操作为导向的 Support Plan UI**：重新设计 **Support Plan** 窗口，优先展示你当前订阅计划下可用的支持选项，而非通用的计划对比。此变更有助于你快速识别基于当前计划的支持获取方式。

  详细信息参见 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 2026 年 1 月 15 日

**通用变更**

- **TiDB Cloud Dedicated**

    - 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/) 升级至 [v8.5.5](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/)。