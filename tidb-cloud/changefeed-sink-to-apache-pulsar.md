---
title: Sink to Apache Pulsar
summary: 本文档介绍如何创建变更订阅（changefeed），以将数据从 TiDB Cloud 流式传输到 Apache Pulsar。内容包括限制条件、前置条件，以及为 Apache Pulsar 配置变更订阅的步骤。该过程涉及网络连接的设置和变更订阅规范的配置。
---

# Sink to Apache Pulsar

本文档介绍如何创建变更订阅（changefeed），以将数据从 TiDB Cloud 流式传输到 Apache Pulsar。

> **Note:**
>
> - 若要使用变更订阅功能将数据同步到 Apache Pulsar，请确保你的 TiDB Cloud Dedicated 集群版本为 v7.5.1 或更高版本。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，变更订阅功能不可用。

## 限制条件

- 每个 TiDB Cloud 集群最多可创建 100 个变更订阅。
- 目前，TiDB Cloud 不支持上传自签名 TLS 证书以连接到 Pulsar broker。
- 由于 TiDB Cloud 使用 TiCDC 建立变更订阅，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，在某些重试场景下，由于缺乏唯一约束，可能会导致下游插入重复数据。
- 目前，TiCDC 不会自动创建 Pulsar topic。在向 topic 分发事件之前，请确保该 topic 已在 Pulsar 中存在。

## 前置条件

在创建变更订阅以将数据流式传输到 Apache Pulsar 之前，你需要完成以下前置条件：

- 设置网络连接
- 为 Pulsar ACL 授权添加权限
- 在 Apache Pulsar 中手动创建 topic，或在 Apache Pulsar broker 配置中启用 [`allowAutoTopicCreation`](https://pulsar.apache.org/reference/#/4.0.x/config/reference-configuration-broker?id=allowautotopiccreation)

### 网络

确保你的 TiDB 集群能够连接到 Apache Pulsar 服务。你可以选择以下任一连接方式：

- VPC Peering：需要进行网络规划，以避免潜在的 VPC CIDR 冲突，并考虑安全性问题。
- 公网 IP：适用于 Pulsar 以公网 IP 方式对外提供服务的场景。该方式不推荐用于生产环境，并需谨慎考虑安全性。

<SimpleTab>
<div label="VPC Peering">

如果你的 Apache Pulsar 服务部署在没有互联网访问权限的 AWS VPC 中，请按照以下步骤操作：

1. 在 Apache Pulsar 服务所在的 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 Apache Pulsar 服务关联的安全组的入站规则。

    你需要将 TiDB Cloud 集群所在区域的 CIDR 添加到入站规则中。该 CIDR 可在 **VPC Peering** 页面找到。这样可以允许来自 TiDB 集群到 Pulsar broker 的流量。

3. 如果 Apache Pulsar 的 URL 包含主机名，你需要允许 TiDB Cloud 解析 Apache Pulsar broker 的 DNS 主机名。

    1. 按照 [为 VPC Peering 连接启用 DNS 解析](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html) 的步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

如果你的 Apache Pulsar 服务部署在没有互联网访问权限的 Google Cloud VPC 中，请按照以下步骤操作：

1. 在 Apache Pulsar 服务所在的 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 Apache Pulsar 所在 VPC 的 ingress 防火墙规则。

    你需要将 TiDB Cloud 集群所在区域的 CIDR 添加到 ingress 防火墙规则中。该 CIDR 可在 **VPC Peering** 页面找到。这样可以允许来自 TiDB 集群到 Pulsar broker 的流量。

</div>
<div label="Public IP">

如果你希望通过公网 IP 访问 Apache Pulsar 服务，需要为所有 Pulsar broker 分配公网 IP 地址。

**不推荐**在生产环境中使用公网 IP。

</div>
</SimpleTab>

### 在 Apache Pulsar 中创建 topic

目前，TiCDC 不会自动创建 Pulsar topic。在创建变更订阅之前，你需要在 Pulsar 中创建所需的 topic。topic 的数量和命名方式取决于你选择的分发模式：

- 若希望所有 Pulsar 消息分发到单个 topic：只需创建一个你喜欢名称的 topic。
- 若希望每个表的 Pulsar 消息分发到专用 topic，则需为每个需要同步的表，按 `<Topic Prefix><DatabaseName><Separator><TableName><Topic Suffix>` 格式创建 topic。
- 若希望每个数据库的 Pulsar 消息分发到专用 topic，则需为每个需要同步的数据库，按 `<Topic Prefix><DatabaseName><Topic Suffix>` 格式创建 topic。

根据你的配置，可能还需要为非行事件（如 schema 变更）准备一个默认 topic。

更多信息请参见 Apache Pulsar 官方文档 [How to create a topic](https://pulsar.apache.org/docs/4.0.x/tutorials-topic/)。

## 第 1 步：打开 Apache Pulsar 的 Changefeed 页面

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com)。
2. 进入将作为变更订阅事件源的 TiDB 集群的集群概览页面，然后点击左侧导航栏的 **Data** > **Changefeed**。
3. 点击 **Create Changefeed**。

## 第 2 步：配置变更订阅目标

1. 在 **Destination** 区域，选择 **Pulsar**。
2. 在 **Connection** 区域，填写以下信息：

    - **Destination Protocol**：选择 **Pulsar** 或 **Pulsar+SSL**。
    - **Connectivity Method**：根据你计划如何连接到 Pulsar 端点，选择 **VPC Peering** 或 **Public**。
    - **Pulsar Broker**：填写你的 Pulsar broker 的端点。端口与域名或 IP 地址之间用冒号分隔，例如 `example.org:6650`。

3. 在 **Authentication** 区域，根据你的 Pulsar 认证配置选择 **Auth Type** 选项，并根据选择填写所需的凭证信息。
4. 可选：在 **Advanced Settings** 区域，配置其他高级设置：

    - **Compression**：为本变更订阅中的数据选择可选的压缩算法。
    - **Max Messages per Batch** 和 **Max Publish Delay**：指定发送到 Pulsar 的事件消息批量设置。**Max Messages per Batch** 设置每批最大消息数，**Max Publish Delay** 设置发送一批消息前的最大等待时间。
    - **Connection Timeout**：调整与 Pulsar 建立 TCP 连接的超时时间。
    - **Operation Timeout**：调整使用 TiCDC Pulsar 客户端发起操作的超时时间。
    - **Send Timeout**：调整 TiCDC Pulsar producer 发送消息的超时时间。

5. 点击 **Next** 测试网络连接。若测试通过，将进入下一步。

## 第 3 步：配置变更订阅同步内容

1. 自定义 **Table Filter**，筛选你希望同步的表。规则语法参见 [table filter rules](/table-filter.md)。

    - **Case Sensitive**：你可以设置过滤规则中数据库和表名的匹配是否区分大小写。默认情况下，匹配不区分大小写。
    - **Filter Rules**：你可以在此列设置过滤规则。默认有一条规则 `*.*`，表示同步所有表。添加新规则后，TiDB Cloud 会查询 TiDB 中的所有表，并在右侧框中仅显示符合规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **Tables without valid keys**：此列显示缺少主键或唯一键的表。这些表在同步过程中存在挑战，因为缺乏唯一标识符可能导致下游处理重复事件时数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一键或主键，或通过添加过滤规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

2. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以在此列设置事件过滤器应用于哪些表。规则语法与前述 **Table Filter** 区域相同。每个变更订阅最多可添加 10 条事件过滤规则。
    - **Event Filter**：你可以使用以下事件过滤器从变更订阅中排除特定事件：
        - **Ignore event**：排除指定类型的事件。
        - **Ignore SQL**：排除匹配指定表达式的 DDL 事件。例如，`^drop` 排除以 `DROP` 开头的语句，`add column` 排除包含 `ADD COLUMN` 的语句。
        - **Ignore insert value expression**：排除满足特定条件的 `INSERT` 语句。例如，`id >= 100` 排除 `id` 大于等于 100 的 `INSERT` 语句。
        - **Ignore update new value expression**：排除新值满足指定条件的 `UPDATE` 语句。例如，`gender = 'male'` 排除更新后 `gender` 为 `male` 的更新。
        - **Ignore update old value expression**：排除旧值满足指定条件的 `UPDATE` 语句。例如，`age < 18` 排除旧值 `age` 小于 18 的更新。
        - **Ignore delete value expression**：排除满足指定条件的 `DELETE` 语句。例如，`name = 'john'` 排除 `name` 为 `'john'` 的删除。

3. 在 **Start Replication Position** 区域，选择变更订阅开始向 Pulsar 同步数据的起点：

    - **Start replication from now on**：变更订阅将从当前时刻开始同步数据。
    - **Start replication from a specific TSO**：变更订阅将从指定的 [TSO](/tso.md) 开始同步数据。指定的 TSO 必须在 [垃圾回收安全点](/read-historical-data.md#how-tidb-manages-the-data-versions) 之内。
    - **Start replication from a specific time**：变更订阅将从指定的时间戳开始同步数据。指定的时间戳必须在垃圾回收安全点之内。

4. 在 **Data Format** 区域，选择你期望的 Pulsar 消息格式。

    - Canal-JSON 是一种纯 JSON 文本格式，易于解析。更多信息参见 [TiCDC Canal-JSON Protocol](https://docs.pingcap.com/tidb/stable/ticdc-canal-json/)。

    - 若需在 Pulsar 消息体中添加 TiDB 扩展字段，可启用 **TiDB Extension** 选项。更多信息参见 [TiCDC Canal-JSON Protocol 中的 TiDB 扩展字段](https://docs.pingcap.com/tidb/stable/ticdc-canal-json/#tidb-extension-field)。

5. 在 **Topic Distribution** 区域，选择分发模式，并根据所选模式填写 topic 名称配置。

    分发模式控制变更订阅如何将事件消息分发到 Pulsar topic，可以将所有消息发送到一个 topic，或按表、按数据库分别发送到不同 topic。

    > **Note:**
    >
    > 当你选择 Pulsar 作为下游时，变更订阅不会自动创建 topic。你必须提前创建所需的 topic。

    - **Send all changelogs to one specified Pulsar Topic**

        如果你希望变更订阅将所有消息发送到单个 Pulsar topic，请选择此模式。你可以在 **Topic Name** 字段中指定 topic 名称。

    - **Distribute changelogs by table to Pulsar Topics**

        如果你希望变更订阅将每个表的 Pulsar 消息发送到专用 Pulsar topic，请选择此模式。你可以通过设置 **Topic Prefix**、数据库名与表名之间的 **Separator** 以及 **Topic Suffix**，为表指定 topic 名称。例如，若分隔符设置为 `_`，则 Pulsar 消息将发送到名称为 `<Topic Prefix><DatabaseName>_<TableName><Topic Suffix>` 的 topic。你需要提前在 Pulsar 上创建这些 topic。

        对于非行事件（如 Create Schema Event）的变更日志，你可以在 **Default Topic Name** 字段中指定 topic 名称。变更订阅会将这些非行事件发送到该 topic 以收集相关变更日志。

    - **Distribute changelogs by database to Pulsar Topics**

        如果你希望变更订阅将每个数据库的 Pulsar 消息发送到专用 Pulsar topic，请选择此模式。你可以通过设置 **Topic Prefix** 和 **Topic Suffix**，为数据库指定 topic 名称。

        对于非行事件（如 Resolved Ts Event）的变更日志，你可以在 **Default Topic Name** 字段中指定 topic 名称。变更订阅会将这些非行事件发送到该 topic 以收集相关变更日志。

    由于 Pulsar 支持多租户，如果 **Pulsar Tenant** 和 **Pulsar Namespace** 与默认值不同，你也可以进行设置。

6. 在 **Partition Distribution** 区域，你可以决定 Pulsar 消息发送到哪个分区。你可以为所有表定义 **单一分区分发器**，也可以为不同表定义 **不同的分区分发器**。TiDB Cloud 提供四种规则选项，将变更事件分发到 Pulsar 分区：

    - **Primary key or unique index**

        如果你希望变更订阅将表的 Pulsar 消息分发到不同分区，请选择此分发方式。行变更日志的主键或索引值决定该变更日志发送到哪个分区。该方式可实现更好的分区均衡，并保证行级有序性。

    - **Table**

        如果你希望变更订阅将表的 Pulsar 消息发送到同一个 Pulsar 分区，请选择此分发方式。行变更日志的表名决定该变更日志发送到哪个分区。该方式保证表级有序性，但可能导致分区不均衡。

    - **Timestamp**

        如果你希望变更订阅根据时间戳将 Pulsar 消息分发到不同 Pulsar 分区，请选择此分发方式。行变更日志的 commitTs 决定该变更日志发送到哪个分区。该方式可实现更好的分区均衡，并保证每个分区内的有序性。但同一数据项的多次变更可能被发送到不同分区，不同消费者的消费进度可能不同，可能导致数据不一致。因此，消费者需要在消费前按 commitTs 对来自多个分区的数据进行排序。

    - **Column value**

        如果你希望变更订阅将表的 Pulsar 消息分发到不同分区，请选择此分发方式。行变更日志中指定的列值将决定该变更日志发送到哪个分区。该方式保证每个分区内的有序性，并确保具有相同列值的变更日志被发送到同一分区。

7. 在 **Split Event** 区域，选择是否将 `UPDATE` 事件拆分为独立的 `DELETE` 和 `INSERT` 事件，或保持为原始的 `UPDATE` 事件。更多信息参见 [为非 MySQL sink 拆分主键或唯一键 UPDATE 事件](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks)。

8. 点击 **Next**。

## 第 4 步：配置规范并审核

1. 在 **Specification and Name** 区域：

    - 指定该变更订阅的 [Replication Capacity Units (RCUs)](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md) 数量。
    - 输入变更订阅的名称。

2. 审核所有变更订阅配置。

    - 如果发现问题，可以返回上一步进行修改。
    - 如果没有问题，可以点击 **Submit** 创建变更订阅。