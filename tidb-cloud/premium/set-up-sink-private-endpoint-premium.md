---
title: 为 Changefeed 设置 Private Endpoint
summary: 了解如何为 changefeed 设置 private endpoint。
---

# 为 Changefeed 设置 Private Endpoint

本文档介绍如何在你的 {{{ .premium }}} 实例中为 changefeed 创建 private endpoint，从而使你能够通过私有连接安全地将数据流式传输到自托管 Kafka、Amazon MSK Provisioned 集群或 MySQL。

## 前提条件 {#prerequisites}

- 检查创建 private endpoint 的权限
- 设置网络连接

### 权限 {#permissions}

只有在你的组织中具有以下角色之一的用户才能为 changefeed 创建 private endpoint：

- `Organization Owner`
- 对应实例的 `Instance Manager`

有关 TiDB Cloud 中角色的更多信息，请参见[用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

### 网络 {#network}

Private endpoint 利用云服务提供商的 **Private Link** 技术，使你的 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 中一样。

> **注意：**
>
> - Private endpoint 是组织级别的资源，不绑定到特定的 {{{ .premium }}} 实例。在同一组织和同一区域内创建的 private endpoint 可以由多个连接到同一下游服务的实例共享，因此你无需为每个实例单独创建 endpoint。
> - 删除 {{{ .premium }}} 实例不会删除其 private endpoint。即使之前使用该 private endpoint 的实例仍然可用，如果 30 天内没有任何实例使用该 private endpoint，它也会被自动删除。你也可以在不再需要时手动删除 private endpoint。但是，当它仍被任何实例使用时，你无法删除它。

<SimpleTab>
<div label="AWS">

如果你的 changefeed 下游服务托管在 AWS 上，请根据连接类型收集以下信息：

- **AWS Endpoint Service**：你的下游服务的 endpoint service 名称，以及你的下游服务部署所在的可用区（AZ）。

    如果你的下游服务尚未提供 Private Endpoint Service，请按照[步骤 2. 将 Kafka 集群暴露为 Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)设置负载均衡器和 Private Link Service。

- **Amazon MSK Provisioned**：你的 Amazon MSK Provisioned 集群的 ARN。要了解如何为 changefeed 创建 Amazon MSK Provisioned 集群，请参见[通过 AWS PrivateLink 设置 Amazon MSK Provisioned 集群](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md)。

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

在 AWS 上，请根据下游服务选择连接类型：

- 如果你的下游服务通过 AWS endpoint service 暴露，例如自托管 Kafka 或 MySQL，请选择 **AWS Endpoint Service**。
- 如果你的下游服务是 Amazon MSK Provisioned 集群，请选择 **Amazon MSK Provisioned**。

**AWS Endpoint Service**

1. 在 **Networking** 页面中，点击 **AWS Private Endpoints for External Services** 部分中的 **Create Private Endpoint for External Services**。
2. 在显示的对话框中，为 private endpoint 输入一个名称。
3. 按照提示授权 TiDB Cloud 的 [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) 创建 endpoint。
4. 输入你在[网络](#network)部分中收集到的 **Endpoint Service Name**，然后选择 **AWS Endpoint Service** 作为连接类型。
5. 选择 **Number of AZs**。确保 AZ 的数量和 AZ ID 与你的 Kafka 部署匹配。
6. 如果此 private endpoint 是为 Apache Kafka 创建的，请选中 **Configure Advertised Listener for Kafka** 复选框。
7. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若要将 **TiDB Managed** 域名用于 advertised listener，请在 **Domain Pattern** 字段中输入一个唯一字符串，然后点击 **Generate**。TiDB Cloud 将为每个可用区生成带有子域名的 broker 地址。
    - 若要将你自己的 **Custom** 域名用于 advertised listener，请将域名类型切换为 **Custom**，在 **Custom Domain** 字段中输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

8. 点击 **Create** 以验证配置并创建 private endpoint。

**Amazon MSK Provisioned**

1. 在 **Networking** 页面中，点击 **AWS Private Endpoints for External Services** 部分中的 **Create Private Endpoint for External Services**.
2. 在显示的对话框中，为 private endpoint 输入一个名称，然后选择 **AWS MSK Provisioned** 作为连接类型。
3. 输入你的 Amazon MSK Provisioned 集群的 **MSK Cluster ARN**。要了解如何为 changefeed 创建 Amazon MSK Provisioned 集群，请参见[通过 AWS PrivateLink 设置 Amazon MSK Provisioned 集群](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md)。
4. 点击 **Create** 以验证配置并创建 private endpoint。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1. 在 **Networking** 页面中，点击 **Alibaba Cloud Private Endpoints for External Services** 部分中的 **Create Private Endpoint for External Services**。
2. 在 **Create Private Endpoint for External Services** 对话框中，为 private endpoint 输入一个名称。
3. 按照提示将 TiDB Cloud 的 Alibaba Cloud account ID 添加到你的 endpoint service 的 allowlist 中，以授予 TiDB Cloud VPC 访问权限。更多信息，请参见 [managing account IDs in the allowlist of an endpoint service](https://www.alibabacloud.com/help/en/privatelink/user-guide/add-and-manage-service-whitelists)。
4. 输入你在[网络](#network)部分中收集到的 **Endpoint Service Name**。
5. 选择 **Number of AZs**。确保 AZ 的数量和 AZ ID 与你的 Kafka 部署匹配。
6. 如果此 private endpoint 是为 Apache Kafka 创建的，请选中 **Configure Advertised Listener for Kafka** 复选框。
7. 使用 **TiDB Managed** 域名或 **Custom** 域名配置 Kafka 的 advertised listener。

    - 若要将 **TiDB Managed** 域名用于 advertised listener，请在 **Domain Pattern** 字段中输入一个唯一字符串，然后点击 **Generate**。TiDB 将为每个可用区生成带有子域名的 broker 地址。
    - 若要将你自己的 **Custom** 域名用于 advertised listener，请将域名类型切换为 **Custom**，在 **Custom Domain** 字段中输入根域名，点击 **Check**，然后为每个可用区指定 broker 子域名。

8. 点击 **Create** 以验证配置并创建 private endpoint。

</div>
</CustomContent>
</SimpleTab>