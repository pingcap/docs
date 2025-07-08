---
title: Sink to Apache Kafka
summary: 本文档说明如何创建 changefeed，将数据从 TiDB Cloud 流式传输到 Apache Kafka。内容包括限制条件、前提条件，以及配置 Apache Kafka 的 changefeed 步骤。流程涉及设置网络连接、添加 Kafka ACL 权限以及配置 changefeed 规范。
---

# Sink to Apache Kafka

本文档描述了如何创建 changefeed，将数据从 TiDB Cloud 流式传输到 Apache Kafka。

> **Note:**
>
> - 若要使用 changefeed 功能，确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高版本。
> - 对于 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，不支持使用 changefeed 功能。

## Restrictions

- 每个 TiDB Cloud 集群最多可以创建 100 个 changefeed。
- 目前，TiDB Cloud 不支持上传自签名 TLS 证书以连接 Kafka broker。
- 由于 TiDB Cloud 使用 TiCDC 来建立 changefeed，因此具有与 TiCDC 相同的 [restrictions](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待复制的表没有主键或非空唯一索引，复制过程中缺少唯一约束可能导致在某些重试场景中下游插入重复数据。
- 如果选择 Private Link 或 Private Service Connect 作为网络连接方式，请确保你的 TiDB 集群版本满足以下要求：

    - v6.5.x：版本 v6.5.9 或更高
    - v7.1.x：版本 v7.1.4 或更高
    - v7.5.x：版本 v7.5.1 或更高
    - v8.1.x：支持所有 v8.1.x 及更高版本
- 若要使用 Debezium 作为数据格式，请确保你的 TiDB 集群版本为 v8.1.0 或更高。
- 关于 Kafka 消息的分区分布，注意以下内容：

    - 若要按主键或索引值将变更日志分发到具有指定索引名的 Kafka 分区，确保你的 TiDB 集群版本为 v7.5.0 或更高。
    - 若要按列值将变更日志分发到 Kafka 分区，确保你的 TiDB 集群版本为 v7.5.0 或更高。

## Prerequisites

在创建将数据流式传输到 Apache Kafka 的 changefeed 之前，你需要完成以下前提条件：

- 设置网络连接
- 添加 Kafka ACL 权限

### Network

确保你的 TiDB 集群可以连接到 Apache Kafka 服务。你可以选择以下连接方式之一：

- Private Connect：适合避免 VPC CIDR 冲突和满足安全合规，但会产生额外的 [Private Data Link Cost](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。
- VPC Peering：作为一种成本效益较高的方案，但需要管理潜在的 VPC CIDR 冲突和安全考虑。
- Public IP：适合快速部署。

<SimpleTab>
<div label="Private Connect">

Private Connect 利用云提供商的 **Private Link** 或 **Private Service Connect** 技术，使你的 VPC 中的资源可以通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 内一样。

TiDB Cloud 目前仅支持自托管 Kafka 的 Private Connect，不支持与 MSK、Confluent Kafka 或其他 Kafka SaaS 服务的直接集成。若要通过 Private Connect 连接这些 Kafka SaaS 服务，可以部署 [kafka-proxy](https://github.com/grepplabs/kafka-proxy) 作为中介，将 Kafka 服务暴露为自托管 Kafka。详细示例请参见 [Set Up Self-Hosted Kafka Private Service Connect by Kafka-proxy in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy)。所有 Kafka SaaS 服务的设置类似。

- 如果你的 Apache Kafka 服务托管在 AWS，请参考 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)，确保网络连接配置正确。配置完成后，在 TiDB Cloud 控制台提供以下信息以创建 changefeed：

    - Kafka Advertised Listener Pattern 中的 ID
    - Endpoint Service Name
    - Bootstrap Ports

- 如果你的 Apache Kafka 服务托管在 Google Cloud，请参考 [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)，确保网络连接配置正确。配置完成后，在 TiDB Cloud 控制台提供以下信息以创建 changefeed：

    - Kafka Advertised Listener Pattern 中的 ID
    - Service Attachment
    - Bootstrap Ports

- 如果你的 Apache Kafka 服务托管在 Azure，请参考 [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md)，确保网络连接配置正确。配置完成后，在 TiDB Cloud 控制台提供以下信息以创建 changefeed：

    - Kafka Advertised Listener Pattern 中的 ID
    - Private Link Service 的别名
    - Bootstrap Ports

</div>
<div label="VPC Peering">

如果你的 Apache Kafka 服务在没有互联网访问权限的 AWS VPC 中，请按以下步骤操作：

1. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 Kafka 服务所在的 VPC 和你的 TiDB 集群。
2. 修改 Kafka 服务关联的安全组的入站规则。

    必须在入站规则中添加你的 TiDB Cloud 集群所在区域的 CIDR。该 CIDR 可在 **VPC Peering** 页面找到。这样可以确保流量从你的 TiDB 集群流向 Kafka broker。

3. 如果 Kafka URL 中包含主机名，还需允许 TiDB Cloud 解析 Kafka broker 的 DNS 主机名。

    1. 按照 [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html) 的步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

如果你的 Apache Kafka 服务在没有互联网访问权限的 Google Cloud VPC 中，请按以下步骤操作：

1. [设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，连接 Kafka 服务所在的 VPC 和你的 TiDB 集群。
2. 修改 Kafka 所在 VPC 的入站防火墙规则。

    必须在入站防火墙规则中添加你的 TiDB Cloud 集群所在区域的 CIDR。该 CIDR 可在 **VPC Peering** 页面找到。这样可以确保流量从你的 TiDB 集群流向 Kafka broker。

</div>
<div label="Public IP">

如果你希望为你的 Kafka 服务提供 Public IP 访问，请为所有 Kafka broker 分配 Public IP 地址。

**不建议**在生产环境中使用 Public IP。

</div>
</SimpleTab>

### Kafka ACL authorization

为了让 TiDB Cloud changefeed 能够向 Apache Kafka 流式传输数据并自动创建 Kafka 主题，请确保在 Kafka 中添加以下权限：

- 为主题资源类型添加 `Create` 和 `Write` 权限。
- 为集群资源类型添加 `DescribeConfigs` 权限。

例如，如果你的 Kafka 集群在 Confluent Cloud，可以参考 [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) 和 [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) 获取更多信息。

## Step 1. Open the Changefeed page for Apache Kafka

1. 登录到 [TiDB Cloud 控制台](https://tidbcloud.com)。
2. 进入目标 TiDB 集群的概览页面，然后在左侧导航栏点击 **Data** > **Changefeed**。
3. 点击 **Create Changefeed**，选择 **Kafka** 作为 **Destination**。

## Step 2. Configure the changefeed target

根据你选择的连接方式，步骤会有所不同。

<SimpleTab>
<div label="VPC Peering or Public IP">

1. 在 **Connectivity Method** 中选择 **VPC Peering** 或 **Public IP**，填写你的 Kafka broker 端点。多个端点用逗号 `,` 分隔。
2. 根据你的 Kafka 认证配置选择 **Authentication** 选项。

    - 如果你的 Kafka 不需要认证，保持默认的 **Disable**。
    - 如果需要认证，选择相应的认证类型，然后填写你的 Kafka 账号的 **user name** 和 **password**。

3. 选择你的 **Kafka Version**。如果不确定，选择 **Kafka v2**。
4. 选择本次 changefeed 的 **Compression** 类型。
5. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 连接，请开启 **TLS Encryption**。
6. 点击 **Next** 测试网络连接。测试成功后，将跳转到下一页。

</div>
<div label="Private Link (AWS)">

1. 在 **Connectivity Method** 中选择 **Private Link**。
2. 授权 [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) 让 TiDB Cloud 创建端点以访问你的端点服务。网页提示中会提供 AWS Principal 信息。
3. 确保你在 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 的 **Network** 部分，选择了相同的 **Number of AZs** 和 **AZ IDs of Kafka Deployment**，并在 **Kafka Advertised Listener Pattern** 填写了相同的唯一 ID。
4. 填写在 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 中配置的 **Endpoint Service Name**。
5. 填写 **Bootstrap Ports**，建议每个 AZ 设置至少一个端口，多个端口用逗号 `,` 分隔。
6. 根据你的 Kafka 认证配置选择 **Authentication** 选项。

    - 如果你的 Kafka 不需要认证，保持默认的 **Disable**。
    - 如果需要认证，选择相应的认证类型，然后填写 **user name** 和 **password**。

7. 选择你的 **Kafka Version**。如果不确定，选择 **Kafka v2**。
8. 选择本次 changefeed 的 **Compression** 类型。
9. 如果启用了 TLS 加密，开启 **TLS Encryption**。
10. 点击 **Next** 测试网络连接。测试成功后，跳转到下一页。
11. TiDB Cloud 会创建 **Private Link** 的端点，可能需要几分钟时间。
12. 端点创建完成后，登录云服务提供商控制台，接受连接请求。
13. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，确认已接受连接请求。TiDB Cloud 会测试连接，成功后进入下一步。

</div>
<div label="Private Service Connect (Google Cloud)">

1. 在 **Connectivity Method** 中选择 **Private Service Connect**。
2. 在 [Setup Self Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 中配置的 **Kafka Advertised Listener Pattern** 填写相同的唯一 ID。
3. 填写在 [Setup Self Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 中配置的 **Service Attachment**。
4. 填写 **Bootstrap Ports**，建议提供多个端口，用逗号 `,` 分隔。
5. 根据你的 Kafka 认证配置选择 **Authentication** 选项。

    - 如果你的 Kafka 不需要认证，保持默认的 **Disable**。
    - 如果需要认证，选择相应的认证类型，然后填写 **user name** 和 **password**。

6. 选择你的 **Kafka Version**。如果不确定，选择 **Kafka v2**。
7. 选择本次 changefeed 的 **Compression** 类型。
8.  如果启用了 TLS 加密，开启 **TLS Encryption**。
9.  点击 **Next** 测试网络连接。测试成功后，跳转到下一页。
10. TiDB Cloud 会创建 **Private Service Connect** 的端点，可能需要几分钟。
11. 端点创建完成后，登录云服务提供商控制台，接受连接请求。
12. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，确认已接受连接请求。TiDB Cloud 会测试连接，成功后进入下一步。

</div>
<div label="Private Link (Azure)">

1. 在 **Connectivity Method** 中选择 **Private Link**。
2. 在创建 changefeed 前，授权 TiDB Cloud 的 Azure 订阅或允许任何拥有你的别名的人访问你的 Private Link 服务。网页提示中的 **Reminders before proceeding** 提供 Azure 订阅信息。关于 Private Link 服务的可见性，详见 [Control service exposure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure)。
3. 确保在 [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md) 中填写的 **Kafka Advertised Listener Pattern** 中填写了相同的唯一 ID。
4. 填写在 [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md) 中配置的 **Alias of Private Link Service**。
5. 填写 **Bootstrap Ports**，建议每个 AZ 设置至少一个端口，多个端口用逗号 `,` 分隔。
6. 根据你的 Kafka 认证配置选择 **Authentication** 选项。

    - 如果你的 Kafka 不需要认证，保持默认的 **Disable**。
    - 如果需要认证，选择相应的认证类型，然后填写 **user name** 和 **password**。

7. 选择你的 **Kafka Version**。如果不确定，选择 **Kafka v2**。
8. 选择本次 changefeed 的 **Compression** 类型。
9. 如果启用了 TLS 加密，开启 **TLS Encryption**。
10. 点击 **Next** 测试网络连接。测试成功后，跳转到下一页。
11. TiDB Cloud 会创建 **Private Link** 的端点，可能需要几分钟时间。
12. 端点创建完成后，登录 [Azure portal](https://portal.azure.com/)，接受连接请求。
13. 返回 [TiDB Cloud 控制台](https://tidbcloud.com)，确认已接受连接请求。TiDB Cloud 会测试连接，成功后进入下一步。

</div>
</SimpleTab>

## Step 3. Set the changefeed

1. 自定义 **Table Filter**，筛选你想要复制的表。规则语法请参考 [table filter rules](/table-filter.md)。

    - **Filter Rules**：可以在此列设置过滤规则。默认规则为 `*.*`，表示复制所有表。添加新规则后，TiDB Cloud 会查询所有表，并只显示匹配规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：显示具有有效键（主键或唯一索引）的表。
    - **Tables without valid keys**：显示缺少主键或唯一键的表。这些表在复制时存在挑战，因为缺少唯一标识符可能导致下游处理重复事件时数据不一致。为确保数据一致性，建议在开始复制前为这些表添加唯一键或主键，或者通过过滤规则排除这些表，例如用规则 `"!test.tbl1"` 排除 `test.tbl1` 表。

2. 自定义 **Event Filter**，筛选你想要复制的事件。

    - **Tables matching**：设置事件过滤器应用的表。规则语法与前述 **Table Filter** 相同。每个 changefeed 最多可添加 10 条事件过滤规则。
    - **Ignored events**：设置事件过滤器排除的事件类型。

3. 自定义 **Column Selector**，选择事件中的列，只将相关列的数据变更发送到下游。

    - **Tables matching**：指定列选择器应用的表。未匹配任何规则的表，全部列都会被发送。
    - **Column Selector**：指定哪些列会被发送到下游。

    关于匹配规则的详细信息，参见 [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors)。

4. 在 **Data Format** 区域，选择你希望的 Kafka 消息格式。

    - Avro：一种紧凑、快速的二进制数据格式，支持丰富的数据结构，广泛应用于各种流系统。详见 [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol)。
    - Canal-JSON：一种纯 JSON 文本格式，易于解析。详见 [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json)。
    - Open Protocol：一种行级数据变更通知协议，提供监控、缓存、全文索引、分析引擎以及不同数据库之间的主从复制的数据源。详见 [Open Protocol data format](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol)。
    - Debezium：一种捕获数据库变更的工具，将每个捕获的变更转换为“事件”消息并发送到 Kafka。详见 [Debezium data format](https://docs.pingcap.com/tidb/stable/ticdc-debezium)。

5. 如果你想在 Kafka 消息中添加 TiDB-extension 字段，可以开启 **TiDB Extension** 选项。

    关于 TiDB-extension 字段的详细信息，参见 [TiDB extension fields in Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) 和 [TiDB extension fields in Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)。

6. 如果选择 **Avro** 作为数据格式，页面会显示一些 Avro 相关配置项。你可以按如下方式填写：

    - 在 **Decimal** 和 **Unsigned BigInt** 配置中，指定 TiDB Cloud 如何处理 Kafka 消息中的 decimal 和 unsigned bigint 类型。
    - 在 **Schema Registry** 区域，填写你的 schema registry 端点。如果启用 **HTTP Authentication**，会显示用户名和密码字段，并会自动填入你的 TiDB 集群端点和密码。

7. 在 **Topic Distribution** 区域，选择分发模式，并根据模式填写主题名配置。

    如果你选择 **Avro** 作为数据格式，**Distribution Mode** 下拉列表中只能选择 **Distribute changelogs by table to Kafka Topics** 模式。

    分发模式控制 changefeed 如何创建 Kafka 主题，可以按表、按数据库，或为所有变更日志创建一个主题。

    - **Distribute changelogs by table to Kafka Topics**

        若希望每个表对应一个专属 Kafka 主题，选择此模式。此时，某个表的所有 Kafka 消息会发送到专属的 Kafka 主题。可以通过设置主题前缀、数据库名与表名的分隔符以及后缀来自定义主题名。例如，若分隔符设为 `_`，则主题名格式为 `<Prefix><DatabaseName>_<TableName><Suffix>`。

        对于非行事件的变更日志（如 Create Schema Event），可以在 **Default Topic Name** 字段中指定主题名，changefeed 会据此创建主题。

    - **Distribute changelogs by database to Kafka Topics**

        若希望每个数据库对应一个专属 Kafka 主题，选择此模式。此时，某个数据库的所有 Kafka 消息会发送到专属的 Kafka 主题。可以通过设置主题前缀和后缀来自定义主题名。对于非行事件（如 Resolved Ts Event），也可以在 **Default Topic Name** 指定主题。

    - **Send all changelogs to one specified Kafka Topic**

        若希望所有变更日志都发送到同一个 Kafka 主题，选择此模式。可以在 **Topic Name** 字段中定义主题名。

8. 在 **Partition Distribution** 区域，决定 Kafka 消息的分区策略。可以定义 **所有表使用单一分区调度器**，或 **不同表使用不同分区调度器**。TiDB Cloud 提供四种调度器类型：

    - **Distribute changelogs by primary key or index value to Kafka partition**

        若希望将某个表的 Kafka 消息分发到不同分区，选择此方式。行变更的主键或索引值决定消息的分区。这种方式能实现更好的分区平衡和行级有序。

    - **Distribute changelogs by table to Kafka partition**

        若希望每个表的 Kafka 消息都在同一分区，选择此方式。行变更的表名决定消息的分区。此方式保证表内有序，但可能导致分区不均衡。

    - **Distribute changelogs by timestamp to Kafka partition**

        若希望随机将 Kafka 消息分发到不同分区，选择此方式。行变更的 commitTs 决定消息的分区。这种方式提供较好的分区平衡和每个分区的有序性，但可能导致同一数据项的多次变更被分发到不同分区，消费者的进度也会不同，可能引发数据不一致。消费者在消费前需要按 commitTs 排序。

    - **Distribute changelogs by column value to Kafka partition**

        若希望按列值将表的 Kafka 消息分发到不同分区，选择此方式。行变更的指定列值决定消息的分区。这种方式保证每个分区内的有序性，并确保相同列值的变更都在同一分区。

9. 在 **Topic Configuration** 区域，配置以下参数，changefeed 会根据这些参数自动创建 Kafka 主题。

    - **Replication Factor**：控制每个 Kafka 消息的复制数。有效值范围为 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 到 Kafka broker 数量。
    - **Partition Number**：控制主题中的分区数。有效值范围为 `[1, 10 * Kafka broker 数量]`。

10. 点击 **Next**。

## Step 4. Configure your changefeed specification

1. 在 **Changefeed Specification** 区域，指定 changefeed 使用的复制容量单位（RCUs）数量。
2. 在 **Changefeed Name** 区域，为 changefeed 指定一个名称。
3. 点击 **Next**，确认已设置的配置并进入下一页。

## Step 5. Review the configurations

在此页面，你可以查看所有已设置的 changefeed 配置。

如果发现任何错误，可以返回修正。确认无误后，在底部勾选复选框，点击 **Create** 即可创建 changefeed。