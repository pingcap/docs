---
title: Sink to TiDB Cloud
summary: 本文档介绍如何将数据从 TiDB Cloud Dedicated 集群实时同步到 TiDB Cloud Serverless 集群。该功能对 changefeed 和 region 的数量有限制。前置条件包括延长 tidb_gc_life_time、备份数据以及获取 TiDB Cloud sink 的起始位置。要创建 TiDB Cloud sink，请进入集群概览页面，建立连接，自定义表和事件过滤器，填写起始同步位点，指定 changefeed 规格，检查配置并创建 sink。最后，将 tidb_gc_life_time 恢复为原值。
---

# Sink to TiDB Cloud

本文档描述如何将数据从 TiDB Cloud Dedicated 集群实时同步到 TiDB Cloud Serverless 集群。

> **注意：**
>
> 要使用 Changefeed 功能，请确保你的 TiDB Cloud Dedicated 集群版本为 v6.1.3 或更高。

## 限制

- 每个 TiDB Cloud 集群最多可以创建 100 个 changefeed。
- 由于 TiDB Cloud 使用 TiCDC 建立 changefeed，因此具有与 [TiCDC 相同的限制](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)。
- 如果待同步的表没有主键或非空唯一索引，在某些重试场景下，由于缺少唯一约束，可能会导致下游插入重复数据。
- **Sink to TiDB Cloud** 功能仅对以下 AWS 区域且创建时间在 2022 年 11 月 9 日之后的 TiDB Cloud Dedicated 集群开放：

    - AWS Oregon (us-west-2)
    - AWS Frankfurt (eu-central-1)
    - AWS Singapore (ap-southeast-1)
    - AWS Tokyo (ap-northeast-1)

- 源 TiDB Cloud Dedicated 集群和目标 TiDB Cloud Serverless 集群必须在同一个项目且同一区域内。
- **Sink to TiDB Cloud** 功能仅支持通过私有终端节点进行网络连接。当你创建 changefeed 将数据从 TiDB Cloud Dedicated 集群同步到 TiDB Cloud Serverless 集群时，TiDB Cloud 会自动为两个集群建立私有终端节点连接。

## 前置条件

**Sink to TiDB Cloud** 连接器只能在某个 [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso) 之后，将 TiDB Cloud Dedicated 集群的增量数据同步到 TiDB Cloud Serverless 集群。

在创建 changefeed 之前，你需要先将源 TiDB Cloud Dedicated 集群的现有数据导出，并加载到目标 TiDB Cloud Serverless 集群。

1. 将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 设置为大于以下两个操作总耗时的值，以确保这段时间内的历史数据不会被 TiDB 垃圾回收。

    - 导出和导入现有数据所需的时间
    - 创建 **Sink to TiDB Cloud** 所需的时间

    例如：

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 从 TiDB Cloud Dedicated 集群导出数据，然后使用 [TiDB Cloud Serverless Import](/tidb-cloud/import-csv-files-serverless.md) 将数据加载到目标 TiDB Cloud Serverless 集群。

3. 从 [Dumpling 导出的文件](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files) 中，获取 TiDB Cloud sink 的起始位置（TSO），该信息位于 metadata 文件中：

    以下是一个示例 metadata 文件片段。`SHOW MASTER STATUS` 的 `Pos` 字段即为现有数据的 TSO，也是 TiDB Cloud sink 的起始位置。

    ```
    Started dump at: 2023-03-28 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2023-03-28 10:40:20
    ```

## 创建 TiDB Cloud sink

完成前置条件后，你可以将数据同步到目标 TiDB Cloud Serverless 集群。

1. 进入目标 TiDB 集群的集群概览页面，在左侧导航栏点击 **Data** > **Changefeed**。

2. 点击 **Create Changefeed**，并选择 **TiDB Cloud** 作为目标。

3. 在 **TiDB Cloud Connection** 区域，选择目标 TiDB Cloud Serverless 集群，并填写目标集群的用户名和密码。

4. 点击 **Next**，建立两个 TiDB 集群之间的连接，并测试 changefeed 是否可以成功连接：

    - 如果连接成功，将进入下一步配置。
    - 如果连接失败，会显示连接错误，你需要处理该错误。错误解决后，重新点击 **Next**。

5. 自定义 **Table Filter**，筛选你希望同步的表。规则语法可参考 [table filter rules](/table-filter.md)。

    - **Filter Rules**：你可以在此列设置过滤规则。默认有一条规则 `*.*`，表示同步所有表。添加新规则后，TiDB Cloud 会查询所有表，并在右侧仅显示匹配规则的表。最多可添加 100 条过滤规则。
    - **Tables with valid keys**：此列显示具有有效键（主键或唯一索引）的表。
    - **Tables without valid keys**：此列显示缺少主键或唯一键的表。这类表在同步时存在风险，因为缺少唯一标识，可能导致下游处理重复事件时数据不一致。为保证数据一致性，建议在同步前为这些表添加唯一键或主键，或者通过添加过滤规则排除这些表。例如，可以通过规则 `"!test.tbl1"` 排除表 `test.tbl1`。

6. 自定义 **Event Filter**，筛选你希望同步的事件。

    - **Tables matching**：你可以在此列设置事件过滤器应用到哪些表。规则语法与前述 **Table Filter** 区域相同。每个 changefeed 最多可添加 10 条事件过滤规则。
    - **Event Filter**：你可以使用以下事件过滤器从 changefeed 中排除特定事件：
        - **Ignore event**：排除指定类型的事件。
        - **Ignore SQL**：排除匹配指定表达式的 DDL 事件。例如，`^drop` 排除以 `DROP` 开头的语句，`add column` 排除包含 `ADD COLUMN` 的语句。
        - **Ignore insert value expression**：排除满足特定条件的 `INSERT` 语句。例如，`id >= 100` 排除 `id` 大于等于 100 的 `INSERT` 语句。
        - **Ignore update new value expression**：排除新值满足指定条件的 `UPDATE` 语句。例如，`gender = 'male'` 排除更新后 `gender` 为 `male` 的更新。
        - **Ignore update old value expression**：排除旧值满足指定条件的 `UPDATE` 语句。例如，`age < 18` 排除旧值 `age` 小于 18 的更新。
        - **Ignore delete value expression**：排除满足指定条件的 `DELETE` 语句。例如，`name = 'john'` 排除 `name` 为 `'john'` 的删除。

7. 在 **Start Replication Position** 区域，填写你从 Dumpling 导出 metadata 文件中获取的 TSO。

8. 点击 **Next**，配置 changefeed 规格。

    - 在 **Changefeed Specification** 区域，指定 changefeed 使用的 Replication Capacity Units (RCUs) 数量。
    - 在 **Changefeed Name** 区域，为 changefeed 指定一个名称。

9. 点击 **Next**，检查 changefeed 配置。

    如果确认所有配置无误，勾选跨区域同步合规性，并点击 **Create**。

    如果需要修改配置，点击 **Previous** 返回上一步。

10. sink 很快会启动，你可以看到 sink 状态从 **Creating** 变为 **Running**。

    点击 changefeed 名称，可以查看更多关于 changefeed 的详细信息，如 checkpoint、同步延迟及其他指标。

11. sink 创建完成后，将 [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) 恢复为原值（默认值为 `10m`）：

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```