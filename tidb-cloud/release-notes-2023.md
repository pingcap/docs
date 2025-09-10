---
title: 2023 年 TiDB Cloud 发布说明
summary: 了解 2023 年 TiDB Cloud 的发布说明。
---

# 2023 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2023 年的发布说明。

## 2023 年 12 月 5 日

**通用变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持恢复失败的 changefeed，无需重新创建，节省你的操作成本。

    详细信息参见 [Changefeed 状态](/tidb-cloud/changefeed-overview.md#changefeed-states)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的连接体验。

    优化 **Connect** 对话框界面，为 TiDB Cloud Serverless 用户提供更流畅、高效的连接体验。此外，TiDB Cloud Serverless 新增了更多客户端类型，并允许你选择所需分支进行连接。

    详细信息参见 [连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 2023 年 11 月 28 日

**通用变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持从备份中恢复 SQL 绑定。

    现在，TiDB Cloud 专属集群在从备份恢复时，默认会恢复用户账户和 SQL 绑定。该增强适用于 v6.2.0 及以上版本的集群，简化了数据恢复流程。SQL 绑定的恢复确保了查询相关配置和优化的顺利回归，为你提供更全面、高效的恢复体验。

    详细信息参见 [备份与恢复 TiDB Cloud 专属集群数据](/tidb-cloud/backup-and-restore.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持监控 SQL 语句的 RU 消耗。

    现在，TiDB Cloud Serverless 提供每条 SQL 语句的 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 详细信息。你可以查看每条 SQL 语句的 **Total RU** 和 **Mean RU** 消耗。该功能有助于你识别和分析 RU 消耗，为运营成本优化提供参考。

    要查看 SQL 语句 RU 详情，请进入 [你的 TiDB Cloud Serverless 集群](https://tidbcloud.com/project/clusters) 的 **Diagnosis** 页面，并点击 **SQL Statement** 标签页。

## 2023 年 11 月 21 日

**通用变更**

- [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 支持 Google Cloud 上部署的 TiDB 集群的高速物理模式。

    现在，你可以在 AWS 和 Google Cloud 上部署的 TiDB 集群使用物理模式。物理模式的迁移速度可达 110 MiB/s，是逻辑模式的 2.4 倍。该性能提升适用于大规模数据集的快速迁移至 TiDB Cloud。

    详细信息参见 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 11 月 14 日

**通用变更**

- 从 TiDB Cloud 专属集群恢复数据时，默认行为已由不恢复用户账户改为恢复所有用户账户。

    详细信息参见 [备份与恢复 TiDB Cloud 专属集群数据](/tidb-cloud/backup-and-restore.md)。

- 引入 changefeed 事件过滤器。

    该增强支持你直接在 [TiDB Cloud 控制台](https://tidbcloud.com/) 管理 changefeed 的事件过滤器，简化了排除特定事件的流程，并为下游数据同步提供更好的控制能力。

    详细信息参见 [Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

## 2023 年 11 月 7 日

**通用变更**

- 新增以下资源使用率告警。新告警默认关闭，你可按需开启。

    - TiDB 节点最大内存使用率超过 70% 持续 10 分钟
    - TiKV 节点最大内存使用率超过 70% 持续 10 分钟
    - TiDB 节点最大 CPU 使用率超过 80% 持续 10 分钟
    - TiKV 节点最大 CPU 使用率超过 80% 持续 10 分钟

  详细信息参见 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)。

## 2023 年 10 月 31 日

**通用变更**

- 支持在 TiDB Cloud 控制台直接升级为企业支持计划，无需联系销售。

    详细信息参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 10 月 25 日

**通用变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 Google Cloud 上的双区域备份（Beta）。

    部署在 Google Cloud 上的 TiDB Cloud 专属集群可无缝对接 Google Cloud Storage。与 Google Cloud Storage 的 [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr) 功能类似，TiDB Cloud 专属集群的双区域需选择同一多区域下的两个区域。例如，东京和大阪同属 `ASIA` 多区域，可共同用于双区域存储。

    详细信息参见 [开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

- [将数据变更日志流式写入 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) 功能现已正式发布（GA）。

    经过 10 个月的 Beta 试用，TiDB Cloud 到 Apache Kafka 的数据变更日志流式写入功能正式可用。在数据集成场景中，将 TiDB 数据流式写入消息队列是常见需求。你可以通过 Kafka sink 集成其他数据处理系统（如 Snowflake）或支持业务消费。

    详细信息参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。

## 2023 年 10 月 11 日

**通用变更**

- 支持 [AWS 上部署的 TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [双区域备份（Beta）](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

    你现在可以在云服务商的不同地理区域间复制备份。该功能为数据保护和灾难恢复提供了额外保障。

    详细信息参见 [备份与恢复 TiDB Cloud 专属集群数据](/tidb-cloud/backup-and-restore.md)。

- 数据迁移现已支持物理模式和逻辑模式迁移现有数据。

    物理模式下，迁移速度可达 110 MiB/s。相比逻辑模式的 45 MiB/s，迁移性能大幅提升。

    详细信息参见 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 10 月 10 日

**通用变更**

- 支持在 [Vercel Preview Deployments](https://vercel.com/docs/deployments/preview-deployments) 中使用 TiDB Cloud Serverless 分支，并集成 TiDB Cloud Vercel。

    详细信息参见 [通过分支连接 TiDB Cloud Serverless](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-branching)。

## 2023 年 9 月 28 日

**API 变更**

- 新增 TiDB Cloud 账单 API 接口，可获取指定组织某月账单。

    该账单 API 接口已在 TiDB Cloud API v1beta1（最新版本）中发布。详细信息参见 [API 文档 (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing)。

## 2023 年 9 月 19 日

**通用变更**

- 移除 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 2 vCPU TiDB 和 TiKV 节点选项。

    2 vCPU 选项已不再出现在 **Create Cluster** 或 **Modify Cluster** 页面。

- 发布 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md) for JavaScript。

    TiDB Cloud serverless driver for JavaScript 支持通过 HTTPS 连接 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。该驱动特别适用于 TCP 连接受限的边缘环境，如 [Vercel Edge Function](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。

    详细信息参见 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md)。

**控制台变更**

- 对于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群，你可以在 **Usage This Month** 面板或设置消费上限时获取费用预估。

## 2023 年 9 月 5 日

**通用变更**

- [数据服务（Beta）](https://tidbcloud.com/project/data-service) 支持为每个 API key 自定义限流，以满足不同场景下的限流需求。

    你可以在 [创建](/tidb-cloud/data-service-api-key.md#create-an-api-key) 或 [编辑](/tidb-cloud/data-service-api-key.md#edit-an-api-key) API key 时调整限流。

    详细信息参见 [限流](/tidb-cloud/data-service-api-key.md#rate-limiting)。

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新增支持 AWS 区域：圣保罗（sa-east-1）。

- 每个 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 IP 访问列表支持最多添加 100 个 IP 地址。

    详细信息参见 [配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

**控制台变更**

- 为 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群引入 **Events** 页面，记录集群主要变更。

    你可以在该页面查看最近 7 天的事件历史，并追踪触发时间、操作用户等重要信息。

    详细信息参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

**API 变更**

- 发布多项 TiDB Cloud API 接口，用于管理 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 或 [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)：

    - 为集群创建私有端点服务
    - 获取集群的私有端点服务信息
    - 为集群创建私有端点
    - 列出集群的所有私有端点
    - 列出项目下的所有私有端点
    - 删除集群的私有端点

  详细信息参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)。

## 2023 年 8 月 23 日

**通用变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)。

    你现在可以为部署在 Google Cloud 上的 TiDB Cloud 专属集群创建私有端点并建立安全连接。

    主要优势：

    - 操作直观：只需几步即可创建私有端点。
    - 安全增强：建立安全连接，保护你的数据。
    - 性能提升：提供低延迟、高带宽的连接。

  详细信息参见 [通过 Google Cloud 私有端点连接](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

- 支持通过 changefeed 将 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的数据流式写入 [Google Cloud Storage (GCS)](https://cloud.google.com/storage)。

    你可以使用自己的 GCS 存储桶并精确配置权限，将 TiDB Cloud 的数据流式写入 GCS。数据复制到 GCS 后，你可按需分析数据变更。

    详细信息参见 [流式写入云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2023 年 8 月 15 日

**通用变更**

- [数据服务（Beta）](https://tidbcloud.com/project/data-service) 支持 `GET` 请求的分页，提升开发体验。

    对于 `GET` 请求，你可以在 **Advance Properties** 启用 **Pagination**，并在调用接口时通过查询参数指定 `page` 和 `page_size`。例如，获取第 2 页且每页 10 条数据：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    注意：该功能仅适用于最后一条查询为 `SELECT` 语句的 `GET` 请求。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

- [数据服务（Beta）](https://tidbcloud.com/project/data-service) 支持为 `GET` 请求的接口响应设置缓存 TTL。

    该功能可降低数据库负载，优化接口延迟。

    对于使用 `GET` 方法的接口，你可以在 **Advance Properties** 启用 **Cache Response** 并配置缓存 TTL。

    详细信息参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

- 禁用 2023 年 8 月 15 日后在 AWS 上新建的 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的负载均衡优化，包括：

    - 扩容 AWS 上的 TiDB 节点时，不再自动迁移现有连接到新节点。
    - 缩容 AWS 上的 TiDB 节点时，不再自动迁移现有连接到可用节点。

  此变更避免混合部署时的资源争用，不影响已启用该优化的现有集群。如需为新集群启用负载均衡优化，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 8 月 8 日

**通用变更**

- [数据服务（Beta）](https://tidbcloud.com/project/data-service) 现支持 Basic 认证。

    你可以在请求中将公钥作为用户名、私钥作为密码，使用 ['Basic' HTTP 认证](https://datatracker.ietf.org/doc/html/rfc7617)。与 Digest 认证相比，Basic 认证更简单，便于调用数据服务接口。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 8 月 1 日

**通用变更**

- TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 支持 Data App 的 OpenAPI 规范。

    TiDB Cloud 数据服务为每个 Data App 自动生成 OpenAPI 文档。你可以在文档中查看接口、参数和响应，并直接试用接口。

    你还可以下载 Data App 及其已部署接口的 OpenAPI 规范（OAS），格式为 YAML 或 JSON。OAS 提供标准化 API 文档、简化集成和便捷代码生成，加快开发和协作。

    详细信息参见 [使用 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification) 及 [结合 Next.js 使用 OpenAPI 规范](/tidb-cloud/data-service-oas-with-nextjs.md)。

- 支持在 [Postman](https://www.postman.com/) 中运行 Data App。

    Postman 集成支持你将 Data App 的接口导入为集合到工作区，便于协作和无缝 API 测试，支持 Postman Web 和桌面应用。

    详细信息参见 [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)。

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新增 **Pausing** 状态，支持低成本暂停，暂停期间不计费。

    当你点击 **Pause**，集群会先进入 **Pausing** 状态，暂停完成后状态变为 **Paused**。

    只有状态变为 **Paused** 后，集群才能恢复，解决了因频繁点击 **Pause** 和 **Resume** 导致的异常恢复问题。

    详细信息参见 [暂停或恢复 TiDB Cloud 专属集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 2023 年 7 月 26 日

**通用变更**

- TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 推出自动生成接口功能。

    开发者现在可以通过极少的点击和配置，轻松创建 HTTP 接口。无需重复编写样板代码，简化并加速接口创建，减少潜在错误。

    详细用法参见 [自动生成接口](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)。

- TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 支持接口的 `PUT` 和 `DELETE` 请求方法。

    - `PUT` 方法用于更新或修改数据，类似于 `UPDATE` 语句。
    - `DELETE` 方法用于删除数据，类似于 `DELETE` 语句。

  详细信息参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

- TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service) 支持 `POST`、`PUT`、`DELETE` 方法的 **批量操作**。

    启用 **Batch Operation** 后，你可以在单次请求中操作多行数据。例如，使用单个 `POST` 请求插入多行数据。

    详细信息参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

## 2023 年 7 月 25 日

**通用变更**

- 新建 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的默认 TiDB 版本由 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3) 升级至 [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)。

**控制台变更**

- 优化 TiDB Cloud 用户访问 PingCAP 支持的入口，包括：

    - 在左下角 <MDSvgIcon name="icon-top-organization" /> 处新增 **Support** 入口。
    - 优化 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角 **?** 图标菜单，使其更直观。

  详细信息参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 7 月 18 日

**通用变更**

- 优化组织级和项目级的基于角色的访问控制（RBAC），可为用户分配最小权限角色，提升安全性、合规性和生产力。

    - 组织角色包括：`Organization Owner`、`Organization Billing Admin`、`Organization Console Audit Admin`、`Organization Member`。
    - 项目角色包括：`Project Owner`、`Project Data Access Read-Write`、`Project Data Access Read-Only`。
    - 管理项目中的集群（如创建、修改、删除集群）需具备 `Organization Owner` 或 `Project Owner` 角色。

  各角色权限详情参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)（AWS）支持客户自管加密密钥（CMEK）（Beta）。

    你可以基于 AWS KMS 创建 CMEK，对存储在 EBS 和 S3 的数据进行加密，操作均可在 TiDB Cloud 控制台完成，确保数据由客户自主管理密钥，提升安全性。

    该功能目前有一定限制，仅支持申请开通。如需申请，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

- 优化 TiDB Cloud 的导入功能，提升数据导入体验，具体改进如下：

    - Serverless 集群导入入口统一：本地文件和 Amazon S3 文件导入入口合并，便于切换。
    - 配置流程简化：Amazon S3 文件导入仅需一步配置，节省时间。
    - CSV 配置增强：CSV 配置项移至文件类型选项下，便于快速设置参数。
    - 目标表选择优化：支持通过勾选选择目标表，无需复杂表达式，简化操作。
    - 展示信息优化：修复导入过程中的信息不准确问题，并移除预览功能，避免数据不全和误导。
    - 源文件映射改进：支持自定义源文件与目标表的映射关系，无需修改源文件名以适配命名要求。

## 2023 年 7 月 11 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 现已正式发布（GA）。

- 推出 TiDB Bot（Beta），基于 OpenAI 的智能聊天机器人，支持多语言、7x24 实时响应、集成文档访问。

    TiDB Bot 为你带来以下优势：

    - 持续支持：随时为你解答问题，提升支持体验。
    - 提高效率：自动回复减少等待时间，提升整体运维效率。
    - 无缝文档访问：可直接访问 TiDB Cloud 文档，便于信息检索和快速解决问题。

  使用方法：在 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角点击 **?**，选择 **Ask TiDB Bot** 开始对话。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持 [分支功能（Beta）](/tidb-cloud/branch-overview.md)。

    TiDB Cloud 支持为 Serverless 集群创建分支。分支是原集群数据的独立副本，提供隔离环境，便于自由试验而不影响原集群。

    你可以通过 [TiDB Cloud 控制台](/tidb-cloud/branch-manage.md) 或 [TiDB Cloud CLI](/tidb-cloud/ticloud-branch-create.md) 为 2023 年 7 月 5 日后创建的 Serverless 集群创建分支。

    如果你使用 GitHub 进行应用开发，可将分支集成到 CI/CD 流程，实现自动化测试而不影响生产库。详细信息参见 [将 TiDB Cloud Serverless 分支（Beta）集成到 GitHub](/tidb-cloud/branch-github-integration.md)。

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持每周自动备份。详细信息参见 [开启自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 2023 年 7 月 4 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群支持时间点恢复（PITR）（Beta）。

    你现在可以将 Serverless 集群恢复到过去 90 天内的任意时间点。该功能提升了 Serverless 集群的数据恢复能力。例如，数据写入出错时可用 PITR 恢复到早期状态。

    详细信息参见 [备份与恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#restore)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群概览页的 **Usage This Month** 面板，提供更清晰的资源使用视图。

- 优化整体导航体验，具体变更如下：

    - 将右上角 <MDSvgIcon name="icon-top-organization" /> **Organization** 和 <MDSvgIcon name="icon-top-account-settings" /> **Account** 合并到左侧导航栏。
    - 将左侧导航栏 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin** 合并到 <MDSvgIcon name="icon-left-projects" /> **Project**，并移除左上角 ☰ 悬浮菜单。现在你可以点击 <MDSvgIcon name="icon-left-projects" /> 切换项目及修改项目设置。
    - 将所有帮助和支持信息整合到右下角 **?** 图标菜单，包括文档、交互式教程、自学培训和支持入口。

- TiDB Cloud 控制台现支持暗黑模式，提供更舒适、护眼的体验。你可在左侧导航栏底部切换明暗模式。

## 2023 年 6 月 27 日

**通用变更**

- 新建 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群不再预置示例数据集。

## 2023 年 6 月 20 日

**通用变更**

- 新建 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的默认 TiDB 版本由 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2) 升级至 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)。

## 2023 年 6 月 13 日

**通用变更**

- 支持通过 changefeed 将数据流式写入 Amazon S3。

    该功能实现 TiDB Cloud 与 Amazon S3 的无缝集成，支持将 [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的数据实时捕获并复制到 Amazon S3，确保下游应用和分析系统获取最新数据。

    详细信息参见 [流式写入云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 16 vCPU TiKV 节点最大存储由 4 TiB 提升至 6 TiB。

    该增强提升了集群的数据存储能力，提高了工作负载扩展效率，满足数据增长需求。

    详细信息参见 [集群规格选择](/tidb-cloud/size-your-cluster.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群的 [监控指标保留期](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 由 3 天延长至 7 天。

    保留期延长后，你可访问更多历史数据，有助于识别集群趋势和模式，提升决策和故障排查效率。

**控制台变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 **Key Visualizer** 页面，获取所需信息，提升 SQL 诊断体验和用户友好性。

## 2023 年 6 月 6 日

**通用变更**

- [TiDB Cloud 专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 引入 Index Insight（Beta），为慢查询提供索引优化建议，提升查询性能。

    通过 Index Insight，你可以：

    - 提升查询性能：识别慢查询并推荐合适索引，加速查询执行，缩短响应时间，提升用户体验。
    - 降低成本：优化查询性能，减少额外计算资源消耗，更高效利用现有基础设施，降低运维成本。
    - 简化优化流程：自动识别并推荐索引，无需手动分析和猜测，节省时间和精力。
    - 提高应用效率：优化数据库性能后，应用可承载更大负载和更多并发用户，提升扩展能力。

  使用方法：进入专属集群的 **Diagnosis** 页面，点击 **Index Insight BETA** 标签。

- 推出 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes)，无需注册或安装即可体验 TiDB 全功能的交互式平台。

    TiDB Playground 提供一站式体验，支持扩展性、MySQL 兼容性和实时分析等能力。

    你可以在受控环境下实时试用 TiDB 功能，无需复杂配置，便于理解 TiDB 特性。

    立即体验，请访问 [**TiDB Playground**](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes) 页面，选择你想探索的功能，开始体验。

## 2023 年 6 月 5 日

**通用变更**

- 支持将 [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) 连接到 GitHub。

    [连接 Data App 到 GitHub](/tidb-cloud/data-service-manage-github-connection.md) 后，你可以将所有配置作为 [代码文件](/tidb-cloud/data-service-app-config-files.md) 管理，实现与系统架构和 DevOps 流程的无缝集成。

    该功能提升 Data App 的 CI/CD 体验，支持：

    - 通过 GitHub 自动部署 Data App 变更。
    - 在 GitHub 上配置 Data App 的 CI/CD 流程并进行版本控制。
    - 断开已连接的 GitHub 仓库。
    - 部署前审查接口变更。
    - 查看部署历史并在失败时采取措施。
    - 重新部署某个提交以回滚到早期部署。

  详细信息参见 [通过 GitHub 自动部署 Data App](/tidb-cloud/data-service-manage-github-connection.md)。

## 2023 年 6 月 2 日

**通用变更**

- 为简化和明晰产品命名，我们更新了产品名称：

    - "TiDB Cloud Serverless Tier" 现称为 "TiDB Cloud Serverless"
    - "TiDB Cloud Dedicated Tier" 现称为 "TiDB Cloud 专属集群"
    - "TiDB On-Premises" 现称为 "TiDB 自管版"

    名称焕新，性能如一。你的体验始终是我们的首要任务。

## 2023 年 5 月 30 日

**通用变更**

- 增强 TiDB Cloud 数据迁移功能对增量数据迁移的支持。

    你现在可以指定 binlog 位置或全局事务标识（GTID），仅复制指定位置之后产生的增量数据到 TiDB Cloud。该增强为你选择和复制所需数据提供更大灵活性，满足特定需求。

    详情参见 [仅迁移 MySQL 兼容数据库的增量数据到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

- [**Events**](/tidb-cloud/tidb-cloud-events.md) 页面新增事件类型（`ImportData`）。

- 从 TiDB Cloud 控制台移除 **Playground**。

    敬请期待全新独立 Playground，体验将进一步优化。

## 2023 年 5 月 23 日

**通用变更**

- 上传 CSV 文件到 TiDB 时，列名除英文和数字外，还可使用中文、日文等字符。特殊字符仅支持下划线（`_`）。

    详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2023 年 5 月 16 日

**控制台变更**

- 为专属集群和 Serverless 集群引入按功能分类的左侧导航入口。

    新导航更易发现功能入口。可在集群概览页体验新导航。

- 专属集群 **Diagnosis** 页的以下两个标签页发布全新原生 Web 架构：

    - [Slow Query](/tidb-cloud/tune-performance.md#slow-query)
    - [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis)

    新架构让你更便捷地浏览这两个标签页，提升 SQL 诊断体验和用户友好性。

## 2023 年 5 月 9 日

**通用变更**

- 支持为 2023 年 4 月 26 日后创建的 GCP 集群变更节点规格。

    你可以根据需求升级为高性能节点或降级为低成本节点，灵活调整集群容量，优化成本。

    详细步骤参见 [变更节点规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)。

- 支持导入压缩文件。你可以导入 `.gzip`、`.gz`、`.zstd`、`.zst`、`.snappy` 格式的 CSV 和 SQL 文件。该功能提升了数据导入效率，降低数据传输成本。

    详细信息参见 [从云存储导入 CSV 文件到 TiDB Cloud 专属集群](/tidb-cloud/import-csv-files.md) 及 [导入示例数据](/tidb-cloud/import-sample-data.md)。

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持基于 AWS PrivateLink 的私有端点连接，作为新的网络访问管理选项。

    私有端点连接不会将数据暴露在公网，并支持 CIDR 重叠，便于网络管理。

    详细信息参见 [设置私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

- [**Event**](/tidb-cloud/tidb-cloud-events.md) 页面新增事件类型，记录专属集群的备份、恢复和 changefeed 操作。

    事件类型完整列表参见 [已记录事件](/tidb-cloud/tidb-cloud-events.md#logged-events)。

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的 [**SQL Diagnosis**](/tidb-cloud/tune-performance.md) 页面新增 **SQL Statement** 标签。

    **SQL Statement** 标签提供：

    - 所有 SQL 语句的全面概览，便于识别和诊断慢查询。
    - 每条 SQL 语句的详细信息，如查询时间、执行计划、数据库响应，助力优化性能。
    - 友好的界面，便于排序、筛选和搜索大量数据，聚焦关键查询。

  详细信息参见 [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis)。

## 2023 年 5 月 6 日

**通用变更**

- 支持直接访问 TiDB [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 所在区域的 [Data Service endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint)。

    新建 Serverless 集群的 endpoint URL 现包含集群区域信息。通过 `<region>.data.tidbcloud.com` 可直接访问对应区域的 endpoint。

    你也可以请求全局域名 `data.tidbcloud.com`，此时 TiDB Cloud 会内部重定向到目标区域，但可能增加延迟。如采用此方式，调用接口时请确保 curl 命令加上 `--location-trusted`。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 4 月 25 日

**通用变更**

- 组织下前 5 个 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 可享受如下免费额度：

    - 行存储：5 GiB
    - [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

  2023 年 5 月 31 日前，Serverless 集群仍免费（100% 折扣）。之后超出免费额度部分将计费。

    你可在集群 **Overview** 页的 **Usage This Month** 区域 [监控用量或提升额度](/tidb-cloud/manage-serverless-spend-limit.md)。免费额度用尽后，集群读写操作将被限流，直至提升额度或新月重置。

    各资源（读、写、SQL CPU、网络出口）RU 消耗、定价及限流说明参见 [TiDB Cloud Serverless Tier 价格详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 支持备份与恢复。

     详细信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore-serverless.md)。

- 新建 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的默认 TiDB 版本由 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1) 升级至 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)。

- 提供维护窗口功能，便于你为 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 计划和管理维护任务。

    维护窗口是执行操作系统更新、安全补丁、基础设施升级等计划性维护的指定时间段，保障 TiDB Cloud 服务的可靠性、安全性和性能。

    维护期间可能出现短暂连接中断或 QPS 波动，但集群保持可用，SQL 操作、数据导入、备份、恢复、迁移、同步等任务可正常运行。维护期间允许和禁止的操作见 [文档](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)。

    我们将尽量减少维护频率。若有维护计划，默认开始时间为目标周三 03:00（以组织时区为准）。请关注维护计划，合理安排操作。

    - 每次维护窗口，TiDB Cloud 会发送三封邮件通知：维护前、开始时、结束后。
    - 你可在 **Maintenance** 页面修改维护开始时间或延后维护，以减少影响。

  详细信息参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 优化 AWS 上新建（2023 年 4 月 25 日后）[专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 TiDB 负载均衡，缩放 TiDB 节点时减少连接中断。

    - 扩容时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容时，支持自动迁移现有连接到可用 TiDB 节点。

  目前该功能适用于所有 AWS 上的专属集群。

**控制台变更**

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，提升监控体验和用户友好性。

## 2023 年 4 月 18 日

**通用变更**

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持扩缩 [数据迁移任务规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

    你可以通过扩容提升迁移性能，或缩容降低成本。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)。

**控制台变更**

- 全新设计的 [集群创建](https://tidbcloud.com/clusters/create-cluster) UI，更加友好，支持一键创建和配置集群。

    新设计简化界面，减少视觉干扰，指引清晰。点击 **Create** 后将直接跳转到集群概览页，无需等待集群创建完成。

    详细信息参见 [创建集群](/tidb-cloud/create-tidb-cluster.md)。

- **Billing** 页新增 **Discounts** 标签，展示组织所有者和账单管理员的折扣信息。

    详细信息参见 [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts)。

## 2023 年 4 月 11 日

**通用变更**

- 优化 AWS 上 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 TiDB 负载均衡，缩放 TiDB 节点时减少连接中断。

    - 扩容时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容时，支持自动迁移现有连接到可用 TiDB 节点。

  目前该功能仅适用于 AWS `Oregon (us-west-2)` 区域的专属集群。

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 [New Relic](https://newrelic.com/) 集成。

    你可以将 TiDB 集群的监控数据发送到 [New Relic](https://newrelic.com/)，在 New Relic 上同时监控应用和数据库性能，便于快速定位和排查问题。

    集成步骤及可用指标参见 [集成 New Relic](/tidb-cloud/monitor-new-relic-integration.md)。

- 为专属集群的 Prometheus 集成新增以下 [changefeed](/tidb-cloud/changefeed-overview.md) 指标：

    - `tidbcloud_changefeed_latency`
    - `tidbcloud_changefeed_replica_rows`

    已集成 Prometheus 的用户可实时监控 changefeed 性能和健康状况，并可基于这些指标创建告警。

**控制台变更**

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面升级为 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server)。

    节点级指标可更准确反映资源消耗，帮助你了解实际服务使用情况。

    访问方法：进入集群 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，点击 **Metrics** 标签下的 **Server** 类别。

- 优化 [Billing](/tidb-cloud/tidb-cloud-billing.md#billing-details) 页面，将账单项按 **Summary by Project** 和 **Summary by Service** 分类，信息更清晰。

## 2023 年 4 月 4 日

**通用变更**

- 为防止误报，从 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) 移除以下两项告警。因为单节点临时离线或 OOM 不会显著影响集群整体健康。

    - 集群中至少有一个 TiDB 节点 OOM
    - 一个或多个集群节点离线

**控制台变更**

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新增 [Alerts](/tidb-cloud/monitor-built-in-alerting.md) 页面，展示每个集群的活跃和已关闭告警。

    **Alerts** 页面提供：

    - 直观友好的界面。即使未订阅告警邮件，也可在此查看集群告警。
    - 高级筛选，按严重性、状态等属性快速查找和排序，并可查看近 7 天历史，便于追踪。
    - **Edit Rule** 功能。可自定义告警规则，满足集群需求。

  详细信息参见 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

- 将 TiDB Cloud 的帮助信息和操作整合到一个入口。

    现在，你可在 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角点击 **?** 获取所有帮助信息及联系支持。

- 推出 [Getting Started](https://tidbcloud.com/getting-started) 页面，帮助你快速了解 TiDB Cloud。

    **Getting Started** 页面提供交互式教程、基础指南和实用链接。通过交互式教程，你可用预置行业数据集（Steam Game Dataset、S&P 500 Dataset）体验 TiDB Cloud 功能和 HTAP 能力。

    访问方法：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左侧导航栏点击 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Getting Started**。你可点击 **Query Sample Dataset** 打开交互式教程，或点击其他链接探索 TiDB Cloud。也可在右下角 **?** 菜单点击 **Interactive Tutorials**。

## 2023 年 3 月 29 日

**通用变更**

- [数据服务（Beta）](/tidb-cloud/data-service-overview.md) 支持 Data App 更细粒度的访问控制。

    在 Data App 详情页，你可以关联集群并为每个 API key 指定角色。角色控制 API key 是否可读写关联集群数据，可设为 `ReadOnly` 或 `ReadAndWrite`。该功能实现 Data App 的集群级和权限级访问控制，灵活满足业务需求。

    详细信息参见 [管理关联集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) 和 [管理 API key](/tidb-cloud/data-service-api-key.md)。

## 2023 年 3 月 28 日

**通用变更**

- [changefeed](/tidb-cloud/changefeed-overview.md) 新增 2 RCUs、4 RCUs、8 RCUs 规格，支持在 [创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时选择。

    使用新规格，数据同步成本最高可降低 87.5%（相较于原需 16 RCUs 的场景）。

- 支持为 2023 年 3 月 28 日后创建的 [changefeed](/tidb-cloud/changefeed-overview.md) 扩缩规格。

    你可通过选择更高规格提升同步性能，或选择更低规格降低同步成本。

    详细信息参见 [扩缩 changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)。

- 支持将 AWS 上 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的增量数据实时同步到同项目同区域的 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。

    详细信息参见 [流式写入 TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)。

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能新增支持两个 GCP 区域：`Singapore (asia-southeast1)` 和 `Oregon (us-west1)`。

    新增区域为数据迁移提供更多选择。若上游数据存储于或靠近这些区域，可获得更快、更可靠的迁移体验。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 页面，提升 SQL 诊断体验和用户友好性。

## 2023 年 3 月 21 日

**通用变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 推出 [数据服务（Beta）](https://tidbcloud.com/project/data-service)，支持通过自定义 API endpoint 以 HTTPS 请求访问数据。

    数据服务可无缝集成 TiDB Cloud 与任何兼容 HTTPS 的应用或服务。常见场景包括：

    - 移动或 Web 应用直接访问 TiDB 集群数据库。
    - 使用无服务器边缘函数调用接口，避免连接池扩展性问题。
    - 通过数据服务作为数据源集成数据可视化项目。
    - 在不支持 MySQL 接口的环境中连接数据库。

    此外，TiDB Cloud 提供 [Chat2Query API](/tidb-cloud/use-chat2query-api.md)，可通过 AI 生成并执行 SQL 语句。

    访问方法：左侧导航栏进入 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。详细文档：

    - [数据服务概览](/tidb-cloud/data-service-overview.md)
    - [数据服务快速入门](/tidb-cloud/data-service-get-started.md)
    - [Chat2Query API 快速入门](/tidb-cloud/use-chat2query-api.md)

- 支持缩小 TiDB、TiKV、TiFlash 节点规格，对 2022 年 12 月 31 日后在 AWS 上创建的 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 进行缩容。

    你可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 缩小节点规格。

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的 [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 功能新增支持 GCP 区域：`Tokyo (asia-northeast1)`。

    该功能便于将 GCP 上的 MySQL 兼容数据库迁移到 TiDB 集群。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新增 **Events** 页面，记录集群主要变更。

    你可查看最近 7 天的事件历史，追踪触发时间、操作用户等信息。例如，查看集群暂停、规格变更等事件。

    详细信息参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的 **Monitoring** 页面新增 **Database Status** 标签，展示以下数据库级指标：

    - QPS Per DB
    - Average Query Duration Per DB
    - Failed Queries Per DB

  通过这些指标，你可监控各数据库性能，做出数据驱动决策，提升应用性能。

  详细信息参见 [Serverless 集群监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 3 月 14 日

**通用变更**

- 新建 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的默认 TiDB 版本由 [v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0) 升级至 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)。

- 支持在上传带表头的本地 CSV 文件时，修改 TiDB Cloud 自动创建目标表的列名。

    向 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 导入带表头的本地 CSV 文件时，若表头列名不符合 TiDB Cloud 命名规范，将在对应列名旁显示警告图标。你可悬停图标，根据提示编辑或输入新列名。

    列命名规范参见 [导入本地文件](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)。

## 2023 年 3 月 7 日

**通用变更**

- 所有 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的默认 TiDB 版本由 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0) 升级至 [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)。

## 2023 年 2 月 28 日

**通用变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 新增 [SQL Diagnosis](/tidb-cloud/tune-performance.md) 功能。

    通过 SQL Diagnosis，你可深入了解 SQL 运行时状态，提升 SQL 性能调优效率。目前 Serverless 集群仅提供慢查询数据。

    使用方法：在 Serverless 集群页面左侧导航栏点击 **SQL Diagnosis**。

**控制台变更**

- 优化左侧导航。

    你可更高效地切换页面，例如：

    - 鼠标悬停左上角可快速切换集群或项目。
    - 可在 **Clusters** 和 **Admin** 页面间切换。

**API 变更**

- 发布多项数据导入相关 TiDB Cloud API 接口：

    - 列出所有导入任务
    - 获取导入任务详情
    - 创建导入任务
    - 更新导入任务
    - 上传本地文件
    - 启动导入前预览数据
    - 获取导入任务角色信息

  详细信息参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)。

## 2023 年 2 月 22 日

**通用变更**

- 支持使用 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md) 跟踪组织成员在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的各类操作。

    该功能仅对 `Owner` 或 `Audit Admin` 可见，默认关闭。启用方法：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 右上角点击 <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**。

    通过分析审计日志，可识别可疑操作，提升组织资源和数据安全。

    详细信息参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 `ticloud cluster connect-info` 命令。

    `ticloud cluster connect-info` 可获取集群连接字符串。需将 [ticloud 升级](/tidb-cloud/ticloud-upgrade.md) 至 v0.3.2 或更高版本。

## 2023 年 2 月 21 日

**通用变更**

- 支持使用 IAM 用户的 AWS 访问密钥访问 Amazon S3 存储桶导入数据。

    该方式比使用 Role ARN 更简单。详细信息参见 [配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

- 监控指标保留期由 2 天延长：

    - 专属集群可查看近 7 天指标数据。
    - Serverless 集群可查看近 3 天指标数据。

  保留期延长后，你可访问更多历史数据，有助于识别趋势和模式，提升决策和故障排查效率。

**控制台变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的 Monitoring 页面发布全新原生 Web 架构。

    新架构让你更便捷地浏览 Monitoring 页面，提升监控体验和用户友好性。

## 2023 年 2 月 17 日

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 [`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md) 命令。

    `ticloud connect` 支持你无需安装 SQL 客户端，直接从本地连接 TiDB Cloud 集群并执行 SQL 语句。

## 2023 年 2 月 14 日

**通用变更**

- 支持缩减 TiKV 和 TiFlash 节点数量，对 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 进行缩容。

    你可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-node-number) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 缩减节点数量。

**控制台变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 新增 **Monitoring** 页面。

    **Monitoring** 页面提供 SQL 每秒执行数、平均查询时长、失败查询数等多项指标，帮助你全面了解 Serverless 集群 SQL 性能。

    详细信息参见 [TiDB Cloud 内置监控](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 2 月 2 日

**CLI 变更**

- 推出 TiDB Cloud CLI 客户端 [`ticloud`](/tidb-cloud/cli-reference.md)。

    使用 `ticloud`，你可通过命令行或自动化流程轻松管理 TiDB Cloud 资源。针对 GitHub Actions，我们提供了 [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli) 便捷集成。

    详细信息参见 [TiDB Cloud CLI 快速入门](/tidb-cloud/get-started-with-cli.md) 和 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2023 年 1 月 18 日

**通用变更**

* 支持使用 Microsoft 账户 [注册](https://tidbcloud.com/free-trial) TiDB Cloud。

## 2023 年 1 月 17 日

**通用变更**

- 新建 [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 的默认 TiDB 版本由 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) 升级至 [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)。

- 新注册用户将自动创建一个免费的 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，便于快速开启数据探索之旅。

- [专属集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 新增支持 AWS 区域：`Seoul (ap-northeast-2)`。

    该区域支持以下功能：

    - [使用数据迁移迁移 MySQL 兼容数据库到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [通过 changefeed 将 TiDB Cloud 数据流式写入其他服务](/tidb-cloud/changefeed-overview.md)
    - [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日

**通用变更**

- 优化本地 CSV 文件导入 TiDB 的体验，提升 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 用户体验。

    - 现在可直接拖拽 CSV 文件到 **Import** 页上传区域。
    - 创建导入任务时，若目标数据库或表不存在，可输入名称自动创建。新建目标表时可指定主键或选择多字段组成复合主键。
    - 导入完成后，可点击 **Explore your data by Chat2Query** 或任务列表中的目标表名，使用 [AI 驱动的 Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) 探索数据。

  详细信息参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

**控制台变更**

- 每个集群新增 **Get Support** 选项，简化针对特定集群的支持请求流程。

    你可通过以下方式请求支持：

    - 在项目 [**Clusters**](https://tidbcloud.com/project/clusters) 页，点击集群行的 **...** 并选择 **Get Support**。
    - 在集群概览页右上角点击 **...** 并选择 **Get Support**。

## 2023 年 1 月 5 日

**控制台变更**

- [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 将 SQL Editor（Beta）重命名为 Chat2Query（Beta），并支持 AI 生成 SQL 查询。

  在 Chat2Query 中，你可以让 AI 自动生成 SQL 查询，也可手动编写 SQL 并直接运行，无需终端。

  访问方法：在项目 [**Clusters**](https://tidbcloud.com/project/clusters) 页点击集群名，再点击左侧导航栏的 **Chat2Query**。

## 2023 年 1 月 4 日

**通用变更**

- 支持通过增加 **Node Size(vCPU + RAM)** 扩容 AWS 上（2022 年 12 月 31 日后创建）的 TiDB Cloud 专属集群的 TiDB、TiKV、TiFlash 节点。

    你可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 增加节点规格。

- [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的指标保留期延长至两天。

    你现在可访问近两天的指标数据，更灵活地监控集群性能和趋势。

    该提升无需额外费用，可在集群 [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的 **Diagnosis** 标签访问，有助于更高效地排查性能问题和监控集群健康。

- 支持为 Prometheus 集成自定义 Grafana dashboard JSON。

    已集成 Prometheus 的用户可导入预置 Grafana dashboard 并自定义，便于快速监控 TiDB Cloud 集群，及时发现性能问题。

    详细信息参见 [使用 Grafana GUI dashboard 可视化指标](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)。

- 所有 [Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 的默认 TiDB 版本由 [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0) 升级至 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)。Serverless 集群升级至 v6.4.0 后的冷启动问题已修复。

**控制台变更**

- 简化 [**Clusters**](https://tidbcloud.com/project/clusters) 页和集群概览页展示。

    - 你可在 [**Clusters**](https://tidbcloud.com/project/clusters) 页点击集群名进入概览页并开始操作。
    - 从概览页移除 **Connection** 和 **Import** 面板。你可在右上角点击 **Connect** 获取连接信息，或在左侧导航栏点击 **Import** 导入数据。