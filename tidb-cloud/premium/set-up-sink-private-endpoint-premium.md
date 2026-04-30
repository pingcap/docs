---
title: 为 Changefeed 设置 Private Endpoint
summary: 了解如何为 changefeed 设置 private endpoint。
---

# 为 Changefeed 设置 Private Endpoint

本文档介绍如何在你的 {{{ .premium }}} 实例中为 changefeed 创建 private endpoint，从而使你能够通过私有连接安全地将数据流式传输到自托管 Kafka 或 MySQL。

## 前提条件 {#prerequisites}

- 检查创建 private endpoint 的权限
- 设置网络连接

### 权限 {#permissions}

只有在你的组织中具有以下任一角色的用户才能为 changefeed 创建 private endpoint：

- `Organization Owner`
- 对应实例的 `Instance Manager`

有关 TiDB Cloud 中角色的更多信息，请参见[用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

### 网络 {#network}

Private endpoint 利用云服务提供商的 **Private Link** 技术，使你的 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 中一样。

<SimpleTab>
<div label="AWS">

如果你的 changefeed 下游服务托管在 AWS 上，请收集以下信息：

- 你的下游服务的 Private Endpoint Service 名称
- 你的下游服务部署所在的可用区（AZ）

如果你的下游服务尚未提供 Private Endpoint Service，请按照[步骤 2. 将 Kafka 集群暴露为 Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)设置负载均衡器和 Private Link Service。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

如果你的 changefeed 下游服务托管在 Alibaba Cloud 上，请收集以下信息：

- 你的下游服务的 Private Endpoint Service 名称
- 你的下游服务部署所在的可用区（AZ）

要授予 TiDB Cloud VPC 访问权限，你必须将 TiDB Cloud 的 Alibaba Cloud account ID 添加到你的 endpoint service 的 allowlist 中。

如果你的下游服务尚未提供 Private Endpoint Service，请按照[步骤 2. 将 Kafka 集群暴露为 Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)设置负载均衡器和 Private Link Service。

</div>
</CustomContent>

</SimpleTab>

## 步骤 1. 打开实例的 Networking 页面 {#step-1-open-the-networking-page-for-your-instance}

1. 登录 [TiDB Cloud console](https://tidbcloud.com/)。

2. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .premium }}} 实例的名称，进入其实例概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的组合框在组织和实例之间切换。

3. 在左侧导航栏中，点击 **Settings** > **Networking**。

## 步骤 2. 为 changefeed 配置 private endpoint {#step-2-configure-the-private-endpoint-for-changefeeds}

配置步骤因实例部署所在的云服务提供商而异。

<SimpleTab>
<div label="AWS">

1. 在 **Networking** 页面中，点击 **AWS Private Endpoint for Changefeed** 部分中的 **Create Private Endpoint**。
2. 在 **Create Private Endpoint for Changefeed** 对话框中，为 private endpoint 输入一个名称。
3. 按照提示授权 TiDB Cloud 的 [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) 创建 endpoint。
4. 输入你在[网络](#network)部分中收集到的 **Endpoint Service Name**。
5. 选择 **Number of AZs**。确保 AZ 的数量和 AZ ID 与你的 Kafka 部署匹配。
6. 如果此 private endpoint 是为 Apache Kafka 创建的，请启用 **Advertised Listener for Kafka** 选项。
7. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若要将 **TiDB Managed** 域名用于 advertised listener，请在 **Domain Pattern** 字段中输入一个唯一字符串，然后点击 **Generate**。TiDB 将为每个可用区生成带有子域名的 broker 地址。
    - 若要将你自己的 **Custom** 域名用于 advertised listener，请将域名类型切换为 **Custom**，在 **Custom Domain** 字段中输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

8. 点击 **Create** 以验证配置并创建 private endpoint。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1. 在 **Networking** 页面中，点击 **Alibaba Cloud Private Endpoint for Changefeed** 部分中的 **Create Private Endpoint**。
2. 在 **Create Private Endpoint for Changefeed** 对话框中，为 private endpoint 输入一个名称。
3. 按照提示将 TiDB Cloud 的 Alibaba Cloud account ID 添加到你的 endpoint service 的 allowlist 中，以授予 TiDB Cloud VPC 访问权限。更多信息，请参见 [managing account IDs in the allowlist of an endpoint service](https://www.alibabacloud.com/help/en/privatelink/user-guide/add-and-manage-service-whitelists)。
4. 输入你在[网络](#network)部分中收集到的 **Endpoint Service Name**。
5. 选择 **Number of AZs**。确保 AZ 的数量和 AZ ID 与你的 Kafka 部署匹配。
6. 如果此 private endpoint 是为 Apache Kafka 创建的，请启用 **Advertised Listener for Kafka** 选项。
7. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若要将 **TiDB Managed** 域名用于 advertised listener，请在 **Domain Pattern** 字段中输入一个唯一字符串，然后点击 **Generate**。TiDB 将为每个可用区生成带有子域名的 broker 地址。
    - 若要将你自己的 **Custom** 域名用于 advertised listener，请将域名类型切换为 **Custom**，在 **Custom Domain** 字段中输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

8. 点击 **Create** 以验证配置并创建 private endpoint。

</div>
</CustomContent>
</SimpleTab>