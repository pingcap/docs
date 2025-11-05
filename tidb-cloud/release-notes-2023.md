---
title: 2023 年 TiDB Cloud 发布说明
summary: 了解 2023 年 TiDB Cloud 的发布说明。
---

# 2023 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2023 年的发布说明。

## 2023 年 12 月 5 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持恢复失败的 changefeed，无需重新创建，节省操作成本。

    详细信息参见 [Changefeed 状态](/tidb-cloud/changefeed-overview.md#changefeed-states)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 的连接体验。

    优化 **Connect** 对话框界面，为 TiDB Cloud Serverless 用户提供更流畅、高效的连接体验。此外，TiDB Cloud Serverless 新增了更多客户端类型，并允许你选择所需分支进行连接。

    详细信息参见 [连接到 TiDB Cloud Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 2023 年 11 月 28 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持从备份中恢复 SQL 绑定。

    TiDB Cloud Dedicated 现在在从备份恢复时，默认会恢复用户账号和 SQL 绑定。该增强适用于 v6.2.0 及以上版本的集群，简化了数据恢复流程。SQL 绑定的恢复确保了查询相关配置和优化的顺利回归，为你提供更全面、高效的恢复体验。

    详细信息参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 支持监控 SQL 语句的 RU 消耗。

    TiDB Cloud Serverless 现在可以详细展示每条 SQL 语句的 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 消耗。你可以查看每条 SQL 语句的 **Total RU** 和 **Mean RU**。该功能有助于你识别和分析 RU 消耗，为运营成本优化提供参考。

    查看 SQL 语句 RU 详情，请进入 [你的 TiDB Cloud Serverless 集群](https://tidbcloud.com/project/clusters)的 **Diagnosis** 页面，并点击 **SQL Statement** 标签页。

## 2023 年 11 月 21 日

**通用变更**

- [数据迁移](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 支持 Google Cloud 上部署的 TiDB 集群的高速物理模式。

    现在你可以在 AWS 和 Google Cloud 上部署的 TiDB 集群使用物理模式。物理模式的迁移速度可达 110 MiB/s，是逻辑模式的 2.4 倍。该性能提升适合大规模数据集的快速迁移至 TiDB Cloud。

    详细信息参见 [迁移现有数据和增量数据](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data)。

## 2023 年 11 月 14 日

**通用变更**

- 从 TiDB Cloud Dedicated 集群恢复数据时，默认行为由不恢复用户账号改为恢复所有用户账号。

    详细信息参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 为 changefeed 引入事件过滤器。

    该增强支持你直接在 [TiDB Cloud 控制台](https://tidbcloud.com/) 管理 changefeed 的事件过滤器，简化了排除特定事件的流程，并为下游数据同步提供更好的控制。

    详细信息参见 [Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)。

## 2023 年 11 月 7 日

**通用变更**

- 新增以下资源使用率告警，默认关闭。你可按需开启。

    - TiDB 节点最大内存使用率超过 70% 持续 10 分钟
    - TiKV 节点最大内存使用率超过 70% 持续 10 分钟
    - TiDB 节点最大 CPU 使用率超过 80% 持续 10 分钟
    - TiKV 节点最大 CPU 使用率超过 80% 持续 10 分钟

  详细信息参见 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts)。

## 2023 年 10 月 31 日

**通用变更**

- 支持在 TiDB Cloud 控制台直接升级到 Enterprise 支持计划，无需联系销售。

    详细信息参见 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 10 月 25 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 支持 Google Cloud 上的双区域备份（beta）。

    部署在 Google Cloud 上的 TiDB Cloud Dedicated 集群可无缝对接 Google Cloud Storage。与 Google Cloud Storage 的 [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr) 功能类似，TiDB Cloud Dedicated 的双区域需选择同一多区域下的两个区域。例如，东京和大阪同属 `ASIA` 多区域，可共同用于双区域存储。

    详细信息参见 [开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

- [将数据变更日志流式写入 Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) 功能现已正式 GA。

    经过 10 个月的 beta 试用，该功能现已正式可用。将 TiDB Cloud 的数据变更日志流式写入 Apache Kafka 是数据集成场景的常见需求。你可以通过 Kafka sink 集成其他数据处理系统（如 Snowflake）或支持业务消费。

    详细信息参见 [Changefeed 概览](/tidb-cloud/changefeed-overview.md)。

## 2023 年 10 月 11 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（部署在 AWS）支持 [双区域备份（beta）](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

    你现在可以在云服务商内部跨地理区域复制备份。该功能为数据保护和灾难恢复提供了额外保障。

    详细信息参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

- 数据迁移现已支持物理模式和逻辑模式迁移现有数据。

    物理模式下迁移速度可达 110 MiB/s，相较逻辑模式的 45 MiB/s，性能大幅提升。

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

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群移除 2 vCPU 的 TiDB 和 TiKV 节点选项。

    **Create Cluster** 和 **Modify Cluster** 页面均不再提供 2 vCPU 选项。

- 发布 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md) for JavaScript。

    该驱动允许你通过 HTTPS 连接 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群，特别适用于 TCP 连接受限的边缘环境，如 [Vercel Edge Function](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。

    详细信息参见 [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群支持在 **Usage This Month** 面板或设置消费上限时预估费用。

## 2023 年 9 月 5 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持为每个 API key 自定义限流，以满足不同场景下的速率限制需求。

    你可以在 [创建](/tidb-cloud/data-service-api-key.md#create-an-api-key) 或 [编辑](/tidb-cloud/data-service-api-key.md#edit-an-api-key) API key 时调整限流。

    详细信息参见 [速率限制](/tidb-cloud/data-service-api-key.md#rate-limiting)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增支持 AWS 区域：圣保罗（sa-east-1）。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 IP 访问列表支持最多添加 100 个 IP 地址。

    详细信息参见 [配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

**控制台变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群新增 **Events** 页面，记录集群主要变更。

    该页面可查看最近 7 天的事件历史，并追踪触发时间、操作用户等重要信息。

    详细信息参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

**API 变更**

- 发布多项 TiDB Cloud API 接口，用于管理 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 或 [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) 相关的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群：

    - 为集群创建私有端点服务
    - 获取集群的私有端点服务信息
    - 为集群创建私有端点
    - 列出集群的所有私有端点
    - 列出项目下的所有私有端点
    - 删除集群的私有端点

  详细信息参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster)。

## 2023 年 8 月 23 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持 Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)。

    你现在可以为部署在 Google Cloud 的 TiDB Cloud Dedicated 集群创建私有端点并建立安全连接。

    主要优势：

    - 操作直观：仅需几步即可创建私有端点。
    - 安全增强：建立安全连接，保护数据安全。
    - 性能提升：提供低延迟、高带宽的连接。

  详细信息参见 [通过 Google Cloud 私有端点连接](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

- 支持通过 changefeed 将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群数据流式写入 [Google Cloud Storage (GCS)](https://cloud.google.com/storage)。

    你可以使用自己的 GCS 存储桶并精确配置权限，将数据流式复制到 GCS，便于后续分析数据变更。

    详细信息参见 [流式写入云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

## 2023 年 8 月 15 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持 `GET` 请求的分页，提升开发体验。

    对于 `GET` 请求，你可以在 **Advance Properties** 启用 **Pagination**，并在调用接口时通过查询参数指定 `page` 和 `page_size`。例如，获取第 2 页且每页 10 条数据：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    注意：该功能仅适用于最后一条查询为 `SELECT` 语句的 `GET` 请求。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 支持为 `GET` 请求的接口响应设置缓存 TTL。

    该功能可降低数据库负载，优化接口延迟。

    对于 `GET` 请求接口，你可在 **Advance Properties** 启用 **Cache Response** 并配置缓存 TTL。

    详细信息参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

- 禁用 2023 年 8 月 15 日后在 AWS 上新建的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的负载均衡改进，包括：

    - 扩容 AWS 上的 TiDB 节点时，不再自动迁移现有连接到新节点。
    - 缩容 AWS 上的 TiDB 节点时，不再自动迁移现有连接到可用节点。

  该变更避免了混合部署的资源争用，不影响已启用该功能的现有集群。如需为新集群启用负载均衡改进，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 2023 年 8 月 8 日

**通用变更**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) 现支持 Basic Authentication。

    你可以在请求中将公钥作为用户名、私钥作为密码，使用 ['Basic' HTTP 认证](https://datatracker.ietf.org/doc/html/rfc7617)。与 Digest Authentication 相比，Basic Authentication 更简单，便于调用 Data Service 接口。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 8 月 1 日

**通用变更**

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 支持 Data App 的 OpenAPI 规范。

    TiDB Cloud Data Service 为每个 Data App 自动生成 OpenAPI 文档。你可以在文档中查看接口、参数和响应，并直接试用接口。

    你还可以下载 Data App 及其已部署接口的 OpenAPI 规范（OAS），支持 YAML 或 JSON 格式。OAS 提供标准化 API 文档、简化集成和便捷代码生成，加快开发和协作。

    详细信息参见 [使用 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification) 及 [结合 Next.js 使用 OpenAPI 规范](/tidb-cloud/data-service-oas-with-nextjs.md)。

- 支持在 [Postman](https://www.postman.com/) 中运行 Data App。

    Postman 集成支持你将 Data App 的接口作为集合导入工作区，便于协作和 API 测试，支持 Postman Web 和桌面应用。

    详细信息参见 [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 **Pausing** 状态，暂停期间无需付费。

    当你点击 **Pause**，集群会先进入 **Pausing** 状态，暂停完成后状态变为 **Paused**。

    只有状态变为 **Paused** 后才能恢复，解决了因频繁点击 **Pause** 和 **Resume** 导致的异常恢复问题。

    详细信息参见 [暂停或恢复 TiDB Cloud Dedicated 集群](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 2023 年 7 月 26 日

**通用变更**

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 推出自动生成接口功能。

    开发者可通过极少的点击和配置，快速创建 HTTP 接口，省去重复样板代码，简化并加速接口创建，减少潜在错误。

    详细用法参见 [自动生成接口](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)。

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 支持接口的 `PUT` 和 `DELETE` 请求方法。

    - `PUT` 用于更新或修改数据，类似 `UPDATE` 语句。
    - `DELETE` 用于删除数据，类似 `DELETE` 语句。

  详细信息参见 [配置属性](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)。

- TiDB Cloud [Data Service](https://tidbcloud.com/project/data-service) 支持 `POST`、`PUT`、`DELETE` 请求方法的 **Batch Operation**。

    启用 **Batch Operation** 后，可在单次请求中操作多行数据。例如，使用单条 `POST` 请求插入多行数据。

    详细信息参见 [高级属性](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties)。

## 2023 年 7 月 25 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3) 升级至 [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)。

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
    - 管理项目内集群（如创建、修改、删除集群）需具备 `Organization Owner` 或 `Project Owner` 角色。

  各角色权限详情参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（AWS）支持客户自管加密密钥（CMEK）（beta）。

    你可基于 AWS KMS 创建 CMEK，对 EBS 和 S3 存储的数据进行加密，密钥由客户自主管理，提升安全性。

    该功能有一定限制，仅支持申请开通。如需申请，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

- 优化 TiDB Cloud 的导入功能，提升数据导入体验，具体改进如下：

    - Serverless 导入入口统一：合并本地文件和 Amazon S3 文件导入入口，便于切换。
    - 配置简化：从 Amazon S3 导入数据仅需一步，节省时间。
    - CSV 配置增强：CSV 配置项移至文件类型选项下，便于快速配置参数。
    - 目标表选择优化：支持通过勾选选择目标表，无需复杂表达式，简化操作。
    - 展示信息优化：修复导入过程中的信息不准确问题，并移除预览功能，避免数据不全导致误导。
    - 源文件映射改进：支持自定义源文件与目标表的映射关系，无需修改源文件名以适配命名要求。

## 2023 年 7 月 11 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 现已正式 GA。

- 推出 TiDB Bot（beta），基于 OpenAI 的智能聊天机器人，支持多语言、7x24 实时响应、集成文档访问。

    TiDB Bot 带来如下优势：

    - 持续支持：随时为你解答问题，提升支持体验。
    - 提高效率：自动回复减少等待，提升整体运维效率。
    - 无缝文档访问：可直接访问 TiDB Cloud 文档，便于信息检索和问题快速定位。

  使用方法：在 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角点击 **?**，选择 **Ask TiDB Bot** 开始对话。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群支持 [分支功能（beta）](/tidb-cloud/branch-overview.md)。

    你可以为 TiDB Cloud Serverless 集群创建分支。分支是原集群数据的分叉副本，提供隔离环境，便于自由实验而不影响原集群。

    2023 年 7 月 5 日后创建的 Serverless 集群可通过 [TiDB Cloud 控制台](/tidb-cloud/branch-manage.md) 或 [TiDB Cloud CLI](/tidb-cloud/ticloud-branch-create.md) 创建分支。

    若你使用 GitHub 进行应用开发，可将分支集成到 CI/CD 流程，实现自动化测试而不影响生产库。详细信息参见 [与 GitHub 集成 TiDB Cloud Serverless 分支（Beta）](/tidb-cloud/branch-github-integration.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持每周自动备份。详细信息参见 [开启自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 2023 年 7 月 4 日

**通用变更**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群支持时间点恢复（PITR）（beta）。

    你现在可以将 Serverless 集群恢复到过去 90 天内的任意时间点，提升数据恢复能力。例如，数据写入出错时可用 PITR 恢复到早期状态。

    详细信息参见 [备份与恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md#restore)。

**控制台变更**

- 优化 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群概览页的 **Usage This Month** 面板，资源使用情况更清晰。

- 优化整体导航体验，具体变更如下：

    - 将右上角 <MDSvgIcon name="icon-top-organization" /> **Organization** 和 <MDSvgIcon name="icon-top-account-settings" /> **Account** 合并至左侧导航栏。
    - 将左侧导航栏 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin** 合并至 <MDSvgIcon name="icon-left-projects" /> **Project**，并移除左上角 ☰ 悬浮菜单。现在可通过 <MDSvgIcon name="icon-left-projects" /> 切换项目及修改项目设置。
    - 所有帮助与支持信息整合至右下角 **?** 菜单，包括文档、交互式教程、自学课程和支持入口。

- TiDB Cloud 控制台现支持暗黑模式，提供更舒适、护眼的体验。可在左侧导航栏底部切换明暗模式。

## 2023 年 6 月 27 日

**通用变更**

- 新建 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群不再预置示例数据集。

## 2023 年 6 月 20 日

**通用变更**

- 新建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2) 升级至 [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3)。

## 2023 年 6 月 13 日

**通用变更**

- 支持使用 changefeed 将数据流式写入 Amazon S3。

    实现 TiDB Cloud 与 Amazon S3 的无缝集成，支持将 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据实时捕获并复制到 Amazon S3，确保下游应用和分析系统获取最新数据。

    详细信息参见 [流式写入云存储](/tidb-cloud/changefeed-sink-to-cloud-storage.md)。

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 16 vCPU TiKV 节点最大存储由 4 TiB 提升至 6 TiB。

    该增强提升了集群的数据存储能力，提高了扩展效率，满足数据增长需求。

    详细信息参见 [集群规格选择](/tidb-cloud/size-your-cluster.md)。

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [监控指标保留期](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 由 3 天延长至 7 天。

    保留期延长后，你可访问更多历史数据，有助于识别集群趋势和模式，提升决策和故障排查效率。

**控制台变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 页面发布全新原生 Web 架构。

    新架构下，**Key Visualizer** 页面导航更便捷，信息获取更直观高效，极大优化了 SQL 诊断体验。

## 2023 年 6 月 6 日

**通用变更**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群引入 Index Insight（beta），为慢查询提供索引优化建议，提升查询性能。

    Index Insight 可帮助你：

    - 查询性能提升：识别慢查询并推荐合适索引，加速查询、降低响应时间、提升用户体验。
    - 成本优化：通过索引优化减少额外计算资源消耗，更高效利用现有基础设施，降低运维成本。
    - 优化流程简化：自动识别并推荐索引，无需手动分析和猜测，节省时间和精力。
    - 应用效率提升：优化数据库性能后，应用可承载更大负载并支持更多并发用户，提升扩展能力。

  使用方法：进入 TiDB Cloud Dedicated 集群的 **Diagnosis** 页面，点击 **Index Insight BETA** 标签。

- 推出 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes)，无需注册或安装即可体验 TiDB 全功能的交互平台。

    TiDB Playground 提供一站式体验，包括扩展性、MySQL 兼容性、实时分析等特性。

    你可在受控环境下实时试用 TiDB 功能，便于理解 TiDB 特性。

    立即体验，请访问 [**TiDB Playground**](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes) 页面，选择要探索的功能并开始。

## 2023 年 6 月 5 日

**通用变更**

- 支持将 [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) 连接至 GitHub。

    [连接 Data App 至 GitHub](/tidb-cloud/data-service-manage-github-connection.md) 后，可将所有配置以 [代码文件](/tidb-cloud/data-service-app-config-files.md) 形式托管在 Github，实现与系统架构和 DevOps 流程的无缝集成。

    该功能提升 Data App 的 CI/CD 体验，支持：

    - 与 GitHub 自动部署 Data App 变更。
    - 在 GitHub 上配置 Data App 变更的 CI/CD 流程并进行版本控制。
    - 断开已连接的 GitHub 仓库。
    - 部署前审查接口变更。
    - 查看部署历史并在失败时采取措施。
    - 重新部署某次提交以回滚到早期部署。

  详细信息参见 [通过 GitHub 自动部署 Data App](/tidb-cloud/data-service-manage-github-connection.md)。

## 2023 年 6 月 2 日

**通用变更**

- 为简化和明晰产品命名，现已更新产品名称：

    - "TiDB Cloud Serverless Tier" 现称为 "TiDB Cloud Serverless"
    - "TiDB Cloud Dedicated Tier" 现称为 "TiDB Cloud Dedicated"
    - "TiDB On-Premises" 现称为 "TiDB Self-Managed"

    名称焕新，性能如一。你的体验始终是我们的首要任务。

## 2023 年 5 月 30 日

**通用变更**

- 增强 TiDB Cloud 数据迁移功能对增量数据迁移的支持。

    你现在可以指定 binlog 位置或全局事务标识（GTID），仅复制指定位置之后产生的增量数据到 TiDB Cloud。该增强为你提供更灵活的数据选择与复制能力，满足个性化需求。

    详情参见 [仅迁移 MySQL 兼容数据库的增量数据到 TiDB Cloud](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)。

- [**Events**](/tidb-cloud/tidb-cloud-events.md) 页面新增事件类型（`ImportData`）。

- TiDB Cloud 控制台移除 **Playground**。

    敬请期待全新独立 Playground，体验将进一步优化。

## 2023 年 5 月 23 日

**通用变更**

- 上传 CSV 文件至 TiDB 时，列名除英文和数字外，还可使用中文、日文等字符。特殊字符仅支持下划线（`_`）。

    详情参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

## 2023 年 5 月 16 日

**控制台变更**

- 为 Dedicated 和 Serverless 集群引入按功能分类的左侧导航入口。

    新导航更易发现功能入口，提升操作直观性。可在集群概览页体验新导航。

- Dedicated 集群 **Diagnosis** 页的以下两个标签页发布全新原生 Web 架构：

    - [Slow Query](/tidb-cloud/tune-performance.md#slow-query)
    - [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis)

    新架构下，页面导航更便捷，信息获取更高效，极大优化了 SQL 诊断体验。

## 2023 年 5 月 9 日

**通用变更**

- 支持为 2023 年 4 月 26 日后创建的 GCP 集群更改节点规格。

    你可根据需求升级高性能节点或降级低性能节点，灵活调整集群容量，优化成本。

    详细步骤参见 [更改节点规格](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram)。

- 支持导入压缩文件。可导入 `.gzip`、`.gz`、`.zstd`、`.zst`、`.snappy` 格式的 CSV 和 SQL 文件，提升导入效率并降低数据传输成本。

    详细信息参见 [从云存储导入 CSV 文件到 TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md) 及 [导入示例数据](/tidb-cloud/import-sample-data.md)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群支持基于 AWS PrivateLink 的私有端点连接，作为新的网络访问管理选项。

    私有端点连接不暴露数据于公网，支持 CIDR 重叠，便于网络管理。

    详细信息参见 [设置私有端点连接](/tidb-cloud/set-up-private-endpoint-connections.md)。

**控制台变更**

- [**Event**](/tidb-cloud/tidb-cloud-events.md) 页面新增 Dedicated 集群的备份、恢复、changefeed 操作事件类型。

    事件类型完整列表参见 [已记录事件](/tidb-cloud/tidb-cloud-events.md#logged-events)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [**SQL Diagnosis**](/tidb-cloud/tune-performance.md) 页面新增 **SQL Statement** 标签。

    **SQL Statement** 标签提供：

    - 全面展示 TiDB 执行的所有 SQL 语句，便于识别和诊断慢查询。
    - 展示每条 SQL 语句的详细信息，如查询时间、执行计划、数据库响应等，助力性能优化。
    - 友好的界面，支持排序、筛选、搜索，便于聚焦关键查询。

  详细信息参见 [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis)。

## 2023 年 5 月 6 日

**通用变更**

- 支持直接访问 TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群所在区域的 [Data Service endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint)。

    新建 Serverless 集群的 endpoint URL 现包含集群区域信息。通过 `<region>.data.tidbcloud.com` 可直接访问对应区域的 endpoint。

    也可通过 `data.tidbcloud.com` 全局域名访问，系统会自动重定向，但可能增加延迟。此方式下，curl 命令需加 `--location-trusted`。

    详细信息参见 [调用接口](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint)。

## 2023 年 4 月 25 日

**通用变更**

- 组织下前五个 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群可享免费额度：

    - 行存储：5 GiB
    - [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RUs

  2023 年 5 月 31 日前，Serverless 集群全免费。之后超出免费额度部分将计费。

    你可在集群 **Overview** 页的 **Usage This Month** 区域 [监控用量或提升额度](/tidb-cloud/manage-serverless-spend-limit.md)。超出免费额度后，读写操作将被限流，直至提升额度或新月重置。

    各资源（读、写、SQL CPU、网络出流量）RU 消耗、定价及限流说明参见 [TiDB Cloud Serverless Tier 价格详情](https://www.pingcap.com/tidb-cloud-starter-pricing-details)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群支持备份与恢复。

     详细信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore-serverless.md)。

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1) 升级至 [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2)。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持维护窗口功能，便于计划和管理维护任务。

    维护窗口为自动执行操作系统更新、安全补丁、基础设施升级等计划性维护的时间段，保障服务可靠性、安全性和性能。

    维护期间可能出现短暂连接中断或 QPS 波动，但集群可用，SQL 操作、数据导入、备份、恢复、迁移、同步等任务可正常运行。维护期间允许与禁止的操作见 [文档](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window)。

    我们将尽量减少维护频率。若有维护计划，默认开始时间为目标周三 03:00（以组织时区为准）。请关注维护计划，合理安排操作。

    - 每次维护窗口，TiDB Cloud 会发送三封邮件通知：维护前、开始时、结束后。
    - 你可在 **Maintenance** 页面修改维护开始时间或延后维护，降低影响。

  详细信息参见 [配置维护窗口](/tidb-cloud/configure-maintenance-window.md)。

- 优化 AWS 上新建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB 负载均衡，缩扩容时减少连接中断。

    - 扩容时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容时，支持自动迁移现有连接到可用 TiDB 节点。

  目前该功能适用于所有 AWS 上的 Dedicated Tier 集群。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面发布全新原生 Web 架构。

    新架构下，页面导航更便捷，信息获取更高效，极大优化了监控体验。

## 2023 年 4 月 18 日

**通用变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持扩缩 [数据迁移任务规格](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration)。

    你可通过扩容提升迁移性能，或缩容降低成本。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification)。

**控制台变更**

- 优化 [集群创建](https://tidbcloud.com/clusters/create-cluster) UI，提升易用性，支持一键创建和配置集群。

    新设计简洁明了，减少视觉干扰，指引清晰。点击 **Create** 后将直接跳转至集群概览页，无需等待集群创建完成。

    详细信息参见 [创建集群](/tidb-cloud/create-tidb-cluster.md)。

- **Billing** 页新增 **Discounts** 标签，展示组织所有者和账单管理员的折扣信息。

    详细信息参见 [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts)。

## 2023 年 4 月 11 日

**通用变更**

- 优化 AWS 上 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB 负载均衡，缩扩容时减少连接中断。

    - 扩容时，支持自动迁移现有连接到新 TiDB 节点。
    - 缩容时，支持自动迁移现有连接到可用 TiDB 节点。

  目前仅适用于 AWS `Oregon (us-west-2)` 区域的 Dedicated Tier 集群。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群支持 [New Relic](https://newrelic.com/) 集成。

    你可将 TiDB 集群的监控数据发送至 [New Relic](https://newrelic.com/)，实现应用与数据库的统一监控和分析，便于快速定位和解决问题。

    集成步骤及可用指标参见 [集成 New Relic](/tidb-cloud/monitor-new-relic-integration.md)。

- 为 Dedicated Tier 集群的 Prometheus 集成新增以下 [changefeed](/tidb-cloud/changefeed-overview.md) 指标：

    - `tidbcloud_changefeed_latency`
    - `tidbcloud_changefeed_replica_rows`

    已集成 Prometheus 的集群可实时监控 changefeed 性能和健康状况，并可基于这些指标创建告警。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面现采用 [节点级资源指标](/tidb-cloud/built-in-monitoring.md#server)。

    节点级指标可更准确反映资源消耗，便于了解实际服务使用情况。

    访问方法：进入集群 [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面，点击 **Metrics** 标签下的 **Server** 分类。

- 优化 [Billing](/tidb-cloud/tidb-cloud-billing.md#billing-details) 页，将账单项按 **Summary by Project** 和 **Summary by Service** 重组，信息更清晰。

## 2023 年 4 月 4 日

**通用变更**

- 为防止误报，从 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) 移除以下两项告警。因单节点临时离线或 OOM 不会显著影响集群健康。

    - 集群中至少有一个 TiDB 节点内存耗尽
    - 一个或多个集群节点离线

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 [Alerts](/tidb-cloud/monitor-built-in-alerting.md) 页面，展示每个集群的活跃和已关闭告警。

    **Alerts** 页面提供：

    - 直观友好的界面，无需订阅邮件即可查看集群告警。
    - 高级筛选，支持按严重性、状态等属性快速查找和排序，并可查看近 7 天历史，便于追踪。
    - **Edit Rule** 功能，支持自定义告警规则。

  详细信息参见 [TiDB Cloud 内置告警](/tidb-cloud/monitor-built-in-alerting.md)。

- TiDB Cloud 的帮助信息和操作整合至同一入口。

    现在可通过 [TiDB Cloud 控制台](https://tidbcloud.com/) 右下角 **?** 获取所有帮助信息及联系支持。

- 新增 [Getting Started](https://tidbcloud.com/getting-started) 页面，帮助你快速了解 TiDB Cloud。

    **Getting Started** 页面提供交互式教程、基础指南和实用链接。通过交互式教程可体验 TiDB Cloud 功能和 HTAP 能力，内置 Steam 游戏和 S&P 500 行业数据集。

    访问方法：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左侧导航栏点击 <svg ...></svg> **Getting Started**，或点击 **?** > **Interactive Tutorials**。

## 2023 年 3 月 29 日

**通用变更**

- [Data Service (beta)](/tidb-cloud/data-service-overview.md) 支持 Data App 更细粒度的访问控制。

    在 Data App 详情页，你可关联集群并为每个 API key 指定角色（`ReadOnly` 或 `ReadAndWrite`），实现集群级和权限级访问控制，灵活满足业务需求。

    详细信息参见 [管理关联集群](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) 和 [管理 API key](/tidb-cloud/data-service-api-key.md)。

## 2023 年 3 月 28 日

**通用变更**

- [changefeed](/tidb-cloud/changefeed-overview.md) 新增 2 RCUs、4 RCUs、8 RCUs 规格，支持在 [创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时选择。

    新规格下，数据同步成本较原需 16 RCUs 的场景最高可降 87.5%。

- 支持为 2023 年 3 月 28 日后创建的 [changefeed](/tidb-cloud/changefeed-overview.md) 扩缩规格。

    你可选择更高规格提升同步性能，或选择更低规格降低成本。

    详细信息参见 [扩缩 changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed)。

- 支持将 AWS 上 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的增量数据实时同步到同项目同区域的 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群。

    详细信息参见 [流向 TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据迁移功能新增支持 GCP 区域：`Singapore (asia-southeast1)` 和 `Oregon (us-west1)`。

    新增区域为数据迁移提供更多选择，靠近数据源可提升迁移速度和可靠性。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 [Slow Query](/tidb-cloud/tune-performance.md#slow-query) 页面发布全新原生 Web 架构。

    新架构下，页面导航更便捷，信息获取更高效，极大优化了 SQL 诊断体验。

## 2023 年 3 月 21 日

**通用变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群推出 [Data Service (beta)](https://tidbcloud.com/project/data-service)，支持通过自定义 API endpoint 以 HTTPS 请求访问数据。

    Data Service 可无缝集成 TiDB Cloud 与任何兼容 HTTPS 的应用或服务。常见场景包括：

    - 移动或 Web 应用直接访问 TiDB 数据库。
    - 使用无服务器边缘函数调用接口，避免连接池扩展问题。
    - 作为数据源集成数据可视化项目。
    - 在不支持 MySQL 接口的环境中访问数据库。

    此外，TiDB Cloud 提供 [Chat2Query API](/tidb-cloud/use-chat2query-api.md)，可通过 AI 生成并执行 SQL。

    访问方法：左侧导航栏进入 [**Data Service**](https://tidbcloud.com/project/data-service)。详细文档：

    - [Data Service 概览](/tidb-cloud/data-service-overview.md)
    - [Data Service 入门](/tidb-cloud/data-service-get-started.md)
    - [Chat2Query API 入门](/tidb-cloud/use-chat2query-api.md)

- 支持缩小 AWS 上 2022 年 12 月 31 日后创建的 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的 TiDB、TiKV、TiFlash 节点规格。

    可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 操作。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的数据迁移功能新增支持 GCP 区域：`Tokyo (asia-northeast1)`。

    便于将 GCP 上的 MySQL 兼容数据库迁移至 TiDB 集群。

    详细信息参见 [使用数据迁移迁移 MySQL 兼容数据库](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

**控制台变更**

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增 **Events** 页面，记录集群主要变更。

    可查看最近 7 天的事件历史，追踪触发时间、操作用户等信息，如集群暂停、规格变更等。

    详细信息参见 [TiDB Cloud 集群事件](/tidb-cloud/tidb-cloud-events.md)。

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 **Monitoring** 页面新增 **Database Status** 标签，展示以下数据库级指标：

    - QPS Per DB
    - Average Query Duration Per DB
    - Failed Queries Per DB

  便于监控单个数据库性能，数据驱动决策，提升应用性能。

  详细信息参见 [Serverless 集群监控指标](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 3 月 14 日

**通用变更**

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0) 升级至 [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1)。

- 支持在上传带表头的本地 CSV 文件时，修改 TiDB Cloud 创建目标表的列名。

    若上传的 CSV 文件表头不符合 TiDB Cloud 列名规范，系统会在对应列名旁显示警告图标。你可悬停查看提示并编辑列名。

    列名规范参见 [导入本地文件](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files)。

## 2023 年 3 月 7 日

**通用变更**

- 所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本由 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0) 升级至 [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)。

## 2023 年 2 月 28 日

**通用变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群新增 [SQL Diagnosis](/tidb-cloud/tune-performance.md) 功能。

    SQL Diagnosis 可深入洞察 SQL 运行状态，提升 SQL 性能调优效率。目前仅提供慢查询数据。

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
    - 导入前预览数据
    - 获取导入任务角色信息

  详细信息参见 [API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import)。

## 2023 年 2 月 22 日

**通用变更**

- 支持使用 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md) 跟踪组织成员在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的各类操作。

    仅 `Owner` 或 `Audit Admin` 角色可见，默认关闭。开启方法：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 右上角点击 <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging**。

    通过分析审计日志，可识别可疑操作，提升资源和数据安全。

    详细信息参见 [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 `ticloud cluster connect-info` 命令。

    该命令可获取集群连接字符串。需将 [ticloud 升级](/tidb-cloud/ticloud-upgrade.md) 至 v0.3.2 或更高版本。

## 2023 年 2 月 21 日

**通用变更**

- 支持使用 IAM 用户的 AWS access key 访问 Amazon S3 存储桶导入数据。

    该方式比 Role ARN 更简单。详细信息参见 [配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

- [监控指标保留期](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) 由 2 天延长：

    - Dedicated Tier 集群可查看近 7 天指标数据。
    - Serverless Tier 集群可查看近 3 天指标数据。

  保留期延长后，可访问更多历史数据，便于趋势分析和故障排查。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的 Monitoring 页面发布全新原生 Web 架构。

    新架构下，页面导航更便捷，信息获取更高效，极大优化了监控体验。

## 2023 年 2 月 17 日

**CLI 变更**

- [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) 新增 [`ticloud connect`](/tidb-cloud/ticloud-serverless-shell.md) 命令。

    该命令支持本地直接连接 TiDB Cloud 集群，无需安装 SQL 客户端。连接后可在 CLI 中执行 SQL 语句。

## 2023 年 2 月 14 日

**通用变更**

- 支持缩减 TiKV 和 TiFlash 节点数量，缩容 TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。

    可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-node-number) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 操作。

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群新增 **Monitoring** 页面。

    **Monitoring** 页面提供 SQL 每秒执行数、平均查询时长、失败查询数等多项指标，便于全面了解集群 SQL 性能。

    详细信息参见 [TiDB Cloud 内置监控](/tidb-cloud/built-in-monitoring.md)。

## 2023 年 2 月 2 日

**CLI 变更**

- 推出 TiDB Cloud CLI 客户端 [`ticloud`](/tidb-cloud/cli-reference.md)。

    使用 `ticloud`，你可通过命令行或自动化流程轻松管理 TiDB Cloud 资源。针对 GitHub Actions，已提供 [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli) 便捷集成。

    详细信息参见 [TiDB Cloud CLI 快速入门](/tidb-cloud/get-started-with-cli.md) 及 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## 2023 年 1 月 18 日

**通用变更**

* 支持使用 Microsoft 账号 [注册](https://tidbcloud.com/free-trial) TiDB Cloud。

## 2023 年 1 月 17 日

**通用变更**

- 新建 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群的默认 TiDB 版本由 [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) 升级至 [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)。

- 新注册用户将自动创建一个免费的 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群，便于快速开启数据探索。

- [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群新增支持 AWS 区域：`Seoul (ap-northeast-2)`。

    该区域支持以下功能：

    - [使用数据迁移迁移 MySQL 兼容数据库](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [通过 changefeed 将数据流向其他服务](/tidb-cloud/changefeed-overview.md)
    - [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日

**通用变更**

- 优化本地 CSV 文件导入 TiDB 的体验，提升 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的易用性。

    - 支持拖拽上传 CSV 文件至 **Import** 页面。
    - 创建导入任务时，若目标数据库或表不存在，可输入名称自动创建。新建表时可指定主键或选择多字段组成复合主键。
    - 导入完成后，可通过点击 **Explore your data by Chat2Query** 或任务列表中的目标表名，使用 [AI 驱动的 Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) 探索数据。

  详细信息参见 [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

**控制台变更**

- 每个集群新增 **Get Support** 选项，简化针对特定集群的支持请求流程。

    你可通过以下方式请求支持：

    - 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击集群行的 **...** 并选择 **Get Support**。
    - 在集群概览页右上角点击 **...** 并选择 **Get Support**。

## 2023 年 1 月 5 日

**控制台变更**

- [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群将 SQL Editor (beta) 重命名为 Chat2Query (beta)，并支持 AI 生成 SQL 查询。

  在 Chat2Query 中，你可让 AI 自动生成 SQL 查询，也可手动编写并运行 SQL，无需终端即可操作数据库。

  访问方法：在项目 [**Clusters**](https://tidbcloud.com/project/clusters) 页面点击集群名，再点击左侧导航栏的 **Chat2Query**。

## 2023 年 1 月 4 日

**通用变更**

- 支持通过增加 **Node Size(vCPU + RAM)** 扩容 AWS 上 2022 年 12 月 31 日后创建的 TiDB Cloud Dedicated 集群的 TiDB、TiKV、TiFlash 节点。

    可通过 [TiDB Cloud 控制台](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) 或 [TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster) 操作。

- [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的指标保留期延长至两天。

    你可访问近两天的指标数据，便于分析集群性能和趋势。

    该提升无需额外费用，可在集群 [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页的 **Diagnosis** 标签访问，有助于更高效地定位和监控集群健康。

- 支持为 Prometheus 集成自定义 Grafana dashboard JSON。

    已集成 Prometheus 的集群可导入预置 Grafana dashboard 并自定义，便于快速监控和问题定位。

    详细信息参见 [使用 Grafana GUI dashboard 可视化指标](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)。

- 所有 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#starter) 集群的默认 TiDB 版本由 [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0) 升级至 [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)。升级后已解决冷启动问题。

**控制台变更**

- 简化 [**Clusters**](https://tidbcloud.com/project/clusters) 页面和集群概览页展示：

    - 你可在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面点击集群名进入概览页并开始操作。
    - 集群概览页移除 **Connection** 和 **Import** 面板。你可点击右上角 **Connect** 获取连接信息，点击左侧导航栏 **Import** 导入数据。