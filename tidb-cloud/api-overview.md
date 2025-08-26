---
title: TiDB Cloud API Overview
summary: 了解什么是 TiDB Cloud API、其功能，以及如何使用 API 管理你的 TiDB Cloud 集群。
---

# TiDB Cloud API 概览（Beta）

> **Note:**
>
> TiDB Cloud API 目前处于 beta 阶段。

TiDB Cloud API 是一个 [REST 接口](https://en.wikipedia.org/wiki/Representational_state_transfer)，为你提供以编程方式管理 TiDB Cloud 内部管理对象的能力。通过该 API，你可以自动且高效地管理诸如项目、集群、备份、恢复、导入、计费以及 [Data Service](/tidb-cloud/data-service-overview.md) 中的资源等。

该 API 具有以下特性：

- **JSON entities.** 所有实体均以 JSON 格式表示。
- **HTTPS-only.** 你只能通过 HTTPS 访问该 API，确保所有通过网络传输的数据都经过 TLS 加密。
- **Key-based access and digest authentication.** 在访问 TiDB Cloud API 之前，你必须生成一个 API key，参考 [API Key Management](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)。所有请求都通过 [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication) 进行身份验证，确保 API key 永远不会在网络上传输。

TiDB Cloud API 提供以下两个版本：

- v1beta1
    - 集群级资源：
        - [TiDB Cloud Starter 或 Essential 集群](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless)：管理 TiDB Cloud Starter 或 Essential 集群的集群、分支、数据导出任务和数据导入任务。
        - [TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated)：管理 TiDB Cloud Dedicated 集群的集群、区域、私有端点连接和数据导入任务。
    - 组织或项目级资源：
        - [Billing](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)：管理 TiDB Cloud 集群的计费。
        - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)：管理 TiDB Cloud 集群中 Data Service 的资源。
        - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)：管理 TiDB Cloud 集群的 API key。
        - [MSP (Deprecated)](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
- [v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta)
    - [Project](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project)
    - [Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Cluster)
    - [Backup](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Backup)
    - [Import (Deprecated)](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Import)
    - [Restore](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Restore)