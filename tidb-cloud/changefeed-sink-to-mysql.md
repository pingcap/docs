---
title: Sink to MySQL
summary: 本文档介绍如何使用 **Sink to MySQL** changefeed 将数据从 TiDB Cloud 实时同步到 MySQL。内容包括限制、前置条件，以及创建 MySQL sink 进行数据同步的步骤。该过程涉及网络连接配置、将已有数据导入 MySQL 以及在 MySQL 中创建目标表。完成前置条件后，用户即可创建 MySQL sink，将数据同步到 MySQL。
---

# Sink to MySQL

本文档介绍如何使用 **Sink to MySQL** changefeed，将数据从 TiDB Cloud 实时同步到 MySQL。

> **注意：**
>
> - 要使用 changefeed 功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高版本。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，changefeed 功能不可用。

## 限制

- 每个 TiDB Cloud 集群最多可创建 100 个 changefeed。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

## 前置条件

在创建 changefeed 之前，你需要完成以下前置条件：

- 配置网络连接
- 导出并加载已有数据到 MySQL（可选）
- 如果你不加载已有数据，仅希望同步增量数据到 MySQL，则需要在 MySQL 中手动创建对应的目标表

### 网络

确保你的 TiDB Cloud 集群能够连接到 MySQL 服务。

<SimpleTab>
<div label="VPC Peering">

如果你的 MySQL 服务位于没有公网访问权限的 AWS VPC 中，请按照以下步骤操作：

1. 在 MySQL 服务所在 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. 修改 MySQL 服务关联的安全组的入站规则。

    你必须将 [TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站规则中。这样可以允许来自 TiDB 集群的流量访问 MySQL 实例。

3. 如果 MySQL URL 包含主机名，你需要允许 TiDB Cloud 能够解析 MySQL 服务的 DNS 主机名。

    1. 按照 [为 VPC Peering 连接启用 DNS 解析](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns) 的步骤操作。
    2. 启用 **Accepter DNS resolution** 选项。

如果你的 MySQL 服务位于没有公网访问权限的 Google Cloud VPC 中，请按照以下步骤操作：

1. 如果你的 MySQL 服务是 Google Cloud SQL，必须在 Google Cloud SQL 实例关联的 VPC 中暴露一个 MySQL 端点。你可能需要使用 Google 提供的 [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy)。
2. 在 MySQL 服务所在 VPC 与 TiDB 集群之间 [建立 VPC Peering 连接](/tidb-cloud/set-up-vpc-peering-connections.md)。
3. 修改 MySQL 所在 VPC 的入站防火墙规则。

    你必须将 [TiDB Cloud 集群所在区域的 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) 添加到入站防火墙规则中。这样可以允许来自 TiDB Cloud 集群的流量访问 MySQL 端点。

</div>

<div label="Private Endpoint">

私有端点利用云服务商的 **Private Link** 或 **Private Service Connect** 技术，使你 VPC 中的资源能够通过私有 IP 地址连接到其他 VPC 的服务，就像这些服务直接托管在你的 VPC 内一样。

你可以通过私有端点安全地将 TiDB Cloud 集群连接到 MySQL 服务。如果你的 MySQL 服务尚未启用私有端点，请参考 [Set Up Private Endpoint for Changefeeds](/tidb-cloud/set-up-sink-private-endpoint.md) 创建私有端点。

</div>

</SimpleTab>

### 加载已有数据（可选）

**Sink to MySQL** 连接器只能将某一时间戳之后的增量数据从 TiDB 集群同步到 MySQL。如果你的 TiDB 集群中已经有数据，可以在启用 **Sink to MySQL** 之前，将已有数据导出并加载到 MySQL。

加载已有数据的步骤如下：

1. 将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 设置为大于以下两个操作总耗时的值，以避免这段时间内的历史数据被 TiDB 垃圾回收。

    - 导出和导入已有数据所需的时间
    - 创建 **Sink to MySQL** 所需的时间

    例如：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 从 TiDB 集群导出数据，然后使用社区工具如 [mydumper/myloader](https://centminmod.com/mydumper.html) 将数据加载到 MySQL 服务。

3. 从 [Dumpling 导出的文件](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files) 中，获取 MySQL sink 的起始位置（start position），该信息位于 metadata 文件中：

    以下是示例 metadata 文件的一部分。`SHOW MASTER STATUS` 的 `Pos` 即为已有数据的 TSO，也是 MySQL sink 的起始位置。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

### 在 MySQL 中创建目标表

如果你没有加载已有数据，需要在 MySQL 中手动创建对应的目标表，用于存储来自 TiDB 的增量数据。否则，数据将无法同步。

## 创建 MySQL sink

完成前置条件后，你可以将数据同步到 MySQL。

1. 进入目标 TiDB 集群的集群总览页面，在左侧导航栏点击 **Data** > **Changefeed**。

2. 点击 **Create Changefeed**，并选择 **MySQL** 作为 **Destination**。

3. 在 **Connectivity Method** 中，选择连接 MySQL 服务的方法。

    - 如果选择 **VPC Peering** 或 **Public IP**，请填写你的 MySQL 端点。
    - 如果选择 **Private Link**，请选择你在 [网络](#network) 部分创建的私有端点，并填写 MySQL 服务的端口。

4. 在 **Authentication** 中，填写 MySQL 服务的用户名和密码。

5. 点击 **Next** 测试 TiDB 是否能成功连接到 MySQL：

    - 如果连接成功，将进入下一步配置。
    - 如果连接失败，会显示连接错误，你需要排查并解决问题。解决后再次点击 **Next**。

6. 自定义 **Table Filter**，筛选你希望同步的表。规则语法详见 [table filter rules](/table-filter.md)。

    - **Case Sensitive**：你可以设置过滤规则中数据库和表名的匹配是否区分大小写。默认情况下，匹配不区分大小写。
    - **Filter Rules**：你可以在此列设置过滤规则。默认有一条规则 `*.*`，表示同步所有表。添加新规则后，TiDB Cloud 会查询 TiDB 中所有表，并在右侧仅显示匹配规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：此列显示具有有效键（主键或唯一索引）的表。
    - **Tables without valid keys**：此列显示缺少主键或唯一索引的表。这些表在同步时存在风险，因为下游处理重复事件时，缺少唯一标识可能导致数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一索引或主键，或者通过过滤规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

7. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以设置事件过滤器应用于哪些表。规则语法与前述 **Table Filter** 区域相同。每个 changefeed 最多可添加 10 条事件过滤规则。
    - **Event Filter**：你可以使用以下事件过滤器，从 changefeed 中排除特定事件：
        - **Ignore event**：排除指定类型的事件。
        - **Ignore SQL**：排除匹配指定表达式的 DDL 事件。例如，`^drop` 排除以 `DROP` 开头的语句，`add column` 排除包含 `ADD COLUMN` 的语句。
        - **Ignore insert value expression**：排除满足特定条件的 `INSERT` 语句。例如，`id >= 100` 排除 `id` 大于等于 100 的 `INSERT` 语句。
        - **Ignore update new value expression**：排除新值满足指定条件的 `UPDATE` 语句。例如，`gender = 'male'` 排除更新后 `gender` 为 `male` 的操作。
        - **Ignore update old value expression**：排除旧值满足指定条件的 `UPDATE` 语句。例如，`age < 18` 排除旧值 `age` 小于 18 的更新操作。
        - **Ignore delete value expression**：排除满足指定条件的 `DELETE` 语句。例如，`name = 'john'` 排除 `name` 为 `'john'` 的删除操作。

8. 在 **Start Replication Position** 中，配置 MySQL sink 的起始同步位置。

    - 如果你已通过 Dumpling [加载了已有数据](#load-existing-data-optional)，请选择 **Start replication from a specific TSO**，并填写从 Dumpling 导出 metadata 文件中获取的 TSO。
    - 如果上游 TiDB 集群没有任何数据，选择 **Start replication from now on**。
    - 其他情况下，你可以选择 **Start replication from a specific time**，自定义起始时间点。

9. 点击 **Next** 配置 changefeed 规格。

    - 在 **Changefeed Specification** 区域，指定 changefeed 使用的 Replication Capacity Units（RCU）数量。
    - 在 **Changefeed Name** 区域，指定 changefeed 的名称。

10. 点击 **Next**，检查 changefeed 配置。

    如果确认所有配置无误，勾选跨区域同步合规性，并点击 **Create**。

    如果需要修改配置，点击 **Previous** 返回上一步。

11. sink 很快会启动，你可以看到 sink 状态从 **Creating** 变为 **Running**。

    点击 changefeed 名称，可以查看更多 changefeed 详情，如 checkpoint、同步延迟及其他指标。

12. 如果你已通过 Dumpling [加载了已有数据](#load-existing-data-optional)，在 sink 创建完成后，需要将 GC 时间恢复为原值（默认值为 `10m`）：

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```