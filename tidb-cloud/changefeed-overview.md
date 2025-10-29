---
title: Changefeed
summary: TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。
---

# Changefeed

TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。目前，TiDB Cloud 支持将数据流式传输到 Apache Kafka、MySQL、TiDB Cloud 以及云存储。

> **Note:**
>
> - 目前，TiDB Cloud 每个集群最多只允许创建 100 个 changefeed。
> - 目前，TiDB Cloud 每个 changefeed 最多只允许配置 100 条表过滤规则。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群，changefeed 功能不可用。

## 查看 Changefeed 页面

要访问 changefeed 功能，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Changefeed**。此时会显示 changefeed 页面。

在 **Changefeed** 页面，你可以创建 changefeed，查看已有 changefeed 列表，并对已有 changefeed 进行操作（如扩缩容、暂停、恢复、编辑和删除 changefeed）。

## 创建 changefeed

要创建 changefeed，请参考以下教程：

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)
- [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
- [Sink to cloud storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## 查询 Changefeed RCU

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要查询的 changefeed，在 **Action** 列点击 **...** > **View**。
3. 你可以在页面的 **Specification** 区域看到当前 TiCDC Replication Capacity Units（RCU）。

## 扩缩容 changefeed

你可以通过扩容或缩容 changefeed 来更改 TiCDC Replication Capacity Units（RCU）。

> **Note:**
>
> - 若要为某个集群扩缩容 changefeed，请确保该集群的所有 changefeed 均为 2023 年 3 月 28 日之后创建。
> - 如果某个集群存在 2023 年 3 月 28 日之前创建的 changefeed，则该集群的现有 changefeed 及新建 changefeed 均不支持扩缩容。

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要扩缩容的 changefeed，在 **Action** 列点击 **...** > **Scale Up/Down**。
3. 选择新的规格。
4. 点击 **Submit**。

扩缩容过程大约需要 10 分钟（期间 changefeed 正常工作），切换到新规格大约需要几秒钟（期间 changefeed 会自动暂停并恢复）。

## 暂停或恢复 changefeed

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要暂停或恢复的 changefeed，在 **Action** 列点击 **...** > **Pause/Resume**。

## 编辑 changefeed

> **Note:**
>
> TiDB Cloud 目前仅支持在暂停状态下编辑 changefeed。

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要暂停的 changefeed，在 **Action** 列点击 **...** > **Pause**。
3. 当 changefeed 状态变为 `Paused` 后，点击 **...** > **Edit** 编辑对应的 changefeed。

    TiDB Cloud 默认会填充 changefeed 配置。你可以修改以下配置项：

    - Apache Kafka sink：所有配置项。
    - MySQL sink：**MySQL Connection**、**Table Filter** 和 **Event Filter**。
    - TiDB Cloud sink：**TiDB Cloud Connection**、**Table Filter** 和 **Event Filter**。
    - 云存储 sink：**Storage Endpoint**、**Table Filter** 和 **Event Filter**。

4. 编辑配置后，点击 **...** > **Resume** 恢复对应的 changefeed。

## 删除 changefeed

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要删除的 changefeed，在 **Action** 列点击 **...** > **Delete**。

## Changefeed 计费

如需了解 TiDB Cloud 中 changefeed 的计费方式，请参见 [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)。

## Changefeed 状态

复制任务的状态表示复制任务的运行状态。在运行过程中，复制任务可能因错误失败，或被手动暂停或恢复。这些操作会导致复制任务状态发生变化。

各状态说明如下：

- `CREATING`：复制任务正在创建中。
- `RUNNING`：复制任务正常运行，checkpoint-ts 正常推进。
- `EDITING`：复制任务正在编辑中。
- `PAUSING`：复制任务正在暂停中。
- `PAUSED`：复制任务已暂停。
- `RESUMING`：复制任务正在恢复中。
- `DELETING`：复制任务正在删除中。
- `DELETED`：复制任务已删除。
- `WARNING`：复制任务返回警告。由于某些可恢复的错误，复制无法继续。处于该状态的 changefeed 会持续尝试恢复，直到状态变为 `RUNNING`。该状态下的 changefeed 会阻塞 [GC 操作](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)。
- `FAILED`：复制任务失败。由于某些错误，复制任务无法恢复且无法自动修复。如果在增量数据的垃圾回收（GC）之前解决了问题，你可以手动恢复失败的 changefeed。增量数据的默认生存时间（TTL）为 24 小时，即 changefeed 中断后 24 小时内 GC 机制不会删除任何数据。