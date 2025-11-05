---
title: Sink to Apache Kafka
summary: 本文档介绍如何创建变更订阅（changefeed），将数据从 TiDB Cloud 流式同步到 Apache Kafka。内容包括限制、前置条件，以及为 Apache Kafka 配置变更订阅的步骤。该过程涉及网络连接设置、Kafka ACL 授权权限添加，以及变更订阅规范的配置。
---

# Sink to Apache Kafka

本文档介绍如何创建变更订阅（changefeed），将数据从 TiDB Cloud 流式同步到 Apache Kafka。

<CustomContent plan="dedicated">

> **Note:**
>
> - 要使用变更订阅功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高版本。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，不支持变更订阅功能。

</CustomContent>
<CustomContent plan="premium">

> **Note:**
>
> 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，不支持变更订阅功能。

</CustomContent>

## 限制

- 每个 TiDB Cloud <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>，最多可以创建 100 个变更订阅。
- 目前，TiDB Cloud 不支持上传自签名 TLS 证书以连接 Kafka broker。
- 由于 TiDB Cloud 使用 TiCDC 建立变更订阅，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

<CustomContent plan="dedicated">

- 如果你选择 Private Link 或 Private Service Connect 作为网络连接方式，请确保 TiDB 集群版本满足以下要求：

    - v6.5.x：需为 v6.5.9 或更高版本
    - v7.1.x：需为 v7.1.4 或更高版本
    - v7.5.x：需为 v7.5.1 或更高版本
    - v8.1.x：支持所有 v8.1.x 及更高版本
- 如果你希望使用 Debezium 作为数据格式，请确保 TiDB 集群版本为 v8.1.0 或更高版本。
- 关于 Kafka 消息的分区分布，请注意以下事项：

    - 如果你希望按主键或索引值分发变更日志到指定索引名的 Kafka 分区，请确保 TiDB 集群版本为 v7.5.0 或更高版本。
    - 如果你希望按列值分发变更日志到 Kafka 分区，请确保 TiDB 集群版本为 v7.5.0 或更高版本。

</CustomContent>

## 前置条件

在创建变更订阅将数据流式同步到 Apache Kafka 之前，你需要完成以下前置条件：

- 设置网络连接
- 添加 Kafka ACL 授权权限

### 网络

确保你的 TiDB <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 能够连接到 Apache Kafka 服务。你可以选择以下任一连接方式：

- Private Connect：适用于避免 VPC CIDR 冲突并满足安全合规要求，但会产生额外的 [Private Data Link Cost](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)。
- VPC Peering：作为一种性价比较高的选项，但需要管理潜在的 VPC CIDR 冲突和安全问题。
- Public IP：适用于快速搭建场景。

<CustomContent plan="dedicated">

<SimpleTab>
<div label="Private Connect">

Private Connect 利用云服务商的 **Private Link** 或 **Private Service Connect** 技术，使你 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 内一样。

TiDB Cloud 目前仅支持自建 Kafka 的 Private Connect，不支持与 MSK、Confluent Kafka 或其他 Kafka SaaS 服务的直接集成。若需通过 Private Connect 连接这些 Kafka SaaS 服务，你可以部署一个 [kafka-proxy](https://github.com/grepplabs/kafka-proxy) 作为中间层，将 Kafka 服务暴露为自建 Kafka。详细示例可参考 [Set Up Self-Hosted Kafka Private Service Connect by Kafka-proxy in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy)。该方案适用于所有 Kafka SaaS 服务。

- 如果你的 Apache Kafka 服务托管在 AWS，请按照 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 配置网络连接并获取 **Bootstrap Ports** 信息，然后按照 [Set Up Private Endpoint for Changefeeds](/tidb-cloud/set-up-sink-private-endpoint.md) 创建私有端点。
- 如果你的 Apache Kafka 服务托管在 Google Cloud，请按照 [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) 配置网络连接并获取 **Bootstrap Ports** 信息，然后按照 [Set Up Private Endpoint for Changefeeds](/tidb-cloud/set-up-sink-private-endpoint.md) 创建私有端点。
- 如果你的 Apache Kafka 服务托管在 Azure，请按照 [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md) 配置网络连接并获取 **Bootstrap Ports** 信息，然后按照 [Set Up Private Endpoint for Changefeeds](/tidb-cloud/set-up-sink-private-endpoint.md) 创建私有端点。

</div>
<div label="VPC Peering">

如果你的 Apache Kafka 服务位于没有互联网访问的 AWS VPC，请按以下步骤操作：

1. 在 Apache Kafka 服务所在 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 Apache Kafka 服务关联的安全组的入站规则。

    你需要将 TiDB Cloud 集群所在区域的 CIDR 添加到入站规则中。该 CIDR 可在 **VPC Peering** 页面找到。这样可以允许 TiDB 集群的流量访问 Kafka broker。

3. 如果 Apache Kafka 的 URL 包含主机名，你需要允许 TiDB Cloud 能够解析 Apache Kafka broker 的 DNS 主机名。

    1. 按照 [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html) 的步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

如果你的 Apache Kafka 服务位于没有互联网访问的 Google Cloud VPC，请按以下步骤操作：

1. 在 Apache Kafka 服务所在 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 Apache Kafka 所在 VPC 的 ingress 防火墙规则。

    你需要将 TiDB Cloud 集群所在区域的 CIDR 添加到 ingress 防火墙规则中。该 CIDR 可在 **VPC Peering** 页面找到。这样可以允许 TiDB 集群的流量访问 Kafka broker。

</div>
<div label="Public IP">

如果你希望通过 Public IP 访问 Apache Kafka 服务，请为所有 Kafka broker 分配 Public IP 地址。

**不建议**在生产环境中使用 Public IP。

</div>
</SimpleTab>
</CustomContent>

<CustomContent plan="premium">

<SimpleTab>
<div label="Private Connect">

Private Connect 利用云服务商的 **Private Link** 或 **Private Service Connect** 技术，使你 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 内一样。

TiDB Cloud 目前仅支持自建 Kafka 的 Private Connect，不支持与 MSK、Confluent Kafka 或其他 Kafka SaaS 服务的直接集成。若需通过 Private Connect 连接这些 Kafka SaaS 服务，你可以部署一个 [kafka-proxy](https://github.com/grepplabs/kafka-proxy) 作为中间层，将 Kafka 服务暴露为自建 Kafka。

如果你的 Apache Kafka 服务托管在 AWS，请按照 [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) 配置网络连接并获取 **Bootstrap Ports** 信息，然后按照 [Set Up Private Endpoint for Changefeeds](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md) 创建私有端点。

</div>
<div label="Public IP">

如果你希望通过 Public IP 访问 Apache Kafka 服务，请为所有 Kafka broker 分配 Public IP 地址。

**不建议**在生产环境中使用 Public IP。

</div>

<div label="VPC Peering">

目前，TiDB Cloud Premium 实例的 VPC Peering 功能仅支持按需申请。若需申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。在 **Description** 字段填写“Apply for VPC Peering for TiDB Cloud Premium instance”，并点击 **Submit**。

</div>
</SimpleTab>
</CustomContent>

### Kafka ACL 授权

为了让 TiDB Cloud 变更订阅能够将数据流式同步到 Apache Kafka 并自动创建 Kafka topic，请确保在 Kafka 中添加以下权限：

- 为 topic 资源类型添加 `Create` 和 `Write` 权限。
- 为 cluster 资源类型添加 `DescribeConfigs` 权限。

例如，如果你的 Kafka 集群在 Confluent Cloud，可以参考 Confluent 文档中的 [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) 和 [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) 获取更多信息。

## 第 1 步：打开 Apache Kafka 的 Changefeed 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com)。
2. 进入目标 TiDB <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>的概览页面，在左侧导航栏点击 **Data** > **Changefeed**。
3. 点击 **Create Changefeed**，并选择 **Kafka** 作为 **Destination**。

## 第 2 步：配置变更订阅目标

具体步骤根据你选择的连接方式有所不同。

<SimpleTab>
<div label="VPC Peering or Public IP">

1. 在 **Connectivity Method** 选择 **VPC Peering** 或 **Public IP**，填写你的 Kafka broker 端点。多个端点可用英文逗号 `,` 分隔。
2. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账号的 **user name** 和 **password**。

3. 选择你的 **Kafka Version**。如果不确定，建议选择 **Kafka v2**。
4. 选择本次变更订阅的数据 **Compression** 类型。
5. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，请启用 **TLS Encryption** 选项。
6. 点击 **Next** 测试网络连接。测试通过后会进入下一页面。

</div>
<div label="Private Link (AWS)">

1. 在 **Connectivity Method** 选择 **Private Link**。
2. 在 **Private Endpoint** 选择你在 [网络](#network) 部分创建的私有端点。确保私有端点的 AZ 与 Kafka 部署的 AZ 匹配。
3. 填写你在 [网络](#network) 部分获取的 **Bootstrap Ports**。建议每个 AZ 至少设置一个端口。多个端口可用英文逗号 `,` 分隔。
4. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账号的 **user name** 和 **password**。
5. 选择你的 **Kafka Version**。如果不确定，建议选择 **Kafka v2**。
6. 选择本次变更订阅的数据 **Compression** 类型。
7. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，请启用 **TLS Encryption** 选项。
8. 点击 **Next** 测试网络连接。测试通过后会进入下一页面。
9. TiDB Cloud 会为 **Private Link** 创建端点，可能需要几分钟时间。
10. 端点创建完成后，登录你的云服务商控制台，接受连接请求。
11. 返回 [TiDB Cloud 控制台](https://tidbcloud.com) 确认你已接受连接请求。TiDB Cloud 会测试连接，测试通过后进入下一页面。

</div>

<CustomContent plan="dedicated">
<div label="Private Service Connect (Google Cloud)">

1. 在 **Connectivity Method** 选择 **Private Service Connect**。
2. 在 **Private Endpoint** 选择你在 [网络](#network) 部分创建的私有端点。
3. 填写你在 [网络](#network) 部分获取的 **Bootstrap Ports**。建议填写多个端口。多个端口可用英文逗号 `,` 分隔。
4. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账号的 **user name** 和 **password**。
5. 选择你的 **Kafka Version**。如果不确定，建议选择 **Kafka v2**。
6. 选择本次变更订阅的数据 **Compression** 类型。
7. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，请启用 **TLS Encryption** 选项。
8. 点击 **Next** 测试网络连接。测试通过后会进入下一页面。
9. TiDB Cloud 会为 **Private Service Connect** 创建端点，可能需要几分钟时间。
10. 端点创建完成后，登录你的云服务商控制台，接受连接请求。
11. 返回 [TiDB Cloud 控制台](https://tidbcloud.com) 确认你已接受连接请求。TiDB Cloud 会测试连接，测试通过后进入下一页面。

</div>
</CustomContent>

<CustomContent plan="dedicated">
<div label="Private Link (Azure)">

1. 在 **Connectivity Method** 选择 **Private Link**。
2. 在 **Private Endpoint** 选择你在 [网络](#network) 部分创建的私有端点。
3. 填写你在 [网络](#network) 部分获取的 **Bootstrap Ports**。建议每个 AZ 至少设置一个端口。多个端口可用英文逗号 `,` 分隔。
4. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账号的 **user name** 和 **password**。
5. 选择你的 **Kafka Version**。如果不确定，建议选择 **Kafka v2**。
6. 选择本次变更订阅的数据 **Compression** 类型。
7. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，请启用 **TLS Encryption** 选项。
8. 点击 **Next** 测试网络连接。测试通过后会进入下一页面。
9. TiDB Cloud 会为 **Private Link** 创建端点，可能需要几分钟时间。
10. 端点创建完成后，登录 [Azure portal](https://portal.azure.com/) 并接受连接请求。
11. 返回 [TiDB Cloud 控制台](https://tidbcloud.com) 确认你已接受连接请求。TiDB Cloud 会测试连接，测试通过后进入下一页面。

</div>
</CustomContent>
</SimpleTab>

## 第 3 步：设置变更订阅

1. 自定义 **Table Filter**，筛选你希望同步的表。规则语法详见 [table filter rules](/table-filter.md)。

    - **Case Sensitive**：你可以设置过滤规则中数据库和表名的匹配是否区分大小写。默认情况下，匹配不区分大小写。
    - **Filter Rules**：你可以在此列设置过滤规则。默认有一条规则 `*.*`，表示同步所有表。添加新规则后，TiDB Cloud 会查询 TiDB 中所有表，并在右侧仅显示匹配规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：此列显示具有有效键（主键或唯一索引）的表。
    - **Tables without valid keys**：此列显示缺少主键或唯一键的表。这些表在同步时存在挑战，因为缺少唯一标识符可能导致下游处理重复事件时数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一键或主键，或通过过滤规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以设置事件过滤器应用于哪些表。规则语法与前述 **Table Filter** 区域相同。每个变更订阅最多可添加 10 条事件过滤规则。
    - **Event Filter**：你可以使用以下事件过滤器排除特定事件类型：
        - **Ignore event**：排除指定类型的事件。
        - **Ignore SQL**：排除匹配指定表达式的 DDL 事件。例如，`^drop` 排除以 `DROP` 开头的语句，`add column` 排除包含 `ADD COLUMN` 的语句。
        - **Ignore insert value expression**：排除满足特定条件的 `INSERT` 语句。例如，`id >= 100` 排除 `id` 大于等于 100 的 `INSERT` 语句。
        - **Ignore update new value expression**：排除新值满足指定条件的 `UPDATE` 语句。例如，`gender = 'male'` 排除更新后 `gender` 为 `male` 的变更。
        - **Ignore update old value expression**：排除旧值满足指定条件的 `UPDATE` 语句。例如，`age < 18` 排除旧值 `age` 小于 18 的变更。
        - **Ignore delete value expression**：排除满足指定条件的 `DELETE` 语句。例如，`name = 'john'` 排除 `name` 为 `'john'` 的删除操作。

3. 自定义 **Column Selector**，选择事件中的列，仅将这些列的数据变更发送到下游。

    - **Tables matching**：指定列选择器应用于哪些表。未匹配任何规则的表将发送所有列。
    - **Column Selector**：指定匹配表中哪些列会被发送到下游。

    更多匹配规则说明，参见 [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors)。

4. 在 **Data Format** 区域，选择你期望的 Kafka 消息格式。

    - Avro 是一种紧凑、高效的二进制数据格式，支持丰富的数据结构，广泛应用于各种流式系统。详见 [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol)。
    - Canal-JSON 是一种纯 JSON 文本格式，易于解析。详见 [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json)。
    - Open Protocol 是一种行级数据变更通知协议，为监控、缓存、全文索引、分析引擎及不同数据库间主从复制等场景提供数据源。详见 [Open Protocol data format](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol)。
    - Debezium 是一个捕获数据库变更的工具。它将每个捕获到的数据库变更转换为一个称为“事件”的消息，并发送到 Kafka。详见 [Debezium data format](https://docs.pingcap.com/tidb/stable/ticdc-debezium)。

5. 如果你希望在 Kafka 消息体中添加 TiDB 扩展字段，请启用 **TiDB Extension** 选项。

    有关 TiDB 扩展字段的更多信息，参见 [Avro 数据格式中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) 和 [Canal-JSON 数据格式中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)。

6. 如果你选择 **Avro** 作为数据格式，页面会显示一些 Avro 专属配置。你可以按如下方式填写：

    - 在 **Decimal** 和 **Unsigned BigInt** 配置项中，指定 TiDB Cloud 如何在 Kafka 消息中处理 decimal 和 unsigned bigint 数据类型。
    - 在 **Schema Registry** 区域，填写你的 schema registry 端点。如果启用 **HTTP Authentication**，会显示用户名和密码字段，并自动填充为 TiDB <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>的端点和密码。

7. 在 **Topic Distribution** 区域，选择分发模式，并根据模式填写 topic 名称配置。

    如果你选择 **Avro** 作为数据格式，则只能在 **Distribution Mode** 下拉列表中选择 **Distribute changelogs by table to Kafka Topics** 模式。

    分发模式控制变更订阅如何创建 Kafka topic，可以按表、按库，或将所有变更日志发送到一个 topic。

    - **Distribute changelogs by table to Kafka Topics**

        如果你希望为每个表创建一个专用的 Kafka topic，选择此模式。这样，某个表的所有 Kafka 消息都会发送到专用 topic。你可以通过设置 topic 前缀、数据库名与表名之间的分隔符和后缀自定义 topic 名称。例如，分隔符设置为 `_` 时，topic 名称格式为 `<Prefix><DatabaseName>_<TableName><Suffix>`。

        对于非行级事件（如 Create Schema Event）的变更日志，可以在 **Default Topic Name** 字段指定 topic 名称，变更订阅会相应创建 topic 收集这些变更日志。

    - **Distribute changelogs by database to Kafka Topics**

        如果你希望为每个数据库创建一个专用的 Kafka topic，选择此模式。这样，某个数据库的所有 Kafka 消息都会发送到专用 topic。你可以通过设置 topic 前缀和后缀自定义数据库的 topic 名称。

        对于非行级事件（如 Resolved Ts Event）的变更日志，可以在 **Default Topic Name** 字段指定 topic 名称，变更订阅会相应创建 topic 收集这些变更日志。

    - **Send all changelogs to one specified Kafka Topic**

        如果你希望所有变更日志都发送到同一个 Kafka topic，选择此模式。这样，变更订阅中的所有 Kafka 消息都会发送到一个 topic。你可以在 **Topic Name** 字段定义 topic 名称。

8. 在 **Partition Distribution** 区域，你可以决定 Kafka 消息发送到哪个分区。你可以为所有表定义 **单一分区分发器**，也可以为不同表定义 **不同的分区分发器**。TiDB Cloud 提供四种分发器类型：

    - **Distribute changelogs by primary key or index value to Kafka partition**

        如果你希望将某个表的 Kafka 消息分发到不同分区，选择此方式。行变更日志的主键或索引值决定其发送到哪个分区。该方式有助于分区均衡，并保证行级有序。

    - **Distribute changelogs by table to Kafka partition**

        如果你希望将某个表的 Kafka 消息全部发送到同一个分区，选择此方式。行变更日志的表名决定其发送到哪个分区。该方式保证表级有序，但可能导致分区不均衡。

    - **Distribute changelogs by timestamp to Kafka partition**

        如果你希望将 Kafka 消息随机分发到不同分区，选择此方式。行变更日志的 commitTs 决定其发送到哪个分区。该方式有助于分区均衡，并保证每个分区内有序。但同一数据项的多次变更可能被发送到不同分区，不同消费者的消费进度可能不同，可能导致数据不一致。因此，消费者需要在消费前按 commitTs 对多分区数据进行排序。

    - **Distribute changelogs by column value to Kafka partition**

        如果你希望将某个表的 Kafka 消息分发到不同分区，选择此方式。行变更日志的指定列值决定其发送到哪个分区。该方式保证每个分区内有序，并确保相同列值的变更日志发送到同一分区。

9. 在 **Topic Configuration** 区域，配置以下数值。变更订阅会根据这些数值自动创建 Kafka topic。

    - **Replication Factor**：控制每条 Kafka 消息在多少个 Kafka 服务器上进行副本。有效取值范围为 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 到 Kafka broker 数量。
    - **Partition Number**：控制 topic 的分区数量。有效取值范围为 `[1, 10 * Kafka broker 数量]`。

10. 在 **Split Event** 区域，选择是否将 `UPDATE` 事件拆分为独立的 `DELETE` 和 `INSERT` 事件，或保持原始 `UPDATE` 事件。详见 [Split primary or unique key UPDATE events for non-MySQL sinks](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

11. 点击 **Next**。

## 第 4 步：配置变更订阅规范

1. 在 **Changefeed Specification** 区域，指定本变更订阅使用的 <CustomContent plan="dedicated">Replication Capacity Units (RCUs)</CustomContent><CustomContent plan="premium">Changefeed Capacity Units (CCUs)</CustomContent> 数量。
2. 在 **Changefeed Name** 区域，指定变更订阅的名称。
3. 点击 **Next**，检查你设置的配置并进入下一页面。

## 第 5 步：检查配置

在此页面，你可以检查所有已设置的变更订阅配置。

如果发现有误，可以返回修改。如果没有问题，勾选底部的复选框，然后点击 **Create** 创建变更订阅。