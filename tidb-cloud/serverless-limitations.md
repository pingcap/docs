---
title: TiDB Cloud Serverless 限制与配额
summary: 了解 TiDB Cloud Serverless 的限制。
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloud Serverless 限制与配额

<!-- markdownlint-disable MD026 -->

TiDB Cloud Serverless 支持几乎所有 TiDB 支持的工作负载，但与 TiDB 自主部署版或 TiDB Cloud 专属集群相比，TiDB Cloud Serverless 集群在某些功能上存在差异。本文档介绍了 TiDB Cloud Serverless 的相关限制。

我们正在不断缩小 TiDB Cloud Serverless 与 TiDB Cloud 专属集群之间的功能差距。如果你需要这些尚未支持的功能或能力，请使用 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 或 [联系我们](https://www.pingcap.com/contact-us/?from=en) 提交功能需求。

## 限制

### 审计日志

- [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md) 目前不可用。

### 连接

- 仅支持 [Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) 和 [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) 连接方式。你无法使用 [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) 连接到 TiDB Cloud Serverless 集群。
- 不支持 [IP Access list](/tidb-cloud/configure-ip-access-list.md)。

### 加密

- 你在 TiDB Cloud Serverless 集群中持久化的数据会使用云服务商提供的加密工具进行加密。对于 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)，在集群创建过程中可选择启用第二层加密，为默认的静态加密提供额外的安全保障。
- 目前不支持使用 [客户自管加密密钥（CMEK）](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

### 维护窗口

- [维护窗口](/tidb-cloud/configure-maintenance-window.md) 目前不可用。

### 监控与诊断

- 不支持 [第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。
- 不支持 [内置告警](/tidb-cloud/monitor-built-in-alerting.md)。
- 不支持 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)。
- 不支持 [Index Insight](/tidb-cloud/tune-performance.md#index-insight-beta)。

### 自助升级

- TiDB Cloud Serverless 是 TiDB 的全托管部署。TiDB Cloud Serverless 的主版本和次版本升级由 TiDB Cloud 统一管理，用户无法自行发起升级。

### 流式数据

- TiDB Cloud Serverless 目前不支持 [Changefeed](/tidb-cloud/changefeed-overview.md)。
- TiDB Cloud Serverless 目前不支持 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

### 生存时间（TTL）

- 在 TiDB Cloud Serverless 中，表的 [`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) 属性固定为 `15m`，不可修改。这意味着 TiDB Cloud Serverless 每 15 分钟会调度一次后台任务清理过期数据。

### 其他

- 事务持续时间不能超过 30 分钟。
- 有关 SQL 限制的更多细节，请参阅 [Limited SQL Features](/tidb-cloud/limited-sql-features.md)。

## 使用配额

在 TiDB Cloud 的每个组织中，默认最多可以创建 5 个 [免费集群](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。如需创建更多 TiDB Cloud Serverless 集群，你需要添加信用卡并创建 [可扩展集群](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) 以进行使用。

对于你组织中的前 5 个 TiDB Cloud Serverless 集群（无论是免费还是可扩展），TiDB Cloud 为每个集群提供如下免费使用配额：

- 行存储：5 GiB
- 列存储：5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

Request Unit（RU）是用于衡量查询或事务资源消耗的单位。它是一种指标，可以帮助你估算处理特定数据库请求所需的计算资源。Request Unit 也是 TiDB Cloud Serverless 服务的计费单位。

当集群达到其使用配额时，将立即拒绝所有新的连接尝试，直到你 [增加配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) 或在新月开始时重置使用量。已在达到配额前建立的连接会保持活跃，但会受到限流影响。

如需了解不同资源（包括读、写、SQL CPU 和网络出口）的 RU 消耗、定价详情及限流信息，请参阅 [TiDB Cloud Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

如果你希望创建配额更高的 TiDB Cloud Serverless 集群，可以选择可扩展集群计划，并在集群创建页面编辑消费上限。更多信息请参见 [Create a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)。

在创建 TiDB Cloud Serverless 集群后，你仍然可以在集群概览页面查看和编辑消费上限。更多信息请参见 [Manage Spending Limit for TiDB Cloud Serverless Clusters](/tidb-cloud/manage-serverless-spend-limit.md)。