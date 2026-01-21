---
title: Sink to MySQL (Beta)
summary: 本文档介绍如何使用 **Sink to MySQL** changefeed 将数据从 TiDB Cloud Essential 实时同步到 MySQL。内容包括限制、前置条件，以及创建 MySQL sink 进行数据复制的步骤。该过程涉及网络连接设置、将已有数据加载到 MySQL 以及在 MySQL 中创建目标表。完成前置条件后，用户即可创建 MySQL sink，将数据复制到 MySQL。
---

# Sink to MySQL (Beta)

本文档描述如何使用 **Sink to MySQL** changefeed，将数据从 TiDB Cloud Essential 实时同步到 MySQL。

## 限制

- 每个 TiDB Cloud Essential cluster 最多可创建 10 个 changefeed。
- 由于 TiDB Cloud Essential 使用 TiCDC 建立 changefeed，因此具有与 [TiCDC 的相同限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。

## 前置条件

在创建 changefeed 之前，你需要完成以下前置条件：

- 设置网络连接
- 导出并加载已有数据到 MySQL（可选）
- 如果不加载已有数据，仅希望同步增量数据到 MySQL，则需在 MySQL 中创建对应的目标表

### 网络

确保你的 TiDB Cloud Essential cluster 能够连接到 MySQL service。你可以选择以下任一连接方式：

- Private Link Connection：满足安全合规要求，并保证网络质量。
- Public Network：适用于快速搭建。

<SimpleTab>
<div label="Private Link Connection">

Private link 连接利用云服务商的 **Private Link** 技术，使你 VPC 内的资源可以通过私有 IP 地址连接到其他 VPC 的 service，就像这些 service 直接部署在你的 VPC 内一样。

你可以通过 private link 连接，将 TiDB Cloud Essential cluster 安全地连接到 MySQL service。如果你的 MySQL service 尚未支持 private link 连接，请参考 [Connect to Amazon RDS via a Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-aws-rds.md) 或 [Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-alicloud-rds.md) 创建连接。

</div>

<div label="Public Network">

如果你的 MySQL service 可以通过公网访问，你可以选择通过公网 IP 或域名连接到 MySQL。

</div>

</SimpleTab>

### 加载已有数据（可选）

**Sink to MySQL** 连接器只能将 TiDB Cloud Essential cluster 中某一时间点之后的增量数据同步到 MySQL。如果你的 TiDB Cloud Essential cluster 中已经存在数据，可以在启用 **Sink to MySQL** 之前，将已有数据导出并加载到 MySQL。

加载已有数据的步骤如下：

1. 将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 设置为大于以下两个操作总耗时的值，以避免这期间的历史数据被 TiDB GC 回收。

    - 导出和导入已有数据的时间
    - 创建 **Sink to MySQL** 的时间

    例如：

    ```sql
    SET GLOBAL tidb_gc_life_time = '72h';
    ```

2. 使用 [Export](/tidb-cloud/serverless-export.md) 功能从 TiDB Cloud Essential cluster 导出数据，然后使用社区工具如 [mydumper/myloader](https://centminmod.com/mydumper.html) 将数据加载到 MySQL service。

3. 记录 [Export](/tidb-cloud/serverless-export.md) 返回的 snapshot time。在配置 MySQL sink 时，将该时间戳作为起始位置。

### 在 MySQL 中创建目标表

如果你没有加载已有数据，需要在 MySQL 中手动创建对应的目标表，用于存储来自 TiDB 的增量数据。否则，数据将无法被同步。

## 创建 MySQL sink

完成前置条件后，你可以将数据同步到 MySQL。

1. 进入目标 TiDB Cloud Essential cluster 的概览页面，在左侧导航栏点击 **Data** > **Changefeed**。

2. 点击 **Create Changefeed**，并选择 **MySQL** 作为 **Destination**。

3. 在 **Connectivity Method** 中，选择连接 MySQL service 的方式。

    - 如果选择 **Public**，填写你的 MySQL endpoint。
    - 如果选择 **Private Link**，选择你在 [网络](#网络) 部分创建的 private link 连接，并填写 MySQL service 的 port。

4. 在 **Authentication** 中，填写 MySQL 用户名和密码，并为 MySQL service 配置 TLS 加密。目前，TiDB Cloud 不支持 MySQL TLS 连接的自签名证书。

5. 点击 **Next**，测试 TiDB 是否能成功连接到 MySQL：

    - 如果连接成功，将进入下一步配置。
    - 如果连接失败，会显示连接错误，你需要处理该错误。错误解决后，重新点击 **Next**。

6. 自定义 **Table Filter**，筛选你希望同步的表。规则语法详见 [table filter rules](https://docs.pingcap.com/tidb/stable/table-filter/#syntax)。

    - **Replication Scope**：你可以选择仅同步具有有效键的表，或同步所有选中的表。
    - **Filter Rules**：你可以在此列设置过滤规则。默认规则为 `*.*`，表示同步所有表。添加新规则并点击 **Apply** 后，TiDB Cloud 会查询 TiDB 中所有表，仅显示符合规则的表在 **Filter results** 下。
    - **Case Sensitive**：你可以设置过滤规则中数据库和表名的匹配是否大小写敏感。默认情况下，匹配不区分大小写。
    - **Filter results with valid keys**：此列显示具有有效键（包括主键或唯一索引）的表。
    - **Filter results without valid keys**：此列显示缺少主键或唯一键的表。这些表在同步时存在挑战，因为缺少唯一标识，可能导致下游处理重复事件时数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一键或主键，或通过添加过滤规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

7. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以在此列设置 event filter 应用到哪些表。规则语法与前述 **Table Filter** 区域相同。
    - **Event Filter**：你可以选择要忽略的事件类型。

8. 在 **Start Replication Position** 中，配置 MySQL sink 的起始位置。

    - 如果你已通过 Export [加载了已有数据](#加载已有数据可选)，请选择 **From Time**，并填写 Export 返回的 snapshot time，确保时区设置正确。
    - 如果上游 TiDB cluster 没有任何数据，选择 **Start replication from now on**。

9. 点击 **Next** 配置 changefeed。

    在 **Changefeed Name** 区域，指定 changefeed 的名称。

10. 检查配置。如果所有设置无误，点击 **Submit**。

    如果需要修改配置，点击 **Previous** 返回上一步配置页面。

11. 创建完成后，sink 状态会从 **Creating** 变为 **Running**。

    点击 changefeed 名称，可以查看更多 changefeed 详情，如 checkpoint、replication latency 及其他统计/指标（信息）。

12. 如果你已 [加载了已有数据](#加载已有数据可选) 并延长了 GC 时间，sink 创建完成后请将其恢复为原值（默认值为 `10m`）：

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```