---
title: TiDB Cloud Starter 和 Essential 的限制与配额
summary: 了解 TiDB Cloud Starter 的限制。
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloud Starter 和 Essential 的限制与配额

<!-- markdownlint-disable MD026 -->

TiDB Cloud Starter 和 Essential 支持几乎所有 TiDB 支持的工作负载，但与 TiDB 自建版或 TiDB Cloud Dedicated 集群相比，存在一些功能差异。本文档介绍了 TiDB Cloud Starter 和 TiDB Cloud Essential 的限制。

我们正在不断缩小 TiDB Cloud Starter/Essential 与 TiDB Cloud Dedicated 集群之间的功能差距。如果你需要这些尚未支持的功能或能力，请使用 [TiDB Cloud Dedicated 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 或 [联系我们](https://www.pingcap.com/contact-us/?from=en) 提交功能需求。

## 限制

### 审计日志

- [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md) 目前不可用。

### 连接

- 仅支持 [Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) 和 [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) 连接。你无法使用 [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) 连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
- Private Endpoint 不支持 [Firewall Rules](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

> **Note:**
>
> 由于 [AWS Global Accelerator 的限制](https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html#about-idle-timeout)，在 AWS 上 Public Endpoint 连接的空闲超时时间为 340 秒。出于同样的原因，你无法使用 TCP keep-alive 包保持连接持续打开。

### 加密

- 你在 TiDB Cloud Starter 或 TiDB Cloud Essential 集群中持久化的数据，使用由管理你集群的云服务商提供的加密工具进行加密。对于 TiDB Cloud Starter（消费额度 > 0）和 TiDB Cloud Essential 集群，在集群创建过程中可选启用第二层加密，为默认的静态加密提供额外的安全保障。
- 目前不支持使用 [客户自管加密密钥（CMEK）](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)。

### 维护窗口

- 目前不支持 [维护窗口](/tidb-cloud/configure-maintenance-window.md)。

### 监控与诊断

- 目前不支持 [第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。
- 目前不支持 [内置告警](/tidb-cloud/monitor-built-in-alerting.md)。
- 目前不支持 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)。

### 自助升级

- TiDB Cloud Starter 和 TiDB Cloud Essential 是 TiDB 的全托管部署。TiDB Cloud Starter 和 TiDB Cloud Essential 的主版本和小版本升级由 TiDB Cloud 统一管理，用户无法自行发起升级。

### 流式数据

- 目前 TiDB Cloud Starter 和 TiDB Cloud Essential 不支持 [Changefeed](/tidb-cloud/changefeed-overview.md)。
- 目前 TiDB Cloud Starter 和 TiDB Cloud Essential 不支持 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

### 生存时间（TTL）

- 在 TiDB Cloud Starter 和 TiDB Cloud Essential 中，表的 [`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) 属性固定为 `15m`，不可修改。这意味着 TiDB Cloud Starter 和 TiDB Cloud Essential 每 15 分钟会调度一次后台任务清理过期数据。

### 其他

- 事务持续时间不能超过 30 分钟。
- 有关 SQL 限制的更多细节，请参阅 [Limited SQL Features](/tidb-cloud/limited-sql-features.md)。

## 使用配额

在 TiDB Cloud 的每个组织中，默认最多可以创建 5 个 [免费 TiDB Cloud Starter 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。如需创建更多 TiDB Cloud Starter 集群，你需要添加信用卡并为使用量 [设置每月消费额度](/tidb-cloud/manage-serverless-spend-limit.md)。

对于你组织中的前 5 个 TiDB Cloud Starter 集群，TiDB Cloud 为每个集群提供如下免费使用配额：

- 行存储：5 GiB
- 列存储：5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

Request Unit（RU）是用于衡量查询或事务资源消耗的单位。它是一种指标，可以帮助你估算处理特定数据库请求所需的计算资源。Request Unit 也是 TiDB Cloud Starter 服务的计费单位。

一旦集群达到其使用配额，将立即拒绝所有新的连接尝试，直到你 [增加配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) 或新月开始时用量被重置。已在达到配额前建立的连接会保持活跃，但会受到限流影响。

如需了解不同资源（包括读、写、SQL CPU 和网络出口）的 RU 消耗、定价详情及限流信息，请参阅 [TiDB Cloud Starter Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

如果你希望创建配额更高的 TiDB Cloud Starter 集群，可以在集群创建页面设置每月消费额度。更多信息请参阅 [创建 TiDB Cloud Starter 集群](/tidb-cloud/create-tidb-cluster-serverless.md)。

集群创建后，你仍然可以在集群概览页面查看和编辑消费额度。更多信息请参阅 [管理 TiDB Cloud Starter 集群的消费额度](/tidb-cloud/manage-serverless-spend-limit.md)。