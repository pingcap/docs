---
title: Sink to Apache Kafka (Beta)
summary: 本文档介绍如何创建 changefeed，将数据从 TiDB Cloud Essential 流式传输到 Apache Kafka。内容包括限制、前提条件，以及为 Apache Kafka 配置 changefeed 的步骤。该过程涉及设置网络连接、为 Kafka ACL 授权添加权限，以及配置 changefeed。
---

# Sink to Apache Kafka (Beta)

本文档描述如何创建 changefeed，将数据从 TiDB Cloud Essential 流式传输到 Apache Kafka。

## 限制

- 每个 TiDB Cloud Essential 集群最多可创建 10 个 changefeed。
- 目前，TiDB Cloud Essential 不支持上传自签名 TLS 证书以连接 Kafka broker。
- 由于 TiDB Cloud Essential 使用 TiCDC 建立 changefeed，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，则在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

## 前提条件

在创建 changefeed 将数据流式传输到 Apache Kafka 之前，你需要完成以下前提条件：

- 设置网络连接
- 为 Kafka ACL 授权添加权限

### 网络

确保你的 TiDB Cloud Essential 集群能够连接到 Apache Kafka 服务。你可以选择以下任一连接方法：

- Private Link Connection：满足安全合规要求并确保网络质量。
- Public Network：适用于快速搭建。

<SimpleTab>
<div label="Private Link Connection">

Private link 连接利用云服务商的 **Private Link** 技术，使你 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 中的服务，就像这些服务直接托管在你的 VPC 内一样。

TiDB Cloud Essential 目前仅支持自建 Kafka、Confluent Cloud Dedicated 集群和 Amazon MSK Provisioned 的 Private Link 连接。不支持与其他 Kafka SaaS 服务的直接集成。

根据你的 Kafka 部署和云服务商，设置 Private Link 连接的具体方法请参考以下指南：

- [通过 Private Link 连接到 AWS 上的 Confluent Cloud](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md)
- [通过 Private Link 连接到 AWS 上的自建 Kafka](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [通过 Private Link 连接到阿里云自建 Kafka](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)
- [通过 Private Link 连接到 Amazon MSK Provisioned](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)

</div>

<div label="Public Network">

如果你希望为 Apache Kafka 服务提供公网访问，需要为所有 Kafka broker 分配公网 IP 地址或域名。

不建议在生产环境中使用公网访问。

</div>
</SimpleTab>

### Kafka ACL 授权

为了让 TiDB Cloud Essential changefeed 能够将数据流式传输到 Apache Kafka 并自动创建 Kafka topic，请确保在 Kafka 中添加了以下权限：

- 为 Kafka 的 topic 资源类型添加 `Create` 和 `Write` 权限。
- 为 Kafka 的 cluster 资源类型添加 `DescribeConfigs` 权限。

例如，如果你的 Kafka 集群在 Confluent Cloud，请参考 Confluent 文档中的 [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) 和 [Adding ACLs](https://docs.confluent.io/platform/current/security/authorization/acls/manage-acls.html#add-acls) 获取更多信息。

## 第 1 步：打开 Apache Kafka 的 Changefeed 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com)。
2. 进入目标 TiDB Cloud Essential 集群的概览页面，然后在左侧导航栏点击 **Data** > **Changefeed**。
3. 点击 **Create Changefeed**，然后在 **Destination** 选择 **Kafka**。

## 第 2 步：配置 changefeed 目标

具体步骤根据你选择的连接方式有所不同。

<SimpleTab>
<div label="Public">

1. 在 **Connectivity Method** 选择 **Public**，并填写你的 Kafka broker endpoint。多个 endpoint 可用逗号 `,` 分隔。
2. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账户的 **user name** 和 **password** 进行认证。

3. 在 **Kafka Version** 选择 **Kafka v2** 或 **Kafka v3**，具体取决于你的 Kafka 版本。
4. 选择本 changefeed 的数据 **Compression** 类型。
5. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，则启用 **TLS Encryption** 选项。
6. 点击 **Next** 进行网络连接测试。测试通过后会进入下一页面。

</div>
<div label="Private Link">

1. 在 **Connectivity Method** 选择 **Private Link**。
2. 在 **Private Link Connection** 选择你在 [网络](#network) 部分创建的 private link 连接。确保 private link 连接的可用区与 Kafka 部署的可用区一致。
3. 填写你在 [网络](#network) 部分获得的 **Bootstrap Port**。如果你使用的是 Amazon MSK Provisioned 的 private link 连接，可以跳过此项。
4. 根据你的 Kafka 认证配置，选择 **Authentication** 选项。

    - 如果 Kafka 不需要认证，保持默认选项 **Disable**。
    - 如果 Kafka 需要认证，选择相应的认证类型，并填写 Kafka 账户的 **user name** 和 **password** 进行认证。

5. 在 **Kafka Version** 选择 **Kafka v2** 或 **Kafka v3**，具体取决于你的 Kafka 版本。
6. 选择本 changefeed 的数据 **Compression** 类型。
7. 如果你的 Kafka 启用了 TLS 加密，并希望使用 TLS 加密连接 Kafka，则启用 **TLS Encryption** 选项。
8. 如果你的 Kafka 需要 TLS SNI 验证，请填写 **TLS Server Name**，例如 `Confluent Cloud Dedicated clusters`。
9. 点击 **Next** 进行网络连接测试。测试通过后会进入下一页面。

</div>
</SimpleTab>

## 第 3 步：设置 changefeed

1. 自定义 **Table Filter**，筛选你希望同步的表。规则语法详见 [table filter 规则](https://docs.pingcap.com/tidb/stable/table-filter/#syntax)。

    - **Replication Scope**：你可以选择仅同步具有有效键的表，或同步所有选中的表。
    - **Filter Rules**：你可以在此列设置筛选规则。默认规则为 `*.*`，表示同步所有表。添加新规则并点击 **Apply** 后，TiDB Cloud 会查询 TiDB 中所有表，并仅显示符合规则的表在 **Filter results** 下。
    - **Case Sensitive**：你可以设置筛选规则中数据库和表名的匹配是否大小写敏感。默认情况下，匹配不区分大小写。
    - **Filter results with valid keys**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **Filter results without valid keys**：此列显示缺少主键或唯一键的表。这些表在同步时存在挑战，因为缺少唯一标识符可能导致下游处理重复事件时数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一键或主键，或者通过添加筛选规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以设置事件筛选器应用于哪些表。规则语法与前述 **Table Filter** 区域相同。
    - **Event Filter**：你可以选择需要忽略的事件。

3. 自定义 **Column Selector**，选择事件中的列，仅将这些列相关的数据变更发送到下游。

    - **Tables matching**：指定 column selector 应用到哪些表。未匹配任何规则的表将发送所有列。
    - **Column Selector**：指定匹配表中哪些列会被发送到下游。

    更多匹配规则说明，参见 [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors)。

4. 在 **Data Format** 区域，选择你期望的 Kafka 消息格式。

    - Avro 是一种紧凑、高效的二进制数据格式，支持丰富的数据结构，广泛应用于各类流式系统。详见 [Avro 数据格式](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol)。
    - Canal-JSON 是一种纯 JSON 文本格式，易于解析。详见 [Canal-JSON 数据格式](https://docs.pingcap.com/tidb/stable/ticdc-canal-json)。
    - Open Protocol 是一种行级数据变更通知协议，可为监控、缓存、全文索引、分析引擎以及不同数据库间主从复制等场景提供数据源。详见 [Open Protocol 数据格式](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol)。
    - Debezium 是一个捕获数据库变更的工具。它将每个捕获到的数据库变更转换为一个称为“事件”的消息，并将这些事件发送到 Kafka。详见 [Debezium 数据格式](https://docs.pingcap.com/tidb/stable/ticdc-debezium)。

5. 如果你希望在 Kafka 消息体中添加 TiDB-extension 字段，请启用 **TiDB Extension** 选项。

    有关 TiDB-extension 字段的更多信息，参见 [Avro 数据格式中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) 和 [Canal-JSON 数据格式中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field)。

6. 如果你选择 **Avro** 作为数据格式，页面会显示一些 Avro 专属配置。你可以按如下方式填写：

    - 在 **Decimal** 和 **Unsigned BigInt** 配置项中，指定 TiDB Cloud 如何在 Kafka 消息中处理 decimal 和 unsigned bigint 数据类型。
    - 在 **Schema Registry** 区域，填写你的 schema registry endpoint。如果启用 **HTTP Authentication**，请输入用户名和密码。

7. 在 **Topic Distribution** 区域，选择分发模式，并根据所选模式填写 topic 名称配置。

    如果你选择 **Avro** 作为数据格式，则只能在 **Distribution Mode** 下拉列表中选择 **Distribute changelogs by table to Kafka Topics** 模式。

    分发模式控制 changefeed 如何创建 Kafka topic：按表、按数据库，或所有变更日志共用一个 topic。

    - **Distribute changelogs by table to Kafka Topics**

        如果你希望 changefeed 为每个表创建一个专用 Kafka topic，请选择此模式。这样，某个表的所有 Kafka 消息都会发送到专用 topic。你可以通过设置 topic 前缀、数据库名与表名之间的分隔符以及后缀自定义 topic 名称。例如，分隔符设置为 `_` 时，topic 名称格式为 `<Prefix><DatabaseName>_<TableName><Suffix>`。

        对于非行事件（如 Create Schema Event）的变更日志，可以在 **Default Topic Name** 字段指定 topic 名称。changefeed 会相应创建 topic 收集此类变更日志。

    - **Distribute changelogs by database to Kafka Topics**

        如果你希望 changefeed 为每个数据库创建一个专用 Kafka topic，请选择此模式。这样，某个数据库的所有 Kafka 消息都会发送到专用 topic。你可以通过设置 topic 前缀和后缀自定义数据库的 topic 名称。

        对于非行事件（如 Resolved Ts Event）的变更日志，可以在 **Default Topic Name** 字段指定 topic 名称。changefeed 会相应创建 topic 收集此类变更日志。

    - **Send all changelogs to one specified Kafka Topic**

        如果你希望 changefeed 为所有变更日志创建一个 Kafka topic，请选择此模式。这样，changefeed 中的所有 Kafka 消息都会发送到同一个 Kafka topic。你可以在 **Topic Name** 字段定义 topic 名称。

8. 在 **Partition Distribution** 区域，你可以决定 Kafka 消息将被发送到哪个分区。你可以为所有表定义 **单一分区分发器**，也可以为不同表定义 **不同的分区分发器**。TiDB Cloud 提供四种分发器类型：

    - **Distribute changelogs by primary key or index value to Kafka partition**

        如果你希望 changefeed 将某个表的 Kafka 消息分发到不同分区，请选择此分发方式。行变更日志的主键或索引值将决定其被发送到哪个分区。若希望使用主键，可将 **Index Name** 字段留空。此分发方式可获得更好的分区均衡，并保证行级有序。

    - **Distribute changelogs by table to Kafka partition**

        如果你希望 changefeed 将某个表的 Kafka 消息发送到同一个 Kafka 分区，请选择此分发方式。行变更日志的表名将决定其被发送到哪个分区。此分发方式保证表级有序，但可能导致分区不均衡。

    - **Distribute changelogs by timestamp to Kafka partition**

        如果你希望 changefeed 随机将 Kafka 消息发送到不同分区，请选择此分发方式。行变更日志的 commitTs 将决定其被发送到哪个分区。此分发方式可获得更好的分区均衡，并保证每个分区内有序。但同一数据项的多次变更可能被发送到不同分区，不同消费者的消费进度可能不同，可能导致数据不一致。因此，消费者需要在消费前按 commitTs 对多个分区的数据进行排序。

    - **Distribute changelogs by column value to Kafka partition**

        如果你希望 changefeed 将某个表的 Kafka 消息分发到不同分区，请选择此分发方式。行变更日志中指定列的值将决定其被发送到哪个分区。此分发方式保证每个分区内有序，并确保具有相同列值的变更日志被发送到同一分区。

9. 在 **Topic Configuration** 区域，配置以下数值。changefeed 会根据这些数值自动创建 Kafka topic。

    - **Replication Factor**：控制每条 Kafka 消息会被复制到多少台 Kafka 服务器。有效取值范围为 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 到 Kafka broker 数量。
    - **Partition Number**：控制 topic 中分区的数量。有效取值范围为 `[1, 10 * Kafka broker 数量]`。

10. 在 **Split Event** 区域，选择是否将 `UPDATE` 事件切分为独立的 `DELETE` 和 `INSERT` 事件，或保持为原始 `UPDATE` 事件。详见 [为非 MySQL sink 切分主键或唯一键 UPDATE 事件](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

11. 点击 **Next**。

## 第 4 步：审核并创建 changefeed

1. 在 **Changefeed Name** 区域，为 changefeed 指定一个名称。
2. 审核你设置的所有 changefeed 配置。如需修改，点击 **Previous** 返回修改。
3. 如果所有配置无误，点击 **Submit** 创建 changefeed。