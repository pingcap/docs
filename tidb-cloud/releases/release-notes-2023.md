---
title: 2023 年 TiDB Cloud 发布说明
summary: 了解 2023 年 TiDB Cloud 的发布说明。
---

# 2023 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2023 年的发布说明。

## 2023 年 12 月 5 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持恢复失败的 changefeed，节省了你重新创建 changefeed 的操作成本。

    详情参见 [Changefeed 状态](/tidb-cloud/changefeed-overview.md#changefeed-states)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 的连接体验。

    优化 **Connect** 对话框界面，为 TiDB Cloud Serverless 用户带来更流畅高效的连接体验。此外，TiDB Cloud Serverless 新增了更多 client type，并允许你选择所需分支进行连接。

    详情参见 [连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 2023 年 11 月 28 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持从备份中恢复 SQL 绑定。

    现在，TiDB Cloud Dedicated 在从备份恢复时默认恢复 user account 和 SQL 绑定。该增强适用于 v6.2.0 及 later version 的集群，简化了数据恢复流程。SQL 绑定的恢复确保了 query 相关配置和优化的顺利回归，为你提供更全面高效的恢复体验。

    详情参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 支持监控 SQL statement 的 RU 成本。

    TiDB Cloud Serverless 现在可以详细展示每条 SQL statement 的 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)。你可以查看每条 SQL statement 的 **Total RU** 和 **Mean RU** 成本。该功能有助于你识别和分析 RU 成本，为运维提供潜在的成本优化空间。

    查看 SQL statement RU 详情，请前往 [你的 TiDB Cloud Serverless 集群](https://tidbcloud.com/project/clusters) 的 **Diagnosis** 页面，并点击 **SQL Statement** 标签页。

## 2023 年 11 月 21 日

**通用变更**

- [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 支持 Google Cloud 上 TiDB 集群的高速物理模式。

    现在你可以在 AWS 和 Google Cloud 上的 TiDB 集群使用物理模式。物理模式的迁移速度可达 110 MiB/s，是 logic 模式的 2.4 倍。该性能提升适用于大数据集快速迁移到 TiDB Cloud 的 scenario。

    详情参见 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 11 月 14 日

**通用变更**

- 从 TiDB Cloud Dedicated 集群恢复数据时，默认行为已由不恢复 user account 改为恢复所有 user account。

    详情参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 引入 changefeed 的事件过滤器。

    该增强使你可以直接在 [TiDB Cloud 控制台](https://tidbcloud.com/)中便捷管理 changefeed 的事件过滤器，简化了排除特定事件的流程，并为下游数据同步提供更好的控制。

    详情参见 [Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

## 2023 年 11 月 7 日

**通用变更**

- 新增以下资源使用率报警。新报警默认关闭，你可按需开启。

    - TiDB 节点最大 memory 使用率 10 分钟超过 70%
    - TiKV 节点最大 memory 使用率 10 分钟超过 70%
    - TiDB 节点最大 CPU 使用率 10 分钟超过 80%
    - TiKV 节点最大 CPU 使用率 10 分钟超过 80%

  详情参见 [TiDB Cloud 内置报警](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)。

## 2023 年 10 月 31 日

**通用变更**

- 支持在 TiDB Cloud 控制台直接升级到 Enterprise 支持计划，无需联系销售。

    详情参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 10 月 25 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 Google Cloud 上的双区域备份（beta）。

    部署在 Google Cloud 上的 TiDB Cloud Dedicated 集群可无缝对接 Google Cloud Storage。与 Google Cloud Storage 的 [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr) 功能类似，TiDB Cloud Dedicated 的双区域所选 region 必须属于同一 multi-region。例如，东京和大阪同属 multi-region `ASIA`，因此可共同用于双区域存储。

    详情参见 [开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

- [将数据变更日志流式同步到 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) 功能现已正式 GA。

    经过 10 个月的 beta 试用后，TiDB Cloud 到 Apache Kafka 的数据变更日志流式同步功能正式可用。将 TiDB 数据流式同步到消息队列是数据集成常见需求。你可以通过 Kafka sink 集成其他数据处理系统（如 Snowflake）或支持业务消费。

    详情参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。

## 2023 年 10 月 11 日

**通用变更**

- 支持 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群在 AWS 上的 [双区域备份（beta）](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

    你现在可以在云服务商的不同地理 region 之间复制备份。该功能为数据提供了额外的保护层和容灾能力。

    详情参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 数据迁移现已支持物理模式和逻辑模式迁移现有数据。

    在物理模式下，迁移速度可达 110 MiB/s。相比逻辑模式的 45 MiB/s，迁移性能大幅提升。

    详情参见 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 10 月 10 日

**通用变更**

- 支持在 [Vercel Preview Deployments](https://vercel.com/docs/deployments/preview-deployments) 中使用 TiDB Cloud Serverless 分支，并集成 TiDB Cloud Vercel。

    详情参见 [通过分支连接 TiDB Cloud Serverless](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-branching)。

## 2023 年 9 月 28 日

**API 变更**

- 新增 TiDB Cloud Billing API 端点，用于获取指定组织某月账单。

    该 Billing API 端点已在 TiDB Cloud API v1beta1（最新 API 版本）中发布。详情参见 [API 文档 (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)。

## 2023 年 9 月 19 日

**通用变更**

- 从 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中移除 2 vCPU 的 TiDB 和 TiKV 节点。

    2 vCPU 选项已不再出现在 **Create Cluster** 或 **Modify Cluster** 页面。

- 发布 [TiDB Cloud serverless driver (beta)](/develop/serverless-driver.md) for JavaScript。

    TiDB Cloud serverless driver for JavaScript 允许你通过 HTTPS 连接 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群。该 driver 尤其适用于 TCP 连接受限的边缘环境，如 [Vercel Edge Function](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。

    详情参见 [TiDB Cloud serverless driver (beta)](/develop/serverless-driver.md)。

**控制台变更**

- 对于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群，你可以在 **Usage This Month** 面板或设置消费上限时获取费用预估。

## 2023 年 9 月 5 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持为每个 API key 自定义限流，以满足不同 scenario 下的限流需求。

    你可以在 [创建](/tidb-cloud/data-service-api-key.md#create-an-api-key) 或 [编辑](/tidb-cloud/data-service-api-key.md#edit-an-api-key) API key 时调整限流。

    详情参见 [限流](/tidb-cloud/data-service-api-key.md#rate-limiting)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持新的 AWS region：圣保罗 (sa-east-1)。

- 每个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 IP 访问列表支持最多添加 100 个 IP 地址。

    详情参见 [配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

**控制台变更**

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群引入 **Events** 页面，记录集群的主要变更。

    你可以在该页面查看最近 7 天的事件历史，并追踪触发时间、操作用户等重要信息。

    详情参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

**API 变更**

- 发布多组 TiDB Cloud API 端点，用于管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 或 [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)：

    - 为集群创建私有 endpoint service
    - 获取集群的私有 endpoint service 信息
    - 为集群创建私有 endpoint
    - 列出集群的所有私有 endpoint
    - 列出项目下所有私有 endpoint
    - 删除集群的私有 endpoint

  详情参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)。

## 2023 年 8 月 23 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持 Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)。

    你现在可以创建私有 endpoint，并与部署在 Google Cloud 上的 TiDB Cloud Dedicated 集群建立安全连接。

    主要优势：

    - 操作直观：只需几步即可创建私有 endpoint。
    - 安全增强：建立安全连接，保护你的数据。
    - 性能提升：提供低延时、高带宽的连接。

  详情参见 [通过 Google Cloud 私有 endpoint 连接](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

- 支持通过 changefeed 将数据从 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群流式同步到 [Google Cloud Storage (GCS)](https://cloud.google.com/storage)。

    你可以使用自己的 GCS bucket 并精确配置权限，将 TiDB Cloud 数据流式同步到 GCS。数据复制到 GCS 后，你可以按需分析数据变更。

    详情参见 [同步到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2023 年 8 月 15 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持 `GET` 请求的分页，提升开发体验。

    对于 `GET` 请求，你可以在 **Advance Properties** 启用 **Pagination**，并在调用 endpoint 时通过 query parameter 指定 `page` 和 `page_size`。例如，获取第 2 页、每页 10 条数据，可用如下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    注意：该功能仅适用于最后一个 query 为 `SELECT` statement 的 `GET` 请求。

    详情参见 [调用 endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持为 `GET` 请求的 endpoint 响应设置指定 TTL 的 cache。

    该功能可降低数据库负载，优化 endpoint 延时。

    对于使用 `GET` 方法的 endpoint，你可以在 **Advance Properties** 启用 **Cache Response** 并配置 cache 的 TTL。

    详情参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

- 对 2023 年 8 月 15 日后在 AWS 上新建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，禁用负载均衡改进，包括：

    - 禁用 TiDB 节点扩容时自动迁移现有连接到新 TiDB 节点。
    - 禁用 TiDB 节点缩容时自动迁移现有连接到可用 TiDB 节点。

  此变更避免了 hybrid deployment 的资源争用，不影响已启用该改进的现有集群。如需为新集群启用负载均衡改进，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 8 月 8 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 现已支持 Basic Authentication。

    你可以在请求中将 public key 作为用户名、private key 作为密码，使用 ['Basic' HTTP Authentication](https://datatracker.ietf.org/doc/html/rfc7617)。与 Digest Authentication 相比，Basic Authentication 更简单，便于调用 Data Service endpoint。

    详情参见 [调用 endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 8 月 1 日

**通用变更**

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 支持 Data App 的 OpenAPI 规范。

    TiDB Cloud Data Service 为每个 Data App 自动生成 OpenAPI 文档。你可以在文档中查看 endpoint、parameter、响应，并直接试用 endpoint。

    你还可以下载 Data App 及其已部署 endpoint 的 OpenAPI Specification (OAS)，格式为 YAML 或 JSON。OAS 提供标准化 API 文档、简化集成和便捷代码生成，加速开发、提升协作。

    详情参见 [使用 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification) 及 [结合 Next.js 使用 OpenAPI 规范](/tidb-cloud/data-service-oas-with-nextjs.md)。

- 支持在 [Postman](https://www.postman.com/) 中运行 Data App。

    Postman 集成让你可将 Data App 的 endpoint 作为集合导入到工作区，便于协作和无缝 API 测试，支持 Postman web 和桌面应用。

    详情参见 [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 **Pausing** 状态，实现低成本暂停，暂停期间不计费。

    当你点击 **Pause**，集群会先进入 **Pausing** 状态，暂停完成后状态变为 **Paused**。

    只有状态变为 **Paused** 后，集群才能恢复，解决了因频繁点击 **Pause** 和 **Resume** 导致的异常恢复问题。

    详情参见 [暂停或恢复 TiDB Cloud Dedicated 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 2023 年 7 月 26 日

**通用变更**

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 推出自动生成 endpoint 的强大功能。

    开发者现在只需极少点击和配置即可轻松创建 HTTP endpoint。无需重复样板代码，简化并加速 endpoint 创建，减少潜在错误。

    详情参见 [自动生成 endpoint](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)。

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 的 endpoint 支持 `PUT` 和 `DELETE` 请求方法。

    - 使用 `PUT` 方法更新或修改数据，类似 `UPDATE` statement。
    - 使用 `DELETE` 方法删除数据，类似 `DELETE` statement。

  详情参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 的 endpoint 支持 `POST`、`PUT`、`DELETE` 方法的 **Batch Operation**。

    启用 **Batch Operation** 后，你可以在单次请求中对多行数据进行操作。例如，使用单个 `POST` 请求插入多行数据。

    详情参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

## 2023 年 7 月 25 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.3](https://docs.pingcap.com/tidb/stable/release-6.5.3) 升级为 [v7.1.1](https://docs.pingcap.com/tidb/stable/release-7.1.1)。

**控制台变更**

- 通过优化支持入口，简化 TiDB Cloud 用户访问 PingCAP 支持的流程。改进包括：

    - 在左下角 <MDSvgIcon name="icon-top-organization" /> 处新增 **Support** 入口。
    - 重构 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角 **?** 图标菜单，使其更直观。

  详情参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 7 月 18 日

**通用变更**

- 优化组织级和项目级的基于角色的访问控制，让你以最小权限为用户分配角色，提升安全性、合规性和生产力。

    - 组织角色包括：`Organization Owner`、`Organization Billing Admin`、`Organization Console Audit Admin`、`Organization Member`。
    - 项目角色包括：`Project Owner`、`Project Data Access Read-Write`、`Project Data Access Read-Only`。
    - 管理项目中的集群（如创建、修改、删除集群）需具备 `Organization Owner` 或 `Project Owner` 角色。

  各角色权限详情参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS 上）支持客户自管加密密钥（CMEK）（beta）。

    你可以基于 AWS KMS 创建 CMEK，对存储在 EBS 和 S3 的数据进行加密，操作均可在 TiDB Cloud 控制台完成，确保数据由客户自管密钥加密，提升安全性。

    注意：该功能有一定限制，仅支持申请开通。如需申请，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

- 优化 TiDB Cloud 的导入功能，提升数据导入体验。主要改进如下：

    - TiDB Cloud Serverless 统一导入入口：整合本地文件和 Amazon S3 文件导入入口，便于切换。
    - 配置简化：从 Amazon S3 导入数据仅需一步，节省时间和精力。
    - CSV 配置增强：CSV 配置项移至文件类型选项下，便于快速配置参数。
    - 目标表选择优化：支持通过勾选选择目标表，无需复杂表达式，简化目标表选择。
    - 展示信息优化：修复导入过程中的信息不准确问题，并移除 Preview 功能，避免数据展示不全和误导。
    - 源文件映射增强：支持自定义源文件与目标表的映射关系，解决需修改源文件名以满足命名要求的难题。

## 2023 年 7 月 11 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 现已正式 GA。

- 推出 TiDB Bot（beta），基于 OpenAI 的聊天机器人，支持多语言、7x24 实时响应、集成文档访问。

    TiDB Bot 为你带来以下优势：

    - 持续支持：随时为你解答问题，提升支持体验。
    - 效率提升：自动化响应降低延时，提升整体运维效率。
    - 无缝文档访问：可直接访问 TiDB Cloud 文档，便于信息检索和快速解决问题。

  使用方法：点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角 **?**，选择 **Ask TiDB Bot** 开始对话。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群支持 [分支功能（beta）](/tidb-cloud/branch-overview.md)。

    TiDB Cloud 支持为 TiDB Cloud Serverless 集群创建分支。分支是原集群数据的分叉副本，提供隔离环境，便于你自由实验而不影响原集群。

    2023 年 7 月 5 日后创建的 TiDB Cloud Serverless 集群可通过 [TiDB Cloud 控制台](/tidb-cloud/branch-manage.md) 或 [TiDB Cloud CLI](/tidb-cloud/ticloud-branch-create.md) 创建分支。

    如果你使用 GitHub 进行应用开发，可将 TiDB Cloud Serverless 分支集成到 GitHub CI/CD 流水线，实现 PR 自动测试而不影响生产库。详情参见 [集成 TiDB Cloud Serverless 分支（Beta）与 GitHub](/tidb-cloud/branch-github-integration.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持每周备份。详情参见 [开启自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 2023 年 7 月 4 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群支持时间点恢复（PITR）（beta）。

    你现在可以将 TiDB Cloud Serverless 集群恢复到过去 90 天内的任意时间点。该功能增强了 TiDB Cloud Serverless 集群的数据恢复能力。例如，当发生数据写入错误时，你可以通过 PITR 恢复到更早状态。

    详情参见 [备份与恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#restore)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群概览页的 **Usage This Month** 面板，提供更清晰的资源使用视图。

- 优化整体导航体验，具体变更如下：

    - 将右上角 <MDSvgIcon name="icon-top-organization" /> **Organization** 和 <MDSvgIcon name="icon-top-account-settings" /> **Account** 合并到左侧导航栏。
    - 将左侧导航栏 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin** 合并到 <MDSvgIcon name="icon-left-projects" /> **Project**，并移除左上角 ☰ 悬浮菜单。现在你可以点击 <MDSvgIcon name="icon-left-projects" /> 切换项目及修改项目设置。
    - 将所有 TiDB Cloud 的帮助与支持信息整合到右下角 **?** 图标菜单，包括文档、交互式教程、自助培训和支持入口。

- TiDB Cloud 控制台现已支持暗黑模式，带来更舒适、护眼的体验。你可以在左侧导航栏底部切换明暗模式。

## 2023 年 6 月 27 日

**通用变更**

- 新建 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群不再预置示例数据集。

## 2023 年 6 月 20 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.2](https://docs.pingcap.com/tidb/stable/release-6.5.2) 升级为 [v6.5.3](https://docs.pingcap.com/tidb/stable/release-6.5.3)。

## 2023 年 6 月 13 日

**通用变更**

- 支持通过 changefeed 将数据流式同步到 Amazon S3。

    该功能实现 TiDB Cloud 与 Amazon S3 的无缝集成。可将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的实时数据捕获并同步到 Amazon S3，确保下游应用和分析系统获取最新数据。

    详情参见 [同步到云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 16 vCPU TiKV 节点最大存储由 4 TiB 提升至 6 TiB。

    该增强提升了 TiDB Cloud Dedicated 集群的数据存储能力，提高了 workload 扩展效率，满足不断增长的数据需求。

    详情参见 [集群规格选择](/tidb-cloud/size-your-cluster.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [监控指标保留时间](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 从 3 天延长至 7 天。

    保留时间延长后，你可访问更多历史数据，有助于识别集群趋势和模式，提升决策和故障排查效率。

**控制台变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 **Key Visualizer** 页面，获取所需信息，提升了 SQL 诊断的用户体验。

## 2023 年 6 月 6 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 Index Insight（beta），为慢 query 提供索引推荐，优化 query 性能。

    通过 Index Insight，你可以提升数据库操作的整体性能和效率，具体包括：

    - 查询性能提升：Index Insight 识别慢 query 并建议合适索引，加速 query 执行，降低响应时间，提升用户体验。
    - 成本效益：通过 Index Insight 优化 query 性能，减少额外计算资源需求，更高效利用现有架构，降低运维成本。
    - 优化流程简化：Index Insight 简化索引优化的识别与实施，无需手动分析和猜测，节省时间和精力。
    - 应用效率提升：通过 Index Insight 优化数据库性能，TiDB Cloud 上的应用可承载更大 workload 并支持更多并发用户，提升应用扩展效率。

  使用方法：进入 TiDB Cloud Dedicated 集群的 **Diagnosis** 页面，点击 **Index Insight BETA** 标签页。

- 推出 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes)，无需注册或安装即可体验 TiDB 全功能的交互式平台。

    TiDB Playground 提供一站式体验，便于探索 TiDB 的扩展性、MySQL 兼容性、实时分析等能力。

    你可以在受控环境下实时试用 TiDB 功能，无需复杂配置，便于理解 TiDB 特性。

    立即体验，请访问 [**TiDB Playground**](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes) 页面，选择你想探索的功能，开始体验。

## 2023 年 6 月 5 日

**通用变更**

- 支持将 [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) 连接到 GitHub。

    [连接 Data App 到 GitHub](/tidb-cloud/data-service-manage-github-connection.md) 后，你可以将 Data App 的所有配置作为 [代码文件](/tidb-cloud/data-service-app-config-files.md) 管理，实现 TiDB Cloud Data Service 与系统架构和 DevOps 流程的无缝集成。

    该功能可帮助你轻松完成以下任务，提升 Data App 开发的 CI/CD 体验：

    - 通过 GitHub 自动部署 Data App 变更。
    - 在 GitHub 上配置 Data App 变更的 CI/CD 流水线并进行版本控制。
    - 断开与已连接 GitHub 仓库的关联。
    - 部署前审查 endpoint 变更。
    - 查看部署历史并在失败时采取措施。
    - 重新部署 commit，实现回滚。

  详情参见 [通过 GitHub 自动部署 Data App](/tidb-cloud/data-service-manage-github-connection.md)。

## 2023 年 6 月 2 日

**通用变更**

- 为简化和明晰产品命名，我们对产品名称进行了更新：

    - “TiDB Cloud Serverless Tier” 现称为 “TiDB Cloud Serverless”。
    - “TiDB Cloud Dedicated Tier” 现称为 “TiDB Cloud Dedicated”。
    - “TiDB On-Premises” 现称为 “TiDB Self-Managed”。

    名称焕新，体验如一。你的体验始终是我们的首要任务。

## 2023 年 5 月 30 日

**通用变更**

- 增强 TiDB Cloud 数据迁移功能对增量数据迁移的支持。

    你现在可以指定 binlog position 或全局 transaction 标识符（GTID），仅同步指定位置之后产生的增量数据到 TiDB Cloud。该增强为你选择和同步所需数据提供了更大灵活性，满足特定需求。

    详情参见 [仅迁移 MySQL 兼容数据库的增量数据到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

- [**Events**](/tidb-cloud/tidb-cloud-events.md) 页面新增事件类型（`ImportData`）。

- 从 TiDB Cloud 控制台移除 **Playground**。

    敬请期待全新独立 Playground，体验更优。

## 2023 年 5 月 23 日

**通用变更**

- 上传 CSV 文件到 TiDB 时，除英文和数字外，还可用中文、日文等字符定义列名。但特殊字符仅支持下划线（`_`）。

    详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2023 年 5 月 16 日

**控制台变更**

- 为 Dedicated 和 Serverless 两种 tier 引入按功能分类的左侧导航入口。

    新导航让你更便捷、直观地发现功能入口。访问集群概览页即可体验新导航。

- 为 Dedicated Tier 集群的 **Diagnosis** 页的以下两个标签页发布全新原生 Web 架构：

    - [Slow Query](/tidb-cloud/tune-performance.md#slow-query)
    - [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis)

    新架构让你更便捷地浏览这两个标签页，获取所需信息，提升 SQL 诊断的用户体验。

## 2023 年 5 月 9 日

**通用变更**

- 支持为 2023 年 4 月 26 日后创建的 GCP 集群变更节点规格。

    你可以根据需求升级为高性能节点，或降级为低性能节点以节省成本。该功能让你灵活调整集群容量，优化成本。

    详细步骤参见 [变更节点规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)。

- 支持导入压缩文件。你可以导入 `.gzip`、`.gz`、`.zstd`、`.zst`、`.snappy` 格式的 CSV 和 SQL 文件。该功能提升了数据导入效率，降低数据传输成本。

    详情参见 [从云存储导入 CSV 文件到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md) 及 [导入示例数据](/tidb-cloud/import-sample-data.md)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群支持基于 AWS PrivateLink 的 endpoint 连接，作为新的网络访问管理选项。

    私有 endpoint 连接不会将你的数据暴露在公网，并支持 CIDR 重叠，便于网络管理。

    详情参见 [设置私有 endpoint 连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

- [**Event**](/tidb-cloud/tidb-cloud-events.md) 页面新增事件类型，记录 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的备份、恢复、changefeed 操作。

    所有可记录事件参见 [已记录事件](/tidb-cloud/tidb-cloud-events.md#logged-events)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [**SQL Diagnosis**](/tidb-cloud/tune-performance.md) 页面新增 **SQL Statement** 标签页。

    **SQL Statement** 标签页提供：

    - TiDB 数据库所有 SQL statement 的全面概览，便于识别和诊断慢 query。
    - 每条 SQL statement 的详细信息，如 query 时间、执行计划、数据库 server 响应，助你优化数据库性能。
    - 友好的界面，便于对大量数据进行排序、筛选和搜索，聚焦关键 query。

  详情参见 [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis)。

## 2023 年 5 月 6 日

**通用变更**

- 支持直接访问 TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群所在 region 的 [Data Service endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint)。

    新建 Serverless Tier 集群的 endpoint URL 现包含集群 region 信息。通过请求区域域名 `<region>.data.tidbcloud.com`，可直接访问集群所在 region 的 endpoint。

    你也可以请求全局域名 `data.tidbcloud.com`，此时 TiDB Cloud 会内部重定向到目标 region，但可能增加延时。如采用此方式，调用 endpoint 时请确保 curl 命令加上 `--location-trusted` 选项。

    详情参见 [调用 endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 4 月 25 日

**通用变更**

- 你的组织下前 5 个 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群，每个都可享受如下免费额度：

    - 行存储：5 GiB
    - [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)：每月 5000 万 RUs

  截至 2023 年 5 月 31 日，Serverless Tier 集群仍免费（100% 折扣）。之后超出免费额度部分将计费。

    你可以在集群 **Overview** 页的 **Usage This Month** 区域 [监控集群用量或提升额度](/tidb-cloud/manage-serverless-spend-limit.md)。集群用量达到免费额度后，读写操作将被限流，直至提升额度或新月重置。

    各资源（包括读、写、SQL CPU、网络出口）的 RU 消耗、定价及限流信息，参见 [TiDB Cloud Serverless Tier 价格详情](https://www.pingcap.com/tidb-cloud-starter-pricing-details)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群支持备份与恢复。

     详情参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore-serverless.md)。

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.1](https://docs.pingcap.com/tidb/stable/release-6.5.1) 升级为 [v6.5.2](https://docs.pingcap.com/tidb/stable/release-6.5.2)。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群提供维护窗口功能，便于你轻松安排和管理计划性维护。

    维护窗口是指定时间段，自动执行操作系统更新、安全补丁、基础设施升级等计划性维护，保障 TiDB Cloud 服务的可靠性、安全性和性能。

    维护窗口期间，可能出现临时连接中断或 QPS 波动，但集群保持可用，SQL 操作、现有数据导入、备份、恢复、迁移、同步任务均可正常运行。维护期间允许和不允许的操作详见 [维护窗口期间的操作列表](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)。

    我们将尽量减少维护频率。如有维护计划，默认开始时间为目标周三 03:00（以 TiDB Cloud 组织时区为准）。请关注维护计划，合理安排操作，避免影响。

    - TiDB Cloud 会为每个维护窗口发送三封邮件通知：维护前、开始时、结束后。
    - 你可在 **Maintenance** 页面修改维护开始时间或延后维护，降低影响。

  详情参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 优化 AWS 上新建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB 负载均衡，缩容/扩容 TiDB 节点时减少连接中断。

    - 扩容 TiDB 节点时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容 TiDB 节点时，支持自动迁移现有连接到可用 TiDB 节点。

  目前该功能适用于所有 AWS 上的 Dedicated Tier 集群。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，获取所需信息，提升监控体验。

## 2023 年 4 月 18 日

**通用变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持扩容/缩容 [数据迁移作业规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

    你可以通过扩容提升迁移性能，或通过缩容降低成本。

    详情参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)。

**控制台变更**

- 重构 [集群创建](https://tidbcloud.com/clusters/create-cluster) UI，提升用户体验，让你只需几步即可创建和配置集群。

    新设计注重简洁、减少视觉干扰、提供清晰指引。点击 **Create** 后将直接跳转到集群概览页，无需等待集群创建完成。

    详情参见 [创建集群](/tidb-cloud/create-tidb-cluster.md)。

- **Billing** 页新增 **Discounts** 标签，展示组织 owner 和 billing admin 的折扣信息。

    详情参见 [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts)。

## 2023 年 4 月 11 日

**通用变更**

- 优化 AWS 上 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB 负载均衡，缩容/扩容 TiDB 节点时减少连接中断。

    - 扩容 TiDB 节点时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容 TiDB 节点时，支持自动迁移现有连接到可用 TiDB 节点。

  目前该功能仅适用于 AWS `Oregon (us-west-2)` region 的 Dedicated Tier 集群。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持 [New Relic](https://newrelic.com/) 集成。

    通过 New Relic 集成，你可以将 TiDB 集群的 metric 数据发送到 [New Relic](https://newrelic.com/)，实现应用和数据库的统一监控与分析，便于快速定位和排查问题，缩短故障处理时间。

    集成步骤及可用指标参见 [集成 TiDB Cloud 与 New Relic](/tidb-cloud/monitor-new-relic-integration.md)。

- 为 Dedicated Tier 集群的 Prometheus 集成新增以下 [changefeed](/tidb-cloud/changefeed-overview.md) 指标：

    - `tidbcloud_changefeed_latency`
    - `tidbcloud_changefeed_replica_rows`

    已集成 Prometheus 的用户可实时监控 changefeed 的性能和健康状况，并可基于这些指标创建报警。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面现采用 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server)。

    节点级资源指标可更准确反映资源消耗，帮助你了解实际服务使用情况。

    访问方法：进入集群的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，在 **Metrics** 标签下查看 **Server** 类别。

- 优化 [Billing](/tidb-cloud/tidb-cloud-billing.md#billing-details) 页面，重组 **Summary by Project** 和 **Summary by Service** 的账单项，使账单信息更清晰。

## 2023 年 4 月 4 日

**通用变更**

- 从 [TiDB Cloud 内置报警](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) 中移除以下两项报警，避免误报。因为单个节点临时 offline 或 OOM 不会显著影响集群整体健康。

    - 集群中至少一个 TiDB 节点 OOM。
    - 一个或多个集群节点 offline。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 [Alerts](/tidb-cloud/monitor-built-in-alerting.md) 页面，展示每个 Dedicated Tier 集群的活跃和已关闭报警。

    **Alerts** 页面提供：

    - 直观友好的界面。即使未订阅报警邮件，也可在此页面查看集群报警。
    - 高级筛选，按严重性、状态等属性快速查找和排序报警，并可查看最近 7 天历史，便于追踪报警历史。
    - **Edit Rule** 功能。你可自定义报警规则，满足集群特定需求。

  详情参见 [TiDB Cloud 内置报警](/tidb-cloud/monitor-built-in-alerting.md)。

- 将 TiDB Cloud 的帮助相关信息和操作整合到一个入口。

    现在，你可点击 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角 **?** 获取所有 [TiDB Cloud 帮助信息](/tidb-cloud/tidb-cloud-support.md) 并联系支持。

- 推出 [Getting Started](https://tidbcloud.com/getting-started) 页面，帮助你了解 TiDB Cloud。

    **Getting Started** 页面提供交互式教程、基础指南和实用链接。通过交互式教程，你可轻松体验 TiDB Cloud 功能和 HTAP 能力，内置行业数据集（Steam Game Dataset 和 S&P 500 Dataset）。

    访问方法：点击 [TiDB Cloud 控制台](https://tidbcloud.com/) 左侧导航栏 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Getting Started**，点击 **Query Sample Dataset** 进入交互式教程，或点击其他链接探索 TiDB Cloud。你也可以点击右下角 **?**，选择 **Interactive Tutorials**。

## 2023 年 3 月 29 日

**通用变更**

- [Data Service (beta)](/tidb-cloud/data-service-overview.md) 支持 Data App 的更细粒度访问控制。

    在 Data App 详情页，你可以关联集群并为每个 API key 指定角色。角色控制 API key 是否可对关联集群读写数据，可设为 `ReadOnly` 或 `ReadAndWrite`。该功能实现 Data App 的集群级和权限级访问控制，灵活满足业务需求。

    详情参见 [管理关联集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) 和 [管理 API key](/tidb-cloud/data-service-api-key.md)。

## 2023 年 3 月 28 日

**通用变更**

- [changefeed](/tidb-cloud/changefeed-overview.md) 新增 2 RCUs、4 RCUs、8 RCUs 规格，支持在 [创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时选择所需规格。

    使用新规格，数据同步成本最高可降低 87.5%（相较于原需 16 RCUs 的场景）。

- 支持为 2023 年 3 月 28 日后创建的 [changefeed](/tidb-cloud/changefeed-overview.md) 扩容/缩容规格。

    你可以通过选择更高规格提升同步性能，或选择更低规格降低同步成本。

    详情参见 [扩容/缩容 changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)。

- 支持将 AWS 上 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的增量数据实时同步到同项目同 region 的 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群。

    详情参见 [同步到 TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据迁移功能新增两个 GCP region：`Singapore (asia-southeast1)` 和 `Oregon (us-west1)`。

    新 region 为你提供更多数据迁移到 TiDB Cloud 的选择。如果上游数据位于或接近这些 region，可获得更快、更可靠的迁移体验。

    详情参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 页面，提升 SQL 诊断体验。

## 2023 年 3 月 21 日

**通用变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群引入 [Data Service (beta)](https://tidbcloud.com/project/data-service)，支持通过自定义 API endpoint 以 HTTPS 方式访问数据。

    Data Service 让 TiDB Cloud 可无缝集成任何兼容 HTTPS 的应用或服务。常见 scenario 包括：

    - 直接从移动或 Web 应用访问 TiDB 集群数据库。
    - 使用 serverless edge function 调用 endpoint，避免数据库连接池带来的扩展性问题。
    - 通过 Data Service 作为数据源集成数据可视化项目。
    - 从不支持 MySQL interface 的环境连接数据库。

    此外，TiDB Cloud 提供 [Chat2Query API](/tidb-cloud/use-chat2query-api.md)，可通过 RESTful 接口结合 AI 生成并执行 SQL statement。

    访问方法：左侧导航栏进入 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。更多信息参见：

    - [Data Service 概览](/tidb-cloud/data-service-overview.md)
    - [Data Service 入门](/tidb-cloud/data-service-get-started.md)
    - [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)

- 支持对 2022 年 12 月 31 日后在 AWS 上创建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群缩容 TiDB、TiKV、TiFlash 节点规格。

    你可以通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 缩容节点规格。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据迁移功能新增 GCP region：`Tokyo (asia-northeast1)`。

    该功能可帮助你将 Google Cloud Platform (GCP) 上的 MySQL 兼容数据库数据高效迁移到 TiDB 集群。

    详情参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 **Events** 页面，记录集群主要变更。

    你可以查看最近 7 天的事件历史，追踪触发时间、操作用户等重要信息。例如，可查看集群暂停、规格变更等事件。

    详情参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 **Monitoring** 页面新增 **Database Status** 标签，展示以下数据库级指标：

    - QPS Per DB
    - Average Query Duration Per DB
    - Failed Queries Per DB

  通过这些指标，你可以监控各数据库的性能，做出数据驱动决策，提升应用性能。

  详情参见 [Serverless Tier 集群监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 3 月 14 日

**通用变更**

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0) 升级为 [v6.5.1](https://docs.pingcap.com/tidb/stable/release-6.5.1)。

- 上传带表头的本地 CSV 文件到 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群时，支持修改 TiDB Cloud 自动创建目标表的列名。

    如果表头中的列名不符合 TiDB Cloud 列名规范，系统会在对应列名旁显示警告图标。你可将鼠标悬停在图标上，根据提示修改或输入新列名。

    列名规范参见 [导入本地文件](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)。

## 2023 年 3 月 7 日

**通用变更**

- 所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本由 [v6.4.0](https://docs.pingcap.com/tidb/stable/release-6.4.0) 升级为 [v6.6.0](https://docs.pingcap.com/tidb/stable/release-6.6.0)。

## 2023 年 2 月 28 日

**通用变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群新增 [SQL Diagnosis](/tidb-cloud/tune-performance.md) 功能。

    通过 SQL Diagnosis，你可以深入了解 SQL 相关的运行时状态，提升 SQL 性能调优效率。目前 Serverless Tier 的 SQL Diagnosis 仅提供慢 query 数据。

    使用方法：在 Serverless Tier 集群页面左侧导航栏点击 **SQL Diagnosis**。

**控制台变更**

- 优化左侧导航。

    你可以更高效地导航页面，例如：

    - 鼠标悬停左上角可快速切换集群或项目。
    - 可在 **Clusters** 和 **Admin** 页面间切换。

**API 变更**

- 发布多组 TiDB Cloud API 端点用于数据导入：

    - 列出所有导入任务
    - 获取导入任务
    - 创建导入任务
    - 更新导入任务
    - 上传本地文件到导入任务
    - 启动导入任务前预览数据
    - 获取导入任务的角色信息

  详情参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)。

## 2023 年 2 月 22 日

**通用变更**

- 支持使用 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md) 跟踪组织成员在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的各类操作。

    控制台审计日志仅对 `Owner` 或 `Audit Admin` 角色可见，默认关闭。开启方法：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 右上角点击 <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**。

    通过分析审计日志，你可以识别组织内的可疑操作，提升资源和数据安全性。

    详情参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 `ticloud cluster connect-info` 命令。

    `ticloud cluster connect-info` 可获取集群连接字符串。使用该命令需将 [ticloud 升级](/tidb-cloud/ticloud-upgrade.md) 至 v0.3.2 或更高版本。

## 2023 年 2 月 21 日

**通用变更**

- 数据导入到 TiDB Cloud 时，支持使用 IAM 用户的 AWS access key 访问 Amazon S3 bucket。

    该方式比使用 Role ARN 更简单。详情参见 [配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

- [监控指标保留时间](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 从 2 天延长：

    - Dedicated Tier 集群可查看过去 7 天的指标数据。
    - Serverless Tier 集群可查看过去 3 天的指标数据。

  保留时间延长后，你可访问更多历史数据，有助于识别集群趋势和模式，提升决策和故障排查效率。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 Monitoring 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 Monitoring 页面，提升监控体验。

## 2023 年 2 月 17 日

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 [`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md) 命令。

    `ticloud connect` 允许你无需安装 SQL client，即可从本地连接 TiDB Cloud 集群，并在 CLI 中执行 SQL statement。

## 2023 年 2 月 14 日

**通用变更**

- 支持缩减 TiKV、TiFlash 节点数量，实现 TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的缩容。

    你可以通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-node-number) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 缩减节点数量。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群新增 **Monitoring** 页面。

    **Monitoring** 页面提供多项指标和数据，如每秒 SQL statement 数、平均 query 时长、失败 query 数，帮助你全面了解 Serverless Tier 集群 SQL statement 的整体性能。

    详情参见 [TiDB Cloud 内置监控](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 2 月 2 日

**CLI 变更**

- 推出 TiDB Cloud CLI 客户端 [`ticloud`](/tidb-cloud/cli-reference.md)。

    使用 `ticloud`，你可以通过终端或自动化流程轻松管理 TiDB Cloud 资源。针对 GitHub Actions，我们提供了 [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli)，便于快速设置 `ticloud`。

    详情参见 [TiDB Cloud CLI 快速入门](/tidb-cloud/get-started-with-cli.md) 及 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2023 年 1 月 18 日

**通用变更**

* 支持使用 Microsoft 账号 [注册](https://tidbcloud.com/free-trial) TiDB Cloud。

## 2023 年 1 月 17 日

**通用变更**

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) 升级为 [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)。

- 新注册用户将自动创建一个免费的 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群，便于你快速开启 TiDB Cloud 数据探索之旅。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持新的 AWS region：`Seoul (ap-northeast-2)`。

    该 region 支持以下功能：

    - [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [通过 changefeed 将 TiDB Cloud 数据流式同步到其他数据服务](/tidb-cloud/changefeed-overview.md)
    - [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日

**通用变更**

- 优化本地 CSV 文件导入 TiDB 的功能，提升 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的用户体验。

    - 你现在可以直接拖拽 CSV 文件到 **Import** 页的上传区域。
    - 创建导入任务时，如目标数据库或表不存在，可输入名称让 TiDB Cloud 自动创建。对于新建目标表，你可指定主键或选择多个字段组成复合主键。
    - 导入完成后，可点击 **Explore your data by Chat2Query** 或任务列表中的目标表名，使用 [AI 驱动的 Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) 探索数据。

  详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

**控制台变更**

- 每个集群新增 **Get Support** 选项，简化针对特定集群的支持请求流程。

    你可以通过以下任一方式请求集群支持：

    - 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击集群行的 **...**，选择 **Get Support**。
    - 在集群概览页右上角点击 **...**，选择 **Get Support**。

## 2023 年 1 月 5 日

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群将 SQL Editor (beta) 重命名为 Chat2Query (beta)，并支持通过 AI 生成 SQL query。

  在 Chat2Query 中，你可以让 AI 自动生成 SQL query，也可手动编写 SQL query，并直接对数据库执行，无需终端。

  访问方法：进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击集群名，再点击左侧导航栏的 **Chat2Query**。

## 2023 年 1 月 4 日

**通用变更**

- 支持为 2022 年 12 月 31 日后在 AWS 上创建的 TiDB Cloud Dedicated 集群扩容 TiDB、TiKV、TiFlash 节点（提升 **Node Size(vCPU + RAM)**）。

    你可以通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 扩容节点规格。

- [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的指标保留时间延长至两天。

    你现在可以访问最近两天的指标数据，更灵活地洞察集群性能和趋势。

    该提升无需额外费用，可在集群 [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的 **Diagnosis** 标签下访问，有助于更高效地定位和排查性能问题，监控集群健康。

- 支持为 Prometheus 集成自定义 Grafana dashboard JSON。

    已 [集成 Prometheus 的 TiDB Cloud](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) 用户可导入预置 Grafana dashboard 并自定义，便于快速监控 TiDB Cloud 集群，及时发现性能问题。

    详情参见 [使用 Grafana GUI dashboard 可视化指标](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)。

- 所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本由 [v6.3.0](https://docs.pingcap.com/tidb/stable/release-6.3.0) 升级为 [v6.4.0](https://docs.pingcap.com/tidb/stable/release-6.4.0)。Serverless Tier 集群升级到 v6.4.0 后的冷启动问题已修复。

**控制台变更**

- 简化 [**Clusters**](https://tidbcloud.com/project/clusters) 页面和集群概览页的展示。

    - 你可以在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面点击集群名进入集群概览页，开始操作集群。
    - 从集群概览页移除 **Connection** 和 **Import** 面板。你可点击右上角 **Connect** 获取连接信息，点击左侧导航栏 **Import** 导入数据。