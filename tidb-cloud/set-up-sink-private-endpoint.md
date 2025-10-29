---
title: 为 Changefeed 设置私有端点
summary: 了解如何为 changefeed 设置私有端点。
---

# 为 Changefeed 设置私有端点

本文档介绍如何在你的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中创建 changefeed 的私有端点，使你能够通过私有连接安全地将数据流式传输到自托管的 Kafka 或 MySQL。

## 限制

在同一个 VPC 内，AWS 的每个 Private Endpoint Service、Google Cloud 的 Service Attachment 或 Azure 的 Private Link Service 最多可以有 5 个私有端点。如果超过此限制，请在创建新端点前移除未使用的私有端点。

## 前提条件

- 检查创建私有端点的权限
- 配置你的网络连接

### 权限

只有在你的组织中拥有以下任意角色的用户才能为 changefeed 创建私有端点：

- `Organization Owner`
- `Project Owner`
- `Project Data Access Read-Write`

关于 TiDB Cloud 中的角色详情，请参见 [用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

### 网络

私有端点利用云服务商的 **Private Link** 或 **Private Service Connect** 技术，使你 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 的服务，就像这些服务直接托管在你的 VPC 内一样。

<SimpleTab>
<div label="AWS">

如果你的 changefeed 下游服务托管在 AWS 上，请收集以下信息：

- 下游服务的 Private Endpoint Service 名称
- 下游服务部署的可用区（AZs）

如果下游服务没有可用的 Private Endpoint Service，请按照 [步骤 2. 将 Kafka 集群暴露为 Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) 设置负载均衡器和 Private Link Service。

</div>

<div label="Google Cloud">

如果你的 changefeed 下游服务托管在 Google Cloud 上，请收集下游服务的 Service Attachment 信息。

如果下游服务没有可用的 Service Attachment，请按照 [步骤 2. 将 Kafka-proxy 暴露为 Private Service Connect Service](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#step-2-expose-kafka-proxy-as-private-service-connect-service) 获取 Service Attachment 信息。

</div>

<div label="Azure">

如果你的 changefeed 下游服务托管在 Azure 上，请收集下游服务的 Private Link Service 别名。

如果下游服务没有可用的 Private Endpoint Service，请按照 [步骤 2. 将 Kafka 集群暴露为 Private Link Service](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) 设置负载均衡器和 Private Link Service。

</div>
</SimpleTab>

## 步骤 1. 打开集群的 Networking 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)。

2. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

3. 在左侧导航栏，点击 **Settings** > **Networking**。

## 步骤 2. 配置 changefeed 的私有端点

根据你的集群部署的云服务商，配置步骤有所不同。

<SimpleTab>
<div label="AWS">

1. 在 **Networking** 页面，点击 **Create Private Endpoint**，位于 **AWS Private Endpoint for Changefeed** 区域。
2. 在 **Create Private Endpoint for Changefeed** 对话框中，输入私有端点的名称。
3. 按照提示授权 TiDB Cloud 的 [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) 创建端点。
4. 输入你在 [网络](#network) 部分收集的 **Endpoint Service Name**。
5. 选择 **Number of AZs**。确保 AZ 数量和 AZ ID 与你的 Kafka 部署一致。
6. 如果该私有端点用于 Apache Kafka，请启用 **Advertised Listener for Kafka** 选项。
7. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若使用 **TiDB Managed** 域名作为 advertised listener，在 **Domain Pattern** 字段输入唯一字符串，然后点击 **Generate**。TiDB 会为每个可用区生成带有子域名的 broker 地址。
    - 若使用你自己的 **Custom** 域名作为 advertised listener，将域名类型切换为 **Custom**，在 **Custom Domain** 字段输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

8. 点击 **Create** 验证配置并创建私有端点。

</div>

<div label="Google Cloud">

1. 在 **Networking** 页面，点击 **Create Private Endpoint**，位于 **Google Cloud Private Endpoint for Changefeed** 区域。
2. 在 **Create Private Endpoint for Changefeed** 对话框中，输入私有端点的名称。
3. 按照提示授权 TiDB Cloud 的 [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) 预先批准端点创建，或在收到端点连接请求时手动批准。
4. 输入你在 [网络](#network) 部分收集的 **Service Attachment**。
5. 如果该私有端点用于 Apache Kafka，请启用 **Advertised Listener for Kafka** 选项。
6. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若使用 **TiDB Managed** 域名作为 advertised listener，在 **Domain Pattern** 字段输入唯一字符串，然后点击 **Generate**。TiDB 会为每个可用区生成带有子域名的 broker 地址。
    - 若使用你自己的 **Custom** 域名作为 advertised listener，将域名类型切换为 **Custom**，在 **Custom Domain** 字段输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

7. 点击 **Create** 验证配置并创建私有端点。

</div>

<div label="Azure">

1. 在 **Networking** 页面，点击 **Create Private Endpoint**，位于 **Azure Private Endpoint for Changefeed** 区域。
2. 在 **Create Private Endpoint for Changefeed** 对话框中，输入私有端点的名称。
3. 按照提示授权 TiDB Cloud 的 Azure 订阅，或允许任何拥有你别名的人在创建 changefeed 前访问你的 Private Link 服务。关于 Private Link 服务可见性的更多信息，请参见 Azure 文档中的 [Control service exposure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure)。
4. 输入你在 [网络](#network) 部分收集的 **Alias of Private Link Service**。
5. 如果该私有端点用于 Apache Kafka，请启用 **Advertised Listener for Kafka** 选项。
6. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若使用 **TiDB Managed** 域名作为 advertised listener，在 **Domain Pattern** 字段输入唯一字符串，然后点击 **Generate**。TiDB 会为每个可用区生成带有子域名的 broker 地址。
    - 若使用你自己的 **Custom** 域名作为 advertised listener，将域名类型切换为 **Custom**，在 **Custom Domain** 字段输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

7. 点击 **Create** 验证配置并创建私有端点。

</div>
</SimpleTab>